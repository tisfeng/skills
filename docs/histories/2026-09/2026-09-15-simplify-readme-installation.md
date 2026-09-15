# 简化 README 安装说明

- 日期：2026-09-15
- 状态：completed
- 关联计划：none

## 目标

使用一组无版本安装命令同时覆盖安装与更新，删除重复说明。

## 实际变更

- 中英文 README 明确安装命令可重复执行并获取默认分支的最新内容。
- 删除独立更新章节，保留项目和全局安装命令。
- 将全局 Skill 和 lock 路径修正为 `~/.agents/` 下的实际位置。

## 验证

- `python3.12 scripts/validate-skills.py`
- `git diff --check`

## 交付

与 README 变更一起创建本地提交；未 push、发布或修改全局 Skill。
