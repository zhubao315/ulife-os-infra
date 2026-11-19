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
