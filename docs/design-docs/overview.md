# Agent 资产结构设计

- 状态：adopted
- 初次记录：2026-09-09
- 最近修订：2026-09-11，移除 Codex 子代理，仓库只发布 Agent Skills

## 背景

本仓库发布可复用的 Agent Skills。Skill 需要可审查、可版本化和可由下游项目安装。若把当前
规则、设计理由、安装边界和执行历史混在入口文件中，任务路由会膨胀，并逐渐形成多个相互冲突的
权威来源。

仓库曾同时发布 Codex 子代理配置（TOML、`.codex/agents/` 发现目录与独立 npm 安装器）。该形式
绑定单一 Agent 平台，其他平台的消费方无法适配，因此已整体移除；再次引入平台专属资产前需要
重新评估。

## 设计决策

```text
用户请求
  └─ AGENTS.md 路由
      ├─ docs/agents/：当前专题规则
      └─ skills/<name>/SKILL.md：按需调用的工作流源码

项目内专属能力使用 `.agents/skills/<name>/SKILL.md`；发布流程和版本日志集中在 `docs/release/`，
不列入公开 Skill 目录。
```

| 位置 | 权威内容 | 主要用途 |
| --- | --- | --- |
| `AGENTS.md` | 通用约束和唯一任务路由 | 告诉 Agent 当前任务需要读取哪些规则 |
| `docs/agents/request-boundary.md` | 请求与执行边界 | 规定授权、任务状态、Mutation Gate 和受保护状态 |
| `docs/agents/git-workflow.md` | Git 工作流 | 规定状态保护、本地交付和 worktree 集成 |
| `docs/agents/build-and-test.md` | 验证规则 | 规定验证策略和证明边界 |
| `docs/agents/development.md` | 开发规则 | 规定代码、脚本、配置、文档和源码资产质量 |
| `docs/agents/README.md` | 仓库治理 | 规定文档生命周期和源码资产安装边界 |
| `docs/design-docs/` | 长期设计理由 | 记录为什么采用重要边界或策略 |
| `docs/exec-plans/` | 执行过程 | 记录获准工作的目标、风险、进度和验证 |
| `docs/histories/` | 完成结果 | 记录已落地变更及其关键背景 |
| `.agents/skills/` | 项目技能发现入口 | 通过相对链接使用公开源码，并保存项目专属 Skill 实目录 |
| `docs/release/` | 发布流程和日志 | 说明发布步骤，并保存每个公开版本的 Release 正文 |

`skills/` 是 `npx skills add` 识别的 Skill 源码，也是本仓库唯一的对外发布资产。Skills 与仓库
共用 tag；安装器按 tag 或分支解析源码，消费方的 lock 与来源选择由消费方维护。

公开技能通过 `.agents/skills/<name> -> ../../skills/<name>` 逐项链接供本仓库自用。
项目技能发现目录与源码分发目录不同；链接让当前 checkout 的修改直接可读，也避免复制后出现
两份内容。逐项链接保留了内部 `release` 实目录，相对路径可随 checkout 和 worktree 移动。
不整体搬迁公开目录，也不把整个 `.agents/skills/` 替换成链接；维护规则见
[`源码资产与安装边界`](../agents/README.md#源码资产与安装边界)。

宿主政策与 Skill 执行流程分离：项目决定允许什么、要求什么，Skill 完成通用步骤并承担内部
一致性与失败处理。这样修复或升级 Skill 时，消费方无需复制新流程或版本补丁。本仓库自用也
遵守这一边界，现行维护规则见 [Skill 与宿主职责](../agents/README.md#skill-与宿主职责)。
跨 Skill 组合可以保留，但资源和依赖必须在消费者环境中可用；源码 checkout 中链接存在并不
证明安装后可用。固定宿主规则的隔离测试用于发现这类隐式依赖。

## 非目标

- 不把所有规则集中到 `AGENTS.md`，也不建立多层 README 作为重复任务路由。
- 不把下游项目的 lock、安装快照或项目专属交付策略当作本仓库的源码约束。
- 不用设计文档替代当前规则、执行计划、完成 history 或用户明确指令。
- 发布 source tag 不自动授权 GitHub release、push 或全局安装。

## 重新评估条件

- 根入口再次明显膨胀并承载详细专题规则。
- 同一约束在两个以上文件都被视为权威，或单个专题出现多个可独立路由的职责。
- Skills 与仓库 tag 的对应关系或安装边界发生实质变化。
- 需要再次评估引入平台专属资产，例如某个 Agent 的子代理或专属配置文件。
- 链接、结构和发布资产无法通过低成本静态检查保持可信。
