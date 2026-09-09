# 对齐 worktree 集成暂存规则

- 日期：2026-09-09
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-09-align-worktree-staging.md`](../../exec-plans/completed/2026-09-09-align-worktree-staging.md)

## 目标

消除 `git-commit` 与 `worktree-rebase-merge` 对空索引显式交付的冲突，使明确、未限定范围的
worktree integration 可安全执行一次 `git add .`，同时保持 implementation 自动本地提交仅精确暂存。

## 实际变更

- 在 `git-commit` 集中定义 `existing-index`、`explicit-paths`、`explicit-worktree-once` 与
  `auto-exact` 四种暂存策略，要求预检冻结候选并在暂存后以 staged raw patch 重验。
- 让 worktree 提交路径复用该决策矩阵；删除空索引一律暂停的覆盖规则。
- 扩展 `git-delivery` 输入与 prepare/apply 协议，使主 Agent 冻结暂存策略，交付 Agent 不自行推断。
- 更新仓库 Git 交付规则，明确全工作树显式候选与自动精确候选的授权边界。
- 新增 worktree 暂存契约测试，并加入 CI。

## 验证

- `python3.12 scripts/validate-skills.py`
- `python3.12 scripts/validate-agents.py`
- `python3.12 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`
- `python3.12 -m unittest discover -s skills/worktree-rebase-merge/tests -p 'test_*.py'`
- `node --test tests/agents-installer.test.mjs`
- `git diff --check`

静态契约测试验证发布的规则层一致性；它不能证明未来 Agent 的每一次实际 Git 操作都遵守该策略。

## 交付

本任务按仓库自动本地提交门禁交付；不 push、pull、rebase、merge、发布或修改下游安装副本。
