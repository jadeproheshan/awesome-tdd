# 其余五个单步技能实际验证

范围：只在本 single-steps 目录新增 planning 与 green-refactor 隔离 fixture 及用户明确要求的过程记录。未改 skill、全局配置或执行 git 提交。实际使用前已逐一阅读 skills/tdd-scope、tdd-case、tdd-contract、tdd-green、tdd-refactor 的 SKILL.md。

## 每步输出和停点

| 步骤 | 实际动作与结果 | 停点与证据 |
| --- | --- | --- |
| scope | 将用户规则整理为已确认需求与验收边界，影响行为的未决规则为零 | 仅需求澄清，未建代码或测试；planning/scope-output.md |
| case | 选择新增并列出规范化标题的最小闭环，列出空清单、去边缘空白、内部空白保留、创建顺序、拒绝空标题的可观察场景 | 仅场景，不写代码；planning/case-output.md |
| contract | 新增 TodoList.add、list_titles 签名和两个 NotImplementedError 占位；用 ValueError 表达空标题拒绝的技术约定 | 导入与签名检查退出码 0；未实现业务、未建测试；planning/contract-output.md、contract-import.txt |
| green | 先真实运行两项已有测试，均因占位 NotImplementedError 出错，退出码 1；用通用累计实现 subtotal，随后两项通过、退出码 0 | 保持测试不变，目标和回归通过后停止；green-refactor/green-output.md、green-baseline.txt、green-result.txt |
| refactor | 先跑基线两项通过，只有 amount→total、item→price 局部变量改名，再跑两项通过；逆向改名后 AST 与原版本一致 | 保持公开接口和算法，未加功能或改测试；green-refactor/refactor-output.md、refactor-baseline.txt、refactor-result.txt |

scope/case 的文档是本任务要求的输出记录，并非技能强制项目建文档。contract 的检查只证明导入和签名可用，不代表业务通过。green/refactor 的通过只对应 fixture 中 []=>0、[2,3]=>5 两项既有测试；未声称完成更广的需求验收。

## 实际命令

- contract 在 planning 目录执行：`python3 -B -c 'import inspect; from todo import TodoList; print("add", inspect.signature(TodoList.add)); print("list_titles", inspect.signature(TodoList.list_titles))'`，退出码 0。
- green 基线、green 完成、refactor 基线、refactor 完成均在 green-refactor 目录执行：`python3 -B -m unittest discover -s . -v`，退出码依次为 1、0、0、0。
- refactor 另真实执行标准库 AST 对照：对新 AST 的 Name 节点执行 `total→amount`、`price→item` 映射后，`ast.dump(before_tree) == ast.dump(mapped_after_tree)` 断言通过。

各命令完整 stdout/stderr 及退出码保存在相应 txt 日志。日志保存脚本自身退出码为 0，不与 unittest 子进程基线的退出码 1 混淆。`-B` 避免生成字节码缓存。

## 每步文件变化快照

每个步骤的 `snapshots/<步骤>.json` 保存执行前/后的相对文件清单、完整内容和 SHA-256。快照排除 snapshots 目录自身，以避免自引用；其余 fixture 文件及输出记录均纳入。执行阶段的 before/after 不包含之后步骤的改动。

| 步骤 | 新增文件 | 修改文件 | 删除文件 |
| --- | --- | --- | --- |
| scope | `scope-output.md` | `无` | `无` |
| case | `case-output.md` | `无` | `无` |
| contract | `contract-import.txt`, `contract-output.md`, `todo.py` | `无` | `无` |
| green | `green-baseline.txt`, `green-output.md`, `green-result.txt` | `pricing.py` | `无` |
| refactor | `refactor-baseline.txt`, `refactor-output.md`, `refactor-result.txt` | `pricing.py` | `无` |

## 源码 hash 与保持检查

| 文件/阶段 | SHA-256 |
| --- | --- |
| planning/todo.py contract 后 | `d12e6973ae14c0367a017ec600d95ad18a34e4888b1f4f630e35734e30f8c5e3` |
| green-refactor/pricing.py green 前 | `081dadc21d7d17b40018177b9a6f2b7845dedba105c2d202adc596802c2b7d6a` |
| green-refactor/pricing.py green 后 / refactor 前 | `c2cf94edaa798da21b6c6fb4e17648ee802dec1ae23aadded61acaa15cbef30d` |
| green-refactor/pricing.py refactor 后 | `21efaef67baf94c57285d68673a95b213667ec55cc145db5515d844c0ca4f555` |
| green-refactor/test_pricing.py 所有阶段不变 | `06e619ae19b380bc580adece4101894d824ebcaff4d0801d22519f0c5456014a` |

已实际断言：scope/case 后无 Python 文件；contract 后唯一 Python 文件为 todo.py 且包含两处 NotImplementedError；green/refactor 测试 hash 不变；磁盘最终业务文件 hash 与最终阶段快照一致。每一步均按该请求停点结束，后续步骤只因独立明确请求而执行。
