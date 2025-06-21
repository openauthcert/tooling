import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from openauthcert_tooling import validate_vendor


def test_main_error(monkeypatch, tmp_path):
    vendor_file = tmp_path / "vendor.json"
    vendor_file.write_text("{}")

    def fake_urlretrieve(url, filename, *args, **kwargs):
        Path(filename).write_text("{}");
        return filename, None

    def fake_run(*args, **kwargs):
        raise subprocess.CalledProcessError(returncode=1, cmd=args[0])

    monkeypatch.setattr(validate_vendor.urllib.request, "urlretrieve", fake_urlretrieve)
    monkeypatch.setattr(validate_vendor.subprocess, "run", fake_run)

    assert validate_vendor.main([str(vendor_file)]) == 1
