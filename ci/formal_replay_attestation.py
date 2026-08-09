#!/usr/bin/env python3
"""Content-addressed formal replay attestation utilities.

A reused receipt is evidence of a prior full formal replay. It is never reported
as a fresh Lean execution on the current transition.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable

DEFAULT_POLICY = Path("governance/formal_replay_policy.json")
RECEIPT_STATUS = "FULL_FORMAL_REPLAY_SUCCEEDED"
REUSE_STATUS = "REUSED_BIT_IDENTICAL_FORMAL_ATTESTATION"
SHA40 = re.compile(r"^[0-9a-f]{40}$")


class PolicyError(RuntimeError):
    pass


def canonical_json(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_policy(path: Path = DEFAULT_POLICY) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise PolicyError("formal replay policy schema_version must be 1")
    lanes = data.get("lanes")
    if not isinstance(lanes, dict) or not lanes:
        raise PolicyError("formal replay policy must define lanes")
    return data


def lane_policy(policy: dict, lane: str) -> dict:
    try:
        return policy["lanes"][lane]
    except KeyError as exc:
        raise PolicyError(f"unknown formal replay lane: {lane}") from exc


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False)


def git_head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD").stdout.decode().strip()


def is_ancestor(repo: Path, ancestor: str, descendant: str = "HEAD") -> bool:
    if not SHA40.fullmatch(ancestor):
        return False
    return _git(repo, "merge-base", "--is-ancestor", ancestor, descendant, check=False).returncode == 0


def tracked_closure(repo: Path, paths: Iterable[str]) -> list[dict]:
    requested = list(dict.fromkeys(paths))
    if not requested:
        raise PolicyError("formal replay closure cannot be empty")
    for rel in requested:
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts:
            raise PolicyError(f"unsafe closure path: {rel}")
    cp = _git(repo, "ls-files", "-s", "-z", "--", *requested)
    entries: list[dict] = []
    for raw in cp.stdout.split(b"\0"):
        if not raw:
            continue
        meta, path_b = raw.split(b"\t", 1)
        mode_b, blob_b, stage_b = meta.split(b" ", 2)
        if stage_b.decode() != "0":
            raise PolicyError(f"unmerged index entry in formal replay closure: {path_b!r}")
        entries.append({"mode": mode_b.decode(), "blob": blob_b.decode(), "path": path_b.decode("utf-8")})
    entries.sort(key=lambda x: x["path"])
    seen = {entry["path"] for entry in entries}
    for rel in requested:
        if rel in seen:
            continue
        prefix = rel.rstrip("/") + "/"
        if not any(path.startswith(prefix) for path in seen):
            raise PolicyError(f"declared replay input has no tracked files: {rel}")
    return entries


def digest_payload(repo: Path, policy: dict, lane: str) -> dict:
    lp = lane_policy(policy, lane)
    global_cfg = policy.get("global", {})
    closure_paths = list(global_cfg.get("inputs", [])) + list(lp.get("roots", [])) + list(lp.get("files", []))
    return {
        "algorithm": "sha256(canonical-json-v1)",
        "policy": {
            "schema_version": policy["schema_version"],
            "operation": policy.get("operation"),
            "global": global_cfg,
            "lane": lane,
            "lane_policy": lp,
        },
        "tracked_git_inputs": tracked_closure(repo, closure_paths),
    }


def compute_digest(repo: Path, policy: dict, lane: str) -> tuple[str, dict]:
    payload = digest_payload(repo, policy, lane)
    return sha256_bytes(canonical_json(payload)), payload


def parse_time(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return parsed.astimezone(dt.timezone.utc)


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def validate_receipt(repo: Path, policy: dict, lane: str, receipt: dict, *, now: dt.datetime | None = None) -> tuple[bool, str]:
    lp = lane_policy(policy, lane)
    expected_digest, _ = compute_digest(repo, policy, lane)
    required = {
        "schema_version": 1,
        "lane": lane,
        "status": RECEIPT_STATUS,
        "input_digest": expected_digest,
        "repository": policy["global"]["repository"],
        "origin_event": "push",
        "origin_ref": "refs/heads/main",
        "policy_operation": policy.get("operation"),
    }
    for key, value in required.items():
        if receipt.get(key) != value:
            return False, f"receipt_{key}_mismatch"
    origin_commit = receipt.get("origin_commit", "")
    if not SHA40.fullmatch(origin_commit):
        return False, "receipt_origin_commit_invalid"
    if not is_ancestor(repo, origin_commit):
        return False, "receipt_origin_not_ancestor"
    run_id = str(receipt.get("origin_run_id", ""))
    if not run_id.isdigit() or int(run_id) <= 0:
        return False, "receipt_origin_run_id_invalid"
    try:
        created = parse_time(str(receipt["created_at"]))
    except (KeyError, TypeError, ValueError):
        return False, "receipt_created_at_invalid"
    current = (now or now_utc()).astimezone(dt.timezone.utc)
    age = (current - created).total_seconds()
    if age < 0:
        return False, "receipt_from_future"
    if age >= float(policy["sentinel"]["reuse_max_age_hours"]) * 3600:
        return False, "sentinel_replay_due"
    if receipt.get("command") != lp.get("command"):
        return False, "receipt_command_mismatch"
    if receipt.get("proof_semantic_tcb") != lp.get("proof_semantic_tcb"):
        return False, "receipt_tcb_mismatch"
    return True, "receipt_valid_and_fresh"


def result_digest(paths: Iterable[Path]) -> str:
    records = []
    for path in paths:
        if not path.exists() or not path.is_file():
            raise PolicyError(f"result file missing: {path}")
        records.append({"path": path.as_posix(), "sha256": sha256_bytes(path.read_bytes())})
    return sha256_bytes(canonical_json(records))


def emit_receipt(repo: Path, policy: dict, lane: str, output: Path, *, origin_commit: str, origin_run_id: str, origin_run_attempt: str, origin_event: str, origin_ref: str, result_files: list[Path], created_at: dt.datetime | None = None) -> dict:
    if origin_event != "push" or origin_ref != "refs/heads/main":
        raise PolicyError("reusable receipts may be emitted only for protected-main push executions")
    if origin_commit != git_head(repo):
        raise PolicyError("receipt origin commit must equal checked-out HEAD")
    if not str(origin_run_id).isdigit() or int(origin_run_id) <= 0:
        raise PolicyError("origin run id must be a positive integer")
    digest, _ = compute_digest(repo, policy, lane)
    lp = lane_policy(policy, lane)
    receipt = {
        "schema_version": 1,
        "lane": lane,
        "status": RECEIPT_STATUS,
        "input_digest": digest,
        "repository": policy["global"]["repository"],
        "origin_commit": origin_commit,
        "origin_run_id": str(origin_run_id),
        "origin_run_attempt": str(origin_run_attempt),
        "origin_event": origin_event,
        "origin_ref": origin_ref,
        "policy_operation": policy.get("operation"),
        "command": lp.get("command"),
        "proof_semantic_tcb": lp.get("proof_semantic_tcb"),
        "result_digest": result_digest(result_files),
        "result_files": [p.as_posix() for p in result_files],
        "created_at": (created_at or now_utc()).astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def scan_forbidden(repo: Path, policy: dict, lane: str) -> list[str]:
    lp = lane_policy(policy, lane)
    patterns = [re.compile(p) for p in lp.get("forbidden_source_patterns", [])]
    if not patterns:
        return []
    findings: list[str] = []
    entries = tracked_closure(repo, lp.get("roots", []))
    for entry in entries:
        path = repo / entry["path"]
        if path.suffix != ".lean":
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            if pattern.search(text):
                findings.append(f"{entry['path']}: {pattern.pattern}")
    return findings


def check_policy(repo: Path, policy: dict) -> None:
    global_cfg = policy.get("global", {})
    for key in ("repository", "cache_namespace", "cache_action_sha", "lean_action_sha"):
        if not global_cfg.get(key):
            raise PolicyError(f"missing global policy key: {key}")
    if not SHA40.fullmatch(global_cfg["cache_action_sha"]):
        raise PolicyError("cache_action_sha must be immutable")
    if not SHA40.fullmatch(global_cfg["lean_action_sha"]):
        raise PolicyError("lean_action_sha must be immutable")
    workflow = (repo / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for sha_key in ("cache_action_sha", "lean_action_sha"):
        if global_cfg[sha_key] not in workflow:
            raise PolicyError(f"workflow does not bind {sha_key}")
    max_age = float(policy["sentinel"]["reuse_max_age_hours"])
    required = float(policy["sentinel"]["required_full_replay_within_hours"])
    if not 0 < max_age <= required:
        raise PolicyError("invalid sentinel freshness bounds")
    for lane in sorted(policy["lanes"]):
        compute_digest(repo, policy, lane)
        findings = scan_forbidden(repo, policy, lane)
        if findings:
            raise PolicyError("forbidden formal source token(s): " + "; ".join(findings))


def write_github_output(path: str | None, values: dict[str, object]) -> None:
    if not path:
        return
    with open(path, "a", encoding="utf-8") as fh:
        for key, value in values.items():
            if isinstance(value, bool):
                value = "true" if value else "false"
            fh.write(f"{key}={value}\n")


def cmd_digest(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    policy = load_policy(repo / args.policy)
    digest, payload = compute_digest(repo, policy, args.lane)
    values = {"lane": args.lane, "digest": digest, "cache_prefix": f"{policy['global']['cache_namespace']}-{args.lane}-{digest}-"}
    write_github_output(args.github_output, values)
    print(json.dumps({**values, "payload": payload}, sort_keys=True))
    return 0


def cmd_decide(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    policy = load_policy(repo / args.policy)
    receipt_path = repo / args.receipt
    if not receipt_path.exists():
        reuse, reason = False, "receipt_missing"
    else:
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            reuse, reason = validate_receipt(repo, policy, args.lane, receipt, now=parse_time(args.now) if args.now else None)
        except Exception as exc:
            reuse, reason = False, f"receipt_invalid:{type(exc).__name__}"
    values = {"reuse": reuse, "reason": reason, "status": REUSE_STATUS if reuse else "FULL_FORMAL_REPLAY_REQUIRED"}
    write_github_output(args.github_output, values)
    print(json.dumps(values, sort_keys=True))
    return 0


def cmd_emit(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    policy = load_policy(repo / args.policy)
    receipt = emit_receipt(repo, policy, args.lane, repo / args.output, origin_commit=args.origin_commit, origin_run_id=args.origin_run_id, origin_run_attempt=args.origin_run_attempt, origin_event=args.origin_event, origin_ref=args.origin_ref, result_files=[repo / p for p in args.result_file])
    print(json.dumps(receipt, sort_keys=True))
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    policy = load_policy(repo / args.policy)
    check_policy(repo, policy)
    print("formal replay content-addressing policy: valid")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=".")
    p.add_argument("--policy", default=str(DEFAULT_POLICY))
    sub = p.add_subparsers(dest="command", required=True)
    d = sub.add_parser("digest")
    d.add_argument("--lane", required=True)
    d.add_argument("--github-output")
    d.set_defaults(func=cmd_digest)
    c = sub.add_parser("decide")
    c.add_argument("--lane", required=True)
    c.add_argument("--receipt", required=True)
    c.add_argument("--now")
    c.add_argument("--github-output")
    c.set_defaults(func=cmd_decide)
    e = sub.add_parser("emit-receipt")
    e.add_argument("--lane", required=True)
    e.add_argument("--output", required=True)
    e.add_argument("--origin-commit", required=True)
    e.add_argument("--origin-run-id", required=True)
    e.add_argument("--origin-run-attempt", default="1")
    e.add_argument("--origin-event", required=True)
    e.add_argument("--origin-ref", required=True)
    e.add_argument("--result-file", action="append", default=[])
    e.set_defaults(func=cmd_emit)
    ch = sub.add_parser("check-policy")
    ch.set_defaults(func=cmd_check)
    return p


def main() -> int:
    try:
        args = parser().parse_args()
        return args.func(args)
    except (PolicyError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"formal replay attestation error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
