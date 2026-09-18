# 同步 Easydict agent 文档重构

<!-- 文件名：YYYY-MM-DD-<slug>.md；命名规则见 docs/histories/README.md 的“命名与 slug”。 -->
<!-- 本模板只用于多步骤、跨模块或高风险的执行任务。 -->

- 状态：completed
- 创建日期：2026-09-18
- 负责人：tisfeng
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `ZCode`
- **Model:** `account:zai-individual-coding-plan/GLM-5.3-Flash`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 背景

Easydict 本轮拆分移除了 `docs/agents/README.md`，规则下沉到 exec-plans/histories 目录 README
与 skills.md，并统一了排版。本仓库与治理文档同构，需要同步移植；本仓库是 Skill 上游，没有
消费方 lock 和来源基线内容。

## 目标与范围

- 目标结果：删除 `docs/agents/README.md`，plan/history 规则下沉到目录 README，Skill 源码与
  发现规则独立为 `docs/agents/skills.md`，文件引用链接化并统一排版。
- 允许修改路径：`AGENTS.md`、`docs/agents/`、`docs/exec-plans/`、`docs/histories/` 治理
  Markdown 及既有死链修正。
- 同任务 history：`docs/histories/2026-09/2026-09-18-sync-agent-docs-refactor.md`
- 用户限制：保留本仓库的宿主边界与「不创建消费方 lock」上游定位；不 push。
- 非目标：不改 Skill 源码、测试和发布流程；不改写档案正文。
- 验收标准：链接与锚点校验零失败、治理文档正文 ≤100 列、`git diff --check` 通过。

## 工作计划

1. 新建 `docs/agents/skills.md` 承接「Skill 源码与发现」规则。
2. 重写 exec-plans/histories README 承接 Plan 与 History 规则，删除 agents/README。
3. 「纯治理 Markdown 不进入工程、运行时或 Skill 安装载荷」迁入 build-and-test.md 的本仓库
   验证清单；重写 `AGENTS.md` 路由与通用规则；重排模板注释。
4. 修正四个 completed 档案的既有相对路径深度死链。
5. 链接校验、覆盖核对、`git diff --check`，归档计划并提交。

## 风险与决策

- 「方案、检查和解释不创建 active plan」「只修改 history 的任务由该记录描述自身」等本仓库
  特有条款分别保留在 exec-plans 和 histories 目录 README。
- 「重命名后不改写 completed 记录的历史事实」归入 histories README；「行为变化同步更新」
  由执行模式第 2 步覆盖，删除；「纯治理 Markdown 不进入安装载荷」归入 build-and-test.md。
- 四个 completed 档案的 `../../histories` 路径深度错误为既有死链，顺手修正为 `../../../`。

## 进度

- [x] skills.md、目录 README、build-and-test 与 AGENTS.md 完成。
- [x] 模板注释重排，agents/README 删除，既有死链修正。
- [x] 验证通过，计划归档并创建本地提交。

## 验证

- 全库链接与锚点校验（73 个链接）：零失败（含修正后档案链接）。
- 覆盖核对：原 README 三个章节的持久条款全部在新位置命中。
- 治理文档行宽 ≤100 列，仅模板 Environment 占位符行作为不可拆行例外。
- `git diff --check`：通过。
- `python3.12 scripts/validate-skills.py`：未运行；本任务不涉及 Skill 源码和发现入口。

## 完成条件

- [x] `docs/agents/README.md` 已删除，规则同构落地且上游定位条款保留。
- [x] 链接与锚点校验零失败。
- [x] history 已记录，计划归档并创建本地提交。
