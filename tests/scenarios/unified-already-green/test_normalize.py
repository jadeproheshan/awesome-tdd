import unittest

from normalize import normalize_label


class NormalizeLabelTests(unittest.TestCase):
    def test_strips_whitespace_and_lowercases(self):
        self.assertEqual(normalize_label(" Hello "), "hello")

    def test_blank_input_normalizes_to_empty_string(self):
        for value in ("", "   ", "\t\n\r "):
            with self.subTest(value=value):
                self.assertEqual(normalize_label(value), "")


if __name__ == "__main__":
    unittest.main()
