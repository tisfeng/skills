# 补齐 submit-pr 的关联证据和截图交付

- 状态：completed
- 创建日期：2026-11-11
- 负责人：Codex
- 关联 Issue/PR：[Easydict #1399](https://github.com/tisfeng/Easydict/pull/1399)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.2.1 / Xcode Unknown (Unknown)`

## 背景

PR 正文遗漏了直接相关的历史 PR，且 helper 会用补图提示覆盖截图区域。

## 目标与范围

- 目标结果：补查相关 Issue 和 PR，交付已有截图并验证最终正文。
- 允许修改路径：`skills/submit-pr/` 以及本任务的 plan 和 history。
- 同任务 history：`docs/histories/2026-11/2026-11-11-submit-pr-evidence.md`
- 用户限制：仅本地提交，不 push、不创建 PR。
- 非目标：修改 Easydict PR #1399。
- 验收标准：覆盖关联 PR、截图、缺图、非 UI 及幂等重试。

## 工作计划

1. 核对维护源、helper、模板、测试与 GitHub 附件流程。
2. 实现固定正文输入和只读回读，补充取证与附件操作契约。
3. 验证并审查最终差异，归档并本地提交。

## 风险与决策

- 保持 Issue 自动关闭策略和 PR 正文比对，附件上传由调用 Agent 使用 GitHub 支持的方式完成。

## 进度

- [x] 核对现有契约和案例。
- [x] 实现并验证。
- [x] 审查和归档。

## 验证

submit-pr 的 34 个测试和 3 个可移植性测试通过。Skill 校验、Python 编译和差异检查通过。
通过本地模拟验证附件补传后的正文回读，实际 GitHub 上传和图片显示未在本次任务执行。

## 完成条件

- 验证通过，review 完成，history 与归档 plan 纳入本地提交。
