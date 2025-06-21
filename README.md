[![Test Suite](https://github.com/openauthcert/tooling/actions/workflows/test.yml/badge.svg)](https://github.com/openauthcert/tooling/actions/workflows/test.yml)
![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)

# OpenAuthCert Tooling

This Python CLI provides utilities to validate OpenAuthCert badge specifications and vendor registry entries.

## Usage

Install in editable mode and run the provided commands:

```bash
pip install -e .[test]
validate-vendor path/to/vendor.json
python -m openauthcert_tooling validate-badge path/to/badge.json
```

## Exit Codes

- `0` - Validation succeeded.
- `1` - Validation failed or the schema could not be retrieved.

## Requirements

- Python 3.8+
- `check-jsonschema`
- `pytest` (for running the test suite)

