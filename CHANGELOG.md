---
title: "CHANGELOG"
created: 2026-11-18
tags:
  - "维度/科技"
  - "类型/参考"
  - "来源/项目"
---

# Changelog

## 1.1.1 — 2026-11-19

命名简化定稿：技能技术名 `ulife-os-infra`（规范合规小写）、展示名 `uLife-OS-infra`，目录 / name / 仓库 URL 同步。

## 1.1.0 — 2026-11-19

对齐《uLife OS：个人智能体操作系统实战指南》v2.1 全篇升级：
1. 品牌定名 uLife OS / Personal Agent OS（SKILL.md + README + 模板标题）
2. 新增冷启动上下文预算契约（T1/T2/T3）→ SKILL.md §2.5 + references/protocols.md
3. 新增人机接力检查点（低风险放行 / 高风险挂起审批）→ protocols.md + hooks 模板
4. 新增 Code-as-Glue 脚本编排 + 本地/云端异构算力路由 → skills.md + SKILL.md 原则
5. L2 记忆升级为「情景 + Outbox 回执 + Inbox/Pending 审批队列」→ memory.md
6. 引入 Rework Rate 返工率观测 + 质量门命令卡 + 收官期护栏 → maintenance.md
7. 成熟度自检扩展至 12 项；技能包 source_guide 指针升级 v2.1

## 1.0.0 — 2026-11-18 — 2026-11-18

从《个人AI基础设施构建指南 v2.0》（现《uLife OS 实战指南》）提炼为可发布技能包，10 轮迭代：

1. 包骨架 + 核心 SKILL.md（触发语 + 契约 + 工作流 + 硬边界）
2. 六份核心 references（身份/记忆/技能/权限/钩子/协议/维护）
3. TELOS 十文件模板
4. 通用模板（身份契约 / 钩子清单 / 权限矩阵 / 成熟度自检）
5. 确定性工具脚本（audit.py 只读审计 · init_pai.py 初始化，零依赖）
6. README（面向大众的安装 / 快速开始 / 四种用法）+ MIT LICENSE
7. 最小可用示例（MISSION / GOALS / 身份契约）
8. CHANGELOG + 可发现性清单
9. agent-skills 规范自检（name/description/frontmatter/渐进披露）
10. 文档双向挂接（指南 §11 新增技能入口）

## 版本语义
- 1.x = 指南 → 技能包的可发布首版
- 后续小版本按 `references/maintenance.md` 五步回路迭代
