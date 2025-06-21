import argparse
import sys
from .validate_badge import main as validate_badge_main
from .validate_vendor import main as validate_vendor_main

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OpenAuthCert Tooling CLI")
    subparsers = parser.add_subparsers(dest="command")

    badge_parser = subparsers.add_parser("validate-badge", help="Validate a badge JSON file")
    badge_parser.add_argument("file", help="Path to the badge JSON file")

    vendor_parser = subparsers.add_parser("validate-vendor", help="Validate a vendor JSON file")
    vendor_parser.add_argument("file", help="Path to the vendor JSON file")

    args = parser.parse_args(argv)

    if args.command == "validate-badge":
        return validate_badge_main([args.file])
    if args.command == "validate-vendor":
        return validate_vendor_main([args.file])
    parser.print_help()
    return 0

if __name__ == "__main__":  # pragma: no cover - manual execution
    sys.exit(main())
