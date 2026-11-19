---
title: "v1.4 运维 — 回执、备份与记忆生命周期"
created: 2026-11-19
tags: ["维度/科技", "类型/参考", "来源/项目"]
---

# 运维（v1.4）

## Outbox Receipt
- `ulife.py receipt --action X --result success --evidence E` 落盘回执。
- OVP 纪律：success 回执必须带外部证据，否则 `receipt audit` 报 ERROR。
- `receipt_engine.audit()` 统计未验证 / 无证据成功数，接 L4 Operational 审计。

## 记忆生命周期
Capture → Classify → Validate → Approve → Persist → Revalidate → Archive。

- 导出：`memory_engine.export_memories()` 
- 备份：`ulife.py memory-backup --out backup.json`
- 恢复：`ulife.py memory-restore --backup backup.json`（merge 模式，不覆盖现有）
- 过期清理：`purge_expired(require_owner=True)` 只报告候选；用户本人确认才删。

## 路由
`ulife.py route --task "私密内容分析" --level PRIVATE` → 自动拦截云端外发，回退 local。
