# Git Skill 组合解耦

- 状态：completed
- 授权：用户要求“继续，整理其他的技能，解耦”；沿用已确定的职责边界。
- 初始 HEAD：`276e16f57721fb8aa356ddb50d09f8e2a6b849cb`，分支 `main`。
- 初始 staged、unstaged、untracked、冲突均为空；本阶段采用自动本地交付。
- Planner 已完成三个 Git Skill 的增量规划；提交消息默认格式保留。

## 目标与范围

Git Skill 自行定位配套能力和兼容运行时，缺依赖时在相应 Git 写入前处理。组合调用依赖任务
语义，不依赖内部章节名。宿主以现有请求和项目政策表达授权，不需要提供同名内部变量。

允许修改：

- `skills/git-commit/SKILL.md`。
- `skills/worktree-rebase-merge/SKILL.md`。
- `skills/submit-pr/SKILL.md`、`skills/submit-pr/references/workflow.md`、
  `skills/submit-pr/scripts/submit_pr.py`、`skills/submit-pr/tests/test_submit_pr.py`。
- `tests/test_skill_portability.py`、`README.md`。
- 本计划和原任务 `docs/histories/2026-09/2026-09-11-decouple-skill-host-policies.md`。

`AGENTS.md`、`docs/agents/`、子代理配置、安装器、版本和消费方保持不变；不 push 或发布。
`review`、`code-simplifier` 检查后已有合理边界，不为凑齐改动而改写正文。

## 步骤与验证

1. 将提交、分支命名和已有提交回执定义为明确的组合任务，保留现有提交格式和安全检查。
2. worktree 在首次 Git 写入前定位 git-commit；submit-pr 仅在需要创建提交时要求此依赖。
3. 使用实际可用解释器，不要求消费者改变产品 Python 版本。
4. 评估并实现显式项目分支名的兼容路径：Git 名称有效且不受保护，保留默认命名与状态保护。
5. 扩展隔离消费者测试到全部公开 Skill 资源，执行三个 Git Skill 的相关单测与独立审查。
6. 使用模拟消费者验证缺依赖与只读模式；分别记录脚本测试、Agent 场景及真实外部验证边界。
7. 精确本地交付，并在同任务 history 追加本阶段结果。

## 风险与完成条件

放宽显式分支命名必须同时检查保护分支及冲突后缀；不能允许命名灵活性扩大 push 范围。
缺少自动提交的任务起点证据时，只限制自动路径，不补造基线或误伤显式 staged-only 提交。
固定宿主 Agent 文档，全阶段不修改；全部必要测试和 review 覆盖最终内容。

## 完成结果

三个 Git Skill 已按任务语义组合，依赖发现和缺失处理由 Skill 自行承担。submit-pr 使用现有
显式参数兼容项目分支名，保留默认命名、保护分支、冲突后缀和字面引用校验；无需新增配置。
本阶段没有修改 `AGENTS.md`、`docs/agents/` 或子代理配置。

相关单测 69 项通过：submit-pr 38、git-commit 19、worktree-rebase-merge 9、消费者测试 3。
消费者测试复制全部六个公开 Skill，覆盖资源引用闭包，以及无规则和短规则项目中的只读操作；
单独安装的 submit-pr 在缺少 git-commit 时仍可规划干净的已有提交。

独立 Planner 完成增量评估，并复用于三个只读消费者场景；场景前后 119 个文件哈希不变。
这些场景带有先前上下文，不是盲测，也没有进行真实 GitHub 操作。独立 reviewer 检查生产、
说明和最终测试；具体结果与验证边界记录在
[同任务 history](../../histories/2026-09/2026-09-11-decouple-skill-host-policies.md)。
