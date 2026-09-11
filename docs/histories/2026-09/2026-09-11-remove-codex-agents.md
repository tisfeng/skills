# 移除 Codex 子代理

- 日期：2026-09-11
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-11-remove-codex-agents.md`](../../exec-plans/completed/2026-09-11-remove-codex-agents.md)

## 目标

按用户确认的方案移除 Codex 子代理，使仓库只发布平台无关的 Agent Skills：不发布新的 npm
版本并对旧包执行 deprecate、删除 `package.json`、治理规则移除子代理描述。

## 实际变更

- 删除 `.codex/agents/{planner,reviewer,tester}.toml`、`bin/codex-agents.mjs`、`src/cli.mjs`、
  `tests/agents-installer.test.mjs`、`scripts/validate-agents.py` 与 `package.json`。
- `.github/workflows/validate.yml` 移除 Codex agent 与安装器步骤并支持 `workflow_call`；
  `publish.yml` 替换为 `release.yml`，由统一校验通过后创建 GitHub Release。
- `AGENTS.md`、`docs/agents/{request-boundary,build-and-test,development,README}.md` 移除子代理
  路由、委派决策和角色边界，只保留平台无关的任务、验证与资产规则。
- `docs/design-docs/overview.md` 记录单资产结构与移除原因；`docs/release/overview.md` 与
  `.agents/skills/release/SKILL.md` 改为 tag → GitHub Release 流程。
- `README.md` 与 `README.en.md` 删除子代理目录与安装命令，新增一次性迁移说明。

## 验证

- `python3.12 -m compileall -q skills scripts`、`python3.12 scripts/validate-skills.py` 通过。
- `tests/test_validate_skills.py` 9 项、`tests/test_skill_portability.py` 3 项通过。
- 全库搜索确认子代理与 npm 安装器引用只保留在迁移说明、设计文档的历史描述和历史归档中。
- 无 `package.json` 的仓库副本执行 `npx skills add <path> --list`，仍能列出全部 7 个 Skill。

外部边界：未 push、未创建 tag、未创建 GitHub Release；npm deprecate 属于外部写入，在本次
仓库交付之外单独执行。

## 交付

仅在本仓库本地提交，不修改消费项目。
