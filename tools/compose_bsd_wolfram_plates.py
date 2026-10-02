#!/usr/bin/env python3
"""Replay the reviewed BSD exact-object web derivatives byte-for-byte.

Mathematical fixtures remain governed by ``bsd_wolfram_semantic_master.wl``.
Presentation geometry is reviewed against ``bsd_wolfram_layout_reference.wl``.
This tool deliberately copies the approved static SVG snapshots rather than
re-composing them: the superseded free-coordinate compositor caused text
bleeding and is no longer allowed to synthesize live typography. No plate is
mathematical evidence.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/assets/visual_pedagogy/bsd_exact"
NAMES = (
    "plate_01_rational_point_triangle.svg",
    "plate_02_group_law.svg",
    "plate_03_good_prime.svg",
    "plate_04_strong_bsd_ledger.svg",
    "plate_05_theorem_frontier.svg",
)


def emit(out: Path) -> list[tuple[str, str]]:
    out.mkdir(parents=True, exist_ok=True)
    hashes: list[tuple[str, str]] = []
    for name in NAMES:
        src = SOURCE / name
        data = src.read_bytes()
        dst = out / name
        if dst.resolve() != src.resolve():
            dst.write_bytes(data)
        hashes.append((name, hashlib.sha256(data).hexdigest()))
    return hashes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=SOURCE)
    parser.add_argument("--hashes", action="store_true")
    args = parser.parse_args()
    hashes = emit(args.root)
    if args.hashes:
        for name, digest in hashes:
            print(f"{digest}  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
