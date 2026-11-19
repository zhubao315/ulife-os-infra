---
title: "ARCHITECTURE_PROPOSAL — Skill 控制面 / Runtime 执行面 / USER 资产面"
created: 2026-11-19
tags: ["维度/科技", "类型/框架", "来源/项目"]
---

# 架构提议

## 三面分离（核心原则）

- **Skill（控制面）**：本仓库——描述标准、生成配置、提供验证工具。零运行时依赖。
- **Runtime（执行面）**：Claude Code / Codex / Cursor / 自研 Agent——实际执行任务。
- **USER（资产面）**：TELOS / Preferences / Memory / Workflows——用户拥有，写保护。

**不在本仓库内实现**完整记忆数据库、MCP 网关、多 Agent 服务器——只给 Schema、模板、验证器与适配器。

## 目标结构（v1.2 落地部分）

```
ulife-os-infra/
├── SKILL.md              # 规范 frontmatter + 四工作模式
├── scripts/ulife.py      # 统一 CLI：init / audit / doctor / export / backup
├── scripts/audit_engine.py # 五层审计（可独立调用）
├── scripts/init_engine.py  # canonical 模板初始化
├── scripts/policy_engine.py# 一次性授权凭据
├── schemas/              # memory / receipt / task / policy JSON Schema
├── templates/starter/    # Starter 五文件（默认档）
├── tests/ + .github/workflows/ci.yml
└── references/ · templates/ · examples/  # 保留现有有效资产
```

## 五层审计语义

L1 Structure → L2 Content → L3 Security → L4 Operational → L5 Value。
不能检查的项标 `NOT CHECKED`，不默认通过。
