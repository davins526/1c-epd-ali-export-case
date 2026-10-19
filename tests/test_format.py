import tempfile
import unittest
from pathlib import Path
from demo.format import safe_field, to_kopecks, validate_file, validate_set, write_demo_file


class ExportTests(unittest.TestCase):
    def test_sanitizing(self):
        self.assertEqual(safe_field("Тест=1\r\nновая"), "Тест 1 новая")

    def test_decimal_kopecks(self):
        self.assertEqual(to_kopecks("123.45"), "12345")
        self.assertEqual(to_kopecks("0.015"), "2")

    def test_empty_positions_and_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "A0426.txt"
            write_demo_file(p, ["ДЕМО", "", "", "", "", ""], [["ЛС-1", ""] + [""] * 18])
            self.assertIn(b"=", p.read_bytes())
            self.assertEqual(validate_file(p), [])
            self.assertEqual(p.read_bytes().decode("cp1251").splitlines()[1].count("="), 19)

    def test_invalid_count(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "I0426.txt"
            p.write_bytes("a=b=c=d=e=f\r\na=b\r\n".encode("cp1251"))
            self.assertIn("expected 3", " ".join(validate_file(p)))

    def test_different_period(self):
        with tempfile.TemporaryDirectory() as directory:
            p1 = Path(directory) / "A0426.txt"
            p2 = Path(directory) / "I0526.txt"
            write_demo_file(p1, [""] * 6, [[""] * 20])
            write_demo_file(p2, [""] * 6, [[""] * 3])
            self.assertIn("different MMYY", " ".join(validate_set([p1, p2])))


if __name__ == "__main__":
    unittest.main()
