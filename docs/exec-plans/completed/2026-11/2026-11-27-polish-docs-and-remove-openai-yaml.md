# 完善项目文档并移除 openai.yaml 适配

- 状态：completed
- 创建日期：2026-11-27
- 负责人：isfeng
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Antigravity`
- **Model:** `Gemini 4 Neon (Medium)`
- **Environment:** `macOS 27.2.1 / Xcode 27.2 (27B52)`

## 背景

`README.md` 与 `README.en.md` 中对 `code-maintenance`、`review` 等技能的用途描述过于粗糙，目录下方混排了底层参数与中文软换行；各技能目录下的 `agents/openai.yaml` 属于特定宿主适配，不符合通用技能集合定位；同时部分治理文档与测试注释存在陈旧路径或描述。

## 目标与范围

- 目标结果：移除全部 `skills/*/agents/openai.yaml`；重写双语 README 的技能目录与说明结构；同步完善 `code-maintenance` 描述；修正测试注释及治理文档中的陈旧路径。
- 允许修改路径：`skills/*/agents/`、`skills/code-maintenance/SKILL.md`、`README.md`、`README.en.md`、`tests/test_skill_portability.py`、`AGENTS.md`、`docs/histories/template.md`、`docs/exec-plans/templates.md` 及本任务计划与 history。
- 同任务 history：`docs/histories/2026-11/2026-11-27-polish-docs-and-remove-openai-yaml.md`
- 用户限制：不新增 `openai.yaml` 校验，直接移除 `openai.yaml` 相关文件；不新增测试代码；不 push。
- 非目标：修改 Skill 运行脚本逻辑、发布新版本或修改历史归档记录。
- 验收标准：全仓库校验与所有现有单测通过，现行文档无断链或陈旧路径，双语目录准确反映各 Skill 能力。

## 工作计划

1. 移除全部 6 个 `skills/*/agents/openai.yaml` 及其空目录。
2. 重写 `README.md`、`README.en.md`，并同步更新 `skills/code-maintenance/SKILL.md` 的 `description`。
3. 修正 `tests/test_skill_portability.py` 顶部 docstring，以及 `AGENTS.md`、`docs/histories/template.md`、`docs/exec-plans/templates.md` 的路径表述。
4. 运行仓库校验矩阵、全部单测及 `git diff --check`，归档计划并本地提交。

## 风险与决策

- 移除 `agents/openai.yaml` 不影响 `SKILL.md` 规范发现、仓库校验和可移植性测试。
- README 重写保留 `validate-skills.py` 要求的目录表格链接格式 `[\`<name>\`](skills/<name>/SKILL.md)`。

## 进度

- [x] 移除 `skills/*/agents/openai.yaml`
- [x] 更新双语 README、技能描述与治理文档
- [x] 运行校验与单测
- [x] 归档计划、记录 history 并创建本地提交

## 验证

- `git diff --check`、`python3.12 scripts/validate-skills.py`（6 个公开技能）、`python3.12 -m compileall -q scripts skills` 均通过。
- `python3.12 -m unittest discover -s tests -v` 全部 5 项单测通过。
- 确认 `skills/` 下不再存在任何 `agents/` 目录或 `openai.yaml` 文件。

## 完成条件

- 仓库校验、`compileall`、全部现有单测与 `git diff --check` 通过。
- 计划归档至 `docs/exec-plans/completed/2026-11/`，同任务 history 完成并随本地提交交付。
