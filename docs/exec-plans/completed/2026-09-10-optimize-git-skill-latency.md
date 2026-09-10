# 优化 Git Skill 执行延迟

- 状态：completed
- 创建日期：2026-09-10
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

实际调用显示 `git-commit` 与 `worktree-rebase-merge` 的 Git 命令只占端到端时间的小部分，
主要等待来自正常成功路径中反复返回模型、串行调度只读检查以及重复输出 Git 状态。用户要求在
尽量保持现有功能、权限边界、安全门禁和完整回执的前提下重构执行方式，而不是刻意缩短 Skill。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 受阻操作及原因（如有）：none
- 目标结果：减少正常成功路径中的 Agent/工具往返和无关输出，保持逐命令 Git 写入与失败恢复边界。
- 允许修改路径：`skills/git-commit/`、`skills/worktree-rebase-merge/`、
  `docs/agents/git-workflow.md`、`.github/workflows/{validate,publish}.yml`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-10-optimize-git-skill-latency.md`
- 禁止动作：不 push、fetch、pull、rebase、merge、发布或修改下游安装；不以删除功能或安全检查换取速度。
- 预期交付物：两个 Skill 的程序化执行契约、窄职责只读检查脚本、真实 Git 行为测试、CI 入口及记录。
- 验收标准：相关单测、Skill 校验、Python 编译、YAML 解析和 diff 检查通过；正常路径工具编排阶段明显减少。

## 语义与范围

- 用户要求 Agent 做什么：执行上一轮基于最新源码给出的性能重构方案。
- 授权的工作树、artifact 和 external service 操作：只修改当前仓库获准路径并运行本地验证。
- 否定、条件和范围限制：不刻意删减 Skill 长度，尽量保持当前功能。
- 前轮仍有效的授权和限制：上一轮只读分析已完成独立 Planner 评估，本轮复用经核验仍成立的结论。
- 附件或引用中被明确采纳的约束：采用 OpenAI 官方延迟优化与 Programmatic Tool Calling 原则；附件中的历史诊断仅作为测量证据。
- 歧义：none

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible；初始索引和工作树为空，HEAD 未漂移，范围可精确分离。
- 初始 HEAD：`4833d34612aef0be534ddf8cb36dfe55cd996795`
- 初始 staged 路径：none
- 初始 unstaged 路径：none
- 初始 untracked 路径：none
- 初始冲突：none
- Agent-owned paths：本计划及上述允许路径内本任务实际新增或修改的文件。

## 目标与非目标

### 目标

- 将可预测的只读检查并行收集，并以紧凑结构返回关键事实。
- 在一次程序化调用内按顺序等待独立命令，避免正常成功结果反复返回模型。
- 保留 staged 范围、写前复验、逐命令退出状态、审批、冲突、漂移和完整回执门禁。
- 用真实临时 Git 仓库验证只读检查器的状态、范围、worktree 和漂移行为。

### 非目标

- 不引入负责 stage、commit、rebase 或 merge 的宽泛写入 runner。
- 不恢复 Git 交付子代理、跨 Agent 交接协议或通用恢复框架。
- 不承诺固定绝对耗时，不以减少最终用户回执字段换取速度。

## 工作计划

1. 为 `git-commit` 增加程序化预检、连续执行、完成态判断和紧凑输出契约。
2. 为 worktree 流程增加窄职责只读事实检查器，并让 Skill 规定并行远程解析、精确 ref/worktree 筛选及连续写后门禁。
3. 添加真实 Git 行为测试并恢复两份 CI workflow 的 worktree 测试入口。
4. 同步 Git 工作流文档，运行针对性与仓库级验证。
5. 完成独立只读复核、归档计划、写入 history，并按 auto-local-commit 精确本地提交。

## 风险与决策

- 程序化调用只减少模型返回次数；每条 Git 写命令仍单独调用、单独审批、单独检查退出状态。
- `session_id` 或缺少 `exit_code` 均不是成功，必须等待完成；只有 `exit_code === 0` 才继续。
- 首次完整 raw patch 仍由模型语义检查；后续只用内容证据复验并在漂移时返回详情。
- 只读检查器不判断用户授权、不执行 Git 写入，也不替代写入前即时复验。

## 验证

- `git-commit` 19 项、`worktree-rebase-merge` 9 项、`review-pr` 27 项、`submit-pr` 26 项和
  agent installer 6 项测试通过。
- `python3.12 scripts/validate-skills.py`、`python3.12 scripts/validate-agents.py`、两个修改 Skill
  的 `quick_validate.py`、Python compileall、两份 workflow YAML 解析和 `git diff --check` 通过。
- 只读检查器真实临时 Git 测试覆盖精确目标 worktree、dirty/untracked/rename、detached 分支冲突、
  完整触及路径、实时远程 HEAD、缓存仅诊断、进行中 merge、同分支短路和 clean-filter raw bytes。
- 当前仓库同分支显式目标检查连续 5 次为 0.36–0.41 秒，单次 JSON 约 1.2 KB；该数据只证明
  helper 本身，不代表完整 Codex 端到端耗时。
- 独立 reviewer 首轮报告 3 个 P2；修复命令/非命令成功契约、同分支提前分流和 raw bytes 指纹后，
  增量复核无 finding。
- 尚未证明跨 Git 版本、真实宿主审批/session 编排或 Codex 端到端性能；需在后续真实调用中继续
  记录端到端、工具 wall time、审批等待、模型往返和输出量。

## 完成条件

- 实现、测试、文档和 CI 一致，全部必要验证覆盖最终快照。
- 无未解决审查 finding 或验证失败。
- active plan 移入 completed，history 链接完成计划，并按规则完成本地提交。
