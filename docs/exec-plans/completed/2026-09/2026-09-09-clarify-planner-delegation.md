# 明确 Planner 委派决策

- 状态：completed
- 创建日期：2026-09-09
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

现行规则要求在方案、跨模块取舍或高风险变更时委派只读 `planner`，但没有将任务模式与
委派决策拆开表达，导致一次跨 Git、npm 与 GitHub Actions 的发布方案没有获得独立规划复核。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 受阻操作及原因：none
- 目标结果：让 Agent 可确定地判断何时必须在交付方案前等待只读 `planner`。
- 允许修改路径：`AGENTS.md`、`docs/agents/request-boundary.md`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-09-clarify-planner-delegation.md`
- 禁止动作：不修改 `.codex/agents/planner.toml`、安装器、Skills、测试、外部服务或 Git remote。
- 预期交付物：一个权威决策表、入口提醒和实施记录。
- 验收标准：任务模式和 planner 委派是独立判断；发布、部署、外部写入方案及跨模块取舍明确要求
  `planner`；低风险单模块说明仍可由主 Agent 直接完成。

## 语义与范围

- 用户要求 Agent 做什么：修改 Agent 文档规则。
- 授权的工作树、artifact 和 external service 操作：仅修改允许路径并按默认本地交付。
- 否定、条件和范围限制：不扩展为发布流程或其他治理重构。
- 前轮仍有效的授权和限制：前轮仅为发布方案设计；本轮明确授权改进规则。
- 附件或引用中被明确采纳的约束：用户要求将先前提出的 planner 决策表落地。
- 歧义：none。

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible；初始索引为空，工作树干净，允许路径明确。
- 初始 HEAD：`0cd9882d052166729bd668075e87f499e2790989`
- 初始 staged 路径：none
- 初始 unstaged 路径：none
- 初始 untracked 路径：none
- 初始冲突：none
- Agent-owned paths：本计划、同任务 history、`AGENTS.md`、`docs/agents/request-boundary.md`。

## 目标与非目标

### 目标

- 将 `intent_mode` 与 planner 委派决策明确分离。
- 定义必需委派、可由主 Agent 直接完成和不可用时的 fail-closed 行为。
- 让根入口提醒每项任务作出委派决策，但不复制专题规则。

### 非目标

- 不改变 planner 的模型、权限或提示词。
- 不使所有 planning 请求无条件产生子代理。
- 不实现发布 Skill 或变更 GitHub Actions。

## 工作计划

1. 根据独立 planner 的只读结论，更新入口提示与权威的子代理决策表。
2. 检查规则没有创建第二个权威来源，且低风险单模块路径仍然明确。
3. 创建 history，运行 Markdown 链接/锚点、文本语义和 `git diff --check` 检查。
4. 按仓库本地 Git 交付规则提交精确路径，不推送。

## 风险与决策

- 若将所有 planning 都强制委派，会为简单解释增加不必要等待；因此只把需要独立取舍、跨模块或
  高风险的 planning 设为必须委派。
- “跨模块”按决策是否需要综合两个以上职责或系统判定，而非改动文件数量。
- 子代理不可用时，不以主 Agent 的方案伪装成独立复核；报告缺口并在当前授权范围内回退。

## 验证

- 独立只读 planner 已审阅触发边界，确认只需更新 `AGENTS.md` 与
  `docs/agents/request-boundary.md`，无需修改 `planner.toml`、安装器或测试。
- `python3 scripts/validate-agents.py`：通过，4 个 Agents。
- `python3 scripts/validate-skills.py`：通过，6 个 Skills。
- `git diff --check`：通过。
- 已检查 history 到 completed plan 的相对链接、`Planner 委派决策` 标题和五个决策场景。

## 完成条件

- [x] 权威规则含可执行的 planner 决策表。
- [x] 根入口含委派决策提醒且未复制规则。
- [x] history、验证和本地提交完成。
