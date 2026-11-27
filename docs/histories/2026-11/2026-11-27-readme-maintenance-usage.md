# 补充双语 README 中 code-maintenance 的推荐用法

- 日期：2026-11-27
- 状态：completed
- 关联计划：none

## 执行上下文

- **Agent Name:** `Antigravity`
- **Model:** `Gemini 4 Neon (Medium)`
- **Environment:** `macOS 27.2.1 / Xcode 27.2 (27B52)`

## 目标

在双语 README 中简明说明 `code-maintenance` 的默认只读巡检行为以及每周定时运行、定向重构的推荐使用方式。

## 实际变更

- 在 `README.md` 与 `README.en.md` 的补充说明小节增加 `code-maintenance` 的推荐用法条目。

## 验证

- `git diff --check` 通过。
- `python3.12 scripts/validate-skills.py` 校验 6 个公开技能、发现入口及双语目录通过。

## 交付

文档改动与本任务记录随本地提交交付，未执行 push。
