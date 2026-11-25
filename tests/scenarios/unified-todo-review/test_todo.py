"""Business acceptance tests for adding and listing title-only todos."""

import unittest

from todo import TodoList


class TodoListTests(unittest.TestCase):
    def test_new_list_is_empty(self) -> None:
        self.assertEqual(TodoList().list_titles(), [])

    def test_adds_a_title(self) -> None:
        todos = TodoList()

        result = todos.add('买牛奶')

        self.assertIsNone(result)
        self.assertEqual(todos.list_titles(), ['买牛奶'])

    def test_strips_outer_whitespace_but_preserves_inner_whitespace(self) -> None:
        todos = TodoList()

        todos.add(' \t读  书\n')

        self.assertEqual(todos.list_titles(), ['读  书'])

    def test_lists_titles_in_creation_order(self) -> None:
        todos = TodoList()

        todos.add('第二项')
        todos.add('第一项')
        todos.add('第三项')

        self.assertEqual(todos.list_titles(), ['第二项', '第一项', '第三项'])

    def test_allows_duplicate_normalized_titles(self) -> None:
        todos = TodoList()

        todos.add('重复')
        todos.add(' 重复 ')

        self.assertEqual(todos.list_titles(), ['重复', '重复'])

    def test_rejects_empty_and_whitespace_only_titles(self) -> None:
        for title in ('', '   ', '\t\n'):
            with self.subTest(title=repr(title)):
                todos = TodoList()

                with self.assertRaises(ValueError):
                    todos.add(title)

                self.assertEqual(todos.list_titles(), [])

    def test_rejected_add_does_not_change_existing_titles(self) -> None:
        todos = TodoList()
        todos.add('第一项')

        with self.assertRaises(ValueError):
            todos.add(' \t\n ')
        todos.add('第二项')

        self.assertEqual(todos.list_titles(), ['第一项', '第二项'])


if __name__ == '__main__':
    unittest.main()
