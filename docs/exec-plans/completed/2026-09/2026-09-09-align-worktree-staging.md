# 对齐 worktree 集成暂存规则

- 状态：completed
- 创建日期：2026-09-09
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

`git-commit` 允许空索引的显式、未限定范围交付执行一次 `git add .`，但
`worktree-rebase-merge` 在总规则、直接提交和源分支提交路径中要求空索引停止。通用
`git-delivery` 协议也未区分显式 integration 的全工作树候选与 implementation 自动提交的精确候选。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 受阻操作及原因（如有）：none
- 目标结果：让显式、未限定范围的 worktree integration 复用一次性暂存规则，同时保持自动本地提交精确暂存。
- 允许修改路径：`skills/git-commit/SKILL.md`、`skills/worktree-rebase-merge/`、`.codex/agents/git-delivery.toml`、`docs/agents/git-workflow.md`、`.github/workflows/validate.yml`、本计划、同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-09-align-worktree-staging.md`
- 禁止动作：不修改下游安装副本，不 push、pull、rebase、merge、发布或修改用户全局 Codex 配置。
- 预期交付物：统一暂存决策矩阵、明确的交付代理暂存策略、回归测试和 CI 覆盖。
- 验收标准：四类暂存场景无冲突；结构、代理、单测与差异检查通过；创建一次本地提交且未 push。

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible；用户已明确要求执行，初始索引和工作树干净，范围可精确分离。
- 初始 HEAD：`0613ad47004cb30918bd03c5e531f57a6c7d67f1`
- 初始 staged 路径：none
- 初始 unstaged 路径：none
- 初始 untracked 路径：none
- 初始冲突：none
- Agent-owned paths：本计划及上述允许路径内由本任务产生的差异。

## 目标与非目标

### 目标

- 统一已有索引、显式路径、显式未限定范围和自动提交的暂存决策。
- 使 `worktree-rebase-merge` 不再以局部规则覆盖 `git-commit` 的显式交付契约。
- 为交付代理冻结并重验暂存策略和候选快照。
- 以回归测试保护规则对齐。

### 非目标

- 不改变提交信息、统计、rebase、merge、目标 worktree 或远程操作规则。
- 不放宽自动本地提交为 `git add .`。
- 不同步或修改 boss-resume 中已安装的副本。

## 工作计划

1. 在 `git-commit` 定义共享暂存决策矩阵，区分显式全工作树和自动精确暂存。
2. 让 worktree 和 git-delivery 只消费该矩阵及主 Agent 冻结的策略，暂存后重验 raw patch。
3. 更新仓库 Git 交付规则，记录 integration 的候选快照与策略边界。
4. 新增规则回归测试并接入 CI，创建 history，执行最终验证和本地交付。

## 风险与决策

- `git add .` 仅适用于初始索引为空、用户明确交付且未限定路径的场景；暂存前后候选变化均进入 protected。
- 显式 integration 与 implementation 自动交付是不同授权路径；后者始终精确暂存。
- 静态契约测试只能防止文档规则漂移，不能证明未来 Agent 的实际执行。

## 验证

- `python3.12 scripts/validate-skills.py`
- `python3.12 scripts/validate-agents.py`
- `python3.12 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`
- `python3.12 -m unittest discover -s skills/worktree-rebase-merge/tests -p 'test_*.py'`
- `node --test tests/agents-installer.test.mjs`
- `git diff --check`

## 进度

- [x] 定义共享暂存策略并复用至 worktree integration。
- [x] 更新交付代理与仓库 Git 规则。
- [x] 新增回归测试与 CI 覆盖。
- [x] 创建 history，完成最终验证并准备自动本地提交。

## 完成条件

- worktree、git-commit、git-delivery 与仓库 Git 规则不再相互覆盖暂存策略。
- 所有适用检查通过，计划归档、history 链接最终计划。
- 本任务创建一次经提交前后校验的本地提交，工作树干净且未 push。
