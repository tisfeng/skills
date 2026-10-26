# 修复 review-pr 复审分支快进

- 状态：completed
- 创建日期：2026-10-27
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 背景

P2 F1：PR head 前进后，使用 --reuse-branch 复审会拒绝落后的已关联同名分支，与普通准备的快进行为不一致。

## 目标与范围

- 目标结果：刷新 PR 快照后，在既有同名分支快进复审，不改变 upstream 或创建多余分支。
- 允许修改路径：`skills/review-pr/`、本任务 plan/history。
- 同任务 history：`docs/histories/2026-10/2026-10-27-review-pr-reuse-fast-forward.md`
- 用户限制：补充测试，验证和 Review 后本地提交，保持 main，不 push。
- 非目标：自动合并最新 base、调整 fallback 身份规则、修改全局或消费方技能。
- 验收标准：A→远程 B→冻结 B 并 --reuse-branch 成功；分支名、upstream 和本地分支集合保持不变，重复执行不增加分支；错误关联、领先和分叉仍按协议处理。

## 工作计划

1. 补充远程推进后复审测试，确认修复前失败。
2. 先校验 upstream 和身份，再允许已关联同名分支快进，更新协议。
3. 运行相关验证并按 review 技能审查最终差异。
4. 完成 history、归档计划并使用 git-commit 技能本地提交。

## 风险与决策

- 初始 HEAD 为 `16c9fc5142f1e461059be93c74bd2222018c3ecd`，main 工作树与索引干净。
- 先核验身份与 upstream，再切换并校验原 HEAD，最后只做 --ff-only；不改写本地提交。
- 领先分支仍用冻结远程对象审查，fallback 仍须准确匹配冻结 head。

## 进度

- [x] 读取规则及实现，确认基线。
- [x] 回归测试与修复。
- [x] 验证与 Review。
- [x] history、计划归档；本地提交由最终交付执行。

## 验证

- 新增远程推进用例在修复前失败（PR 分支和其他分支起始状态均复现），修复后通过。
- `python3.12 -m unittest discover -s skills/review-pr/tests`：79 项通过，包含 36 项分支准备测试。
- 消费者可移植性 3 项通过；6 个技能及发现入口校验、quick_validate、Python compileall、bash -n 和 git diff --check 通过。
- 远程本地 bare 仓库实际推进后，连续两次 --reuse-branch 复审均快进到冻结 head，分支名、upstream 和本地分支集合不变。
- 按 review 技能审查相对初始基线的完整任务差异，确认 P2 F1 已修复，关联校验先于快进、原 HEAD 在切换后复验，领先/分叉/fallback 处理符合协议，无未解决 finding；结束前复验 3 个变更技能文件 SHA-256 未漂移。
- 使用临时本地仓库和 fake gh，未操作真实 PR。

## 完成条件

P2 已修复，测试和 Review 通过，计划归档、history 完成，本地提交且不 push。
