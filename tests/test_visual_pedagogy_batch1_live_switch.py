import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/visual_pedagogy/batch1_live_switch.json"
RUNTIME = ROOT / "docs/javascripts/documentary.js"
GARDEN_CORRECTION = ROOT / "governance/visual_pedagogy/garden_live_correction_r2.json"
REVIEW_REF = "https://github.com/grandchallenge/MATH-PROGRAMME/issues/429#issuecomment-5252274813"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


class VisualPedagogyBatch1LiveSwitchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.runtime = RUNTIME.read_text(encoding="utf-8")
        cls.superseded_runtime_refs = {}
        if GARDEN_CORRECTION.is_file():
            correction = json.loads(GARDEN_CORRECTION.read_text(encoding="utf-8"))
            if correction.get("state") == "LIVE_CORRECTION_CANDIDATE__NO_MERGE_AUTHORITY":
                cls.superseded_runtime_refs["UC-GARDEN-PLATE-I"] = correction["activation"]["r2_runtime_reference"]

    def test_batch1_live_switch_is_exact_and_review_bound(self):
        data = self.data
        self.assertEqual(
            data["operation_id"],
            "MP-DOC-VISUAL-PROPAGATION-BATCH1-LIVE-SWITCH-001",
        )
        self.assertEqual(data["implementation_issue"], 431)
        self.assertEqual(data["review_issue"], 429)
        self.assertEqual(data["review_evidence"], REVIEW_REF)
        self.assertEqual(data["expected_plate_count"], 6)
        self.assertFalse(data["visual_is_evidence"])
        self.assertEqual(data["activation_mode"], "shared_reader_exact_path_rewrite")
        self.assertEqual(data["live_asset_root"], "docs/assets/visual_pedagogy/batch1")
        self.assertTrue(data["predecessor_policy"]["preserve_audited_asset_root"])
        self.assertEqual(len(data["plates"]), 6)

        ids = set()
        live_paths = set()
        predecessors = set()

        for plate in data["plates"]:
            ids.add(plate["plate_id"])
            live_paths.add(plate["live_path"])
            predecessors.add(plate["predecessor_path"])
            self.assertEqual(plate["review_outcome"], "APPROVED")
            self.assertNotEqual(plate["live_path"], plate["predecessor_path"])
            self.assertNotEqual(plate["source_reference"], plate["live_reference"])
            self.assertTrue(plate["live_path"].startswith("docs/assets/visual_pedagogy/batch1/"))
            self.assertTrue(plate["predecessor_path"].startswith("docs/assets/documentaries/"))

            predecessor = ROOT / plate["predecessor_path"]
            candidate = ROOT / plate["review_candidate_path"]
            live = ROOT / plate["live_path"]
            self.assertTrue(predecessor.is_file())
            self.assertTrue(candidate.is_file())
            self.assertTrue(live.is_file())
            self.assertEqual(live.read_bytes(), candidate.read_bytes())
            self.assertEqual(sha256(live), plate["reviewed_digest"])

            self.assertEqual(self.runtime.count(repr(plate["source_reference"])), 1)
            current_ref = self.superseded_runtime_refs.get(plate["plate_id"])
            if current_ref is None:
                self.assertEqual(self.runtime.count(repr(plate["live_reference"])), 1)
            else:
                self.assertEqual(self.runtime.count(repr(plate["live_reference"])), 0)
                self.assertEqual(self.runtime.count(repr(current_ref)), 1)

            contract_path = (
                ROOT / "governance/visual_pedagogy/plates" / f"{plate['plate_id']}.json"
            )
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            self.assertEqual(contract["independent_review"]["status"], "reviewed")
            self.assertIn(REVIEW_REF, contract["independent_review"]["evidence_refs"])
            self.assertFalse(contract["claim_boundary"]["visual_is_evidence"])
            self.assertEqual(contract["predecessor"], plate["predecessor_path"])

        self.assertEqual(len(ids), 6)
        self.assertEqual(len(live_paths), 6)
        self.assertEqual(len(predecessors), 6)

    def test_batch1_source_pages_keep_exact_rollback_references(self):
        docs = {
            "union_closed": (ROOT / "docs/documentaries/union_closed.md").read_text(
                encoding="utf-8"
            ),
            "bsd": (ROOT / "docs/documentaries/bsd.md").read_text(encoding="utf-8"),
        }
        for plate in self.data["plates"]:
            self.assertIn(plate["source_reference"], docs[plate["reader"]])
            self.assertNotIn(plate["live_reference"], docs[plate["reader"]])

    def test_batch1_scope_does_not_activate_later_assets(self):
        self.assertEqual(self.runtime.count("dataset.visualPedagogyActivation"), 1)
        self.assertEqual(self.runtime.count("visualPedagogyActivation = 'batch1'"), 1)
        self.assertNotIn("plate_vorticity_v2", self.runtime)
        self.assertNotIn("plate_geometry_v2", self.runtime)
        self.assertNotIn("plate_gauge_v2", self.runtime)


if __name__ == "__main__":
    unittest.main()
