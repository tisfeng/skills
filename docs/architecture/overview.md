# 架构概览

本仓库发布两种互补的 Agent 资产：

```text
用户请求
  └─ AGENTS.md 路由
      ├─ skills/<name>/SKILL.md：按需调用的工作流说明
      └─ .codex/agents/<name>.toml：可委派的专用子代理
```

`skills/` 是 `npx skills add` 识别的 Skill 源码。`.codex/agents/` 是 Codex 原生发现的
项目级子代理配置。两者共用仓库 tag，但安装、锁文件和升级逻辑各自独立。

`bin/codex-agents.mjs` 提供 agent installer：它从指定源码读取 `.codex/agents/*.toml`，在
项目级写入 `.codex/agents/`，或在全局级写入 `~/.codex/agents/`。安装器绝不覆盖同名且被
本地修改的角色，除非用户明确使用覆盖选项。
