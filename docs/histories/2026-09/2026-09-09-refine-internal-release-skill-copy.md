# 精简内部发布 Skill 的入口文案

- 日期：2026-09-09
- 状态：completed

## 目标

让项目内部 `release` Skill 先说明版本发布职责，不在操作入口重复目录归属或公开性分类。

## 变更

- 将 frontmatter 描述改为本仓库版本的发布、预检与续办。
- 将开头改为覆盖版本号、发布日志、Git tag、npm 包和 GitHub Release 的职责说明。
- 保留发布步骤、权限边界、失败续办、workflow 和目录结构不变。

## 验证

- 对内部 Skill 运行 `skill-creator` 的快速校验；如环境缺少其依赖，则使用仓库无依赖结构与链接校验器。
- 运行公开 Skill 校验和 `git diff --check`；未运行 npm 发布、GitHub Actions 或外部安装。

## 交付

- 本任务仅调整项目内部 Skill 的文案；未修改版本、创建 tag、push、发布 npm 或创建 GitHub Release。
