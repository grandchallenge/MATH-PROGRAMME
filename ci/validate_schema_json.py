#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main() -> int:
    paths = sorted((ROOT / "schemas").glob("*.json"))
    if not paths:
        raise SystemExit("no governed schemas found")
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))
        print(f"valid json: {path.relative_to(ROOT).as_posix()}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
