# 发布流程

本流程发布 `@tisfeng/codex-agents`，由 Git tag 触发 GitHub Actions Trusted Publishing。发布请求、
权限边界和失败续办以 [内部 release Skill](../../.agents/skills/release/SKILL.md) 为准。

## 准备

发布版本必须是稳定的 `X.Y.Z`，并且满足以下条件：

- 工作树和索引干净，待发布范围已从上一公开 tag 审阅。
- `package.json` 的版本、`docs/release/changelog/X.Y.Z.md` 与目标 tag `vX.Y.Z` 一致。
- 远程 tag、npm 版本和 GitHub Release 未占用；网络、权限或认证错误不是未占用证据。
- 当前仓库的普通 CI、发布 workflow 和 npm production 环境可用。

## 执行

1. 更新版本和对应发布日志，运行发布相关验证与 `npm pack --dry-run`。
2. 创建发布提交并 push `main`，等待该提交的普通 CI 通过。
3. 创建并 push annotated `vX.Y.Z` tag。
4. tag workflow 先验证 tag、发布提交和发布日志，再发布 npm 包并创建 GitHub Release。
5. 核验 tag、npm `latest`、GitHub Release 和隔离安装；最后回填实际发布证据。

GitHub Release 使用同版本的 changelog 文件作为正文。发布记录提交可以晚于 tag；公开 tag 一经创建
不得移动。

## 恢复

main CI 失败时不要创建 tag。公开 tag 需要源码修正时发布新版本。npm 发布状态不明时先查询 registry
和 workflow；npm 已成功而 GitHub Release 失败时只恢复 Release。任何安装验收失败都必须如实报告，
不能把静态检查写成发布成功。
