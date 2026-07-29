#!/usr/bin/env python3
"""Validate the programme umbrella audit and its exact closure conditions."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "governance" / "workflow_coverage_audit.json"
SCHEMA_PATH = ROOT / "schemas" / "workflow_coverage_audit.schema.json"
EXPECTED_PROGRAMME_BASE = "8b965d2e8913ed1252f37dc83de8456a335cedd9"
EXPECTED_AREAS = {
    "GLOBAL-POLICY",
    "CAMPAIGN-REPLAY-DISCOVERY",
    "CI-REACHABILITY",
    "REPOSITORY-TESTS",
    "EXPERIMENT-REACHABILITY",
    "SYMBOLIC-BUDGETS",
    "CROSS-PILLAR-LANES",
    "MATHFORGE-PROVIDER-IMPORTS",
    "MATHSOLVE-ROUTING",
    "MATHCERT-CONFORMANCE",
    "MATHFORGE-BOUNDED-WITNESS",
    "MATHSOLVE-BOUNDED-TACTIC",
    "FORMAL-REPLAYS",
    "EXTERNAL-MATHCERT-EVIDENCE",
    "STRICT-DOCUMENTATION-BUILD",
    "PAGES-PUBLICATION-CONTRACT",
    "RELEASE-TRUST-EVIDENCE",
    "FAST-PATH-WORKFLOWS",
}
EXPECTED_CHILDREN = {
    ("grandchallenge/MATH-PROGRAMME", 7),
    ("grandchallenge/MATH-PROGRAMME", 125),
    ("grandchallenge/MATHFORGE", 6),
    ("grandchallenge/MATHSOLVE", 6),
}
EXPECTED_ADMINISTRATIVE_IMPLEMENTATION = {
    "release_trust_workflow_run_id": 30446399649,
    "release_trust_artifact_id": 8721612194,
    "evidence_sha256": "a3cfeea6a58de0e193015b96fd5929567bae9a3ee2aca68efe52795474669a85",
}
EXPECTED_RELEASE_TRUST_EVIDENCE = {
    "contract_id": "ORG-REL-TRUST-01",
    "evidence_id": "ORG-REL-TRUST-01-EVIDENCE",
    "generated_at": "2026-07-29T11:09:00.207599+00:00",
    "workflow_run_id": 30446399649,
    "workflow_run_url": "https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30446399649",
    "workflow_head_sha": "8b965d2e8913ed1252f37dc83de8456a335cedd9",
    "artifact_id": 8721612194,
    "artifact_url": "https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/actions/artifacts/8721612194",
    "artifact_sha256": "719c28ea73b69cfcb07049988ab48f231c235160e8c2b01f48761b49623ac33e",
    "evidence_file_sha256": "6c09d735c3b4f1ee4f5f53031658183ebc7a98a65fecc9c0eb9eca6a8ded2e74",
    "evidence_sha256": "a3cfeea6a58de0e193015b96fd5929567bae9a3ee2aca68efe52795474669a85",
    "contract_sha256": "1eb8c72397f6f4922df1a89cb9cf592ed87b93bd5e1b8c1a1854539fde2315e0",
    "policy_workflow_run_id": 30446169969,
    "pages_workflow_run_id": 30446339153,
    "validated_site_artifact_id": 8721515246,
    "validated_site_artifact_sha256": "b2ef8d7fb07fa1190e3fff52b5a3477e8fcf3510cad22217290edbff23beedd1",
    "site_archive_sha256": "a771b421510d925e16a4da966fb26d91c68ca9ae87b5c4e56f3c417313b6d445",
    "index_sha256": "9a54a3831d6fb0922b1e21a792c246051d1d8f078621fac5da5e87cdd59535c7",
    "live_index_sha256": "9a54a3831d6fb0922b1e21a792c246051d1d8f078621fac5da5e87cdd59535c7",
    "repository_rulesets": [
        {
            "repository": "grandchallenge/MATHCERT",
            "snapshot_sha256": "7603eb6ad0ddb61ce41a2e81f8f7313ac43e822c11892dd32ed0e8266522ad5d",
        },
        {
            "repository": "grandchallenge/MATHSOLVE",
            "snapshot_sha256": "4801f0b22bde3695ec152e3981ab8d7137eb1c73abc98da27c2bc4263112dd76",
        },
        {
            "repository": "grandchallenge/MATH-PROGRAMME",
            "snapshot_sha256": "7274655588e344e6e8c0504611ab9ff7486ac245368690eabdf50b4fb11ccb92",
        },
        {
            "repository": "grandchallenge/INTELLECT",
            "snapshot_sha256": "3ed304398948814f7c9b3ef6afb66bf8ce2a61c0c60833d880fc937b3398e53c",
        },
    ],
    "verified": True,
}
EXPECTED_TECHNICAL_IMPLEMENTATIONS = {
    ("grandchallenge/MATHFORGE", 6): {
        "pull_request": 25,
        "tested_head": "95be2b36d1cfb6f64c3f4e64c0b5c71d2ef2def6",
        "merge_commit": "5d6461b6812dd9a99d73ddf98904c33465bffca0",
        "workflow_run_id": 30426791431,
        "schema": {
            "path": "schemas/algebraic_witness.schema.json",
            "git_blob_sha1": "517d96566f35a0563c2b4059338aac0738a0a1b7",
        },
        "registry": {
            "path": "governance/algebraic_witness_registry.json",
            "git_blob_sha1": "022ebb5dbffa6685aef1dcb9bea8b1d338c5e7ec",
        },
    },
    ("grandchallenge/MATHSOLVE", 6): {
        "pull_request": 77,
        "tested_head": "107312712da7fce228c7100c7d15a1ee45bae03a",
        "merge_commit": "1f763c3a554814f40806a424e8b2c83f3ec8d24e",
        "workflow_run_id": 30427137579,
        "schema": {
            "path": "schemas/grobner_tactic_invocation.schema.json",
            "git_blob_sha1": "845117b233ddb5676d59f0e2e6a43f8e17abb497",
        },
        "registry": {
            "path": "governance/grobner_tactic_registry.json",
            "git_blob_sha1": "5ee8b1aa596172f3c7d96126e93809bc80e1dcda",
        },
    },
}


class WorkflowCoverageAuditError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise WorkflowCoverageAuditError(message)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path = ROOT) -> None:
    audit = load(root / "governance/workflow_coverage_audit.json")
    schema = load(root / "schemas/workflow_coverage_audit.schema.json")
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(audit),
        key=lambda error: list(error.path),
    )
    require(not errors, "; ".join(f"{error.json_path}: {error.message}" for error in errors))
    require(
        audit["programme_main_commit"] == EXPECTED_PROGRAMME_BASE,
        "umbrella audit base commit drift",
    )
    require(
        audit["release_trust_evidence"] == EXPECTED_RELEASE_TRUST_EVIDENCE,
        "release-trust evidence identity drift",
    )

    areas = audit["coverage_areas"]
    area_ids = [area["area_id"] for area in areas]
    require(len(area_ids) == len(set(area_ids)), "workflow coverage audit has duplicate area IDs")
    require(set(area_ids) == EXPECTED_AREAS, "workflow coverage area set drift")

    children = audit["children"]
    child_keys = [(child["repository"], child["issue"]) for child in children]
    require(len(child_keys) == len(set(child_keys)), "umbrella audit has duplicate child issues")
    require(set(child_keys) == EXPECTED_CHILDREN, "umbrella child issue set drift")

    technical = [child for child in children if child["category"] == "technical"]
    administrative = [child for child in children if child["category"] == "administrative"]
    require(len(technical) == 2, "umbrella audit must have exactly two technical children")
    require(len(administrative) == 2, "umbrella audit must have exactly two administrative children")

    for child in technical:
        key = (child["repository"], child["issue"])
        require(child["state"] == "CLOSED", f"technical child remains open: {key}")
        require(child["complete"] is True, f"technical child is not complete: {key}")
        require(child["close_conditions"] == [], f"completed technical child retains close conditions: {key}")
        require(
            child["implementation"] == EXPECTED_TECHNICAL_IMPLEMENTATIONS[key],
            f"technical child implementation identity drift: {key}",
        )

    for child in administrative:
        require(child["state"] == "CLOSED", f"administrative child remains open: {child['issue']}")
        require(child["complete"] is True, f"administrative child is not complete: {child['issue']}")
        require(
            child["implementation"] == EXPECTED_ADMINISTRATIVE_IMPLEMENTATION,
            f"administrative child evidence identity drift: {child['issue']}",
        )
        require(
            child["close_conditions"] == [],
            f"completed administrative child retains close conditions: {child['issue']}",
        )

    technical_complete = all(child["complete"] for child in technical)
    administrative_complete = all(child["complete"] for child in administrative)
    operational_complete = all(child["complete"] for child in children)
    require(
        audit["technical_children_complete"] is technical_complete,
        "technical_children_complete does not match child records",
    )
    require(
        audit["administrative_children_complete"] is administrative_complete,
        "administrative_children_complete does not match child records",
    )
    require(
        audit["operational_release_complete"] is operational_complete,
        "operational_release_complete does not match all four child records",
    )

    blockers = audit["remaining_blockers"]
    blocker_ids = [blocker["blocker_id"] for blocker in blockers]
    require(len(blocker_ids) == len(set(blocker_ids)), "workflow coverage audit has duplicate blockers")
    if operational_complete:
        require(not blockers, "completed operational release retains blockers")
        require(audit["operational_release_closure"] == "COMPLETE", "completed release must have COMPLETE closure")
        require(audit["umbrella_issue_disposition"] == "CLOSE", "completed release must close issue #6")
    else:
        require(blockers, "incomplete operational release lacks blockers")
        require(audit["operational_release_closure"] == "BLOCKED", "incomplete release must remain BLOCKED")
        require(audit["umbrella_issue_disposition"] == "KEEP_OPEN", "issue #6 must remain open while any child is incomplete")

    for required in (
        ".github/workflows/ci.yml",
        ".github/workflows/pages.yml",
        "ci/validate_workflow_semantics.py",
        "ci/validate_policy_reachability.py",
        "ci/validate_repository_execution.py",
        "ci/validate_symbolic_resource_budgets.py",
        "ci/validate_cross_pillar_lane_packages.py",
        "governance/mathcert_cross_repository_conformance.json",
    ):
        require((root / required).is_file(), f"audited workflow control is missing: {required}")


def main() -> int:
    try:
        validate()
    except (WorkflowCoverageAuditError, OSError, json.JSONDecodeError) as exc:
        print(f"workflow coverage audit rejected: {exc}", file=sys.stderr)
        return 1
    print(
        "umbrella audit checked: technical and administrative children complete; operational release closure is complete"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
