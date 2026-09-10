# 公开技能通过项目入口自用

## 结果

- 六个公开技能新增 `.agents/skills/<name> -> ../../skills/<name>` 相对目录链接，源码仍维护在
  `skills/`，内部 `release` 实目录保持原样。
- 治理与设计文档明确项目发现入口、公开源码和内部技能的职责；本仓库任务需核对实际加载的
  源码路径，避免误用同名全局副本。
- 技能校验器检查链接完整性、精确相对目标、断链、旧链接及内部技能结构，并要求保留
  `release` 实目录。

## 验证

- 独立 tester 编写并执行 `python3.12 -m unittest discover -s tests -p 'test_validate_skills.py'`：
  九项通过，覆盖正常入口、缺失、复制、错误目标、断链、旧链接及内部技能保护。
- `python3.12 scripts/validate-skills.py`：六个公开技能及项目发现入口通过。
- `python3.12 scripts/validate-agents.py`：三个 agent 通过。
- `PYTHONPYCACHEPREFIX=<临时缓存目录> python3.12 -m compileall -q scripts skills`：通过。
- tester 另运行 `python3.12 -m compileall -q scripts skills tests`，覆盖新增测试文件：通过。
- `git diff --check`、变更文档的本地链接和新增锚点：通过。
- Codex Desktop 0.136.0 的独立 `app-server --stdio`，使用临时 `CODEX_HOME`，依次调用
  `initialize` 与 `skills/list`（当前仓库 cwd，`forceReload: true`）：返回七个启用的 `repo`
  技能，六个公开技能的路径解析到当前 worktree 的 `skills/`，`release` 指向原实目录。

运行时证据覆盖 Codex 的本地技能发现接口；没有重启当前桌面会话，也未验证其技能选择器缓存或
模型对全局同名技能的选择结果。未修改全局配置、执行发布或推送。

## 关联

- [执行计划](../../exec-plans/completed/2026-09-10-enable-local-skill-discovery.md)
