"""Minimal inventory contract; business implementation awaits test review.

Products are identified by strings. Quantities must be positive integers;
booleans are not quantities. Invalid quantities and insufficient stock raise
ValueError without changing inventory. Successful mutations return None.
"""


class Inventory:
    """An independent, in-memory collection of product stock counts."""

    def add(self, product: str, quantity: int) -> None:
        """Add a positive integer quantity. Business logic is pending."""
        pass

    def remove(self, product: str, quantity: int) -> None:
        """Remove stock, or raise ValueError. Business logic is pending."""
        pass

    def stock(self, product: str) -> int:
        """Return the stock count, with zero for unknown products."""
        return 0
