# Agent 规则与仓库治理

本目录存放面向编码 Agent 的现行专题规则。根目录 [`AGENTS.md`](../../AGENTS.md) 是唯一任务入口；
本文件说明文档生命周期、维护原则和本仓库的源码资产边界，不提供第二套路由。

## 文档分层

- `docs/agents/`：当前有效的 Agent 和贡献者工作流规则。
- `docs/design-docs/`：需要长期维护的重要设计决策和资产结构理由。
- `docs/exec-plans/`：获准 implementation 的多步骤工作计划。
- `docs/histories/`：最终产生仓库文件差异的 implementation 记录。
- `skills/`：对外发布的 Agent Skill 源码。
- `.codex/agents/`：对外发布的 Codex 子代理配置。

历史、completed plan 和参考资料是证据，不是当前执行指令。只有当前用户请求、适用的
`AGENTS.md` 和被明确调用的 Skill 才约束实施。

## Plan 与 History

- planning 阶段的方案只出现在当前回复中，不创建或更新 active plan。
- 用户明确批准 implementation 且 Mutation Gate 通过后，架构、协议、迁移、多步骤、跨模块或
  高风险工作在 `docs/exec-plans/active/` 创建执行计划。
- implementation 最终产生仓库文件差异时，必须在同一任务中创建或更新一条 `docs/histories/`
  记录；没有差异时不创建空记录。
- 同一任务分多轮实施时复用同一条 history。只修改 history 的任务由该记录描述自身，不递归创建
  第二条。
- 存在执行计划时，完成后移动到 `docs/exec-plans/completed/`，并让同任务 history 链接
  completed plan。
- 交付时将同任务 history 与其他任务变更一起验证和精确暂存。缺少 history 时在允许范围内补齐；
  用户明确排除该路径时不扩权，并按 Git 规则报告交付阻塞。
- 显式提交已有 staged 内容不反向要求补写 implementation history。
- plan 记录目标、授权、范围、限制、初始 Git 快照、Agent-owned paths、工作计划、风险、验证和
  完成条件；history 只记录已落地结果，不复制完整对话。

## 文档维护

- 每份现行规则只维护一个主要职责；跨职责使用链接，不复制完整条款。
- 同一专题仍内聚且不超过约 500 行时，不仅为缩短文件继续拆分；超过该规模或出现多个独立职责时
  再评估拆分。
- 新增、删除或重命名规则文件时，只在根 `AGENTS.md` 维护任务路由，不建立多层索引。
- 使用相对仓库路径，不提交机器本地绝对路径。行为变化时同步更新实现、测试和受影响文档。
- 治理 Markdown、plan、history 和 `docs/` 文档不属于安装器载荷；Skill 与 agent TOML 则由安装器
  从 Git 源码读取。npm 包是否包含其他运行时文件由 `package.json` 的 files 清单决定。

## 源码资产与安装边界

`skills/` 和 `.codex/agents/` 是本仓库直接维护、可审查和随 tag 发布的源码，不是下游项目的
受管副本。两者是独立安装单元：前者由 `npx skills` 管理，后者由 `@tisfeng/codex-agents` 的
安装器管理。

- 修改通用行为、Skill 脚本、测试或 agent TOML 时，直接在本仓库完成验证；不要改写为下游项目的
  `.agents/skills/` 路径。
- 下游项目的 lock、来源选择、内容哈希和本地例外属于消费方治理；本仓库不创建或维护这些消费方
  快照。
- 发布 tag 不自动授权 npm 发布、GitHub release、push 或用户全局安装；这些外部动作仍需明确授权。
- 安装器、Skill 源码、agent TOML 或发布配置的行为变更应同步更新对应测试和用户文档；纯治理文档
  变更不要求改动安装器。
