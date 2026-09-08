# 规范化 npm 仓库 URL

- 日期：2026-09-08
- 状态：completed
- 关联计划：none

## 目标

使用 npm 推荐的 Git URL 格式声明 package 仓库，避免发布时由 npm 临时规范化
`repository.url` 并产生警告。

## 变更

- 将 `package.json` 的 `repository.url` 从普通 HTTPS 地址改为
  `git+https://github.com/tisfeng/skills.git`。
- 保持仓库位置、package 内容、发布 workflow 和现有 `v0.3.1` 产物不变。

## 验证

- `npm pkg fix`：通过，未产生额外规范化变更。
- `npm pack --dry-run`：通过，不再出现 `repository.url` 自动规范化警告。
- `npm run test:agents`：通过。
- Skills、Agents 校验和 `git diff --check`：通过。

## 交付

- 通过 implementation 自动本地提交交付，不 push，不修改或重新发布 `v0.3.1`。
