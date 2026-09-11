# 发布流程

本流程发布本仓库的公开 Skills，由 Git tag 触发 GitHub Actions。请求语义和授权边界以
[内部 release Skill](../../.agents/skills/release/SKILL.md) 为准。

## 准备

只读预检到此报告，不执行发布步骤。

- 工作树和索引干净，完整 `v<上一版本>..HEAD` 范围已审阅，目标 remote 和认证状态明确。
- 目标版本为稳定的 `X.Y.Z`；目标 tag 与 GitHub Release 的占用状态已确认。
- 新发布的 tag 和 GitHub Release 未占用；续办则先核验既有产物身份，按下方恢复规则继续。
  网络、权限或认证错误不是未占用证据，状态不明时停止相关动作。
- 当前仓库的普通 CI 与发布 workflow 可用。

## 执行

1. 确认目标版本；不创建手写版本发布日志。GitHub Release 的标题精确使用目标 tag `vX.Y.Z`，
   正文使用 GitHub 默认生成的 Release Notes。
2. 运行本仓库验证矩阵并冻结候选内容。
3. 按 `git-commit` 创建 Angular-style 发布提交，之后记录完整发布 SHA。复验远程没有漂移后
   push `main`，等待该 SHA 的普通 CI 成功；后续 push、CI 和 tag 均核对该 SHA。
4. 再次核验占用状态，在该发布提交创建并 push annotated `vX.Y.Z` tag。不移动或覆盖公开 tag。
5. tag workflow 复用普通校验，再创建 GitHub Release；显式传入
   `--title "$RELEASE_TAG" --generate-notes`，不传入手写正文。
6. 等待 workflow 完成，核验 tag peeled SHA、GitHub Release 标题等于 tag 且正文为 GitHub
   默认生成内容，以及固定 tag Skills 的隔离安装。
7. 回填真实证据、归档计划，并提交和 push 发布记录。记录可以晚于 tag，不为容纳记录移动 tag。

## 恢复

- main CI 失败：不创建 tag；修复后重新验证并冻结候选。
- 公开 tag 校验失败且需要修改源码：使用下一版本，不移动 tag。
- GitHub Release 创建失败：只恢复 Release 阶段；创建或更新时仍使用精确 tag 标题与 GitHub
  默认生成正文。
- 发布完成但隔离安装失败：如实报告，修复使用新版本。

静态检查和 workflow 配置只能证明流程代码一致；只有实际 CI、Release 和隔离安装才能证明
发布成功。
