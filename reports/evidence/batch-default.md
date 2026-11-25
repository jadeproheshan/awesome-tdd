# batch-default 执行证据

交付目录：`隔离测试目录/batch-default`

本次按 `仓库/skills/tdd-batch/SKILL.md` 默认逐行为循环自动推进。全部写入均在上述隔离目录内；未提交、未推送，未改动 skill 或全局配置。

## 需求与最小契约

- Python 标准库；纯内存，无 Web、数据库或外部依赖。
- `BookingBook.create(room, start, end) -> Reservation`；预约含独立递增的 `id`、`room`、`start`、`end`。
- 时间为整数分钟，采用半开区间 `[start, end)`；`start >= end` 抛 `ValueError`，非整数（含 bool）抛 `TypeError`。
- 同房间重叠抛 `BookingConflict`，相邻允许，不同房间独立。
- `BookingBook.cancel(reservation_id)` 删除指定预约，使时段可重订；未知编号遵循字典语义抛 `KeyError`。

## 实际执行顺序与结果

1. 使用 `cat 仓库/skills/tdd-batch/SKILL.md` 读取技能；读取仓库 `README.md`，检索相关说明、代码和测试，检查上级 `AGENTS.md`。目标目录最初不存在，无现成契约或代码可复用。
2. `mkdir -p 隔离测试目录/batch-default`；写入 `Reservation`、`BookingConflict`、`BookingBook.create` 最小骨架和创建测试。骨架的 `create` 仅 `pass`，测试可真实导入执行。
3. 运行创建测试：`python3 -m unittest -v`，退出 1，1 个测试业务断言失败（期望预约，实际 `None`），见 `01-create-red.log`。
4. 实现通用创建、存储及递增编号；运行同一命令，退出 0，1 个测试通过，见 `02-create-green.log`。
5. 新增时间约束组合测试；运行同一命令，退出 1，2 个测试中的 6 个子场景失败（未抛预期异常），见 `03-time-red.log`。
6. 实现整数及 `start < end` 校验；运行同一命令，退出 0，2 个测试通过，见 `04-time-green.log`。
7. 新增同房间五种重叠形状测试（完全相等、左交叉、右交叉、被包含、包含）；运行同一命令，退出 1，3 个测试中的 5 个子场景失败（未抛冲突），见 `05-overlap-red.log`。
8. 实现同房间区间冲突判断 `start < existing.end and existing.start < end`；运行同一命令，退出 0，3 个测试通过，见 `06-overlap-green.log`。
9. 新增前后相邻与不同房间同时预约测试；运行同一命令，退出 0，5 个测试通过，见 `07-adjacency-rooms-already-green.log`。这些新测试被既有实现直接覆盖；未倒退实现制造 Red。
10. 新增 `cancel` 最小骨架及取消释放测试；运行同一命令，退出 1，6 个测试中 1 个业务错误：取消后重订仍抛 `BookingConflict`。这是取消未释放时段的行为失败，不是导入、编译或环境错误；见 `08-cancel-red.log`。
11. 实现按编号删除预约；运行同一命令，退出 0，6 个测试通过，见 `09-cancel-green.log`。测试同时检查取消后可重订、编号不复用，以及同房间其他预约、其他房间预约仍阻止冲突。
12. 最终并行执行整批回归与编译检查：
    - `python3 -m unittest discover -v`：退出 0，6 个测试全部通过，见 `10-final-regression.log`。
    - `python3 -m compileall -q booking.py test_booking.py`：退出 0，见 `11-compile.log`。

每轮先新增测试并真实运行，再补实现并运行该轮及既有回归。修改使用 `apply_patch`，未修改测试预期来迁就实现。相邻与不同房间测试已通过，因此没有为其添加多余实现。

## 命令与日志保存方式

所有测试命令的工作目录均为交付目录。第 1 轮通过 shell 重定向保存 stdout/stderr 并保留退出码；其余轮次通过以下标准库包装实际调用测试命令、合并输出、写日志、回传真实退出码（`LOG` 为表中具体日志文件名）：

```python
import subprocess, pathlib
p = subprocess.run(
    ["python3", "-m", "unittest", "-v"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
)
pathlib.Path(LOG).write_text(p.stdout)
print(p.stdout, end="")
raise SystemExit(p.returncode)
```

最终回归增加 `discover` 参数；编译检查同样由 `subprocess.run` 执行并记录真实退出码。

运行环境：Python 3.9.6；无安装命令、环境修复或环境阻塞。

## 复查入口与限制

- 实现：`booking.py`；测试：`test_booking.py`。
- 重跑：在本目录运行 `python3 -m unittest discover -v`。
- 此模块面向单进程、顺序调用，未承诺或验证多线程原子性、持久化、Web API；未实现这些未请求功能。
- 负整数分钟未被禁止（需求仅要求整数及 `start < end`）；房间名按传入字符串精确比较。
- 未知编号取消的 `KeyError` 是本地最小接口约定，本次未额外增加该约定的测试。
- 最终无未完成的请求行为；早期失败日志为真实 TDD 历史，当前整批为通过状态。
