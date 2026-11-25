# 内存购物车：执行证据

## 范围与契约

按指定单入口 `仓库/skills/tdd/SKILL.md` 的批量流程推进；用户已要求完成限定功能，没有测试审阅停点。

全部创建及修改均位于 `本地隔离测试目录/batch`。未读取旧测试样例，未改 Skill、Git 或全局配置，未安装依赖。

- `ShoppingCart.add(product_id, unit_price_cents, quantity)`：新增商品；同 ID 同价格累计数量。
- `ShoppingCart.total_cents()`：返回整数分总价；空购物车返回 0。
- 非负整数分单价、正整数数量；采用 Python 内置 `int`，明确拒绝 `bool`、浮点数、字符串和 `None`。非法参数或同 ID 价格不一致均抛出 `ValueError`，验证在写入前完成。
- 商品 ID 以字符串使用；未增加 ID 格式规则。
- 仅内存存储、Python 标准库；未实现删除、支付、数据库、Web 或并发保证。

## 真实动作顺序及命令结果

1. 用 `cat 仓库/skills/tdd/SKILL.md` 读取指定入口，退出码 0。
2. 用 `mkdir -p 本地隔离测试目录/batch` 创建指定目录，退出码 0。
3. 创建最小可调用骨架：`add` 暂不操作，`total_cents` 返回 0；先写空购物车和多商品总价测试。
4. 实际运行测试，新增商品业务断言失败；实现存储及总价后重跑通过。
5. 写重复商品累计测试，实际运行失败；实现累计后重跑通过。
6. 写价格冲突及零价格冲突测试，实际运行失败；实现冲突拒绝后重跑通过。
7. 写非法数量、非法单价测试，覆盖已存在和新商品，并在拒绝后验证总价不变及后续合法增加仍正确；实际运行失败。加入先校验后写入逻辑后，整批测试通过。
8. 用 `python3 --version` 检查运行环境，输出 `Python 3.9.6`，退出码 0；最后记录本文件并检查最终交付文件。

下表每次测试的真实命令均为：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
```

执行工作目录均为 `本地隔离测试目录/batch`。

| 次序 | 运行前动作 | 真实结果 | 退出码 |
| --- | --- | --- | --- |
| 1 | 空购物车及多商品测试 + 骨架 | Ran 2 tests; FAILED (failures=1)，总价 `0 != 895`；空购物车已通过 | 1 |
| 2 | 实现存储和总价 | Ran 2 tests; OK | 0 |
| 3 | 增加重复商品累计测试 | Ran 3 tests; FAILED (failures=1)，总价 `635 != 885` | 1 |
| 4 | 实现数量累计 | Ran 3 tests; OK | 0 |
| 5 | 增加价格冲突测试 | Ran 5 tests; FAILED (failures=2)，均为 `ValueError not raised` | 1 |
| 6 | 实现价格冲突拒绝 | Ran 5 tests; OK | 0 |
| 7 | 增加非法数量、非法价格测试 | Ran 7 tests; FAILED (failures=25, errors=2) | 1 |
| 8 | 实现参数校验并整批验收 | Ran 7 tests in 0.001s; OK | 0 |

第 7 次运行的 2 个 errors 是字符串/None 数量与已有整数数量相加时产生的运行期 `TypeError`；不是导入、编译或环境错误。25 个 failures 是未抛出预期 `ValueError` 的业务断言失败。已有商品的部分非法价格已被价格冲突逻辑拒绝，因此那些子场景直接通过，没有人为破坏实现制造失败。全部运行均正常导入被测代码。

## 最终覆盖与停点

`test_cart.py` 含 7 个测试方法，其中两个参数化方法分别含 18 个数量子场景和 16 个价格子场景；覆盖空购物车、多个商品总价、零单价、重复累计、价格冲突、非法输入及拒绝后继续操作。

交付文件：`cart.py`、`test_cart.py`、`evidence.md`。业务实现及所需回归已完成；当前停在整批验收通过。没有等待用户确认，也没有未完成的范围内功能。

调用示例：

```python
from cart import ShoppingCart

cart = ShoppingCart()
cart.add("apple", 125, 2)
cart.add("apple", 125, 3)
assert cart.total_cents() == 625
```
