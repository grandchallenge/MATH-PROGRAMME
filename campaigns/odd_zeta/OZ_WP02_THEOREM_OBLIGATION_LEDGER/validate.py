#!/usr/bin/env python3
"""Validate the OZ-WP02 theorem and proof-obligation ledger."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parent
EXPECTED_THEOREMS = {f"OZ-THM-T{i:03d}" for i in range(1, 12)}
EXPECTED_ORDER = ["OZ-THM-T002", "OZ-THM-T005", "OZ-THM-T008", "OZ-THM-T009"]
EXPECTED_ROLES = {
    "Axiomatist",
    "Cartographer",
    "Grammarian",
    "Verifier",
    "Adversary",
    "Formalist",
    "Amanuensis",
    "Referee",
}
KEY_OPEN_OBLIGATIONS = {
    "OZ-OBL-AB-003",
    "OZ-OBL-AB-004",
    "OZ-OBL-AB-006",
    "OZ-OBL-AB-007",
    "OZ-OBL-AB-009",
    "OZ-OBL-AB-010",
    "OZ-OBL-AB-012",
    "OZ-OBL-LB-002",
    "OZ-OBL-T3-004",
    "OZ-OBL-SH-003",
    "OZ-OBL-SH-004",
    "OZ-OBL-Z7-002",
}


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_yaml(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.name}: root must be a mapping")
    return data


def dependency_cycle(graph: dict[str, list[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dep in graph[node]:
            if visit(dep):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def validate(root: Path = ROOT) -> list[str]:
    package = root / "campaigns/odd_zeta/OZ_WP02_THEOREM_OBLIGATION_LEDGER"
    errors: list[str] = []
    try:
        ledger = load_yaml(package / "THEOREM_LEDGER.yaml")
        norms = load_yaml(package / "NORMALIZATION_REGISTER.yaml")
        obligations_data = load_yaml(package / "PROOF_OBLIGATIONS.yaml")
        review = load_yaml(package / "REVIEW_REGISTER.yaml")
        atlas = load_yaml(root / "campaigns/odd_zeta/OZ_WP01_FALSE_PROOF_ATLAS/ATLAS.yaml")
        bridges = load_yaml(
            root
            / "campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE"
            / "03_IRRATIONALITY_BRIDGE_REGISTER.yaml"
        )

        require(ledger.get("ledger_id") == "OZ-WP02-THEOREM-LEDGER", "wrong theorem ledger ID")
        require(ledger.get("research_order") == EXPECTED_ORDER, "research order drift")
        require(ledger.get("next_executable_lane") == "OZ-RT-APERY-BROW-001", "next lane must be Apéry B-row")
        authority = ledger.get("source_authority", {})
        require(
            authority.get("oz_next_006_merge") == "a2eb1c685e85961515e7c748bf732b4469f63204",
            "OZ-NEXT-006 authority drift",
        )
        require(
            authority.get("oz_wp01_merge") == "9620485c00488c8307cb0b7224640871f533c57c",
            "OZ-WP01 authority drift",
        )

        theorems = ledger.get("theorems", [])
        require(isinstance(theorems, list) and len(theorems) == 11, "exactly eleven theorem records required")
        theorem_map = {item.get("id"): item for item in theorems if isinstance(item, dict)}
        require(set(theorem_map) == EXPECTED_THEOREMS, "theorem ID set drift")
        for theorem_id, theorem in theorem_map.items():
            for field in (
                "title",
                "exact_statement",
                "quantifier_scope",
                "modulus",
                "prime_scope",
                "normalization_ids",
                "source_records",
                "evidence_effects",
                "disposition",
                "novelty_status",
                "promotion_boundary",
            ):
                require(field in theorem, f"{theorem_id}: missing {field}")
            require(theorem["source_records"], f"{theorem_id}: source records required")
            require(theorem["promotion_boundary"], f"{theorem_id}: promotion boundary required")
            require(theorem["disposition"] in ledger["allowed_dispositions"], f"{theorem_id}: invalid disposition")
            require(theorem["novelty_status"] != "NEW_AFTER_AUDIT", f"{theorem_id}: novelty inflation")

        t1 = theorem_map["OZ-THM-T001"]
        require("zeta(33)" in t1["exact_statement"] and "At least one" in t1["exact_statement"], "finite disjunction drift")
        t2 = theorem_map["OZ-THM-T002"]
        require(t2["modulus"] == "p" and t2["prime_scope"] == "p>=5", "Apéry B-row scope drift")
        require({"OZ-NRM-N002", "OZ-NRM-N003", "OZ-NRM-N005"} <= set(t2["normalization_ids"]), "Apéry normalization lock incomplete")
        t3 = theorem_map["OZ-THM-T003"]
        require(t3["disposition"] == "FINITE_EVIDENCE_ONLY", "multi-digit theorem must remain finite evidence")
        require(t3.get("bounded_domain") == "5 <= p <= 31 and n <= 320", "multi-digit bounded domain drift")
        t4 = theorem_map["OZ-THM-T004"]
        require(t4["disposition"] == "FORMALLY_REPLAYED_ABSTRACT_CONDITIONAL", "Theorem LB scope drift")
        t8 = theorem_map["OZ-THM-T008"]
        require(t8["disposition"] == "OPEN_WITH_FINITE_EVIDENCE", "T3 must remain open")
        t9 = theorem_map["OZ-THM-T009"]
        require(t9["disposition"] == "CONDITIONAL_CHAIN_NOT_ACCEPTED", "sharp-12 status drift")
        promotion = ledger.get("promotion", {})
        require(promotion.get("theorem_promotions") == [], "theorem promotion prohibited")
        require(promotion.get("novelty_promotions") == [], "novelty promotion prohibited")
        require(promotion.get("new_irrationality_conclusions") == [], "irrationality promotion prohibited")
        require(promotion.get("sharp12_accepted") is False, "sharp-12 may not be accepted")

        normalizations = norms.get("normalizations", [])
        norm_map = {item.get("id"): item for item in normalizations if isinstance(item, dict)}
        require(set(norm_map) == {f"OZ-NRM-N{i:03d}" for i in range(1, 8)}, "normalization ID set drift")
        require(norms.get("required_equivalence") == "bMin_n = 6 B_n", "factor-six equivalence missing")
        require(norm_map["OZ-NRM-N002"].get("equivalence") == "bMin_n = 6 B_n", "B/bMin equivalence drift")
        for theorem in theorems:
            unknown = set(theorem["normalization_ids"]) - set(norm_map)
            require(not unknown, f"{theorem['id']}: unknown normalizations {sorted(unknown)}")

        obligations = obligations_data.get("obligations", [])
        require(isinstance(obligations, list) and len(obligations) == 40, "exactly forty proof obligations required")
        obligation_map = {item.get("id"): item for item in obligations if isinstance(item, dict)}
        require(len(obligation_map) == 40, "duplicate proof-obligation IDs")
        allowed_status = set(obligations_data.get("status_vocabulary", []))
        atlas_ids = {item.get("id") for item in atlas.get("cases", [])}
        graph: dict[str, list[str]] = {}
        for obligation_id, obligation in obligation_map.items():
            require(obligation.get("theorem_id") in theorem_map, f"{obligation_id}: unknown theorem")
            require(obligation.get("status") in allowed_status, f"{obligation_id}: invalid status")
            deps = obligation.get("dependencies")
            require(isinstance(deps, list), f"{obligation_id}: dependencies must be a list")
            require(not (set(deps) - set(obligation_map)), f"{obligation_id}: unknown dependency")
            controls = obligation.get("false_proof_controls")
            require(isinstance(controls, list), f"{obligation_id}: false-proof controls must be a list")
            require(not (set(controls) - atlas_ids), f"{obligation_id}: unknown false-proof control")
            graph[obligation_id] = deps
        require(not dependency_cycle(graph), "proof-obligation dependency cycle")

        for obligation_id in KEY_OPEN_OBLIGATIONS:
            require(obligation_map[obligation_id]["status"] in {"OPEN", "BLOCKED"}, f"{obligation_id}: premature discharge")
        require(obligation_map["OZ-OBL-T3-002"]["status"] == "FINITE_EVIDENCE_ONLY", "T3 finite evidence drift")
        require(obligation_map["OZ-OBL-SH-003"]["status"] == "OPEN", "T1-top must remain open")
        require(obligation_map["OZ-OBL-SH-004"]["status"] == "OPEN", "DEPTH must remain open")

        gates = obligations_data.get("promotion_gates", {})
        expected_gates = {
            "OZ-RT-APERY-BROW-001",
            "OZ-RT-LB-INSTANCE-001",
            "OZ-RT-BZ-T3-001",
            "OZ-RT-SHARP12-001",
        }
        require(set(gates) == expected_gates, "promotion-gate set drift")
        for lane, gate in gates.items():
            required = gate.get("required_obligations", [])
            require(required, f"{lane}: required obligations missing")
            require(not (set(required) - set(obligation_map)), f"{lane}: unknown required obligation")
        require(obligations_data.get("next_executable_lane") == "OZ-RT-APERY-BROW-001", "obligation ledger next lane drift")

        roles = review.get("roles", [])
        role_names = {item.get("role") for item in roles if isinstance(item, dict)}
        require(role_names == EXPECTED_ROLES, "eight-role review incomplete")
        referee = next(item for item in roles if item.get("role") == "Referee")
        require(referee.get("verdict") == "PROMOTE_ON_EXACT_HEAD_CI_SUCCESS", "Referee verdict drift")
        review_promotion = review.get("promotion", {})
        require(review_promotion.get("authorizes") == "OZ-RT-APERY-BROW-001", "review authorization drift")
        require(review_promotion.get("theorem_promotions") == [], "review may not promote theorems")

        bridge_records = bridges.get("bridges", [])
        require(len(bridge_records) == 8, "eight irrationality bridges required")
        require(all(item.get("status") == "OPEN" for item in bridge_records), "irrationality bridges must remain open")

    except (ValidationError, KeyError, TypeError, StopIteration, yaml.YAMLError) as exc:
        errors.append(str(exc))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"OZ-WP02 validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("OZ-WP02 theorem and proof-obligation ledger is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
