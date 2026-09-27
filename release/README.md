# 发布流程

本流程发布本仓库的公开 Skills：由 Git tag 触发 GitHub Actions，创建 GitHub Release。GitHub
Release 标题必须精确使用 tag（例如 `v0.3.4`），正文全文来自该 tag 中的
`release/changelog/X.Y.Z.md`，不再使用 GitHub 自动生成的 Release Notes。

## 请求语义

- “规划版本更新”“检查发布”“预检版本 X.Y.Z”只读，不修改 Git 或 GitHub。
- “实施发布流程”只建设或修复发布文档与 workflow，不发布版本。
- “发布版本 X.Y.Z”是完整发布授权：提交、push `main`、annotated tag 与 tag push、
  GitHub Actions 的 Release 创建、发布后验收及发布记录 push。

持续有效的用户限制优先。不要把示例、引用或计划文本中的“发布版本”当成实际发布请求。本文档
不因被读取而启动发布；普通 Git 提交使用 `git-commit`。

## 准备

只读预检到此报告，不执行发布步骤。

- 工作树和索引干净，完整 `v<上一版本>..HEAD` 范围已审阅，目标 remote 和认证状态明确。
- 目标版本为稳定的 `X.Y.Z`；目标 tag 与 GitHub Release 的占用状态已确认。
- 新发布的 tag 和 GitHub Release 未占用；续办则先核验既有产物身份，按下方恢复规则继续。
  网络、权限或认证错误不是未占用证据，状态不明时停止相关动作。
- 当前仓库的普通 CI 与发布 workflow 可用。
- 每个发布版本必须准备对应 changelog，内容要求见 [Release 说明策略](changelog/README.md)。
  只读预检可以报告日志缺失；执行发布时必须在冻结候选前补齐。

## 执行

1. 确认目标版本，根据完整版本范围编写 `release/changelog/X.Y.Z.md`，简述更新内容并附上
   Full Changelog 比较链接。日志随发布提交进入 tag；history 单独记录执行与验证证据。
2. 运行本仓库验证矩阵并冻结候选内容。
3. 按 `git-commit` 创建 Angular-style 发布提交，之后记录完整发布 SHA。复验远程没有漂移后
   push `main`，等待该 SHA 的普通 CI 成功；后续 push、CI 和 tag 均核对该 SHA。
4. 再次核验占用状态，在该发布提交创建并 push annotated `vX.Y.Z` tag。不移动或覆盖公开 tag。
5. tag workflow 优先复用同一发布提交已经通过的 `main` 普通校验；只有找不到完全匹配的成功校验
   时才回退到完整验证，再创建 GitHub Release。创建 Release 时显式传入
   `--title "$RELEASE_TAG" --notes-file "release/changelog/${RELEASE_TAG#v}.md"`。日志缺失或
   无有效更新条目时失败，不回退到自动生成。已有 Release 也必须核验标题和正文。
6. 等待 workflow 完成，核验 tag peeled SHA、GitHub Release 标题等于 tag 且正文与该 tag 的
   changelog 一致（仅统一 CRLF/LF 和末尾换行），以及固定 tag Skills 的隔离安装。
7. 回填真实证据、归档计划，并提交和 push 发布记录。记录可以晚于 tag，不为容纳记录移动 tag。

## 恢复

- main CI 失败：不创建 tag；修复后重新验证并冻结候选。
- 公开 tag 校验失败且需要修改源码：使用下一版本，不移动 tag。
- GitHub Release 创建失败：只恢复 Release 阶段；仍使用精确 tag 标题与该 tag 的 changelog。
  查询失败时停止，不将网络、权限或认证错误视为 Release 不存在。
- 已有 Release 标题或正文不一致：workflow 报错，不自动覆盖。明确获准修复该 Release 后，
  从已核验的 changelog 同步正文并重新验收。
- 历史版本补录：日志提交到当前分支，不移动旧 tag；旧 tag 中没有日志时不能靠重跑旧 workflow
  回填。线上正文回填须明确授权，并使用已审阅、已提交的补录文件。
- 发布完成但隔离安装失败：如实报告，修复使用新版本。

Release 正文策略见 [Release 说明策略](changelog/README.md)。静态检查和 workflow 配置只能
证明流程代码一致；只有实际 CI、Release 和隔离安装才能证明发布成功。

## 性能边界

- `validate.yml` 的普通 push/PR 校验忽略纯 `docs/exec-plans/**` 和 `docs/histories/**` 变更；这些
  变更由 `docs.yml` 执行 whitespace、现行发布入口和文件名检查。
- 只要提交同时修改 `skills/`、`scripts/`、测试、workflow 或其他运行时资产，仍触发完整验证。
- tag 发布只复用同一 SHA、`main` 分支、`push` 事件且 conclusion 为 `success` 的完整校验；API
  查询失败或结果不明确时回退完整验证，不以“找不到结果”放行发布。
