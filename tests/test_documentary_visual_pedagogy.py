from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_documentary_visual_pedagogy import (  # noqa: E402
    AUDIT_PATH,
    SCHEMA_PATH,
    audit_inventory,
    git_blob_sha,
    load_json,
    visual_pedagogy_errors,
)


class DocumentaryVisualPedagogyTests(unittest.TestCase):
    def test_live_visual_pedagogy_contract_is_closed(self) -> None:
        self.assertEqual([], visual_pedagogy_errors(ROOT))

    def test_audit_counts_and_positive_controls(self) -> None:
        audit = load_json(ROOT / AUDIT_PATH)
        inventory = audit_inventory(audit)
        self.assertEqual(45, len(inventory))
        self.assertEqual(8, audit["inventory_counts"]["decorative_covers"])
        self.assertEqual(37, audit["inventory_counts"]["instructional_plates"])
        self.assertEqual(8, len(audit["reference_pilot"]["selected"]))
        dispositions = {item["disposition"] for item in audit["reference_pilot"]["selected"]}
        self.assertIn("KEEP", dispositions)
        self.assertTrue({"REDRAW", "REPLACE"} & dispositions)

    def test_predecessor_git_identity_is_bound(self) -> None:
        audit = load_json(ROOT / AUDIT_PATH)
        inventory = {item["asset"]: item for item in audit_inventory(audit)}
        relative = "docs/assets/documentaries/p_vs_np/reduction.svg"
        self.assertEqual(
            inventory[relative]["blob_sha"],
            git_blob_sha(ROOT / relative),
        )

    def test_schema_rejects_visual_evidence_promotion(self) -> None:
        schema = load_json(ROOT / SCHEMA_PATH)
        validator = Draft202012Validator(schema)
        contract_path = ROOT / "governance/visual_pedagogy/plates/PNP-REDUCTION-PLATE-II.json"
        contract = load_json(contract_path)
        mutation = copy.deepcopy(contract)
        mutation["claim_boundary"]["visual_is_evidence"] = True
        self.assertTrue(list(validator.iter_errors(mutation)))

    def test_schema_rejects_unknown_representation_class(self) -> None:
        schema = load_json(ROOT / SCHEMA_PATH)
        validator = Draft202012Validator(schema)
        contract_path = ROOT / "governance/visual_pedagogy/plates/EUCLID-ANTHYPHAIRESIS-PLATE-I.json"
        contract = load_json(contract_path)
        mutation = copy.deepcopy(contract)
        mutation["representation_class"] = "looks-correct"
        self.assertTrue(list(validator.iter_errors(mutation)))

    def test_all_pilot_contracts_keep_independent_review_explicit(self) -> None:
        contract_dir = ROOT / "governance/visual_pedagogy/plates"
        contracts = [json.loads(path.read_text(encoding="utf-8")) for path in contract_dir.glob("*.json")]
        self.assertEqual(8, len(contracts))
        self.assertTrue(all(contract["independent_review"]["status"] == "pending" for contract in contracts))

    def test_successor_renderer_compiles(self) -> None:
        generator_path = ROOT / "tools/render_visual_pedagogy_successors.py"
        source = generator_path.read_text(encoding="utf-8")
        compile(source, str(generator_path), "exec")

    def test_successor_derivative_sha256_digests_are_bound(self) -> None:
        contract_dir = ROOT / "governance/visual_pedagogy/plates"
        checked = 0
        for contract_path in sorted(contract_dir.glob("*.json")):
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            for derivative in contract.get("derivatives", []):
                digest = derivative.get("digest")
                if not isinstance(digest, str) or not digest.startswith("sha256:"):
                    continue
                path = ROOT / derivative["path"]
                self.assertTrue(path.is_file(), derivative["path"])
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(digest.removeprefix("sha256:"), actual, derivative["path"])
                checked += 1
        self.assertEqual(7, checked)

    def test_successor_manifest_preserves_authority_boundary_and_controls(self) -> None:
        manifest = load_json(ROOT / "governance/visual_pedagogy/successor_render_manifest.json")
        self.assertEqual("MP-DOC-VISUAL-PILOT-SUCCESSORS-001", manifest["operation_id"])
        self.assertEqual("3b79b35fadc6805775246c03124deb3e1425ef86", manifest["protected_base_commit"])
        self.assertFalse(manifest["authority_boundary"]["visual_is_evidence"])
        self.assertFalse(manifest["authority_boundary"]["programme_wide_migration_authorized"])
        self.assertFalse(manifest["authority_boundary"]["mathematical_claim_promoted"])
        controls = {item["path"]: item["git_blob"] for item in manifest["positive_controls"]}
        self.assertEqual(
            "e351902a073e9fdb41d0953400992d1732fd0fd4",
            controls["docs/assets/documentaries/p_vs_np/reduction.svg"],
        )
        self.assertEqual(
            "6bcddb97bcd31d99575cfbbe1f6698b9c6eb3cd1",
            controls["docs/assets/documentaries/euclid_book_vii/plate_anthyphairesis.svg"],
        )


if __name__ == "__main__":
    unittest.main()
