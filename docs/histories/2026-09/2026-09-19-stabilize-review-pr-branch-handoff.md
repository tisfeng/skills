# 稳定 review-pr 的分支与工作树交接

- 日期：2026-09-19
- 状态：completed
- 关联计划：[`执行计划`](../../exec-plans/completed/2026-09/2026-09-19-stabilize-review-pr-branch-handoff.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `Unknown`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 目标

修复 review-pr 在同一工作树的多阶段 review 中无显式分支交接、可能静默改选 fallback，以及
无法追溯实际加载 Skill 版本的问题。

## 实际变更

- `prepare-pr-branch.sh` 新增 `--reuse-branch`，严格复验 PR head、upstream、worktree 占用、
  保护分支和允许的 head/fallback 命名；漂移时停止，不自动切换分支。
- 结构化 receipt 增加 `reused_branch` 与 `helper.path`/`helper.sha256`，便于绑定后续阶段和
  发现 Skill 版本漂移。
- `review-pr` 入口和本地准备参考文档明确两阶段 review 必须复用首次 receipt 的分支，且
  `--reuse-branch` 不得与 `--worktree` 混用。
- 增加 4 个回归测试：latest-base 保持已选分支、HEAD 漂移拒绝、非法分支名拒绝、worktree
  组合拒绝；同步覆盖 helper 身份回执。

## 验证

- 57 个 review-pr 单测、2 个 portability 测试通过。
- Skill 校验、quick validation、Python compileall、Shell 语法和 `git diff --check` 通过。
- 未操作真实 PR、远程线程、push、已有 worktree 或用户分支。

## 交付

创建本地 Angular-style 提交，不 push。
