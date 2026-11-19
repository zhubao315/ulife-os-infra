"""Memory Engine：统一 Schema 校验、类型区分、生命周期、冲突检测。零依赖。"""
import json, re
from pathlib import Path

TYPES = ["explicit_fact", "inferred_preference", "episodic", "semantic",
         "procedural", "temporary", "unverified_hypothesis"]
STATUSES = ["captured", "classified", "validated", "approved", "persisted", "archived"]
FLOW = ["Capture", "Classify", "Validate", "Approve", "Persist", "Revalidate"]

def validate(mem):
    errs = []
    for k in ["id", "type", "content", "source", "created_at", "status"]:
        if k not in mem or not mem[k]:
            errs.append("缺必需字段: " + k)
    if mem.get("type") not in TYPES:
        errs.append("非法 type: " + str(mem.get("type")))
    if mem.get("status") not in STATUSES:
        errs.append("非法 status: " + str(mem.get("status")))
    if mem.get("sensitivity") not in (None, "PUBLIC", "INTERNAL", "PRIVATE", "RESTRICTED"):
        errs.append("非法 sensitivity: " + str(mem.get("sensitivity")))
    return errs

def lifecycle_stage(status):
    return {"captured": 0, "classified": 1, "validated": 2,
            "approved": 3, "persisted": 4, "archived": 5}.get(status, -1)

def detect_conflicts(memories):
    out = []
    for i, a in enumerate(memories):
        for b in memories[i+1:]:
            if a.get("type") == b.get("type"):
                sa = set(re.findall(r"\w+", a.get("content", "").lower()))
                sb = set(re.findall(r"\w+", b.get("content", "").lower()))
                if len(sa & sb) >= 2 and sa != sb:
                    out.append((a.get("id"), b.get("id"), "同类型关键词重合，请人工核对"))
    return out

def load_all(root):
    p = Path(root) / "USER" / "memory"
    if not p.exists():
        return []
    items = []
    for f in p.glob("*.json"):
        try:
            items.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            pass
    return items

def lint(root):
    items = load_all(root)
    report = {"count": len(items), "errors": [], "conflicts": [], "expired": []}
    now = datetime_now()
    for m in items:
        errs = validate(m)
        for e in errs:
            report["errors"].append((m.get("id"), e))
        exp = m.get("expires_at")
        if exp and exp < now:
            report["expired"].append(m.get("id"))
        # 推断未经确认不得标 explicit_fact
        if m.get("type") == "explicit_fact" and m.get("source") in ("inference", "inferred"):
            report["errors"].append((m.get("id"), "推断内容不得标为 explicit_fact"))
    report["conflicts"] = detect_conflicts(items)
    return report

def datetime_now():
    import datetime
    return datetime.datetime.now().isoformat()
