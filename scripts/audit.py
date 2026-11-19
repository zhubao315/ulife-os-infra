#!/usr/bin/env python3
"""兼容 shim：旧入口转发到统一 CLI 的 audit（v1.2 五层审计）。"""
import sys
from pathlib import Path
import audit_engine

if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    r = audit_engine.run(root, "standard")
    print(r.to_md(root))
    sys.exit(1 if r.counts()["ERROR"] else 0)
