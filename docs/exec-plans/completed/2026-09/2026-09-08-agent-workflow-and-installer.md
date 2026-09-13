# 通用 Agent 工作流与安装器

- 状态：completed
- 创建日期：2026-09-08
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

仓库已发布通用 Skills，但缺少统一的 Agent 工作流、可公开管理的 Codex 子代理以及它们的
项目级/全局级安装方式。

## 目标与非目标

目标：建立通用 `AGENTS.md` 与治理文档；发布四个角色；提供可从 Git 源安装角色的 npm CLI；
将验证接入 CI。

非目标：不复制 Easydict 的 Swift/Xcode、发布、分支或产品规则；不发布 npm 包、GitHub release
或远程 Git 变更；不安装或覆盖用户现有全局配置。

## 授权与范围

- 意图模式：implementation
- 交付授权：none
- 允许路径：`AGENTS.md`、`docs/`、`.codex/agents/`、`bin/`、`src/`、`tests/`、`scripts/`、
  `package.json`、README 与 CI。

## 工作计划

1. 移植并裁剪通用工作流文档。
2. 将 planner、reviewer、tester、git-delivery 作为项目级 Codex agents。
3. 实现带 lock 和冲突保护的 installer。
4. 增加测试、静态校验、README 和 CI。

## 验证

记录实际执行的结构检查、Node installer 测试、既有 Skill 单测与 diff 检查。

## 完成条件

- 路由、角色、安装器和验证文档均已存在。
- 项目级、全局级、冲突拒绝和更新路径有自动化覆盖。
- 未发生 npm 发布、push 或全局配置改动。
