# 移除 Worktree 展示名称中的斜杠

- 日期：2026-09-17
- 状态：completed
- 关联计划：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model ID:** `Unknown`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 目标

将 `worktree-rebase-merge` 的用户可见名称改为不含斜杠的形式。

## 实际变更

- 将 `display_name` 从 `Worktree Rebase/Merge` 改为 `Worktree Rebase Merge`。
- 保留 Skill 名称、说明、默认提示词和调用行为不变。

## 验证

- 使用 Ruby YAML 解析器检查全部公开 Skill 的 `agents/openai.yaml`。
- 运行仓库 Skill 校验和 `git diff --check`。
- OpenAI `quick_validate.py` 因当前 Python 3.12 环境缺少 PyYAML 无法运行；该脚本仅校验
  `SKILL.md` frontmatter，不校验 `agents/openai.yaml`。

## 交付

- 变更与本 history 一并完成本地提交。
- 未执行 push、fetch、pull、rebase、merge、发布或安装操作。
