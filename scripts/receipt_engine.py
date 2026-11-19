"""Outbox Receipt：外部真实世界回执的落盘、校验、审计关联。零依赖。"""
import json, datetime
from pathlib import Path

def build_receipt(action, result, external_evidence="", verified=False, approver=""):
    return {
        "receipt_id": "rcpt-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "action": action,
        "result": result,  # success / failure / partial
        "external_evidence": external_evidence,
        "timestamp": datetime.datetime.now().isoformat(),
        "verified": bool(verified),
        "approver": approver,
    }

def persist(root, receipt):
    p = Path(root) / "Outbox" / (receipt["receipt_id"] + ".json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    return p

def validate(r):
    errs = []
    for k in ["receipt_id", "action", "result", "timestamp", "verified"]:
        if k not in r:
            errs.append("缺字段: " + k)
    if r.get("result") not in ("success", "failure", "partial"):
        errs.append("非法 result")
    if r.get("result") == "success" and not r.get("external_evidence"):
        errs.append("success 回执缺外部证据（OVP 纪律）")
    return errs

def audit(root):
    """统计回执健康：无证据成功数、未验证数。"""
    p = Path(root) / "Outbox"
    items = []
    if p.exists():
        for f in p.glob("*.json"):
            try:
                items.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                pass
    return {
        "count": len(items),
        "unverified": sum(1 for r in items if not r.get("verified")),
        "success_without_evidence": sum(1 for r in items if r.get("result") == "success" and not r.get("external_evidence")),
        "errors": [e for r in items for e in validate(r)],
    }
