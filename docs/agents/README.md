# Agent 文档与仓库治理

根目录 [`AGENTS.md`](../../AGENTS.md) 是唯一任务入口；`docs/agents/` 只存放当前有效的项目专题
规则。design doc 记录长期设计，plan 记录执行过程，history 记录已落地结果；历史材料不是
当前执行指令。

## Plan 与 History

- 方案、检查和解释只在当前回复中呈现，不创建 active plan。
- 多步骤、跨模块或高风险的执行任务在 `docs/exec-plans/active/` 使用
  [执行计划模板](../exec-plans/templates.md)；完成后按文件名月份移入
  `docs/exec-plans/completed/YYYY-MM/`。
- 执行任务产生仓库差异时，在 `docs/histories/YYYY-MM/` 使用
  [history 模板](../histories/template.md) 记录结果；没有差异时不创建空记录。
- plan 与 history 使用 `YYYY-MM-DD-<slug>.md`，同一任务共享 slug 并跨轮复用；存在 plan 时，
  history 链接归档后的 plan。只修改 history 的任务由该记录描述自身。
- `<slug>` 使用小写 kebab-case；其中完整的标准标识可保留点号（如 `release-0.1.1`、
  `upgrade-skills-v0.3.8`）。不使用空格、下划线、大写字母、斜杠、反斜杠或冒号。
- plan 记录目标、范围、步骤、风险和验证；history 只记录最终变更和关键决策，不复制完整对话。
- 自动本地交付将同任务 history 与其他变更一起校验和交付；显式提交既有 staged 内容不反向
  要求补写 history。

## 文档维护

- 每份现行规则只维护一个主要职责；跨职责使用链接，不复制完整条款。
- 新增、删除或重命名现行规则时，只在根 `AGENTS.md` 维护任务路由。
- 使用相对仓库路径，不提交机器本地绝对路径。重命名后更新活动引用，不改写 completed
  plan/history 记录的历史事实。
- 行为变化时同步更新实现、测试和受影响文档；纯治理 Markdown 不进入工程、运行时或 Skill 安装载荷。

## Skill 源码与发现

宿主规则只表达本项目的验证、history、自动交付、发布和资产边界；Skill 自行维护通用
取证、Git 状态保护、执行、恢复和结果校验契约。

- `skills/` 是由本仓库直接维护、可审查并随 tag 发布的唯一公开 Skill 源码；`npx skills` 直接
  读取该目录，本仓库不发布 npm 包。
- `.agents/skills/<name>` 仅使用指向 `../../skills/<name>` 的相对目录链接提供本仓库发现入口；
  新增或删除公开 Skill 时同步维护链接。
- 仓库不维护专属 Skill；`SKILL.md` 只出现在 `skills/` 及其 `.agents/skills/` 发现链接中。
- 本仓库任务使用当前 checkout 的 Skill 源码；同名全局 Skill 并存时核对实际加载路径，运行时
  尚未刷新时重新启动 Agent。
- 不向本仓库复制自身 Skill，也不创建消费方 lock；下游的 lock、来源选择、内容哈希和本地例外
  属于消费方治理。
- 修改 Skill 行为、脚本、必需资源或依赖时，同步源码、相关测试和必要文档；验证范围以
  [`build-and-test.md`](build-and-test.md#本仓库验证) 为准。
- 发布 tag 不自动授权 GitHub Release、push 或用户全局安装；这些外部动作仍需明确要求。
