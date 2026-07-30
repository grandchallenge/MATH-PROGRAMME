#!/usr/bin/env python3
"""Validate the OZ-RT-APERY-BROW-001 proof, correspondence and formal replay package."""
from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
PACKAGE_REL = Path("campaigns/odd_zeta/OZ_RT_APERY_BROW_001")
WP00_REL = Path("campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE")
WP02_REL = Path("campaigns/odd_zeta/OZ_WP02_THEOREM_OBLIGATION_LEDGER")
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
MANDATORY_OBLIGATIONS = {f"OZ-OBL-AB-{i:03d}" for i in range(1, 13)}
EXPECTED_LEAN_TARGETS = {
    "ZetaLucas.apery_lucas",
    "ZetaLucas.bMin_lucas",
    "ZetaLucas.bMin_eq_bApery",
    "ZetaLucas.apery_b_harmonic_closed_form",
    "ZetaLucas.bApery_lucas",
}
EXPECTED_SOURCE_IDENTITIES = {
    "papers_out/lucas2nd/sec-weight3.tex": (20655, "6641f3af3804fa8b4230284ec6e6843e0071de0f10b3613b5c18ae9aa3514e3e", "5a5c7a555a919125877d4c2e22f9cfd1e8a58335"),
    "papers_out/lucas2nd/sec-minimal.tex": (27493, "201c7a31cf72ec2d5b241e709ccc0ad634954683939e0f157775b6eb466a16ae", "d3c38d524b124eb13a415e5006c548c3002a1d31"),
    "lean/ZetaLucas/Apery.lean": (6045, "d7cb7bde2d897c4995818f16260fcac50c687b3be76446f964dd71fefc44c295", "bc0c92165d125ca1881145e0cd4a66c5df1a29fd"),
    "lean/ZetaLucas/TheoremLB.lean": (12328, "549d8dafb6dbedd8ff09129a7e3e6e8bea165d4fc73886097880988f916be590", "2c79d82232a3e0e2e5aa9d0174e86d28dcf4697d"),
    "lean/ZetaLucas/Instances.lean": (11821, "c5d460150770cd24bc87490709e9a638c91fde411364a0e68bbd8840826bd6b3", "08c243da431f26311c40f8de70f4b7c092f069e7"),
    "lean/ZetaLucas/MinimalForm.lean": (21358, "57b4d42e614060f4c217ede9ac462025daba298863f248ed508a28a9f47b002c", "7ade6d8fae3095b1bccc207438f3899d43e17926"),
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


def load_identity_table(path: Path) -> dict[str, tuple[int, str, str]]:
    rows: dict[str, tuple[int, str, str]] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["entry_type"] == "blob":
                rows[row["path"]] = (int(row["bytes"]), row["sha256"], row["git_object_sha1"])
    return rows


def validate(root: Path = ROOT) -> list[str]:
    package = root / PACKAGE_REL
    wp00 = root / WP00_REL
    wp02 = root / WP02_REL
    errors: list[str] = []
    try:
        proof = load_yaml(package / "DIRECT_PROOF_AUDIT.yaml")
        semantics = load_yaml(package / "SEMANTIC_CORRESPONDENCE.yaml")
        lean = load_yaml(package / "LEAN_REPLAY.yaml")
        review = load_yaml(package / "REVIEW_REGISTER.yaml")
        theorem_ledger = load_yaml(wp02 / "THEOREM_LEDGER.yaml")
        obligations = load_yaml(wp02 / "PROOF_OBLIGATIONS.yaml")
        bridges = load_yaml(wp00 / "03_IRRATIONALITY_BRIDGE_REGISTER.yaml")

        require(proof.get("audit_id") == "OZ-RT-APERY-BROW-001-DIRECT-PROOF", "proof audit ID drift")
        require(proof.get("theorem_id") == "OZ-THM-T002", "wrong theorem target")
        require(proof.get("source_lock", {}).get("commit") == "968477ed7e406df6542f8da6fbe1cd6ca7273c47", "source commit drift")
        target = proof.get("exact_target", {})
        require(target.get("modulus") == "p", "target modulus must remain p")
        require(target.get("prime_scope") == "p>=5", "target prime scope drift")
        require(target.get("digit_scope") == "1<=a<p and 0<=r<p", "target digit scope drift")
        require(len(proof.get("proof_routes", [])) == 2, "two independent evidence routes required")
        direct = next(item for item in proof["proof_routes"] if item.get("id") == "OZ-AB-ROUTE-DIRECT")
        require(direct.get("status") == "ACCEPTED_BY_INDEPENDENT_GCL_AUDIT", "direct proof not accepted")
        steps = direct.get("outline", [])
        require([item.get("id") for item in steps] == [f"D{i:02d}" for i in range(1, 11)], "direct proof-step inventory drift")
        require(all(item.get("finding") == "PASS" for item in steps), "all direct proof steps must pass")

        disposition = proof.get("obligation_disposition", {})
        require(MANDATORY_OBLIGATIONS <= set(disposition), "mandatory obligation disposition incomplete")
        for obligation_id in MANDATORY_OBLIGATIONS - {"OZ-OBL-AB-011", "OZ-OBL-AB-012"}:
            require(str(disposition[obligation_id]).startswith("SATISFIED"), f"{obligation_id}: proof audit did not discharge obligation")
        require(disposition.get("OZ-OBL-AB-011") == "PENDING_EXACT_HEAD_LEAN_REPLAY", "Lean replay gate drift")
        require(disposition.get("OZ-OBL-AB-012") == "PENDING_EXACT_HEAD_LEAN_REPLAY", "semantic replay gate drift")
        require(disposition.get("OZ-OBL-AB-013") == "OPEN_NOVELTY_REVIEW", "novelty obligation must remain open")

        require(semantics.get("correspondence_id") == "OZ-RT-APERY-BROW-001-SEMANTICS", "semantic correspondence ID drift")
        objects = semantics.get("objects", {})
        require(objects.get("paper_double_sum_companion", {}).get("relation") == "NOT_DIRECTLY_FORMALIZED", "double-sum formalization inflation")
        edges = {item.get("id"): item for item in semantics.get("correspondence_edges", [])}
        require(set(edges) == {f"OZ-COR-AB-{i:03d}" for i in range(1, 6)}, "semantic edge set drift")
        require(edges["OZ-COR-AB-004"].get("status") == "PAPER_PROOF_ACCEPTED_NOT_LEAN_FORMALIZED", "paper bridge boundary drift")
        boundary = semantics.get("formalization_boundary", {})
        require(boundary.get("exact_target_for_recurrence_sequence_formalized") is True, "recurrence target must be formalized")
        require(boundary.get("direct_double_sum_definition_present_in_lean") is False, "double-sum definition is not in Lean")
        require(boundary.get("double_sum_equivalence_formalized") is False, "double-sum equivalence is not kernel-checked")
        require(semantics.get("verdict") == "ACCEPT_PENDING_EXACT_HEAD_LEAN_REPLAY", "semantic verdict drift")

        require(lean.get("replay_id") == "OZ-RT-APERY-BROW-001-LEAN", "Lean replay ID drift")
        require(lean.get("status") == "PENDING_EXACT_HEAD_CI", "pre-merge Lean status must remain CI-gated")
        targets = {item.get("declaration") for item in lean.get("targets", [])}
        require(targets == EXPECTED_LEAN_TARGETS, "Lean target inventory drift")
        require(all(item.get("expected_sorryAx") is False for item in lean.get("targets", [])), "sorryAx expectation drift")
        require(set(lean.get("required_jobs", [])) == {"proof-package", "lean-apery-brow"}, "required job set drift")

        identities = load_identity_table(
            wp00 / "source_lock/A004/OZ-SRC-RIVER-MOREMATH-001.FILE_IDENTITIES.tsv"
        )
        for path, expected in EXPECTED_SOURCE_IDENTITIES.items():
            require(identities.get(path) == expected, f"source identity drift: {path}")
        proof_source = proof["source_lock"]
        require((proof_source["direct_proof"]["bytes"], proof_source["direct_proof"]["sha256"], proof_source["direct_proof"]["git_blob"]) == EXPECTED_SOURCE_IDENTITIES["papers_out/lucas2nd/sec-weight3.tex"], "direct proof identity mismatch")
        require((proof_source["representation_bridge"]["bytes"], proof_source["representation_bridge"]["sha256"], proof_source["representation_bridge"]["git_blob"]) == EXPECTED_SOURCE_IDENTITIES["papers_out/lucas2nd/sec-minimal.tex"], "representation bridge identity mismatch")
        for source_file in lean.get("source_files", []):
            path = source_file["path"]
            require((source_file["bytes"], source_file["sha256"], source_file["git_blob"]) == EXPECTED_SOURCE_IDENTITIES[path], f"Lean source identity mismatch: {path}")

        theorem = next(item for item in theorem_ledger.get("theorems", []) if item.get("id") == "OZ-THM-T002")
        require(theorem.get("modulus") == "p", "WP02 theorem modulus drift")
        require(theorem.get("prime_scope") == "p>=5", "WP02 theorem prime scope drift")
        require(theorem.get("target_lane") == "OZ-RT-APERY-BROW-001", "WP02 target-lane drift")
        obligation_map = {item.get("id"): item for item in obligations.get("obligations", [])}
        require(MANDATORY_OBLIGATIONS <= set(obligation_map), "WP02 mandatory obligation set drift")

        roles = review.get("roles", [])
        role_names = {item.get("role") for item in roles if isinstance(item, dict)}
        require(role_names == EXPECTED_ROLES, "eight-role review incomplete")
        referee = next(item for item in roles if item.get("role") == "Referee")
        require(referee.get("verdict") == "PROMOTE_TARGET_THEOREM_ON_EXACT_HEAD_CI_SUCCESS", "Referee gate drift")
        success = review.get("disposition_on_success", {})
        require(success.get("mathematical_theorem") == "REFEREE_ACCEPTED", "theorem disposition drift")
        require(success.get("recurrence_sequence_lean_theorem") == "FORMALLY_REPLAYED", "formal disposition drift")
        require(success.get("paper_double_sum_to_minimal_bridge") == "PAPER_PROOF_ACCEPTED_NOT_LEAN_FORMALIZED", "formal boundary inflation")
        require(success.get("novelty") == "APPARENTLY_NEW_PENDING_REVIEW", "novelty status drift")
        require(success.get("multi_digit_mod_p3") == "FINITE_EVIDENCE_ONLY", "multi-digit status drift")
        require(success.get("new_irrationality_conclusion") is False, "irrationality inflation")
        require(success.get("authorizes") == "OZ-RT-LB-INSTANCE-001", "successor authorization drift")

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
        print(f"OZ-RT-APERY-BROW-001 validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("OZ-RT-APERY-BROW-001 proof and formal-correspondence package is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
