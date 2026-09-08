# 恢复通用 Agent 自动本地提交链路

- 日期：2026-09-08
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-08-restore-auto-local-commit.md`](../../exec-plans/completed/2026-09-08-restore-auto-local-commit.md)

## 目标

修复从 Easydict 移植 Agent 治理规则时丢失的 implementation 自动本地提交授权与安全收尾链路，
并保持 Skill、子代理对不同宿主项目的通用性。

## 实际变更

- 恢复 planning、implementation、delivery authorization 与 protected 的独立状态，明确
  implementation 在没有持续禁止要求时默认候选自动本地提交。
- 增加首次 Git 快照、Agent-owned paths、最终内容验证、history 与精确暂存的完整门禁。
- 扩充通用 `git-delivery` 的 `commit`、`auto-local-commit`、`integration` 和 prepare/apply
  协议，但仍只消费宿主规则或调用方已经授予的权限。
- 澄清 `git-commit` 的 `initial_head`、允许路径与实际提交路径、唯一暂存步骤和 Agent 文档策略。
- 更新执行计划模板，使交付授权、持续限制、写入前状态和验证边界可被明确记录。

## 审查与修复

- 独立 reviewer 发现显式 staged 提交可能因重复暂存混入同路径未暂存内容；已改为只冻结和复验
  staged raw patch，空索引候选才执行一次精确暂存。
- 独立 reviewer 发现仅修改 plan/history 的 implementation 在宿主规则与 Skill 间存在冲突；
  已改为由宿主仓库政策决定。
- 增量复核确认上述问题已修复，未发现远程授权扩大、重复确认或既有提交 integration 回归。

## 验证

- `python3 scripts/validate-skills.py`
- `python3 scripts/validate-agents.py`
- `python3 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`
- `node --test tests/agents-installer.test.mjs`
- `git diff --check`

`skill-creator` 的独立 `quick_validate.py` 因当前环境缺少 PyYAML 未执行成功；仓库自带的 Skill
与 Agent validator 均通过。静态规则和测试不能证明未来真实 Agent 每次都会遵守新策略。

## 交付

本任务通过自动本地提交门禁创建一个本地提交；未 push、pull、rebase、merge、发布或修改
Easydict 与用户全局 Codex 配置。
