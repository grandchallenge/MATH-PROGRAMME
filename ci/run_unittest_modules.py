#!/usr/bin/env python3
"""Run explicit or discovered unittest modules with bounded per-module execution."""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_STR = str(ROOT)
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)

# Empirical 2026-09-01 protected-run envelope:
#   heaviest observed module: 356.6 s
#   OZ suite: 1324.8 s
#   repository regression: 1446.2 s
# Preserve legitimate sentinel work while bounding pathological execution below 30 min.
DEFAULT_MODULE_TIMEOUT_SECONDS = 420
DEFAULT_TOTAL_TIMEOUT_SECONDS = 1620
TIMEOUT_EXIT = 124


def _safe_repo_path(raw: str, *, suffix: str | None = None) -> Path:
    rel = Path(raw)
    if rel.is_absolute() or ".." in rel.parts:
        raise RuntimeError(f"unsafe repository path: {raw!r}")
    path = (ROOT / rel).resolve()
    if ROOT not in path.parents or not path.is_file() or (suffix is not None and path.suffix != suffix):
        raise RuntimeError(f"invalid repository file: {raw!r}")
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
        out.append(_safe_repo_path(raw, suffix=".py"))
    return out


def _discover(root: str, pattern: str) -> list[Path]:
    rel = Path(root)
    if rel.is_absolute() or ".." in rel.parts:
        raise RuntimeError(f"unsafe discovery root: {root!r}")
    base = (ROOT / rel).resolve()
    if ROOT not in base.parents and base != ROOT:
        raise RuntimeError(f"unsafe discovery root: {root!r}")
    if not base.is_dir():
        raise RuntimeError(f"missing discovery root: {root!r}")
    paths = sorted(p.resolve() for p in base.rglob(pattern) if p.is_file() and p.suffix == ".py")
    if not paths:
        raise RuntimeError(f"no tests matched {root!r} / {pattern!r}")
    return paths


def _validate_exclude_pattern(pattern: str) -> str:
    if not pattern or "/" in pattern or "\\" in pattern or pattern in {".", ".."}:
        raise RuntimeError(f"unsafe exclusion pattern: {pattern!r}")
    return pattern


def _apply_exclusions(
    paths: list[Path],
    *,
    exclude_patterns: list[str],
    exclude_manifests: list[str],
) -> tuple[list[Path], list[tuple[Path, str]]]:
    patterns = [_validate_exclude_pattern(pattern) for pattern in exclude_patterns]
    manifest_members: dict[Path, str] = {}
    for raw in exclude_manifests:
        manifest = _safe_repo_path(raw, suffix=".json")
        for path in _manifest_paths(manifest):
            manifest_members[path] = manifest.relative_to(ROOT).as_posix()

    selected: list[Path] = []
    excluded: list[tuple[Path, str]] = []
    for path in paths:
        manifest = manifest_members.get(path)
        if manifest is not None:
            excluded.append((path, f"manifest:{manifest}"))
            continue
        matched = next((pattern for pattern in patterns if fnmatch.fnmatchcase(path.name, pattern)), None)
        if matched is not None:
            excluded.append((path, f"pattern:{matched}"))
            continue
        selected.append(path)

    if not selected:
        raise RuntimeError("all selected test modules were excluded")
    return selected, excluded


def _suite_for(path: Path) -> unittest.TestSuite:
    if ROOT_STR not in sys.path:
        sys.path.insert(0, ROOT_STR)
    return unittest.defaultTestLoader.discover(
        str(path.parent.relative_to(ROOT)), pattern=path.name
    )


def _record(path: Path, result: unittest.TestResult, elapsed: float) -> dict[str, object]:
    return {
        "module": path.relative_to(ROOT).as_posix(),
        "seconds": round(elapsed, 6),
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "status": "PASS" if result.wasSuccessful() else "FAIL",
    }


def _single_module(path: Path, result_json: Path) -> int:
    started = time.perf_counter()
    result = unittest.TextTestRunner(verbosity=1).run(_suite_for(path))
    result_json.write_text(
        json.dumps(_record(path, result, time.perf_counter() - started), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0 if result.wasSuccessful() else 1


def _terminate_process_tree(proc: subprocess.Popen[str]) -> str:
    if proc.poll() is not None:
        out, _ = proc.communicate()
        return out or ""
    try:
        if os.name == "posix":
            os.killpg(proc.pid, signal.SIGTERM)
        else:
            proc.terminate()
        out, _ = proc.communicate(timeout=5)
        return out or ""
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            os.killpg(proc.pid, signal.SIGKILL)
        else:
            proc.kill()
        out, _ = proc.communicate()
        return out or ""


def _run_child(path: Path, result_json: Path, timeout_seconds: float) -> tuple[int, str, bool]:
    proc = subprocess.Popen(
        [
            sys.executable,
            str(Path(__file__).resolve()),
            "--single-module",
            path.relative_to(ROOT).as_posix(),
            "--single-result-json",
            str(result_json),
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=(os.name == "posix"),
    )
    try:
        out, _ = proc.communicate(timeout=timeout_seconds)
        return int(proc.returncode or 0), out or "", False
    except subprocess.TimeoutExpired:
        return TIMEOUT_EXIT, _terminate_process_tree(proc), True


def _write_report(path: str | None, records: list[dict[str, object]], total: float) -> None:
    if path:
        (ROOT / path).write_text(
            json.dumps(
                {"module_count": len(records), "seconds": round(total, 6), "modules": records},
                indent=2,
                sort_keys=True,
            ) + "\n",
            encoding="utf-8",
        )


def _parent_main(args: argparse.Namespace) -> int:
    paths = (
        _manifest_paths(_safe_repo_path(args.manifest, suffix=".json"))
        if args.manifest
        else _discover(args.discover_root, args.pattern)
    )
    paths, excluded = _apply_exclusions(
        paths,
        exclude_patterns=args.exclude_pattern,
        exclude_manifests=args.exclude_manifest,
    )
    for path, reason in excluded:
        print(
            f"POLICY_TEST_EXCLUDED module={path.relative_to(ROOT).as_posix()} reason={reason}",
            flush=True,
        )
    print(
        f"POLICY_TEST_SELECTION selected={len(paths)} excluded={len(excluded)}",
        flush=True,
    )

    records: list[dict[str, object]] = []
    failures = 0
    started = time.perf_counter()
    deadline = started + args.total_timeout_seconds if args.total_timeout_seconds > 0 else None

    with tempfile.TemporaryDirectory(prefix="gcl-policy-tests-") as tmp:
        tmp_root = Path(tmp)
        for index, path in enumerate(paths, 1):
            rel = path.relative_to(ROOT).as_posix()
            now = time.perf_counter()
            remaining = None if deadline is None else deadline - now
            if remaining is not None and remaining <= 0:
                total = now - started
                records.append({
                    "module": rel, "seconds": 0.0, "tests_run": 0,
                    "failures": 0, "errors": 1, "skipped": 0,
                    "status": "TOTAL_TIMEOUT",
                })
                print(
                    f"POLICY_TEST_TOTAL_TIMEOUT module={rel} limit_seconds={args.total_timeout_seconds} elapsed_seconds={total:.3f}",
                    flush=True,
                )
                _write_report(args.report_json, records, total)
                return TIMEOUT_EXIT

            timeout = float(args.module_timeout_seconds)
            if remaining is not None:
                timeout = min(timeout, max(0.001, remaining))
            result_path = tmp_root / f"module-{index}.json"
            print(
                f"POLICY_TEST_START module={rel} index={index}/{len(paths)} timeout_seconds={timeout:.3f}",
                flush=True,
            )
            module_started = time.perf_counter()
            returncode, output, timed_out = _run_child(path, result_path, timeout)
            elapsed = time.perf_counter() - module_started
            if output:
                sys.stdout.write(output)
                sys.stdout.flush()

            if timed_out:
                records.append({
                    "module": rel, "seconds": round(elapsed, 6), "tests_run": 0,
                    "failures": 0, "errors": 1, "skipped": 0, "status": "TIMEOUT",
                })
                total = time.perf_counter() - started
                print(
                    f"POLICY_TEST_TIMEOUT module={rel} seconds={elapsed:.3f} limit_seconds={timeout:.3f}",
                    flush=True,
                )
                _write_report(args.report_json, records, total)
                return TIMEOUT_EXIT

            if result_path.is_file():
                record = json.loads(result_path.read_text(encoding="utf-8"))
            else:
                record = {
                    "module": rel, "seconds": round(elapsed, 6), "tests_run": 0,
                    "failures": 0, "errors": 1, "skipped": 0, "status": "ERROR",
                }
            records.append(record)
            ok = returncode == 0 and record.get("status") == "PASS"
            failures += 0 if ok else 1
            print(
                f"POLICY_TEST_TIMING module={rel} seconds={elapsed:.3f} tests={record.get('tests_run', 0)} status={record.get('status', 'ERROR')}",
                flush=True,
            )

    total = time.perf_counter() - started
    print(f"POLICY_TEST_TIMING_TOTAL modules={len(records)} seconds={total:.3f} failures={failures}")
    _write_report(args.report_json, records, total)
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--manifest")
    mode.add_argument("--discover-root")
    ap.add_argument("--pattern", default="test_*.py")
    ap.add_argument("--exclude-pattern", action="append", default=[])
    ap.add_argument("--exclude-manifest", action="append", default=[])
    ap.add_argument("--report-json")
    ap.add_argument("--module-timeout-seconds", type=float, default=DEFAULT_MODULE_TIMEOUT_SECONDS)
    ap.add_argument("--total-timeout-seconds", type=float, default=DEFAULT_TOTAL_TIMEOUT_SECONDS)
    ap.add_argument("--single-module", help=argparse.SUPPRESS)
    ap.add_argument("--single-result-json", help=argparse.SUPPRESS)
    args = ap.parse_args()

    try:
        if args.module_timeout_seconds <= 0 or args.total_timeout_seconds < 0:
            raise RuntimeError("timeouts must be positive; total timeout may be zero only to disable it")
        if args.single_module:
            if not args.single_result_json:
                raise RuntimeError("single-module execution requires --single-result-json")
            return _single_module(_safe_repo_path(args.single_module, suffix=".py"), Path(args.single_result_json))
        if not args.manifest and not args.discover_root:
            raise RuntimeError("one of --manifest or --discover-root is required")
        return _parent_main(args)
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError, ImportError) as exc:
        print(f"timed unittest runner error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
