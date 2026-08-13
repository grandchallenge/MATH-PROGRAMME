#!/usr/bin/env python3
"""Run an explicit or discovered unittest module set with per-module timing."""
from __future__ import annotations

import argparse
import json
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _safe_repo_file(raw: str) -> Path:
    rel = Path(raw)
    if rel.is_absolute() or ".." in rel.parts:
        raise RuntimeError(f"unsafe test path: {raw!r}")
    path = (ROOT / rel).resolve()
    if ROOT not in path.parents or not path.is_file() or path.suffix != ".py":
        raise RuntimeError(f"invalid test module: {raw!r}")
    return path


def _manifest_paths(path: Path) -> list[Path]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("manifest_id") != "MP-CONTRACT-TEST-MANIFEST-001":
        raise RuntimeError("contract-test manifest identity drift")
    rows = data.get("tests")
    if not isinstance(rows, list) or not rows:
        raise RuntimeError("contract-test manifest is empty")
    seen: set[str] = set()
    out: list[Path] = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str) or not isinstance(row.get("category"), str):
            raise RuntimeError("invalid contract-test manifest row")
        raw = row["path"]
        if raw in seen:
            raise RuntimeError(f"duplicate contract-test module: {raw}")
        seen.add(raw)
        out.append(_safe_repo_file(raw))
    return out


def _discover(root: str, pattern: str) -> list[Path]:
    base = (ROOT / root).resolve()
    if ROOT not in base.parents and base != ROOT:
        raise RuntimeError(f"unsafe discovery root: {root!r}")
    if not base.is_dir():
        raise RuntimeError(f"missing discovery root: {root!r}")
    paths = sorted(p.resolve() for p in base.rglob(pattern) if p.is_file())
    if not paths:
        raise RuntimeError(f"no tests matched {root!r} / {pattern!r}")
    return paths


def _suite_for(path: Path) -> unittest.TestSuite:
    rel_parent = path.parent.relative_to(ROOT)
    return unittest.defaultTestLoader.discover(str(rel_parent), pattern=path.name, top_level_dir=str(ROOT))


def main() -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--manifest")
    mode.add_argument("--discover-root")
    ap.add_argument("--pattern", default="test_*.py")
    ap.add_argument("--report-json")
    args = ap.parse_args()
    try:
        paths = _manifest_paths(_safe_repo_file(args.manifest)) if args.manifest else _discover(args.discover_root, args.pattern)
        records: list[dict[str, object]] = []
        failures = 0
        started = time.perf_counter()
        for path in paths:
            rel = path.relative_to(ROOT).as_posix()
            t0 = time.perf_counter()
            result = unittest.TextTestRunner(verbosity=1).run(_suite_for(path))
            elapsed = time.perf_counter() - t0
            ok = result.wasSuccessful()
            failures += 0 if ok else 1
            record = {
                "module": rel,
                "seconds": round(elapsed, 6),
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "skipped": len(result.skipped),
                "status": "PASS" if ok else "FAIL",
            }
            records.append(record)
            print(
                f"POLICY_TEST_TIMING module={rel} seconds={elapsed:.3f} "
                f"tests={result.testsRun} status={record['status']}",
                flush=True,
            )
        total = time.perf_counter() - started
        report = {"module_count": len(records), "seconds": round(total, 6), "modules": records}
        print(f"POLICY_TEST_TIMING_TOTAL modules={len(records)} seconds={total:.3f} failures={failures}")
        if args.report_json:
            (ROOT / args.report_json).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return 1 if failures else 0
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"timed unittest runner error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
