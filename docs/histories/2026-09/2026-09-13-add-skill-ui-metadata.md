# 为公开 Skill 添加 UI 元数据

- 日期：2026-09-13
- 状态：completed
- 关联计划：none

## 目标

依据 OpenAI 官方 Skill 文档，为缺少配置的公开 Skill 添加 `agents/openai.yaml`，使其在
ChatGPT 桌面应用中显示清晰名称、简短说明和默认提示词。

## 实际变更

- 为 `code-simplifier`、`git-commit`、`review-pr`、`review` 和
  `worktree-rebase-merge` 添加 UI 元数据。
- 保留默认隐式调用行为，不添加未提供的图标、品牌色或工具依赖。
- 保留 `submit-pr` 已有的 `agents/openai.yaml`。

## 验证

- 解析全部公开 Skill 的 `agents/openai.yaml`，检查字段类型、描述长度和默认提示词中的 Skill 引用。
- 运行 `python3.12 scripts/validate-skills.py`。
- 运行 `git diff --check`。

## 交付

- 变更与本 history 一并完成本地提交。
- 未执行 push 或发布。
