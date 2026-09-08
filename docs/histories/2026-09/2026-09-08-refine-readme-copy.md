# 优化 README 文案

- 日期：2026-09-08
- 状态：completed
- 关联计划：none

## 目标

改善中英文 README 的项目定位、权限边界、安装说明和排版，并说明本仓库与 Easydict Agent 开发流程的关系。

## 实际变更

- 重写项目简介，同时覆盖 Agent Skills 和 Codex 子代理配置。
- 说明本仓库是 Easydict Agent 开发流程的一部分，Easydict 使用这里发布的 Skills 和子代理。
- 将远程操作边界改为以用户明确授权和工作流条件为准，补充发布操作。
- 统一中英文术语、安装器要求、lock 文件用途与本地修改保护说明。
- 移除中文段落中的硬换行，避免 Markdown 渲染出中文词语间的异常空格。

## 验证

已通过 `python3 scripts/validate-skills.py`、`python3 -m compileall -q scripts/validate-skills.py`、README 异常空白扫描和 `git diff --check`。

## 交付

本任务通过自动本地提交门禁交付；不执行 push、pull、rebase、merge 或发布。
