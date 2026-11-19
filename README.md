---
title: "README"
created: 2026-11-18
tags:
  - "维度/科技"
  - "类型/参考"
  - "来源/项目"
---

# uLife-OS-infra — uLife OS Personal Agent OS Skill

> 把「个人智能体操作系统」从理念变成可安装、可审计、可复用的技能包。对齐《uLife OS：个人智能体操作系统（Personal Agent OS）实战指南》v2.1，基于 [Daniel Miessler 的 PAI 框架](https://github.com/danielmiessler/Personal_AI_Infrastructure)，结合 2026 年 MCP / A2A / Agent Skills / 上下文工程进展。

## 为什么需要它

普通 AI 聊天是无状态的：每次从零开始，不记得你是谁。这个 Skill 让 AI 助理拥有**身份契约 + 四层记忆 + 冷启动预算 + 协议层 + 人机接力护栏**，从"一次性工具"升级为"持续理解你的个人智能体操作系统"。

**v1.1 新增（对齐指南 v2.1）**：冷启动上下文预算表（T1/T2/T3）· 人机接力检查点 · Code-as-Glue 脚本编排 · 本地/云端异构算力路由 · Rework Rate 返工率观测。

## 安装

支持 Agent Skills 的客户端（Claude Code / Codex / Cursor 等）任选其一：

```bash
# 方式 A：skills CLI（如可用）
npx skills add zhubao315/ulife-os-infra

# 方式 B：手动
git clone https://github.com/zhubao315/ulife-os-infra.git
# 将目录放到你的 skills 路径，或让 Agent 读取 SKILL.md
```

零运行时依赖：核心只需要 Markdown；`scripts/` 为可选 Python 3 工具（仅标准库）。

## 5 分钟快速开始

1. 说："用 PAI Skill 帮我搭建个人 AI 基础设施。"
2. Agent 读 `SKILL.md` 并按 §4 工作流引导你填 `templates/telos/` 的十文件（每个 3–5 句起步）。
3. 运行审计：`python3 scripts/audit.py ./my-pai`（检查骨架是否合规）。
4. 需要时按 `references/` 深入各主题。

## 四种典型用法

| 你说 | Skill 做 |
|---|---|
| "让 AI 记住我 / 加载我的背景" | 生成/挂载 TELOS 身份契约 |
| "我的长任务总是丢上下文" | 应用长时程三件套（压缩/笔记/子Agent） |
| "把这个工作流封装成 Skill" | 按确定性优先链 + agentskills 规范生成能力包 |
| "审计我的 AI 基础设施" | 跑 `scripts/audit.py` + 成熟度自检 |

## 目录结构

```
ulife-os-infra/
├── SKILL.md              # 契约 + 触发语 + 工作流（主入口）
├── references/           # 六主题按需读（身份/记忆/技能/权限/钩子/协议/维护）
├── templates/            # TELOS 十文件 + 身份契约/钩子/权限/自检模板
├── scripts/              # audit.py（只读审计）· init_pai.py（初始化）
├── examples/             # 最小可用示例
├── LICENSE               # MIT
└── CHANGELOG.md          # 版本与迭代日志
```

## 设计原则

不要从工具开始，从自己开始 · 架构比模型重要 · 确定性优先 · 上下文是有限预算 · 协议化才能互操作 · 安全从第一天设计 · 允许说"不知道" · 从简单开始允许迭代。

## 许可

MIT — 见 [LICENSE](LICENSE)。欢迎 issue / PR；改进遵循 `references/maintenance.md` 的五步回路。
