import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from openauthcert_tooling import validate_badge


def make_fake_schema(monkeypatch):
    def fake_urlretrieve(url, filename, *args, **kwargs):
        Path(filename).write_text("{}")
        return filename, None

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 0)

    monkeypatch.setattr(validate_badge.urllib.request, "urlretrieve", fake_urlretrieve)
    monkeypatch.setattr(validate_badge.subprocess, "run", fake_run)

    class DummyResponse:
        def __init__(self, status=200):
            self.status = status

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(validate_badge.urllib.request, "urlopen", lambda url: DummyResponse())



def test_badge_missing_fields(monkeypatch, tmp_path):
    make_fake_schema(monkeypatch)
    badge_file = tmp_path / "badge.json"
    badge_file.write_text("{}")
    assert validate_badge.main([str(badge_file)]) == 1


def test_badge_valid(monkeypatch, tmp_path):
    make_fake_schema(monkeypatch)
    badge_file = tmp_path / "badge.json"
    badge = {
        "auth_protocols": ["OIDC"],
        "docs_url": "https://example.com",
        "version": "1.0.0",
        "status": "certified",
    }
    badge_file.write_text(__import__("json").dumps(badge))
    assert validate_badge.main([str(badge_file)]) == 0
