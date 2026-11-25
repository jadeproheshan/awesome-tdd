# Phase 2：最小行为、契约与可调用骨架

## 本轮请求与范围

> 需求就按刚才的来。重复标题允许。先列最小行为和验收场景，然后只定接口和必要实体，落个能调用的骨架，别实现。

沿用已读的统一 Skill `仓库/skills/tdd/SKILL.md` 和 Phase 1 上下文。重复标题现在是用户明确确认的规则。

## 最小行为与验收场景

按依赖顺序梳理；多个行为可以由同一条端到端场景验证，不要求行为、测试、函数一一对应。

| 顺序 | 最小行为 | 输入与动作 | 可观察预期 |
| --- | --- | --- | --- |
| 1 | 空清单列出 | 新建清单，列出 | `[]` |
| 2 | 新增有效标题 | 新增 `买牛奶`，列出 | `['买牛奶']`；新增成功返回 `None` |
| 3 | 标题规范化 | 新增 `' \t读  书\n'`，列出 | `['读  书']`，首尾空白去掉，中间空白保留 |
| 4 | 拒绝空标题并保持原状态 | 已有 `第一项`，分别尝试新增 `''`、`'   '`、`'\t\n'` | 每次抛出 `ValueError`，清单仍为 `['第一项']` |
| 5 | 按创建顺序列出 | 依次新增 `第一项`、`第二项` | `['第一项', '第二项']` |
| 6 | 允许重复标题 | 依次新增 `重复`、` 重复 ` | `['重复', '重复']` |

接口层约定：每次列出返回标题列表快照，修改返回值不应修改内部清单。这是返回值所有权的技术选择，不引入新业务功能。标题输入范围为 `str`，本轮不定义其他类型的错误语义。

## 最小契约与必要实体

仅需 `TodoList` 一个实体，内部保留 `list[str]`，不引入 ID、状态、时间戳或额外项目实体。

```python
class TodoList:
    def __init__(self) -> None: ...
    def add(self, title: str) -> None: ...
    def list_titles(self) -> list[str]: ...
```

- `add`：新增 `title.strip()`，保留中间空白；规范化后为空则抛出 `ValueError`，不改变清单；允许重复；成功返回 `None`。
- `list_titles`：返回按成功新增顺序排列的标题列表快照。
- 内存生命周期：各实例拥有独立状态；不做持久化。
- 骨架文件：`todo.py`。构造器仅建立必要状态，两个业务方法明确抛出 `NotImplementedError`，没有实现标题验证、添加或读取行为。

## 真实动作、命令与结果

1. `cat 本地隔离测试目录/routing/phase1.md`：退出码 0，复用前轮已确认规则。
2. 在写骨架前先交付最小行为顺序及接口选择；随后使用 heredoc 创建本目录的 `todo.py`。
3. 真实执行 `python3 -B - <<'PY'` 骨架烟雾检查：切换至本目录并加入模块搜索路径，导入 `TodoList`、实例化，分别调用 `add('  买牛奶  ')` 和 `list_titles()`，确认两者均抛出 `NotImplementedError`；退出码 0。输出：

```text
add: callable skeleton raises NotImplementedError as intended
list_titles: callable skeleton raises NotImplementedError as intended
Skeleton import and calls verified; business behavior has not been tested.
```

4. 使用 heredoc 写本记录。全部写入限本目录，未修改 Skill、Git 或全局配置，未读取旧样例。

上述检查仅证明模块可导入、类可实例化、方法可调用且仍为占位；没有运行业务验收测试，不表示任何业务行为已通过。

## 当前停点

本轮最小行为、验收场景、接口和必要实体已确定，可调用骨架已落盘。停在契约/骨架交付点；没有编写业务测试，没有实现业务。等待用户下一轮授权。
