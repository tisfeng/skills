---
name: release
description: 发布当前 skills 仓库的版本；用于明确的“发布版本 X.Y.Z”、发布预检或发布续办，不用于普通 Git 提交。
---

# 发布版本

仅用于当前仓库的 `@tisfeng/codex-agents` 发布。它是项目内 Skill，不是 `skills/` 目录中可复用的
公开 Skill。执行前阅读 [发布流程](../../../docs/release/overview.md)；具体版本的发布日志位于
[`docs/release/changelog/`](../../../docs/release/changelog/README.md)。

## 请求语义

- “规划版本更新”“检查发布”“预检版本 X.Y.Z”只读，不修改 Git、npm 或 GitHub。
- “实施发布流程”只建设或修复本 Skill、发布文档和 workflow，不发布版本。
- “发布版本 X.Y.Z”是完整发布授权：版本和日志修改、提交、push `main`、annotated tag 与 tag push、
  GitHub Actions 的 npm 发布和 GitHub Release、发布后验收及发布记录 push。

持续有效的用户限制优先。不要把示例、引用或计划文本中的“发布版本”当成实际发布请求。

## 发布步骤

1. 先委派并等待只读 `planner`，再记录干净工作树、完整 `v<上一版本>..HEAD` 范围、目标 remote、
   package 版本、目标 tag/npm/Release 占用和认证状态。查询失败或状态不明时停止，不把它当作未占用。
2. 只接受稳定的 `X.Y.Z` 版本。更新 `package.json` 并创建
   `docs/release/changelog/X.Y.Z.md`；日志只记录实际面向用户的变更，且必须与版本一致。
3. 按发布流程运行完整验证和 `npm pack --dry-run`，冻结候选 tarball 摘要与发布提交 SHA。
4. 创建 Angular-style 发布提交，复验远程没有漂移后 push `main`，等待该 SHA 的普通 CI 成功。
5. 再次核验占用状态，在发布提交创建并 push annotated `vX.Y.Z` tag。不要移动或覆盖公开 tag。
6. 等待 tag workflow 完成，分别核验 npm 精确版本和 `latest`、tag peeled SHA、GitHub Release、
   包摘要/签名，以及固定 tag Skills 与精确 npm agents 的隔离安装。
7. 回填真实证据、归档 plan 和提交发布记录；记录可以晚于 tag，但不得为容纳记录移动 tag。

## 失败续办

- main CI 失败：不创建 tag；修复后重新冻结候选。
- 公开 tag 的校验失败且需要改源码：使用下一版本，不移动 tag。
- npm 状态不明：先查 registry 与 workflow，不重复 publish。
- npm 已成功而 Release 失败：只恢复 Release 阶段。
- 发布完成但隔离安装失败：如实报告，修复使用新版本。

静态检查和 workflow 配置只能证明流程代码一致；只有实际运行的 CI、registry、Release 与隔离安装
才能证明一次发布成功。
