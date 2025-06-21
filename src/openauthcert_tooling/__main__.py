import argparse
from .validate_badge import validate_badge_main
from .validate_vendor import validate_vendor_main

def main():
    parser = argparse.ArgumentParser(description="OpenAuthCert Tooling CLI")
    subparsers = parser.add_subparsers(dest="command")

    badge_parser = subparsers.add_parser("validate-badge", help="Validate a badge JSON file")
    badge_parser.add_argument("file", help="Path to the badge JSON file")

    vendor_parser = subparsers.add_parser("validate-vendor", help="Validate a vendor JSON file")
    vendor_parser.add_argument("file", help="Path to the vendor JSON file")

    args = parser.parse_args()

    if args.command == "validate-badge":
        validate_badge_main(args.file)
    elif args.command == "validate-vendor":
        validate_vendor_main(args.file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
