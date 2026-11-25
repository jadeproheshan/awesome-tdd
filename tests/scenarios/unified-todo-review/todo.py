"""In-memory title-only todo list contract; business methods are pending."""


class TodoList:
    """Keep titles in insertion order, including duplicate titles."""

    def __init__(self) -> None:
        self._titles: list[str] = []

    def add(self, title: str) -> None:
        """Append title.strip(); raise ValueError if empty, without mutation.

        Interior whitespace is preserved. Duplicate titles are permitted.
        """
        raise NotImplementedError("Adding titles is not implemented yet")

    def list_titles(self) -> list[str]:
        """Return a list snapshot of normalized titles in insertion order."""
        raise NotImplementedError("Listing titles is not implemented yet")
