import unittest
from page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_single_title(self):
        md = "# Heading one"
        self.assertEqual(extract_title(md), "Heading one")

    def test_no_title(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_multiple_titles_same_line(self):
        md = "# Heading one" + " # Heading two"

        with self.assertRaises(Exception):
            extract_title(md)

    def test_multiple_titles_different_lines(self):
        md = "# Heading one" + "\n# Heading two"

        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
