"""Model Routing：本地/云端决策器 + 敏感数据外发拦截。零依赖。"""
from policy_engine import DATA_LEVELS, can_send_external

RULES = [
    ("日记情景识别", "local", "PUBLIC"),
    ("Frontmatter 补全", "local", "INTERNAL"),
    ("普通文件检索", "local", "INTERNAL"),
    ("复杂架构研究", "cloud", "INTERNAL"),
    ("跨领域综合", "hybrid", "INTERNAL"),
    ("私密内容分析", "local", "PRIVATE"),
    ("高风险决策", "human", "RESTRICTED"),
]

def route(task_type):
    for name, target, level in RULES:
        if name in task_type or task_type in name:
            return {"task": name, "route": target, "data_level": level,
                    "external_ok": target in ("cloud", "hybrid")}
    return {"task": task_type, "route": "local", "data_level": "INTERNAL", "external_ok": False}

def decide(task_type, override_level=None):
    d = route(task_type)
    if override_level:
        d["data_level"] = override_level
    if d["route"] in ("cloud", "hybrid"):
        ok, msg = can_send_external(d["data_level"], "external_send")
        if not ok:
            d["route"] = "local"
            d["blocked_reason"] = msg
            d["external_ok"] = False
    return d
