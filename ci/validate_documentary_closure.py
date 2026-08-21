#!/usr/bin/env python3
"""Validate terminal documentary integrity for governed MATH-PROGRAMME work."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from validate_programme import CORE_CAMPAIGN_AGENTS, ROOT, SCHEMA_BOUND_AGENT_REVIEWS

TERMINAL_AGENT_REVIEW_STATUSES = {"completed", "certified", "published", "archived"}
REGISTRY_REL = "governance/governed_closure_registry.json"
REGISTRY_SCHEMA_REL = "schemas/governed_closure_registry.schema.json"
CONTRACT_SCHEMA_REL = "schemas/governed_closure_contract.schema.json"
REQUIRED_POLICY_BINDINGS = (
    "AGENTS.md",
    "docs/AGENT_COUNCIL_GOVERNANCE.md",
    "docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def safe_repo_path(root: Path, relative: str) -> Path | None:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        return None
    resolved = root / path
    return resolved


def nested_contains_artifact_id(value: Any, artifact_id: str) -> bool:
    if isinstance(value, dict):
        if value.get("artifact_id") == artifact_id:
            return True
        return any(nested_contains_artifact_id(item, artifact_id) for item in value.values())
    if isinstance(value, list):
        return any(nested_contains_artifact_id(item, artifact_id) for item in value)
    return False


def ledger_contains_entry(path: Path, entry_id: str) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        try:
            return nested_contains_artifact_id(json.loads(text), entry_id)
        except json.JSONDecodeError:
            return False
    return entry_id in text


def duplicate_values(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def agent_review_terminal_errors(
    review: dict[str, Any], label: str, root: Path = ROOT
) -> list[str]:
    """Enforce documentary continuity for promotion or terminal lifecycle state."""
    errors: list[str] = []
    artifact = review.get("artifact", {})
    promotion = review.get("promotion", {})
    status = artifact.get("status")
    gate_active = bool(promotion.get("ready_for_next_stage")) or status in TERMINAL_AGENT_REVIEW_STATUSES
    if not gate_active:
        return errors

    reason = (
        f"terminal lifecycle status {status!r}"
        if status in TERMINAL_AGENT_REVIEW_STATUSES
        else "promotion.ready_for_next_stage=true"
    )
    prefix = f"{label}: {reason} requires documentary closure"
    amanuensis = review.get("amanuensis_control", {})

    ledger = amanuensis.get("artifact_ledger", {})
    ledger_ref = ledger.get("ledger_ref")
    entry_id = ledger.get("entry_id")
    if not ledger_ref or not entry_id:
        errors.append(f"{prefix}: artifact-ledger reference and entry ID are required")
    else:
        ledger_path = safe_repo_path(root, str(ledger_ref))
        if ledger_path is None or not ledger_path.is_file():
            errors.append(f"{prefix}: artifact ledger does not resolve: {ledger_ref}")
        elif not ledger_contains_entry(ledger_path, str(entry_id)):
            errors.append(f"{prefix}: artifact ledger {ledger_ref} lacks entry {entry_id}")

    provenance = amanuensis.get("review_provenance", {})
    if provenance.get("complete") is not True:
        errors.append(f"{prefix}: review provenance must be complete")
    if not provenance.get("evidence_refs"):
        errors.append(f"{prefix}: review provenance requires at least one evidence reference")

    consistency = amanuensis.get("cross_document_consistency", {})
    if consistency.get("status") != "reviewed":
        errors.append(f"{prefix}: cross-document consistency must be reviewed")
    if not consistency.get("checked_against"):
        errors.append(f"{prefix}: cross-document consistency requires checked-against references")
    if consistency.get("conflicts"):
        errors.append(f"{prefix}: unresolved cross-document conflicts must not be hidden")

    integration = amanuensis.get("final_editorial_integration", {})
    if integration.get("status") != "reviewed":
        errors.append(f"{prefix}: final editorial integration must be reviewed")
    integrated_ref = integration.get("integrated_artifact_ref")
    if not integrated_ref:
        errors.append(f"{prefix}: authoritative integrated artifact is required")
    else:
        integrated_path = safe_repo_path(root, str(integrated_ref))
        if integrated_path is None or not integrated_path.exists():
            errors.append(f"{prefix}: authoritative integrated artifact does not resolve: {integrated_ref}")

    council = review.get("council_review", {})
    for agent in CORE_CAMPAIGN_AGENTS:
        agent_status = council.get(agent, {}).get("status")
        if agent_status != "reviewed":
            errors.append(f"{prefix}: {agent} must be reviewed, found {agent_status!r}")
    for agent, record in council.items():
        if record.get("status") == "blocked":
            errors.append(f"{prefix}: {agent} remains blocked")

    for obligation in review.get("unresolved_obligations", []):
        if obligation.get("blocking"):
            errors.append(
                f"{prefix}: unresolved blocking obligation {obligation.get('id', '<unknown>')}"
            )

    if promotion.get("blockers"):
        errors.append(f"{prefix}: promotion/documentary blockers must be empty")
    return errors


def discovered_closure_contracts(root: Path = ROOT) -> set[str]:
    evidence_root = root / "governance" / "rebuild_evidence"
    if not evidence_root.is_dir():
        return set()
    return {
        path.relative_to(root).as_posix()
        for path in evidence_root.rglob("closure_contract.json")
    }


def closure_contract_errors(
    contract: dict[str, Any], label: str, root: Path = ROOT
) -> list[str]:
    errors = [
        f"{label}: {error}"
        for error in schema_errors(contract, root / CONTRACT_SCHEMA_REL)
    ]
    if errors:
        return errors

    ledger = contract["artifact_ledger"]
    ledger_ref = ledger["ledger_ref"]
    ledger_path = safe_repo_path(root, ledger_ref)
    if ledger_path is None or not ledger_path.is_file():
        errors.append(f"{label}: artifact ledger does not resolve: {ledger_ref}")
    elif not ledger_contains_entry(ledger_path, ledger["entry_id"]):
        errors.append(
            f"{label}: artifact ledger {ledger_ref} lacks entry {ledger['entry_id']}"
        )

    artifact_ref = contract["final_editorial_integration"]["authoritative_artifact_ref"]
    artifact_path = safe_repo_path(root, artifact_ref)
    if artifact_path is None or not artifact_path.exists():
        errors.append(f"{label}: authoritative artifact does not resolve: {artifact_ref}")

    for policy_ref in contract["binding"]["policy_refs"]:
        policy_path = safe_repo_path(root, policy_ref)
        if policy_path is None or not policy_path.is_file():
            errors.append(f"{label}: policy reference does not resolve: {policy_ref}")

    for checked_ref in contract["cross_document_consistency"]["checked_against"]:
        checked_path = safe_repo_path(root, checked_ref)
        if checked_path is None or not checked_path.exists():
            errors.append(f"{label}: consistency reference does not resolve: {checked_ref}")
    return errors


def closure_registry_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    registry_path = root / REGISTRY_REL
    if not registry_path.is_file():
        return [f"documentary closure registry is missing: {REGISTRY_REL}"]
    registry = load_json(registry_path)
    errors.extend(
        f"{REGISTRY_REL}: {error}"
        for error in schema_errors(registry, root / REGISTRY_SCHEMA_REL)
    )
    if errors:
        return errors

    registered = set(registry["contracts"])
    discovered = discovered_closure_contracts(root)
    for relative in sorted(discovered - registered):
        errors.append(f"documentary closure: discovered contract is unregistered: {relative}")
    for relative in sorted(registered - discovered):
        errors.append(f"documentary closure: registered contract is missing: {relative}")

    contract_ids: list[str] = []
    work_ids: list[str] = []
    for relative in registry["contracts"]:
        contract_path = safe_repo_path(root, relative)
        if contract_path is None or not contract_path.is_file():
            continue
        contract = load_json(contract_path)
        contract_ids.append(str(contract.get("contract_id", "")))
        work_ids.append(str(contract.get("governed_work_id", "")))
        errors.extend(closure_contract_errors(contract, relative, root))

    for duplicate in sorted(duplicate_values(contract_ids)):
        errors.append(f"documentary closure: duplicate contract_id {duplicate}")
    for duplicate in sorted(duplicate_values(work_ids)):
        errors.append(f"documentary closure: duplicate governed_work_id {duplicate}")
    return errors


def instruction_binding_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    required_fragments = {
        "AGENTS.md": (
            "Terminal documentary integrity",
            "governance/governed_closure_registry.json",
            "docs/AGENT_COUNCIL_GOVERNANCE.md",
        ),
        "docs/AGENT_COUNCIL_GOVERNANCE.md": (
            "Terminal documentary closure boundary",
            "ci/validate_documentary_closure.py",
            "governance/governed_closure_registry.json",
        ),
        "docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md": (
            "Terminal closure gate",
            "closure_contract.json",
        ),
    }
    for relative, fragments in required_fragments.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"documentary closure instruction binding is missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{relative}: documentary closure binding missing {fragment!r}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(instruction_binding_errors())
    errors.extend(closure_registry_errors())

    for relative in SCHEMA_BOUND_AGENT_REVIEWS:
        path = ROOT / relative
        if not path.is_file():
            continue
        review = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(review, dict):
            errors.extend(agent_review_terminal_errors(review, relative))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"documentary closure validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1

    print(
        "documentary closure integrity is valid: terminal Agent Council records and "
        "registered governed-operation contracts are continuous"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
