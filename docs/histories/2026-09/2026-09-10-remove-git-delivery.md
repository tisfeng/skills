# 移除 Git 交付子代理并简化工作流

- 日期：2026-09-10
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-10-remove-git-delivery.md)

## 目标

按用户批准的方案，由当前模型直接完成 Git 交付，删除专用角色与多余交接协议，并选择性撤销
`f2cd711` 中不再需要的实现。该角色和部分协议早于此提交，因此没有整笔 revert。

## 实际变更

- 删除 `.codex/agents/git-delivery.toml`、集成检查脚本及专属测试。
- 宿主规则与 worktree Skill 改为主 Agent 串行执行，去掉阶段派发、角色回退和重复回执编排。
- 保留四种暂存策略、候选 patch 核对、状态复验、受限路径权限处理、提交前后校验和完整回执；
  限定路径时仍检查每个提交，多提交统计使用合并前目标 OID 和 rebase 后源 OID。
- 更新中英文目录及旧安装清理说明；暂存契约测试继续覆盖两个 Skill，不再读取已删除的角色。
- planner、reviewer、tester 配置不变，原 completed plan/history 保留，安装器实现不变。

## 验证

- `python3.12 scripts/validate-skills.py`：6 个 Skill 通过。
- `python3.12 scripts/validate-agents.py`：3 个子代理通过。
- Git 提交相关单测 19 项、worktree 暂存契约单测 2 项通过。
- `python3.12 -m compileall -q scripts skills` 与 `git diff --check` 通过。
- 现行规则链接和删除路径引用检查通过；其余三个 TOML 与初始 HEAD 完全一致。
- `node bin/codex-agents.mjs add . --list` 只读发现 planner、reviewer、tester。
- 复用前轮独立规划；本轮独立只读审查及增量复核未发现需修复的问题。

## 交付

本任务按 auto-local-commit 由当前主 Agent 直接交付。未执行 push、发布、全局或下游安装修改；
源码与静态验证不代表已安装角色自动卸载或 Codex 运行时重载。
