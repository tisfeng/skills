# 移除 Codex 子代理

- 状态：completed
- 创建日期：2026-09-11
- 负责人：main agent
- 关联 Issue/PR：none

## 背景

本仓库同时发布可复用的 Agent Skills 与 Codex 子代理。子代理依赖 Codex 的 TOML 配置、
`.codex/agents/` 发现目录和模型字段，其他 agent 平台无法适配，成为仓库中唯一的平台专属表面。
用户决定移除子代理，使仓库只发布平台无关的 Skills。

## 任务摘要

- 意图模式：implementation
- 交付授权：auto-local-commit
- 安全状态：normal
- 受阻操作及原因（如有）：npm deprecate、push、tag、GitHub Release 属于外部写入，另行授权
- 目标结果：删除子代理资产与安装器；仓库只保留 Skills；发布流程退化为 tag → GitHub Release
- 允许修改路径：`.codex/agents/`、`bin/`、`src/`、`tests/agents-installer.test.mjs`、
  `scripts/validate-agents.py`、`package.json`、`.github/workflows/`、`AGENTS.md`、`README.md`、
  `README.en.md`、`docs/agents/`、`docs/design-docs/overview.md`、`docs/release/overview.md`、
  `.agents/skills/release/SKILL.md`、本计划、同任务 history
- 同任务 history：`docs/histories/2026-09/2026-09-11-remove-codex-agents.md`
- 禁止动作：push、创建或移动 tag、发布或 deprecate npm、修改消费项目
- 预期交付物：单一资产类型的仓库源码、更新后的治理与用户文档、本地提交
- 验收标准：静态校验通过；无残留的子代理或安装器引用；文档与 workflow 和实际资产一致

## 语义与范围

- 用户要求 Agent 做什么：执行已确认的移除方案
- 用户已确认的决策：不发布新版本并 `npm deprecate`；删除 `package.json`；治理规则移除子代理描述
- 否定、条件和范围限制：不重新引入子代理；不改写历史归档；外部发布动作单独授权
- 歧义：无

## 写入前状态

- 写入前检查：pass
- 自动提交资格及原因：eligible，初始索引为空且工作树干净
- 初始 HEAD：`c2b5689dd18e69120141c8e5b7a727f4976572bc`
- 初始 staged / unstaged / untracked 路径：均为空
- 初始冲突：无
- Agent-owned paths：见“允许修改路径”

## 目标与非目标

### 目标

- 删除子代理配置、安装器代码、安装器测试与 agent 校验器。
- 让 CI 与发布 workflow 只覆盖 Skills，并让 tag workflow 复用统一校验。
- 把治理规则、设计文档、发布文档与两份 README 改写为单资产结构。

### 非目标

- 不新增替代的子代理或平台专属机制。
- 不改写 `docs/histories/`、`docs/exec-plans/completed/`、`docs/release/changelog/` 的历史事实。
- 不执行 push、tag、Release 或消费项目迁移。

## 工作计划

1. 记录基线并验证 `skills` CLI 不依赖 `package.json`。
2. 删除子代理资产与安装器相关代码、测试和校验器。
3. 更新两个 workflow，使释放流程为“统一校验 → GitHub Release”。
4. 改写治理、设计与发布文档，移除全部子代理描述。
5. 更新两份 README 并补迁移说明。
6. 运行验证矩阵，创建 history，本地提交。

## 风险与决策

- `package.json` 删除后 Skills 仍可安装，已用无包清单的仓库副本实测确认。
- 治理规则不再要求委派子代理，独立审查能力降级为环境相关；本次按用户决定移除。
- tag workflow 无法本地端到端验证，只能由首次真实发布暴露。

## 验证

- `python3 scripts/validate-skills.py`、`python3 -m compileall -q skills scripts`、`git diff --check`。
- 全库搜索确认 `.codex/agents`、`@tisfeng/codex-agents`、`validate-agents` 仅出现在历史归档。
- Markdown 相对链接与锚点扫描；workflow YAML 解析。
- 无 `package.json` 的仓库副本执行 `npx skills add <path> --list`。

## 完成条件

- 上述验证全部通过，仓库差异只包含本计划允许的路径，本地提交完成。

## 完成结果

子代理资产、npm 安装器代码与测试、agent 校验器和 `package.json` 已删除；CI 只覆盖 Skills，
发布 workflow 改为复用统一校验后创建 GitHub Release。治理、设计、发布文档和两份 README
已改写为单资产结构，并加入一次性消费方迁移说明。外部动作（push、tag、Release、npm
deprecate）未在本计划内执行。
