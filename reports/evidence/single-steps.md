# 单步技能实际行为验证

本记录中的命令均真实执行。所有生成文件均位于本目录；未修改技能、全局配置，未执行 git 提交。

## 使用依据

已阅读仓库 README.md、skills/tdd-red/SKILL.md 和 skills/tdd-verify/SKILL.md。测试使用 Python 标准库 unittest；`-B` 禁止生成字节码缓存。

## 1. tdd-red：新测试直接通过

用户请求：给空白字符串归一化为 `''` 补一条测试，只做 red 这步。

先建立 fixture：`normalize_label(value)` 当前实现为 `return value.strip().lower()`；原有测试断言 `" Hello "` 返回 `"hello"`。基线真实运行通过（1 项，退出码 0），完整输出见 red-baseline.txt。

动作：只在 red/test_labels.py 新增一条有明确输出断言的测试：

```python
    def test_normalizes_whitespace_to_empty_string(self):
        self.assertEqual(normalize_label(" \t\n "), "")
```

实际运行结果：

```text
Working directory: 隔离测试目录/single-steps/red
$ python3 -B -m unittest discover -s . -v
test_normalizes_whitespace_to_empty_string (test_labels.NormalizeLabelTests) ... ok
test_trims_and_lowercases_label (test_labels.NormalizeLabelTests) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK

Exit code: 0
```

结论与停点：原有正确实现已经覆盖这个边界，新测试直接通过，未故意破坏实现制造 Red。仅新增测试，生产代码 hash 不变。在测试审阅点停止，未进入 green/refactor。

## 2. tdd-verify：发现既有错误但不修复

用户请求：验收当前版本，告诉我结果。

先建立独立 fixture：`total_price(prices)` 错误地 `return 0`；已有测试断言 `[2, 3]` 应得 `5`。这个行为标准明确，无其他构建或静态检查配置。

动作：只运行 fixture 全套 unittest；未修改生产代码或测试。

实际运行结果：

```text
Working directory: 隔离测试目录/single-steps/verify
$ python3 -B -m unittest discover -s . -v
test_sums_prices (test_pricing.TotalPriceTests) ... FAIL

======================================================================
FAIL: test_sums_prices (test_pricing.TotalPriceTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "隔离测试目录/single-steps/verify/test_pricing.py", line 8, in test_sums_prices
    self.assertEqual(total_price([2, 3]), 5)
AssertionError: 0 != 5

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)

Exit code: 1
```

结论与停点：验收失败，目标求和行为未完成，错误是行为断言失败 `0 != 5`，并非导入/编译/环境阻塞。属于 fixture 初始已有错误。按 verify 默认范围只报告，未修复、未弱化断言。覆盖限制：仅验证本 fixture 已有的一项求和需求，无声明其他功能或端到端验收完成。

## 初始与最终 SHA-256

初始 hash 在 fixture 创建后、新增 red 测试和执行 verify 前采集；最终 hash 在全部实际运行后采集。已程序断言只有 red 测试文件变化，其余三者不变。

| 文件 | 初始 SHA-256 | 最终 SHA-256 |
| --- | --- | --- |
| `red/labels.py` | `0a8da21e949f8014d172e064a5f160ffeb63ad2eeb6b16a997f40fe4525194e2` | `0a8da21e949f8014d172e064a5f160ffeb63ad2eeb6b16a997f40fe4525194e2` |
| `red/test_labels.py` | `6ec582146686e773838fea99b008304c68bb55503f350c1b22511d3d19a08810` | `a0f71e870fa4b72dfb8b53b06be969d3dc9c25678a2f097e3e51688375dca92d` |
| `verify/pricing.py` | `15d5ee4199e2d701d1fe1a47229d6a13902226c8b9db55de2413dc88dc917eb1` | `15d5ee4199e2d701d1fe1a47229d6a13902226c8b9db55de2413dc88dc917eb1` |
| `verify/test_pricing.py` | `3c0fb994b209bc1f7ed2018689a5af7e4a4e8320fc28b729a3323558f8122ae2` | `3c0fb994b209bc1f7ed2018689a5af7e4a4e8320fc28b729a3323558f8122ae2` |

机器可读 hash 另存 initial-hashes.json、final-hashes.json。日志中的退出码对应子进程 unittest 命令；执行日志保存脚本本身正常完成。
