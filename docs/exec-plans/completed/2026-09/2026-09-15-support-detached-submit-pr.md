# 支持 detached checkout 提交 PR

- 状态：completed
- 创建日期：2026-09-15
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

`submit-pr` 已定义 `<type>/<kebab-case-summary>` 默认任务分支格式，但 helper 在仓库拓扑发现阶段
直接拒绝 detached HEAD，导致调用 Agent 无法为已经提交的 detached checkout 创建任务分支并继续
PR 流程。

## 目标与范围

- 目标结果：调用 Agent 在 detached checkout 自动推导任务分支名；helper 的 `plan` 只读预览，
  `apply` 从冻结 HEAD 创建或复用本地分支 ref，且不切换 checkout。
- 允许修改路径：`skills/submit-pr/`、`tests/test_skill_portability.py`、本计划及对应 history。
- 同任务 history：`docs/histories/2026-09/2026-09-15-support-detached-submit-pr.md`
- 用户限制：本轮实施并创建本地提交；不 push、不创建 PR、不发布版本。
- 非目标：不修改 `git-commit` 的分支命名协议，不改变 PR 正文、Issue 或 GitHub 验证契约。
- 验收标准：detached plan 无 Git 写入；detached apply 创建精确分支 ref 并保持 checkout detached；
  attached checkout 现有行为不回归。

## 工作计划

1. 更新 `submit-pr` 入口和工作流契约，定义 detached 自动命名及不切换 checkout 的边界。
2. 让 helper 以可空当前分支解析拓扑、计划 head 分支并在写入前校验 checkout 漂移。
3. 增加 detached plan、apply、缺失名称、状态漂移和隔离消费者行为测试。
4. 运行相关单测、Skill 校验、Python 编译和 diff 检查，记录 history 并创建本地提交。

## 风险与决策

- helper 不从可能为非英文的 PR 标题机械生成分支名；调用 Agent 依据用户、项目、任务和 diff 语义
  生成候选，并显式传入 `--head-branch`。
- `plan` 不创建 ref；只有已有 PR 校验完成后的 `apply` 才允许创建或更新本地 ref。
- detached checkout 不具备 branch-scoped Git 配置，拓扑发现跳过这些配置并沿用现有显式参数和
  repository/default remote fallback。
- 本地分支冲突继续使用现有兼容性与数字后缀策略；不 force push。

## 进度

- [x] 更新 Skill 契约和 helper。
- [x] 补充行为与可移植性测试。
- [x] 完成验证、history、归档和本地提交准备。

## 验证

- `submit-pr` 23 项行为测试通过。
- 2 项隔离消费者可移植性测试通过。
- 6 个公开 Skill 与仓库发现入口通过校验，`submit-pr` 通过 `skill-creator` quick validate。
- Python 编译和 `git diff --check` 通过。

## 完成条件

- detached 与 attached 场景通过最终快照验证，diff 无无关变更，计划已归档并进入本地提交交付。
