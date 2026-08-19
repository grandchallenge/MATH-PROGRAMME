#!/usr/bin/env python3
"""Bounded advisory PRVSR Phase 1 collector/publisher for MATH-PROGRAMME."""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from autonomy_github import AutonomyError, Client
import pr_visual_status_policy as policy
import pr_visual_status_transport as transport

CONFIG_PATH = Path("governance/pr_visual_status_phase1.json")
ALLOWED_REPOSITORY = "grandchallenge/MATH-PROGRAMME"
COMMENT_MARKER = "<!-- prvsr-phase1:pr-{pr_number} -->"


class OperationalError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise OperationalError(f"cannot read Phase 1 config: {exc}") from exc
    if not isinstance(value, dict) or value.get("repository") != ALLOWED_REPOSITORY:
        raise OperationalError("Phase 1 repository boundary is invalid")
    if value.get("significance_profile_version") != policy.SIGNIFICANCE_PROFILE_VERSION:
        raise OperationalError("significance profile version mismatch")
    expected = {
        "advisory_only": True,
        "visual_is_authoritative": False,
        "new_merge_gate": False,
        "cross_repository_propagation": False,
        "human_performance_claims_authorized": False,
    }
    if value.get("authority_boundary") != expected:
        raise OperationalError("Phase 1 authority boundary is invalid")
    return value


def paged(client: Client, path: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    page = 1
    joiner = "&" if "?" in path else "?"
    while True:
        batch = client.get(f"{path}{joiner}per_page=100&page={page}")
        if not isinstance(batch, list):
            raise OperationalError(f"expected list from {path}")
        out.extend(item for item in batch if isinstance(item, dict))
        if len(batch) < 100:
            return out
        page += 1


def content_json(client: Client, repo: str, path: str, ref: str) -> dict[str, Any] | None:
    try:
        value = client.get(
            f"/repos/{repo}/contents/{path}?ref={urllib.parse.quote(ref, safe='')}"
        )
    except AutonomyError as exc:
        if " 404 " in str(exc):
            return None
        raise
    try:
        result = json.loads(base64.b64decode(value["content"]))
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise OperationalError(f"invalid governed JSON at {path}") from exc
    if not isinstance(result, dict):
        raise OperationalError(f"governed JSON at {path} must be an object")
    return result


def governed_override(
    client: Client, repo: str, pr_number: int, head: str, config: dict[str, Any]
) -> tuple[dict[str, Any] | None, list[str]]:
    path = str(config["manual_override_path_template"]).format(pr_number=pr_number)
    record = content_json(client, repo, path, "main")
    if record is None:
        return None, []
    if record.get("exact_head_sha") != head:
        return None, ["governed manual significance override is bound to a different head"]
    authority, reason = record.get("authority"), record.get("reason")
    if authority not in policy.GOVERNED_OVERRIDE_AUTHORITIES:
        raise OperationalError("manual override record has invalid authority")
    if not isinstance(reason, str) or not reason.strip():
        raise OperationalError("manual override record lacks a reason")
    return {"authority": authority, "reason": reason.strip()}, []


def significance_signals(
    pr: dict[str, Any], files: list[dict[str, Any]], override: dict[str, Any] | None
) -> dict[str, Any]:
    paths = [str(item.get("filename") or "").lower() for item in files]
    body = str(pr.get("body") or "").lower()

    def has(*needles: str) -> bool:
        return any(any(n in p for n in needles) for p in paths)

    signals: dict[str, Any] = {
        "formal_disposition": "disposition" in body and any(
            x in body for x in ("human_steward", "referee", "council")
        ),
        "governance_or_control_plane": any(
            p.startswith(("governance/", "schemas/")) for p in paths
        ) or has("ruleset", "branch_protection", "release-trust"),
        "administrative_automation": has("administrative_", "administrative-"),
        "protected_branch_or_merge_control": has(
            "ruleset", "branch_protection", "release-trust", "merge_control", "auto_merge"
        ),
        "source_or_claim_classification": has("source", "claim", "concordance")
        or any(x in body for x in ("source admission", "claim classification")),
        "theorem_certification_or_formal_replay": any(
            p.endswith(".lean") or p.startswith("fixtures/formal/") for p in paths
        ) or has("certificate", "certification", "formal_replay"),
        "repository_policy_or_workflow": any(
            p.startswith(".github/workflows/")
            or p.startswith("ci/validate_")
            or p.startswith("ci/test_")
            or "policy" in p
            for p in paths
        ),
        "material_nonclaims_blockers_or_residuals": any(
            x in body
            for x in ("nonclaim", "blocker", "residual obligation", "open_with_characterized_blocker")
        ),
    }
    if override:
        signals["manual_override"] = {
            "enabled": True,
            "authority": override["authority"],
            "reason": override["reason"],
        }
    return signals


def active_rulesets(client: Client, repo: str) -> tuple[list[dict[str, Any]], str | None]:
    try:
        summaries = client.get(f"/repos/{repo}/rulesets?includes_parents=true")
        if not isinstance(summaries, list):
            raise OperationalError("ruleset summary is not a list")
        details = []
        for item in summaries:
            if not isinstance(item, dict) or item.get("enforcement") != "active":
                continue
            rid = item.get("id")
            if isinstance(rid, int):
                detail = client.get(f"/repos/{repo}/rulesets/{rid}")
                if isinstance(detail, dict) and detail.get("enforcement") == "active":
                    details.append(detail)
        return details, None
    except (AutonomyError, OperationalError) as exc:
        return [], f"live ruleset requiredness unavailable: {exc}"


def ruleset_requirements(rulesets: list[dict[str, Any]]) -> tuple[set[str], bool | None]:
    contexts: set[str] = set()
    review_required: bool | None = False
    for ruleset in rulesets:
        for rule in ruleset.get("rules", []):
            if not isinstance(rule, dict):
                continue
            params = rule.get("parameters", {})
            if rule.get("type") == "required_status_checks":
                for item in params.get("required_status_checks", []):
                    context = item.get("context") if isinstance(item, dict) else None
                    if isinstance(context, str):
                        contexts.add(context)
            elif rule.get("type") == "pull_request":
                try:
                    if int(params.get("required_approving_review_count", 0)) > 0:
                        review_required = True
                except (TypeError, ValueError):
                    review_required = None
    return contexts, review_required


def latest_check_runs(client: Client, repo: str, head: str) -> dict[str, dict[str, Any]]:
    value = client.get(f"/repos/{repo}/commits/{head}/check-runs?per_page=100")
    latest: dict[str, dict[str, Any]] = {}
    for run in value.get("check_runs", []) if isinstance(value, dict) else []:
        if not isinstance(run, dict):
            continue
        name = str(run.get("name") or "")
        if not name:
            continue
        stamp = str(run.get("started_at") or run.get("created_at") or "")
        prior = latest.get(name)
        prior_stamp = str((prior or {}).get("started_at") or (prior or {}).get("created_at") or "")
        if prior is None or stamp >= prior_stamp:
            latest[name] = run
    return latest


def check_records(
    client: Client, repo: str, head: str, required: set[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    latest = latest_check_runs(client, repo, head)
    observed = [
        {
            "name": name,
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "check_run_id": run.get("id"),
            "head_sha": run.get("head_sha"),
        }
        for name, run in sorted(latest.items())
    ]
    records = []
    allowed = {
        "success", "failure", "cancelled", "skipped", "neutral",
        "action_required", "timed_out", "stale",
    }
    for name in sorted(required):
        run = latest.get(name)
        if run is None:
            records.append(
                {
                    "name": name, "required": True, "status": "queued",
                    "conclusion": None, "run_id": None, "head_sha": head,
                }
            )
            continue
        status = str(run.get("status") or "unknown")
        conclusion = run.get("conclusion")
        if conclusion is not None and conclusion not in allowed:
            conclusion = "unknown"
        records.append(
            {
                "name": name,
                "required": True,
                "status": status if status in {"queued", "in_progress", "completed"} else "unknown",
                "conclusion": conclusion,
                "run_id": int(run["id"]) if isinstance(run.get("id"), int) else None,
                "head_sha": str(run.get("head_sha") or head),
            }
        )
    return records, observed


def review_authority(
    client: Client, repo: str, pr: dict[str, Any], required: bool | None
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    number, head = int(pr["number"]), str(pr["head"]["sha"])
    author = str(pr.get("user", {}).get("login") or "")
    reviews = paged(client, f"/repos/{repo}/pulls/{number}/reviews?")
    observed = [
        {
            "review_id": r.get("id"), "actor": r.get("user", {}).get("login"),
            "state": r.get("state"), "commit_sha": r.get("commit_id"),
            "submitted_at": r.get("submitted_at"),
        }
        for r in reviews if str(r.get("user", {}).get("login") or "") != author
    ]
    if required is None:
        return {
            "required": False, "state": "UNKNOWN", "review_id": None,
            "actor": None, "commit_sha": None,
        }, observed
    if required is False:
        return {
            "required": False, "state": "NOT_REQUIRED", "review_id": None,
            "actor": None, "commit_sha": None,
        }, observed
    exact = [
        r for r in reviews
        if str(r.get("user", {}).get("login") or "") != author
        and str(r.get("commit_id") or "") == head
        and str(r.get("state") or "").upper() in {"APPROVED", "CHANGES_REQUESTED"}
    ]
    exact.sort(key=lambda r: (str(r.get("submitted_at") or ""), int(r.get("id") or 0)))
    if not exact:
        return {
            "required": True, "state": "PENDING", "review_id": None,
            "actor": None, "commit_sha": None,
        }, observed
    r = exact[-1]
    return {
        "required": True, "state": str(r["state"]).upper(), "review_id": int(r["id"]),
        "actor": str(r.get("user", {}).get("login") or "unknown"), "commit_sha": head,
    }, observed


def steward_authority(
    client: Client, repo: str, pr: dict[str, Any], config: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    number, head = int(pr["number"]), str(pr["head"]["sha"])
    allowed = set(str(x) for x in config.get("human_steward_logins", []))
    comments = paged(client, f"/repos/{repo}/issues/{number}/comments?")
    observed, candidates = [], []
    for item in comments:
        body, login = str(item.get("body") or ""), str(item.get("user", {}).get("login") or "")
        first = body.splitlines()[0].strip() if body.splitlines() else ""
        if first.startswith("HUMAN_STEWARD_"):
            observed.append(
                {
                    "comment_id": item.get("id"), "actor": login, "marker": first,
                    "created_at": item.get("created_at"), "exact_head_present": head in body,
                }
            )
        if login in allowed and first.startswith("HUMAN_STEWARD_") and head in body:
            candidates.append(item)
    candidates.sort(key=lambda x: (str(x.get("created_at") or ""), int(x.get("id") or 0)))
    if not candidates:
        return {
            "required": False, "state": "UNKNOWN", "comment_id": None,
            "actor": None, "commit_sha": None, "disposition": None,
        }, observed
    item = candidates[-1]
    marker = str(item.get("body") or "").splitlines()[0].strip()
    state = "DECLINED" if any(x in marker.upper() for x in ("DECLIN", "REJECT")) else "AUTHORIZED"
    return {
        "required": True, "state": state, "comment_id": int(item["id"]),
        "actor": str(item.get("user", {}).get("login") or "unknown"),
        "commit_sha": head, "disposition": marker,
    }, observed


def integration_state(
    client: Client, repo: str, pr: dict[str, Any], config: dict[str, Any]
) -> dict[str, Any]:
    merged, state = bool(pr.get("merged")), str(pr.get("state") or "").lower()
    merge_sha = pr.get("merge_commit_sha")
    merge_state = "MERGED" if merged else ("CLOSED_UNMERGED" if state == "closed" else ("OPEN" if state == "open" else "UNKNOWN"))
    if not config.get("protected_readback_required", True):
        readback = {"required": False, "state": "NOT_APPLICABLE", "main_sha": None}
    elif merge_state == "MERGED" and isinstance(merge_sha, str):
        main = client.get(f"/repos/{repo}/branches/main")
        main_sha = str(main.get("commit", {}).get("sha") or "")
        readback = {
            "required": True,
            "state": "COMPLETE" if main_sha == merge_sha else "PENDING",
            "main_sha": main_sha if re.fullmatch(r"[0-9a-f]{40}", main_sha) else None,
        }
    else:
        readback = {"required": True, "state": "PENDING", "main_sha": None}
    return {
        "merge_state": merge_state,
        "merge_commit_sha": merge_sha if isinstance(merge_sha, str) and re.fullmatch(r"[0-9a-f]{40}", merge_sha) else None,
        "protected_readback": readback,
    }


def collect_report(
    client: Client, repo: str, pr_number: int, observed_at: str, config: dict[str, Any]
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    if repo != ALLOWED_REPOSITORY:
        raise OperationalError(f"repository {repo!r} is outside Phase 1 authority")
    pr = client.get(f"/repos/{repo}/pulls/{pr_number}")
    if not isinstance(pr, dict) or int(pr.get("number") or 0) != pr_number:
        raise OperationalError("pull request readback failed")
    head = str(pr.get("head", {}).get("sha") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise OperationalError("exact PR head is unavailable")
    files = paged(client, f"/repos/{repo}/pulls/{pr_number}/files?")
    override, limitations = governed_override(client, repo, pr_number, head, config)
    significance = policy.classify_significance(significance_signals(pr, files, override))
    summary: dict[str, Any] = {
        "selected": bool(significance["significant"]), "repository": repo,
        "pr_number": pr_number, "exact_head_sha": head,
        "significance": significance, "limitations": limitations,
    }
    if not significance["significant"]:
        return None, summary

    rulesets, ruleset_error = active_rulesets(client, repo)
    contexts, review_required = ruleset_requirements(rulesets)
    if ruleset_error:
        review_required = None
    checks, observed_checks = check_records(client, repo, head, contexts)
    review, observed_reviews = review_authority(client, repo, pr, review_required)
    steward, observed_steward = steward_authority(client, repo, pr, config)

    blockers = []
    if ruleset_error:
        blockers.append(
            {
                "id": "PRVSR-SOURCE-RULESET-UNAVAILABLE", "status": "OPEN",
                "summary": "Required-check/review ruleset source is unavailable; advisory state fails closed.",
            }
        )
        limitations.append(ruleset_error)
    for label in pr.get("labels", []):
        name = str(label.get("name") or "")
        if "blocker" in name.lower() or name.lower() in {"blocked", "do-not-merge"}:
            blockers.append(
                {
                    "id": f"PR-LABEL-{re.sub(r'[^A-Za-z0-9_.-]+', '-', name).strip('-') or 'BLOCKED'}",
                    "status": "OPEN", "summary": f"PR carries blocker-like label {name!r}.",
                }
            )

    report_id = f"PRVSR-LIVE-PR{pr_number}-{head[:12]}-{re.sub(r'[^0-9]', '', observed_at)[:14]}"
    history = []
    if pr.get("created_at"):
        history.append({"at": str(pr["created_at"]), "event": "PR_CREATED", "outcome": "RETAINED"})
    if pr.get("updated_at"):
        history.append({"at": str(pr["updated_at"]), "event": "PR_UPDATED", "outcome": "RETAINED"})
    report = {
        "report_id": report_id,
        "identity": {
            "repository": repo, "pr_number": pr_number,
            "title": str(pr.get("title") or f"PR #{pr_number}"),
            "exact_head_sha": head, "current_head_sha": head,
        },
        "significance": significance,
        "authority": {"independent_review": review, "human_steward": steward},
        "checks": checks,
        "integration": integration_state(client, repo, pr, config),
        "blockers": blockers,
        "nonclaims": [
            "PRVSR is advisory and derived; authoritative GitHub/governance records remain controlling.",
            "Report absence, staleness, generation failure, render failure, or archive failure is not a merge blocker.",
            "No cross-repository propagation authority is created.",
            "No claim is made that reviewer speed or factual accuracy improves.",
            "Machine collection does not infer missing human, mathematical, source-admission, or certification authority.",
        ],
        "history": history[-8:],
        "modules": {
            "phase1": {
                "operation": "PRVSR-PHASE1-IMPLEMENTATION-001", "issue": 462,
                "config_version": str(config["schema_version"]),
                "ruleset_source_available": ruleset_error is None,
                "required_status_contexts": sorted(contexts),
                "changed_file_count": len(files),
                "observed_check_runs": observed_checks,
                "observed_non_author_reviews": observed_reviews[-20:],
                "observed_human_steward_markers": observed_steward[-20:],
                "collector_limitations": limitations,
            }
        },
        "provenance": {"observed_at": observed_at},
    }
    sealed = policy.seal_report(report)
    summary.update(
        report_id=report_id,
        operative_state=sealed["derived"]["operative_state"],
        freshness=sealed["derived"]["freshness"],
    )
    return sealed, summary


def branch_info(client: Client, repo: str, branch: str) -> dict[str, Any] | None:
    try:
        value = client.get(f"/repos/{repo}/branches/{urllib.parse.quote(branch, safe='')}")
    except AutonomyError as exc:
        if " 404 " in str(exc):
            return None
        raise
    return value if isinstance(value, dict) else None


def ensure_archive_branch(client: Client, repo: str, branch: str) -> str:
    current = branch_info(client, repo, branch)
    if current:
        return str(current["commit"]["sha"])
    main = client.get(f"/repos/{repo}/branches/main")
    sha = str(main.get("commit", {}).get("sha") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise OperationalError("cannot seed archive branch")
    client.post(f"/repos/{repo}/git/refs", {"ref": f"refs/heads/{branch}", "sha": sha})
    current = branch_info(client, repo, branch)
    if not current:
        raise OperationalError("archive branch creation readback failed")
    return str(current["commit"]["sha"])


def commit_bundle(
    client: Client, repo: str, branch: str, bundle_dir: Path, archive_dir: str, report_id: str
) -> str:
    parent = ensure_archive_branch(client, repo, branch)
    commit = client.get(f"/repos/{repo}/git/commits/{parent}")
    base_tree = str(commit.get("tree", {}).get("sha") or "")
    entries = []
    for name in ("report.json", "report.txt", "report.svg", "receipt.json"):
        data = (bundle_dir / name).read_bytes()
        blob = client.post(
            f"/repos/{repo}/git/blobs",
            {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"},
        )
        entries.append(
            {"path": f"{archive_dir}/{name}", "mode": "100644", "type": "blob", "sha": blob["sha"]}
        )
    tree = client.post(f"/repos/{repo}/git/trees", {"base_tree": base_tree, "tree": entries})
    new = client.post(
        f"/repos/{repo}/git/commits",
        {"message": f"Archive advisory PRVSR report {report_id}", "tree": tree["sha"], "parents": [parent]},
    )
    client.patch(
        f"/repos/{repo}/git/refs/heads/{urllib.parse.quote(branch, safe='/')}",
        {"sha": new["sha"], "force": False},
    )
    return str(new["sha"])


def invalidate_receipt(
    client: Client, repo: str, branch: str, archive_dir: str, replacement_head: str
) -> None:
    info = branch_info(client, repo, branch)
    if not info:
        return
    parent = str(info["commit"]["sha"])
    commit = client.get(f"/repos/{repo}/git/commits/{parent}")
    blob = client.post(
        f"/repos/{repo}/git/blobs",
        {
            "content": base64.b64encode(
                f"Target PR head moved during publication to {replacement_head}.\n".encode()
            ).decode("ascii"),
            "encoding": "base64",
        },
    )
    tree = client.post(
        f"/repos/{repo}/git/trees",
        {
            "base_tree": commit["tree"]["sha"],
            "tree": [
                {"path": f"{archive_dir}/receipt.json", "mode": "100644", "type": "blob", "sha": None},
                {"path": f"{archive_dir}/INVALIDATED.txt", "mode": "100644", "type": "blob", "sha": blob["sha"]},
            ],
        },
    )
    new = client.post(
        f"/repos/{repo}/git/commits",
        {"message": "Invalidate stale advisory PRVSR receipt", "tree": tree["sha"], "parents": [parent]},
    )
    client.patch(
        f"/repos/{repo}/git/refs/heads/{urllib.parse.quote(branch, safe='/')}",
        {"sha": new["sha"], "force": False},
    )


def upsert_comment(client: Client, repo: str, pr_number: int, body: str) -> int:
    marker = COMMENT_MARKER.format(pr_number=pr_number)
    comments = paged(client, f"/repos/{repo}/issues/{pr_number}/comments?")
    for item in reversed(comments):
        if marker in str(item.get("body") or "") and str(item.get("user", {}).get("login") or "") == "github-actions[bot]":
            value = client.patch(
                f"/repos/{repo}/issues/comments/{item['id']}", {"body": f"{marker}\n{body}"}
            )
            return int(value["id"])
    value = client.post(
        f"/repos/{repo}/issues/{pr_number}/comments", {"body": f"{marker}\n{body}"}
    )
    return int(value["id"])


def publish_report(
    client: Client, repo: str, pr_number: int, report: dict[str, Any],
    output_root: Path, config: dict[str, Any]
) -> dict[str, Any]:
    exact = report["identity"]["exact_head_sha"]
    before = client.get(f"/repos/{repo}/pulls/{pr_number}")
    if str(before.get("head", {}).get("sha") or "") != exact:
        raise OperationalError("target PR head moved before archive publication")
    bundle_dir = transport.write_archive_bundle(
        report, output_root, target_head_before=exact, target_head_after=exact
    )
    archive_dir = transport.archive_relative_dir(report)
    branch = f"{config['archive_branch_prefix']}{pr_number}"
    archive_commit = commit_bundle(
        client, repo, branch, bundle_dir, archive_dir, report["report_id"]
    )
    after = client.get(f"/repos/{repo}/pulls/{pr_number}")
    after_head = str(after.get("head", {}).get("sha") or "")
    if after_head != exact:
        invalidate_receipt(client, repo, branch, archive_dir, after_head)
        raise OperationalError("target PR head moved during publication; receipt invalidated")
    comment = transport.render_verified_pr_comment(bundle_dir)
    comment += (
        f"\nPhase 1 archive branch: `{branch}`\n"
        f"Archive path: `{archive_dir}/`\n"
        "Report generation or archive failure remains advisory and non-blocking.\n"
    )
    return {
        "archive_branch": branch,
        "archive_commit": archive_commit,
        "archive_dir": archive_dir,
        "comment_id": upsert_comment(client, repo, pr_number, comment),
    }


def write_summary(path: str | None, value: dict[str, Any]) -> None:
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    print(text, end="")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ALLOWED_REPOSITORY))
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--observed-at")
    parser.add_argument("--output-root", default=".")
    parser.add_argument("--summary")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    if not args.token:
        parser.error("--token or GITHUB_TOKEN is required")
    client = Client(args.token)
    config = load_config()
    try:
        report, summary = collect_report(
            client, args.repo, args.pr, args.observed_at or utc_now(), config
        )
        if report is not None:
            if args.publish:
                summary["publication"] = publish_report(
                    client, args.repo, args.pr, report, Path(args.output_root), config
                )
            else:
                path = transport.write_archive_bundle(
                    report, Path(args.output_root),
                    target_head_before=report["identity"]["exact_head_sha"],
                    target_head_after=report["identity"]["exact_head_sha"],
                )
                summary["local_bundle_dir"] = path.as_posix()
        write_summary(args.summary, summary)
        return 0
    except (AutonomyError, OperationalError, policy.ReportError, transport.TransportError, OSError) as exc:
        write_summary(
            args.summary,
            {
                "selected": None, "repository": args.repo, "pr_number": args.pr,
                "error": str(exc),
                "authority_boundary": "ADVISORY_FAILURE__NO_MERGE_BLOCKER_CREATED",
            },
        )
        print(f"PRVSR Phase 1 advisory error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
