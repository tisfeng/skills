# 明确集成阶段的验证边界与未验证披露

- 日期：2026-09-21
- 状态：completed
- 关联计划：none

## 执行上下文

- **Agent Name:** Mavis
- **Model:** deepseek-flash
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 目标

`worktree-rebase-merge` 在 rebase 后只要求一句「只在仓库规则、用户请求或变更风险要求时扩大
验证」，其中「扩大验证」没有定义扩展集，也没有规定未运行验证时如何披露，读起来悬空且会让跳过
构建、测试的集成结果看起来与已验证的结果相同。

## 实际变更

- `integration-workflow.md` 的 Rebase 段：把「扩大验证」具体化为「构建、测试等超出该检查的
  验证」，触发来源写为仓库规则、用户授权或变更风险，并补充未运行时必须在回执中记录未验证部分。
- `reporting.md` 的「集成结果」清单新增验证项，要求写明实际运行的命令与结果；未运行时写
  `未执行（本次仅运行 git diff --check）`。直接提交模式同步约定写 `未执行（直接提交模式）`，
  与该文件既有的「Rebase、Merge 和 Push 都明确写未执行」以及 `git-commit` 回执的「提交后
  校验」字段保持一致——「未执行」是显式值，不是留白。

未采纳的替代方案：把验证范围整体移交给宿主规则、Skill 不再列举触发条件。可移植性会因此下降，
下游项目缺少 `build-and-test` 类规则时反而失去授权来源，故保留自包含写法。

## 验证

- `python3.12 scripts/validate-skills.py`：通过，验证 6 个 Skills 及发现入口。
- `python3.12 -m unittest discover -s skills/worktree-rebase-merge/tests -p 'test_*.py'`：6/6 通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：2/2 通过。
- `git diff --check`：通过。
- 现状核对：`skills/worktree-rebase-merge/tests/` 与 `tests/` 中无断言引用「集成结果」
  「diff --check」或「扩大验证」，`validate-skills.py` 只校验 frontmatter、Markdown 链接、冲突
  标记与发现入口，不校验正文措辞，故本次文本改动不改变既有测试与校验结论。
- 未运行项：未执行真实 worktree 集成流程，未验证真实 Agent 在新措辞下生成的回执。
- Review：纯文档、低风险变更，按 `AGENTS.md` 免于 `review` 技能审查。

## 交付

- 在任务分支 `docs/clarify-integration-verification-boundary` 创建本地提交并回执；未 push。
