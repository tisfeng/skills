# 为 README 目录添加文档链接

- 日期：2026-09-08
- 状态：completed
- 关联计划：none

## 目标

让 README 中的 Skill 和 Codex 子代理目录可以直接跳转到对应文档，并防止目录与源码发生漂移。

## 实际变更

- 将中英文 Skill 表格中的名称和配套 Skill 改为对应 `SKILL.md` 链接。
- 新增中英文 Codex 子代理表格，并链接到四个 TOML 配置。
- 精简安装章节的重复列表，让公共权限说明同时覆盖 Skills 与子代理。
- 扩展 Skill 和子代理校验器，检查 README 目录完整性及链接目标。

## 验证

已通过 Skill 与子代理目录校验、Python 编译检查、69 个 Python 单测、6 个 Node 安装器测试、Shell 语法检查、README 异常空白扫描和 `git diff --check`。

## 交付

本任务通过自动本地提交门禁交付；不执行 push、pull、rebase、merge 或发布。
