# 移植 Scoco Agent 治理规则

- 日期：2026-09-15
- 状态：completed
- 关联计划：
  [`2026-09-15-port-scoco-agent-governance.md`](../../exec-plans/completed/2026-09/2026-09-15-port-scoco-agent-governance.md)

## 目标

参考 Scoco `dev` 的现行 Agent 文档，将可复用的测试授权、编码规范和文档命名规则语义移植到
skills 仓库，同时保留本仓库自己的 Skill 源码、验证和发布边界。

## 实际变更

- 明确只有用户在当前任务中要求添加测试代码时，才允许新增或扩写测试；未获授权时仍可运行、
  分析现有测试并建议补充测试。
- 将 `docs/agents/development.md` 重命名为 `coding-guidelines.md`，补充跨语言组织、命名和注释规则，
  并更新根任务路由。
- 将 completed plan 的归档依据统一为文件名月份，允许版本号等稳定标识在 slug 中保留点号，模板
  统一引用 `docs/agents/README.md` 的命名规则。
- 保留本仓库的验证矩阵、Skill 源码与发现边界、发布授权和历史事实，不引入 Scoco 专属规则。

## 验证

- `git diff --check`：通过。
- 现行文档旧路径扫描：无 `development.md` 引用。
- 关键语义检查：测试授权、现有测试运行边界、归档月份、稳定标识和新路由均存在。
- 变更文档相对链接与锚点检查：通过。

## 交付

- 使用 Angular-style 双语提交信息创建一个本地提交。
- 未执行 push、Pull Request、发布或其他外部写入。
