# README 安装说明与中文默认页

- 日期：2026-09-08
- 状态：completed
- 关联计划：none

## 目标

将根 README 设为中文默认页，并简化 Skills 与 Codex 子代理的安装说明。

## 实际变更

- 将中文内容置于根 `README.md`，并将英文版迁移为 `README.en.md`。
- 将 Skills 和子代理安装命令合并到单一安装模块，按项目和全局范围组织。
- 保留 Skills 命令的 `--yes`，并将 README 改为只呈现用户需要的安装与本地定制信息。
- 删除重复且过时的 `docs/agent-installation.md`，移除固定 Git tag 和开发与验证章节；更新 README
  校验脚本的英文文件名。

## 验证

运行 `python3 scripts/validate-skills.py`、`python3 -m compileall -q scripts/validate-skills.py` 和
`git diff --check`。

## 交付

本任务未创建提交、推送、发布或修改用户全局 Codex 配置。
