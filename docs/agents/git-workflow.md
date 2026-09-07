# Git 工作流

- Git 操作遵循用户明确的提交、集成、推送和发布授权；implementation 不自动授权远程副作用。
- 未经明确授权，不改变索引、不 push、不 pull、不 rebase、不 merge 或强制移动 ref。
- 显式调用 `git-commit` 时，先阅读 `skills/git-commit/SKILL.md`；显式调用 worktree 集成时，先
  阅读 `skills/worktree-rebase-merge/SKILL.md`。
- 交付前核对实际 diff、允许路径与验证结果。提交仅包含当前任务已获准的内容。
- `git-delivery` 只执行主 Agent 已核验和展示的交付范围；它不修改产品内容，也不自行扩大 staged
  范围。
