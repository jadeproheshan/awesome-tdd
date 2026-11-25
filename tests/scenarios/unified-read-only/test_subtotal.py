import unittest

from subtotal import subtotal


class SubtotalTests(unittest.TestCase):
    def test_totals_prices(self):
        self.assertEqual(subtotal([2, 3]), 5)


if __name__ == "__main__":
    unittest.main()
