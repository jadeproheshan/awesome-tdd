import unittest

from cart import ShoppingCart


class ShoppingCartTests(unittest.TestCase):
    def test_empty_cart_total_is_zero(self):
        self.assertEqual(ShoppingCart().total_cents(), 0)

    def test_add_products_and_calculate_total_in_cents(self):
        cart = ShoppingCart()
        cart.add("apple", 125, 3)
        cart.add("bread", 260, 2)
        cart.add("sample", 0, 4)
        self.assertEqual(cart.total_cents(), 895)

    def test_repeated_product_with_same_price_accumulates_quantity(self):
        cart = ShoppingCart()
        cart.add("apple", 125, 2)
        cart.add("bread", 260, 1)
        cart.add("apple", 125, 3)
        self.assertEqual(cart.total_cents(), 885)

    def test_different_price_is_rejected_without_changing_cart(self):
        cart = ShoppingCart()
        cart.add("apple", 125, 2)
        cart.add("bread", 260, 1)
        with self.assertRaises(ValueError):
            cart.add("apple", 126, 3)
        self.assertEqual(cart.total_cents(), 510)
        cart.add("apple", 125, 1)
        self.assertEqual(cart.total_cents(), 635)

    def test_zero_price_cannot_be_changed_on_a_repeated_product(self):
        cart = ShoppingCart()
        cart.add("sample", 0, 2)
        with self.assertRaises(ValueError):
            cart.add("sample", 1, 1)
        self.assertEqual(cart.total_cents(), 0)

    def test_invalid_quantity_is_rejected_without_changing_cart(self):
        for quantity in (0, -1, -5, 1.5, 2.0, True, False, "2", None):
            for product_id in ("apple", "pear"):
                with self.subTest(quantity=quantity, product_id=product_id):
                    cart = ShoppingCart()
                    cart.add("apple", 125, 2)
                    cart.add("bread", 260, 1)
                    with self.assertRaises(ValueError):
                        cart.add(product_id, 125, quantity)
                    self.assertEqual(cart.total_cents(), 510)
                    cart.add(product_id, 125, 1)
                    self.assertEqual(cart.total_cents(), 635)

    def test_invalid_unit_price_is_rejected_without_changing_cart(self):
        for price in (-1, -100, 1.5, 125.0, True, False, "125", None):
            for product_id in ("apple", "pear"):
                with self.subTest(price=price, product_id=product_id):
                    cart = ShoppingCart()
                    cart.add("apple", 125, 2)
                    cart.add("bread", 260, 1)
                    with self.assertRaises(ValueError):
                        cart.add(product_id, price, 1)
                    self.assertEqual(cart.total_cents(), 510)
                    cart.add(product_id, 125, 1)
                    self.assertEqual(cart.total_cents(), 635)


if __name__ == "__main__":
    unittest.main()
