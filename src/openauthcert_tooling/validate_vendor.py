"""Validate vendor JSON files against the badge specification schema."""

import argparse
import subprocess
import sys
import tempfile
import urllib.request


SCHEMA_URL = (
    "https://raw.githubusercontent.com/openauthcert/"
    "badge-spec/main/specs/v1.0.0/badge-schema.json"
)


def validate_vendor(file_path: str) -> int:
    """Validate ``file_path`` against the published badge schema.

    Returns 0 on success and 1 on failure.
    """
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
