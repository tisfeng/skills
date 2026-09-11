# AGENTS.md

`skills` 发布可复用的 Agent Skills 和 Codex 子代理配置。`AGENTS.md` 是唯一任务入口和
路由；现行专题规则位于 `docs/agents/`，每项规则只维护一个权威来源。

## 始终阅读

- 每个任务先阅读 `docs/agents/request-boundary.md`，确认请求语义、写入授权、任务模式、
  Mutation Gate，以及是否需要按其 `Planner 委派决策` 使用子代理。
- 回复以及新建或修改的仓库文档使用用户当前请求的语言；代码标识、API 名称、命令、路径、
  品牌名称和固定输出契约保留原文。
- 再按当前任务读取下方最小必要规则，不通过其他 README 或索引进行二次路由。

## 任务路由

- Git 状态保护、暂存、本地提交和 worktree 集成：`docs/agents/git-workflow.md`。
- 验证、独立 review 和 tester：`docs/agents/build-and-test.md`。
- 文档生命周期、外部安装边界和源码资产维护：`docs/agents/README.md`。
- 代码、脚本、配置和文档质量：`docs/agents/development.md`。
- 重要设计决策和本仓库资产结构：`docs/design-docs/overview.md`。
- 版本发布流程与记录：`docs/release/overview.md`。
- 具体 Skill：执行前读取 `skills/<skill-name>/SKILL.md`。
- Codex 子代理：`.codex/agents/<agent-name>.toml`。

## Review 路由

- 本地任务、工作树、提交/range、文件或模块审查使用 `skills/review/SKILL.md`；独立只读审查
  使用 `.codex/agents/reviewer.toml`。
- GitHub PR review 使用 `skills/review-pr/SKILL.md`；默认不授权产品修复、远程评论、approve、
  关闭 PR 或 push。

## 回复与交付表达

- 先说明真实结果，再给必要证据、修改范围、已执行/未执行验证和外部交付状态；只有需要用户
  决策时才提出问题。
- 因规则暂停或留下未完成工作时，链接实际权威条款，区分明确要求与 Agent 推断，不重复询问
  已有授权。
- 不从材料复制无关要求，不把计划写成完成结果，也不把静态检查写成构建或运行测试。标题、
  提交信息和 PR 描述优先表达实际新增、修复、保留或验证的行为。

## 维护约束

- `skills/` 与 `.codex/agents/` 是本仓库维护、随 tag 发布的源码；不要改写为下游项目的
  `.agents/skills/` 路径。源码变更不因此授权 npm 发布、GitHub release、push 或修改用户全局
  Codex 配置；完整资产边界见 `docs/agents/README.md`。
- 其余维护约束不在此复述，以对应专题文件为唯一来源：材料与写入授权见
  `docs/agents/request-boundary.md`，Git 状态保护见 `docs/agents/git-workflow.md`，
  文档与资产生命周期见 `docs/agents/README.md`。
