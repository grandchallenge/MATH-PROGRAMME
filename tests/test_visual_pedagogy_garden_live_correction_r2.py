import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "governance" / "visual_pedagogy" / "garden_live_correction_r2.json"
CORRECTION = ROOT / "governance" / "visual_pedagogy" / "garden_correction_r2.json"
CONTRACT = ROOT / "governance" / "visual_pedagogy" / "plates" / "UC-GARDEN-PLATE-I.json"
HISTORICAL = ROOT / "governance" / "visual_pedagogy" / "batch1_live_switch.json"
RUNTIME = ROOT / "docs" / "javascripts" / "documentary.js"
R1 = ROOT / "docs" / "assets" / "visual_pedagogy" / "batch1" / "union_closed" / "plate_garden.svg"
R2 = ROOT / "docs" / "assets" / "visual_pedagogy" / "batch1" / "union_closed" / "plate_garden_r2.svg"
R2_SOURCE = ROOT / "governance" / "visual_pedagogy" / "review_candidates" / "union_closed" / "plate_garden_successor_r2.svg"

R1_SHA256 = "a70b8af6df46589d0df3d2c5c508e54933dd8c01259711e75640821f2188cef7"
R1_BLOB = "83554d48df79b0c15d1772ab47918acdcdd77ca4"
R2_SHA256 = "2931b423942ac079002b37233e4a42a1f4a6da462f096938393b2715dd71d296"
R2_BLOB = "36ea19cdb49aa444b533075171e26a1b2fb002d4"
HISTORICAL_BLOB = "738938edd80713593389491d82b3d90fcdaa0d72"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


class GardenLiveCorrectionR2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.correction = json.loads(CORRECTION.read_text(encoding="utf-8"))
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.runtime = RUNTIME.read_text(encoding="utf-8")
        cls.svg = R2.read_text(encoding="utf-8")

    def test_admitted_r2_bytes_are_reused_exactly(self):
        self.assertEqual(R2_SOURCE.read_bytes(), R2.read_bytes())
        self.assertEqual(R2_SHA256, sha256(R2_SOURCE))
        self.assertEqual(R2_SHA256, sha256(R2))
        self.assertEqual(R2_BLOB, git_blob(R2_SOURCE))
        self.assertEqual(R2_BLOB, git_blob(R2))

    def test_r1_is_preserved_as_exact_rollback_identity(self):
        self.assertEqual(R1_SHA256, sha256(R1))
        self.assertEqual(R1_BLOB, git_blob(R1))
        rollback = self.ledger["r1_rollback"]
        self.assertEqual(R1_SHA256, rollback["sha256"])
        self.assertEqual(R1_BLOB, rollback["git_blob"])
        self.assertTrue(rollback["preserved"])
        self.assertTrue(self.ledger["rollback"]["r1_remains_addressable"])
        self.assertFalse(self.ledger["rollback"]["deletion_required"])

    def test_only_garden_runtime_reference_moves_to_r2(self):
        garden_key = "'../../assets/documentaries/union_closed/plate_garden.svg': {"
        start = self.runtime.index(garden_key)
        end = self.runtime.index("\n      },", start)
        block = self.runtime[start:end]
        self.assertIn("../../assets/visual_pedagogy/batch1/union_closed/plate_garden_r2.svg", block)
        self.assertNotIn("../../assets/visual_pedagogy/batch1/union_closed/plate_garden.svg", block)
        self.assertIn("strict Hasse-style cover diagram", block)
        self.assertIn("without claiming the general Frankl conjecture", block)
        self.assertEqual(1, self.runtime.count("plate_garden_r2.svg"))
        self.assertNotIn("plate_garden_successor_r2.svg", self.runtime)

        unchanged_live_refs = [
            "../../assets/visual_pedagogy/batch1/union_closed/plate_frequency.svg",
            "../../assets/visual_pedagogy/batch1/union_closed/plate_lattice.svg",
            "../../assets/visual_pedagogy/batch1/union_closed/plate_entropy.svg",
            "../../assets/visual_pedagogy/batch1/union_closed/plate_frontier.svg",
            "../../assets/visual_pedagogy/batch1/bsd/plate_curve.png",
        ]
        for ref in unchanged_live_refs:
            self.assertEqual(1, self.runtime.count(ref), ref)
        self.assertEqual(6, self.runtime.count("src: '../../assets/visual_pedagogy/batch1/"))

    def test_historical_batch1_activation_record_is_not_rewritten(self):
        self.assertEqual(HISTORICAL_BLOB, git_blob(HISTORICAL))
        historical = json.loads(HISTORICAL.read_text(encoding="utf-8"))
        garden = next(item for item in historical["plates"] if item["plate_id"] == "UC-GARDEN-PLATE-I")
        self.assertEqual("docs/assets/visual_pedagogy/batch1/union_closed/plate_garden.svg", garden["live_path"])
        self.assertEqual("../../assets/visual_pedagogy/batch1/union_closed/plate_garden.svg", garden["live_reference"])
        self.assertEqual("sha256:" + R1_SHA256, garden["reviewed_digest"])
        self.assertEqual(R1_BLOB, garden["live_blob"])

    def test_ledger_binds_review_candidate_admission_and_fail_closed_state(self):
        self.assertEqual(438, self.ledger["issue"])
        self.assertEqual(435, self.ledger["parent_correction_issue"])
        self.assertEqual(416, self.ledger["propagation_issue"])
        self.assertEqual(436, self.ledger["candidate_pr"])
        self.assertEqual("8a9baedd7962cc1311801f180ba728c3091b12eb", self.ledger["candidate_admission_merge"])
        review = self.ledger["candidate_review"]
        self.assertEqual("jimsteeg", review["reviewer"])
        self.assertEqual(4911355174, review["review_id"])
        self.assertEqual("3aa37edca34bf2adc64b03e4b088709d6fc69437", review["reviewed_commit"])
        self.assertEqual("APPROVED", review["status"])
        self.assertEqual("LIVE_CORRECTION_CANDIDATE__NO_MERGE_AUTHORITY", self.ledger["state"])
        self.assertTrue(self.ledger["batch2_paused"])
        self.assertFalse(self.ledger["visual_is_evidence"])
        self.assertEqual("one_plate_only", self.ledger["activation"]["scope"])

    def test_correction_record_preserves_separate_authority_boundary(self):
        candidate = self.correction["correction_candidate"]
        self.assertEqual("approved_and_candidate_admitted", candidate["review_status"])
        self.assertEqual("8a9baedd7962cc1311801f180ba728c3091b12eb", candidate["candidate_admission_merge"])
        self.assertFalse(candidate["live_switch_authorized"])
        self.assertTrue(self.correction["batch2_paused"])
        self.assertFalse(self.correction["visual_is_evidence"])

    def test_r2_semantics_cure_the_recorded_presentation_defects(self):
        self.assertEqual(7, self.svg.count('class="line"'))
        self.assertIn('aria-label="empty set"', self.svg)
        self.assertIn("strict Hasse-style inclusion diagram", self.svg)
        self.assertIn("a exceeds and b meets", self.svg)
        self.assertIn("Selected unions", self.svg)
        self.assertIn("with at least one nonempty member", self.svg)
        self.assertNotIn("a and b meet", self.svg)
        self.assertNotIn("every finite nonempty union-closed family", self.svg)
        self.assertIn("visual_is_evidence: false", self.svg)

    def test_contract_preserves_r1_history_and_binds_r2_review(self):
        derivatives = {item["path"]: item for item in self.contract["derivatives"]}
        self.assertEqual("sha256:" + R1_SHA256, derivatives["governance/visual_pedagogy/review_candidates/union_closed/plate_garden_successor.svg"]["digest"])
        self.assertEqual("sha256:" + R2_SHA256, derivatives["governance/visual_pedagogy/review_candidates/union_closed/plate_garden_successor_r2.svg"]["digest"])
        self.assertEqual("sha256:" + R2_SHA256, derivatives["docs/assets/visual_pedagogy/batch1/union_closed/plate_garden_r2.svg"]["digest"])
        refs = self.contract["independent_review"]["evidence_refs"]
        self.assertIn("https://github.com/grandchallenge/MATH-PROGRAMME/issues/429#issuecomment-5252274813", refs)
        self.assertIn("https://github.com/grandchallenge/MATH-PROGRAMME/pull/436#pullrequestreview-4911355174", refs)
        self.assertFalse(self.contract["claim_boundary"]["visual_is_evidence"])
        self.assertIn("seven cover relations", self.contract["claim_boundary"]["strongest_visual_claim"])


if __name__ == "__main__":
    unittest.main()
