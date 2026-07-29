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
EXPECTED_PROGRAMME_BASE = "813f53ea28e1d941cc16c8f3da517c0dcfdc08a5"
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
    "release_trust_workflow_run_id": 30450610588,
    "release_trust_artifact_id": 8723362498,
    "evidence_sha256": "acd7e9c3ea10e9c03ea5dc81a0b84918d7241fea886426d2304e168b10c936f8",
}
EXPECTED_RELEASE_TRUST_EVIDENCE = {
    "contract_id": "ORG-REL-TRUST-01",
    "evidence_id": "ORG-REL-TRUST-01-EVIDENCE",
    "generated_at": "2026-07-29T12:13:58.925324+00:00",
    "workflow_run_id": 30450610588,
    "workflow_run_url": "https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/30450610588",
    "workflow_head_sha": "813f53ea28e1d941cc16c8f3da517c0dcfdc08a5",
    "artifact_id": 8723362498,
    "artifact_url": "https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/actions/artifacts/8723362498",
    "artifact_sha256": "b6f153fda1ce0d80742828aa6ede7a51c0070e908babdc924df1fe6aef65a3da",
    "evidence_file_sha256": "95f06401dfdd0cc5535c0d812e3818fd621db01dae5509b67f68ae9ff8d2e536",
    "evidence_sha256": "acd7e9c3ea10e9c03ea5dc81a0b84918d7241fea886426d2304e168b10c936f8",
    "contract_sha256": "ce540a41792288f811c6cbb91b77580905b0daaebd157b51bd0409f91911b642",
    "policy_workflow_run_id": 30450487344,
    "pages_workflow_run_id": 30450675046,
    "validated_site_artifact_id": 8723277027,
    "validated_site_artifact_sha256": "c0e1719ffb935d9b7c3f3042c6010310ac6a210a101e04609e5c29d34047f19a",
    "site_archive_sha256": "876400862c926f4c91d3932f00e852426e4f76dab841845e18bba4744c3b6465",
    "index_sha256": "9a54a3831d6fb0922b1e21a792c246051d1d8f078621fac5da5e87cdd59535c7",
    "live_index_sha256": "9a54a3831d6fb0922b1e21a792c246051d1d8f078621fac5da5e87cdd59535c7",
    "repository_rulesets": [
        {
            "repository": "grandchallenge/MATHCERT",
            "snapshot_sha256": "22901830aef56c55d262ae16969cbddfd38d09d366ad9b973eb48b9f2e07e5c8",
        },
        {
            "repository": "grandchallenge/MATHSOLVE",
            "snapshot_sha256": "9a7d468030c08420cf45bf4002caaef983972a291376f1da8a430cad99f71b2d",
        },
        {
            "repository": "grandchallenge/MATH-PROGRAMME",
            "snapshot_sha256": "1dd5d9c30865e1fb6adeeb73c2300fb7a829a8802d54d176b572fd5a1c059190",
        },
        {
            "repository": "grandchallenge/INTELLECT",
            "snapshot_sha256": "9d1ff325ee6439f8db30275de91d65985502e030ca432ebc24e88a8d34a66119",
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
