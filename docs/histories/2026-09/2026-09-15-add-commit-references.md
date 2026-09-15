# 为 Git 提交增加外部引用尾段

- 日期：2026-09-15
- 状态：completed
- 关联计划：[`2026-09-15-add-commit-references.md`](../../exec-plans/completed/2026-09/2026-09-15-add-commit-references.md)

## 目标

让 `git-commit` 在变更依赖外部 PR、Issue、review thread、文档或网页时，将实际影响决策的
来源保存在可直接跳转的提交信息中，同时保留既有 Angular-style、三段正文、双语和
`BREAKING CHANGE` 契约。

## 实际变更

- 增加全局可选 `References:` 尾段：它固定出现在整个提交末尾，在双语模式下只出现一次，
  不重复语言无关的 URL。
- 每个引用条目使用可选标签和绝对 HTTP(S) URL；契约要求精确页面、最小来源集合、稳定顺序、
  URL 去重和明确证据边界，并排除具有 Issue 状态语义的 `Closes:`、`Fixes:`、`Resolves:`。
- 校验器在单双语解析前提取引用尾段，拒绝空段、错误标题或位置、非列表条目、非绝对 URL、
  无效 URL 和重复 URL；原有无引用消息及 `BREAKING CHANGE` 行为保持不变。
- 测试覆盖英文、双语、与 breaking footer 共存、提交后消息一致性，以及引用位于正文或双语
  区块之间等错误形式。

## 验证

- git-commit 单元测试 18 项通过。
- 6 个公开 Skills 和仓库发现入口校验通过；2 项隔离消费者 portability 测试通过。
- Python compileall、`git diff --check` 通过。
- 提交前 `review` 无 finding。未运行外部链接可达性检查或真实 Agent 运行；结构校验不替代引用
  内容的语义核实。

## 交付

本任务按仓库 `auto-local-commit` 规则精确暂存上述 Skill、测试、plan 和 history，并创建
Angular-style 双语本地提交；未执行 push、PR、发布或下游安装。
