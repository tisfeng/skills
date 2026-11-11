# 支持 CLI 新建 PR 附图并锁定非截图正文

- 日期：2026-11-11
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-11/2026-11-11-submit-pr-cli-screenshot-creation.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.2.1 / Xcode Unknown (Unknown)`

## 目标

恢复无浏览器环境的新建 PR 截图交付，并确保补传复验只允许截图区域发生变化。

## 实际变更

- `apply --screenshot-file` 在新建 PR 时使用 GitHub CLI 上传，并读回验证已上传附件。部分上传时返回已上传和缺失的截图，重试复用已创建的 PR。
- apply 回执包含非截图正文摘要，补传计划和复验都会检查。缺少摘要的旧回执无法用于补传。

## 验证

- 34 个 submit-pr 测试、3 个可移植性测试、Skill 校验、Python 编译和差异检查通过。
- 本地模拟覆盖完整上传、部分上传、全部失败、幂等重试及非截图正文漂移。未实际上传到 GitHub。

## 交付

仓库版 Skill 随本地提交交付。未推送或更新全局安装。
