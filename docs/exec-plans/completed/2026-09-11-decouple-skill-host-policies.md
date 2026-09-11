# Skill 与宿主规则解耦

- 状态：completed
- 授权：用户在只读方案后明确要求“执行”；限本仓库首轮实施与默认本地交付。
- 初始 HEAD：`2502791495edf23f9bcbd50f06c6ea3912598c86`，分支 `main`。
- 初始 staged、unstaged、untracked 和冲突均为空；没有需要保留的初始任务 diff。
- 复用上一轮只读 Planner 结论，目标、源码及兼容假设未变化。

## 目标与范围

项目保留授权、自动提交、history、提交规范和验证要求；Skill 自己完成内部取证、校验与失败
处理。以 `review-pr` 为样板，升级内部实现不要求宿主 Agent 文档补规则。

允许修改及 Agent-owned 候选路径：

- `AGENTS.md`、`docs/agents/git-workflow.md`、`docs/agents/README.md`、
  `docs/agents/build-and-test.md`、`docs/design-docs/overview.md`、`README.md`。
- `skills/review-pr/SKILL.md`、`skills/review-pr/references/snapshot-protocol.md`、
  `skills/review-pr/scripts/review_snapshot.py`。
- `skills/review-pr/tests/test_review_snapshot.py`、`tests/test_skill_portability.py`。
- `.github/workflows/validate.yml`：将新增消费者测试接入现有验证任务。
- 本计划及同任务 `docs/histories/2026-09/2026-09-11-decouple-skill-host-policies.md`。

不修改 Scoco、全局安装、其他 worktree、安装器或版本号；不 push 或发布。
不改变既有提交格式、角色模型和权限，不引入宿主必填配置。

## 实施步骤

1. 精简本仓库 Git 规则，明确受影响文档与宿主政策边界。
2. 在所有并行采集结束后复验 PR 身份、head 和 base；统一 helper 与手动回退要求。
3. 明确 Skill 依赖发现和缺失处理；在隔离消费者中验证安装资产和 helper 行为。
4. 执行针对性检查与独立 review；完成计划、history 和精确本地提交。

## 验证与完成条件

- 并发读取结束后的 head/base/身份漂移及读取失败不能产生可接受快照或输出文件。
- `collect`、`refresh`、未变化压缩和文件传输都经过同一复验；正常字段与指纹保持兼容。
- 消费者测试不复制源码仓库治理，固定宿主文档并验证 helper 运行及安装资源边界。
- 运行相关 Python 单测、Skill/agent 校验、Python 编译、Markdown 链接及 diff 检查。
- 以独立 Agent 场景检查自然语言规则的实际遵守情况，分别报告脚本测试和 Agent 验证。
- 必要检查和 review 覆盖最终快照；按 Git Skill 精确暂存本任务内容并本地提交。

## 风险

远程 API 多次读取不是原子快照；最后复验只能证明采集期间观测到的身份一致，不能保证之后
不再变化。最终报告仍保留快照边界。无真实远程 PR 操作时，不把模拟 API 测试写成线上验证。

## 完成结果

职责清理、最终身份复验、消费者隔离测试及 CI 接入已完成。独立 reviewer 的 history 例外歧义
和临时目录清理后断言两项反馈均已处理，增量复核无未解决 finding。具体检查与验证边界见
[同任务 history](../../histories/2026-09/2026-09-11-decouple-skill-host-policies.md)。

本轮保留既有 Git Skill 格式和角色配置；仅在本仓库精确本地交付，不发布或升级消费方。
