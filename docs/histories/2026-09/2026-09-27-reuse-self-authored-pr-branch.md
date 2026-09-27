# 本人 PR 审查复用功能分支

- 日期：2026-09-27
- 状态：completed
- 关联计划：[本人 PR 审查复用功能分支](../../exec-plans/completed/2026-09/2026-09-27-reuse-self-authored-pr-branch.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0 / Xcode 27.2 (27B5019j)`

## 目标

针对 tisfeng/Easydict#1332 的准备记录：功能分支比远程 PR head 多一个未推送提交时，
旧 helper 创建了 review 分支。改为保留本人功能分支，仍准确审查远程 PR 内容。

## 实际变更

- 核实本人 PR 后，相同或落后的同名分支沿用安全准备；领先时保留本地提交，使用冻结 Git 对象
  审查。分叉、错误 upstream 或受保护分支停止，不自动新建 review 分支。
- 支持后续 `--reuse-branch` 复验，以及复用已打开的干净 worktree；目标脏状态停止，调用
  checkout 的分支、HEAD 和文件状态保持不变。
- 准备回执升级到 schema v2，分别记录 checkout 与 review SHA、取证模式、ahead/behind、
  分支选择原因及已有 worktree 复用状态。远程 snapshot schema 维持原版本。
- 更新技能入口、准备、取证和报告协议。补读远程源码使用冻结 SHA；当前领先 checkout 的
  构建和测试不能作为 PR 验证证据。latest-base 仍要求准确远程 head，领先时停止。
- 更新回归用例，实际调用 review 快照采集器证明 diff 包含远程源码且排除本地额外实现。

## 验证

- `python3.12 -m unittest discover -s skills/review-pr/tests -p 'test_prepare_pr_branch.py'`：28 项通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：2 项通过。
- `python3.12 scripts/validate-skills.py`：6 个 Skill 及发现入口校验通过。
- skill-creator 的 `quick_validate.py`、`bash -n`、`python3.12 -m compileall -q scripts skills`
  和 `git diff --check` 通过。
- 使用 review 审查最终实现、测试和协议，未发现可证实的有效缺陷；本地 fixture 验证不代表
  已更新或在真实消费方运行新技能。

## 交付

- 在 skills 仓库创建本地提交，未 push、创建 PR 或发布。
- 未修改消费方安装及 Easydict 分支；下游需要同步新技能才能使用该行为。
