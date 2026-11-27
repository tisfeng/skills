# 精简 code-maintenance 技能并设为默认只读检查

- 日期：2026-11-27
- 状态：completed
- 关联计划：none

## 执行上下文

- **Agent Name:** `Antigravity`
- **Model:** `Gemini 4 Neon (Medium)`
- **Environment:** `macOS 27.2.1 / Xcode 27.2 (27B52)`

## 目标

精简 `code-maintenance` 的冗余防御条款，移除默认的 Markdown 80–100 字符硬折行规则，并将默认运行模式与范围调整为适合定时任务与日常巡检的安全配置。

## 实际变更

- 重写 `skills/code-maintenance/SKILL.md`：
  - 明确默认仅只读检查并输出建议方案，仅在用户明确要求修改时执行改动；
  - 将默认范围收紧为最近 7 天、最多 50 个提交；
  - 移除 Markdown 80–100 源码字符硬折行及周边防御条文，聚焦段落结构、列表层级与链接完整；
  - 将原 `references/code-simplifier.md` 的核心简化要点合并入主入口，保留 Swift/Xcode 与 Electron/TypeScript 两份平台指南的一跳直链。
- 删除薄文件 `skills/code-maintenance/references/code-simplifier.md`。

## 验证

- `git diff --check` 通过。
- `python3.12 scripts/validate-skills.py` 校验 6 个公开技能及发现入口通过。
- `python3.12 -m unittest discover -s tests -v` 全部 5 项单测（含隔离安装与链接闭包检查）通过。

## 交付

技能改动与本任务记录随本地提交交付，未执行 push。
