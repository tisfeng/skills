# 统一版本化文档命名

- 日期：2026-09-16
- 状态：completed
- 关联计划：none
- 来源提交：`easykol-scout-extension@979863ef1739a0cad5d0797449b1be128ae9c22a`

## 目标

将 EasyKOL Scout 的版本化文档命名修正语义移植到 skills，同时保留本仓库的文档生命周期边界。

## 实际变更

- 精简 `<slug>` 规则，保留 kebab-case、完整标准标识和禁用字符三项约束。
- 检查现有 plan 与 history 文件名，确认没有需要迁移的连字符版本标识。

## 验证

- 本次变更文件的 Markdown 相对链接检查：通过。
- `git diff --check`：通过。
- 连字符版本文件名与引用检查：无残留。

## 交付

- 创建本地 Angular-style 提交，不 push。
