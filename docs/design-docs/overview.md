# Agent 资产结构设计

- 状态：adopted
- 初次记录：2026-09-09

## 背景

本仓库同时发布可复用的 Agent Skills 与 Codex 子代理。两种资产都需要可审查、可版本化和可由
下游项目安装，但其发现方式、安装器和升级逻辑并不相同。若把当前规则、设计理由、安装边界和
执行历史混在入口文件中，任务路由会膨胀，并逐渐形成多个相互冲突的权威来源。

## 设计决策

```text
用户请求
  └─ AGENTS.md 路由
      ├─ docs/agents/：当前专题规则
      ├─ skills/<name>/SKILL.md：按需调用的工作流源码
      └─ .codex/agents/<name>.toml：可委派的专用子代理源码

项目内专属能力使用 `.agents/skills/<name>/SKILL.md`；发布流程和版本日志集中在 `docs/release/`，
不列入公开 Skill 目录或 npm package 载荷。
```

| 位置 | 权威内容 | 主要用途 |
| --- | --- | --- |
| `AGENTS.md` | 通用约束和唯一任务路由 | 告诉 Agent 当前任务需要读取哪些规则 |
| `docs/agents/request-boundary.md` | 请求与执行边界 | 规定授权、任务状态、Mutation Gate 和子代理边界 |
| `docs/agents/git-workflow.md` | Git 工作流 | 规定状态保护、本地交付和 worktree 集成 |
| `docs/agents/build-and-test.md` | 验证规则 | 规定验证策略、reviewer/tester 和证明边界 |
| `docs/agents/development.md` | 开发规则 | 规定代码、脚本、配置、文档和源码资产质量 |
| `docs/agents/README.md` | 仓库治理 | 规定文档生命周期和源码资产安装边界 |
| `docs/design-docs/` | 长期设计理由 | 记录为什么采用重要边界或策略 |
| `docs/exec-plans/` | 执行过程 | 记录获准工作的目标、风险、进度和验证 |
| `docs/histories/` | 完成结果 | 记录已落地变更及其关键背景 |
| `.agents/skills/` | 项目内部 Skill | 提供当前仓库专属的标准 Skill 格式工作流 |
| `docs/release/` | 发布流程和日志 | 说明发布步骤，并保存每个公开版本的 Release 正文 |

`skills/` 是 `npx skills add` 识别的 Skill 源码；`.codex/agents/` 是 Codex 原生发现的项目级
子代理配置。两者共用仓库 tag，但安装、lock 和升级逻辑各自独立。`bin/codex-agents.mjs` 从指定
源码读取 `.codex/agents/*.toml`，在项目级或全局级安装，并拒绝覆盖本地修改过的同名角色，除非
用户明确使用覆盖选项。

## 非目标

- 不把所有规则集中到 `AGENTS.md`，也不建立多层 README 作为重复任务路由。
- 不把下游项目的 lock、安装快照或项目专属交付策略当作本仓库的源码约束。
- 不用设计文档替代当前规则、执行计划、完成 history 或用户明确指令。
- 发布 source tag 不自动授权 npm 发布、GitHub release、push 或全局安装。

## 重新评估条件

- 根入口再次明显膨胀并承载详细专题规则。
- 同一约束在两个以上文件都被视为权威，或单个专题出现多个可独立路由的职责。
- Skills、agents 或安装器不再共同随 tag 发布，或者安装边界发生实质变化。
- 链接、结构和发布资产无法通过低成本静态检查保持可信。
