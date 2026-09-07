# 安装 Codex 子代理

本仓库的 Skills 与 Codex 子代理独立安装、独立锁定版本，但共享同一个 Git tag。

## 安装 Skills

```bash
npx skills add 'tisfeng/skills#v0.2.0' --skill '*' --agent codex --yes
```

加入 `--global` 后，Skills 安装到 `~/.codex/skills/`；否则安装到当前项目的
`.agents/skills/`。

## 安装子代理

发布 npm 包后，使用：

```bash
# 当前项目
npx @tisfeng/codex-agents add 'tisfeng/skills#v0.2.0' --agent '*'

# 全局
npx @tisfeng/codex-agents add 'tisfeng/skills#v0.2.0' --agent '*' --global
```

项目安装写入 `.codex/agents/` 和 `.codex/agents-lock.json`；全局安装写入
`~/.codex/agents/` 和 `~/.codex/agents-lock.json`。Codex 会从这些目录发现独立 TOML 角色。

可用角色：`planner`、`reviewer`、`tester`、`git-delivery`。

```bash
# 只查看一个来源提供哪些角色
npx @tisfeng/codex-agents add tisfeng/skills --list

# 仅安装 planner 与 reviewer
npx @tisfeng/codex-agents add 'tisfeng/skills#v0.2.0' \
  --agent planner --agent reviewer
```

## 更新与冲突

```bash
npx @tisfeng/codex-agents update
npx @tisfeng/codex-agents update --global
```

更新只处理 lock 文件中记录的角色。若目标 TOML 与 lock 记录的哈希不同，安装器会拒绝覆盖，
以保护本地定制；确认替换后显式加入 `--force`。

安装器当前是仓库源码，尚未发布 npm 包；在发布前可从本仓库检验：

```bash
node bin/codex-agents.mjs add . --list
node bin/codex-agents.mjs add . --agent planner
```
