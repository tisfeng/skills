# 优化 Git Skill 执行延迟

- 日期：2026-09-10
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-10-optimize-git-skill-latency.md)

## 目标

在不刻意缩短 `git-commit` 和 `worktree-rebase-merge`、不删除既有功能、安全门禁、逐命令权限或
完整回执的前提下，减少正常成功路径在每条 Git 命令之间反复返回模型的等待。

## 实际变更

- 两个 Skill 新增快速执行协议：首次完整 raw patch 仍由模型审核；无依赖只读检查并行执行，
  预期成功的确定性命令在一次程序化调用内逐一等待；用户确认、漂移、审批、失败、冲突和语义
  歧义仍立即返回模型。
- 明确只有命令工具使用 `exit_code === 0` 和运行中 session 完成态判断；消息文件写入等非命令
  工具按原生成功/错误契约处理。程序化调用不合并 Git 权限、命令退出状态或恢复边界。
- 新增只读 `collect-integration-facts.py`，并行解析 source 与实时远程目标，只输出精确目标
  checkout、OID、状态、操作、detached 候选及提交范围。后续复验使用显式目标，避免重复远程查询。
- 同分支在 source/target 解析后立即返回 `direct-commit`，不枚举 worktree 或提交范围；候选分支
  使用精确安静 ref 检查，不再输出全部 refs。
- 内容指纹结合 staged/unstaged Git 证据、候选 tracked 原始 bytes、文件类型/mode 及 untracked
  bytes；它用于发现采样漂移，但不替代提交前后的真实 raw patch 等价检查。
- 新增 9 项临时 Git 仓库行为测试，并在 validate 和 publish workflow 中恢复
  `worktree-rebase-merge` 测试入口；Git 工作流治理同步程序化编排与紧凑输出边界。

## 验证

- `git-commit` 19 项、`worktree-rebase-merge` 9 项、`review-pr` 27 项、`submit-pr` 26 项、agent
  installer 6 项测试通过。
- Skill/agent 仓库校验、两个修改 Skill 的 quick validation、Python 编译、workflow YAML 解析和
  `git diff --check` 通过。
- 当前仓库同分支 helper 连续 5 次为 0.36–0.41 秒，单次 JSON 约 1.2 KB。该微基准不证明完整
  Codex 端到端延迟，真实审批/session 和跨 Git 版本仍需后续调用验证。
- 独立 reviewer 的 3 个 P2 已修复；最终增量复核无 finding。

## 交付

本任务按 `auto-local-commit` 精确本地提交；未执行 push、fetch、pull、rebase、merge、发布或
下游安装。
