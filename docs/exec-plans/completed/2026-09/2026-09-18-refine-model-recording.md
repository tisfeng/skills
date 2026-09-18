# 优化模型记录规则

- 状态：completed
- 创建日期：2026-09-18
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-5`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 背景

现有模板只接受完整模型 ID，导致运行上下文明示模型别名或基础模型时仍需填写 `Unknown`。
本任务将 Easydict 的最终回退语义同步到 skills 仓库。

## 目标与范围

- 目标结果：将模型字段改为 `Model`，按完整模型 ID、模型别名、基础模型、`Unknown` 的顺序记录。
- 允许修改路径：Plan 与 History 模板、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-18-refine-model-recording.md`
- 用户限制：语义移植，不 push。
- 非目标：不修改公开 Skill 源码、脚本、测试、发现入口、发布资产或既有 completed 记录。
- 验收标准：字段和取值规则与 Easydict 一致，静态检查通过。

## 工作计划

1. 更新 Plan 与 History 模板的模型字段及取值优先级。
2. 检查字段顺序、旧规则残留、相对链接和 Markdown diff。
3. 更新 history，归档计划并创建本地提交。

## 风险与决策

- 字段改为 `Model`，准确容纳完整 ID、别名和基础模型。
- `Auto` 是选择模式而非模型身份；只有 `Auto` 时填写 `Unknown`。
- 不回填既有 completed plan/history，保留历史事实。

## 进度

- [x] 确认来源语义和目标边界。
- [x] 更新 Plan 与 History 模板。
- [x] 完成静态检查和 history；本地提交在计划归档后创建。

## 验证

- 模板检查：两个模板均使用 `Model`，并明确完整 ID、别名、基础模型、`Unknown` 的顺序。
- `Auto` 边界和旧 `Model ID` 字段残留检查：通过。
- 相对链接和 `git diff --check`：通过。
- Skill 校验：未运行；本任务未修改 Skill 源码、脚本、测试或发现入口。

## 完成条件

- [x] 两个模板的字段与取值规则一致。
- [x] 适用的静态检查通过。
- [x] history 已记录结果，计划可以归档并创建本地提交。
