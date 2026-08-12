import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/visual_pedagogy/batch2_live_switch.json"
BATCH1 = ROOT / "governance/visual_pedagogy/batch1_live_switch.json"
GARDEN = ROOT / "governance/visual_pedagogy/garden_live_correction_r2.json"
RUNTIME = ROOT / "docs/javascripts/documentary.js"
REVIEW_REF = "https://github.com/grandchallenge/MATH-PROGRAMME/issues/452#issuecomment-5260912708"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class VisualPedagogyBatch2LiveSwitchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.runtime = RUNTIME.read_text(encoding="utf-8")
        cls.docs = {
            "bsd": (ROOT / "docs/documentaries/bsd.md").read_text(encoding="utf-8"),
            "hodge": (ROOT / "docs/documentaries/hodge.md").read_text(encoding="utf-8"),
        }

    def test_live_switch_scope_and_authority_boundary(self):
        data = self.data
        self.assertEqual(data["operation_id"], "MP-DOC-VISUAL-PROPAGATION-BATCH2-LIVE-SWITCH-001")
        self.assertEqual(data["parent_issue"], 416)
        self.assertEqual(data["implementation_issue"], 457)
        self.assertEqual(data["candidate_issue"], 445)
        self.assertEqual(data["candidate_pr"], 447)
        self.assertEqual(data["review_issue"], 452)
        self.assertEqual(data["review_evidence"], REVIEW_REF)
        self.assertEqual(data["candidate_admission_merge"], "8857be70791f379f27c534eb4f5b1630c6c82c68")
        self.assertEqual(data["candidate_admission_policy_run"], 31567944355)
        self.assertEqual(data["state"], "LIVE_SWITCH_CANDIDATE__NO_MERGE_AUTHORITY")
        self.assertFalse(data["live_switch_authorized"])
        self.assertIsNone(data["activation_merge"])
        self.assertEqual(data["expected_plate_count"], 6)
        self.assertFalse(data["visual_is_evidence"])
        self.assertEqual(data["live_asset_root"], "docs/assets/visual_pedagogy/batch2")
        self.assertTrue(data["predecessor_policy"]["preserve_bytes"])
        self.assertTrue(data["predecessor_policy"]["preserve_paths"])
        self.assertFalse(data["predecessor_policy"]["delete_or_overwrite_predecessor"])
        self.assertEqual(data["runtime_scope"]["expected_new_mapping_count"], 6)
        self.assertTrue(data["runtime_scope"]["batch1_mappings_unchanged"])
        self.assertTrue(data["runtime_scope"]["source_markdown_unchanged"])
        self.assertEqual(len(data["plates"]), 6)

    def test_six_live_assets_are_byte_identical_to_admitted_candidates(self):
        ids = set()
        live_paths = set()
        source_refs = set()
        live_refs = set()

        for plate in self.data["plates"]:
            ids.add(plate["plate_id"])
            live_paths.add(plate["live_path"])
            source_refs.add(plate["source_reference"])
            live_refs.add(plate["live_reference"])

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
            self.assertTrue(plate["live_path"].startswith("docs/assets/visual_pedagogy/batch2/"))
            self.assertTrue(plate["predecessor_path"].startswith("docs/assets/documentaries/"))
            self.assertNotEqual(plate["live_path"], plate["predecessor_path"])

        self.assertEqual(len(ids), 6)
        self.assertEqual(len(live_paths), 6)
        self.assertEqual(len(source_refs), 6)
        self.assertEqual(len(live_refs), 6)

    def test_runtime_contains_exactly_six_batch2_rewrites(self):
        self.assertEqual(self.runtime.count("../../assets/visual_pedagogy/batch2/"), 6)
        for plate in self.data["plates"]:
            self.assertEqual(self.runtime.count(repr(plate["source_reference"])), 1)
            self.assertEqual(self.runtime.count(repr(plate["live_reference"])), 1)
        self.assertNotIn("governance/visual_pedagogy/review_candidates/", self.runtime)

    def test_source_markdown_preserves_rollback_references(self):
        for plate in self.data["plates"]:
            doc = self.docs[plate["reader"]]
            self.assertIn(plate["source_reference"], doc)
            self.assertNotIn(plate["live_reference"], doc)

    def test_contracts_bind_candidate_and_live_derivatives(self):
        for plate in self.data["plates"]:
            contract_path = ROOT / "governance/visual_pedagogy/plates" / f"{plate['plate_id']}.json"
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            self.assertEqual(contract["predecessor"], plate["predecessor_path"])
            self.assertEqual(contract["independent_review"]["status"], "reviewed")
            self.assertIn(REVIEW_REF, contract["independent_review"]["evidence_refs"])
            self.assertFalse(contract["claim_boundary"]["visual_is_evidence"])
            derivatives = {item["path"]: item for item in contract["derivatives"]}
            self.assertIn(plate["review_candidate_path"], derivatives)
            self.assertIn(plate["live_path"], derivatives)
            self.assertEqual(derivatives[plate["review_candidate_path"]]["digest"], plate["reviewed_digest"])
            self.assertEqual(derivatives[plate["live_path"]]["digest"], plate["reviewed_digest"])

    def test_all_batch1_runtime_mappings_remain_present(self):
        batch1 = json.loads(BATCH1.read_text(encoding="utf-8"))
        correction = json.loads(GARDEN.read_text(encoding="utf-8")) if GARDEN.is_file() else None
        for plate in batch1["plates"]:
            self.assertEqual(self.runtime.count(repr(plate["source_reference"])), 1)
            expected_live = plate["live_reference"]
            if plate["plate_id"] == "UC-GARDEN-PLATE-I" and correction:
                if correction.get("state") == "LIVE_CORRECTION_CANDIDATE__NO_MERGE_AUTHORITY":
                    expected_live = correction["activation"]["r2_runtime_reference"]
            self.assertEqual(self.runtime.count(repr(expected_live)), 1)
        self.assertEqual(self.runtime.count("../../assets/visual_pedagogy/batch1/"), 6)

    def test_superseded_hodge_cycles_draft_is_preserved_and_non_live(self):
        history = self.data["superseded_history"]
        self.assertEqual(len(history), 1)
        entry = history[0]
        path = ROOT / entry["path"]
        self.assertTrue(path.is_file())
        self.assertEqual(entry["disposition"], "SUPERSEDED_BEFORE_REVIEW")
        self.assertFalse(entry["live_switch_eligibility"])
        self.assertTrue(entry["preserved"])
        self.assertNotIn(entry["path"], self.runtime)
        self.assertNotIn(path.name, self.runtime)


if __name__ == "__main__":
    unittest.main()
