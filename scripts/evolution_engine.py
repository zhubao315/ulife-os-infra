"""Evolution：从审计/观测发现瓶颈 → 生成变更提案 → 验证 → 迁移/回滚。零依赖。"""
import json, shutil, datetime
from pathlib import Path

def find_bottlenecks(audit_counts, obs):
    """基于真实数据找瓶颈，不臆测。"""
    out = []
    if audit_counts.get("ERROR", 0) > 0:
        out.append(("P0", f"审计发现 {audit_counts['ERROR']} 个 ERROR，先修复"))
    if audit_counts.get("NOT CHECKED", 0) > audit_counts.get("PASS", 0) // 2:
        out.append(("P1", "NOT CHECKED 过多：补数据契约而非标绿"))
    for k in ["rework_rate", "context_efficiency", "maintenance_cost"]:
        if obs.get(k) is None:
            out.append(("P2", f"{k} 无数据：需埋点，禁止估算"))
    return out

def snapshot(root, backup_dir):
    """变更前的可回滚快照。"""
    b = Path(backup_dir)
    b.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    dest = b / f"snapshot-{stamp}"
    shutil.copytree(root, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return dest

def rollback(snapshot_dir, root):
    """从快照回滚（覆盖现有，需用户确认后调用）。"""
    shutil.copytree(snapshot_dir, root, dirs_exist_ok=True)
    return True
