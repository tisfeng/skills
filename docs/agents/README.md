# Agent 规则与仓库治理

本目录存放面向编码 Agent 的现行专题规则。根目录 [`AGENTS.md`](../../AGENTS.md) 是唯一任务入口；
本文件说明文档生命周期、维护原则和本仓库的源码资产边界，不提供第二套路由。

## 文档分层

- `docs/agents/`：当前有效的 Agent 和贡献者工作流规则。
- `docs/design-docs/`：需要长期维护的重要设计决策和资产结构理由。
- `docs/exec-plans/`：获准 implementation 的多步骤工作计划。
- `docs/histories/`：最终产生仓库文件差异的 implementation 记录。
- `skills/`：对外发布的 Agent Skill 源码。
- `.agents/skills/`：项目技能发现入口，只包含公开源码的相对目录链接。
- `docs/release/`：版本发布流程、GitHub 默认 Release 说明策略与历史日志归档。

历史、completed plan 和参考资料是证据，不是当前执行指令。只有当前用户请求、适用的
`AGENTS.md` 和被明确调用的 Skill 才约束实施。

## Plan 与 History

- planning 阶段的方案只出现在当前回复中，不创建或更新 active plan。
- 用户明确批准 implementation 且 Mutation Gate 通过后，架构、协议、迁移、多步骤、跨模块或
  高风险工作从 [执行计划模板](../exec-plans/templates.md) 起草，保存为
  `docs/exec-plans/active/YYYY-MM-DD-<slug>.md`；完成后移动到 `docs/exec-plans/completed/`。
- implementation 最终产生仓库文件差异时，必须在同一任务中创建或更新一条 history，从
  [history 模板](../histories/template.md) 起草并保存为
  `docs/histories/YYYY-MM/YYYY-MM-DD-<slug>.md`；没有差异时不创建空记录。
- 计划与 history 的 `<slug>` 使用小写 kebab-case，两者共享同一任务标识。
- 同一任务分多轮实施时复用同一条 history。只修改 history 的任务由该记录描述自身，不递归创建
  第二条。
- 存在执行计划时，让同任务 history 链接 completed plan。
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
  “受影响”按下面的职责边界判断，不因 Skill 升级默认修改宿主 Agent 规则。
- 治理 Markdown、plan、history 和 `docs/` 文档不属于安装载荷；`skills/` 由 `npx skills`
  直接从 Git 源码读取。本仓库不发布 npm 包。

## Skill 与宿主职责

- 宿主规则表达项目政策：任务授权、构建命令、代码约定、交付范围、是否自动提交、history
  要求及何时需要独立审查。Skill 遵守已有政策；不要求项目采用新的治理目录或必填配置。
- Skill 负责完成通用能力：取证、执行、结果校验、漂移检测、失败处理及自身依赖检查。项目
  只引用稳定入口，不引用内部章节、脚本字段或版本专属补救步骤。
- Skill 内部修复更新所属源码、测试和必要使用说明。仅当项目政策、公开入口、必填输入或
  支持依赖发生实际变化时，更新相应宿主规则或提供迁移说明。不能把内部缺陷当成接口迁移。
- 必需脚本和参考资料随 Skill 分发；跨 Skill 组合应明确依赖、按实际加载位置发现并处理缺失，
  不能假设宿主复制本仓库治理。依赖不足时报告限制或使用 Skill 定义的等价回退。
- 以固定宿主规则的消费者场景验证升级；源码结构检查、隔离 helper 测试和实际 Agent 行为
  分别取证。通用性验证不能通过复制整套本仓库 Agent 文档达标。

## 源码资产与安装边界

`skills/` 是本仓库直接维护、可审查和随 tag 发布的源码，不是下游项目的受管副本，由
`npx skills` 管理。

`.agents/skills/` 是本仓库自用的项目技能发现入口：

- 每个公开技能使用 `.agents/skills/<name> -> ../../skills/<name>` 相对目录链接，链接随 Git
  保存，`skills/<name>/` 始终是唯一源码。新增或删除公开技能时同步维护对应链接。
- 仓库不维护专属技能：`SKILL.md` 只允许出现在 `skills/` 与 `.agents/skills/`，其他文档按
  普通 Markdown 维护，校验脚本会拒绝其他位置。
- 不向本仓库复制自身技能，也不为这些源码链接创建消费方 lock。
- 本仓库任务使用当前 checkout 的技能源码。同名全局技能可能并存，调用时确认实际加载路径；
  技能未刷新时重新启动当前 Agent 运行时。其他宿主的发现目录和符号链接支持需分别核实。

- 修改通用行为、公开 Skill 脚本或测试时，直接在本仓库完成验证；不要改写为下游项目的
  `.agents/skills/` 路径。本仓库的发现链接与技能位置按上面的职责维护。
- 下游项目的 lock、来源选择、内容哈希和本地例外属于消费方治理；本仓库不创建或维护这些消费方
  快照。
- 发布 tag 不自动授权 GitHub release、push 或用户全局安装；这些外部动作仍需明确授权。
- Skill 源码或发布配置的行为变更应同步更新对应测试和用户文档；纯治理文档变更不需要改动源码。
