# Phase 5：内部存储字段重命名

## 本轮请求与范围

> 只做一个重构，把TodoList内部存储字段 _titles 改为 _items，公开接口和行为保持不变。

沿用统一 tdd Skill 与已有实现。仅进行指定字段重命名和必要测试回归，不推进其他阶段。“每步确认”继续有效。

## 改动

`todo.py` 中仅替换三处私有属性引用：

```diff
-        self._titles: list[str] = []
+        self._items: list[str] = []
-        self._titles.append(normalized_title)
+        self._items.append(normalized_title)
-        return self._titles.copy()
+        return self._items.copy()
```

`TodoList`、构造器、`add`、`list_titles` 的公开接口不变；校验、空白清理、重复标题、顺序与列表快照实现不变。未修改测试，也未新增业务需求或修改历史产物/快照。

## 真实动作、命令与结果

1. 实际计算重构前 `todo.py`、`test_todo.py` SHA-256，保存 `phase5-before-hashes.json`。
2. 在本目录真实执行测试基线：

```sh
python3 -B -m unittest -v test_todo
```

基线退出码 0，7 个测试方法全部通过（含空标题的 3 个子场景）；完整输出保存 `phase5-baseline.log`。
3. 使用 `apply_patch` 完成上述三处字段重命名。
4. 实际执行相同测试命令，退出码 0，7 个测试方法全部通过；完整输出保存 `phase5-regression.log`。
5. 实际计算重构后 SHA-256，保存 `phase5-code-hashes.json`；测试文件前后哈希一致。

测试由 Python subprocess 调用真实 unittest 进程，日志保存原始合并输出与实际结果，不是模拟通过。全部新增或修改文件仅在授权目录，未改 Skill、Git、全局配置，未读取旧样例。

## 代码前后 SHA-256

| 文件 | 重构前 | 重构后 |
| --- | --- | --- |
| `todo.py` | `cd1ec145e8512dc1d97b7ccb41032e9e4c80f49a5d769cf0d7c67592834a4e66` | `19484c6881a5478c2dbdd04a97f62e78252b52745003b87f2b0ce26dfb8ca20a` |
| `test_todo.py` | `d82e9d62ceec64da308ed94ad7a7f34b09f6427cf39a50ff1287c614fb9793d5` | `d82e9d62ceec64da308ed94ad7a7f34b09f6427cf39a50ff1287c614fb9793d5` |

## 当前停点

指定字段重命名完成，重构前后相关测试均通过，测试内容未修改。当前停在本轮重构交付点；未推进独立验收或其他行为开发。
