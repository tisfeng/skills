# 统一技能边界并精简重复规则

- 状态：completed
- 创建日期：2026-09-10
- 负责人：Codex

## 目标与授权

用户批准执行上一轮审查方案，并明确同意调整 PR 刷新条件和删除纯措辞暂存测试。
复用已完成的独立规划，修正提交/PR 准备顺序与授权衔接，再合并重复说明，保持双语提交、
完整交付回执和实际安全检查。任务为 implementation，默认 auto-local-commit，由当前主 Agent
直接完成本地交付；不 push、发布、操作真实 PR 或修改下游安装及子代理配置。

## 写入前状态与范围

- 初始 HEAD：`e4240dacad4cf10349fb8a5e0f0154945971f66c`，分支 `main`。
- 初始 staged、unstaged、untracked 和冲突均为空；写入前检查通过，候选自动提交资格成立。
- 允许修改：`skills/{git-commit,worktree-rebase-merge,review-pr,submit-pr,code-simplifier}/SKILL.md`、
  `skills/submit-pr/references/workflow.md`、worktree 的措辞测试、`docs/agents/{request-boundary,git-workflow}.md`、
  `.agents/skills/release/SKILL.md`、`docs/release/overview.md`、两份 CI workflow 中对应的测试步骤，
  以及本计划和同任务 history。必要的针对性测试限现有 Skill 测试目录。
- 以上实际变更均归本任务所有，最终精确冻结提交路径。
- 同任务 history：`docs/histories/2026-09/2026-09-10-align-skill-workflows.md`。

## 工作安排

1. 前置提交模式判断，统一预览规则，修正子目录暂存；明确 PR review 有限准备权限。
2. 调整 submit-pr 的 staged/base 准备顺序，保持 plan 只读和当前最新 base 限制。
3. 精简 Git、review-pr、submit-pr、code-simplifier 和 release 中重复说明；删除措辞测试及 CI 调用。
4. 执行相关脚本测试、结构/链接校验、实际场景检查和独立复核，补齐记录并归档计划后本地提交。

## 风险与验收

不把纯预览升级为暂存，不把 PR 准备升级为自动提交、修复或远程操作；显式路径保持原位置含义。
不新增交接协议、通用框架或模拟实现的测试。最终线程刷新基于已检查快照，失败与新活动如实报告。
已发布的消息格式和完整回执保持不变；发布流程仅整理说明，不触发发布。

## 验证

实现完成。69 项脚本测试、Skill/agent 结构检查、修改 Skill 的 quick_validate、Python 编译、
两份 YAML 解析、链接/锚点检查与 diff 检查通过。独立仅预览场景保持工作文件和 Git 元数据不变；
根目录暂存、相对路径及首次 PR 提交准备场景通过。消息契约和完整回执区块与基线逐字一致。
独立审查及增量复核无待修复问题；实际范围和验证边界记录在同任务 history 中。
