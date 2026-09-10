# 改用 GitHub 默认生成的 Release 说明

- 日期：2026-09-11
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09-11-use-github-generated-release-notes.md`](../../exec-plans/completed/2026-09-11-use-github-generated-release-notes.md)

## 目标

让后续 GitHub Release 标题精确使用 tag、正文使用 GitHub 默认生成的 Release Notes，并同步修正所有既有 Release。

## 实际变更

- release Skill、发布流程和 tag workflow 改为使用精确 tag 标题与 GitHub 默认生成 Release Notes；
  workflow 不再校验或读取手写 changelog。
- 既有 `docs/release/changelog/X.Y.Z.md` 保留为历史归档，新发布不再创建该类文件。
- 原地更新 `v0.1.0` 至 `v0.3.4` 共七个 GitHub Release。所有标题现在均等于 tag；正文来自 GitHub
  Release Notes API，`v0.3.4` 包含该 API 生成的 PR #1 和贡献者段落。

## 验证

- `git diff --check`、Skill 结构校验、9 项相关单测、YAML 解析和相对链接检查均通过。
- 提交 `86a80bb30080c93440dc60b1629b1e4e4c339395` 已推送；普通 CI
  [`34504098200`](https://github.com/tisfeng/skills/actions/runs/34504098200) 通过。
- 远程回读确认七个 Release 的 ID、tag、assets（0）、draft（false）、prerelease（false）和
  target（`main`）未变，标题与 tag 相等，正文为对应范围的 GitHub 生成内容。

## 交付

- 未创建或移动 tag，未发布 npm 包，未删除或重建 Release。
