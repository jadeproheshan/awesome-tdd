import unittest

from pricing import total_price


class TotalPriceTests(unittest.TestCase):
    def test_sums_prices(self):
        self.assertEqual(total_price([2, 3]), 5)


if __name__ == "__main__":
    unittest.main()
