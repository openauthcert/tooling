"""Validate vendor JSON files against the badge specification schema."""

import argparse
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
from urllib.parse import urlparse


SCHEMA_URL = (
    "https://raw.githubusercontent.com/openauthcert/"
    "badge-spec/main/specs/v1.0.0/badge-schema.json"
)

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)


def validate_vendor(file_path: str) -> int:
    """Validate ``file_path`` against the published badge schema.

    Returns 0 on success and 1 on failure.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as exc:  # noqa: BLE001 - print error for CLI users
        print(f"Invalid JSON file: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []

    auth = data.get("auth", {}) if isinstance(data.get("auth"), dict) else {}
    if not any(auth.get(p) is True for p in ("oidc", "saml", "ldap")):
        errors.append(
            "At least one of 'auth.oidc', 'auth.saml', or 'auth.ldap' must be true"
        )

    doc_url = data.get("documentation")
    if not doc_url or not urlparse(str(doc_url)).scheme or not urlparse(str(doc_url)).netloc:
        errors.append("Field 'documentation' must be a valid URL")

    version = data.get("version")
    if not version or not isinstance(version, str) or not SEMVER_RE.match(version):
        errors.append("Field 'version' must be a valid semantic version (MAJOR.MINOR.PATCH)")

    if errors:
        for msg in errors:
            print(msg, file=sys.stderr)
        return 1

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_schema:
            urllib.request.urlretrieve(SCHEMA_URL, temp_schema.name)
            subprocess.run(
                ["check-jsonschema", "--schemafile", temp_schema.name, file_path],
                check=True,
            )
    except subprocess.CalledProcessError:
        return 1
    except Exception as exc:  # noqa: BLE001 - print error for CLI users
        print(f"Error fetching or validating schema: {exc}", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    """Command line entry point for ``validate-vendor``."""

    parser = argparse.ArgumentParser(description="Validate a vendor JSON file")
    parser.add_argument("file", help="Path to the vendor JSON file")
    args = parser.parse_args(argv)

    return validate_vendor(args.file)


if __name__ == "__main__":  # pragma: no cover - manual execution
    sys.exit(main())
