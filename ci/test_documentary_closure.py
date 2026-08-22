#!/usr/bin/env python3
"""Regression tests for terminal documentary-closure rejection paths."""

from __future__ import annotations

import copy
from pathlib import Path

import yaml

from validate_documentary_closure import (
    FIXED_LEGACY_EVIDENCE_PACKAGES,
    ROOT,
    agent_review_terminal_errors,
    closure_contract_errors,
    closure_registry_errors,
    discovered_closure_contracts,
    discovered_evidence_packages,
    evidence_package_coverage_errors,
    instruction_binding_errors,
    load_json,
)


def main() -> int:
    published = yaml.safe_load(
        (ROOT / "reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert published["artifact"]["status"] == "published"
    assert published["promotion"]["ready_for_next_stage"] is False
    assert not agent_review_terminal_errors(published, "DOCS-DOCUMENTARY-001")

    incomplete_terminal = copy.deepcopy(published)
    incomplete_terminal["amanuensis_control"]["review_provenance"]["complete"] = False
    assert any(
        "review provenance must be complete" in error
        for error in agent_review_terminal_errors(
            incomplete_terminal, "DOCS-DOCUMENTARY-001"
        )
    )

    missing_terminal_evidence = copy.deepcopy(published)
    missing_terminal_evidence["amanuensis_control"]["review_provenance"][
        "evidence_refs"
    ] = []
    assert any(
        "at least one evidence reference" in error
        for error in agent_review_terminal_errors(
            missing_terminal_evidence, "DOCS-DOCUMENTARY-001"
        )
    )

    unresolved_terminal_conflict = copy.deepcopy(published)
    unresolved_terminal_conflict["amanuensis_control"]["cross_document_consistency"][
        "conflicts"
    ] = ["synthetic conflict"]
    assert any(
        "must not be hidden" in error
        for error in agent_review_terminal_errors(
            unresolved_terminal_conflict, "DOCS-DOCUMENTARY-001"
        )
    )

    missing_integrated_artifact = copy.deepcopy(published)
    missing_integrated_artifact["amanuensis_control"]["final_editorial_integration"][
        "integrated_artifact_ref"
    ] = "docs/DOES-NOT-EXIST.md"
    assert any(
        "authoritative integrated artifact does not resolve" in error
        for error in agent_review_terminal_errors(
            missing_integrated_artifact, "DOCS-DOCUMENTARY-001"
        )
    )

    active_incomplete = copy.deepcopy(incomplete_terminal)
    active_incomplete["artifact"]["status"] = "active"
    active_incomplete["promotion"]["ready_for_next_stage"] = False
    assert not agent_review_terminal_errors(active_incomplete, "ACTIVE-NONTERMINAL")

    assert not instruction_binding_errors()
    assert not closure_registry_errors()

    codeowners = (ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8")
    assert "@grandchallenge/the-council" not in codeowners
    for required_owner_line in (
        "/AGENTS.md @grandchallenge/math-programme-maintainers @grandchallenge/amanuensis",
        "/docs/AGENT_COUNCIL_* @grandchallenge/math-programme-maintainers @grandchallenge/amanuensis",
        "/ci/validate_documentary_closure.py @grandchallenge/math-programme-maintainers @grandchallenge/amanuensis",
        "/ci/test_documentary_closure.py @grandchallenge/math-programme-maintainers @grandchallenge/amanuensis",
        "/governance/ @grandchallenge/math-programme-maintainers @grandchallenge/amanuensis",
        "/schemas/ @grandchallenge/math-programme-maintainers @grandchallenge/amanuensis",
        "/decisions/ @grandchallenge/math-programme-maintainers @grandchallenge/amanuensis",
        "/.github/ @grandchallenge/security @grandchallenge/math-programme-maintainers @grandchallenge/amanuensis",
    ):
        assert required_owner_line in codeowners

    registry = load_json(ROOT / "governance/governed_closure_registry.json")
    registered_contracts = set(registry["contracts"])
    registered_legacy = set(registry["legacy_evidence_packages"])
    discovered_contracts = discovered_closure_contracts()
    discovered_packages = discovered_evidence_packages()

    assert registered_contracts == discovered_contracts
    assert registered_legacy == set(FIXED_LEGACY_EVIDENCE_PACKAGES)
    assert not evidence_package_coverage_errors(
        discovered_packages,
        registered_contracts,
        registered_legacy,
    )

    contract_packages = {
        Path(relative).parent.as_posix() for relative in registered_contracts
    }
    assert discovered_packages == contract_packages | registered_legacy

    synthetic_uncontracted = set(discovered_packages)
    synthetic_uncontracted.add("governance/rebuild_evidence/MP-FUTURE-UNCONTRACTED-001")
    assert any(
        "MP-FUTURE-UNCONTRACTED-001" in error
        and "lacks a registered closure_contract.json" in error
        for error in evidence_package_coverage_errors(
            synthetic_uncontracted,
            registered_contracts,
            registered_legacy,
        )
    )

    synthetic_legacy_expansion = set(registered_legacy)
    synthetic_legacy_expansion.add("governance/rebuild_evidence/MP-FUTURE-LEGACY-001")
    assert any(
        "unauthorized legacy evidence package exemption" in error
        for error in evidence_package_coverage_errors(
            discovered_packages | synthetic_legacy_expansion,
            registered_contracts,
            synthetic_legacy_expansion,
        )
    )

    assert any(
        "fixed legacy evidence baseline entry is missing" in error
        for error in evidence_package_coverage_errors(
            discovered_packages,
            registered_contracts,
            set(),
        )
    )

    legacy_overlap = set(registered_legacy)
    contract_package = sorted(contract_packages)[0]
    legacy_overlap.add(contract_package)
    assert any(
        "cannot be both legacy and contract-bound" in error
        for error in evidence_package_coverage_errors(
            discovered_packages,
            registered_contracts,
            legacy_overlap,
        )
    )

    low_friction_path = ROOT / registry["contracts"][0]
    low_friction = load_json(low_friction_path)
    assert not closure_contract_errors(
        low_friction, registry["contracts"][0]
    )

    bad_ledger = copy.deepcopy(low_friction)
    bad_ledger["artifact_ledger"]["entry_id"] = "MISSING-LEDGER-ENTRY"
    assert any(
        "lacks entry MISSING-LEDGER-ENTRY" in error
        for error in closure_contract_errors(bad_ledger, "synthetic")
    )

    bad_consistency_ref = copy.deepcopy(low_friction)
    bad_consistency_ref["cross_document_consistency"]["checked_against"].append(
        "governance/DOES-NOT-EXIST.json"
    )
    assert any(
        "consistency reference does not resolve" in error
        for error in closure_contract_errors(bad_consistency_ref, "synthetic")
    )

    print("documentary closure rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
