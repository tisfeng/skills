# 补齐 submit-pr 的关联证据和截图交付

- 日期：2026-11-11
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-11/2026-11-11-submit-pr-evidence.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.2.1 / Xcode Unknown (Unknown)`

## 目标

在预览前补查直接解释改动来由的 Issue 和 PR，并把已有截图交付到 PR 正文。

## 实际变更

- 规定从任务上下文、Git 历史和 GitHub 核对关联证据。固定正文的关联区域支持 Issue 关系说明和单独的 `--related-pr` 输入。
- 支持截图 URL、部分缺图提示及 `plan --verify-pr` 只读正文回读。附件上传由调用 Agent 通过 GitHub 支持的流程完成。
- 规定创建后补传时如何保留现有正文和附件、核对不确定的写入结果并验证图片显示。

## 验证

- 34 个 submit-pr 测试与 3 个可移植性测试通过。Skill 校验、Python 编译和差异检查通过。
- 现有截图、缺图、非 UI、关联 PR、补传后回读和重试通过本地测试覆盖。真实上传及 GitHub 渲染未执行。

## 交付

源码、测试和任务记录随本地提交交付。未 push、创建 PR 或修改 Easydict 案例。
