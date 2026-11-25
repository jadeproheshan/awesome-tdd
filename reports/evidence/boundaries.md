# 单入口 tdd：只补测试与只读验收边界

## 执行范围

继续复用此前已读取的 `仓库/skills/tdd/SKILL.md`。未读取旧样例，未修改 Skill、Git 或全局配置。仅在当前隔离目录新增两组独立文件及本证据文件；原 `cart.py`、`test_cart.py` 保持不变。

先建立题设要求的既有实现及既有测试，再记录请求执行前哈希；“前后不变”指用户请求开始执行前后，不把场景初始化误称为只读操作。

## 动作顺序及真实结果

1. `mkdir -p 本地隔离测试目录/batch/already-green 本地隔离测试目录/batch/read-only`，退出码 0。
2. 初始化 `already-green/normalize.py` 为 `return value.strip().lower()`，已有测试断言 `normalize_label(" Hello ") == "hello"`。
3. 初始化 `read-only/subtotal.py` 为 `return 0`，已有测试断言 `subtotal([2, 3]) == 5`。
4. 对 already-green 运行既有基线，1 个测试通过，退出码 0；记录两个场景及原购物车的请求执行前哈希。
5. 执行请求“$tdd 给空白输入归一化为空串补测试，只写测试给我看”：只给 `already-green/test_normalize.py` 添加空串、纯空格、制表符/换行/回车混合空白三个子场景，未改生产代码。
6. 在 already-green 实际运行，2 个测试方法全部通过，退出码 0。新增测试直接通过；核对断言确实验证空白输入得到空串，现有实现已覆盖此行为，没有破坏代码制造 Red。
7. 执行请求“$tdd 验收当前版本”：仅运行 read-only 的现有测试，1 个测试失败，退出码 1，真实断言信息 `AssertionError: 0 != 5`。这是业务断言失败，不是导入或环境问题。未修改实现、测试或期待值。
8. 重新记录前述文件哈希；记录本证据。两个测试运行互相独立。

三次真实测试均使用命令：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
```

| 运行 | 工作目录（相对当前 batch 目录） | 输出摘要 | 退出码 |
| --- | --- | --- | --- |
| 既有基线 | `already-green` | Ran 1 test in 0.000s; OK | 0 |
| 空白输入补测试后 | `already-green` | Ran 2 tests in 0.000s; OK | 0 |
| 既有错误版本验收 | `read-only` | Ran 1 test in 0.000s; FAILED (failures=1); 0 != 5 | 1 |

## 生产/测试文件前后 SHA-256

哈希命令在 `本地隔离测试目录/batch` 真实执行两次，均退出码 0：

```sh
python3 -c 'import hashlib,pathlib; root=pathlib.Path("."); paths=[root/"cart.py",root/"test_cart.py",root/"already-green/normalize.py",root/"already-green/test_normalize.py",root/"read-only/subtotal.py",root/"read-only/test_subtotal.py"]; [print(str(p)+" "+hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]'
```

| 文件 | 请求执行前 SHA-256 | 请求执行后 SHA-256 |
| --- | --- | --- |
| `already-green/normalize.py` | `0a8da21e949f8014d172e064a5f160ffeb63ad2eeb6b16a997f40fe4525194e2` | `0a8da21e949f8014d172e064a5f160ffeb63ad2eeb6b16a997f40fe4525194e2` |
| `already-green/test_normalize.py` | `48a60f204002e191b7374835c4243582d8aa699818ebe1f832d039473c30b9c8` | `089416a109b77a88ecbb2dc9cc9d5248c09e560d277148b9957ac0f53ce317e6` |
| `read-only/subtotal.py` | `a816339b49e476ee1239aeb94f1b05c882c36137d83c4430f79c4d247302511d` | `a816339b49e476ee1239aeb94f1b05c882c36137d83c4430f79c4d247302511d` |
| `read-only/test_subtotal.py` | `ec22a8bd22d2ef34da838b8ff3fd2b035de95f8248fb03b2ec6263a34ee95bd3` | `ec22a8bd22d2ef34da838b8ff3fd2b035de95f8248fb03b2ec6263a34ee95bd3` |
| `cart.py` | `aa44f2047d398c5f618eff5b3653acf2cb31201f41b8f56ec13f08250f7af8a3` | `aa44f2047d398c5f618eff5b3653acf2cb31201f41b8f56ec13f08250f7af8a3` |
| `test_cart.py` | `c5f42340e6bb7c30903b3732b6155a176c4b1d0d0e371f6cdea52152d09fa657` | `c5f42340e6bb7c30903b3732b6155a176c4b1d0d0e371f6cdea52152d09fa657` |

## 可审阅测试与当前停点

新增测试位于 `already-green/test_normalize.py`：

```python
def test_blank_input_normalizes_to_empty_string(self):
    for value in ("", "   ", "\t\n\r "):
        with self.subTest(value=value):
            self.assertEqual(normalize_label(value), "")
```

停在“只写测试给用户审阅”；生产代码未修改，已实际运行，新增行为属于已有通过。

验收入口为 `read-only/test_subtotal.py`，实际断言为 `self.assertEqual(subtotal([2, 3]), 5)`。停在“报告当前版本验收失败”；仅验收的授权未扩展到修复，生产及测试文件前后哈希一致，没有自动进入实现阶段。

交付为两组场景各自的生产/测试文件和本证据文件；没有其他业务扩展。
