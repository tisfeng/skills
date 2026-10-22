# 统一 PR 英文标题与正文语言规则

- 日期：2026-10-23
- 状态：completed
- 关联计划：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 目标

在 skills 源仓库修改 submit-pr：PR 标题统一使用英文，正文按用户语言偏好生成。
不修改 Easydict 的受管副本，不创建或切换分支。

## 实际变更

- 更新 submit-pr 入口流程，区分英文标题与正文语言。
- 标题的 Angular-style subject 固定使用英文；正文保留原有用户语言解析顺序及仓库正文语言约束。
- 预览前分别核对标题和正文语言；最终报告按用户语言偏好生成，引用标题时保留英文原文。
- 保留 helper 的格式校验职责，不添加启发式语言识别或修改现有测试。
- 本次为范围明确的低风险文档调整，不创建独立执行计划。

## 验证

- `python3.12 scripts/validate-skills.py`：6 个公开 Skill 及仓库发现入口校验通过。
- `python3.12 -m unittest discover -s skills/submit-pr/tests -p 'test_submit_pr.py'`：现有 30 项测试通过。
- skill-creator 的 `quick_validate.py skills/submit-pr`：通过。
- `git diff --check`：通过。
- 手动核对入口、工作流契约和公开说明：移除标题跟随首选语言的旧要求，正文语言规则一致。

## 交付

- 在既有 main 分支完成本地提交；未创建或切换分支。
- 仅修改源仓库的 submit-pr 文档与本 history；未发布、push 或同步 Easydict 受管副本。
