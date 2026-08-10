from __future__ import annotations

import copy
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


if __name__ == "__main__":
    unittest.main()
