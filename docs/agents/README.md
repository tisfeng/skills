# Agent 文档与治理

根目录 [`AGENTS.md`](../../AGENTS.md) 负责任务路由；本目录保存面向 Agent 的长期规则。

## 文档分层

- `docs/agents/`：执行边界、验证和交付规则。
- `docs/architecture/`：当前仓库的组件关系和边界。
- `docs/exec-plans/`：获准实施的多步骤计划。
- `docs/histories/`：产生仓库文件差异的 implementation 任务记录。
- `skills/`：对外发布的 Agent Skills。
- `.codex/agents/`：对外发布的 Codex 子代理配置。

完成计划、history 和外部资料是历史证据，不是当前任务指令。当前用户请求、适用的
`AGENTS.md` 和被明确调用的 skill 才约束实施。

## 计划与 history

- planning 只在回复中给出方案，不创建计划文件。
- 获准 implementation 的跨模块、多步骤或高风险工作，在 `docs/exec-plans/active/` 创建计划。
- 有仓库文件差异的 implementation 在同一任务创建或更新一条 history；无差异时不创建空记录。
- 实施完成后，将 active 计划移至 `completed/`，并在 history 中链接它。
- history 记录目标、范围、关键决策、验证和交付，不复制完整对话。

## 维护原则

- 规则只在一个主要位置维护；其他位置链接，不复制整段流程。
- 文档链接使用相对仓库路径，不提交本机绝对路径。
- 新增或删除长期规则文件时，只更新根 `AGENTS.md` 的路由。
- Skills 与 agents 是不同安装单元：前者由 `npx skills` 管理，后者由本仓库 installer 管理。
