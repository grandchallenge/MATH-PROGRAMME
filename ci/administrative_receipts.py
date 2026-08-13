from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any, Callable

import administrative_automation as aa

GitRunner = Callable[[list[str]], str]
SYNTHETIC_PULL_REQUEST_MERGE_RE = re.compile(
    r"^Merge ([0-9a-f]{40}) into ([0-9a-f]{40})$"
)
DEFAULT_PULL_REQUEST_MERGE_RE = re.compile(
    r"^Merge pull request #(\d+) from [^\n]+(?:\n\n.*)?$",
    re.DOTALL,
)
DERIVE_RECORD_SHA256 = "DERIVE_FROM_IMMUTABLE_RECORD"


def default_git_runner(args: list[str]) -> str:
    completed = subprocess.run(["git", *args], check=True, text=True, capture_output=True)
    return completed.stdout.strip()


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise aa.AutomationError(message)


def protected_ancestor(root: Path, ancestor: str, head_sha: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, head_sha],
        cwd=root,
        check=False,
    )
    return completed.returncode == 0


def normalize_legacy_bootstrap_receipt(
    root: Path,
    receipt: dict[str, Any],
    head_sha: str,
) -> dict[str, Any]:
    merge_commit = str(receipt.get("merge_commit", ""))
    if not aa.SHA_RE.fullmatch(merge_commit):
        raise aa.AutomationError("bootstrap receipt merge commit invalid")
    if not protected_ancestor(root, merge_commit, head_sha):
        raise aa.AutomationError("bootstrap receipt is not ancestral to protected head")
    return dict(receipt)


def normalize_repaired_bootstrap_receipt_476(
    root: Path,
    receipt: dict[str, Any],
    head_sha: str,
    git_runner: GitRunner,
) -> dict[str, Any]:
    repair_id = "MP-ADMIN-RECEIPT-REPAIR-476-001"
    repair_record_path = (
        "governance/administrative_receipt_repairs/"
        "MP-ADMIN-RECEIPT-REPAIR-476-001.json"
    )
    record_path = (
        "governance/administrative_reviews/"
        "MP-ADMIN-ADMINISTRATIVE-REVIEW-2026-08-13-001.json"
    )
    reviewed_head = "1eb3c2cf8375beecc6d84d788ac891402b33757f"
    merge_commit = "7c84b9bf19a1f3e2407860d82965e98fc49512db"
    expected_parents = [
        "cd0d91b4c1b9e3c3ff2eced0c79c104d97af66e2",
        reviewed_head,
    ]
    expected_message = (
        "Merge PR #476: MP-ADMIN-ADMINISTRATIVE-REVIEW-2026-08-13-001\n\n"
        "Exact-head protected administrative merge.\n\n"
        "Candidate head: 1eb3c2cf8375beecc6d84d788ac891402b33757f\n"
        "Protected base: cd0d91b4c1b9e3c3ff2eced0c79c104d97af66e2\n"
        "Independent approval: jimsteeg review 4923702298\n"
        "Human Steward disposition: issue comment 5276363695\n\n"
        "No mathematical, certification, activation, external-claim, direct-push, "
        "or bypass authority is asserted."
    )

    require(receipt.get("repair_id") == repair_id, "administrative-review repair identity drift")
    require(
        receipt.get("repair_record_path") == repair_record_path,
        "administrative-review repair record path drift",
    )
    require(".." not in repair_record_path and not repair_record_path.startswith("/"), "unsafe repair record path")
    repair_path = root / repair_record_path
    require(repair_path.is_file(), "administrative-review repair record missing")
    repair = aa.load_json(repair_path)

    require(repair.get("schema_version") == "1.0.0", "administrative-review repair schema drift")
    require(repair.get("repair_id") == repair_id, "administrative-review repair record identity mismatch")
    require(repair.get("control_id") == "MP-ADMIN-MAINT-001", "administrative-review repair control drift")
    require(repair.get("repository") == "grandchallenge/MATH-PROGRAMME", "administrative-review repair repository drift")
    require(repair.get("source_issue") == 475, "administrative-review repair source issue drift")
    require(
        repair.get("occurrence_key") == "administrative_review:2026-08-13T01:21:00Z",
        "administrative-review repair occurrence drift",
    )

    procedure_id = str(receipt.get("procedure_id", ""))
    scheduled_due_at = aa.iso_z(aa.parse_datetime(str(receipt.get("scheduled_due_at", ""))))
    require(procedure_id == repair.get("procedure_id") == "administrative_review", "administrative-review repair procedure drift")
    require(
        scheduled_due_at
        == aa.iso_z(aa.parse_datetime(str(repair.get("scheduled_due_at", ""))))
        == "2026-08-13T01:21:00Z",
        "administrative-review repair scheduled locus drift",
    )

    record = repair.get("record", {})
    require(receipt.get("record_path") == record.get("path") == record_path, "administrative-review record path drift")
    path = root / record_path
    require(path.is_file(), "administrative-review protected record missing")
    require(record.get("record_id") == "MP-ADMIN-ADMINISTRATIVE-REVIEW-2026-08-13-001", "administrative-review record identity drift")
    require(record.get("status") == "COMPLETE_AUTONOMOUS", "administrative-review record status drift")
    expected_blob = "608c973a61312a4fe4ef8b269c2788d27c650e1f"
    require(receipt.get("record_git_blob") == record.get("git_blob") == expected_blob, "administrative-review immutable record blob drift")
    require(git_blob_sha(path) == expected_blob, "administrative-review immutable record content drift")
    require(receipt.get("record_sha256") == DERIVE_RECORD_SHA256, "administrative-review repair must derive SHA-256")
    record_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()

    pull = repair.get("pull_request", {})
    require(receipt.get("pull_request") == pull.get("number") == 476, "administrative-review PR drift")
    require(receipt.get("reviewed_head") == pull.get("head") == reviewed_head, "administrative-review exact head drift")
    require(receipt.get("merge_commit") == repair.get("merge", {}).get("commit") == merge_commit, "administrative-review merge commit drift")
    disposition = "HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE"
    require(receipt.get("disposition") == pull.get("disposition", {}).get("token") == disposition, "administrative-review disposition drift")

    require(receipt.get("merge_parents") == repair.get("merge", {}).get("parents") == expected_parents, "administrative-review merge parent drift")
    observed_parents = git_runner(["show", "-s", "--format=%P", merge_commit]).split()
    require(observed_parents == expected_parents, "administrative-review merge parent relationship invalid")
    introduction = git_runner(["log", "--first-parent", "--diff-filter=A", "--format=%H", "-1", head_sha, "--", record_path])
    require(introduction == merge_commit, "administrative-review record introduction drift")
    require(protected_ancestor(root, merge_commit, head_sha), "administrative-review merge is not protected-ancestral")

    observed_message = git_runner(["show", "-s", "--format=%B", merge_commit]).strip()
    require(observed_message == repair.get("merge", {}).get("message") == expected_message, "administrative-review malformed message drift")
    require(repair.get("merge", {}).get("message_receipt_parseable") is False, "administrative-review malformed classification drift")
    require(re.search(r"Merge PR #476", observed_message) is not None, "administrative-review PR marker missing")
    require(re.search(r"exact head [0-9a-f]{40}", observed_message) is None, "administrative-review message unexpectedly parseable")
    require(re.search(r"Disposition:\s*[A-Z0-9_]+", observed_message) is None, "administrative-review message unexpectedly has disposition token")

    approval = pull.get("approval", {})
    disposition_record = pull.get("disposition", {})
    require(approval.get("review_id") == receipt.get("review_id") == 4923702298, "administrative-review approval drift")
    require(approval.get("reviewer") == "jimsteeg", "administrative-review reviewer drift")
    require(approval.get("state") == receipt.get("review_state") == "APPROVED", "administrative-review review state drift")
    require(approval.get("exact_head") == reviewed_head, "administrative-review approval head drift")
    require(disposition_record.get("comment_id") == receipt.get("disposition_comment_id") == 5276363695, "administrative-review disposition comment drift")
    require(disposition_record.get("actor") == "fyremael", "administrative-review disposition actor drift")
    require(disposition_record.get("exact_head") == reviewed_head, "administrative-review disposition head drift")

    review_at = aa.parse_datetime(str(approval.get("submitted_at", "")))
    disposition_at = aa.parse_datetime(str(disposition_record.get("posted_at", "")))
    merge_at = aa.parse_datetime(str(repair.get("merge", {}).get("committed_at", "")))
    require(aa.iso_z(review_at) == aa.iso_z(aa.parse_datetime(str(receipt.get("review_submitted_at", "")))), "administrative-review review timestamp drift")
    require(aa.iso_z(disposition_at) == aa.iso_z(aa.parse_datetime(str(receipt.get("disposition_posted_at", "")))), "administrative-review disposition timestamp drift")
    require(aa.iso_z(merge_at) == aa.iso_z(aa.parse_datetime(str(receipt.get("merge_committed_at", "")))), "administrative-review merge timestamp drift")
    require(review_at < disposition_at < merge_at, "administrative-review gate chronology invalid")
    observed_committed_at = aa.parse_datetime(git_runner(["show", "-s", "--format=%cI", merge_commit]))
    require(aa.iso_z(observed_committed_at) == aa.iso_z(merge_at), "administrative-review merge timestamp mismatch")

    require(repair.get("bootstrap", {}).get("record_sha256_mode") == DERIVE_RECORD_SHA256, "administrative-review bootstrap mode drift")
    require(repair.get("bootstrap", {}).get("receipt_state") == "PROTECTED_COMPLETE", "administrative-review bootstrap state drift")
    require(repair.get("authority_boundary", {}).get("protected_main_rewritten") is False, "administrative-review repair rewrites history")
    require(all(value is False for value in repair.get("claim_boundaries", {}).values()), "administrative-review repair inflates claims")

    return {
        "procedure_id": procedure_id,
        "scheduled_due_at": scheduled_due_at,
        "record_path": record_path,
        "record_sha256": record_sha256,
        "merge_commit": merge_commit,
        "reviewed_head": reviewed_head,
        "pull_request": 476,
        "disposition": disposition,
        "receipt_state": "PROTECTED_COMPLETE",
    }


def normalize_repaired_bootstrap_receipt(
    root: Path,
    receipt: dict[str, Any],
    head_sha: str,
    git_runner: GitRunner,
) -> dict[str, Any]:
    repair_id = str(receipt.get("repair_id", ""))
    if repair_id == "MP-ADMIN-RECEIPT-REPAIR-476-001":
        return normalize_repaired_bootstrap_receipt_476(
            root,
            receipt,
            head_sha,
            git_runner,
        )
    require(repair_id == "MP-ADMIN-RECEIPT-REPAIR-244-001", "unsupported bootstrap repair identity")

    repair_record_path = str(receipt.get("repair_record_path", ""))
    require(
        repair_record_path
        == "governance/administrative_receipt_repairs/MP-ADMIN-RECEIPT-REPAIR-244-001.json",
        "bootstrap repair record path drift",
    )
    require(".." not in repair_record_path and not repair_record_path.startswith("/"), "unsafe repair record path")
    repair_path = root / repair_record_path
    require(repair_path.is_file(), "bootstrap repair record missing")
    repair = aa.load_json(repair_path)

    require(repair.get("schema_version") == "1.0.0", "bootstrap repair schema version drift")
    require(repair.get("repair_id") == repair_id, "bootstrap repair identity mismatch")
    require(repair.get("control_id") == "MP-ADMIN-MAINT-001", "bootstrap repair control drift")
    require(repair.get("repository") == "grandchallenge/MATH-PROGRAMME", "bootstrap repair repository drift")
    require(repair.get("source_issue") == 249, "bootstrap repair source issue drift")
    require(repair.get("tracking_issue") == 243, "bootstrap repair tracking issue drift")
    require(
        repair.get("occurrence_key") == "structural_sweep:2026-08-05T22:57:00Z",
        "bootstrap repair occurrence drift",
    )

    procedure_id = str(receipt.get("procedure_id", ""))
    scheduled_due_at = aa.iso_z(aa.parse_datetime(str(receipt.get("scheduled_due_at", ""))))
    require(procedure_id == repair.get("procedure_id") == "structural_sweep", "bootstrap repair procedure drift")
    require(
        scheduled_due_at
        == aa.iso_z(aa.parse_datetime(str(repair.get("scheduled_due_at", ""))))
        == "2026-08-05T22:57:00Z",
        "bootstrap repair scheduled locus drift",
    )

    record = repair.get("record", {})
    record_path = str(receipt.get("record_path", ""))
    require(
        record_path
        == record.get("path")
        == "governance/administrative_structural_sweeps/MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007.json",
        "bootstrap repair record path mismatch",
    )
    require(".." not in record_path and not record_path.startswith("/"), "unsafe bootstrap record path")
    path = root / record_path
    require(path.is_file(), "bootstrap record missing")
    require(
        record.get("sweep_id") == "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007",
        "bootstrap sweep identity drift",
    )
    require(
        record.get("status") == "COMPLETE_WITH_REPAIRED_P2_AND_NONBLOCKING_OPEN_PR",
        "bootstrap sweep status drift",
    )
    expected_blob = str(receipt.get("record_git_blob", ""))
    require(
        expected_blob == record.get("git_blob") == "51db3bc72c8f371ace530ad5ce11322cd6af326c",
        "bootstrap immutable record blob drift",
    )
    require(git_blob_sha(path) == expected_blob, "bootstrap immutable record content drift")
    require(
        receipt.get("record_sha256") == DERIVE_RECORD_SHA256,
        "bootstrap repair must derive record SHA-256 from immutable content",
    )
    record_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()

    pull_request = int(receipt.get("pull_request", 0))
    reviewed_head = str(receipt.get("reviewed_head", ""))
    merge_commit = str(receipt.get("merge_commit", ""))
    disposition = str(receipt.get("disposition", ""))
    require(pull_request == repair.get("pull_request", {}).get("number") == 244, "bootstrap PR drift")
    require(
        reviewed_head
        == repair.get("pull_request", {}).get("head")
        == "3a5977c2d13d8ece9365dcda356d089e7baefd8e",
        "bootstrap reviewed head drift",
    )
    require(
        merge_commit
        == repair.get("merge", {}).get("commit")
        == "ba89cf1cc253486a70ea832c2db8fca9e81f4a9f",
        "bootstrap merge commit drift",
    )
    require(
        disposition
        == repair.get("pull_request", {}).get("disposition", {}).get("token")
        == "HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
        "bootstrap disposition drift",
    )
    require(aa.SHA_RE.fullmatch(reviewed_head) is not None, "bootstrap reviewed head invalid")
    require(aa.SHA_RE.fullmatch(merge_commit) is not None, "bootstrap merge commit invalid")

    expected_parents = [
        "6dd51c29b8bcbac812bcf7a4e803b693ac8be69c",
        reviewed_head,
    ]
    repair_parents = repair.get("merge", {}).get("parents")
    receipt_parents = receipt.get("merge_parents")
    require(repair_parents == expected_parents, "bootstrap repair merge parent drift")
    require(receipt_parents == expected_parents, "bootstrap receipt merge parent drift")
    observed_parents = git_runner(["show", "-s", "--format=%P", merge_commit]).split()
    require(observed_parents == expected_parents, "bootstrap merge parent relationship invalid")

    introduction = git_runner(
        ["log", "--first-parent", "--diff-filter=A", "--format=%H", "-1", head_sha, "--", record_path]
    )
    require(introduction == merge_commit, "bootstrap record introduction commit drift")
    require(protected_ancestor(root, merge_commit, head_sha), "bootstrap repair merge is not protected-ancestral")

    observed_message = git_runner(["show", "-s", "--format=%B", merge_commit]).strip()
    expected_message = str(repair.get("merge", {}).get("message", "")).strip()
    require(observed_message == expected_message, "historical malformed merge message drift")
    default_match = DEFAULT_PULL_REQUEST_MERGE_RE.fullmatch(observed_message)
    require(default_match is not None and int(default_match.group(1)) == pull_request, "historical merge PR identity drift")
    require(repair.get("merge", {}).get("message_receipt_parseable") is False, "historical message classification drift")
    require(re.search(r"Merge PR #\d+", observed_message) is None, "historical message unexpectedly has parser PR marker")
    require(re.search(r"exact head [0-9a-f]{40}", observed_message) is None, "historical message unexpectedly has exact-head marker")
    require(re.search(r"Disposition:\s*[A-Z0-9_]+", observed_message) is None, "historical message unexpectedly has disposition marker")

    approval = repair.get("pull_request", {}).get("approval", {})
    disposition_record = repair.get("pull_request", {}).get("disposition", {})
    require(approval.get("review_id") == receipt.get("review_id") == 4869603629, "bootstrap approval review drift")
    require(approval.get("reviewer") == "jimsteeg", "bootstrap approval reviewer drift")
    require(approval.get("state") == receipt.get("review_state") == "APPROVED", "bootstrap approval state drift")
    require(approval.get("exact_head") == reviewed_head, "bootstrap approval exact-head drift")
    require(
        disposition_record.get("comment_id") == receipt.get("disposition_comment_id") == 5198515780,
        "bootstrap disposition comment drift",
    )
    require(disposition_record.get("actor") == "fyremael", "bootstrap disposition actor drift")
    require(disposition_record.get("exact_head") == reviewed_head, "bootstrap disposition exact-head drift")

    review_at = aa.parse_datetime(str(approval.get("submitted_at", "")))
    disposition_at = aa.parse_datetime(str(disposition_record.get("posted_at", "")))
    merge_at = aa.parse_datetime(str(repair.get("merge", {}).get("committed_at", "")))
    require(
        aa.iso_z(review_at) == aa.iso_z(aa.parse_datetime(str(receipt.get("review_submitted_at", "")))),
        "bootstrap review timestamp drift",
    )
    require(
        aa.iso_z(disposition_at) == aa.iso_z(aa.parse_datetime(str(receipt.get("disposition_posted_at", "")))),
        "bootstrap disposition timestamp drift",
    )
    require(
        aa.iso_z(merge_at) == aa.iso_z(aa.parse_datetime(str(receipt.get("merge_committed_at", "")))),
        "bootstrap merge timestamp drift",
    )
    require(review_at < disposition_at < merge_at, "bootstrap approval/disposition/merge chronology invalid")
    observed_committed_at = aa.parse_datetime(git_runner(["show", "-s", "--format=%cI", merge_commit]))
    require(aa.iso_z(observed_committed_at) == aa.iso_z(merge_at), "bootstrap merge timestamp does not match git")

    bootstrap = repair.get("bootstrap", {})
    require(bootstrap.get("record_sha256_mode") == DERIVE_RECORD_SHA256, "bootstrap SHA-256 mode drift")
    require(bootstrap.get("receipt_state") == "PROTECTED_COMPLETE", "bootstrap receipt state drift")
    require(
        bootstrap.get("protected_completion_declared_before_repair_merge") is False,
        "bootstrap repair rewrites pre-repair completion history",
    )
    require(
        repair.get("authority_boundary", {}).get("protected_main_rewritten") is False,
        "bootstrap repair authorizes protected history rewrite",
    )
    require(
        all(value is False for value in repair.get("claim_boundaries", {}).values()),
        "bootstrap repair inflates claim authority",
    )

    return {
        "procedure_id": procedure_id,
        "scheduled_due_at": scheduled_due_at,
        "record_path": record_path,
        "record_sha256": record_sha256,
        "merge_commit": merge_commit,
        "reviewed_head": reviewed_head,
        "pull_request": pull_request,
        "disposition": disposition,
        "receipt_state": "PROTECTED_COMPLETE",
    }


def normalize_bootstrap_receipt(
    root: Path,
    receipt: dict[str, Any],
    head_sha: str,
    git_runner: GitRunner,
) -> dict[str, Any]:
    if receipt.get("repair_id"):
        return normalize_repaired_bootstrap_receipt(root, receipt, head_sha, git_runner)
    return normalize_legacy_bootstrap_receipt(root, receipt, head_sha)


def receipt_for_record(
    root: Path,
    path: Path,
    procedure_id: str,
    due_fields: list[str],
    head_sha: str,
    git_runner: GitRunner,
) -> dict[str, Any] | None:
    record = aa.load_json(path)
    status = str(record.get("status", ""))
    if not (status.startswith("COMPLETE") or status.startswith("PROTECTED_")):
        return None
    due = aa.record_due(record, due_fields)
    if not due:
        return None
    relative = path.relative_to(root).as_posix()
    merge_commit = git_runner(
        ["log", "--first-parent", "--diff-filter=A", "--format=%H", "-1", head_sha, "--", relative]
    )
    if not aa.SHA_RE.fullmatch(merge_commit):
        raise aa.AutomationError(f"{relative}: no protected first-parent introduction commit")
    if not protected_ancestor(root, merge_commit, head_sha):
        raise aa.AutomationError(f"{relative}: introduction commit is not ancestral to protected head")
    parents = git_runner(["show", "-s", "--format=%P", merge_commit]).split()
    if len(parents) < 2:
        return None
    message = git_runner(["show", "-s", "--format=%B", merge_commit]).strip()
    pr_match = re.search(r"Merge PR #(\d+)", message)
    head_match = re.search(r"exact head ([0-9a-f]{40})", message)
    disposition_match = re.search(r"Disposition:\s*([A-Z0-9_]+)", message)
    if not (pr_match and head_match and disposition_match):
        synthetic = SYNTHETIC_PULL_REQUEST_MERGE_RE.fullmatch(message)
        if synthetic and merge_commit == head_sha and parents == [synthetic.group(2), synthetic.group(1)]:
            return None
        raise aa.AutomationError(f"{relative}: merge receipt lacks PR, exact head, or disposition")
    return {
        "procedure_id": procedure_id,
        "scheduled_due_at": due,
        "record_path": relative,
        "record_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "merge_commit": merge_commit,
        "reviewed_head": head_match.group(1),
        "pull_request": int(pr_match.group(1)),
        "disposition": disposition_match.group(1),
        "receipt_state": "PROTECTED_COMPLETE",
    }


def derive_completion_state(
    root: Path,
    config: dict[str, Any],
    head_sha: str,
    git_runner: GitRunner = default_git_runner,
) -> dict[str, Any]:
    if not aa.SHA_RE.fullmatch(head_sha):
        raise aa.AutomationError("protected head SHA is invalid")
    receipts: list[dict[str, Any]] = [
        normalize_bootstrap_receipt(root, receipt, head_sha, git_runner)
        for receipt in config.get("bootstrap_receipts", [])
    ]
    bootstrap_coverage = {
        (
            receipt["procedure_id"],
            aa.iso_z(aa.parse_datetime(receipt["scheduled_due_at"])),
            receipt["record_path"],
        )
        for receipt in receipts
    }

    for procedure_id, procedure in config["procedures"].items():
        due_fields = procedure.get("due_fields", ["scheduled_due_at"])
        floor_raw = procedure.get("receipt_floor_utc")
        floor = aa.parse_datetime(floor_raw) if floor_raw else None
        for pattern in procedure["record_globs"]:
            for path in sorted(root.glob(pattern)):
                record = aa.load_json(path)
                due_raw = aa.record_due(record, due_fields)
                if not due_raw:
                    continue
                if floor and aa.parse_datetime(due_raw) < floor:
                    continue
                coverage_key = (
                    procedure_id,
                    aa.iso_z(aa.parse_datetime(due_raw)),
                    path.relative_to(root).as_posix(),
                )
                if coverage_key in bootstrap_coverage:
                    continue
                receipt = receipt_for_record(root, path, procedure_id, due_fields, head_sha, git_runner)
                if receipt:
                    receipts.append(receipt)

    seen: dict[tuple[str, str], dict[str, Any]] = {}
    for receipt in receipts:
        if receipt.get("receipt_state") != "PROTECTED_COMPLETE":
            raise aa.AutomationError("non-protected receipt cannot advance completion")
        if not aa.SHA_RE.fullmatch(str(receipt.get("merge_commit", ""))):
            raise aa.AutomationError("receipt merge commit invalid")
        key = (receipt["procedure_id"], aa.iso_z(aa.parse_datetime(receipt["scheduled_due_at"])))
        normalized = {**receipt, "scheduled_due_at": key[1]}
        previous = seen.get(key)
        if previous and aa.canonical_digest(previous) != aa.canonical_digest(normalized):
            raise aa.AutomationError(f"conflicting protected receipts for {key[0]} {key[1]}")
        seen[key] = normalized

    procedures: dict[str, Any] = {}
    for procedure_id in config["procedures"]:
        matching = [receipt for (kind, _), receipt in seen.items() if kind == procedure_id]
        matching.sort(key=lambda item: aa.parse_datetime(item["scheduled_due_at"]))
        procedures[procedure_id] = {
            "completed_through_utc": matching[-1]["scheduled_due_at"] if matching else None,
            "receipt_count": len(matching),
            "receipts": matching,
        }

    return {
        "schema_version": "1.0.0",
        "control_id": "MP-ADMIN-MAINT-001",
        "derived_from_protected_head": head_sha,
        "state": "PROTECTED_RECEIPT_DERIVED",
        "procedures": procedures,
        "authority_boundary": {
            "issues_are_authority": False,
            "workflow_artifacts_are_authority": False,
            "draft_pull_requests_are_authority": False,
            "unmerged_branches_are_authority": False,
            "protected_merge_receipts_required": True,
        },
    }
