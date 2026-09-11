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

## 后续清理（同任务续办）

移除后复查发现残留，按用户确认逐项处理：

- 两份 README 删除子代理迁移说明，不再描述已移除的能力或 npm 包状态。
- 删除无人执行的 `tests/test_validate_skills.py`，该测试已不在 CI 或文档的维护面内。
- `docs/agents/build-and-test.md` 标题改为「构建与测试」，并删除已失效的 `tomllib` 版本说明
  （其唯一使用者 `scripts/validate-agents.py` 已删除）。
- 移除本地空目录 `.codex/`、`bin/`、`src/`；这些目录本就不进入 Git 树。

验证：`python3.12 scripts/validate-skills.py`、`compileall`、5 套 Skill 单测与隔离消费者测试
全部通过；103 个 Markdown 文件的相对链接与锚点无失效；现行文档不再出现子代理、安装器或
npm 包引用，仅 `docs/design-docs/overview.md` 保留说明结构性变更理由的历史描述。

## 后续清理（第二轮）

按用户确认删除设计文档中对已移除能力的说明：`docs/design-docs/overview.md` 不再保留修订标注、
背景段落和重新评估条目，仓库现状由其余内容描述。同时清理本仓库与主 checkout 中被 `.gitignore`
忽略的 `__pycache__` 缓存目录。

验证：`python3.12 scripts/validate-skills.py` 通过；103 个 Markdown 文件的相对链接与锚点无
失效；`git diff --check` 通过；现行文档不再出现已移除能力的任何说明，缓存目录数量为 0。
