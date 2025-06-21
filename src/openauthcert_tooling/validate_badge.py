import subprocess
import sys
from pathlib import Path

def validate_badge_main(file_path):
    schema_path = Path(__file__).parent.parent / "schema" / "badge-schema.json"
    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)
    try:
        subprocess.run([
            "check-jsonschema",
            "--schemafile", str(schema_path),
            str(file_path)
        ], check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)