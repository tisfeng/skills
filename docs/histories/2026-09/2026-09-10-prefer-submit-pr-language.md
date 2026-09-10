# 统一 submit-pr 的用户语言选择

- 日期：2026-09-10
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-10-prefer-submit-pr-language.md)
- 关联 PR：[#1](https://github.com/tisfeng/skills/pull/1)

## 目标与变更

用户要求解释 PR #1 的英文正文来源，并在确认方案后授权实施。根因是 `submit-pr` 只要求调用
Agent 起草 title、Summary 和 Verification，没有规定用户首选语言；Python helper 始终原样使用
这些参数，并未强制英语或自动翻译。

- 新增 PR 用户语言契约：显式偏好优先，其次为当前对话、用户系统首选语言，最后兜底英语。
- 目标仓库明确的 PR 语言要求继续作为独立硬约束；英文模板、提交信息、分支名或终端 locale
  不能覆盖已经确定的对话语言。
- PR 默认使用一种首选语言，技术标识及模板原有 headings、说明、checklist 和固定结构保持原文。
- `SKILL.md` 要求在 helper plan 前显示语言及来源并检查正文一致性。helper 不新增语言参数，继续
  只负责校验、模板渲染、GitHub 写入和状态验证。
- 新增真实 helper plan/apply fixture，验证中文 Angular title、Summary 和 Verification 在 fake
  GitHub 中保持不变；已有英文 PR 用中文内容重试时仍停止，PR 对象不被覆盖且不重复创建。

## 验证

- `git-commit` 19 项、`worktree-rebase-merge` 9 项、`review-pr` 27 项、`submit-pr` 29 项和
  Agent installer 6 项通过，共 90 项自动化测试。
- `scripts/validate-skills.py` 验证 6 个 Skill，`scripts/validate-agents.py` 验证 3 个 Codex agent。
- Python 编译、review-pr Shell 语法和 `git diff --check` 通过。
- `skill-creator` quick validator 在系统与工作区 Python 中均因缺少 `PyYAML` 未启动；没有安装或
  修改环境，本仓库结构校验已通过。
- 独立只读 reviewer 未发现明确 finding。测试证明 helper 的 Unicode 保真和防覆盖行为，但自然
  语言选择仍由运行时 Agent 依据上下文执行，不能由 deterministic helper 单测证明。

## 交付边界

本任务不修改 Python helper、`git-commit`、分支结构、提交历史或发布配置，不 merge 或发布。
本地提交后使用现有 `submit-pr` 流程安全快进当前任务分支，并对已冻结的 PR #1 进行一次窄范围
title/body 修正及读回核验。
