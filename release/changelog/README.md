# GitHub Release 说明

新版本不创建手写 Markdown 发布日志。tag workflow 使用 GitHub CLI 的
`--title "$RELEASE_TAG" --generate-notes` 创建 Release：标题精确为 `vX.Y.Z`，正文由 GitHub
根据该 tag 与上一个 Release 自动生成。

本目录中的既有 `X.Y.Z.md` 文件是历史归档；它们不再是发布前置条件，也不会再被复制到 GitHub
Release 正文。不要为未发布或新发布版本新增该类文件。
