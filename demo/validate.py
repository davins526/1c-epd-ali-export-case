"""Run: python -m demo.validate demo/samples/A0426.txt ..."""
import argparse
from pathlib import Path
from .format import validate_set


def main():
    parser = argparse.ArgumentParser(description="Demo structural validator, not full EPD contract validator")
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    errors = validate_set(args.files)
    if errors:
        for err in errors:
            print("ERROR:", err)
        raise SystemExit(1)
    print("OK: demo structural validation passed")


if __name__ == "__main__":
    main()
