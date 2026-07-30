#!/usr/bin/env python3
"""Validate the OZ-RT-LB-INSTANCE-001 Franel theorem package."""
from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
PACKAGE_REL = Path("campaigns/odd_zeta/OZ_RT_LB_INSTANCE_001")
WP00_REL = Path("campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE")
WP02_REL = Path("campaigns/odd_zeta/OZ_WP02_THEOREM_OBLIGATION_LEDGER")
EXPECTED_HYPOTHESES = {"H1", "H2", "H3", "H4", "H4c", "Hw", "H5"}
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
EXPECTED_TARGETS = {
    "ZetaLucas.theorem_LB",
    "ZetaLucas.bFranel_lucas",
    "ZetaLucas.bFranel_eq",
    "ZetaLucas.Arow_SF",
}
EXPECTED_IDENTITIES = {
    "papers_out/lucas2nd/sec-general.tex": (8904, "a934fd9bf2be75d130671d788269110186e4bd5183acb4e903dd7ad9d3ace742", "3784746b46ed5c342898f1ac0f148eb96b388951"),
    "papers_out/lucas2nd/sec-families.tex": (18442, "1360dab906effc9cc50148bd002406cdd350191a0f2088af687f3c60c80d687e", "1c9b71446ef9eac59e238bbec67c8482a9aa7c95"),
    "lean/ZetaLucas/TheoremLB.lean": (12328, "549d8dafb6dbedd8ff09129a7e3e6e8bea165d4fc73886097880988f916be590", "2c79d82232a3e0e2e5aa9d0174e86d28dcf4697d"),
    "lean/ZetaLucas/Instances.lean": (11821, "c5d460150770cd24bc87490709e9a638c91fde411364a0e68bbd8840826bd6b3", "08c243da431f26311c40f8de70f4b7c092f069e7"),
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


def load_identities(path: Path) -> dict[str, tuple[int, str, str]]:
    records: dict[str, tuple[int, str, str]] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["entry_type"] == "blob":
                records[row["path"]] = (int(row["bytes"]), row["sha256"], row["git_object_sha1"])
    return records


def validate(root: Path = ROOT) -> list[str]:
    package = root / PACKAGE_REL
    wp00 = root / WP00_REL
    wp02 = root / WP02_REL
    errors: list[str] = []
    try:
        audit = load_yaml(package / "HYPOTHESIS_AUDIT.yaml")
        boundary = load_yaml(package / "SEMANTIC_BOUNDARY.yaml")
        lean = load_yaml(package / "LEAN_REPLAY.yaml")
        review = load_yaml(package / "REVIEW_REGISTER.yaml")
        theorem_ledger = load_yaml(wp02 / "THEOREM_LEDGER.yaml")
        obligations = load_yaml(wp02 / "PROOF_OBLIGATIONS.yaml")
        bridges = load_yaml(wp00 / "03_IRRATIONALITY_BRIDGE_REGISTER.yaml")

        require(audit.get("audit_id") == "OZ-RT-LB-INSTANCE-001-HYPOTHESES", "audit ID drift")
        require(audit.get("selected_family") == "Franel", "selected family drift")
        require(audit.get("source", {}).get("commit") == "968477ed7e406df6542f8da6fbe1cd6ca7273c47", "source commit drift")
        target = audit.get("exact_target", {})
        require(target.get("modulus") == "p", "target modulus must remain p")
        require(target.get("prime_scope") == "odd primes", "target prime scope drift")
        require(target.get("weight") == 2, "Franel weight must remain two")
        require(target.get("character") == "trivial", "Franel character drift")

        hypotheses = audit.get("hypotheses", [])
        hypothesis_map = {item.get("id"): item for item in hypotheses if isinstance(item, dict)}
        require(set(hypothesis_map) == EXPECTED_HYPOTHESES, "hypothesis inventory drift")
        require(all(item.get("status") == "FORMALLY_DISCHARGED" for item in hypotheses), "all hypotheses must be formally discharged")
        for hyp_id, item in hypothesis_map.items():
            require(item.get("proof"), f"{hyp_id}: proof explanation missing")
            require(item.get("lean_witness"), f"{hyp_id}: Lean witness missing")
            require(item.get("adversarial_boundary"), f"{hyp_id}: adversarial boundary missing")
        require("nonzero S(r,s)" in hypothesis_map["H3"]["adversarial_boundary"], "H3 no-borrow boundary drift")
        require("formal argument<=n" in hypothesis_map["H4"]["adversarial_boundary"], "H4 tameness boundary drift")
        require(audit.get("assembly", {}).get("status") == "FORMALLY_PROVED_PENDING_EXACT_HEAD_REPLAY", "assembly gate drift")

        dispositions = audit.get("wp02_obligation_disposition", {})
        expected_obligations = {f"OZ-OBL-LB-{i:03d}" for i in range(1, 11)}
        require(set(dispositions) == expected_obligations, "WP02 obligation overlay drift")
        for obligation_id in expected_obligations - {"OZ-OBL-LB-009", "OZ-OBL-LB-010"}:
            require(str(dispositions[obligation_id]).startswith("SATISFIED"), f"{obligation_id}: not discharged")
        require(dispositions["OZ-OBL-LB-009"] == "PENDING_EXACT_HEAD_LEAN_REPLAY", "formal instantiation gate drift")
        require(dispositions["OZ-OBL-LB-010"] == "PENDING_EXACT_HEAD_REFEREE_GATE", "Referee gate drift")

        require(boundary.get("boundary_id") == "OZ-RT-LB-INSTANCE-001-SEMANTICS", "semantic boundary ID drift")
        formal = boundary.get("formal_objects", {})
        require(formal.get("base_row", {}).get("definition_relation") == "EXACT_EXPLICIT_SUM", "base-row correspondence drift")
        require(formal.get("companion", {}).get("definition_relation") == "EXACT_EXPLICIT_HARMONIC_SUM", "companion correspondence drift")
        recurrence = boundary.get("recurrence_boundary", {})
        require(recurrence.get("formal_status") == "NOT_FORMALIZED", "recurrence equivalence inflation")
        require("explicit harmonic sum" in recurrence.get("permitted_statement", ""), "permitted statement drift")
        require(boundary.get("novelty_boundary", {}).get("new_after_audit") is False, "novelty inflation")
        require(boundary.get("irrationality_boundary", {}).get("new_conclusion") is False, "irrationality inflation")
        require(boundary.get("successor_boundary", {}).get("authorizes_on_merge") == "OZ-RT-BZ-T3-001", "successor drift")
        require(boundary.get("successor_boundary", {}).get("does_not_authorize") == "OZ-RT-SHARP12-001", "sharp-12 gate drift")

        require(lean.get("replay_id") == "OZ-RT-LB-INSTANCE-001-LEAN", "Lean replay ID drift")
        require(lean.get("status") == "PENDING_EXACT_HEAD_CI", "Lean replay must remain CI-gated pre-merge")
        targets = {item.get("declaration") for item in lean.get("targets", [])}
        require(targets == EXPECTED_TARGETS, "Lean target inventory drift")
        require(all(item.get("expected_sorryAx") is False for item in lean.get("targets", [])), "sorryAx expectation drift")
        require(set(lean.get("required_jobs", [])) == {"package-audit", "lean-franel-instance"}, "required job set drift")

        identities = load_identities(wp00 / "source_lock/A004/OZ-SRC-RIVER-MOREMATH-001.FILE_IDENTITIES.tsv")
        for path, expected in EXPECTED_IDENTITIES.items():
            require(identities.get(path) == expected, f"source identity drift: {path}")
        source = audit["source"]
        for key, path in (("theorem_lb_paper", "papers_out/lucas2nd/sec-general.tex"), ("family_paper", "papers_out/lucas2nd/sec-families.tex"), ("lean_instance", "lean/ZetaLucas/Instances.lean")):
            record = source[key]
            require((record["bytes"], record["sha256"], record["git_blob"]) == EXPECTED_IDENTITIES[path], f"audit source identity mismatch: {path}")
        for record in lean.get("files", []):
            path = record["path"]
            require((record["bytes"], record["sha256"], record["git_blob"]) == EXPECTED_IDENTITIES[path], f"Lean identity mismatch: {path}")

        theorem = next(item for item in theorem_ledger.get("theorems", []) if item.get("id") == "OZ-THM-T005")
        require(theorem.get("target_lane") == "OZ-RT-LB-INSTANCE-001", "WP02 target-lane drift")
        obligation_ids = {item.get("id") for item in obligations.get("obligations", [])}
        require(expected_obligations <= obligation_ids, "WP02 obligation set drift")

        role_names = {item.get("role") for item in review.get("roles", []) if isinstance(item, dict)}
        require(role_names == EXPECTED_ROLES, "eight-role review incomplete")
        referee = next(item for item in review["roles"] if item.get("role") == "Referee")
        require(referee.get("verdict") == "PROMOTE_EXPLICIT_FRANEL_INSTANCE_ON_EXACT_HEAD_CI_SUCCESS", "Referee verdict drift")
        success = review.get("disposition_on_success", {})
        require(success.get("explicit_sum_franel_theorem") == "REFEREE_ACCEPTED", "theorem disposition drift")
        require(success.get("lean_declaration") == "FORMALLY_REPLAYED", "Lean disposition drift")
        require(success.get("recurrence_defined_franel_second_solution") == "NOT_CLAIMED", "recurrence claim inflation")
        require(success.get("novelty") == "NOT_ASSESSED", "novelty disposition drift")
        require(success.get("new_irrationality_conclusion") is False, "irrationality disposition drift")
        require(success.get("authorizes") == "OZ-RT-BZ-T3-001", "authorization drift")
        require(success.get("sharp12_authorized") is False, "sharp-12 premature authorization")

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
        print(f"OZ-RT-LB-INSTANCE-001 validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("OZ-RT-LB-INSTANCE-001 Franel theorem package is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
