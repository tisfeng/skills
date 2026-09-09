# 移植 Easydict Agent 治理文档

- 日期：2026-09-09
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-09-port-easydict-agent-governance.md`](../../exec-plans/completed/2026-09-09-port-easydict-agent-governance.md)

## 目标

语义移植 Easydict 提交 `12f05421dc3edb29f4d7f68c257b293b11ab0be7` 与
`7ade3bcbbb0ad5409af993eab2e3ee8cc2a3b20d` 的最终 Agent 治理结构，并将本项目的
`docs/architecture/` 改名为 `docs/design-docs/`。

## 实际变更

- 将执行安全并入请求边界，代码质量并入新的开发规则，回复和 review 路由并入根入口，收敛为
  根入口和五份专题规则。
- 重写仓库治理、验证和 Git 工作流表达，保留本仓库作为 Skill/agent 源码发布者的职责与两种独立
  安装单元边界。
- 将概览移动为 `docs/design-docs/overview.md`，记录 Agent 资产结构的设计理由；删除旧
  `docs/architecture/` 命名和已合并专题规则。
- 保留 `existing-index`、`explicit-paths`、`explicit-worktree-once` 与 `auto-exact` 四种现有
  暂存策略，不采用 Easydict 消费方的更窄规则。

## 审查与修复

独立 reviewer 发现仓库治理文档错误地将 agent TOML 写成非安装器载荷；已改为明确区分治理文档
与从 Git 源码读取的 Skill/agent 安装载荷。增量复核确认根入口与五份专题规则完整、活动路径无旧
引用，且没有移入 Easydict 的 Xcode、双 lock 或消费方限制。

## 验证

- `python3.12 scripts/validate-skills.py`
- `python3.12 scripts/validate-agents.py`
- `python3.12 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`
- `python3.12 -m unittest discover -s skills/worktree-rebase-merge/tests -p 'test_*.py'`
- `node --test tests/agents-installer.test.mjs`
- 活动路径、相对 Markdown 链接、关键暂存策略与 `git diff --check`

静态验证不能证明 npm 发布、下游安装器发现、Codex 运行时加载或真实 Git integration 行为。

## 交付

本任务按自动本地提交门禁交付；不 cherry-pick、不修改下游副本、受管源码以外的发布配置、锁文件或
安装器，不 push、pull、rebase、merge 或发布。
