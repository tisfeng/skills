# 修复 submit-pr 截图补传和复验

- 日期：2026-11-11
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-11/2026-11-11-fix-submit-pr-screenshot-delivery.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.2.1 / Xcode Unknown (Unknown)`

## 目标

修复截图补传期间的正文覆盖风险、复验对当前 Git 引用的依赖，以及非 UI 验证截图无法复用的问题。

## 实际变更

- 先在未保存的 PR 编辑器中取得附件 URL，再复验远程正文并立即保存。读取与保存之间仍存在短暂竞态。
- 使用原始 apply 回执渲染及复验补图后的正文，固定 PR 身份和 head SHA。
- 允许非 UI 改动直接嵌入已有验证截图。无截图且无缺口时使用 `N/A`。

## 验证

- 34 个 submit-pr 测试、3 个可移植性测试、Skill 校验、Python 编译和差异检查通过。
- 本地定向模拟确认正文漂移与 head 漂移会被拒绝，缓存 base 前进不影响复验，非 UI 截图可嵌入。
- 未操作真实 GitHub PR 或上传附件。

## 交付

仓库版 Skill 随本地提交交付。未推送或更新全局安装。
