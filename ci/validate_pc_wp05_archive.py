#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REQUIRED_CLAIMS = {f"PC05-C{i:03d}" for i in range(1, 12)}
REQUIRED_SOURCES = {"P-I", "P-II", "P-III", "KL", "MT"}
REQUIRED_DISCLOSURES = {
    "not a new proof",
    "analytic Ricci-flow proof not formalized",
    "schema validity does not prove event existence",
    "Lean result conditional on ImportedEventRelation",
    "line-by-line source concordance incomplete",
    "no novelty or priority claim",
}
REQUIRED_CHECKS = {"PC-WP05 archival checks", "Programme policy checks"}


def fail(message: str) -> None:
    raise SystemExit(f"PC-WP05 archive policy failure: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load JSON {path}: {exc}")


def main() -> None:
    root = Path.cwd()
    wp = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "campaigns/poincare_reconstruction/WP05_INTEGRATED_CLOSURE"
    )
    required = [
        wp / "00_README.md",
        wp / "01_INTEGRATED_DOSSIER.md",
        wp / "02_SOURCE_CONCORDANCE.md",
        wp / "03_CLAIM_TRUST_MATRIX.yaml",
        wp / "04_CATEGORY_AUDIT.md",
        wp / "05_NON_CIRCULARITY_AUDIT.md",
        wp / "06_DEPENDENCY_CLOSURE.json",
        wp / "07_PUBLICATION_READINESS.md",
        wp / "08_PROOF_DEBT.json",
        wp / "09_ARCHIVAL_MANIFEST.json",
        wp / "10_NEXT_STAGE.md",
    ]
    for path in required:
        if not path.is_file():
            fail(f"missing required artifact {path}")

    manifest = load_json(wp / "09_ARCHIVAL_MANIFEST.json")
    if manifest.get("archive_id") != "ARCHIVE-PC-001":
        fail("incorrect archive_id")
    if manifest.get("publication_status") != "READY_FOR_QUALIFIED_SOLVED_PROBLEM_ARCHIVAL_PUBLICATION":
        fail("archive is not in the qualified-ready state")
    if set(manifest.get("mandatory_disclosures", [])) != REQUIRED_DISCLOSURES:
        fail("mandatory disclosure set drift")
    if set(manifest.get("evidence_policy", {}).get("required_checks", [])) != REQUIRED_CHECKS:
        fail("required check set drift")
    if manifest.get("evidence_policy", {}).get("self_referential_commit_hash") is not False:
        fail("evidence policy must prohibit self-referential commit binding")
    source_keys = {entry.get("key") for entry in manifest.get("source_editions", [])}
    if source_keys != REQUIRED_SOURCES:
        fail(f"source edition set drift: {sorted(source_keys ^ REQUIRED_SOURCES)}")
    for artifact in manifest.get("canonical_artifacts", []):
        if not (root / artifact).is_file():
            fail(f"manifest references missing artifact {artifact}")

    closure = load_json(wp / "06_DEPENDENCY_CLOSURE.json")
    state = closure.get("closure", {})
    required_true = (
        "all_material_edges_classified",
        "category_bridge_explicit",
        "non_circularity_audited",
        "critical_source_concordance_closed",
        "qualified_archival_publication_ready",
    )
    for key in required_true:
        if state.get(key) is not True:
            fail(f"closure flag {key} must be true")
    if state.get("line_by_line_source_concordance_closed") is not False:
        fail("line-by-line concordance must remain explicitly open")
    if state.get("full_analytic_formalization") is not False:
        fail("full analytic formalization must remain false")
    if not closure.get("forbidden_edges"):
        fail("forbidden-edge register is empty")

    matrix = yaml.safe_load((wp / "03_CLAIM_TRUST_MATRIX.yaml").read_text(encoding="utf-8"))
    claim_ids = {entry.get("id") for entry in matrix.get("claims", [])}
    if claim_ids != REQUIRED_CLAIMS:
        fail(f"claim set drift: {sorted(claim_ids ^ REQUIRED_CLAIMS)}")
    if not matrix.get("permanent_prohibitions"):
        fail("permanent prohibitions missing")

    debts = load_json(wp / "08_PROOF_DEBT.json")
    gate = debts.get("publication_gate", {})
    if gate.get("qualified_archival_publication") != "pass":
        fail("qualified publication gate must pass")
    for key in ("new_proof_claim", "full_formal_proof_claim", "independent_analytic_verification_claim"):
        if gate.get(key) not in {"blocked", "permanently_prohibited"}:
            fail(f"stronger claim gate {key} is not blocked")

    concordance = (wp / "02_SOURCE_CONCORDANCE.md").read_text(encoding="utf-8")
    for token in REQUIRED_SOURCES | {"unjustified", "retained concordance debt"}:
        if token not in concordance:
            fail(f"source concordance omits {token}")

    readiness = (wp / "07_PUBLICATION_READINESS.md").read_text(encoding="utf-8")
    if "READY_FOR_QUALIFIED_SOLVED_PROBLEM_ARCHIVAL_PUBLICATION" not in readiness:
        fail("publication decision missing from readiness record")

    print("PC-WP05 archival policy validation passed")


if __name__ == "__main__":
    main()
