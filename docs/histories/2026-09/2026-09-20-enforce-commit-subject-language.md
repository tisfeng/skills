# 强制校验双语提交标题语言

- 日期：2026-09-20
- 状态：completed
- 关联计划：[`docs/exec-plans/completed/2026-09/2026-09-20-enforce-commit-subject-language.md`](../../exec-plans/completed/2026-09/2026-09-20-enforce-commit-subject-language.md)

## 执行上下文

- **Agent Name:** Unknown
- **Model:** Unknown
- **Environment:** `macOS 27.0 / Xcode 27.0 (27A266a)`

## 目标

明确 `git-commit` 双语消息的 subject 语言顺序，并阻止中文正文区块继续使用英文 subject。

## 实际变更

- 规定中文任务先使用中文 subject，再提供英文镜像 subject；禁止两个区块复用同一个英文标题。
- 校验器根据中文正文标签要求本地 subject 包含汉字，并要求英文 subject 包含 ASCII 字母、不得包含汉字且与本地 subject 不同。
- 保留其他非英语本地标题与英文镜像的既有兼容性。

## 验证

- `python3.12 -m unittest discover -s skills/git-commit/tests -v`：19/19 通过。
- `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py' -v`：2/2 通过。
- `python3.12 scripts/validate-skills.py`：通过，验证 6 个 Skills 及发现入口。
- `python3.12 -m compileall -q scripts skills`：通过。
- `quick_validate.py skills/git-commit`：临时 Python 3.12 环境安装 PyYAML 后通过。
- 临时消息样例：两个英文 subject、不同措辞的英文本地 subject、含汉字的英文 subject 均被拒绝；正确中英双语及法英双语消息通过。
- `git diff --check`：通过。
- Review：未发现 finding；未发布 tag、未 push、未同步下游固定版本快照。

## 交付

- 在 `skills` 权威仓库创建本地提交；Easydict 继续使用 `v0.6.2`，待后续正式发布新版本后再按安装器同步。
