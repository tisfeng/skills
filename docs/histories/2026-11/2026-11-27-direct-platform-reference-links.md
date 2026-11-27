# 将平台指南提升为 code-maintenance 一跳直链

- 日期：2026-11-27
- 状态：completed
- 关联计划：none

## 执行上下文

- **Agent Name:** `Antigravity`
- **Model:** `Gemini 4 Neon (Medium)`
- **Environment:** `macOS 27.2.1 / Xcode 27.2 (27B52)`

## 目标

让 `code-maintenance` 的所有代码维护分支（包括文件职责拆分、移动文件和退役代码）都能从主入口一跳直达 Swift/Xcode 与 Electron/TypeScript 平台指南，避免因藏在二级引用而漏加载。

## 实际变更

- 在 `skills/code-maintenance/SKILL.md` 的「清理代码」章节直接列出 `references/swift-xcode.md` 与 `references/electron-typescript.md`，说明涉及对应技术栈的代码维护时按需读取。
- 移除 `skills/code-maintenance/references/code-simplifier.md` 中重复的「平台规则」二级链接小节，保持单一来源。

## 验证

- `git diff --check` 通过。
- `python3.12 scripts/validate-skills.py` 校验 6 个公开技能及发现入口通过。
- `python3.12 -m unittest discover -s tests -v` 全部 5 项单测（含可移植性与 Markdown 链接闭包测试）通过。

## 交付

改动与本任务记录随本地提交交付，未执行 push。
