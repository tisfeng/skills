# Skill 与宿主规则解耦

## 结果

本仓库将项目政策与 Skill 内部步骤分开：自动本地提交、Angular-style、history、允许范围和
验证要求保留在宿主规则；暂存算法、工具调用节奏、结果校验和回执由对应 Skill 执行。显式
staged-only 交付不因此新增 history 要求。内部 Skill 修复不再默认要求修改宿主 Agent 文档。

`review-pr` 在全部并行 context、threads 和 checks 采集完成后，独立复验 PR 编号、URL、head、
base 名称和 SHA。缺字段、读取失败或漂移均拒绝本轮证据，发生在指纹生成及文件保存之前；
`collect`、`refresh`、未变化压缩和文件传输共用此路径。手动回退同步覆盖完整身份，保留既有
查询范围、授权、CLI 参数和指纹语义。

配套 `review` 优先从实际 Skill 清单发现，同级路径是回退位置；缺失时允许有限只读取证并报告
审查能力不足，不要求宿主增加补救规则。新增消费者测试复制实际 `review-pr` 和 `review`
资产，不复制本仓库治理，并已接入现有验证 CI。

## 验证

| 检查 | 实际结果 |
| --- | --- |
| `python3.12 -m unittest discover -s skills/review-pr/tests -p 'test_*.py'` | 93 项通过；其后仅调整一项断言作用域，再跑 snapshot 子集 29 项通过 |
| `python3.12 -m unittest discover -s skills/review/tests -p 'test_*.py'` | 10 项通过 |
| `python3.12 -m unittest discover -s tests -p 'test_validate_skills.py'` | 9 项通过 |
| `python3.12 -m unittest discover -s tests -p 'test_skill_portability.py'` | 2 项通过，包含多个消费者与失败子场景 |
| Skill/agent 结构校验、Python 编译、Markdown 链接及 diff 检查 | 通过 |
| 验证工作流 YAML 解析 | Ruby YAML 解析通过；当前 Python 缺少 PyYAML，未新增依赖 |

事件同步测试证明最终身份读取晚于三项并行 collector 完成；五字段分别漂移或缺失，以及末尾
读取失败，都有拒绝断言。失败不写文件的断言在临时目录清理前执行。隔离 helper 子进程检查
正常采集、未变化刷新、失败不落盘、Markdown 相对引用闭包、无宿主治理目录，以及固定 AGENTS
原文、Git index、refs 和状态不变。

两个独立 Agent 消费者场景分别具备和缺少配套 `review`：均执行本地模拟 API 的 collect 与
refresh，缺依赖时明确限制，不将空 checks 当作绿色 CI；全部 39 个 fixture 文件哈希不变。
因子代理数量限制复用了已有 Planner，带有规划上下文，不是盲测。fixture 没有真实 checkout、
源码或 diff，模拟 `gh` 不支持认证和 diff 查询，因此没有证明完整代码审查或真实 GitHub 行为。

## 审查与交付边界

复用已有独立 Planner 结论；独立 reviewer 检查生产、文档和新增测试。审查发现的显式提交
history 歧义与临时目录清理后断言均已修正。

仅修改本仓库源码、文档、测试和验证 CI。未修改 Scoco、全局安装、其他 worktree、安装器或
版本号，未 push、发布或操作真实 PR。其他 Git Skill 的全面通用化属于后续阶段。

执行过程见 [完成计划](../../exec-plans/completed/2026-09-11-decouple-skill-host-policies.md)。

## 第二阶段：Git Skill 组合解耦

用户继续要求“整理其他的技能，解耦”。本阶段从 `main` 的
`276e16f57721fb8aa356ddb50d09f8e2a6b849cb` 开始，初始索引、工作树及未跟踪内容均为空。
复用原任务 history；新增的
[完成计划](../../exec-plans/completed/2026-09-11-decouple-git-skill-composition.md)
记录本阶段范围。宿主 `AGENTS.md`、`docs/agents/` 与子代理配置保持不变。

`git-commit` 明确区分预览、创建提交、只推导分支名和汇报已有提交。调用方传入任务及已有
证据，不需要了解内部章节或提供同名变量；缺少真实任务起点只限制自动提交，不补造基线，
也不阻止已有授权的 staged-only 提交。已有提交回执不触发新提交或反向校验旧消息格式。

`worktree-rebase-merge` 自行发现 git-commit，在首次 Git 写入前确认完整交付能力；缺失时
仍可只读预检。`submit-pr` 仅在需要创建提交时要求该依赖，干净的已有提交可独立规划；工具
解释器独立于产品 Python 版本选择。组合调用不再依赖其他 Skill 内部章节名。

submit-pr 的现有 `--head-branch` 参数接受项目明确指定的 Git 合法字面分支名，例如
`codex/foo`、`feature/bar`；同名当前分支直接复用。默认 Conventional 命名、当前默认任务
分支不接受不同名称、保护分支与冲突后缀保护继续生效。拒绝 `@{-1}` 等展开式引用。
`review` 和 `code-simplifier` 检查后无需改写正文，二者纳入全部六个公开 Skill 的资源闭包验证。

### 第二阶段验证

| 检查 | 实际结果 |
| --- | --- |
| `python3.12 -m unittest skills/submit-pr/tests/test_submit_pr.py` | 38 项通过 |
| `python3.12 -m unittest discover -s skills/git-commit/tests -p 'test_*.py'` | 19 项通过 |
| `python3.12 -m unittest discover -s skills/worktree-rebase-merge/tests -p 'test_*.py'` | 9 项通过 |
| `python3.12 -m unittest discover -s tests -p test_skill_portability.py` | 3 项通过 |
| Skill 结构校验、Python 编译与 diff 检查 | 通过 |

69 项测试包含显式项目分支的只读 plan、同名分支 apply、保护后缀跳过、非法名称、真实前次
checkout 下可被 Git 展开的 `@{-1}` 拒绝，以及缺少显式参数时保留原有拒绝行为。apply 使用
临时本地 remote 与模拟 gh，证明本地分支不切换、不强制改写其他本地 ref，远端收到精确 HEAD；
这不是实际 GitHub 验证。

消费者测试将六个 Skill 复制到独立目录，不带本仓库治理。无 AGENTS 的项目中运行提交消息
校验、统计、worktree 事实采集和单独安装的 submit-pr plan；后者相邻没有 git-commit。随后
添加简短 AGENTS 再运行 plan，分别验证 index、refs、status 和规则原文不变，未生成宿主 docs。

复用 Planner 执行三个独立只读消费者场景：只命名/汇报已有提交且保留 staged 内容、缺少
git-commit 的 worktree 预检，以及缺少 git-commit 且需要提交的 submit-pr。119 个 fixture
文件前后哈希完全一致；未写宿主规则或 Git 状态。Planner 带有先前规划上下文，不是盲测。
最后一个场景缺少 remote/base 且项目禁止 push，仅验证只读检查与缺口报告，没有完成 plan/apply。

独立 reviewer 对生产脚本、Skill 说明和冻结后的新增测试完成两轮审查，无发现。消费者测试
证明 helper 的独立运行与不写入边界，不代表实际 Agent 已理解所有项目政策。

第二阶段同样未修改 Scoco、全局安装、安装器或版本号，未 push、发布或操作真实 PR。
