# GitHub Release 说明

每个发布版本必须有 `release/changelog/X.Y.Z.md`，文件名不带 `v`。该文件是 GitHub Release
正文的唯一来源，发布前随发布提交进入 tag，workflow 使用 `--notes-file` 原样读取。

## 内容规范

- 使用 `## 更新内容` 开头，以中文简述版本变化，通常 2～5 条；小版本可以只有一条。
- 根据上一版本到本版本的完整差异归纳新增、修复与重要行为变化，说明用户能感知的结果。
- 不兼容变更必须说明影响和必要操作；不复制提交清单、CI 日志或 plan/history。
- 末尾保留 `Full Changelog`，链接到上一版本与当前版本的比较页。
- 不在正文重复版本标题；GitHub Release 标题固定为 `vX.Y.Z`。

```markdown
## 更新内容

- 改进某项能力，说明用户能感知的变化。
- 修复某个问题，说明修复后的行为。

**Full Changelog**: https://github.com/tisfeng/skills/compare/v上一版本...v当前版本
```

## 校验与历史补录

workflow 从 tag checkout 校验目标版本日志，拒绝缺失文件、空白正文或没有实际更新条目的日志，
并核对比较链接指向当前 tag。创建后和重跑时均比对 Release 标题及全文，仅统一 CRLF/LF 和
末尾换行；不一致就失败，不回退自动生成或静默覆盖。

既有历史文件保留原貌。`0.6.2.md` 从现有 Release 正文补录；`0.6.3.md` 和 `0.7.0.md` 根据各自
版本范围补录。补录不代表线上正文已同步，也不意味着旧 tag 已包含这些文件。
发布授权、恢复与线上回填边界见 [发布流程](../README.md)。
