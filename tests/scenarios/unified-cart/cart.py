"""An in-memory shopping cart with prices expressed in integer cents."""


class ShoppingCart:
    def __init__(self) -> None:
        self._items: dict[str, tuple[int, int]] = {}

    def add(self, product_id: str, unit_price_cents: int, quantity: int) -> None:
        """Add a product, raising ValueError before mutation for invalid input."""
        if type(unit_price_cents) is not int or unit_price_cents < 0:
            raise ValueError("unit price must be a non-negative integer in cents")
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("quantity must be a positive integer")
        if product_id in self._items:
            current_price, current_quantity = self._items[product_id]
            if unit_price_cents != current_price:
                raise ValueError("unit price must match the existing product price")
            quantity += current_quantity
        self._items[product_id] = (unit_price_cents, quantity)

    def total_cents(self) -> int:
        """Return the total price as integer cents."""
        return sum(price * quantity for price, quantity in self._items.values())
