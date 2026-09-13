# 精简低价值测试

- 日期：2026-09-13
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-13-prune-low-value-tests.md)

## 目标

逐组检查现有 Skill 测试是否真正执行被测逻辑、保护可观察行为或高风险安全边界，删除无效、
重复和实现细节测试，以更小的套件保留有明确回归价值的证据。

## 实际变更

- 删除 `test_skill_trigger_cases.py` 与自校验 JSON fixture。旧测试没有调用 selector 或模型，
  request 内容即使失真也不会失败，因此不能证明 Skill description 的触发质量。
- 将测试方法从 183 个精简为 88 个，测试代码从 5,630 行降为 3,897 行；连同触发 fixture，
  共移除 1,814 行旧测试材料。
- 各 Skill 只保留代表性成功路径，以及 Git 状态保护、PR/分支/thread 身份、证据漂移、分页
  完整性、远程 mutation 前门禁与写入后复核等高后果失败边界。
- 删除重复输入排列、内部调用次数、诊断措辞、源码文本搜索和已被端到端路径覆盖的低价值案例，
  并清理因此产生的未使用 import。
- 新增 `tests/README.md`，把可观察行为、高风险边界和消费者可移植性确立为保留标准，并明确
  静态语料不能替代真实 selector/model 评测。

## 验证

- `python3.12 scripts/validate-skills.py`：通过，验证 6 个 Skill 及项目发现入口。
- Python 单测：`git-commit` 13 项、`review` 7 项、`worktree-rebase-merge` 6 项、`review-pr`
  45 项、`submit-pr` 15 项、可移植性 2 项，共 88 项全部通过。
- `python3.12 -m compileall -q scripts skills tests`：通过。
- `git diff --check`：通过。
- 未运行真实模型/selector 触发评测；本次不再用静态结构检查冒充该能力的验证结果。

## 交付

本任务按 `auto-local-commit` 精确本地提交；未执行 push、fetch、pull、rebase、merge、发布、
真实 GitHub 写入或下游安装。
