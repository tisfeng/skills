# 新增 code-maintenance 技能

- 日期：2026-11-20
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-11/2026-11-20-add-code-maintenance.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.2.1 / Xcode 27.2 (27B52)`

## 目标

提供一套可跨项目使用的定期代码维护流程，同时处理局部简化、文件组织和有证据支持的废弃代码退役。

## 实际变更

- 新增单文件技能、相对发现链接和双语 README 目录。默认从当前 `HEAD` 选近 7 天内的最多 100 个提交，支持显式提交范围、目录或全仓范围。
- 按请求确定是否修改。沿调用关系确认兼容入口、错误与重试语义、构建目标和资源归属，依据宿主规则验证与交付。

## 验证

- Skill 格式与发现校验、2 个相关 Python 单测、3 个可移植性测试及差异检查通过。
- 临时 Git 仓库分别验证了 7 天窗口、100 个提交上限和显式范围，并核对只读查询前后的工作树与 Git 状态。
- 在 KeepFind `7f4da5b` 的近 100 个候选提交中聚焦导入代码。`collectNonVideo` 可合并 OCR 缓存复用判定，保留无图时 `.skipped`、缓存命中时 `.reused` 和重做时 `.done`。`VideoAnalysisReceipt` 可移入独立文件，保留 `BoardImport` 命名空间并同步主 App 的 Xcode target。
- 沿 `BoardModel`、`BoardImport`、`LinkTransfer` 和相关测试确认了原片发布顺序、结果未知时由用户主动重试、旧续传格式与 `Retry-After` 恢复。试跑前后样本 HEAD、索引和工作树状态一致。验证范围为源码检查和测试阅读。

## 交付

技能、发现入口、目录索引和任务记录随本地提交交付。
