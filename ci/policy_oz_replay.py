#!/usr/bin/env python3
"""Route expensive Odd Zeta computational replays by material input closure.

Fast OZ tests always run when this router owns the transition. Retained
computational modules replay only when their material inputs change. Scheduled
and manual sentinels replay every retained computational module. Producer and
verifier state is never shared; this module changes routing only.
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
COMPUTATIONAL_SUFFIXES = {".py", ".json", ".c", ".h", ".inc"}

LOCAL_MODULES = (
    "tests/test_oz_rt_bz_t3_003.py",
    "tests/test_oz_rt_bz_t3_004.py",
)
SEARCH_MODULE = "tests/test_oz_rt_bz_t3_009_search.py"

EARLY_CHAIN_STAGES = (
    "010_a",
    "010_b",
    "010_c",
    "011_a",
    "011_b",
    "011_c",
    "011_d",
    "011_e",
    "011_f",
    "011_g",
)
EARLY_CHAIN_MODULES = tuple(
    f"tests/test_oz_rt_bz_t3_{stage}.py" for stage in EARLY_CHAIN_STAGES
)

# These stages were added after the original protected runtime profile. They
# form the retained successor chain from 011-H through the current 016-A
# Section C work. A material change in one group invalidates that group and
# every later group. T3-016-A has three local replay modules over one
# computational directory and therefore replays as one group.
LATE_STAGE_GROUPS = (
    ("OZ_RT_BZ_T3_011_H", ("tests/test_oz_rt_bz_t3_011_h.py",)),
    ("OZ_RT_BZ_T3_011_I", ("tests/test_oz_rt_bz_t3_011_i.py",)),
    ("OZ_RT_BZ_T3_011_J", ("tests/test_oz_rt_bz_t3_011_j.py",)),
    ("OZ_RT_BZ_T3_011_K", ("tests/test_oz_rt_bz_t3_011_k.py",)),
    ("OZ_RT_BZ_T3_011_L", ("tests/test_oz_rt_bz_t3_011_l.py",)),
    ("OZ_RT_BZ_T3_011_M", ("tests/test_oz_rt_bz_t3_011_m.py",)),
    ("OZ_RT_BZ_T3_011_N", ("tests/test_oz_rt_bz_t3_011_n.py",)),
    ("OZ_RT_BZ_T3_011_O", ("tests/test_oz_rt_bz_t3_011_o.py",)),
    ("OZ_RT_BZ_T3_011_P", ("tests/test_oz_rt_bz_t3_011_p.py",)),
    ("OZ_RT_BZ_T3_011_Q", ("tests/test_oz_rt_bz_t3_011_q.py",)),
    ("OZ_RT_BZ_T3_011_R", ("tests/test_oz_rt_bz_t3_011_r.py",)),
    ("OZ_RT_BZ_T3_012_A", ("tests/test_oz_rt_bz_t3_012_a.py",)),
    ("OZ_RT_BZ_T3_012_B", ("tests/test_oz_rt_bz_t3_012_b.py",)),
    ("OZ_RT_BZ_T3_013_A", ("tests/test_oz_rt_bz_t3_013_a.py",)),
    ("OZ_RT_BZ_T3_014", ("tests/test_oz_rt_bz_t3_014.py",)),
    ("OZ_RT_BZ_T3_015_A", ("tests/test_oz_rt_bz_t3_015_a.py",)),
    ("OZ_RT_BZ_T3_015_B", ("tests/test_oz_rt_bz_t3_015_b.py",)),
    ("OZ_RT_BZ_T3_015_C", ("tests/test_oz_rt_bz_t3_015_c.py",)),
    (
        "OZ_RT_BZ_T3_016_A",
        (
            "tests/test_oz_rt_bz_t3_016_a.py",
            "tests/test_oz_rt_bz_t3_016_a_gauge_domain.py",
            "tests/test_oz_rt_bz_t3_016_a_minimal_kernel_basis.py",
        ),
    ),
)
LATE_MODULES = tuple(
    module
    for _directory, modules in LATE_STAGE_GROUPS
    for module in modules
)
LATE_MODULE_GROUP = {
    module: index
    for index, (_directory, modules) in enumerate(LATE_STAGE_GROUPS)
    for module in modules
}

HEAVY_MODULES = LOCAL_MODULES + (SEARCH_MODULE,) + EARLY_CHAIN_MODULES + LATE_MODULES

# 011-G performs a producer plus an independently reconstructed verifier replay
# over all 1,282 frozen F records. Exact-head measurements reached the generic
# 420 s boundary without a mathematical/test failure. Keep the recovery local
# to this module and inside the existing 1,680 s OZ shard envelope.
HEAVY_MODULE_TIMEOUT_OVERRIDES = {
    "tests/test_oz_rt_bz_t3_011_g.py": 600.0,
}

T3 = "campaigns/odd_zeta/OZ_RT_BZ_T3_"
T3_010_DIR = f"{T3}010/"
UPSTREAM_DOWNSTREAM_STAGES = ("002", "005", "006", "009")

EARLY_STAGE_TOKEN_VARIANTS = {
    stage: (f"t3_{stage}", f"T3_{stage.upper()}")
    for stage in EARLY_CHAIN_STAGES
}
ALL_EARLY_STAGE_TOKENS = tuple(
    token
    for stage in EARLY_CHAIN_STAGES
    for token in EARLY_STAGE_TOKEN_VARIANTS[stage]
)
EARLY_MODULE_STAGE_INDEX = {
    module: index for index, module in enumerate(EARLY_CHAIN_MODULES)
}


def _normalize(paths: list[str]) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = raw.replace("\\", "/").removeprefix("./")
        if (
            not path
            or path.startswith("/")
            or path == ".."
            or path.startswith("../")
            or "/../" in path
            or path.endswith("/..")
        ):
            raise RuntimeError(f"unsafe changed path: {raw!r}")
        out.append(path)
    return sorted(set(out))


def _git_has_commit(sha: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def _fetch_commit(sha: str) -> None:
    if _git_has_commit(sha):
        return
    cp = subprocess.run(
        ["git", "fetch", "--no-tags", "--depth=1", "origin", sha],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=90,
        check=False,
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
    elif event_name == "merge_group":
        merge_group = event.get("merge_group", {})
        base = str(merge_group.get("base_sha") or "")
        head = str(merge_group.get("head_sha") or "")
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
        ["git", "diff", "--name-only", base, head, "--"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if cp.returncode:
        raise RuntimeError(f"OZ transition diff failed: {cp.stderr.strip()}")
    return event_name, _normalize([line for line in cp.stdout.splitlines() if line.strip()])


def _computational(path: str) -> bool:
    return Path(path).suffix in COMPUTATIONAL_SUFFIXES


def _under_stage(path: str, stage: str) -> bool:
    return path.startswith(f"{T3}{stage}/")


def _early_changed_stage_index(path: str) -> int | None:
    if not path.startswith(T3_010_DIR):
        return None
    name = Path(path).name
    for index, stage in enumerate(EARLY_CHAIN_STAGES):
        if any(token in name for token in EARLY_STAGE_TOKEN_VARIANTS[stage]):
            return index
    return None


def _early_chain_material(path: str, target_index: int) -> bool:
    if not _computational(path):
        return False
    if any(_under_stage(path, upstream) for upstream in UPSTREAM_DOWNSTREAM_STAGES):
        return True
    if not path.startswith(T3_010_DIR):
        return False
    changed_index = _early_changed_stage_index(path)
    # A computational helper without a governed stage token is shared by
    # assumption and therefore invalidates every downstream replay.
    return changed_index is None or changed_index <= target_index


def _late_changed_group_index(path: str) -> int | None:
    for index, (directory, _modules) in enumerate(LATE_STAGE_GROUPS):
        if path.startswith(f"campaigns/odd_zeta/{directory}/"):
            return index
    return None


def _late_chain_material(path: str, target_index: int) -> bool:
    if not _computational(path):
        return False
    if any(_under_stage(path, upstream) for upstream in UPSTREAM_DOWNSTREAM_STAGES):
        return True
    if path.startswith(T3_010_DIR):
        return True
    changed_index = _late_changed_group_index(path)
    return changed_index is not None and changed_index <= target_index


def _material(module: str, path: str) -> bool:
    # A test mutation replays that test itself; tests do not become mathematical
    # predecessor inputs for downstream stages.
    if path == module:
        return True
    if module == LOCAL_MODULES[0]:
        return _computational(path) and _under_stage(path, "003")
    if module == LOCAL_MODULES[1]:
        return _computational(path) and _under_stage(path, "004")
    if module == SEARCH_MODULE:
        if path == f"{T3}008/rank_mod.c":
            return True
        return _computational(path) and any(
            _under_stage(path, upstream) for upstream in UPSTREAM_DOWNSTREAM_STAGES
        )
    early_index = EARLY_MODULE_STAGE_INDEX.get(module)
    if early_index is not None:
        return _early_chain_material(path, early_index)
    late_index = LATE_MODULE_GROUP.get(module)
    if late_index is not None:
        return _late_chain_material(path, late_index)
    raise RuntimeError(f"unregistered OZ retained replay module: {module}")


def select_heavy(changed: list[str] | None) -> list[str]:
    if changed is None:
        return list(HEAVY_MODULES)
    normalized = _normalize(changed)
    return [
        module
        for module in HEAVY_MODULES
        if any(_material(module, path) for path in normalized)
    ]


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


def _write_report(
    path: str,
    records: list[dict[str, object]],
    event: str,
    changed: list[str] | None,
    selected: list[str],
) -> None:
    (ROOT / path).write_text(
        json.dumps(
            {
                "event": event,
                "changed_paths": changed,
                "heavy_profile_count": len(HEAVY_MODULES),
                "heavy_selected": selected,
                "module_count": len(records),
                "modules": records,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _run_selected(selected: list[str]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    fast_report = ROOT / ".oz-fast-timing.json"
    fast_cmd = [
        sys.executable,
        str(RUNNER),
        "--discover-root",
        "tests",
        "--pattern",
        "test_oz*.py",
    ]
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
        cmd = [
            sys.executable,
            str(RUNNER),
            "--discover-root",
            "tests",
            "--pattern",
            Path(module).name,
            "--report-json",
            report.relative_to(ROOT).as_posix(),
        ]
        override = HEAVY_MODULE_TIMEOUT_OVERRIDES.get(module)
        if override is not None:
            cmd.extend(["--module-timeout-seconds", str(override)])
        try:
            _run(cmd)
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
                print(
                    f"OZ_CAMPAIGN_ROUTE_NOOP event={event} "
                    "reason=full-sentinel-owned-by-oz-shard",
                    flush=True,
                )
                _write_report(args.report_json, [], event, changed, [])
                return 0
            if any(path.startswith("tests/test_oz") for path in changed):
                print(
                    "OZ_CAMPAIGN_ROUTE_NOOP reason=oz-shard-already-selected",
                    flush=True,
                )
                _write_report(args.report_json, [], event, changed, [])
                return 0
            if not any(path.startswith("campaigns/odd_zeta/") for path in changed):
                print(
                    "OZ_CAMPAIGN_ROUTE_NOOP reason=no-odd-zeta-material-change",
                    flush=True,
                )
                _write_report(args.report_json, [], event, changed, [])
                return 0

        selected = select_heavy(changed)
        print(
            f"OZ_REPLAY_SELECTION event={event} mode={args.mode} "
            f"heavy_selected={len(selected)} heavy_total={len(HEAVY_MODULES)}",
            flush=True,
        )
        for module in HEAVY_MODULES:
            status = "REPLAY" if module in selected else "UNCHANGED"
            print(f"OZ_REPLAY_ROUTE module={module} status={status}", flush=True)

        records = _run_selected(selected)
        _write_report(args.report_json, records, event, changed, selected)
        print(
            f"OZ_REPLAY_COMPLETE fast_modules={len(records) - len(selected)} "
            f"heavy_replayed={len(selected)} total_modules={len(records)}",
            flush=True,
        )
        return 0
    except (
        OSError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
        subprocess.TimeoutExpired,
    ) as exc:
        print(f"OZ replay routing error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
