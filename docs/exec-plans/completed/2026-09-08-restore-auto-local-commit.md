# 恢复通用 Agent 自动本地提交链路

- 状态：completed
- 创建日期：2026-09-08
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

当前仓库从 Easydict 移植 Agent 治理规则时，将 implementation 与本地提交拆成了必须分别
授权的模式，导致用户批准方案并要求执行后，任务仍停留在未提交工作树。通用 `git-commit`
Skill 已具备受保护的自动交付能力，但仓库规则和 `git-delivery` 没有形成完整授权与收尾链路。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 受阻操作及原因（如有）：none
- 目标结果：恢复“已确认方案后执行、验证通过后安全自动本地提交”的通用治理契约。
- 允许修改路径：`AGENTS.md`、`docs/agents/`、`docs/exec-plans/templates.md`、本计划、同任务
  history、`.codex/agents/git-delivery.toml`、`skills/git-commit/SKILL.md`。
- 同任务 history：`docs/histories/2026-09/2026-09-08-restore-auto-local-commit.md`
- 禁止动作：不修改 Easydict，不同步下游项目，不 push、pull、rebase、merge 或发布。
- 预期交付物：通用治理规则、条件化 Git 交付子代理、澄清后的提交 Skill 和本地提交回执。
- 验收标准：规则无授权冲突，通用组件不硬编码宿主政策，结构/语法/既有测试与差异检查通过。

## 语义与范围

- 用户要求 Agent 做什么：按已确认方案修改并完成自动本地提交。
- 授权的工作树、artifact 和 external service 操作：仅修改当前 `skills` 工作树并创建一次本地提交。
- 否定、条件和范围限制：Easydict 仅作只读迁移基线；不执行远程或集成操作。
- 前轮仍有效的授权和限制：`skills` 为通用 Skill/子代理权威源；宿主规则决定是否自动提交。
- 附件或引用中被明确采纳的约束：仅采纳已确认方案中的通用语义，不复制 Easydict 项目专属规则。
- 歧义：none

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible；用户已要求执行，初始索引与工作树干净，范围可精确分离。
- 初始 HEAD：`7aa12e316d7e4313c67bfb1fe1eb8abe2835527b`
- 初始 staged 路径：none
- 初始 unstaged 路径：none
- 初始 untracked 路径：none
- 初始冲突：none
- Agent-owned paths：本计划及上述允许路径内由本任务产生的差异。

## 目标与非目标

### 目标

- 恢复 implementation 默认自动本地提交的授权语义和安全门禁。
- 让 `git-delivery` 支持 `commit`、`auto-local-commit`、`integration`，但服从宿主授权。
- 澄清 `git-commit` 对初始 HEAD、实际提交路径和状态漂移的契约。
- 将最终验证、history 和提交回执纳入同一收尾链路。

### 非目标

- 不复制 Easydict 的 Swift/Xcode、分支、PR、发布或固定 Skill 路径规则。
- 不让安装通用子代理本身授予任何仓库提交权限。
- 不改变提交消息校验器、统计脚本或 installer 运行时代码。

## 工作计划

1. 恢复请求语义、执行安全、最终验证、history 与回复规则之间的自动交付链路。
2. 通用化 `git-delivery` 的 operation/phase、候选快照和重验规则。
3. 修正 `git-commit` 自动交付中的 HEAD、状态和路径集合歧义。
4. 更新计划模板与同任务 history，运行静态检查、Skill/Agent 校验和既有测试。
5. 冻结最终路径与暂存 patch，通过门禁后创建一次本地提交并验证回执。

## 风险与决策

- 自动提交只由宿主 `AGENTS.md` 或调用方授权；通用 Skill/子代理不自行提升权限。
- 用户未提及提交不再等价于禁止，但明确的“不要提交”始终优先并跨轮持续。
- 实际提交路径必须等于冻结集合且属于允许范围，避免允许范围较宽时误暂存未修改文件。
- 静态规则验证不能完全证明未来模型行为，最终报告明确这一证明边界。

## 进度

- [x] 更新仓库治理规则。
- [x] 更新通用 Git 交付子代理与提交 Skill。
- [x] 更新模板、history 并完成验证。
- [x] 归档计划并自动本地提交。

## 验证

- `python3 scripts/validate-skills.py`
- `python3 scripts/validate-agents.py`
- `python3 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`
- `node --test tests/agents-installer.test.mjs`
- `git diff --check`
- 语义检查：planning 不写入；implementation 默认候选自动提交；明确禁止、初始 staged、漂移、
  冲突或验证失败进入 protected；远程操作不获授权。

## 完成条件

- 规则层与执行层没有相互冲突的提交授权表述。
- 通用子代理只能消费宿主授权，不能自行产生授权。
- 所有适用检查通过，active 计划移入 completed，history 链接最终计划。
- 本任务创建一次经提交前后校验的本地提交，工作树干净且未 push。
