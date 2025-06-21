[![Validate CLI](https://github.com/openauthcert/tooling/actions/workflows/ci.yml/badge.svg)](https://github.com/openauthcert/tooling/actions/workflows/ci.yml)
![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)

# OpenAuthCert Tooling

This Python CLI provides tools to validate OpenAuthCert badge specifications and vendor entries.

## Usage

```bash
pip install -e .
python -m openauthcert_tooling validate-badge path/to/badge.json
```

## Requirements
- Python 3.8+
- check-jsonschema