---
title: "DISCOVERABILITY"
created: 2026-11-18
tags:
  - "维度/科技"
  - "类型/参考"
  - "来源/项目"
---

# 可发现性清单（review 用）

| 检查项 | 状态 | 说明 |
|---|---|---|
| SKILL.md frontmatter name 合规 | ✅ | ulife-os-infra（小写连字符，匹配目录名；展示名 uLife-OS-infra） |
| description 含做什么 + 何时用 + 触发关键词 | ✅ | 含"搭建/记住我/第二大脑/审计"等 |
| 主文件 <500 行 | ✅ | 见 SKILL.md |
| 渐进披露（references 按需加载） | ✅ | 7 份主题文档 |
| 通用触发语覆盖 | ✅ | 8 类用户说法 |
| 反向边界（何时不用） | ✅ | SKILL.md §2 |
| 安装说明 | ✅ | README（CLI + 手动） |
| 零依赖声明 | ✅ | Python 仅标准库 |
| 许可证 | ✅ | MIT |
| 版本与迭代日志 | ✅ | CHANGELOG（v1.1.0 对齐指南 v2.1） |

发布前最后一步：`skills-ref validate ./ulife-os-infra`（如环境有该工具）。
