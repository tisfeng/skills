# 自动化 npm 发布

- 日期：2026-09-08
- 状态：completed
- 关联计划：none

## 目标

使用 GitHub Actions 和 npm Trusted Publishing 自动发布 `@tisfeng/codex-agents`，避免每次
发布都依赖本地 npm 登录、长期 Access Token 或浏览器二次认证。

## 实际变更

- 新增 tag 驱动的 `publish.yml`，在发布前校验 tag 与 package 版本、确认提交属于 `main`，
  并运行仓库现有 Skills、Agent、Python、Node 和 Shell 检查。
- 发布任务绑定 `npm-production` GitHub Environment，仅授予 OIDC 所需的 `id-token: write`
  和只读仓库权限，通过 Trusted Publishing 执行 `npm publish`。
- npm 发布成功后自动创建对应的 GitHub Release；已存在的 Release 保持不变。
- 为 package 补充 GitHub repository 元数据，使 npm OIDC 发布来源与仓库精确对应。

## 验证

- 本地运行仓库现有 Skills、Agent、Python、Node 和 Shell 检查。
- 使用 `npm pack --dry-run --json` 检查 package 内容。
- 检查工作流 YAML 语法、Git diff 空白错误和最终提交范围。
- OIDC 实际发布留待 npm Trusted Publisher 连接建立后的下一版本 tag 验证。

## 交付

- 创建 `npm-production` GitHub Environment，并限制为 `v*` tag 使用，无人工审批门禁。
- 提交并 push `main`；npm Trusted Publisher 的 `Set up connection` 仍需维护者在 npm
  package 设置页完成一次。
