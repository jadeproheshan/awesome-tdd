# Phase 1：库存模块测试审阅停点

## 请求与范围

- 使用 `仓库/skills/tdd-batch/SKILL.md`。
- 用户明确要求先写整批测试并真实运行，审阅后再实现业务。
- 所有新增文件均在 `隔离测试目录/review-gate/`。
- 未提交、未推送，未修改技能或全局配置。

## 实际动作

1. 读取指定 `SKILL.md`、仓库 `README.md`，检查上级 `AGENTS.md`（检查路径均无该文件）。
2. 用 `rg --files` 查找相关说明、库存代码、测试，未发现既有库存接口可复用；隔离目录初始为空。
3. 查看仓库状态：原有未跟踪项为 `.gitignore`、`README.md`、`skills/`，未修改这些内容。
4. 创建 `inventory.py` 最小可调用骨架与 `test_inventory.py` 全批验收测试。
5. 运行标准库 `unittest`，确认实际结果。
6. 保存本记录；停止在业务实现前。

## 最小契约与测试入口

- `Inventory.add(product: str, quantity: int) -> None`
- `Inventory.remove(product: str, quantity: int) -> None`
- `Inventory.stock(product: str) -> int`
- 商品用字符串标识，各实例独立保存内存状态。
- 正整数不包含 `bool`；非正数、非整数、布尔值被拒绝。
- 数量非法或库存不足均约定抛出标准库 `ValueError`，不改库存。
- 测试代码：`test_inventory.py`。
- 这些契约是本轮为测试选择的最小接口，没有实现库存保存、增减或校验逻辑。

## 测试覆盖

- 未知商品查询为 0，重复查询稳定。
- 正整数入库与重复累加；正整数扣减与连续扣减。
- 恰好扣完为 0，之后可重新入库。
- 库存不足拒绝，目标和其他商品库存保持原值，之后仍可正常扣减。
- 未知商品扣减拒绝且库存仍为 0。
- 入库和扣减对非法数量的拒绝与状态保持，覆盖已知/未知商品。
- 商品间及库存实例间的状态独立。

## 实际命令与结果

工作目录：`隔离测试目录/review-gate`

```sh
python3 -B -m unittest discover -s . -p 'test_*.py' -v
```

- 退出码：`1`。
- 输出末尾：`Ran 10 tests in 0.001s` / `FAILED (failures=33)`。
- 10 个测试方法中，未知商品查询方法通过；其余 9 个测试方法失败。
- 33 是断言失败条数，包含 `subTest` 参数场景，不是 33 个测试方法。
- 典型失败：`AssertionError: 0 != 1`、`AssertionError: ValueError not raised`。
- 没有导入、语法或运行环境错误。失败来自尚未实现的库存行为。
- 查询骨架固定返回 0，所以未知商品用例已通过；未为制造全红而破坏它。
- `-B` 避免生成字节码文件；没有安装依赖。

## 当前停点与交接

`add`/`remove` 目前只有 `pass`，`stock` 仅返回 0；未实现业务。整批测试已经写好并运行，等待用户审阅。只有用户明确要求继续实现后，才沿用这批测试进入实现阶段。
