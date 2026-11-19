#!/usr/bin/env python3
"""兼容 shim：旧入口转发到统一 CLI 的 init（v1.2 起 canonical 模板）。"""
import sys
from pathlib import Path
import init_engine

if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./my-ulife")
    init_engine.execute(root, "starter", False, False)
