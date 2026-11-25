# Phase 4：最小实现与相关回归

## 本轮请求和有效节奏

> 继续实现。

沿用统一 tdd Skill、已确认需求、Phase 2 契约和 Phase 3 实际测试，不重新澄清。此前“每步确认”继续有效，本轮只推进实现阶段并完成相关回归；不自动进入重构、发布或独立验收阶段。

## 关键改动

仅修改 `todo.py` 的模块说明与两个业务方法：

- `add` 使用 `str.strip()` 清理首尾空白，规范化后为空则抛出 `ValueError`，验证通过后才追加，因此失败不会改变原状态。
- 使用列表追加，保留重复标题和新增顺序，保留标题中间空白。
- `list_titles` 返回内部标题列表的副本，满足既有快照契约。

没有增加其他业务功能、依赖或架构，没有修改 `test_todo.py` 或历史产物。

## 真实动作和命令

1. 首次尝试用 `mkdir(exist_ok=False)` 建立 `phase3-snapshot`，因目录已经存在而得到 `FileExistsError`；该命令在复制、运行测试和改代码前退出，未覆盖快照。
2. 发现已有快照后，改为读取并核对其中 `todo.py`、`test_todo.py` 的 SHA-256，均与当前实现前代码一致。保留快照原样，不向其写入。
3. 修改前真实执行基线：

```sh
python3 -B -m unittest -v test_todo
```

基线退出码 1，7 个测试方法累计 9 个 `NotImplementedError` 错误；完整输出在 `phase4-baseline.log`。无导入或环境错误，不把占位错误冒充业务断言失败。

4. 使用 `apply_patch` 在 `todo.py` 完成最小实现，未更改测试或断言。
5. 修改后真实执行同一命令，退出码 0：

```text
Ran 7 tests in 0.000s
OK
```

完整输出在 `phase4-regression.log`。其中空标题拒绝的 3 个子场景也均通过。

6. 使用 SHA-256 记录前后代码哈希与快照代码哈希，保存 `phase4-before-hashes.json` 和 `phase4-code-hashes.json`；真实核验测试未改、快照代码未改。本记录随后落盘。

以上测试使用 Python subprocess 调用真正的 unittest 进程并记录实际退出码，不是模拟结果。全部写入限本目录，没有修改 Skill、Git、全局配置或读取旧样例。

## 代码前后 SHA-256

| 文件 | 实现前 | 实现后 |
| --- | --- | --- |
| `todo.py` | `ca46de4c4a172afbdbb982b4049a42d5692a217140db2689ebc31d64bfd11270` | `cd1ec145e8512dc1d97b7ccb41032e9e4c80f49a5d769cf0d7c67592834a4e66` |
| `test_todo.py` | `d82e9d62ceec64da308ed94ad7a7f34b09f6427cf39a50ff1287c614fb9793d5` | `d82e9d62ceec64da308ed94ad7a7f34b09f6427cf39a50ff1287c614fb9793d5` |

## 实际实现

```python
"""In-memory title-only todo list using the Python standard library."""


class TodoList:
    """Keep titles in insertion order, including duplicate titles."""

    def __init__(self) -> None:
        self._titles: list[str] = []

    def add(self, title: str) -> None:
        """Append title.strip(); raise ValueError if empty, without mutation.

        Interior whitespace is preserved. Duplicate titles are permitted.
        """
        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("Title must not be empty")
        self._titles.append(normalized_title)

    def list_titles(self) -> list[str]:
        """Return a list snapshot of normalized titles in insertion order."""
        return self._titles.copy()
```

## 当前停点与验证边界

选定行为的最小实现已完成，原有 7 个测试方法全部通过，未弱化或改写测试。停在实现交付后的确认点，“每步确认”仍有效。

本轮执行的是已有测试的相关回归，没有另行启动全面验收、重构或新增行为测试。列表快照的调用方修改隔离及实例间隔离虽由当前结构支持，现有这批测试未专门覆盖，不声称已经通过独立验证。`phase3-snapshot` 原样保留。
