# 优化发布流水线速度

- 日期：2026-09-20
- 状态：completed
- 关联计划：[`2026-09-20-optimize-release-pipeline.md`](../../exec-plans/completed/2026-09/2026-09-20-optimize-release-pipeline.md)

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `Unknown`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 目标

减少发布 tag 的重复验证，并让纯执行计划/history 提交不再触发完整 Skill 测试。

## 实际变更

- `release.yml` 新增同一 SHA 的成功 `main` `Validate Skills` 查询；匹配时跳过 tag 的重复完整验证，查询失败或无匹配时保留完整验证 fallback。
- `validate.yml` 忽略纯 `docs/exec-plans/**` 与 `docs/histories/**` 的 push/PR 触发。
- 新增 `docs.yml`，对纯计划/history 变更执行 whitespace、旧发布入口和文件名检查；代码、Skill、脚本、workflow 或其他运行时变更仍走完整验证。
- `release/README.md` 补充复用条件、fallback 和性能边界。

## 验证

- 三个 workflow YAML 使用 PyYAML 解析通过。
- 真实 GitHub API 查询确认可按 SHA 找到成功的 `Validate Skills` main run `35454668707`。
- 计划/history 文件名规则、旧 `docs/release` 路径检查和 `git diff --check` 通过。
- 最终只读 review 未发现有效 finding。
- 未执行 push、tag、Release 修改或远程 workflow 运行；本提交仅本地交付。

## 交付

创建本地 Angular-style 提交，不 push。
