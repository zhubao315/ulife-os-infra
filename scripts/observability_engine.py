"""Observability：10 指标定义 + 从可验证数据源计算，不捏造。零依赖。"""
import json
from pathlib import Path

# 指标定义：名称 / 计算口径 / 数据来源 / 是否可自动计算
METRICS = {
    "task_success_rate": ("成功任务/总任务", "Outbox receipt result=success 占比", True),
    "rework_rate": ("返工次数/任务数", "需人工标注 rework，无数据则 NOT MEASURED", False),
    "context_efficiency": ("有效token/总token", "budget_engine 估算 + 工具输出记录", False),
    "memory_accuracy": ("验证通过记忆/总记忆", "memory_engine.lint 的 validated 比例", True),
    "skill_reuse_rate": ("被复用skill/总skill", "需 skill 调用日志，无则 NOT MEASURED", False),
    "policy_violation_rate": ("拦截次数/写入尝试", "grant/verify 拒绝记录", True),
    "approval_rate": ("需审批操作/总操作", "RISK_MATRIX 授权记录", True),
    "agent_failure_rate": ("失败任务/总任务", "Outbox receipt result=failure 占比", True),
    "recovery_success_rate": ("恢复成功/回滚次数", "需 Evolution 变更日志", False),
    "maintenance_cost": ("维护耗时", "需用户记录，不推算", False),
}

def collect(root):
    root = Path(root)
    result = {}
    # 从 Outbox 计算可自动指标
    outbox = root / "Outbox"
    receipts = []
    if outbox.exists():
        for f in outbox.glob("*.json"):
            try:
                receipts.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                pass
    total = len(receipts)
    succ = sum(1 for r in receipts if r.get("result") == "success")
    fail = sum(1 for r in receipts if r.get("result") == "failure")
    result["task_success_rate"] = (succ / total) if total else None
    result["agent_failure_rate"] = (fail / total) if total else None

    # memory accuracy
    try:
        import memory_engine
        m = memory_engine.lint(root)
        if m["count"]:
            result["memory_accuracy"] = max(0, (m["count"] - len(m["errors"])) / m["count"])
        else:
            result["memory_accuracy"] = None
    except Exception:
        result["memory_accuracy"] = None

    # 不可自动计算的指标显式 None（NOT MEASURED）
    for k in METRICS:
        result.setdefault(k, None)
    return result

def report(root):
    c = collect(root)
    lines = ["# 系统健康报告（Observability）", "",
             "| 指标 | 值 | 口径 | 状态 |", "|---|---|---|---|"]
    for name, (definition, source, auto) in METRICS.items():
        v = c.get(name)
        status = "NOT MEASURED" if v is None else ("OK" if isinstance(v, (int, float)) else "手动填写")
        val = "—" if v is None else (f"{v:.1%}" if isinstance(v, float) else str(v))
        lines.append(f"| {name} | {val} | {definition} | {status} |")
    lines += ["", "> 无数据依据的指标一律 NOT MEASURED，禁止标绿（Evidence over Claims）。"]
    return "\n".join(lines)
