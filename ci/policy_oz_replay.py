#!/usr/bin/env python3
"""Route expensive Odd Zeta computational replays by material input closure.

Fast OZ tests always run when this router owns the transition. The measured
expensive modules replay only when their computational inputs change. Scheduled
and manual sentinels replay every expensive module. Producer/verifier state is
never shared; this module changes routing only.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "ci" / "run_unittest_modules.py"
COMPUTATIONAL_SUFFIXES = {".py", ".json", ".c", ".h"}

# Protected-run profile 2026-09-02: these 12 modules consumed ~98% of OZ time.
HEAVY_MODULES = (
    "tests/test_oz_rt_bz_t3_003.py",
    "tests/test_oz_rt_bz_t3_004.py",
    "tests/test_oz_rt_bz_t3_009_search.py",
    "tests/test_oz_rt_bz_t3_010_a.py",
    "tests/test_oz_rt_bz_t3_010_b.py",
    "tests/test_oz_rt_bz_t3_010_c.py",
    "tests/test_oz_rt_bz_t3_011_a.py",
    "tests/test_oz_rt_bz_t3_011_b.py",
    "tests/test_oz_rt_bz_t3_011_c.py",
    "tests/test_oz_rt_bz_t3_011_d.py",
    "tests/test_oz_rt_bz_t3_011_e.py",
    "tests/test_oz_rt_bz_t3_011_f.py",
)

T3 = "campaigns/odd_zeta/OZ_RT_BZ_T3_"
T3_010_DIR = f"{T3}010/"
UPSTREAM_DOWNSTREAM_STAGES = ("002", "005", "006", "009")

# Cumulative stage dependencies inside OZ_RT_BZ_T3_010.
STAGE_TOKENS = {
    "010_a": ("t3_010_a", "T3_010_A"),
    "010_b": ("t3_010_a", "T3_010_A", "t3_010_b", "T3_010_B"),
    "010_c": ("t3_010_a", "T3_010_A", "t3_010_b", "T3_010_B", "t3_010_c", "T3_010_C"),
    "011_a": ("t3_010_a", "T3_010_A", "t3_010_b", "T3_010_B", "t3_010_c", "T3_010_C", "t3_011_a", "T3_011_A"),
    "011_b": ("t3_010_a", "T3_010_A", "t3_010_b", "T3_010_B", "t3_010_c", "T3_010_C", "t3_011_a", "T3_011_A", "t3_011_b", "T3_011_B"),
    "011_c": ("t3_010_a", "T3_010_A", "t3_010_b", "T3_010_B", "t3_010_c", "T3_010_C", "t3_011_a", "T3_011_A", "t3_011_b", "T3_011_B", "t3_011_c", "T3_011_C"),
    "011_d": ("t3_010_a", "T3_010_A", "t3_010_b", "T3_010_B", "t3_010_c", "T3_010_C", "t3_011_a", "T3_011_A", "t3_011_b", "T3_011_B", "t3_011_c", "T3_011_C", "t3_011_d", "T3_011_D"),
    "011_e": ("t3_010_a", "T3_010_A", "t3_010_b", "T3_010_B", "t3_010_c", "T3_010_C", "t3_011_a", "T3_011_A", "t3_011_b", "T3_011_B", "t3_011_c", "T3_011_C", "t3_011_d", "T3_011_D", "t3_011_e", "T3_011_E"),
    "011_f": ("t3_010_a", "T3_010_A", "t3_010_b", "T3_010_B", "t3_010_c", "T3_010_C", "t3_011_a", "T3_011_A", "t3_011_b", "T3_011_B", "t3_011_c", "T3_011_C", "t3_011_d", "T3_011_D", "t3_011_e", "T3_011_E", "t3_011_f", "T3_011_F"),
}
ALL_STAGE_TOKENS = tuple(sorted({token for tokens in STAGE_TOKENS.values() for token in tokens}))
MODULE_STAGE = {
    f"tests/test_oz_rt_bz_t3_{stage}.py": stage
    for stage in STAGE_TOKENS
}


def _normalize(paths: list[str]) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = raw.replace("\\", "/").removeprefix("./")
        if not path or path.startswith("/") or path == ".." or path.startswith("../") or "/../" in path:
            raise RuntimeError(f"unsafe changed path: {raw!r}")
        out.append(path)
    return sorted(set(out))


def _git_has_commit(sha: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    ).returncode == 0


def _fetch_commit(sha: str) -> None:
    if _git_has_commit(sha):
        return
    cp = subprocess.run(
        ["git", "fetch", "--no-tags", "--depth=1", "origin", sha], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90, check=False,
    )
    if cp.returncode:
        raise RuntimeError(f"unable to fetch transition commit {sha}: {cp.stderr.strip()}")


def _changed_paths() -> tuple[str, list[str] | None]:
    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    if event_name in {"schedule", "workflow_dispatch"}:
        return event_name, None
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise RuntimeError("GITHUB_EVENT_PATH unavailable for transition routing")
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    if event_name == "pull_request":
        pr = event.get("pull_request", {})
        base = str(pr.get("base", {}).get("sha") or "")
        head = str(pr.get("head", {}).get("sha") or "")
    elif event_name == "push":
        base = str(event.get("before") or "")
        head = str(event.get("after") or os.environ.get("GITHUB_SHA") or "")
    else:
        raise RuntimeError(f"unsupported OZ routing event: {event_name!r}")
    if len(base) != 40 or len(head) != 40 or set(base) == {"0"}:
        raise RuntimeError("transition base/head unavailable for OZ routing")
    _fetch_commit(base)
    _fetch_commit(head)
    cp = subprocess.run(
        ["git", "diff", "--name-only", base, head, "--"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
    )
    if cp.returncode:
        raise RuntimeError(f"OZ transition diff failed: {cp.stderr.strip()}")
    return event_name, _normalize([line for line in cp.stdout.splitlines() if line.strip()])


def _computational(path: str) -> bool:
    return Path(path).suffix in COMPUTATIONAL_SUFFIXES


def _under_stage(path: str, stage: str) -> bool:
    return path.startswith(f"{T3}{stage}/")


def _downstream_material(path: str, stage: str) -> bool:
    if not _computational(path):
        return False
    if any(_under_stage(path, upstream) for upstream in UPSTREAM_DOWNSTREAM_STAGES):
        return True
    if not path.startswith(T3_010_DIR):
        return False
    name = Path(path).name
    # A computational helper without a governed stage token is shared by
    # assumption and therefore invalidates every downstream heavy replay.
    if not any(token in name for token in ALL_STAGE_TOKENS):
        return True
    return any(token in name for token in STAGE_TOKENS[stage])


def _material(module: str, path: str) -> bool:
    if path == module:
        return True
    if module == "tests/test_oz_rt_bz_t3_003.py":
        return _computational(path) and _under_stage(path, "003")
    if module == "tests/test_oz_rt_bz_t3_004.py":
        return _computational(path) and _under_stage(path, "004")
    if module == "tests/test_oz_rt_bz_t3_009_search.py":
        if path == f"{T3}008/rank_mod.c":
            return True
        return _computational(path) and any(
            _under_stage(path, upstream) for upstream in UPSTREAM_DOWNSTREAM_STAGES
        )
    stage = MODULE_STAGE.get(module)
    return bool(stage and _downstream_material(path, stage))


def select_heavy(changed: list[str] | None) -> list[str]:
    if changed is None:
        return list(HEAVY_MODULES)
    normalized = _normalize(changed)
    return [module for module in HEAVY_MODULES if any(_material(module, path) for path in normalized)]


def _run(args: list[str]) -> None:
    print("OZ_REPLAY_COMMAND " + " ".join(args), flush=True)
    cp = subprocess.run(args, cwd=ROOT, check=False)
    if cp.returncode:
        raise RuntimeError(f"OZ replay command failed with status {cp.returncode}")


def _load_report(path: Path) -> list[dict[str, object]]:
    if not path.is_file():
        raise RuntimeError(f"OZ test report missing: {path}")
    rows = json.loads(path.read_text(encoding="utf-8")).get("modules")
    if not isinstance(rows, list):
        raise RuntimeError(f"OZ test report malformed: {path}")
    return rows


def _write_report(path: str, records: list[dict[str, object]], event: str, changed: list[str] | None, selected: list[str]) -> None:
    (ROOT / path).write_text(
        json.dumps({
            "event": event,
            "changed_paths": changed,
            "heavy_profile_count": len(HEAVY_MODULES),
            "heavy_selected": selected,
            "module_count": len(records),
            "modules": records,
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _run_selected(selected: list[str]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    fast_report = ROOT / ".oz-fast-timing.json"
    fast_cmd = [sys.executable, str(RUNNER), "--discover-root", "tests", "--pattern", "test_oz*.py"]
    for module in HEAVY_MODULES:
        fast_cmd.extend(["--exclude-pattern", Path(module).name])
    fast_cmd.extend(["--report-json", fast_report.relative_to(ROOT).as_posix()])
    try:
        _run(fast_cmd)
        records.extend(_load_report(fast_report))
    finally:
        fast_report.unlink(missing_ok=True)

    for index, module in enumerate(selected, 1):
        report = ROOT / f".oz-heavy-{index}.json"
        try:
            _run([
                sys.executable, str(RUNNER), "--discover-root", "tests",
                "--pattern", Path(module).name,
                "--report-json", report.relative_to(ROOT).as_posix(),
            ])
            records.extend(_load_report(report))
        finally:
            report.unlink(missing_ok=True)
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("routed", "campaign"), default="routed")
    parser.add_argument("--report-json", default="oz-test-timing.json")
    args = parser.parse_args()
    try:
        event, changed = _changed_paths()
        if args.mode == "campaign":
            if changed is None:
                print(f"OZ_CAMPAIGN_ROUTE_NOOP event={event} reason=full-sentinel-owned-by-oz-shard", flush=True)
                _write_report(args.report_json, [], event, changed, [])
                return 0
            if any(path.startswith("tests/test_oz") for path in changed):
                print("OZ_CAMPAIGN_ROUTE_NOOP reason=oz-shard-already-selected", flush=True)
                _write_report(args.report_json, [], event, changed, [])
                return 0
            if not any(path.startswith("campaigns/odd_zeta/") for path in changed):
                print("OZ_CAMPAIGN_ROUTE_NOOP reason=no-odd-zeta-material-change", flush=True)
                _write_report(args.report_json, [], event, changed, [])
                return 0

        selected = select_heavy(changed)
        print(
            f"OZ_REPLAY_SELECTION event={event} mode={args.mode} heavy_selected={len(selected)} heavy_total={len(HEAVY_MODULES)}",
            flush=True,
        )
        for module in HEAVY_MODULES:
            print(f"OZ_REPLAY_ROUTE module={module} status={'REPLAY' if module in selected else 'UNCHANGED'}", flush=True)

        records = _run_selected(selected)
        _write_report(args.report_json, records, event, changed, selected)
        print(
            f"OZ_REPLAY_COMPLETE fast_modules={len(records) - len(selected)} heavy_replayed={len(selected)} total_modules={len(records)}",
            flush=True,
        )
        return 0
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(f"OZ replay routing error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
