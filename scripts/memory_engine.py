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


# ── v1.4：导出 / 备份 / 恢复 / 保留期 / 用户主动删除 ────
def export_memories(root, out_path):
    items = load_all(root)
    Path(out_path).write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(items)

def backup(root, out_path):
    """备份整个 USER/memory 目录为 JSON 快照（只读，不改动原文件）。"""
    items = load_all(root)
    snap = {"backup_at": datetime_now(), "count": len(items), "memories": items}
    Path(out_path).write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    return snap

def restore(root, backup_path, merge=True):
    """从备份恢复；默认 merge（不删现有），冲突 id 保留现有版本。"""
    snap = json.loads(Path(backup_path).read_text(encoding="utf-8"))
    target = Path(root) / "USER" / "memory"
    target.mkdir(parents=True, exist_ok=True)
    existing = {m.get("id") for m in load_all(root)}
    restored = 0
    for m in snap.get("memories", []):
        if m.get("id") in existing and merge:
            continue
        (target / (m["id"] + ".json")).write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        restored += 1
    return restored

def purge_expired(root, require_owner=True):
    """清理过期记忆；require_owner=True 时只报告候选，不自动删（用户自主权）。"""
    items = load_all(root)
    now = datetime_now()
    expired = [m for m in items if m.get("expires_at") and m["expires_at"] < now]
    if require_owner:
        return {"candidates": [m.get("id") for m in expired], "deleted": []}
    deleted = []
    for m in expired:
        p = Path(root) / "USER" / "memory" / (m["id"] + ".json")
        if p.exists():
            p.unlink()
            deleted.append(m["id"])
    return {"candidates": [m.get("id") for m in expired], "deleted": deleted}
