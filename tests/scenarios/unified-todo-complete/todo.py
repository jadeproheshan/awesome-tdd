"""In-memory title-only todo list using the Python standard library."""


class TodoList:
    """Keep titles in insertion order, including duplicate titles."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def add(self, title: str) -> None:
        """Append title.strip(); raise ValueError if empty, without mutation.

        Interior whitespace is preserved. Duplicate titles are permitted.
        """
        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("Title must not be empty")
        self._items.append(normalized_title)

    def list_titles(self) -> list[str]:
        """Return a list snapshot of normalized titles in insertion order."""
        return self._items.copy()
