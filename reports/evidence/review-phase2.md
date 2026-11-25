# 第二轮证据：沿用已审阅测试完成实现

## 本轮授权与执行范围

用户已审阅测试和异常约定，要求“继续实现。沿用这些测试，不用重新讨论实体”。沿用本对话已读取的单入口 `skills/tdd/SKILL.md`，进入“继续实现”能力；没有重开需求讨论，也没有添加功能、测试或额外实体。

所有写入均位于 `本地隔离测试目录/review`。没有修改 Skill、Git、全局配置或安装依赖。

## 实际动作

1. 查看当前文件清单及 `points_account.py` 空骨架；读取审阅前测试哈希，并计算当前测试哈希，确认一致。
2. 在改动实现前，实际运行原测试基线，保存在 `test-run-phase2-baseline.log`。
3. 仅修改业务文件 `points_account.py`：每个账户初始化余额 0；增加积分先校验再累加；消费积分先校验和检查余额，再扣减。无效输入、余额不足均在修改余额前拒绝。保留原公开接口、异常类型与成功返回 None 的约定，排除 bool。
4. 实际运行相同测试命令，结果保存在 `test-run-phase2.log`。
5. 再次核对测试哈希，写入 `test-sha256-after.txt`，使用断言比较审阅前、实现后和第一轮测试快照三个哈希，结果一致。
6. 比较本轮开始及完成后的指定保留文件哈希，确认 `phase1-snapshot` 中两个文件、`phase1-root-run.log`、`test-sha256-before.txt` 均未改变。

## 真实命令与结果

工作目录：`本地隔离测试目录/review`

实现前基线：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s . -p 'test_*.py' -v > test-run-phase2-baseline.log 2>&1
```

退出码 `1`，结果 `Ran 13 tests in 0.001s`、`FAILED (failures=29)`。均为原空骨架产生的业务断言失败，没有导入或环境错误。

实现后回归：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s . -p 'test_*.py' -v > test-run-phase2.log 2>&1
```

退出码 `0`，结果：

```text
Ran 13 tests in 0.001s

OK
```

原 13 个测试方法及其所有参数子场景均通过。没有删除、弱化或修改测试来取得通过。

## 测试哈希与保留证据

实际使用 `shasum -a 256` 以及 Python 标准库 `hashlib.sha256` 计算；Python 执行的比较为：

```python
assert before == after == snapshot, 'reviewed tests changed'
```

| 对象 | SHA-256 |
| --- | --- |
| 审阅前测试（`test-sha256-before.txt` 记录） | `bbc9729f886f0c9838afcb78435266eadbd07af719528c47ea446c4736207332` |
| 实现后 `test_points_account.py` | `bbc9729f886f0c9838afcb78435266eadbd07af719528c47ea446c4736207332` |
| `phase1-snapshot/test_points_account.py` | `bbc9729f886f0c9838afcb78435266eadbd07af719528c47ea446c4736207332` |
| 原 `phase1-snapshot/points_account.py`（前后相同） | `0b07c37bb9f77ea03913f7655dab7e82c6782f05cf27ee8ec6e8d5bfa9b744ee` |
| `phase1-root-run.log`（前后相同） | `b463cf4e8dbb9f5aba00f1d002155f1a5703872a02a99ee564e2b18c9e7cda0d` |
| `test-sha256-before.txt` 文件本身（前后相同） | `46bfa54de42f46db397bbae06f26d1ba2d340c7766a88029e9d4f1fdfa65c129` |

## 当前停点与限制

本轮授权的实现已完成，原测试全部通过。可复查代码为 `points_account.py`，测试仍是第一轮审阅的 `test_points_account.py`。

没有待用户决定的必要事项。本轮结束；没有进入额外重构或扩展功能。交付是内存中的顺序调用账户，未增加持久化、转账、流水、并发或外部服务，也未声称验证这些未请求的能力。
