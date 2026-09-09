# 统一技能边界并精简重复规则

- 日期：2026-09-10
- 状态：completed
- 关联计划：[执行计划](../../exec-plans/completed/2026-09-10-align-skill-workflows.md)

## 目标与变更

用户批准上一轮技能审查方案，并明确同意改进 PR 刷新终点、移除纯措辞暂存测试。

- `git-commit` 先判断模式与授权；纯预览可以读取未暂存候选而不写 Git。完整可见预览由该 Skill
  统一定义；从仓库根目录暂存，用户相对路径仍按原调用目录解释。
- `submit-pr` 在实际交付的最终 plan 前完成获准的 staged 提交和精确 base fetch；纯 plan 缺少
  提交或缓存时只说明限制，不写入。保留要求 HEAD 包含 base 的现有约束。
- 宿主明确 PR review 的有限 Git 准备权限，不扩展为自动交付、产品修复、resolve 或 push。
- 合并 Git、review-pr、submit-pr 和 code-simplifier 的重复说明；PR 刷新以完整已检查快照为边界。
- 内部 release 保留请求语义，步骤与失败恢复集中到发布文档；创建发布提交后再冻结其 SHA。
- 删除只检查关键词/措辞的暂存测试及两份 CI 调用；保留有实际脚本行为覆盖的测试。
- 通用 review、三个子代理配置，以及双语消息契约到完整回执的整个区块均保持不变。

## 验证

- 6 个公开 Skill、3 个子代理结构校验通过；修改的 6 个 Skill（含内部 release）通过
  `quick_validate.py`，相关相对链接和锚点有效。
- Git 提交 19 项、PR review 27 项、PR 提交 23 项测试通过，共 69 项；Python 编译、两份 YAML
  解析与 `git diff --check` 通过。
- 独立场景检查：从临时项目子目录请求仅预览，产出完整双语草稿；逐文件摘要确认全部工作文件和
  Git 元数据未变。另在该临时项目验证根目录一次暂存覆盖全部候选，相对文件路径含义正确。
- 使用现有临时仓库及模拟 GitHub fixture 验证：只有 staged 修改或缺少 cached base 时，纯 plan
  报告前提缺失；按获准提交、精确 fetch、plan 的顺序可以生成新提交的 PR 预览。
- 复用已完成的独立规划；独立只读审查及增量复核无待修复问题。

## 交付边界

按 auto-local-commit 由当前主 Agent 精确暂存并本地交付。本任务没有操作真实 PR、push、发布或
下游安装。临时场景证明所测试路径的行为，不代表所有自然语言请求或真实远程状态均已验证。
