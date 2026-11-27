# 完善项目文档并移除 openai.yaml 适配

- 日期：2026-11-27
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-11/2026-11-27-polish-docs-and-remove-openai-yaml.md)

## 执行上下文

- **Agent Name:** `Antigravity`
- **Model:** `Gemini 4 Neon (Medium)`
- **Environment:** `macOS 27.2.1 / Xcode 27.2 (27B52)`

## 目标

移除面向单一宿主的 `agents/openai.yaml` 适配文件，使仓库保持为通用 Agent Skills 集合；重写双语 README 以准确呈现各技能能力并改善排版；同步清理治理文档与测试中的陈旧描述。

## 实际变更

- 移除全部 6 个公开技能下的 `agents/openai.yaml` 及其空目录。
- 重写 `README.md` 与 `README.en.md`：补全 `code-maintenance`、`review`、`submit-pr` 等技能目录说明；使用 `> [!NOTE]` 呈现 `code-simplifier` 迁移提示；整理宿主规则与依赖约定、安装选项和补充说明，并消除中文句中软换行。
- 更新 `skills/code-maintenance/SKILL.md` 的 `description`，明确包含梳理文件职责与退役废弃代码能力。
- 更新 `tests/test_skill_portability.py` 顶部 docstring，并修正 `AGENTS.md`、`docs/histories/template.md`、`docs/exec-plans/templates.md` 中的陈旧或省略路径。

## 验证

- `git diff --check` 通过。
- `python3.12 scripts/validate-skills.py` 校验 6 个公开技能及发现入口通过。
- `python3.12 -m compileall -q scripts skills` 通过。
- `python3.12 -m unittest discover -s tests -v` 全部 5 项单测通过。
- 确认 `skills/` 下已无 `agents/` 或 `openai.yaml` 残留。

## 交付

改动、归档计划与本任务记录随本地提交交付，未执行 push。
