import subprocess
import sys
import tempfile
import urllib.request

def validate_badge_main(file_path):
    schema_url = "https://raw.githubusercontent.com/openauthcert/badge-spec/main/schema/badge-schema.json"
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_schema:
            urllib.request.urlretrieve(schema_url, temp_schema.name)
            subprocess.run([
                "check-jsonschema",
                "--schemafile", temp_schema.name,
                file_path
            ], check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)
    except Exception as e:
        print(f"Error fetching or validating schema: {e}", file=sys.stderr)
        sys.exit(1)
