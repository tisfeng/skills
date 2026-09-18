# 优化模型记录规则

- 日期：2026-09-18
- 状态：completed
- 关联计划：[`2026-09-18-refine-model-recording.md`](../../exec-plans/completed/2026-09/2026-09-18-refine-model-recording.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-5`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 目标

将 Easydict 优化后的模型记录回退规则语义移植到 skills 仓库，同时保留精简记录结构。

## 实际变更

- 将 plan 与 history 模板的 `Model ID` 字段改为 `Model`。
- 明确取值顺序为完整模型 ID、模型别名、基础模型、`Unknown`。
- 明确只有 `Auto` 等选择模式时填写 `Unknown`。

## 验证

- 模板字段、占位符、取值优先级和 `Auto` 边界检查：通过。
- 旧 `Model ID` 字段残留检查：通过。
- 相对链接和 `git diff --check`：通过。
- Skill 校验：未运行；本任务未修改 Skill 源码、脚本、测试或发现入口。

## 交付

- 本计划与 history 随模板变更创建独立 Angular-style 本地提交，不执行 push。
