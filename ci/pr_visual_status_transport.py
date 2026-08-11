#!/usr/bin/env python3
"""Deterministic non-mutating transport and durable archive contract for ADR-0019."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import pr_visual_status_policy as policy

ARCHIVE_SCHEMA_VERSION = "1.0.0"
TRANSPORT_VERSION = "0.1.0-pilot"
ARCHIVE_ROOT = "governance/pr_visual_status_archive"
_SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9._-]+$")


class TransportError(RuntimeError):
    """Raised when archive or transport integrity cannot be established."""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _safe_component(value: str, field: str) -> str:
    if not isinstance(value, str) or not _SAFE_COMPONENT.fullmatch(value):
        raise TransportError(f"{field} contains unsafe path characters")
    if value in {".", ".."}:
        raise TransportError(f"{field} is not a safe path component")
    return value


def archive_relative_dir(report: dict[str, Any]) -> str:
    policy.verify_report(report)
    repo = report["identity"]["repository"]
    owner, name = repo.split("/", 1)
    owner = _safe_component(owner, "repository owner")
    name = _safe_component(name, "repository name")
    report_id = _safe_component(report["report_id"], "report_id")
    pr_number = int(report["identity"]["pr_number"])
    return f"{ARCHIVE_ROOT}/{owner}/{name}/pr-{pr_number}/{report_id}"


def assert_target_head_unchanged(before_sha: str, after_sha: str, exact_sha: str) -> None:
    for label, sha in (
        ("target head before", before_sha),
        ("target head after", after_sha),
        ("report exact head", exact_sha),
    ):
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise TransportError(f"{label} must be a full lowercase 40-character SHA")
    if before_sha != exact_sha:
        raise TransportError("target head before transport does not equal report exact head")
    if after_sha != before_sha:
        raise TransportError("target PR head changed during archive/transport operation")


def build_archive_bundle(
    report: dict[str, Any],
    *,
    target_head_before: str,
    target_head_after: str,
) -> dict[str, bytes]:
    policy.verify_report(report)
    exact_sha = report["identity"]["exact_head_sha"]
    assert_target_head_unchanged(target_head_before, target_head_after, exact_sha)

    report_bytes = _json_bytes(report)
    text_bytes = policy.render_text(report).encode("utf-8")
    svg_bytes = policy.render_svg(report).encode("utf-8")
    archive_dir = archive_relative_dir(report)

    artifacts = {
        "report.json": report_bytes,
        "report.txt": text_bytes,
        "report.svg": svg_bytes,
    }
    receipt = {
        "schema_version": ARCHIVE_SCHEMA_VERSION,
        "transport_version": TRANSPORT_VERSION,
        "report_id": report["report_id"],
        "repository": report["identity"]["repository"],
        "pr_number": report["identity"]["pr_number"],
        "exact_head_sha": exact_sha,
        "target_head_before": target_head_before,
        "target_head_after": target_head_after,
        "target_pr_head_mutated": False,
        "archive_dir": archive_dir,
        "source_snapshot_sha256": report["provenance"]["source_snapshot_sha256"],
        "operative_state": report["derived"]["operative_state"],
        "freshness": report["derived"]["freshness"],
        "artifacts": {
            name: {
                "path": f"{archive_dir}/{name}",
                "sha256": _sha256_bytes(data),
            }
            for name, data in artifacts.items()
        },
        "authority_boundary": {
            "advisory_only": True,
            "visual_is_authoritative": False,
            "new_merge_gate": False,
            "propagation_authority_created": False,
        },
    }
    receipt_bytes = _json_bytes(receipt)
    return {**artifacts, "receipt.json": receipt_bytes}


def _validate_receipt_metadata(receipt: dict[str, Any]) -> None:
    if not isinstance(receipt, dict):
        raise TransportError("archive receipt must be an object")
    if receipt.get("schema_version") != ARCHIVE_SCHEMA_VERSION:
        raise TransportError("archive receipt schema version mismatch")
    if receipt.get("transport_version") != TRANSPORT_VERSION:
        raise TransportError("archive transport version mismatch")
    if receipt.get("target_pr_head_mutated") is not False:
        raise TransportError("archive receipt does not preserve non-mutating target invariant")
    assert_target_head_unchanged(
        receipt.get("target_head_before"),
        receipt.get("target_head_after"),
        receipt.get("exact_head_sha"),
    )
    expected_boundary = {
        "advisory_only": True,
        "visual_is_authoritative": False,
        "new_merge_gate": False,
        "propagation_authority_created": False,
    }
    if receipt.get("authority_boundary") != expected_boundary:
        raise TransportError("archive receipt authority boundary is invalid")


def verify_archive_bundle(bundle_dir: Path) -> dict[str, Any]:
    receipt_path = bundle_dir / "receipt.json"
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TransportError(f"cannot read archive receipt: {exc}") from exc
    _validate_receipt_metadata(receipt)
    artifacts = receipt.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != {
        "report.json",
        "report.txt",
        "report.svg",
    }:
        raise TransportError("archive receipt artifact set is invalid")
    for name, metadata in artifacts.items():
        if not isinstance(metadata, dict):
            raise TransportError(f"archive metadata for {name} is invalid")
        artifact_path = bundle_dir / name
        try:
            data = artifact_path.read_bytes()
        except OSError as exc:
            raise TransportError(f"cannot read archived artifact {name}: {exc}") from exc
        if metadata.get("sha256") != _sha256_bytes(data):
            raise TransportError(f"archived artifact digest mismatch: {name}")

    report = json.loads((bundle_dir / "report.json").read_text(encoding="utf-8"))
    policy.verify_report(report)
    expected_dir = archive_relative_dir(report)
    if receipt.get("archive_dir") != expected_dir:
        raise TransportError("archive receipt path does not match report identity")
    if receipt.get("source_snapshot_sha256") != report["provenance"]["source_snapshot_sha256"]:
        raise TransportError("archive receipt source digest does not match report")
    if receipt.get("operative_state") != report["derived"]["operative_state"]:
        raise TransportError("archive receipt operative state does not match report")
    if receipt.get("freshness") != report["derived"]["freshness"]:
        raise TransportError("archive receipt freshness does not match report")
    return receipt


def render_pr_comment(receipt: dict[str, Any]) -> str:
    _validate_receipt_metadata(receipt)
    exact = receipt["exact_head_sha"]
    digest = receipt["source_snapshot_sha256"]
    archive_dir = receipt["archive_dir"]
    state = receipt["operative_state"]
    freshness = receipt["freshness"]
    report_id = receipt["report_id"]
    return (
        f"## Advisory visual status report — `{report_id}`\n\n"
        f"- operative state: `{state}`\n"
        f"- freshness: `{freshness}`\n"
        f"- exact PR head: `{exact}`\n"
        f"- source snapshot SHA-256: `{digest}`\n"
        f"- durable archive: `{archive_dir}/`\n\n"
        "This is a deterministic, derived, advisory presentation of governed source state. "
        "It does not create review, authorization, merge, certification, or propagation authority. "
        "The target PR head was not modified by archive or transport generation.\n"
    )


def write_archive_bundle(
    report: dict[str, Any],
    output_root: Path,
    *,
    target_head_before: str,
    target_head_after: str,
) -> Path:
    bundle = build_archive_bundle(
        report,
        target_head_before=target_head_before,
        target_head_after=target_head_after,
    )
    relative_dir = Path(archive_relative_dir(report))
    bundle_dir = output_root / relative_dir
    bundle_dir.mkdir(parents=True, exist_ok=True)
    for name, data in bundle.items():
        (bundle_dir / name).write_bytes(data)
    verify_archive_bundle(bundle_dir)
    return bundle_dir


def _load_report(path: str) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TransportError(f"cannot read report: {exc}") from exc
    if not isinstance(value, dict):
        raise TransportError("report JSON must be an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    archive = sub.add_parser("archive")
    archive.add_argument("report")
    archive.add_argument("--output-root", default=".")
    archive.add_argument("--target-head-before", required=True)
    archive.add_argument("--target-head-after", required=True)

    verify = sub.add_parser("verify")
    verify.add_argument("bundle_dir")

    comment = sub.add_parser("comment")
    comment.add_argument("receipt")

    args = parser.parse_args()
    try:
        if args.command == "archive":
            report = _load_report(args.report)
            path = write_archive_bundle(
                report,
                Path(args.output_root),
                target_head_before=args.target_head_before,
                target_head_after=args.target_head_after,
            )
            print(path.as_posix())
            return 0
        if args.command == "verify":
            verify_archive_bundle(Path(args.bundle_dir))
            print("PR visual status archive: verified")
            return 0
        receipt = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
        print(render_pr_comment(receipt), end="")
        return 0
    except (OSError, json.JSONDecodeError, policy.ReportError, TransportError) as exc:
        print(f"PR visual status transport error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
