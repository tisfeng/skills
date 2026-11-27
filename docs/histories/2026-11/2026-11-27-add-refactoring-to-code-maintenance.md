# 为 code-maintenance 补充结构重构能力

- 日期：2026-11-27
- 状态：completed
- 关联计划：none

## 执行上下文

- **Agent Name:** `Antigravity`
- **Model:** `Gemini 4 Neon (Medium)`
- **Environment:** `macOS 27.2.1 / Xcode 27.2 (27B52)`

## 目标

让 `code-maintenance` 明确涵盖常见的保行为结构重构场景（拆分过长函数与过重类型、抽取清晰抽象与模块边界），并同步双语 README 目录描述。

## 实际变更

- 更新 `skills/code-maintenance/SKILL.md` 的 `description` 与「简化与重构代码」章节，补充结构重构与模块边界整理指引。
- 同步更新 `README.md` 与 `README.en.md` 中 `code-maintenance` 的目录简介。

## 验证

- `git diff --check` 通过。
- `python3.12 scripts/validate-skills.py` 校验 6 个公开技能、发现入口及双语目录通过。
- `python3.12 -m unittest discover -s tests -p 'test_validate_skills.py' -v` 通过。

## 交付

技能、双语目录与本任务记录随本地提交交付，未执行 push。
