# 将版本 changelog 作为 Release 正文来源

- 日期：2026-09-27
- 状态：completed
- 关联计划：[版本 changelog 发布流程](../../exec-plans/completed/2026-09/2026-09-27-require-release-changelog.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0 / Xcode 27.2 (27B5019j)`

## 目标

每个发布版本维护简短中文 changelog，GitHub Release 直接使用该文档全文，避免只剩比较链接。

## 实际变更

- 发布流程要求 `release/changelog/X.Y.Z.md` 随发布提交进入 tag；正文规范集中在目录 README。
- workflow 校验版本号、日志文件、更新条目和比较链接，以 `--notes-file` 创建 Release。
- 查询采用完整分页并在 API 失败时停止；创建后与重跑时均核验标题和正文，不一致不自动覆盖。
- 补录 v0.6.2 现有正文，以及根据版本范围整理的 v0.6.3、v0.7.0 更新摘要；旧 tag 不变。
- 明确历史补录和线上回填的区别，保留 CI 复用及隔离安装验收流程。

## 验证

- workflow YAML 解析、全部 Shell 块 `bash -n`、内嵌 Python 编译检查通过。
- 直接运行 workflow 日志预检，v0.6.2、v0.6.3、v0.7.0 均通过；缺少 v0.7.1 日志时退出 1。
- 只读查询真实 GitHub Release，并运行 workflow 的正文比对表达式：v0.6.2 一致；v0.6.3、
  v0.7.0 按预期报告不一致，确认线上仍缺摘要。本次未回填线上正文。
- `git diff --check`、变更文档相对链接和记录文件名检查通过。
- 按 review 技能审查相对 `81d823c01f19c6952502e562001edb7a6bad0511` 的任务变更，覆盖
  新文件、缺失日志、创建、重跑、API 错误与正文差异路径，未发现有效 finding。直接读取版本
  文档并使用标准 CLI 参数已足够，无需新增发布工具或依赖。
- 未新增测试代码；未运行实际 GitHub Actions 发布、Release 创建或固定 tag 安装，本次结果不
  代表真实发布端到端验证。

## 交付

规则、workflow、近期日志及任务记录一并本地提交；不 push、不发布、不修改线上 Release。
