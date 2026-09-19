# 优化发布流水线速度

- 状态：completed
- 创建日期：2026-09-20
- 负责人：Codex
- 关联 Issue/PR：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `Unknown`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 背景

`v0.6.2` 发布过程中，本地端到端操作约 25 分钟；GitHub Actions 实际执行约 30–40 秒，主要浪费来自
同一发布提交在 `main` push 和 tag push 上重复执行完整验证，以及发布记录提交再次触发完整验证。

## 目标与范围

- 目标结果：减少发布 tag 的重复验证，并让纯执行计划/history 提交只执行轻量文档检查。
- 允许修改路径：`.github/workflows/`、`release/README.md`、本计划、同任务 history。
- 同任务 history：`docs/histories/2026-09/2026-09-20-optimize-release-pipeline.md`
- 用户限制：不削弱首次代码变更的完整验证；不修改公开 Release、tag 或远程仓库；不新增第三方依赖。
- 非目标：不拆分测试矩阵、不重构现有 Skill 测试、不引入本地发布 CLI。
- 验收标准：tag workflow 能复用同一 SHA 的成功 main 验证；无成功结果时仍回退完整验证；纯计划/history 提交触发轻量文档检查而跳过完整验证；workflow YAML 和文档链接通过静态检查。

## 工作计划

1. 增加 tag 对同一 SHA 成功 main 验证的查询与复用门禁。
2. 增加计划/history 纯文档变更的轻量检查 workflow，并让完整验证忽略该范围。
3. 更新发布文档，说明复用条件、fallback 和文档检查边界。
4. 运行 YAML、Shell、文档和相关 workflow 静态检查，审查最终 diff。
5. 回填 history、归档计划并创建本地提交，不 push。

## 风险与决策

- 只有 workflow、事件、分支、SHA、状态和 conclusion 全部匹配时才复用 main 验证；API 查询失败或结果不明确时回退完整验证。
- `workflow_call` 仍保留完整验证能力，避免 tag 在 main CI 尚未完成时失去门禁。
- 轻量检查只覆盖 `docs/exec-plans/**` 和 `docs/histories/**`；任何代码、Skill、脚本、workflow 或发布规则变更仍触发完整验证。

## 进度

- [x] 完成 v0.6.2 时间线诊断，确认主要重复验证点。
- [x] 完成 workflow 和发布文档修改。
- [x] 完成静态验证与 review。
- [x] 回填 history、归档计划并创建本地提交。

## 验证

- 已确认 v0.6.2 的 main 验证约 33 秒、tag 验证约 28 秒、Release job 约 5 秒。
- 已确认当前工作树干净，最新公开 tag 为 `v0.6.2`。
- 三个 workflow YAML 使用 PyYAML 解析通过。
- 真实 GitHub API 查询确认可按 SHA 找到成功的 `Validate Skills` main run `35454668707`。
- 计划/history 文件名规则、旧 `docs/release` 路径检查和 `git diff --check` 通过。
- 最终只读 review 未发现有效 finding。

## 完成条件

- [x] tag 复用和完整验证 fallback 的 workflow 逻辑通过检查。
- [x] 纯计划/history 提交的轻量检查路径明确且不掩盖代码变更。
- [x] 计划与 history 已归档，创建本地提交且未 push。
