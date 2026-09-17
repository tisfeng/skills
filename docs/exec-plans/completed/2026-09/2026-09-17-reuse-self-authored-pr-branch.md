# 复用本人 PR 的本地同名分支

- 状态：completed
- 创建日期：2026-09-17
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model ID:** `Unknown`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 背景

`review-pr` 原先按 upstream 短名称做严格字符串比较。本地同名分支即使跟踪的是指向同一 PR
head repository 的 `origin/<branch>`，也会因不等于 `<head-owner>/<branch>` 被判定为 collision，
继而创建 `review/pr-*` 分支。用户希望审查本人提交的 PR 时安全复用本地同名分支。

## 目标与范围

- 目标结果：当前 GitHub 用户本人提交的 PR 可以复用安全的本地同名分支，并保留现有保护边界。
- 允许修改路径：`skills/review-pr/`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-17-reuse-self-authored-pr-branch.md`
- 用户限制：仅本人 PR 放宽；不得覆盖、reset、rebase、强制更新或 push。
- 非目标：改变他人 PR、显式 worktree、latest-base 授权、线程维护或远程 mutation 行为。
- 验收标准：本人 PR 的等价 upstream 或无 upstream 同名分支可安全切换并 fast-forward；其他不安全状态仍 fallback 或停止。

## 工作计划

1. 将 PR 作者加入直接元数据和保存快照的准备路径。
2. 在同名分支发生 upstream mismatch 时惰性确认当前 GitHub 用户，并校验 upstream 的仓库与分支语义。
3. 复用本人 PR 的安全同名分支；无 upstream 时设置准确 PR head upstream；保留所有现有 collision 保护。
4. 更新本地准备、证据和报告契约及结构化回执验证。
5. 补充本人/他人、等价/缺失/错误 upstream 和安全 fallback 的行为测试。
6. 完成针对性与仓库级验证，使用 `review` 复审，修复有效 finding 后重新验证。

## 风险与决策

- GitHub 身份使用 PR `author.login` 与 `gh api user` 的当前登录名比较，不使用本地 Git 姓名或邮箱。
- 当前用户查询仅在现有同名分支因 upstream 不匹配而可能 fallback 时发生；查询失败则保持旧 fallback。
- 等价 upstream 必须同时匹配准确 head branch 与 head repository URL；remote 别名本身不作为身份。
- 本地分支领先、分叉、跟踪其他仓库/分支、被其他 worktree 占用或工作树不干净时不放宽。
- 保存快照缺少或包含异常作者信息时保持旧 fallback，不猜测 PR 归属。

## 进度

- [x] 定位严格 upstream 名称比较与最终验证路径。
- [x] 实现作者身份和语义 upstream 校验。
- [x] 更新契约文档和行为测试。
- [x] 完成验证、Review、history 与本地提交准备。

## 验证

- `bash -n skills/review-pr/scripts/prepare-pr-branch.sh`：通过。
- `python3.12 -m unittest discover -s skills/review-pr/tests -p 'test_*.py'`：53 个测试通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：2 个测试通过。
- `python3.12 scripts/validate-skills.py`：通过，验证 6 个 Skill 与发现入口。
- `python3.12 -m compileall -q scripts skills`：通过。
- `uv run --python 3.12 --with 'PyYAML==6.0.3' .../quick_validate.py skills/review-pr`：通过；PyYAML 仅用于临时校验环境。
- `git diff --check`：通过。
- `review`：修复异常快照作者类型的安全降级与回执契约遗漏后复审，无剩余 finding。

## 完成条件

- [x] 目标行为和安全 fallback 均有可复现实证。
- [x] 相关验证与适用 Review 通过。
- [x] history 已记录最终结果，计划已归档并准备创建 Angular-style 本地提交。
