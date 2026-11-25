"""Small in-memory inventory with validated stock mutations.

Products are identified by strings. Quantities must be positive integers;
booleans are not quantities. Invalid quantities and insufficient stock raise
ValueError without changing inventory. Successful mutations return None.
"""


class Inventory:
    """An independent, in-memory collection of product stock counts."""

    def __init__(self) -> None:
        self._stock: dict[str, int] = {}

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be a positive integer")

    def add(self, product: str, quantity: int) -> None:
        """Add a positive integer quantity."""
        self._validate_quantity(quantity)
        self._stock[product] = self.stock(product) + quantity

    def remove(self, product: str, quantity: int) -> None:
        """Remove stock, or raise ValueError without changing inventory."""
        self._validate_quantity(quantity)
        current = self.stock(product)
        if quantity > current:
            raise ValueError("insufficient stock")
        self._stock[product] = current - quantity

    def stock(self, product: str) -> int:
        """Return the stock count, with zero for unknown products."""
        return self._stock.get(product, 0)
