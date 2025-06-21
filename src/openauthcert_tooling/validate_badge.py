import argparse
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
from urllib.parse import urlparse

SCHEMA_URL = "https://raw.githubusercontent.com/openauthcert/badge-spec/main/schema/badge-schema.json"

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)

VALID_STATUSES = {"certified", "revoked", "expired"}
PROTOCOLS = {"OIDC", "SAML", "LDAP"}


def validate_badge_main(file_path: str) -> int:
    """Validate a badge JSON file against the specification."""
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as exc:  # noqa: BLE001 - print error for CLI users
        print(f"Invalid JSON file: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []

    protocols = data.get("auth_protocols") or []
    if not isinstance(protocols, list) or not any(p in PROTOCOLS for p in protocols):
        errors.append(
            "'auth_protocols' must contain at least one of OIDC, SAML, or LDAP"
        )

    docs_url = data.get("docs_url")
    parsed = urlparse(str(docs_url)) if docs_url else None
    if not parsed or parsed.scheme not in {"http", "https"} or not parsed.netloc:
        errors.append("'docs_url' must be a valid URL")
    else:
        try:
            with urllib.request.urlopen(docs_url) as resp:
                if resp.status >= 400:
                    errors.append("'docs_url' is not reachable")
        except Exception:  # noqa: BLE001 - network errors for CLI users
            errors.append("'docs_url' is not reachable")

    version = data.get("version")
    if not version or not isinstance(version, str) or not SEMVER_RE.match(version):
        errors.append("'version' must be a valid semantic version (MAJOR.MINOR.PATCH)")

    status = data.get("status")
    if status not in VALID_STATUSES:
        errors.append(
            "'status' must be one of: certified, revoked, expired"
        )

    if errors:
        for msg in errors:
            print(msg, file=sys.stderr)
        return 1

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_schema:
            urllib.request.urlretrieve(SCHEMA_URL, temp_schema.name)
            subprocess.run([
                "check-jsonschema",
                "--schemafile",
                temp_schema.name,
                file_path,
            ], check=True)
    except subprocess.CalledProcessError:
        return 1
    except Exception as e:  # noqa: BLE001 - print error for CLI users
        print(f"Error fetching or validating schema: {e}", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a badge JSON file")
    parser.add_argument("file", help="Path to the badge JSON file")
    args = parser.parse_args(argv)
    return validate_badge_main(args.file)


if __name__ == "__main__":  # pragma: no cover - manual execution
    sys.exit(main())
