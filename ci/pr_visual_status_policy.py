#!/usr/bin/env python3
"""Deterministic, fail-closed policy core for ADR-0019 PR visual status reports."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from html import escape
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"
GENERATOR_VERSION = "0.1.0-pilot"
SIGNIFICANCE_PROFILE_VERSION = "1.0.0"
GOVERNED_OVERRIDE_AUTHORITIES = {"Human Steward", "Referee", "Council"}
AUTOMATIC_SIGNIFICANCE_TRIGGERS = (
    "formal_disposition",
    "governance_or_control_plane",
    "administrative_automation",
    "protected_branch_or_merge_control",
    "source_or_claim_classification",
    "theorem_certification_or_formal_replay",
    "repository_policy_or_workflow",
    "material_nonclaims_blockers_or_residuals",
)


class ReportError(RuntimeError):
    """Raised when a report cannot be deterministically trusted."""


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def source_view(report: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "report_id",
        "identity",
        "significance",
        "authority",
        "checks",
        "integration",
        "blockers",
        "nonclaims",
        "history",
        "modules",
    )
    try:
        return {key: deepcopy(report[key]) for key in keys}
    except KeyError as exc:
        raise ReportError(f"missing canonical source field: {exc.args[0]}") from exc


def classify_significance(signals: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(signals, dict):
        raise ReportError("significance signals must be an object")
    triggered = [
        key for key in AUTOMATIC_SIGNIFICANCE_TRIGGERS if signals.get(key) is True
    ]
    override = signals.get("manual_override", {})
    if override is None:
        override = {}
    if not isinstance(override, dict):
        raise ReportError("manual_override must be an object")
    enabled = override.get("enabled") is True
    authority = override.get("authority")
    reason = override.get("reason")
    if enabled:
        if authority not in GOVERNED_OVERRIDE_AUTHORITIES:
            raise ReportError("manual significance override lacks governed authority")
        if not isinstance(reason, str) or not reason.strip():
            raise ReportError("manual significance override requires a reason")
    else:
        authority = None
        reason = None
    return {
        "profile_version": SIGNIFICANCE_PROFILE_VERSION,
        "significant": bool(triggered or enabled),
        "triggers": triggered,
        "manual_override": {
            "enabled": enabled,
            "authority": authority,
            "reason": reason,
        },
    }


def _freshness(report: dict[str, Any]) -> tuple[str, list[str]]:
    identity = report.get("identity", {})
    exact = identity.get("exact_head_sha")
    current = identity.get("current_head_sha")
    if not current:
        return "UNKNOWN", ["current PR head is unavailable"]
    if current != exact:
        return "STALE", ["report exact head no longer equals current PR head"]
    return "CURRENT", []


def _authority_head_mismatch(
    authority: dict[str, Any],
    exact_head: str,
    accepted_states: set[str],
) -> bool:
    return (
        authority.get("state") in accepted_states
        and authority.get("commit_sha") != exact_head
    )


def evaluate_report(report: dict[str, Any]) -> dict[str, Any]:
    freshness, reasons = _freshness(report)
    if freshness == "STALE":
        return {"freshness": freshness, "operative_state": "STALE", "reasons": reasons}
    if freshness == "UNKNOWN":
        return {
            "freshness": freshness,
            "operative_state": "UNKNOWN",
            "reasons": reasons,
        }

    identity = report["identity"]
    exact = identity["exact_head_sha"]
    review = report["authority"]["independent_review"]
    steward = report["authority"]["human_steward"]

    if _authority_head_mismatch(review, exact, {"APPROVED", "CHANGES_REQUESTED"}):
        reasons.append("independent review is bound to a different head")
        return {"freshness": freshness, "operative_state": "BLOCKED", "reasons": reasons}
    if _authority_head_mismatch(steward, exact, {"AUTHORIZED", "DECLINED"}):
        reasons.append("Human Steward disposition is bound to a different head")
        return {"freshness": freshness, "operative_state": "BLOCKED", "reasons": reasons}

    open_blockers = [b for b in report.get("blockers", []) if b.get("status") == "OPEN"]
    if open_blockers:
        reasons.append(f"{len(open_blockers)} open blocker(s) remain")
        return {"freshness": freshness, "operative_state": "BLOCKED", "reasons": reasons}

    required_checks = [check for check in report.get("checks", []) if check.get("required")]
    for check in required_checks:
        if check.get("head_sha") != exact:
            reasons.append(f"required check {check.get('name')} is not exact-head bound")
            return {"freshness": freshness, "operative_state": "BLOCKED", "reasons": reasons}
        if check.get("status") == "completed" and check.get("conclusion") != "success":
            reasons.append(
                f"required check {check.get('name')} completed without success"
            )
            return {"freshness": freshness, "operative_state": "BLOCKED", "reasons": reasons}

    if review.get("state") == "CHANGES_REQUESTED":
        reasons.append("independent review requests changes")
        return {
            "freshness": freshness,
            "operative_state": "CHANGES_REQUESTED",
            "reasons": reasons,
        }
    if steward.get("state") == "DECLINED":
        reasons.append("Human Steward declined authorization")
        return {"freshness": freshness, "operative_state": "BLOCKED", "reasons": reasons}

    pending_checks = [
        check
        for check in required_checks
        if check.get("status") != "completed" or check.get("conclusion") != "success"
    ]
    if pending_checks:
        reasons.append(f"{len(pending_checks)} required check(s) are not complete")
        return {
            "freshness": freshness,
            "operative_state": "CHECKS_PENDING",
            "reasons": reasons,
        }

    if review.get("required"):
        if review.get("state") != "APPROVED":
            reasons.append("required independent review is not approved")
            return {
                "freshness": freshness,
                "operative_state": "REVIEW_PENDING",
                "reasons": reasons,
            }
    elif review.get("state") != "NOT_REQUIRED":
        reasons.append("independent review requirement/state is inconsistent")
        return {"freshness": freshness, "operative_state": "UNKNOWN", "reasons": reasons}

    if steward.get("required"):
        if steward.get("state") != "AUTHORIZED":
            reasons.append("required Human Steward authorization is not present")
            return {
                "freshness": freshness,
                "operative_state": "AUTHORIZATION_PENDING",
                "reasons": reasons,
            }
    elif steward.get("state") != "NOT_REQUIRED":
        reasons.append("Human Steward requirement/state is inconsistent")
        return {"freshness": freshness, "operative_state": "UNKNOWN", "reasons": reasons}

    integration = report["integration"]
    merge_state = integration.get("merge_state")
    readback = integration.get("protected_readback", {})
    if merge_state == "CLOSED_UNMERGED":
        return {
            "freshness": freshness,
            "operative_state": "CLOSED_UNMERGED",
            "reasons": reasons,
        }
    if merge_state == "UNKNOWN":
        reasons.append("merge state is unavailable")
        return {"freshness": freshness, "operative_state": "UNKNOWN", "reasons": reasons}
    if merge_state == "OPEN":
        state = (
            "AUTHORIZED_FOR_PROTECTED_MERGE"
            if steward.get("required") and steward.get("state") == "AUTHORIZED"
            else "READY_FOR_MERGE"
        )
        return {"freshness": freshness, "operative_state": state, "reasons": reasons}
    if merge_state == "MERGED":
        merge_sha = integration.get("merge_commit_sha")
        if not merge_sha:
            reasons.append("merged state lacks merge commit identity")
            return {"freshness": freshness, "operative_state": "BLOCKED", "reasons": reasons}
        if readback.get("required"):
            if readback.get("state") == "COMPLETE":
                if readback.get("main_sha") != merge_sha:
                    reasons.append("protected readback does not equal merge commit")
                    return {
                        "freshness": freshness,
                        "operative_state": "BLOCKED",
                        "reasons": reasons,
                    }
                return {
                    "freshness": freshness,
                    "operative_state": "PROTECTED_COMPLETE",
                    "reasons": reasons,
                }
            if readback.get("state") == "BLOCKED":
                reasons.append("protected readback is blocked")
                return {
                    "freshness": freshness,
                    "operative_state": "BLOCKED",
                    "reasons": reasons,
                }
            reasons.append("protected readback is not complete")
            return {
                "freshness": freshness,
                "operative_state": "MERGED_READBACK_PENDING",
                "reasons": reasons,
            }
        if readback.get("state") != "NOT_APPLICABLE":
            reasons.append("non-required protected readback has inconsistent state")
            return {"freshness": freshness, "operative_state": "UNKNOWN", "reasons": reasons}
        return {"freshness": freshness, "operative_state": "MERGED", "reasons": reasons}

    reasons.append("unhandled merge state")
    return {"freshness": freshness, "operative_state": "UNKNOWN", "reasons": reasons}


def seal_report(report: dict[str, Any]) -> dict[str, Any]:
    sealed = deepcopy(report)
    provenance = sealed.setdefault("provenance", {})
    observed_at = provenance.get("observed_at")
    if not isinstance(observed_at, str) or not observed_at:
        raise ReportError("provenance.observed_at is required")
    provenance["schema_version"] = SCHEMA_VERSION
    provenance["generator_version"] = GENERATOR_VERSION
    provenance["source_snapshot_sha256"] = sha256_json(source_view(sealed))
    sealed["derived"] = evaluate_report(sealed)
    return sealed


def verify_report(report: dict[str, Any]) -> None:
    provenance = report.get("provenance", {})
    if provenance.get("schema_version") != SCHEMA_VERSION:
        raise ReportError("schema version mismatch")
    expected_digest = sha256_json(source_view(report))
    if provenance.get("source_snapshot_sha256") != expected_digest:
        raise ReportError("source snapshot digest mismatch")
    expected_derived = evaluate_report(report)
    if report.get("derived") != expected_derived:
        raise ReportError("derived status does not match canonical source state")


def _review_label(review: dict[str, Any]) -> str:
    actor = review.get("actor") or "—"
    rid = review.get("review_id")
    suffix = f" #{rid}" if rid else ""
    return f"{review.get('state', 'UNKNOWN')} · {actor}{suffix}"


def _steward_label(steward: dict[str, Any]) -> str:
    disposition = steward.get("disposition") or "—"
    return f"{steward.get('state', 'UNKNOWN')} · {disposition}"


def _check_summary(report: dict[str, Any]) -> str:
    required = [c for c in report.get("checks", []) if c.get("required")]
    successful = sum(
        c.get("status") == "completed"
        and c.get("conclusion") == "success"
        and c.get("head_sha") == report["identity"]["exact_head_sha"]
        for c in required
    )
    return f"{successful}/{len(required)} required exact-head checks successful"


def render_text(report: dict[str, Any]) -> str:
    verify_report(report)
    identity = report["identity"]
    integration = report["integration"]
    review = report["authority"]["independent_review"]
    steward = report["authority"]["human_steward"]
    lines = [
        f"# {report['report_id']} — PR #{identity['pr_number']} visual status",
        "",
        f"Repository: {identity['repository']}",
        f"Title: {identity['title']}",
        f"Operative state: {report['derived']['operative_state']}",
        f"Freshness: {report['derived']['freshness']}",
        f"Exact head: {identity['exact_head_sha']}",
        f"Current head: {identity['current_head_sha'] or 'UNKNOWN'}",
        f"Independent review: {_review_label(review)}",
        f"Human Steward: {_steward_label(steward)}",
        f"Checks: {_check_summary(report)}",
        f"Merge state: {integration['merge_state']}",
        f"Merge commit: {integration['merge_commit_sha'] or '—'}",
        f"Protected readback: {integration['protected_readback']['state']}",
        f"Open blockers: {sum(b['status'] == 'OPEN' for b in report['blockers'])}",
        f"Nonclaims: {len(report['nonclaims'])}",
        f"Source digest: {report['provenance']['source_snapshot_sha256']}",
    ]
    if report["derived"]["reasons"]:
        lines.extend(["", "Reasons:"])
        lines.extend(f"- {reason}" for reason in report["derived"]["reasons"])
    if report["history"]:
        lines.extend(["", "Retained history:"])
        for item in report["history"][-5:]:
            lines.append(f"- {item['at']} · {item['event']} · {item['outcome']}")
    if report["nonclaims"]:
        lines.extend(["", "Bounded nonclaims:"])
        lines.extend(f"- {item}" for item in report["nonclaims"])
    return "\n".join(lines) + "\n"


def render_svg(report: dict[str, Any]) -> str:
    verify_report(report)
    identity = report["identity"]
    review = report["authority"]["independent_review"]
    steward = report["authority"]["human_steward"]
    integration = report["integration"]
    rows = [
        ("STATUS", report["derived"]["operative_state"]),
        ("FRESHNESS", report["derived"]["freshness"]),
        ("REPOSITORY", identity["repository"]),
        ("PR", f"#{identity['pr_number']} · {identity['title']}"),
        ("EXACT HEAD", identity["exact_head_sha"]),
        ("REVIEW", _review_label(review)),
        ("HUMAN STEWARD", _steward_label(steward)),
        ("CHECKS", _check_summary(report)),
        ("MERGE", f"{integration['merge_state']} · {integration['merge_commit_sha'] or '—'}"),
        ("READBACK", integration["protected_readback"]["state"]),
        ("BLOCKERS", str(sum(b["status"] == "OPEN" for b in report["blockers"]))),
        ("SOURCE DIGEST", report["provenance"]["source_snapshot_sha256"]),
    ]
    height = 170 + 54 * len(rows)
    text_rows = []
    y = 150
    for label, value in rows:
        text_rows.append(
            f'<text x="48" y="{y}" font-size="18" font-weight="700">{escape(label)}</text>'
        )
        text_rows.append(
            f'<text x="270" y="{y}" font-size="18">{escape(str(value))}</text>'
        )
        y += 54
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" '
        f'viewBox="0 0 1200 {height}" role="img" '
        f'aria-label="{escape(report["report_id"])} PR visual status report">'
        '<rect width="1200" height="100%" fill="white" stroke="black"/>'
        f'<text x="48" y="62" font-size="30" font-weight="700">{escape(report["report_id"])}</text>'
        f'<text x="48" y="98" font-size="20">Deterministic advisory PR status report</text>'
        + "".join(text_rows)
        + "</svg>\n"
    )


def _load(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ReportError("report JSON must be an object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    render = sub.add_parser("render")
    render.add_argument("input")
    render.add_argument("--sealed-out")
    render.add_argument("--text-out")
    render.add_argument("--svg-out")
    check = sub.add_parser("check")
    check.add_argument("input")
    args = parser.parse_args()
    try:
        if args.command == "check":
            verify_report(_load(args.input))
            print("PR visual status report: verified")
            return 0
        sealed = seal_report(_load(args.input))
        if args.sealed_out:
            Path(args.sealed_out).write_text(
                json.dumps(sealed, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        if args.text_out:
            Path(args.text_out).write_text(render_text(sealed), encoding="utf-8")
        if args.svg_out:
            Path(args.svg_out).write_text(render_svg(sealed), encoding="utf-8")
        if not any((args.sealed_out, args.text_out, args.svg_out)):
            print(json.dumps(sealed, indent=2, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ReportError) as exc:
        print(f"PR visual status report error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
