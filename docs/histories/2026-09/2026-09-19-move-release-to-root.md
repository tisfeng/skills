# 将发布目录移至仓库根目录

- 日期：2026-09-19
- 状态：completed
- 关联计划：none

## 执行上下文

- **Agent Name:** `Codex`
- **Model:** `Unknown`
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 目标

将仓库维护用的发布流程从 `docs/release/` 提升到根目录，同时保留 `changelog/` 作为发布说明归档。

## 实际变更

- 将 `docs/release/` 移动为根目录 `release/`。
- 将入口从 `release/workflow.md` 重命名为 `release/README.md`。
- 保留 `release/changelog/` 及其既有历史版本文件。
- 更新 `AGENTS.md` 的现行发布流程链接。
- 不改写已完成的 `docs/histories/` 与 `docs/exec-plans/completed/` 中的历史路径事实。

## 验证

- 检查现行文档中的旧 `docs/release/` 引用已清除。
- `git diff --check` 通过。
- 仓库 Skill 校验通过。

## 交付

- 创建本地提交；未 push、未创建 tag 或 GitHub Release。
