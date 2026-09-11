#!/usr/bin/env python3
"""Material-closure router and executor for MATH-PROGRAMME formal validation."""
from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Iterable

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance/formal_validation_registry.json"
SCHEMA_PATH = ROOT / "schemas/formal_validation_registry.schema.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
LOCAL_FORBIDDEN = re.compile(r"^[ \t]*(?:sorry|axiom)(?:[ \t]|$)", re.MULTILINE)


class FormalValidationError(RuntimeError):
    pass


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry(root: Path = ROOT) -> dict:
    registry = load_json(root / REGISTRY_PATH.relative_to(ROOT))
    schema = load_json(root / SCHEMA_PATH.relative_to(ROOT))
    jsonschema.validate(registry, schema)
    validate_registry(registry)
    return registry


def validate_registry(registry: dict) -> None:
    if registry["required_context"] != "formal-validation / formal-validation":
        raise FormalValidationError("generic protected formal-validation context drift")
    lanes = registry["lanes"]
    ids = [lane["id"] for lane in lanes]
    if len(ids) != len(set(ids)):
        raise FormalValidationError("formal lane ids must be unique")
    by_id = {lane["id"]: lane for lane in lanes}
    sentinel = registry["sentinels"]["legacy_formal_lanes"]
    if set(sentinel) != {"log-gcd", "pc-wp04", "union-closed-mathcert"}:
        raise FormalValidationError("legacy formal sentinel lane set drift")
    if not set(sentinel).issubset(by_id):
        raise FormalValidationError("sentinel references unknown formal lane")
    cmdg = [lane for lane in lanes if lane["family"] == "CMDG"]
    if not cmdg:
        raise FormalValidationError("CMDG formal lanes are missing")
    package = registry["cmdg_environment"]["package_dir"]
    for lane in cmdg:
        if lane["execution_kind"] != "cmdg-lean-closure":
            raise FormalValidationError(f"{lane['id']}: CMDG lane must use Lean dependency closure")
        if lane["package_dir"] != package:
            raise FormalValidationError(f"{lane['id']}: CMDG package drift")
        if not lane.get("promotion_workflow"):
            raise FormalValidationError(f"{lane['id']}: promotion/sentinel workflow is required")
    required_controls = {
        ".github/workflows/formal-validation.yml",
        "ci/formal_validation.py",
        "ci/test_formal_validation.py",
        "governance/formal_validation_registry.json",
        "schemas/formal_validation_registry.schema.json",
    }
    controls = set(registry["control_plane"]["full_fanout_patterns"])
    if not required_controls.issubset(controls):
        raise FormalValidationError("formal router self-control paths must conservatively full-fanout")


def normalize_paths(paths: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for raw in paths:
        if not isinstance(raw, str) or not raw or "\x00" in raw:
            raise FormalValidationError(f"invalid changed path: {raw!r}")
        path = raw[2:] if raw.startswith("./") else raw
        p = PurePosixPath(path)
        if p.is_absolute() or ".." in p.parts or path.startswith("/"):
            raise FormalValidationError(f"unsafe changed path: {raw!r}")
        normalized.append(path)
    return sorted(set(normalized))


def matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        root = pattern[:-3].rstrip("/")
        return path == root or path.startswith(root + "/")
    return fnmatch.fnmatchcase(path, pattern)


def lane_map(registry: dict) -> dict[str, dict]:
    return {lane["id"]: lane for lane in registry["lanes"]}


def classify_paths(paths: Iterable[str], registry: dict) -> dict:
    changed = normalize_paths(paths)
    lanes = lane_map(registry)
    all_ids = list(lanes)
    cmdg_ids = [lane_id for lane_id, lane in lanes.items() if lane["family"] == "CMDG"]
    controls = registry["control_plane"]

    control_hits = [p for p in changed if any(matches(p, pat) for pat in controls["full_fanout_patterns"])]
    if control_hits:
        return result(changed, all_ids, "control_plane_full_fanout", control_hits, [])

    selected: set[str] = set()
    matched_paths: set[str] = set()
    for lane_id, lane in lanes.items():
        for path in changed:
            if any(matches(path, pat) for pat in lane["material_patterns"]):
                selected.add(lane_id)
                matched_paths.add(path)

    shared_hits = [
        path for path in changed
        if any(matches(path, pat) for pat in controls["shared_cmdg_patterns"])
        and path not in matched_paths
    ]
    if shared_hits:
        selected.update(cmdg_ids)
        matched_paths.update(shared_hits)

    unknown: list[str] = []
    managed_roots = registry["managed_formal_roots"]
    for path in changed:
        if path in matched_paths:
            continue
        if any(path == root or path.startswith(root.rstrip("/") + "/") for root in managed_roots):
            unknown.append(path)
            continue
        if path.startswith("fixtures/formal/") and path.endswith(".lean"):
            unknown.append(path)
            continue
        if (path.startswith("ci/") or path.startswith("tests/")) and path.endswith(".py"):
            name = Path(path).name.lower()
            if "formal" in name or "cmdg" in name:
                unknown.append(path)
    if unknown:
        raise FormalValidationError(
            "unclassified executable/formal path(s): " + ", ".join(sorted(unknown))
        )

    reason = "material_lanes" if selected else "no_formal_material_change"
    return result(changed, [lane_id for lane_id in all_ids if lane_id in selected], reason, [], [])


def result(changed: list[str], lane_ids: list[str], reason: str, control_hits: list[str], unknown: list[str]) -> dict:
    return {
        "changed_paths": changed,
        "lanes": lane_ids,
        "reason": reason,
        "control_plane_hits": sorted(control_hits),
        "unknown_paths": sorted(unknown),
    }


def git(*args: str, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=check, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )


def diff_paths(base: str, head: str, root: Path = ROOT) -> list[str]:
    if not SHA40.fullmatch(base) or not SHA40.fullmatch(head):
        raise FormalValidationError("event diff identities must be full commit SHAs")
    cp = git("diff", "--name-only", "--diff-filter=ACMR", f"{base}...{head}", cwd=root)
    return normalize_paths(line for line in cp.stdout.splitlines() if line)


def event_plan(event_name: str, event: dict, registry: dict, root: Path = ROOT) -> dict:
    if event_name == "schedule":
        expected = registry["sentinels"]["legacy_formal_cron"]
        if event.get("schedule") != expected:
            raise FormalValidationError(f"unknown formal sentinel schedule: {event.get('schedule')!r}")
        lane_ids = list(registry["sentinels"]["legacy_formal_lanes"])
        plan = result([], lane_ids, "protected_main_formal_sentinel", [], [])
        plan["mode"] = "sentinel"
        return plan
    if event_name == "workflow_dispatch":
        plan = result([], list(lane_map(registry)), "manual_conservative_full_fanout", [], [])
        plan["mode"] = "promotion"
        return plan
    if event_name == "pull_request":
        base = str(event.get("pull_request", {}).get("base", {}).get("sha", ""))
        head = str(event.get("pull_request", {}).get("head", {}).get("sha", ""))
        plan = classify_paths(diff_paths(base, head, root), registry)
        plan["mode"] = "development"
        return plan
    if event_name == "merge_group":
        group = event.get("merge_group", {})
        base = str(group.get("base_sha", ""))
        head = str(group.get("head_sha", ""))
        plan = classify_paths(diff_paths(base, head, root), registry)
        plan["mode"] = "promotion"
        return plan
    raise FormalValidationError(f"unsupported formal-validation event: {event_name}")


def matrix_for(lane_ids: list[str], registry: dict) -> dict:
    lanes = lane_map(registry)
    include = []
    for lane_id in lane_ids:
        lane = lanes[lane_id]
        include.append({
            "lane": lane_id,
            "package_dir": lane["package_dir"],
            "external_repository": lane.get("external_repository", ""),
            "external_ref": lane.get("external_ref", ""),
        })
    return {"include": include}


def write_outputs(path: str | None, values: dict[str, object]) -> None:
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        for key, value in values.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, separators=(",", ":"), sort_keys=True)
            elif isinstance(value, bool):
                value = "true" if value else "false"
            handle.write(f"{key}={value}\n")


def run_command(command: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def expand_sources(package: Path, patterns: Iterable[str]) -> list[Path]:
    out: list[Path] = []
    for pattern in patterns:
        matches_ = sorted(package.glob(pattern))
        if not matches_:
            raise FormalValidationError(f"declared formal source pattern has no files: {pattern}")
        out.extend(path for path in matches_ if path.is_file())
    unique = {path.resolve(): path for path in out}
    return [unique[key] for key in sorted(unique, key=str)]


def local_imports(source: Path, package: Path) -> list[Path]:
    imports: list[Path] = []
    for raw in source.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if not stripped.startswith("import "):
            continue
        for module in stripped[len("import "):].split():
            candidate = package / (module.replace(".", "/") + ".lean")
            if candidate.is_file():
                imports.append(candidate)
    return imports


def dependency_order(targets: Iterable[Path], package: Path) -> list[Path]:
    visiting: set[Path] = set()
    visited: set[Path] = set()
    order: list[Path] = []

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in visited:
            return
        if path in visiting:
            raise FormalValidationError(f"local Lean import cycle detected at {path.name}")
        visiting.add(path)
        for dep in local_imports(path, package):
            visit(dep)
        visiting.remove(path)
        visited.add(path)
        order.append(path)

    for target in targets:
        visit(target)
    return order


def reject_local_placeholders(sources: Iterable[Path]) -> None:
    findings = []
    for source in sources:
        text = source.read_text(encoding="utf-8")
        if LOCAL_FORBIDDEN.search(text):
            findings.append(source.name)
    if findings:
        raise FormalValidationError("local Lean placeholders/axioms forbidden: " + ", ".join(findings))


def verify_cmdg_environment(registry: dict, package: Path) -> None:
    expected = registry["cmdg_environment"]
    mathlib = package / ".lake/packages/mathlib"
    if not mathlib.is_dir():
        raise FormalValidationError("pinned mathlib checkout missing after Lean setup")
    commit = git("rev-parse", "HEAD", cwd=mathlib).stdout.strip()
    tree = git("rev-parse", "HEAD^{tree}", cwd=mathlib).stdout.strip()
    if commit != expected["mathlib_commit"] or tree != expected["mathlib_tree"]:
        raise FormalValidationError(
            f"CMDG mathlib identity drift: {commit}/{tree} != "
            f"{expected['mathlib_commit']}/{expected['mathlib_tree']}"
        )


def verify_protected_inputs(lane: dict, package: Path) -> None:
    for relative, expected in lane.get("protected_inputs", {}).items():
        path = package / relative
        if not path.is_file():
            raise FormalValidationError(f"protected formal input missing: {relative}")
        got = git("hash-object", relative, cwd=package).stdout.strip()
        if got != expected:
            raise FormalValidationError(f"protected formal input drift: {relative}: {got} != {expected}")


def compile_cmdg(lane: dict, mode: str, changed_paths: list[str], registry: dict, root: Path = ROOT) -> list[str]:
    package = root / lane["package_dir"]
    verify_cmdg_environment(registry, package)
    verify_protected_inputs(lane, package)

    changed_sources = []
    package_prefix = lane["package_dir"].rstrip("/") + "/"
    if mode == "development":
        for path in changed_paths:
            if path.startswith(package_prefix) and path.endswith(".lean") and any(
                matches(path, pattern) for pattern in lane["material_patterns"]
            ):
                candidate = root / path
                if candidate.is_file():
                    changed_sources.append(candidate)
        targets = changed_sources or expand_sources(package, lane["development_targets"])
    else:
        targets = expand_sources(package, lane["formal_sources"] or lane["development_targets"])

    closure = dependency_order(targets, package)
    reject_local_placeholders(closure)
    build_dir = package / ".lake/build/lib/lean"
    build_dir.mkdir(parents=True, exist_ok=True)
    for source in closure:
        relative = source.relative_to(package).with_suffix("")
        output = build_dir / relative.with_suffix(".olean")
        output.parent.mkdir(parents=True, exist_ok=True)
        run_command(["lake", "env", "lean", "-o", str(output.relative_to(package)), str(source.relative_to(package))], cwd=package)
    return [str(path.relative_to(root)) for path in closure]


def validate_union_evidence(root: Path = ROOT) -> None:
    evidence = load_json(root / "evidence/UC-WP02-MATHCERT.json")
    expected = {
        "repository": "grandchallenge/MATHCERT",
        "commit": "d59173899dcd1a67dbe8f31de0b9f0917cd1459a",
        "command": ["bash", "ci/check_lean.sh"],
    }
    for key, value in expected.items():
        if evidence.get(key) != value:
            raise FormalValidationError(f"Union-Closed evidence {key} drift")


def execute_lane(lane_id: str, mode: str, changed_paths: list[str], registry: dict, root: Path = ROOT) -> dict:
    lanes = lane_map(registry)
    if lane_id not in lanes:
        raise FormalValidationError(f"unknown formal lane: {lane_id}")
    if mode not in {"development", "promotion", "sentinel"}:
        raise FormalValidationError(f"unsupported validation mode: {mode}")
    lane = lanes[lane_id]
    for command in lane["validator_commands"]:
        run_command(command, root)
    compiled: list[str] = []
    kind = lane["execution_kind"]
    if kind == "cmdg-lean-closure":
        compiled = compile_cmdg(lane, mode, changed_paths, registry, root)
    elif kind == "lake-build":
        run_command(["lake", "build"], root / lane["package_dir"])
    elif kind == "external-check":
        validate_union_evidence(root)
        external = root / lane["package_dir"]
        expected = lane["external_ref"]
        got = git("rev-parse", "HEAD", cwd=external).stdout.strip()
        if got != expected:
            raise FormalValidationError(f"external repository identity drift: {got} != {expected}")
        run_command(["bash", "ci/check_lean.sh"], external)
    else:
        raise FormalValidationError(f"unsupported execution kind: {kind}")
    record = {
        "schema_version": 1,
        "lane": lane_id,
        "mode": mode,
        "status": "FORMAL_VALIDATION_SUCCEEDED",
        "changed_paths": changed_paths,
        "compiled_local_lean_closure": compiled,
    }
    out = root / ".formal-validation" / lane_id / "result.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


def command_validate(args: argparse.Namespace) -> int:
    registry = load_registry()
    print(f"{registry['registry_id']}: valid ({len(registry['lanes'])} lanes)")
    return 0


def command_classify_paths(args: argparse.Namespace) -> int:
    registry = load_registry()
    plan = classify_paths(args.path, registry)
    print(json.dumps(plan, sort_keys=True))
    return 0


def command_classify(args: argparse.Namespace) -> int:
    registry = load_registry()
    event = load_json(Path(args.event_path))
    plan = event_plan(args.event_name, event, registry)
    matrix = matrix_for(plan["lanes"], registry)
    outputs = {
        "mode": plan["mode"],
        "formal_lanes": plan["lanes"],
        "formal_matrix": matrix,
        "changed_paths_json": plan["changed_paths"],
        "has_lanes": bool(plan["lanes"]),
        "reason": plan["reason"],
    }
    write_outputs(args.github_output, outputs)
    print(json.dumps({**plan, "matrix": matrix}, sort_keys=True))
    return 0


def command_run(args: argparse.Namespace) -> int:
    registry = load_registry()
    try:
        changed = normalize_paths(json.loads(args.changed_paths_json))
    except json.JSONDecodeError as exc:
        raise FormalValidationError("changed-path JSON is invalid") from exc
    record = execute_lane(args.lane, args.mode, changed, registry)
    print(json.dumps(record, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate")
    v.set_defaults(func=command_validate)
    cp = sub.add_parser("classify-paths")
    cp.add_argument("path", nargs="+")
    cp.set_defaults(func=command_classify_paths)
    c = sub.add_parser("classify")
    c.add_argument("--event-name", required=True)
    c.add_argument("--event-path", required=True)
    c.add_argument("--github-output")
    c.set_defaults(func=command_classify)
    r = sub.add_parser("run")
    r.add_argument("--lane", required=True)
    r.add_argument("--mode", required=True, choices=("development", "promotion", "sentinel"))
    r.add_argument("--changed-paths-json", default="[]")
    r.set_defaults(func=command_run)
    return p


def main() -> int:
    try:
        args = parser().parse_args()
        return args.func(args)
    except (FormalValidationError, jsonschema.ValidationError, OSError, subprocess.CalledProcessError, KeyError, ValueError) as exc:
        print(f"formal validation error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
