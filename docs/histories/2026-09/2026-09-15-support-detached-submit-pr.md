# 支持 detached checkout 提交 PR

- 日期：2026-09-15
- 状态：completed
- 关联计划：[支持 detached checkout 提交 PR](../../exec-plans/completed/2026-09/2026-09-15-support-detached-submit-pr.md)

## 目标

让 `submit-pr` 在 detached checkout 中按现有 Conventional 分支命名契约继续工作：调用 Agent
自动推导并传入任务分支名，helper 只读预览或从冻结 HEAD 创建分支 ref，且不切换 checkout。

## 实际变更

- 更新 Skill 入口和工作流契约：用户或项目命名优先，否则按任务与只读 diff 生成
  `<type>/<english-kebab-case-summary>`；helper 不从 PR 标题机械猜测名称。
- helper 以可空当前分支解析仓库拓扑；detached 状态跳过 branch-scoped base、push remote 和 upstream
  配置，继续使用显式参数及现有 repository/default fallback。
- `plan` 对 detached checkout 输出 `current_branch: null` 及 `would-create`、`would-update` 或
  `would-reuse`，不创建 ref；`apply` 创建、更新或复用冻结 HEAD 的本地 ref，并保持 checkout detached。
- 本地分支写入前复验 attached/detached 状态和 HEAD，保留 `git branch -f` 对其他 worktree 已检出分支
  的保护；现有保护分支、冲突后缀和禁止 force push 行为不变。
- 新增 detached 只读性、缺失名称、branch-scoped 配置跳过、冲突后缀、apply/重复 apply、状态漂移
  和独立安装场景的行为测试。

## 验证

- `python3.12 -m unittest discover -s skills/submit-pr/tests -p 'test_*.py'`：23 项通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：2 项通过。
- `python3.12 scripts/validate-skills.py`：6 个公开 Skill 与仓库发现入口通过。
- `python3.12 -m compileall -q scripts skills`：通过。
- `skill-creator` 的 `quick_validate.py skills/submit-pr`：使用已有且包含 PyYAML 的 Python 环境通过；
  项目的 `python3.12` 缺少该 validator 自身的 PyYAML，未修改项目依赖。
- `git diff --check`：通过。
- 未运行真实 GitHub PR 创建或复用流程；集成测试使用临时 Git 仓库和模拟 GitHub。

## 交付

仅创建本地提交；未 push、未创建真实 PR、未发布版本、未修改全局 Skill 安装。
