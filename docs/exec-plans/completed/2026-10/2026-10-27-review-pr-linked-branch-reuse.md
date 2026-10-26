# review-pr 复用已关联的同名分支

- 状态：completed
- 创建日期：2026-10-27
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `GPT-6`
- **Environment:** `macOS 27.0.1 / Xcode 27.2 (27B5019j)`

## 背景

当前 helper 对其他作者 PR 的等价 upstream 别名、领先分支和既有 worktree 仍采用 collision fallback，导致已关联分支被重复准备。

## 目标与范围

- 目标结果：同名且 upstream 指向准确 PR head 时，不受作者身份限制直接复用；不存在同名分支时创建并自动关联。
- 允许修改路径：`skills/review-pr/`、本任务 plan/history。
- 同任务 history：`docs/histories/2026-10/2026-10-27-review-pr-linked-branch-reuse.md`
- 用户限制：保持 main 分支，补充测试，完成验证与 Review 后本地提交，不 push。
- 非目标：改动无关联同名分支的原有处理策略、修改全局安装或消费方、操作真实 PR。
- 验收标准：首次和复审一致复用，领先保留、落后快进、分叉停止，已有干净 worktree 可复用；明确隔离模式仍按用户要求执行。

## 工作计划

1. 统一已关联分支的身份判断与首次、复审及 worktree 准备流程。
2. 更新现行协议与相关测试，保持无关行为。
3. 运行相关验证，使用 review 技能审查任务差异并修复有效 finding。
4. 完成 history、归档计划，使用 git-commit 技能本地提交。

## 风险与决策

- 初始 HEAD 为 `3614d540fad84512a3a2c053ec699e6caef5eb0f`，main 工作树与索引干净。
- 关联以 Git upstream 的实际 remote 仓库地址和远程分支为准，不新增存储，也不以同名代替身份判断。
- 保留 self_authored 回执字段的原义，新增关联分支的准确回执说明。
- 本地领先时审查冻结远程 Git 对象；分叉不覆盖、不另建分支绕过。

## 进度

- [x] 读取规则、实现和现有测试，确认基线。
- [x] 实现、协议与测试。
- [x] 验证与 Review。
- [x] history 与计划归档；本地提交由最终交付执行。

## 验证

- `python3.12 -m unittest discover -s skills/review-pr/tests`：77 项通过，包含 34 项分支准备测试。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'`：3 项通过。
- 技能结构校验（6 个技能及发现入口）、quick_validate、Python compileall、Shell bash -n 与 git diff --check 通过。
- 按 review 技能审查相对初始基线的完整源码、测试和协议差异，核对复用身份、领先/分叉处理、复审、worktree 与回执，无未解决 finding；审查后复验 5 个变更技能文件的 SHA-256 未漂移。
- 回执核对中修正显式复用旧 fallback 分支的关联复用标记，并新增针对性用例，最终全套验证覆盖该修正。
- 所有 Git 操作测试使用临时本地仓库及 fake gh，未操作真实 PR。

## 完成条件

相关验证与 Review 通过，真实结果写入 history、计划归档并本地提交，工作树干净，未 push。
