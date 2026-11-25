"""Batch acceptance tests to review before implementing inventory behavior.

Run with: python3 -B -m unittest discover -s . -p 'test_*.py' -v
"""

import unittest

from inventory import Inventory


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()

    def test_unknown_products_have_zero_stock(self):
        self.assertEqual(self.inventory.stock("apple"), 0)
        self.assertEqual(self.inventory.stock("pear"), 0)
        self.assertEqual(self.inventory.stock("apple"), 0)

    def test_add_accumulates_positive_integer_quantities(self):
        self.inventory.add("apple", 1)
        self.assertEqual(self.inventory.stock("apple"), 1)
        self.inventory.add("apple", 4)
        self.assertEqual(self.inventory.stock("apple"), 5)

    def test_products_have_independent_stock(self):
        self.inventory.add("apple", 5)
        self.inventory.add("pear", 3)
        self.inventory.remove("apple", 2)
        self.assertEqual(self.inventory.stock("apple"), 3)
        self.assertEqual(self.inventory.stock("pear"), 3)
        self.assertEqual(self.inventory.stock("orange"), 0)

    def test_remove_decreases_stock_by_requested_quantity(self):
        self.inventory.add("apple", 7)
        self.inventory.remove("apple", 1)
        self.assertEqual(self.inventory.stock("apple"), 6)
        self.inventory.remove("apple", 2)
        self.assertEqual(self.inventory.stock("apple"), 4)

    def test_remove_exact_stock_leaves_zero_and_allows_restocking(self):
        self.inventory.add("apple", 3)
        self.inventory.remove("apple", 3)
        self.assertEqual(self.inventory.stock("apple"), 0)
        self.inventory.add("apple", 2)
        self.assertEqual(self.inventory.stock("apple"), 2)

    def test_insufficient_stock_is_rejected_without_changing_any_product(self):
        self.inventory.add("apple", 3)
        self.inventory.add("pear", 4)
        with self.assertRaises(ValueError):
            self.inventory.remove("apple", 4)
        self.assertEqual(self.inventory.stock("apple"), 3)
        self.assertEqual(self.inventory.stock("pear"), 4)
        # A rejected removal must not impair a subsequent valid operation.
        self.inventory.remove("apple", 2)
        self.assertEqual(self.inventory.stock("apple"), 1)

    def test_removing_from_unknown_product_is_rejected_and_keeps_zero(self):
        with self.assertRaises(ValueError):
            self.inventory.remove("missing", 1)
        self.assertEqual(self.inventory.stock("missing"), 0)

    def test_invalid_quantities_are_rejected_without_changing_stock(self):
        invalid_quantities = (0, -1, -8, 1.0, 1.5, "2", None, True, False)
        for method_name in ("add", "remove"):
            for quantity in invalid_quantities:
                with self.subTest(method=method_name, quantity=repr(quantity)):
                    inventory = Inventory()
                    inventory.add("apple", 5)
                    inventory.add("pear", 2)
                    with self.assertRaises(ValueError):
                        getattr(inventory, method_name)("apple", quantity)
                    self.assertEqual(inventory.stock("apple"), 5)
                    self.assertEqual(inventory.stock("pear"), 2)

    def test_invalid_quantities_for_unknown_products_keep_zero(self):
        for method_name in ("add", "remove"):
            for quantity in (0, -1, 1.5, True):
                with self.subTest(method=method_name, quantity=repr(quantity)):
                    with self.assertRaises(ValueError):
                        getattr(self.inventory, method_name)("missing", quantity)
                    self.assertEqual(self.inventory.stock("missing"), 0)

    def test_inventory_instances_do_not_share_stock(self):
        other = Inventory()
        self.inventory.add("apple", 5)
        other.add("apple", 2)
        self.assertEqual(self.inventory.stock("apple"), 5)
        self.assertEqual(other.stock("apple"), 2)
        other.remove("apple", 1)
        self.assertEqual(self.inventory.stock("apple"), 5)
        self.assertEqual(other.stock("apple"), 1)


if __name__ == "__main__":
    unittest.main()
