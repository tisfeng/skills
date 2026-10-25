# review-pr 先回复再关闭线程

- 状态：completed
- 创建日期：2026-10-25
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 背景

现有 review-pr 检查开放线程，但关闭时不回复，且普通审查需要另行取得维护授权。

## 目标与范围

- 目标结果：已修复或不再适用的开放线程先回复说明依据，再关闭；保留只读限制。
- 允许修改路径：`skills/review-pr/`、本计划及同任务 history。
- 同任务 history：`docs/histories/2026-10/2026-10-25-review-pr-reply-resolve.md`
- 用户限制：验证后本地提交，不 push；保持当前分支。
- 非目标：真实 PR 操作、发布、全局安装和其他技能改造。
- 验收标准：回复成功后才关闭；部分失败有回执；刷新后可复用已有回复；outdated 不自动关闭。

## 工作计划

1. 更新技能授权、判定、回复和报告协议。
2. 更新线程 helper 与 fake API 测试（用户已批准包含测试的方案）。
3. 运行相关验证，按 review 技能审查并修复有效问题。
4. 更新 history、归档计划并按 git-commit 技能本地提交。

## 风险与决策

- 回复和关闭是两次远程操作：分别记录结果，失败不盲目重试。
- 复用现有快照和刷新机制；新协议使用 version 2 和显式回复开关，避免旧调用静默发布评论。
- 复用回复前必须重新采集、复核并生成当前 plan，不跳过指纹检查。

## 进度

- [x] 读取规则、确认初始 main 分支与干净工作树；基线 `89de84611e9ce706f98a3fd6d60040aa2466b8dc`。
- [x] 实现与测试。
- [x] 验证、Review、history 和归档；提交由本任务最终交付执行。

## 验证

- `python3.12 -m unittest discover -s skills/review-pr/tests`：68 项通过。
- 最终源码快照的 `test_review*.py`：39 项通过；其中线程测试 18 项。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：3 项通过。
- `python3.12 scripts/validate-skills.py`：6 个技能及发现入口通过。
- skill-creator `quick_validate.py skills/review-pr`、Python compileall 和 `git diff --check` 通过。
- 按 review 技能审查任务相对初始基线的完整 diff；回复必须为已发布状态、gh 正文按字符串传递两项已修复并复验，无未解决 finding。现有快照检查足够，无需新增状态管理框架。
- 不操作真实 PR。

## 完成条件

- 相关验证通过，无未解决的有效 Review finding，完成 history 后归档。
