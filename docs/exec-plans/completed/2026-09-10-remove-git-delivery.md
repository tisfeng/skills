# 移除 Git 交付子代理并简化工作流

- 状态：completed
- 创建日期：2026-09-10
- 负责人：Codex
- 关联 Issue/PR：none

## 目标与授权

用户批准执行已交付方案：删除 `git-delivery`，由当前模型直接执行 Git 工作流，并选择性撤销
`f2cd711` 引入的复杂协议。复用前轮已完成的独立规划，不改动 planner、reviewer、tester。
任务为 implementation，交付授权为 auto-local-commit；用户指定当前模型执行，覆盖旧的强制
Git 委派规则。不 push、发布、改写历史或修改下游及全局安装。

## 写入前状态与范围

- 初始 HEAD：`f2cd711e87990e8317e86fd8eea4274c98bf0f1a`，分支 `main`。
- 初始 staged、unstaged、untracked 和冲突均为空，写入前检查通过，候选自动提交资格成立。
- 允许修改及 Agent-owned 路径：`.codex/agents/git-delivery.toml`、两份根 README、
  `docs/agents/git-workflow.md`、`docs/agents/request-boundary.md`、`skills/git-commit/SKILL.md`、
  `skills/worktree-rebase-merge/SKILL.md`、该 Skill 的集成检查脚本及其测试、现有暂存契约测试，
  以及本计划（完成后归档）和同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-10-remove-git-delivery.md`。
- 最终按实际差异冻结精确提交路径；所有修改属于本任务，无用户原有内容需要合并。

## 工作计划

1. 删除角色、集成检查脚本及配套测试，移除宿主和 Skill 中的交接协议及角色依赖。
2. 保留暂存范围保护、提交前后校验、状态复验、权限处理、真实信息和完整回执。
3. 更新目录与旧安装说明，调整现有暂存契约测试，不修改安装器实现。
4. 运行针对性验证和独立只读审查，记录实际结果并归档计划，再由当前模型精确暂存和本地提交。

## 风险与验收

不整笔 revert：角色和部分交接规则早于 `f2cd711`。保留此前历史记录和四种暂存策略，删除重复
编排；多提交统计仍使用合并前目标 OID 与 rebase 后源 OID。源码删除不会自动卸载旧安装。
验收要求现行工作流不再依赖已删角色或脚本，其他三个角色内容不变，相关检查通过且回执完整。

## 验证

6 个 Skill、3 个子代理结构校验通过；Git 提交相关 19 项与暂存契约 2 项单测、Python 编译、
现行引用检查和 `git diff --check` 通过。安装器只读目录发现仅列出三个保留角色，三份 TOML 与
初始 HEAD 一致。独立只读审查及增量复核无待修复问题。未执行下游安装更新或 Codex 运行时重载。

实现与验证已完成；最终交付使用 git-commit 的唯一精确暂存及提交前后校验，由当前模型执行。
