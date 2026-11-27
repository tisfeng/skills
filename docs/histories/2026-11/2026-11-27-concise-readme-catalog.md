# 精简双语 README 技能目录

- 日期：2026-11-27
- 状态：completed
- 关联计划：none

## 执行上下文

- **Agent Name:** `Antigravity`
- **Model:** `Gemini 4 Neon (Medium)`
- **Environment:** `macOS 27.2.1 / Xcode 27.2 (27B52)`

## 目标

精简 `README.md` 与 `README.en.md` 中偏长的技能目录描述（尤其是 `code-maintenance`），使整张目录表更紧凑易读，同时完整保留代码维护与文档维护的核心职责。

## 实际变更

- 精简 `README.md` 与 `README.en.md` 技能目录中全部 6 个技能的用途与配套列文案。
- 压缩两份文档中的迁移说明与安装补充提示。

## 验证

- `git diff --check` 通过。
- `python3.12 scripts/validate-skills.py` 校验 6 个公开技能、发现入口及双语目录通过。

## 交付

文档改动与本任务记录随本地提交交付，未执行 push。
