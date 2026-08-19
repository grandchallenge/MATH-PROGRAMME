import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/visual_pedagogy/batch3_live_switch.json"
BATCH1 = ROOT / "governance/visual_pedagogy/batch1_live_switch.json"
BATCH2 = ROOT / "governance/visual_pedagogy/batch2_live_switch.json"
GARDEN = ROOT / "governance/visual_pedagogy/garden_live_correction_r2.json"
RUNTIME = ROOT / "docs/javascripts/documentary.js"
REVIEW_REF = "https://github.com/grandchallenge/MATH-PROGRAMME/issues/483#issuecomment-5272982277"
CONSTRUCTION_BASE = "2440dce88ef15d4d0d4bb4224cab5921f355b210"
EXPECTED_PLATES = [
    "NS-FIELD-PLATE-I",
    "NS-FRONTIER-PLATE-IV",
    "PC-EXTINCTION-PLATE-IV",
    "RH-EULER-PLATE-I",
    "RH-EVIDENCE-PLATE-IV",
]


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class VisualPedagogyBatch3LiveSwitchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.runtime = RUNTIME.read_text(encoding="utf-8")
        cls.docs = {
            name: (ROOT / f"docs/documentaries/{name}.md").read_text(encoding="utf-8")
            for name in ("navier_stokes", "poincare", "riemann")
        }

    def test_scope_authority_and_review_binding(self):
        data = self.data
        self.assertEqual(data["operation_id"], "MP-DOC-VISUAL-PROPAGATION-BATCH3-LIVE-SWITCH-001")
        self.assertEqual(
            (data["parent_issue"], data["implementation_issue"], data["candidate_issue"],
             data["candidate_pr"], data["review_issue"]),
            (416, 484, 466, 467, 483),
        )
        self.assertEqual(data["review_disposition_comment_id"], 5272982277)
        self.assertEqual(data["review_disposition_evidence"], REVIEW_REF)
        self.assertEqual(data["candidate_admission_merge"], "4f5adc7fb355657e22f5e13e1de3dfb5cc7d2f01")
        self.assertEqual(data["construction_base"], CONSTRUCTION_BASE)
        self.assertEqual(data["state"], "LIVE_SWITCH_CANDIDATE__NO_MERGE_AUTHORITY")
        self.assertFalse(data["live_switch_authorized"])
        self.assertIsNone(data["activation_merge"])
        self.assertFalse(data["visual_is_evidence"])
        self.assertEqual(data["expected_plate_count"], 5)
        self.assertEqual([p["plate_id"] for p in data["plates"]], EXPECTED_PLATES)
        self.assertTrue(all(p["review_outcome"] == "APPROVED" for p in data["plates"]))
        self.assertEqual(data["runtime_scope"]["expected_new_mapping_count"], 5)
        self.assertTrue(data["runtime_scope"]["batch1_mappings_unchanged"])
        self.assertTrue(data["runtime_scope"]["batch2_mappings_unchanged"])
        self.assertTrue(data["runtime_scope"]["source_markdown_unchanged"])
        self.assertTrue(data["predecessor_policy"]["preserve_bytes"])
        self.assertTrue(data["predecessor_policy"]["preserve_paths"])
        self.assertFalse(data["predecessor_policy"]["delete_or_overwrite_predecessor"])

    def test_live_assets_are_exact_reviewed_candidates(self):
        self.assertEqual(len(self.data["plates"]), 5)
        for plate in self.data["plates"]:
            predecessor = ROOT / plate["predecessor_path"]
            candidate = ROOT / plate["review_candidate_path"]
            live = ROOT / plate["live_path"]
            self.assertTrue(predecessor.is_file())
            self.assertTrue(candidate.is_file())
            self.assertTrue(live.is_file())
            self.assertEqual(git_blob(predecessor), plate["predecessor_blob"])
            self.assertEqual(git_blob(candidate), plate["candidate_blob"])
            self.assertEqual(git_blob(live), plate["live_blob"])
            self.assertEqual(plate["candidate_blob"], plate["live_blob"])
            self.assertEqual(live.read_bytes(), candidate.read_bytes())
            self.assertEqual(sha256(candidate), plate["reviewed_digest"])
            self.assertEqual(sha256(live), plate["reviewed_digest"])
            self.assertTrue(plate["live_path"].startswith("docs/assets/visual_pedagogy/batch3/"))
            self.assertNotEqual(plate["live_path"], plate["predecessor_path"])

    def test_runtime_has_exactly_five_batch3_rewrites(self):
        self.assertEqual(self.runtime.count("../../assets/visual_pedagogy/batch3/"), 5)
        for plate in self.data["plates"]:
            self.assertEqual(self.runtime.count(repr(plate["source_reference"])), 1)
            self.assertEqual(self.runtime.count(repr(plate["live_reference"])), 1)
        self.assertNotIn("governance/visual_pedagogy/review_candidates/", self.runtime)
        self.assertNotIn("../../assets/visual_pedagogy/batch4/", self.runtime)
        self.assertNotIn("../../assets/visual_pedagogy/batch5/", self.runtime)

    def test_markdown_preserves_rollback_references(self):
        for plate in self.data["plates"]:
            doc = self.docs[plate["reader"]]
            self.assertIn(plate["source_reference"], doc)
            self.assertNotIn(plate["live_reference"], doc)

    def test_contracts_bind_review_and_live_derivative(self):
        for plate in self.data["plates"]:
            contract = json.loads(
                (ROOT / "governance/visual_pedagogy/plates" / f"{plate['plate_id']}.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual(contract["predecessor"], plate["predecessor_path"])
            self.assertEqual(contract["independent_review"]["status"], "reviewed")
            self.assertIn(REVIEW_REF, contract["independent_review"]["evidence_refs"])
            self.assertFalse(contract["claim_boundary"]["visual_is_evidence"])
            derivatives = {item["path"]: item for item in contract["derivatives"]}
            self.assertEqual(
                derivatives[plate["review_candidate_path"]]["digest"], plate["reviewed_digest"]
            )
            self.assertEqual(
                derivatives[plate["live_path"]]["digest"], plate["reviewed_digest"]
            )

    def test_prior_batch_runtime_continuity(self):
        batch1 = json.loads(BATCH1.read_text(encoding="utf-8"))
        batch2 = json.loads(BATCH2.read_text(encoding="utf-8"))
        correction = json.loads(GARDEN.read_text(encoding="utf-8")) if GARDEN.is_file() else None
        for plate in batch1["plates"]:
            self.assertEqual(self.runtime.count(repr(plate["source_reference"])), 1)
            expected_live = plate["live_reference"]
            if (
                plate["plate_id"] == "UC-GARDEN-PLATE-I"
                and correction
                and correction.get("state") == "LIVE_CORRECTION_CANDIDATE__NO_MERGE_AUTHORITY"
            ):
                expected_live = correction["activation"]["r2_runtime_reference"]
            self.assertEqual(self.runtime.count(repr(expected_live)), 1)
        for plate in batch2["plates"]:
            self.assertEqual(self.runtime.count(repr(plate["source_reference"])), 1)
            self.assertEqual(self.runtime.count(repr(plate["live_reference"])), 1)
        self.assertEqual(self.runtime.count("../../assets/visual_pedagogy/batch1/"), 6)
        self.assertEqual(self.runtime.count("../../assets/visual_pedagogy/batch2/"), 6)


if __name__ == "__main__":
    unittest.main()
