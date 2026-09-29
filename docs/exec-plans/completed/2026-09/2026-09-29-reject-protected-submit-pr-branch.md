# 提交 PR 时拦截当前保护分支

- 状态：completed
- 创建日期：2026-09-29
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Unknown`
- **Model:** `Unknown`
- **Environment:** `macOS 27.0 / Xcode 27.2 (27B5019j)`

## 背景

PR #1336 的 head 和 base 都使用 `dev`。当前 helper 会保护已解析的 base/default 分支名，但仍允许从保护分支出发并指定另一个 head 分支继续提交；技能没有把当前分支与远程主分支同名作为必须提示用户并停止的条件。

## 目标与范围

- 目标结果：当前分支名与动态解析的 base 或 GitHub default branch 相同则停止提交，说明冲突并要求用户在新任务分支上重新运行；同名判断对 fork head 同样生效。
- 允许修改路径：`skills/submit-pr/SKILL.md`、`skills/submit-pr/references/workflow.md`、`skills/submit-pr/scripts/submit_pr.py`、`skills/submit-pr/tests/test_submit_pr.py`、本计划及对应 history。
- 同任务 history：`docs/histories/2026-09/2026-09-29-reject-protected-submit-pr-branch.md`
- 用户限制：不 push、不创建或修改 GitHub PR、不发布 Skill；保留既有提交，不自动切换 checkout。
- 非目标：改变分支命名格式、remote 拓扑发现、PR 模板或提交内容规则。
- 验收标准：`plan` 与 `apply` 在任何提交、fetch、push 或 PR 操作前识别当前保护分支并给出清晰错误；不同名的任务分支行为保持现状；测试覆盖 base/default 同名及 fork 场景。

## 工作计划

1. 收紧 helper 的保护分支检查与错误信息，并把 `apply` 的检查放到 fetch 前。
2. 补充回归用例，覆盖当前分支与 base/default 同名、指定替代 head 仍需停止，以及跨 fork 的同名 head 保护。
3. 更新 Skill 入口和工作流契约，要求把 helper 拦截结果转成明确的用户提示；说明新建分支会保留现有提交，无需重复生成相同提交。
4. 运行仓库规定的 Skill 校验、直接单测、可移植性测试、Python 编译检查和 diff 检查；按 `review` 技能审查最终快照。
5. 更新 history、归档本计划，并按仓库交付规则创建本地提交；不执行任何远程写入。

## 风险与决策

- 使用 helper 动态解析的 base/default 名称，不硬编码 `main` 或 `dev`。
- 保护的是当前 checkout 的分支身份；允许用户明确创建新任务分支后重新运行，helper 不替用户切换分支。
- 即使当前分支允许作为提交来源，若选定 head 名称与 base/default 同名，仍由既有 head 保护规则拒绝；fork remote 不豁免名称冲突。

## 进度

- [x] 阅读任务路由、Skill 资产、验证、history 与计划规则。
- [x] 更新 submit-pr Skill/helper 与回归覆盖。
- [x] 完成验证和本地审查。
- [x] 写入 history、归档计划并本地提交。

## 验证

- `python3.12 scripts/validate-skills.py`：通过，校验 6 个 Skill 与发现入口。
- `python3.12 -m unittest discover -s skills/submit-pr/tests -p 'test_*.py'`：29 项通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：2 项通过。
- `python3.12 -m compileall -q scripts skills`：通过。
- `skill-creator` 的 `quick_validate.py skills/submit-pr`：通过。
- `git diff --check`：通过。
- 本地 `review`：最终实现无 finding；修正 detached checkout 指引遗漏 `preflight` 后重新通过 Skill 校验与 diff 检查。

## 完成条件

- 保护分支碰撞在 `plan` 与 `apply` 中均明确停止，且拒绝发生在 fetch、push、创建 PR 之前。
- 新增回归场景、Skill 指引、验证结果和 history 一致。
- 计划归档到 `docs/exec-plans/completed/2026-09/`，变更仅本地提交，不 push。
