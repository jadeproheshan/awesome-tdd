import unittest

from labels import normalize_label


class NormalizeLabelTests(unittest.TestCase):
    def test_trims_and_lowercases_label(self):
        self.assertEqual(normalize_label(" Hello "), "hello")

    def test_normalizes_whitespace_to_empty_string(self):
        self.assertEqual(normalize_label(" \t\n "), "")


if __name__ == "__main__":
    unittest.main()
