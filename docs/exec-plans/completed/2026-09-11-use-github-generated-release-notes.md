# 使用 GitHub 默认生成的 Release 说明

- 状态：completed
- 创建日期：2026-09-11
- 负责人：Codex
- 关联 Issue/PR：none

## 任务摘要

- 意图模式：implementation
- 交付授权：push；用户明确执行已审定方案，包含将后续发布行为推送到 `origin/main`，以及原地更新
  `tisfeng/skills` 既有 GitHub Release 元数据。
- 目标结果：后续 Release 标题精确为 tag、正文由 GitHub 默认生成；已发布的七个 Release 已同步为该格式。
- 仓库修改路径：`.agents/skills/release/SKILL.md`、`.github/workflows/publish.yml`、`docs/release/`、
  `docs/agents/README.md`、本计划及同任务 history。
- 外部更新目标：`tisfeng/skills` 的既有 Releases `v0.1.0`、`v0.2.0`、`v0.3.0`、`v0.3.1`、
  `v0.3.2`、`v0.3.3` 和 `v0.3.4`。
- 持续限制：未创建或移动 tag，未发布 npm 包，未删除或重建 Release，未修改 Release assets、状态或 target。

## 写入前状态

- 初始 HEAD：`6112dc9a6e267a9c4598a807adf4a543d6506457`
- 初始 staged、unstaged、untracked、冲突：none
- 初始远程 Release：均为非 draft、非 prerelease、target 为 `main`、assets 为 0；其中
  `v0.3.2`、`v0.3.3` 和 `v0.3.4` 标题带有 `Skills ` 前缀，且正文为手写 Markdown。

## 实施结果

1. 删除 tag workflow 对 `docs/release/changelog/X.Y.Z.md` 的前置校验，创建 Release 时显式使用
   `--title "$RELEASE_TAG" --generate-notes`。
2. 更新项目 release Skill 和发布文档：新版本不再要求手写发布日志，既有 Markdown 文件保留为历史归档。
3. 提交并 push `86a80bb30080c93440dc60b1629b1e4e4c339395`；普通 CI
   [`34504098200`](https://github.com/tisfeng/skills/actions/runs/34504098200) 通过。
4. 使用 GitHub Release Notes API 为每个 tag 生成默认正文，并按实际 Release ID 原地 PATCH 标题和正文。
   `v0.1.0` 使用首个 tag 的 commits 链接；后续版本显式指定前一 tag；`v0.3.4` 保留 GitHub 生成的
   PR #1 与贡献者段落。

## 验证

- 本地通过 `git diff --check`、`python3.12 scripts/validate-skills.py`、9 项
  `test_validate_skills.py` 测试、YAML 解析与现行相对链接检查。
- 远程回读确认七个 Release 的 `name == tag_name`，并确认其正文字段等于各自 GitHub 生成结果。
  Release IDs、tag、assets（0）、draft（false）、prerelease（false）及 target（`main`）保持不变。

## 完成条件

- [x] 后续发布行为已推送并通过普通 CI。
- [x] 所有既有 Release 均已原地更新且远程字段核验通过。
- [x] 计划已归档，history 已记录真实命令、证据和边界。
