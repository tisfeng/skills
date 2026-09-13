# 移植 Easydict Agent 治理文档

- 状态：completed
- 创建日期：2026-09-09
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

Easydict 的 `12f05421dc3edb29f4d7f68c257b293b11ab0be7` 与
`7ade3bcbbb0ad5409af993eab2e3ee8cc2a3b20d` 将重复的 Agent 规则收敛为根入口和五份专题文档。
当前 skills 仍保留独立的执行安全、代码质量和回复规则，并使用 `docs/architecture/` 命名。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 受阻操作及原因（如有）：none
- 目标结果：语义移植最终治理结构，并将 `docs/architecture/` 改为 `docs/design-docs/`。
- 允许修改路径：`AGENTS.md`、`docs/agents/`、`docs/design-docs/`、`docs/exec-plans/`、
  `docs/histories/`。
- 同任务 history：`docs/histories/2026-09/2026-09-09-port-easydict-agent-governance.md`
- 禁止动作：不 cherry-pick、不修改 `skills/`、`.codex/agents/`、安装器、CI、版本、锁文件或下游
  安装副本；不 push、pull、rebase、merge 或发布。
- 预期交付物：根入口、五份专题规则、`design-docs` 概览和同任务历史记录。
- 验收标准：无活动旧路径；当前暂存策略不回退；相关结构与文档检查通过。

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible；用户已明确要求执行，初始索引和工作树干净，范围可精确分离。
- 初始 HEAD：`c236cc6c6034d31dbf07223e4ee7e24e4fc42242`
- 初始 staged 路径：none
- 初始 unstaged 路径：none
- 初始 untracked 路径：none
- 初始冲突：none
- Agent-owned paths：本计划及上述允许路径内由本任务产生的差异。

## 目标与非目标

### 目标

- 将执行安全并入请求边界、代码质量并入开发规则、回复表达并入根入口。
- 保留 `README.md`、`build-and-test.md`、`development.md`、`git-workflow.md`、
  `request-boundary.md` 五份专题规则。
- 将现有概览移动为 `docs/design-docs/overview.md`，并说明源码发布者的双资产边界。
- 保留 `existing-index`、`explicit-paths`、`explicit-worktree-once` 与 `auto-exact`。

### 非目标

- 不移植 Easydict 的 Xcode、Swift、本地化、PR、lock 或消费方受管快照规则。
- 不新增受管 lock、贡献指南、安装器或发布行为。
- 不修改 completed plan/history 中的旧路径。

## 工作计划

1. 根据 Easydict 两个提交的最终语义重组根入口与五份专题规则，并保留 skills 专属边界。
2. 合并并删除重复规则，移动 architecture 概览至 design-docs，更新活动引用。
3. 创建同任务 history，检查活动旧路径、相对链接和暂存策略关键语义。
4. 运行文档、Skill、Agent 与现有测试校验，归档计划并按自动交付门禁创建本地提交。

## 风险与决策

- 这是语义移植，不复制 Easydict 的消费方路径或历史文件。
- Easydict 的自动暂存措辞不能覆盖当前显式 integration 的 `explicit-worktree-once` 分支。
- 静态文档检查不能证明未来 Agent 的运行时行为、安装器发现或真实 Git 集成。

## 验证

- `python3.12 scripts/validate-skills.py`
- `python3.12 scripts/validate-agents.py`
- `python3.12 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`
- `python3.12 -m unittest discover -s skills/worktree-rebase-merge/tests -p 'test_*.py'`
- `node --test tests/agents-installer.test.mjs`
- 活动文档旧路径、相对链接与关键规则检查
- `git diff --check`

## 进度

- [x] 按 Easydict 最终语义收敛根入口与五份专题规则。
- [x] 移动 architecture 概览至 design-docs，并更新活动路由。
- [x] 创建同任务 history，完成独立复核、静态验证与关键语义检查。
- [x] 准备自动本地提交。

## 完成条件

- 根入口只路由五份专题规则，所有活动链接指向 `docs/design-docs/`。
- 当前 Git 暂存策略和本项目发布者身份保持不变。
- 本任务计划/history 与变更共同验证、精确暂存和本地提交，且未 push。
