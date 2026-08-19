import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLATES = ROOT / "governance" / "visual_pedagogy" / "plates"
ADJUDICATION = ROOT / "governance" / "visual_pedagogy" / "final_pilot_adjudication.json"
CONTINUITY = ROOT / "governance" / "visual_pedagogy" / "AManuensis_pilot_continuity.md"

PLATE_IDS = {
    "BSD-CURVE-PLATE-I",
    "EUCLID-ANTHYPHAIRESIS-PLATE-I",
    "HC-CYCLE-CLASS-PLATE-III",
    "NS-VORTICITY-PLATE-II",
    "PC-RICCI-FLOW-PLATE-II",
    "PC-SURGERY-PLATE-III",
    "PNP-REDUCTION-PLATE-II",
    "RH-CRITICAL-STRIP-PLATE-II",
}
CORRECTIVE_IDS = {
    "BSD-CURVE-PLATE-I",
    "HC-CYCLE-CLASS-PLATE-III",
    "NS-VORTICITY-PLATE-II",
    "PC-RICCI-FLOW-PLATE-II",
    "PC-SURGERY-PLATE-III",
    "RH-CRITICAL-STRIP-PLATE-II",
}
FREEZE = "https://github.com/grandchallenge/MATH-PROGRAMME/pull/389#issuecomment-5248330492"
REJECTION = "https://github.com/grandchallenge/MATH-PROGRAMME/pull/389#pullrequestreview-4901258988"
RESERVATION = "https://github.com/grandchallenge/MATH-PROGRAMME/pull/389#pullrequestreview-4901948990"
APPROVAL = "https://github.com/grandchallenge/MATH-PROGRAMME/pull/389#pullrequestreview-4902525377"
MERGE_RECEIPT = "https://github.com/grandchallenge/MATH-PROGRAMME/pull/389#issuecomment-5248406572"
RECOMMENDATION = "BROADER_VISUAL_PEDAGOGY_PROPAGATION_RECOMMENDED_AS_STAGED_GOVERNED_MIGRATION_WITH_RESERVATIONS"


def _plate_records():
    records = []
    for path in sorted(PLATES.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("plate_id") in PLATE_IDS:
            records.append(data)
    return records


class VisualPedagogyFinalAdjudicationTests(unittest.TestCase):
    def test_all_eight_pilot_contracts_are_reviewed_and_non_evidentiary(self):
        records = _plate_records()
        self.assertEqual({record["plate_id"] for record in records}, PLATE_IDS)
        for record in records:
            review = record["independent_review"]
            self.assertEqual(review["status"], "reviewed")
            refs = set(review["evidence_refs"])
            self.assertIn(FREEZE, refs)
            self.assertIn(RESERVATION, refs)
            self.assertIn(APPROVAL, refs)
            self.assertIn(MERGE_RECEIPT, refs)
            self.assertFalse(record["claim_boundary"]["visual_is_evidence"])
            if record["plate_id"] in CORRECTIVE_IDS:
                self.assertIn(REJECTION, refs)

    def test_final_adjudication_is_recommendation_not_authority(self):
        data = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
        self.assertEqual(data["operation_id"], "MP-DOC-VISUAL-PILOT-FINAL-ADJUDICATION-001")
        self.assertEqual(data["parent_docket"], 377)
        self.assertEqual(data["implementation_issue"], 410)
        self.assertEqual(data["recommendation"], RECOMMENDATION)
        self.assertEqual(data["findings"]["reviewer_final_state"], "APPROVED")
        self.assertTrue(data["findings"]["reviewer_reservation_preserved"])
        self.assertFalse(data["findings"]["visual_is_evidence"])
        self.assertFalse(data["propagation_authority"])
        self.assertFalse(data["mathematical_claim_promotion"])
        self.assertFalse(data["live_documentary_asset_replacement_authorized_by_this_record"])
        self.assertEqual(data["evidence"]["reviewed_head"], "603a0df8f40797dbf0ec75c53ac4144b70458eba")
        self.assertEqual(data["evidence"]["protected_successor_merge"], "50f2b4d975b96ab34e26b14192ff635045170cf0")

    def test_amanuensis_record_preserves_rejection_controls_and_exact_review(self):
        text = CONTINUITY.read_text(encoding="utf-8")
        for token in (
            "4901258988",
            "4901948990",
            "4902525377",
            "603a0df8f40797dbf0ec75c53ac4144b70458eba",
            "50f2b4d975b96ab34e26b14192ff635045170cf0",
            "e351902a073e9fdb41d0953400992d1732fd0fd4",
            "6bcddb97bcd31d99575cfbbe1f6698b9c6eb3cd1",
            RECOMMENDATION,
            "This recommendation is not migration authority",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
