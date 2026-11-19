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

## 四种工作模式 + 统一 CLI（v2.0）

所有工具零第三方依赖（Python 3.10+ 标准库）。统一入口 `scripts/ulife.py`：

```bash
# Initialize（三档：starter / standard / advanced）
python3 scripts/ulife.py init --target ./my-ulife --profile starter [--dry-run]

# Audit（五层审计，JSON 或 Markdown）
python3 scripts/ulife.py audit --target ./my-ulife [--format json]
python3 scripts/ulife.py doctor --target ./my-ulife

# Integrate（发现现有资产，禁止未审计建平行系统）
python3 scripts/ulife.py integrate --target . [--discover]

# Evolve（观测 / 瓶颈 / 快照 / 回滚）
python3 scripts/ulife.py observe --target ./my-ulife --format md
python3 scripts/ulife.py evolve --action bottlenecks --target ./my-ulife
python3 scripts/ulife.py evolve --action snapshot --target ./my-ulife --backup ./bak

# 能力子命令
python3 scripts/ulife.py budget --window 200000 --system 4000 --tools 8000 --tier t2
python3 scripts/ulife.py route --task "复杂架构研究" --level PRIVATE
python3 scripts/ulife.py receipt --target ./my-ulife --action publish --result success --evidence <url>
python3 scripts/ulife.py memory-backup --target ./my-ulife --out backup.json
python3 scripts/ulife.py memory-restore --target ./my-ulife --backup backup.json
python3 scripts/ulife.py task --action new --objective "研究方案"
python3 scripts/ulife.py grant --target ./my-ulife --op write --file USER/identity/X.md --diff <hash> --approver <name>
```

> 旧入口 `scripts/init_pai.py` / `scripts/audit.py` 保留为兼容 shim，转发到新引擎。

## 目录结构（v2.0）

```
ulife-os-infra/
├── SKILL.md              # 契约 + 四工作模式 + 动态预算（主入口）
├── references/           # 10+ 主题按需读（身份/记忆/技能/权限/钩子/协议/维护/入职/路由/安全/运维/观测）
├── templates/            # TELOS 十文件 + starter/BOUNDARIES + 身份契约/钩子/权限/自检
├── scripts/              # ulife.py 统一 CLI + 8 个 engine（零依赖）
├── schemas/              # memory / receipt / task / policy 四份 JSON Schema
├── tests/ + .github/     # 34 项单元测试 + CI 工作流
├── examples/             # 可运行示例
├── AUDIT_REPORT.md · GAP_ANALYSIS.md · ARCHITECTURE_PROPOSAL.md · IMPLEMENTATION_PLAN.md
├── LICENSE · CHANGELOG.md · DISCOVERABILITY.md
```

## 设计原则

不要从工具开始，从自己开始 · 架构比模型重要 · 确定性优先 · 上下文是有限预算 · 协议化才能互操作 · 安全从第一天设计 · 允许说"不知道" · 从简单开始允许迭代。

## 许可

MIT — 见 [LICENSE](LICENSE)。欢迎 issue / PR；改进遵循 `references/maintenance.md` 的五步回路。
