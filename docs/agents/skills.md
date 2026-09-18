# Skill 源码与发现

宿主规则只表达本项目的验证、history、自动交付、发布和资产边界；Skill 自行维护通用
取证、Git 状态保护、执行、恢复和结果校验契约。

- `skills/` 是由本仓库直接维护、可审查并随 tag 发布的唯一公开 Skill 源码；`npx skills` 直接
  读取该目录，本仓库不发布 npm 包。
- `.agents/skills/<name>` 仅使用指向 `../../skills/<name>` 的相对目录链接提供本仓库发现入口；
  新增或删除公开 Skill 时同步维护链接。
- 仓库不维护专属 Skill；`SKILL.md` 只出现在 `skills/` 及其 `.agents/skills/` 发现链接中。
- 本仓库任务使用当前 checkout 的 Skill 源码；同名全局 Skill 并存时核对实际加载路径，运行时
  尚未刷新时重新启动 Agent。
- 不向本仓库复制自身 Skill，也不创建消费方 lock；下游的 lock、来源选择、内容哈希和本地例外
  属于消费方治理。
- 修改 Skill 行为、脚本、必需资源或依赖时，同步源码、相关测试和必要文档；验证范围以
  [`build-and-test.md`](build-and-test.md#本仓库验证) 为准。
- 发布 tag 不自动授权 GitHub Release、push 或用户全局安装；这些外部动作仍需明确要求。
