"""一次性授权凭据：操作 + 目标 + Diff + 授权人 + 有效期 + 回执。
ULIFE_GUARD_ACK=1 仅视为意图标识，不能单独作为安全认证。"""
import json, uuid, datetime
from pathlib import Path

def grant(root: Path, operation: str, target: str, diff_hash: str, approver: str, minutes: int = 30):
    now = datetime.datetime.now()
    g = {
        "grant_id": str(uuid.uuid4()),
        "operation": operation,
        "target": target,
        "diff_hash": diff_hash,
        "approver": approver,
        "issued_at": now.isoformat(),
        "expires_at": (now + datetime.timedelta(minutes=minutes)).isoformat(),
        "used": False,
        "receipt": None,
        "note": "ULIFE_GUARD_ACK=1 仅为意图标识；真实边界须由外部权限层执行",
    }
    p = root / "SYSTEM" / "grants" / f"GRANT-{g['grant_id']}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    return g

def verify(root: Path, grant_id: str, diff_hash: str) -> bool:
    p = root / "SYSTEM" / "grants" / f"GRANT-{grant_id}.json"
    if not p.exists():
        return False
    g = json.loads(p.read_text(encoding="utf-8"))
    if g["used"] or g["diff_hash"] != diff_hash:
        return False
    exp = datetime.datetime.fromisoformat(g["expires_at"])
    if exp < datetime.datetime.now():
        return False
    g["used"] = True
    g["receipt"] = datetime.datetime.now().isoformat()
    p.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


# ── v1.4：数据分级 + 风险矩阵 ──────────────────────────
DATA_LEVELS = ["PUBLIC", "INTERNAL", "PRIVATE", "RESTRICTED"]
RISK_MATRIX = {
    "read_only":          {"level": "L0", "approval": False, "external_ok": True},
    "internal_reversible":{"level": "L1", "approval": False, "external_ok": True},
    "user_asset_write":   {"level": "L2", "approval": True,  "external_ok": False},
    "external_send":      {"level": "L3", "approval": True,  "external_ok": True},
    "irreversible":       {"level": "L3", "approval": True,  "external_ok": False},
}

def can_send_external(data_level, operation="external_send", authorized=False):
    """数据分级门禁：PRIVATE/RESTRICTED 必须带显式授权凭据(authorized=True)方可外发。"""
    rule = RISK_MATRIX.get(operation, RISK_MATRIX["irreversible"])
    if data_level in ("PRIVATE", "RESTRICTED") and not authorized:
        return False, f"{data_level} 数据需显式授权凭据方可外发"
    if not rule["external_ok"]:
        return False, f"操作 {operation} 不允许外发"
    return True, "允许"

def risk_of(operation):
    return RISK_MATRIX.get(operation, RISK_MATRIX["irreversible"])
