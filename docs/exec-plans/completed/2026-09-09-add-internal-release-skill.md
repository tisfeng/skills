# 添加项目内部发布 Skill

- 状态：active
- 创建日期：2026-09-09
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

仓库已有 tag 驱动的 npm 与 GitHub Release 自动化，但没有项目内的自然语言发布 Skill、统一的发布
文档入口或可作为 GitHub Release 正文的版本日志。用户要求在 `.agents/skills/release/` 建立内部
Skill，并在 `docs/release/` 集中维护发布说明和日志。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 目标结果：提供项目内部发布 Skill、发布文档和以版本日志创建 GitHub Release 的 CI 支持。
- 允许修改路径：`.agents/skills/release/`、`.github/workflows/publish.yml`、`docs/agents/README.md`、
  `docs/design-docs/overview.md`、`docs/release/`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-09-add-internal-release-skill.md`
- 禁止动作：不修改 `AGENTS.md`，不变更 `package.json`，不创建 `0.3.2` 发布日志，不 push、创建 tag、
  发布 npm 或 GitHub Release。
- 验收标准：`.agents/skills/release/SKILL.md` 提供项目内标准 Skill 格式；发布日志在 npm 发布前被 tag workflow
  校验，并作为 GitHub Release 正文；发布 CI 覆盖 worktree 测试。

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible；初始工作树与索引干净，路径和归属明确。
- 初始 HEAD：`f9f76fa1b77346a8fa3587b65f4c79c408c3349a`
- 初始 staged、unstaged、untracked 路径：none
- 初始冲突：none
- Agent-owned paths：所有允许修改路径。

## 工作计划

1. 创建简洁的内部 `release` Skill，以及发布文档入口、流程说明和日志模板。
2. 说明内部 Skill 与公开 `skills/` 的资产边界，但不在 `AGENTS.md` 增加路由。
3. 让 tag workflow 在 npm 发布前验证版本日志，使用该日志创建 GitHub Release，并补齐 worktree 单测。
4. 创建 history，验证 Skill、Markdown 链接、YAML、现有检查和 npm 打包载荷。
5. 按自动本地交付规则提交精确路径，不 push。

## 风险与决策

- `.agents/skills/release/` 是用户明确要求的项目内标准 Skill 位置；不放入公开 `skills/` 目录。
- 目录本身不能证明下游 `npx skills` 的发现行为；实施后只报告本地结构校验，另行隔离验证该边界。
- 不预先创建 `0.3.2.md`，避免将未发生的发布写成日志。
- Release job 必须 checkout tag 内容后才能读取日志；日志检查前置到 validate job，避免 npm 已发布后才失败。

## 验证

- 内部 Skill frontmatter、相对链接和发布文档链接通过仓库无依赖校验器验证。
- `python3 scripts/validate-skills.py`、`python3 scripts/validate-agents.py`、worktree 单测、Ruby YAML
  解析、`npm pack --dry-run --json` 和 `git diff --check` 均通过。
- `skill-creator` 的 `quick_validate.py` 受环境缺少 `PyYAML` 阻塞；无依赖替代校验已通过。真实发布、
  GitHub Actions 与下游自动发现未运行，不能由静态验证替代。

## 完成条件

- [x] 内部 Skill、发布文档和日志模板存在且职责不重复。
- [x] tag workflow 使用版本日志并覆盖 worktree 单测。
- [x] history、验证和本地提交完成；未发生外部发布。
