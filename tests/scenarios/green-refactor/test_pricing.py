import unittest

from pricing import subtotal


class SubtotalTests(unittest.TestCase):
    def test_empty_prices_total_zero(self):
        self.assertEqual(subtotal([]), 0)

    def test_adds_prices(self):
        self.assertEqual(subtotal([2, 3]), 5)


if __name__ == "__main__":
    unittest.main()
