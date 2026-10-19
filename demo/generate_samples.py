"""Generate fake, non-customer, strictly illustrative sample files."""
from pathlib import Path
from .format import to_kopecks, write_demo_file


def main():
    target = Path(__file__).parent / "samples"
    header = ["DEMO", "Учебный пример", "00", "Тестовый регион", "0426", "20261019"]
    a = ["FAKE-0001", "Примеров Т. Т.", "ул. Учебная", "10А", "", "1"] + [""] * 14
    l = ["FAKE-0001", "DEMO-SERVICE", "2", "1", to_kopecks("123.45")] + [""] * 9
    i = ["FAKE-0001", "DEMO", "Учебное уведомление"]
    for kind, rows in (("A", [a]), ("L", [l]), ("I", [i])):
        write_demo_file(target / f"{kind}0426.txt", header, rows)
        print(target / f"{kind}0426.txt")


if __name__ == "__main__":
    main()
