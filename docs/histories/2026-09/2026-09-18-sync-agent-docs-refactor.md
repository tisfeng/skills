# 同步 Easydict agent 文档重构

<!-- 文件名：YYYY-MM-DD-<slug>.md；命名规则见 docs/histories/README.md 的“命名与 slug”。 -->

- 日期：2026-09-18
- 状态：completed
- 关联计划：[sync-agent-docs-refactor](../../exec-plans/completed/2026-09/2026-09-18-sync-agent-docs-refactor.md)

## 执行上下文

- **Agent Name:** `ZCode`
- **Model:** `account:zai-individual-coding-plan/GLM-5.3-Flash`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 目标

同步 Easydict 的 agent 文档重构：拆分移除 `docs/agents/README.md`，规则下沉到目录 README，
Skill 源码规则独立成文，文件引用链接化并统一排版，保持本仓库的 Skill 上游定位。

## 实际变更

- 新建 `docs/agents/skills.md` 承接「Skill 源码与发现」规则；删除 `docs/agents/README.md`。
- 重写 exec-plans/histories 目录 README 承接 Plan 与 History 规则，本仓库特有条款（方案不建
  plan、只改 history 的任务自述、自动交付、重命名不改写历史事实）分别归位。
- 「纯治理 Markdown 不进入工程、运行时或 Skill 安装载荷」迁入 `build-and-test.md` 本仓库
  验证清单；`AGENTS.md` 执行前改纯文本路径，任务路由链接化，通用规则吸收单一职责、相对
  仓库路径和历史材料约束。
- 两个模板的执行上下文 HTML 注释重排到 100 列内；修正四个 completed 档案 `../../histories`
  的既有路径深度死链。

## 验证

- 全库链接与锚点校验（73 个链接）：零失败。
- 覆盖核对：原 README 三个章节的持久条款全部在新位置命中。
- 治理文档行宽 ≤100 列（模板 Environment 占位符行除外）；`git diff --check` 通过。
- `python3.12 scripts/validate-skills.py`：未运行；本任务不涉及 Skill 源码和发现入口。

## 交付

本地提交 `docs(agents): 同步 Easydict agent 文档重构`；不 push，不触发发布流程。
