#!/usr/bin/env python3
"""Assemble the exact GCL-TCS-00 Markdown source from review parts."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "parts"
OUTPUT = ROOT / "GCL-TCS-00.md"
EXPECTED_SHA256 = "ea750b9b80b53c7d6ed755978fa4bdf59413fad93cec1db81eb3238372ce61c9"


def main() -> int:
    paths = sorted(PARTS.glob("*.md"))
    if len(paths) != 7:
        raise SystemExit(f"Expected 7 review parts, found {len(paths)}")
    data = b"".join(path.read_bytes() for path in paths)
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"Source hash mismatch: expected {EXPECTED_SHA256}, got {digest}")
    OUTPUT.write_bytes(data)
    print(OUTPUT.name)
    print(f"sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
