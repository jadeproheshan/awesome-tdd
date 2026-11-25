# Phase 2：沿用已审阅测试实现并回归

## 授权与范围

用户已审阅第一阶段测试，明确要求继续实现、沿用原测试并运行回归，无须重新讨论实体或规则。本轮只修改隔离目录内的 `inventory.py`，新增本记录；未提交、未推送，未修改技能或全局配置。

## 实际动作

1. 读取现有 `inventory.py`、`test_inventory.py`、`evidence-phase1.md`，确认契约与原批次测试。
2. 通过 Python 标准库 `pathlib`、`hashlib`、`json` 计算测试、第一阶段记录、快照、日志和校验文件的 SHA-256，留作变更前基线。
3. 实现每实例独立的字典库存；入库累加、查询未知商品为 0。
4. 入库和扣减先验证正整数，明确拒绝布尔值；非法数量抛出 `ValueError`。
5. 扣减先验证可用库存，库存不足时抛出 `ValueError`，通过检查后才修改库存。
6. 运行原整批测试，重新计算受保护文件 SHA-256，与变更前基线逐项一致。

## 实际命令与结果

工作目录：`隔离测试目录/review-gate`

```sh
python3 -B -m unittest discover -s . -p 'test_*.py' -v
```

- 退出码：`0`。
- 输出末尾：`Ran 10 tests in 0.001s` / `OK`。
- 原有 10 个测试方法及所有参数化子场景全部通过。
- 未修改、删除或弱化测试；未增加依赖，`-B` 避免生成字节码。
- 第一阶段 33 个断言失败已通过真实库存实现解决。

哈希检查使用两次相同的 `python3 -B -` 脚本，通过 `Path.read_bytes()` 与 `hashlib.sha256()` 读取下列文件并比较结果。变更前后摘要完全一致：

| 文件 | SHA-256 |
| --- | --- |
| `test_inventory.py` | `31dc093528da3da7b22985a44e3950acc68a2a3ff19a0792056702efd3d45677` |
| `evidence-phase1.md` | `6b74a0ba5f5281ccfaf2d0db06d72233f88af0acd1696d2d4ea3f24caa34f098` |
| `phase1-snapshot/inventory.py` | `17fc709c314d3fe2209bb0c4a9808000ec92457ddada0efaeb5bbb251cc24dcb` |
| `phase1-snapshot/test_inventory.py` | `31dc093528da3da7b22985a44e3950acc68a2a3ff19a0792056702efd3d45677` |
| `phase1-root-run.log` | `8444deb744c8794e3cb55286271d2ec1123da9319237c5c4efdfdcc76403e506` |
| `phase1-test.sha256` | `4b89d9c930b40d6dfb4f4b2831a1c3217c815c7d474e21fda3715f68da16e68c` |

## 完成状态

已完成已审阅契约中的全部库存行为及原批次回归。使用范围是独立实例内存库存；没有扩展持久化、并发或其他未请求功能。第一阶段证据保持不变，当前没有待实现的已授权行为。
