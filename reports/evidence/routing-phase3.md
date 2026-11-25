# Phase 3：测试编写与审阅停点

## 本轮请求

> 我们每步确认，下一步写测试，先做新增标题、列出、空标题拒绝这些行为；写好运行给我看。

沿用统一 tdd Skill 与 Phase 2 契约。本轮授权是写测试并真实运行，且“每步确认”生效；不跨入业务实现。

## 本轮产物

- `test_todo.py`：Python 标准库 unittest 测试，验证空清单列出、新增返回值与结果、首尾空白清理且保留中间空白、创建顺序、允许重复、三种空标题拒绝、拒绝后清单不变并可继续新增。
- `phase3-test.log`：真实测试输出，含完整 traceback。
- `phase3-code-hashes.json`：实际命令、退出码、运行前后代码 SHA-256。
- 本记录包含实际测试代码，方便审阅。

测试仅通过公开方法观察结果，没有 mock 或私有状态断言，没有修改原骨架。

## 实际命令与结果

先读取本目录 `todo.py`、`phase2.md`，随后使用 heredoc 创建测试文件。真实测试命令在本目录执行：

```sh
python3 -B -m unittest -v test_todo
```

实际使用 `subprocess.run` 执行上述命令，以原样合并输出写入 `phase3-test.log`，并将实际退出码返回给命令工具；不是模拟测试结果。结果为：

```text
Ran 7 tests in 0.001s
FAILED (errors=9)
Actual test exit code: 1
```

7 个测试方法，其中空标题拒绝包含 3 个子场景，因此累计 9 个错误。所有错误均为可调用骨架抛出的 `NotImplementedError`；模块导入、测试收集和 unittest 运行正常。此处没有业务断言比较失败，不把这些占位错误描述为已经触达业务断言的失败，也不冒充导入/环境问题。拒绝后状态不变的场景当前在首个有效新增处停止，尚未验证其后断言。

运行前后 `todo.py` 和 `test_todo.py` 的哈希相同，证明测试运行没有改代码；`todo.py` 本轮未修改。未改 Skill、Git 或全局配置，未读取旧样例。全部新增文件在本任务授权目录。

## 代码 SHA-256

- `todo.py`：`ca46de4c4a172afbdbb982b4049a42d5692a217140db2689ebc31d64bfd11270`
- `test_todo.py`：`d82e9d62ceec64da308ed94ad7a7f34b09f6427cf39a50ff1287c614fb9793d5`

## 实际测试代码

```python
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
```

## 当前停点

测试已编写并真实运行，交付测试代码和未通过的实际结果。停在测试审阅后等待确认的位置，没有实现新增或列出，没有修改测试期待来追求通过。下一阶段如获用户确认才进入最小实现，并先复跑基线；“每步确认”仍继续有效。
