# 发布流程

本流程发布 `@tisfeng/codex-agents`，由 Git tag 触发 GitHub Actions Trusted Publishing。
请求语义和授权边界以 [内部 release Skill](../../.agents/skills/release/SKILL.md) 为准。

## 准备

先委派并等待只读 `planner`，核对以下事实；只读预检到此报告，不执行发布步骤。

- 工作树和索引干净，完整 `v<上一版本>..HEAD` 范围已审阅，目标 remote 和认证状态明确。
- 目标版本为稳定的 `X.Y.Z`；当前 package 版本及目标 tag/npm/Release 占用状态已确认。
- 新发布的 tag、npm 版本和 GitHub Release 未占用；续办则先核验既有产物身份，按下方恢复规则
  继续。网络、权限或认证错误不是未占用证据，状态不明时停止相关动作。
- 当前仓库的普通 CI、发布 workflow 和 npm production 环境可用。

## 执行

1. 更新 `package.json` 并创建 `docs/release/changelog/X.Y.Z.md`；日志只记录实际面向用户的
   变更，版本与目标 tag `vX.Y.Z` 一致。
2. 运行发布相关完整验证与 `npm pack --dry-run`，记录候选包摘要并冻结待发布内容。
3. 按 `git-commit` 创建 Angular-style 发布提交，之后记录完整发布 SHA。复验远程没有漂移后
   push `main`，等待该 SHA 的普通 CI 成功；后续 push、CI 和 tag 均核对该 SHA。
4. 再次核验占用状态，在该发布提交创建并 push annotated `vX.Y.Z` tag。不移动或覆盖公开 tag。
5. tag workflow 验证 tag、发布提交和日志，再发布 npm 包并创建 GitHub Release；Release 正文
   使用同版本 changelog。
6. 等待 workflow 完成，核验 npm 精确版本与 `latest`、tag peeled SHA、GitHub Release、包摘要/
   签名，以及固定 tag Skills 和精确 npm agents 的隔离安装。
7. 回填真实证据、归档计划，并提交和 push 发布记录。记录可以晚于 tag，不为容纳记录移动 tag。

## 恢复

- main CI 失败：不创建 tag；修复后重新验证并冻结候选。
- 公开 tag 校验失败且需要修改源码：使用下一版本，不移动 tag。
- npm 状态不明：先查询 registry 与 workflow，不重复 publish。
- npm 已成功而 GitHub Release 失败：只恢复 Release 阶段。
- 发布完成但隔离安装失败：如实报告，修复使用新版本。

静态检查和 workflow 配置只能证明流程代码一致；只有实际 CI、registry、Release 和隔离安装
才能证明发布成功。
