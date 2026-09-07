# 通用 Agent 工作流与安装器

- 日期：2026-09-08
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-08-agent-workflow-and-installer.md`](../../exec-plans/completed/2026-09-08-agent-workflow-and-installer.md)

## 目标

将 Easydict 的通用 Agent 开发框架移植到 Skills，并让 Codex 子代理可独立安装、锁定和更新。

## 实际变更

- 新建根 `AGENTS.md` 和通用 `docs/agents/` 路由、边界、执行、Git、质量与验证规则。
- 新建 `.codex/agents/` 下的 planner、reviewer、tester 与 git-delivery。
- 新建零依赖 Node installer、lock 格式、TOML validator 和覆盖保护测试。
- 在 README、安装说明和 CI 中公开两种资产的独立安装方式。

## 验证

以最终任务实际输出为准，包含 Python 校验、Node installer 测试、既有 Skill 单测和
`git diff --check`。

## 交付

本任务未发布 npm 包、创建 GitHub release、推送代码或修改用户全局 Codex 配置。
