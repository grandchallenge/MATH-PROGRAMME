from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

UTC = timezone.utc
ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "administrative_maintenance_trigger_registry.json"
REPORT_PATH = ROOT / "administrative-maintenance-dispatch.json"

SELF_TITLE_PREFIX = "[maintenance-dispatch]"
SELF_MARKER_PREFIX = "<!-- maintenance-dispatch:"
TRACKER_REFRESH = timedelta(minutes=432)

PROCEDURE_TITLES = {
    "structural_sweep": "structural sweep",
    "administrative_review": "administrative portfolio review",
    "deep_conformance_review": "deep conformance review",
    "pilot_review": "accelerated pilot review",
    "constitutional_review": "constitutional review",
}


@dataclass(frozen=True)
class Dispatch:
    kind: str
    key: str
    title: str
    body: str
    severity: str
    due_at: str | None
    source_event: str


def parse_datetime(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"time must include an offset: {value}")
    return parsed.astimezone(UTC)


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_event(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def due_occurrences(procedure: dict[str, Any], now: datetime) -> list[datetime]:
    first_due = parse_datetime(procedure["first_due_utc"])
    active_through = parse_datetime(procedure["active_through_utc"])
    completed_raw = procedure["completed_through_utc"]
    completed_through = parse_datetime(completed_raw) if completed_raw else None

    if now < first_due:
        return []

    upper = min(now, active_through)
    if upper < first_due:
        return []

    interval_minutes = procedure["interval_minutes"]
    if interval_minutes is None:
        candidates = [first_due]
    else:
        interval = timedelta(minutes=interval_minutes)
        count = int((upper - first_due) // interval)
        candidates = [first_due + index * interval for index in range(count + 1)]

    return [
        candidate
        for candidate in candidates
        if candidate <= upper and (completed_through is None or candidate > completed_through)
    ]


def marker(key: str) -> str:
    return f"{SELF_MARKER_PREFIX}{key} -->"


def scheduled_dispatch(procedure: dict[str, Any], due: datetime, now: datetime) -> Dispatch:
    procedure_id = procedure["id"]
    title_name = PROCEDURE_TITLES[procedure_id]
    due_text = iso_z(due)
    late_minutes = max(0, int((now - due).total_seconds() // 60))
    key = f"scheduled:{procedure_id}:{due_text}"
    severity = "P2" if "P2" in procedure["issue_class"] else "P1"
    body = f"""{marker(key)}
## Administrative maintenance dispatch

This issue is a mutable execution notice only. It creates no protected authority and does not satisfy the required procedure.

- control: `MP-ADMIN-MAINT-001`
- procedure: `{procedure_id}`
- scheduled due time: `{due_text}`
- dispatch evaluation time: `{iso_z(now)}`
- lateness at dispatch: `{late_minutes}` minutes
- default classification if not completed: `{procedure["issue_class"]}`
- required output: {procedure["required_output"]}

## Required action

Execute the {title_name} against the exact current protected heads. Preserve the original cadence anchor and record the scheduled deadline, actual execution time, evidence, findings, repairs, review disposition, and claim boundary.

A delayed workflow run or this issue cannot rewrite the deadline, grant a waiver, reset cadence, merge a pull request, or create mathematical, certification, novelty, priority, publication, patentability, product, or commercial authority.
"""
    return Dispatch(
        kind="scheduled",
        key=key,
        title=f"{SELF_TITLE_PREFIX} {title_name} due {due_text}",
        body=body,
        severity=severity,
        due_at=due_text,
        source_event="schedule",
    )


def manual_dispatch(procedure_id: str, now: datetime, registry: dict[str, Any]) -> Dispatch:
    match = next(item for item in registry["procedures"] if item["id"] == procedure_id)
    key = f"manual:{procedure_id}:{iso_z(now)}"
    title_name = PROCEDURE_TITLES[procedure_id]
    body = f"""{marker(key)}
## Manual administrative maintenance dispatch

This recovery notice is non-authoritative. It does not reset the protected cadence.

- control: `MP-ADMIN-MAINT-001`
- procedure: `{procedure_id}`
- requested at: `{iso_z(now)}`
- required output: {match["required_output"]}

Execute the procedure against exact protected heads and record whether it is early, on time, or late relative to the protected schedule.
"""
    return Dispatch(
        kind="manual",
        key=key,
        title=f"{SELF_TITLE_PREFIX} manual {title_name} {iso_z(now)}",
        body=body,
        severity="P2",
        due_at=None,
        source_event="workflow_dispatch",
    )


def event_name_from_environment() -> str:
    return os.environ.get("GITHUB_EVENT_NAME", "").strip() or "unknown"


def own_issue_event(event: dict[str, Any]) -> bool:
    issue = event.get("issue") or {}
    title = str(issue.get("title") or "")
    body = str(issue.get("body") or "")
    return title.startswith(SELF_TITLE_PREFIX) or SELF_MARKER_PREFIX in body


def suspicious_issue_authority(event: dict[str, Any]) -> list[str]:
    if own_issue_event(event):
        return []

    issue = event.get("issue") or {}
    text = f"{issue.get('title') or ''}\n{issue.get('body') or ''}"
    patterns = {
        "may_adjudicate_true": r"\bmay_adjudicate\s*[:=]\s*true\b",
        "proved_target_true": r"\b(?:mathematical_target_proved|proved_target)\s*[:=]\s*true\b",
        "issue_claims_authority": r"\b(?:this issue|issue text)\b.{0,80}\b(?:is authoritative|creates authority|grants authority)\b",
        "non_null_cert_output": r"\bcert_output\s*[:=]\s*(?!null\b|none\b)[^\s,}\]]+",
    }
    return [name for name, pattern in patterns.items() if re.search(pattern, text, re.I | re.S)]


def event_dispatches(
    event_name: str,
    event: dict[str, Any],
    now: datetime,
) -> list[Dispatch]:
    dispatches: list[Dispatch] = []

    if event_name == "push":
        sha = str(event.get("after") or os.environ.get("GITHUB_SHA") or "unknown")
        key = f"event:push:{sha}"
        refresh_due = now + TRACKER_REFRESH
        body = f"""{marker(key)}
## Governed-path material-change triage

A push to `main` changed a governed path and triggered immediate maintenance triage.

- commit: `{sha}`
- observed at: `{iso_z(now)}`
- canonical tracker refresh target: `{iso_z(refresh_due)}`
- protected material synchronization: same governed change sequence

Classify the change as material or nonmaterial, identify affected consumers, verify exact-head evidence, preserve unchanged content-addressed identities, and create protected synchronization records where required. This issue is navigation only and cannot create authority.
"""
        dispatches.append(
            Dispatch(
                kind="event",
                key=key,
                title=f"{SELF_TITLE_PREFIX} governed-path synchronization triage {sha[:12]}",
                body=body,
                severity="P2",
                due_at=iso_z(refresh_due),
                source_event=event_name,
            )
        )

    elif event_name == "branch_protection_rule":
        action = str(event.get("action") or "changed")
        rule = event.get("rule") or {}
        name = str(rule.get("name") or rule.get("pattern") or "unknown")
        key = f"event:branch-protection:{action}:{name}:{iso_z(now)}"
        body = f"""{marker(key)}
## Branch-protection semantic review

A branch-protection rule was `{action}`.

- rule: `{name}`
- observed at: `{iso_z(now)}`
- default classification: `P1` until required-check and release-trust effects are reconciled

Verify required checks, review requirements, bypass actors, force-push and deletion settings, downstream workflow coverage, and exact protected authority. This issue cannot authorize weakening.
"""
        dispatches.append(
            Dispatch(
                kind="event",
                key=key,
                title=f"{SELF_TITLE_PREFIX} P1 branch-protection review: {action} {name}",
                body=body,
                severity="P1",
                due_at=iso_z(now),
                source_event=event_name,
            )
        )

    elif event_name == "workflow_run":
        run = event.get("workflow_run") or {}
        conclusion = str(run.get("conclusion") or "")
        if conclusion and conclusion != "success":
            run_id = str(run.get("id") or "unknown")
            workflow_name = str(run.get("name") or "required workflow")
            key = f"event:workflow-failure:{run_id}"
            body = f"""{marker(key)}
## Required-workflow failure triage

- workflow: `{workflow_name}`
- run id: `{run_id}`
- conclusion: `{conclusion}`
- observed at: `{iso_z(now)}`
- classification: `P1` until the required evidence lane is restored or governed non-applicability is established

Preserve failure evidence, identify affected protected records and campaigns, fail closed where required, repair at a new exact head, and obtain any required review.
"""
            dispatches.append(
                Dispatch(
                    kind="event",
                    key=key,
                    title=f"{SELF_TITLE_PREFIX} P1 required-workflow failure {workflow_name} #{run_id}",
                    body=body,
                    severity="P1",
                    due_at=iso_z(now),
                    source_event=event_name,
                )
            )

    elif event_name == "issues":
        findings = suspicious_issue_authority(event)
        if findings:
            issue = event.get("issue") or {}
            number = str(issue.get("number") or "unknown")
            action = str(event.get("action") or "changed")
            key = f"event:issue-authority:{number}:{action}:{iso_z(now)}"
            body = f"""{marker(key)}
## Issue-language authority triage

Issue #{number} matched protected-authority risk patterns after action `{action}`.

- patterns: {", ".join(f"`{item}`" for item in findings)}
- observed at: `{iso_z(now)}`
- default classification: `P1` until issue wording is reconciled with protected records

Confirm that the issue is navigation only, identify the controlling protected record and exact identity, and remove or qualify any language that could imply mutable issue authority.
"""
            dispatches.append(
                Dispatch(
                    kind="event",
                    key=key,
                    title=f"{SELF_TITLE_PREFIX} P1 issue-authority language review #{number}",
                    body=body,
                    severity="P1",
                    due_at=iso_z(now),
                    source_event=event_name,
                )
            )

    return dispatches


class GitHubIssues:
    def __init__(self, repository: str, token: str) -> None:
        self.repository = repository
        self.token = token
        self.api = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
        self._markers: set[str] | None = None

    def request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        url = f"{self.api}{path}"
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "gcl-administrative-maintenance-dispatcher",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API {method} {path} failed: {exc.code} {detail}") from exc

    def existing_markers(self) -> set[str]:
        if self._markers is not None:
            return self._markers

        markers: set[str] = set()
        for page in range(1, 11):
            query = urllib.parse.urlencode(
                {
                    "state": "all",
                    "per_page": 100,
                    "page": page,
                    "sort": "created",
                    "direction": "desc",
                }
            )
            items = self.request("GET", f"/repos/{self.repository}/issues?{query}")
            if not items:
                break
            for item in items:
                body = str(item.get("body") or "")
                for match in re.findall(r"<!-- maintenance-dispatch:([^>]+) -->", body):
                    markers.add(match)
            if len(items) < 100:
                break

        self._markers = markers
        return markers

    def ensure_issue(self, dispatch: Dispatch, label: str) -> str:
        if dispatch.key in self.existing_markers():
            return "duplicate"

        self.request(
            "POST",
            f"/repos/{self.repository}/issues",
            {
                "title": dispatch.title,
                "body": dispatch.body,
                "labels": [label],
            },
        )
        self.existing_markers().add(dispatch.key)
        return "created"


def deduplicate(dispatches: Iterable[Dispatch]) -> list[Dispatch]:
    seen: set[str] = set()
    result: list[Dispatch] = []
    for dispatch in dispatches:
        if dispatch.key not in seen:
            seen.add(dispatch.key)
            result.append(dispatch)
    return result


def build_dispatches(
    registry: dict[str, Any],
    event_name: str,
    event: dict[str, Any],
    now: datetime,
    manual_procedure: str,
) -> list[Dispatch]:
    dispatches: list[Dispatch] = []

    if event_name == "schedule" or (event_name == "workflow_dispatch" and manual_procedure == "auto"):
        for procedure in registry["procedures"]:
            for due in due_occurrences(procedure, now):
                dispatches.append(scheduled_dispatch(procedure, due, now))

    if event_name == "workflow_dispatch" and manual_procedure != "auto":
        dispatches.append(manual_dispatch(manual_procedure, now, registry))

    dispatches.extend(event_dispatches(event_name, event, now))
    return deduplicate(dispatches)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-path", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--token", default="")
    parser.add_argument("--procedure", default="auto")
    parser.add_argument("--now", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    registry = load_registry()
    event = load_event(args.event_path)
    event_name = event_name_from_environment()
    now = parse_datetime(args.now) if args.now else datetime.now(UTC)

    allowed = {"auto", *(item["id"] for item in registry["procedures"])}
    if args.procedure not in allowed:
        raise SystemExit(f"unsupported procedure: {args.procedure}")

    dispatches = build_dispatches(registry, event_name, event, now, args.procedure)
    results: list[dict[str, Any]] = []

    client: GitHubIssues | None = None
    if not args.dry_run and dispatches:
        if not args.token:
            raise SystemExit("GitHub token is required when dispatches must create issues")
        client = GitHubIssues(args.repository, args.token)

    for dispatch in dispatches:
        disposition = "dry_run"
        if client is not None:
            disposition = client.ensure_issue(dispatch, registry["dispatch"]["default_label"])
        results.append({**asdict(dispatch), "disposition": disposition})

    report = {
        "schema_version": "1.0.0",
        "control_id": registry["control_id"],
        "trigger_id": registry["trigger_id"],
        "evaluated_at": iso_z(now),
        "event_name": event_name,
        "manual_procedure": args.procedure,
        "dry_run": args.dry_run,
        "dispatch_count": len(results),
        "dispatches": results,
        "authority_boundary": {
            "issue_is_navigation_only": True,
            "protected_record_required": True,
            "schedule_anchor_reset": False,
            "claim_promotion": False,
        },
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as handle:
            handle.write(f"dispatch_count={len(results)}\n")
            handle.write(f"report={args.report.as_posix()}\n")

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
