# 公开技能在本仓库自用

- 状态：实现和验证完成
- 授权：用户确认“执行”；implementation，auto-local-commit。
- 初始 HEAD：`4833d34612aef0be534ddf8cb36dfe55cd996795`，detached HEAD。
- 初始 staged、unstaged、untracked 和冲突路径均为空，无用户差异。
- 独立规划：复用上一轮 Planner 的逐项相对链接方案，关键事实仍成立。

## 目标与范围

保留 `skills/` 为公开技能的唯一源码，在 `.agents/skills/` 添加六个相对目录链接，并保留
内部 `release` 实目录。允许路径及 Agent 内容范围：六个链接、`scripts/validate-skills.py`、
`tests/test_validate_skills.py`、`docs/agents/README.md`、`docs/agents/build-and-test.md`、
`docs/design-docs/overview.md`、本计划及同任务 history。

只进行本仓库修改和一次精确本地提交；不安装全局技能、不发布、不推送、不创建分支。

## 工作计划

1. 已添加六个发现入口，同步源码与发现入口的职责说明。
2. 已增加链接完整性校验；独立 tester 的九项针对性测试通过。
3. 技能、Agent、Python 编译、相对链接和差异检查通过；Codex 的技能发现接口返回七个启用的
   项目技能，公开技能均解析到当前 worktree 的源码。
4. 已记录静态与运行时验证边界并归档本计划；最终按 auto-exact 冻结精确范围并本地提交。

## 风险与完成条件

- 同名全局技能可能并存；不能假定项目入口会自动覆盖全局版本。
- 相对目录链接只保证支持符号链接的 checkout 可用；其他宿主需单独验证发现规则。
- 校验器必须拒绝错误入口并保留内部技能；完成不以重启用户应用或修改全局配置为前提。
- 仓库检查通过且如实记录 Codex 发现证据或环境限制后交付。
