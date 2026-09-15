# 简化提交语言选择并本地化正文标记

- 日期：2026-09-15
- 状态：completed
- 关联计划：[`2026-09-15-localize-commit-body-labels.md`](../../exec-plans/completed/2026-09/2026-09-15-localize-commit-body-labels.md)

## 目标

让 `git-commit` 优先依据用户明确偏好和当前对话选择提交信息语言，并为三个正文段增加易于扫描、
可由脚本验证的背景、变更和影响标记。

## 实际变更

- 将语言优先级简化为“用户明确指定、当前对话、系统偏好”，仅在三项都无法判断时使用 English，
  不再枚举平台 locale 变量。
- 中文区块固定使用 `背景：`、`变更：`、`影响：`；英文及其他非中文本地区块使用小写
  `context: `、`change: `、`impact: `，并同步更新完整提交回执示例。
- 校验器要求每个语言区块恰好按顺序使用一套标记且正文非空，拒绝旧无标记、大小写错误、错序、
  混用、额外空格和旧的 `result:` 标记。
- 测试继续覆盖 `BREAKING CHANGE`、全局 `References:`、提交后实际消息一致性和隔离消费者资产。

## 验证

- git-commit 单元测试 19 项通过，2 项隔离消费者 portability 测试通过。
- 6 个公开 Skills 和仓库发现入口校验通过；Python compileall、`git diff --check` 通过。
- 提交前 `review` 无 finding。
- `skill-creator` 的轻量校验器因当前 Python 缺少 `PyYAML` 未能启动；仓库自身 Skill 校验已通过。
  未运行真实 Agent 或安装态 Skill 测试。

## 交付

本任务按仓库 `auto-local-commit` 规则精确暂存上述 Skill、测试、plan 和 history，并创建带
`BREAKING CHANGE` 说明的 Angular-style 双语本地提交；未执行 push、PR、发布或下游安装。
