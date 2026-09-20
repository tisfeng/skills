# 强制校验双语提交标题语言

- 状态：completed
- 创建日期：2026-09-20
- 负责人：Unknown
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** Unknown
- **Model:** Unknown
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 背景

`git-commit` 已按对话语言选择双语提交结构，但只校验正文标签，没有校验两个 subject 的语言。中文正文区块因此仍可能使用英文 subject，并通过结构校验。

## 目标与范围

- 目标结果：明确本地与英文 subject 的语言顺序，并机械拒绝已发生的错误形式。
- 允许修改路径：`skills/git-commit/references/commit-message.md`、`skills/git-commit/scripts/validate-commit-message.py`、本计划及对应 history。
- 同任务 history：`docs/histories/2026-09/2026-09-20-enforce-commit-subject-language.md`
- 用户限制：只改进语言规则；不发布新版本，不 push，不直接修改消费方快照。
- 非目标：不改变 Angular type/scope、正文段落、References 或发布流程。
- 验收标准：现有 Skill 验证通过；中文区块使用英文 subject 的样例失败；正确中英双语样例通过。

## 工作计划

1. 收紧提交语言契约与校验器。
2. 运行现有测试、Skill 验证和临时回归样例。
3. 审查最终差异，记录 history 并创建本地提交。

## 风险与决策

- 根据中文正文标签识别中文本地区块，不新增 CLI 参数，不破坏其他非英语双语消息。
- 英文镜像 subject 必须包含 ASCII 字母、不得包含汉字，并与本地 subject 不同。

## 进度

- [x] 更新规则与校验器。
- [x] 完成验证与审查。
- [x] 记录 history 并归档计划。

## 验证

- 现有测试、可移植性、Skill 结构和临时回归样例均通过；详情见同任务 history。

## 完成条件

- 新语言约束拦截错误样例且不破坏现有验证矩阵。
- history 与本地提交完成，工作树干净。
