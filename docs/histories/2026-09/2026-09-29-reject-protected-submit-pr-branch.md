# 提交 PR 时拦截当前保护分支

- 日期：2026-09-29
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09/2026-09-29-reject-protected-submit-pr-branch.md)

## 执行上下文

- **Agent Name:** `Unknown`
- **Model:** `Unknown`
- **Environment:** `macOS 27.0 / Xcode 27.2 (27B5019j)`

## 目标

当当前分支与动态解析的 PR base 或 GitHub default branch 同名时，提交 PR 技能须先提示用户创建并切换到新的任务分支；同名 fork head 也须拒绝。

## 实际变更

- 新增只读 `preflight` helper 命令，在提交 staged 内容前解析 base/default 并拦截当前保护分支；`plan` 和 `apply` 内部重复检查，`apply` 在 fetch 前停止。
- 错误信息要求用户从当前提交创建并切换到新任务分支后重试，说明既有提交会保留；head 与 base/default 同名时跨 fork 也拒绝。
- 更新 `submit-pr` 入口与工作流契约，规定调用顺序、停止提示和 detached checkout 参数。
- 增加 base/default、替代 head、apply 无 fetch/PR 写入和跨 fork 同名等回归覆盖。

## 验证

- `python3.12 -m unittest discover -s skills/submit-pr/tests -p 'test_*.py'`：29 项通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：2 项通过。
- `python3.12 scripts/validate-skills.py`：通过，校验 6 个 Skill 与发现入口。
- `python3.12 -m compileall -q scripts skills`、`skill-creator` 的 `quick_validate.py skills/submit-pr`、`git diff --check`：通过。
- 按 `review` 技能审查最终实现无 finding；修正 detached checkout 指引遗漏后重新验证通过。

## 交付

- 按仓库规则创建本地提交；未 push、未创建或修改 GitHub PR、未发布 Skill。
