#!/usr/bin/env python3
"""Deterministic advisory operator index over retained PRVSR archive bundles."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.parse
from pathlib import Path
from typing import Any

from autonomy_github import AutonomyError, Client
import pr_visual_status_transport as transport

ALLOWED_REPOSITORY = "grandchallenge/MATH-PROGRAMME"
ARCHIVE_BRANCH_PREFIX = "prvsr-advisory-archive/pr-"
ARCHIVE_REF_PREFIX = f"refs/heads/{ARCHIVE_BRANCH_PREFIX}"
INDEX_BRANCH = "prvsr-operator-index"
INDEX_ROOT = "governance/pr_visual_status_operator"
MANIFEST_PATH = f"{INDEX_ROOT}/latest.json"
PROJECT_PROJECTION_PATH = f"{INDEX_ROOT}/project-triage.json"
MANIFEST_SCHEMA_VERSION = "0.1.0-pilot"
GENERATOR_VERSION = "0.1.0-pilot"
AUTHORITY_BOUNDARY = {
    "advisory_only": True,
    "visual_is_authoritative": False,
    "new_merge_gate": False,
    "project_mutation_active": False,
    "project_write_permission_requested": False,
    "propagation_authority_created": False,
}
ARCHIVE_MESSAGE = re.compile(
    r"^Archive advisory PRVSR report (?P<report_id>[A-Za-z0-9._-]+)$"
)
REF_RE = re.compile(
    r"^refs/heads/prvsr-advisory-archive/pr-(?P<pr>[1-9][0-9]*)$"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ENTRY_KEYS = {
    "pr_number",
    "title",
    "pr_url",
    "exact_head_sha",
    "operative_state",
    "freshness",
    "required_checks",
    "independent_review",
    "human_steward",
    "integration",
    "open_blockers",
    "report_id",
    "observed_at",
    "source_snapshot_sha256",
    "archive_branch",
    "archive_commit_sha",
    "archive_dir",
    "report_url",
    "text_url",
    "receipt_url",
    "archive_url",
}


class OperatorSurfaceError(RuntimeError):
    pass


class OperatorSurfaceConflict(OperatorSurfaceError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _quoted_ref(ref: str) -> str:
    return urllib.parse.quote(ref, safe="")


def _content_bytes(client: Client, repo: str, path: str, ref: str) -> bytes:
    value = client.get(
        f"/repos/{repo}/contents/{urllib.parse.quote(path, safe='/')}"
        f"?ref={_quoted_ref(ref)}"
    )
    if not isinstance(value, dict):
        raise OperatorSurfaceError(f"content response for {path} is not an object")
    try:
        data = base64.b64decode(value["content"])
    except (KeyError, TypeError, ValueError) as exc:
        raise OperatorSurfaceError(f"content response for {path} is invalid") from exc
    return data


def _optional_content_bytes(
    client: Client, repo: str, path: str, ref: str
) -> bytes | None:
    try:
        return _content_bytes(client, repo, path, ref)
    except AutonomyError as exc:
        if " 404 " in str(exc):
            return None
        raise


def _branch_tip(client: Client, repo: str, branch: str) -> str | None:
    try:
        value = client.get(
            f"/repos/{repo}/branches/{urllib.parse.quote(branch, safe='')}"
        )
    except AutonomyError as exc:
        if " 404 " in str(exc):
            return None
        raise
    sha = str((value or {}).get("commit", {}).get("sha") or "")
    if not SHA_RE.fullmatch(sha):
        raise OperatorSurfaceError(f"branch {branch} has invalid tip")
    return sha


def list_archive_refs(client: Client, repo: str) -> list[dict[str, Any]]:
    value = client.get(
        f"/repos/{repo}/git/matching-refs/heads/"
        f"{urllib.parse.quote(ARCHIVE_BRANCH_PREFIX, safe='/')}"
    )
    if not isinstance(value, list):
        raise OperatorSurfaceError("archive ref listing is not an array")
    refs: list[dict[str, Any]] = []
    for item in value:
        ref = str((item or {}).get("ref") or "")
        match = REF_RE.fullmatch(ref)
        if not match:
            continue
        sha = str((item or {}).get("object", {}).get("sha") or "")
        if not SHA_RE.fullmatch(sha):
            raise OperatorSurfaceError(f"archive ref {ref} has invalid tip")
        refs.append(
            {
                "pr_number": int(match.group("pr")),
                "archive_branch": ref.removeprefix("refs/heads/"),
                "archive_commit_sha": sha,
            }
        )
    refs.sort(key=lambda item: int(item["pr_number"]))
    return refs


def _tip_report_id(client: Client, repo: str, tip_sha: str) -> str | None:
    value = client.get(f"/repos/{repo}/git/commits/{tip_sha}")
    message = str((value or {}).get("message") or "").splitlines()[0].strip()
    match = ARCHIVE_MESSAGE.fullmatch(message)
    return match.group("report_id") if match else None


def _load_verified_bundle(
    client: Client,
    repo: str,
    pr_number: int,
    branch: str,
    archive_commit_sha: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    report_id = _tip_report_id(client, repo, archive_commit_sha)
    if report_id is None:
        raise OperatorSurfaceError("archive branch tip is not a retained report commit")
    archive_dir = f"{transport.ARCHIVE_ROOT}/{repo}/pr-{pr_number}/{report_id}"
    with tempfile.TemporaryDirectory() as tmp:
        bundle_dir = Path(tmp) / report_id
        bundle_dir.mkdir()
        for name in ("report.json", "report.txt", "report.svg", "receipt.json"):
            (bundle_dir / name).write_bytes(
                _content_bytes(client, repo, f"{archive_dir}/{name}", branch)
            )
        receipt = transport.verify_archive_bundle(bundle_dir)
        try:
            report = json.loads(
                (bundle_dir / "report.json").read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            raise OperatorSurfaceError(
                "verified report JSON could not be decoded"
            ) from exc

    if int(report["identity"]["pr_number"]) != pr_number:
        raise OperatorSurfaceError("archive branch PR identity mismatch")
    if str(report["identity"]["repository"]) != repo:
        raise OperatorSurfaceError("archive branch repository identity mismatch")
    if str(receipt["report_id"]) != report_id:
        raise OperatorSurfaceError("archive tip report identity mismatch")
    if str(receipt["archive_dir"]) != archive_dir:
        raise OperatorSurfaceError("archive receipt directory mismatch")
    return report, receipt


def _entry_from_bundle(
    repo: str,
    branch: str,
    archive_commit_sha: str,
    report: dict[str, Any],
    receipt: dict[str, Any],
) -> dict[str, Any]:
    identity = report["identity"]
    exact_head = str(identity["exact_head_sha"])
    required = [item for item in report["checks"] if item.get("required") is True]
    successful = sum(
        1
        for item in required
        if item.get("status") == "completed"
        and item.get("conclusion") == "success"
        and item.get("head_sha") == exact_head
    )
    open_blockers = [
        item for item in report["blockers"] if item.get("status") == "OPEN"
    ]
    pr_number = int(identity["pr_number"])
    archive_dir = str(receipt["archive_dir"])
    report_id = str(report["report_id"])
    github_base = f"https://github.com/{repo}"
    blob_base = f"{github_base}/blob/{branch}/{archive_dir}"
    return {
        "pr_number": pr_number,
        "title": str(identity["title"]),
        "pr_url": f"{github_base}/pull/{pr_number}",
        "exact_head_sha": exact_head,
        "operative_state": str(report["derived"]["operative_state"]),
        "freshness": str(report["derived"]["freshness"]),
        "required_checks": {
            "successful": successful,
            "total": len(required),
        },
        "independent_review": {
            "required": bool(report["authority"]["independent_review"]["required"]),
            "state": str(report["authority"]["independent_review"]["state"]),
            "actor": report["authority"]["independent_review"]["actor"],
        },
        "human_steward": {
            "required": bool(report["authority"]["human_steward"]["required"]),
            "state": str(report["authority"]["human_steward"]["state"]),
            "actor": report["authority"]["human_steward"]["actor"],
        },
        "integration": {
            "merge_state": str(report["integration"]["merge_state"]),
            "readback_state": str(
                report["integration"]["protected_readback"]["state"]
            ),
        },
        "open_blockers": len(open_blockers),
        "report_id": report_id,
        "observed_at": str(report["provenance"]["observed_at"]),
        "source_snapshot_sha256": str(
            report["provenance"]["source_snapshot_sha256"]
        ),
        "archive_branch": branch,
        "archive_commit_sha": archive_commit_sha,
        "archive_dir": archive_dir,
        "report_url": f"{blob_base}/report.svg",
        "text_url": f"{blob_base}/report.txt",
        "receipt_url": f"{blob_base}/receipt.json",
        "archive_url": f"{github_base}/tree/{branch}/{archive_dir}",
    }


def _manifest_digest_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": manifest["schema_version"],
        "generator_version": manifest["generator_version"],
        "repository": manifest["repository"],
        "as_of": manifest["as_of"],
        "entries": manifest["entries"],
        "errors": manifest["errors"],
        "authority_boundary": manifest["authority_boundary"],
    }


def seal_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    sealed = json.loads(json.dumps(manifest))
    sealed["source_set_sha256"] = sha256_bytes(
        canonical_bytes(_manifest_digest_payload(sealed))
    )
    return sealed


def validate_manifest(
    value: Any, repo: str = ALLOWED_REPOSITORY
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise OperatorSurfaceError("operator manifest must be an object")
    required_top = {
        "schema_version",
        "generator_version",
        "repository",
        "as_of",
        "source_set_sha256",
        "entries",
        "errors",
        "authority_boundary",
    }
    if set(value) != required_top:
        raise OperatorSurfaceError("operator manifest top-level shape mismatch")
    if value["schema_version"] != MANIFEST_SCHEMA_VERSION:
        raise OperatorSurfaceError("operator manifest schema version mismatch")
    if value["generator_version"] != GENERATOR_VERSION:
        raise OperatorSurfaceError("operator manifest generator version mismatch")
    if value["repository"] != repo:
        raise OperatorSurfaceError("operator manifest repository mismatch")
    if value["authority_boundary"] != AUTHORITY_BOUNDARY:
        raise OperatorSurfaceError("operator manifest authority boundary mismatch")
    if not isinstance(value["entries"], list) or not isinstance(value["errors"], list):
        raise OperatorSurfaceError("operator manifest entries/errors must be arrays")
    if value["as_of"] is not None and not isinstance(value["as_of"], str):
        raise OperatorSurfaceError("operator manifest as_of must be a timestamp or null")
    numbers: list[int] = []
    for entry in value["entries"]:
        if not isinstance(entry, dict) or set(entry) != ENTRY_KEYS:
            raise OperatorSurfaceError("operator manifest entry shape mismatch")
        pr = entry.get("pr_number")
        archive_sha = str(entry.get("archive_commit_sha") or "")
        exact_head = str(entry.get("exact_head_sha") or "")
        source_digest = str(entry.get("source_snapshot_sha256") or "")
        if not isinstance(pr, int) or pr <= 0:
            raise OperatorSurfaceError("operator manifest PR identity is invalid")
        if not SHA_RE.fullmatch(archive_sha) or not SHA_RE.fullmatch(exact_head):
            raise OperatorSurfaceError("operator manifest SHA identity is invalid")
        if not re.fullmatch(r"[0-9a-f]{64}", source_digest):
            raise OperatorSurfaceError("operator manifest source digest is invalid")
        if entry.get("archive_branch") != f"{ARCHIVE_BRANCH_PREFIX}{pr}":
            raise OperatorSurfaceError(
                "operator manifest archive branch identity mismatch"
            )
        checks = entry.get("required_checks")
        if (
            not isinstance(checks, dict)
            or set(checks) != {"successful", "total"}
            or not isinstance(checks["successful"], int)
            or not isinstance(checks["total"], int)
            or checks["successful"] < 0
            or checks["total"] < checks["successful"]
        ):
            raise OperatorSurfaceError(
                "operator manifest required-check summary is invalid"
            )
        if (
            not isinstance(entry.get("open_blockers"), int)
            or entry["open_blockers"] < 0
        ):
            raise OperatorSurfaceError("operator manifest blocker count is invalid")
        numbers.append(pr)
    if numbers != sorted(numbers) or len(numbers) != len(set(numbers)):
        raise OperatorSurfaceError(
            "operator manifest entries are not unique/sorted"
        )
    expected = sha256_bytes(canonical_bytes(_manifest_digest_payload(value)))
    if value["source_set_sha256"] != expected:
        raise OperatorSurfaceError("operator manifest source-set digest mismatch")
    return value


def _load_cached_manifest(client: Client, repo: str) -> dict[str, Any] | None:
    raw = _optional_content_bytes(client, repo, MANIFEST_PATH, INDEX_BRANCH)
    if raw is None:
        return None
    try:
        value = json.loads(raw)
        return validate_manifest(value, repo)
    except (json.JSONDecodeError, OperatorSurfaceError) as exc:
        print(f"PRVSR_OPERATOR_CACHE_IGNORED: {exc}", file=sys.stderr)
        return None


def build_manifest(client: Client, repo: str) -> dict[str, Any]:
    if repo != ALLOWED_REPOSITORY:
        raise OperatorSurfaceError(
            "operator surface is outside bounded repository authority"
        )
    refs = list_archive_refs(client, repo)
    cached = _load_cached_manifest(client, repo)
    cache_by_pr = {
        int(item["pr_number"]): item for item in (cached or {}).get("entries", [])
    }
    entries: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for ref in refs:
        pr_number = int(ref["pr_number"])
        branch = str(ref["archive_branch"])
        tip = str(ref["archive_commit_sha"])
        cached_entry = cache_by_pr.get(pr_number)
        if cached_entry and cached_entry.get("archive_commit_sha") == tip:
            entries.append(cached_entry)
            continue
        try:
            report, receipt = _load_verified_bundle(
                client, repo, pr_number, branch, tip
            )
            entries.append(
                _entry_from_bundle(repo, branch, tip, report, receipt)
            )
        except AutonomyError:
            raise
        except (
            OperatorSurfaceError,
            transport.TransportError,
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            print(
                f"PRVSR_OPERATOR_UNVERIFIABLE pr={pr_number} "
                f"branch={branch} tip={tip}: {exc}",
                file=sys.stderr,
            )
            errors.append(
                {
                    "pr_number": pr_number,
                    "archive_branch": branch,
                    "archive_commit_sha": tip,
                    "code": "UNVERIFIABLE_RETAINED_STATE",
                }
            )

    entries.sort(key=lambda item: int(item["pr_number"]))
    errors.sort(key=lambda item: int(item["pr_number"]))
    observed = sorted(str(item["observed_at"]) for item in entries)
    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "repository": repo,
        "as_of": observed[-1] if observed else None,
        "entries": entries,
        "errors": errors,
        "authority_boundary": dict(AUTHORITY_BOUNDARY),
    }
    return seal_manifest(manifest)


def build_project_projection(manifest: dict[str, Any]) -> dict[str, Any]:
    validate_manifest(manifest, str(manifest["repository"]))
    items = []
    for entry in manifest["entries"]:
        checks = entry["required_checks"]
        items.append(
            {
                "content_url": entry["pr_url"],
                "pr_number": entry["pr_number"],
                "title": entry["title"],
                "fields": {
                    "PRVSR State": entry["operative_state"],
                    "Freshness": entry["freshness"],
                    "Required Checks": (
                        f"{checks['successful']}/{checks['total']}"
                    ),
                    "Independent Review": entry["independent_review"]["state"],
                    "Human Steward": entry["human_steward"]["state"],
                    "Merge": entry["integration"]["merge_state"],
                    "Readback": entry["integration"]["readback_state"],
                    "Open Blockers": entry["open_blockers"],
                    "Exact Head": entry["exact_head_sha"],
                    "Report ID": entry["report_id"],
                },
            }
        )
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "repository": manifest["repository"],
        "source_manifest_sha256": manifest["source_set_sha256"],
        "active": False,
        "authority_boundary": {
            "advisory_only": True,
            "project_mutation_active": False,
            "project_write_permission_requested": False,
            "requires_separate_authorization_to_activate": True,
        },
        "items": items,
    }


def _ensure_index_branch(client: Client, repo: str) -> str:
    current = _branch_tip(client, repo, INDEX_BRANCH)
    if current is not None:
        return current
    main = _branch_tip(client, repo, "main")
    if main is None:
        raise OperatorSurfaceError("cannot seed operator index without main")
    try:
        client.post(
            f"/repos/{repo}/git/refs",
            {"ref": f"refs/heads/{INDEX_BRANCH}", "sha": main},
        )
    except AutonomyError as exc:
        if " 422 " not in str(exc):
            raise
    current = _branch_tip(client, repo, INDEX_BRANCH)
    if current is None:
        raise OperatorSurfaceError(
            "operator index branch creation readback failed"
        )
    return current


def _current_index_bytes(client: Client, repo: str, path: str) -> bytes | None:
    return _optional_content_bytes(client, repo, path, INDEX_BRANCH)


def publish_index(
    client: Client,
    repo: str,
    manifest: dict[str, Any],
    project_projection: dict[str, Any],
) -> dict[str, Any]:
    validate_manifest(manifest, repo)
    manifest_bytes = canonical_bytes(manifest)
    project_bytes = canonical_bytes(project_projection)
    parent = _ensure_index_branch(client, repo)

    current_manifest = _current_index_bytes(client, repo, MANIFEST_PATH)
    current_project = _current_index_bytes(
        client, repo, PROJECT_PROJECTION_PATH
    )
    if current_manifest == manifest_bytes and current_project == project_bytes:
        return {
            "changed": False,
            "branch": INDEX_BRANCH,
            "commit_sha": parent,
            "manifest_sha256": sha256_bytes(manifest_bytes),
            "project_projection_sha256": sha256_bytes(project_bytes),
        }

    parent_commit = client.get(f"/repos/{repo}/git/commits/{parent}")
    base_tree = str((parent_commit or {}).get("tree", {}).get("sha") or "")
    if not SHA_RE.fullmatch(base_tree):
        raise OperatorSurfaceError("operator index parent has invalid tree")
    tree_entries = []
    for path, data in (
        (MANIFEST_PATH, manifest_bytes),
        (PROJECT_PROJECTION_PATH, project_bytes),
    ):
        blob = client.post(
            f"/repos/{repo}/git/blobs",
            {
                "content": base64.b64encode(data).decode("ascii"),
                "encoding": "base64",
            },
        )
        tree_entries.append(
            {
                "path": path,
                "mode": "100644",
                "type": "blob",
                "sha": blob["sha"],
            }
        )
    tree = client.post(
        f"/repos/{repo}/git/trees",
        {"base_tree": base_tree, "tree": tree_entries},
    )
    new_commit = client.post(
        f"/repos/{repo}/git/commits",
        {
            "message": (
                f"Refresh PRVSR operator index "
                f"{manifest['source_set_sha256'][:12]}"
            ),
            "tree": tree["sha"],
            "parents": [parent],
        },
    )
    try:
        client.patch(
            f"/repos/{repo}/git/refs/heads/{INDEX_BRANCH}",
            {"sha": new_commit["sha"], "force": False},
        )
    except AutonomyError as exc:
        if " 409 " in str(exc) or " 422 " in str(exc):
            raise OperatorSurfaceConflict(
                "operator index moved during refresh"
            ) from exc
        raise
    readback = _branch_tip(client, repo, INDEX_BRANCH)
    if readback != str(new_commit["sha"]):
        raise OperatorSurfaceError("operator index commit readback mismatch")
    return {
        "changed": True,
        "branch": INDEX_BRANCH,
        "commit_sha": readback,
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "project_projection_sha256": sha256_bytes(project_bytes),
    }


def refresh(client: Client, repo: str, attempts: int = 3) -> dict[str, Any]:
    for attempt in range(1, attempts + 1):
        manifest = build_manifest(client, repo)
        projection = build_project_projection(manifest)
        try:
            publication = publish_index(client, repo, manifest, projection)
        except OperatorSurfaceConflict:
            if attempt == attempts:
                raise
            continue
        return {
            "manifest": {
                "entries": len(manifest["entries"]),
                "errors": len(manifest["errors"]),
                "as_of": manifest["as_of"],
                "source_set_sha256": manifest["source_set_sha256"],
            },
            "publication": publication,
            "authority_boundary": dict(AUTHORITY_BOUNDARY),
        }
    raise OperatorSurfaceError("operator index refresh attempts exhausted")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--summary")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.repo != ALLOWED_REPOSITORY:
        raise OperatorSurfaceError(
            "operator surface is outside bounded repository authority"
        )
    if args.attempts < 1 or args.attempts > 5:
        raise OperatorSurfaceError("attempts must be between 1 and 5")
    token = os.environ.get("GITHUB_PUBLISH_TOKEN", "")
    result = refresh(Client(token), args.repo, args.attempts)
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.summary:
        Path(args.summary).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
