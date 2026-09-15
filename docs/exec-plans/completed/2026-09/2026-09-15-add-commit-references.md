# 为 Git 提交增加外部引用尾段

- 状态：completed
- 创建日期：2026-09-15
- 负责人：Codex
- 关联 Issue/PR：none

## 背景

`git-commit` 原本只接受每个语言区块的三段正文和可选 `BREAKING CHANGE:` footer，
会拒绝其他 footer。修复或设计依赖外部 PR、Issue、review thread 或文档时，提交信息因此
缺少稳定跳转入口，后续排查需要从源码注释或额外提交恢复上下文。

## 目标与范围

- 目标结果：允许在提交末尾追加一次可选 `References:` 尾段，保留直接外部链接及其简短标签。
- 允许修改路径：`skills/git-commit/references/commit-message.md`、
  `skills/git-commit/scripts/validate-commit-message.py`、
  `skills/git-commit/tests/test_validate_commit_message.py`、本计划和同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-15-add-commit-references.md`
- 用户限制：保持 Angular-style、三段正文、双语和 `BREAKING CHANGE` 既有契约；不 push。
- 非目标：不支持 `Closes:`、`Fixes:` 等具有 Issue 状态语义的 footer，不修改提交统计或回执格式。
- 验收标准：单语和双语提交可选择性携带唯一的末尾引用段；旧格式继续通过；错误位置、
  空引用、非直接 URL 和重复 URL 会被拒绝。

## 工作计划

1. 扩展提交信息契约，定义引用触发、格式、顺序及证据边界。
2. 在结构校验前提取并校验全局 `References:` 尾段，不改变语言区块校验。
3. 增加正反向单元测试及 Git 提交后消息一致性覆盖。
4. 运行针对性、Skill、portability 和 Python 静态验证。
5. 使用 `review` 审查最终快照，修复有效 finding，归档计划并创建本地提交。

## 风险与决策

- 引用尾段只出现一次并位于整个提交末尾；语言无关的 URL 不在双语区块中重复。
- 固定使用 `References:`，每项使用可选标签和绝对 HTTP(S) URL；标签只帮助阅读，URL 才是跳转目标。
- 正文仍负责解释引用与变更的关系及证据限制，尾段不能替代三段正文或制造因果结论。
- 只收录实际影响动机、诊断、设计或验证的来源，不自动收集 staged diff 中的所有链接。

## 进度

- [x] 核对现有提交信息契约、校验器、测试和 Scoco 示例提交。
- [x] 更新契约、实现和测试。
- [x] 完成验证与独立审查。
- [x] 写入 history 并归档计划；本地提交由后续精确交付完成。

## 验证

- `python3.12 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'`：18 项通过。
- `python3.12 scripts/validate-skills.py`：6 个公开 Skills 和发现入口通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：2 项通过。
- `python3.12 -m compileall -q scripts skills`：通过。
- `git diff --check`：通过。
- `review`：对基线 `e95fc40f2f14be12cbbd94eb872f5f9a6ff99e2a` 后的任务变更完成只读审查，
  无 finding；全局尾段方案比在两个语言区块重复链接更适合当前双语契约。
- 未运行外部链接可达性检查或真实 Agent 运行；校验器只验证结构，portability 测试验证隔离消费者资产。

## 完成条件

- 新旧提交格式的针对性测试全部通过。
- Skill 与隔离消费者校验通过，最终 diff 无格式错误。
- 最终快照没有阻塞 finding，计划已归档且 history 记录真实结果。
