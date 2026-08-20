from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "governance" / "rebuild_evidence" / "MP-ADMIN-WORKFLOW-REBUILD-001"
ATTESTATION = BUNDLE / "attestation.json"
SCHEMA = ROOT / "schemas" / "administrative_workflow_rebuild_attestation.schema.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate() -> list[str]:
    errors: list[str] = []
    try:
        att = _load(ATTESTATION)
        schema = _load(SCHEMA)
        Draft202012Validator.check_schema(schema)
        for failure in sorted(
            Draft202012Validator(schema).iter_errors(att),
            key=lambda e: list(e.absolute_path),
        ):
            loc = ".".join(str(p) for p in failure.absolute_path) or "$"
            errors.append(f"rebuild_attestation:{loc}: {failure.message}")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"rebuild_attestation: unreadable package: {exc}"]

    artifacts = att.get("retained_actions_artifacts", {})
    loaded: dict[str, tuple[dict, dict]] = {}
    for stage in ("pre_reactivation", "post_reactivation"):
        info = artifacts.get(stage, {})
        qpath = ROOT / str(info.get("qualification_path", ""))
        rpath = ROOT / str(info.get("reconciliation_path", ""))
        for label, path, expected in (
            ("qualification", qpath, info.get("qualification_sha256")),
            ("reconciliation", rpath, info.get("reconciliation_sha256")),
        ):
            if not path.is_file():
                errors.append(f"{stage}:{label}: retained payload missing: {path}")
                continue
            observed = _sha256(path)
            if observed != expected:
                errors.append(f"{stage}:{label}: sha256 drift: {observed} != {expected}")
        if qpath.is_file() and rpath.is_file():
            loaded[stage] = (_load(qpath), _load(rpath))

    expected = {
        "pre_reactivation": {
            "head": "ce370735fa05fb55b5e38c19870ff23c91578110",
            "run": "32349281060",
            "artifact": "97079a9e1eb5b5f1d4e6d904bc7fff21672ad62be043c6883f19f87aef8ca021",
        },
        "post_reactivation": {
            "head": "e052be7f100976d25694019b55dfafc0a3bec954",
            "run": "32351044135",
            "artifact": "0f72cc095f33ca21dd2774db27977d5ddf4ae298f354bc67f92e4eb1f7e96203",
        },
    }
    for stage, (qualification, reconciliation) in loaded.items():
        exp = expected[stage]
        info = artifacts[stage]
        if info.get("archive_sha256") != exp["artifact"]:
            errors.append(f"{stage}: original archive digest drift")
        if qualification.get("state") != "LIVE_QUALIFICATION_GREEN__REACTIVATION_NOT_AUTHORIZED":
            errors.append(f"{stage}: qualification is not green")
        if (
            qualification.get("protected_head_end") != exp["head"]
            or qualification.get("protected_head_start") != exp["head"]
        ):
            errors.append(f"{stage}: qualification protected-head drift")
        if qualification.get("run_identity", {}).get("github_run_id") != exp["run"]:
            errors.append(f"{stage}: qualification run identity drift")
        if qualification.get("idempotency", {}).get("stable") is not True:
            errors.append(f"{stage}: qualification idempotency is not stable")
        identities = qualification.get("first_pass", {}).get("identities", {})
        if identities.get("role_separation_valid") is not True:
            errors.append(f"{stage}: actor role separation not proved")
        if identities.get("referee", {}).get("identity", {}).get("login") != "github-actions[bot]":
            errors.append(f"{stage}: referee identity drift")
        if identities.get("candidate", {}).get("identity", {}).get("login") != "gcl-release-trust[bot]":
            errors.append(f"{stage}: candidate identity drift")
        if reconciliation.get("terminal_state") != "RULESET_ACTOR_ALREADY_PRESENT__NO_MUTATION":
            errors.append(f"{stage}: ruleset reconciliation terminal state drift")
        target = reconciliation.get("target_actor", {})
        if (
            target.get("actor_id"),
            target.get("actor_type"),
            target.get("bypass_mode"),
        ) != (4423678, "Integration", "pull_request"):
            errors.append(f"{stage}: exact ruleset actor drift")
        if reconciliation.get("mutation_performed") is not False:
            errors.append(f"{stage}: unexpected ruleset mutation")
        for key in (
            "direct_protected_push",
            "bypass_exercised",
            "receipt_mutation_performed",
            "ledger_mutation_performed",
            "mirror_mutation_performed",
        ):
            if reconciliation.get(key) is not False:
                errors.append(f"{stage}: forbidden effect recorded: {key}")

    self_test = att.get("steady_state_self_test", {})
    real = att.get("real_transition_confirmation", {})
    if (
        self_test.get("pull_request") != 626
        or self_test.get("exact_head") != "e40f8ba7c39bf469498a9db0429d368ed24993e7"
    ):
        errors.append("self-test identity drift")
    if self_test.get("protected_merge_commit") != expected["pre_reactivation"]["head"]:
        errors.append("self-test protected merge does not bind pre-reactivation qualification")
    if (
        real.get("pull_request") != 627
        or real.get("exact_head") != "f0a6c92aecf35c40e32c2044c7bd9d0e1ef68fb2"
    ):
        errors.append("real-transition identity drift")
    if real.get("protected_base") != self_test.get("protected_merge_commit"):
        errors.append("real transition does not descend from self-test protected merge")
    if real.get("protected_merge_commit") != expected["post_reactivation"]["head"]:
        errors.append("real-transition protected merge does not bind post-reactivation qualification")
    if att.get("protected_readback", {}).get("protected_head") != real.get("protected_merge_commit"):
        errors.append("protected readback does not bind real-transition merge")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(
            f"administrative workflow rebuild evidence validation failed with {len(errors)} error(s)",
            file=sys.stderr,
        )
        return 1
    print("MP-ADMIN-WORKFLOW-REBUILD-EVIDENCE-001: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
