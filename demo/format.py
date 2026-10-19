"""Standalone educational skeleton of an A/L/I text exchange (not production spec)."""
from decimal import Decimal, ROUND_HALF_UP
import re
from pathlib import Path

FIELD_COUNTS = {"A": 20, "L": 14, "I": 3}
FILENAME = re.compile(r"^([ALI])(0[1-9]|1[0-2])([0-9]{2})\.txt$", re.I)


def safe_field(value: object) -> str:
    """For synthetic fixtures only: separator/newlines cannot occur inside one field."""
    return " ".join(str(value if value is not None else "").replace("=", " ").split())


def serialize(fields: list[object]) -> str:
    return "=".join(safe_field(value) for value in fields)


def to_kopecks(amount: str) -> str:
    return str((Decimal(amount) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def write_demo_file(path: Path, header: list[str], rows: list[list[str]]) -> None:
    match = FILENAME.fullmatch(path.name)
    if not match:
        raise ValueError(f"Not A/L/I MMYY filename: {path.name}")
    if len(header) != 6:
        raise ValueError("Synthetic demo header must contain 6 positions")
    for i, row in enumerate(rows, start=1):
        if len(row) != FIELD_COUNTS[match[1].upper()]:
            raise ValueError(f"Demo row {i}: wrong field count")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(("\r\n".join([serialize(header), *(serialize(row) for row in rows)]) + "\r\n").encode("cp1251"))


def validate_file(path: Path) -> list[str]:
    match = FILENAME.fullmatch(path.name)
    if not match:
        return [f"{path.name}: expected A/L/I + MMYY + .txt"]
    kind = match[1].upper()
    try:
        content = path.read_bytes().decode("cp1251", errors="strict")
    except (OSError, UnicodeError) as exc:
        return [f"{path.name}: cannot read cp1251: {exc}"]
    lines = content.splitlines()
    errors: list[str] = []
    if not lines:
        return [f"{path.name}: empty file"]
    if len(lines[0].split("=")) != 6:
        errors.append(f"{path.name}: header has {len(lines[0].split('='))} fields, expected 6")
    if len(lines) == 1:
        errors.append(f"{path.name}: no informational records")
    for line_no, line in enumerate(lines[1:], start=2):
        actual = len(line.split("="))
        if actual != FIELD_COUNTS[kind]:
            errors.append(f"{path.name}, line {line_no}: {actual} fields, expected {FIELD_COUNTS[kind]}")
    return errors


def validate_set(paths: list[Path]) -> list[str]:
    errors = [err for path in paths for err in validate_file(path)]
    names = [FILENAME.fullmatch(p.name) for p in paths]
    if all(names):
        suffixes = {m[2] + m[3] for m in names if m}
        if len(suffixes) > 1:
            errors.append("Input files refer to different MMYY periods")
    return errors
