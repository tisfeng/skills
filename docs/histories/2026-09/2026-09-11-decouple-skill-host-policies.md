# Skill 与宿主规则解耦首轮

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
