# 稳定 review-pr 的分支与工作树交接

- 状态：completed
- 创建日期：2026-09-19
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `Unknown`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 背景

PR #1277 的审查在同一个 Codex 托管工作树中先创建 PR 同名分支，再在后续
latest-base 阶段切换到 `review/pr-...` 分支。现有 helper 没有把第一次选定的分支作为后续
阶段的显式输入，也没有在回执中记录实际加载的 helper 版本，导致分支选择只能通过 reflog
事后推断。

## 目标与范围

- 目标结果：普通 review 与 latest-base 交接复用已选分支；只有真实冲突才使用 SHA fallback；
  回执能证明分支选择和 helper 版本。
- 允许修改路径：`skills/review-pr/`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-19-stabilize-review-pr-branch-handoff.md`
- 用户限制：只本地修改和验证，不操作真实 PR，不 push。
- 非目标：不删除或重命名现有用户分支，不自动清理 worktree，不改变 PR 远程状态。
- 验收标准：显式复用分支时严格拒绝漂移或不兼容分支；receipt 记录 helper 身份；相关测试、
  Skill 校验、Shell/Python 检查和 diff 检查通过。

## 工作计划

1. 扩展 `prepare-pr-branch.sh`，支持显式复用分支、严格校验和 helper 身份回执。
2. 更新 `review-pr` 的本地准备文档和入口契约，说明两阶段交接规则。
3. 增加现有 helper 测试覆盖回执身份和分支复用。
4. 运行针对性测试、Skill 校验、Shell/Python 检查和 `git diff --check`。
5. 使用 review 审查最终变更，修复有效问题后按规则创建本地提交。

## 风险与决策

- `--reuse-branch` 不尝试修复分支、upstream 或 HEAD 漂移；失败时停止，避免静默切换到另一个
  review 分支。
- fallback 分支仍保留现有 `review/pr-<number>-<head-short-sha>` 命名和保护逻辑。
- helper SHA 只用于可追溯性，不作为运行时授权或远程身份判断。

## 进度

- [x] 完成 helper 和文档修改。
- [x] 完成测试与静态验证。
- [x] 完成最终 review 和本地提交。

## 验证

- `python3.12 -B -m unittest discover -s skills/review-pr/tests -p 'test_*.py'`：57 项通过。
- `python3.12 scripts/validate-skills.py`：6 个 Skill 和发现入口通过。
- `python3.12 -B -m unittest discover -s tests -p 'test_skill_portability.py'`：2 项通过。
- `python3.12 -m compileall -q scripts skills`、`bash -n skills/review-pr/scripts/prepare-pr-branch.sh`、
  `git diff --check`：通过。
- `quick_validate.py skills/review-pr`：通过。
- 未运行真实 GitHub PR、push 或远程 mutation；未删除或重命名已有工作树/分支。

## 完成条件

- 代码、文档和测试变更范围明确且通过验证。
- 计划归档到 `docs/exec-plans/completed/2026-09/`，history 已记录最终结果。
- 本地提交完成，未 push。
