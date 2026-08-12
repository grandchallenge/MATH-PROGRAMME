import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance/visual_pedagogy/batch2_candidate_manifest.json"
STAGE0 = ROOT / "governance/visual_pedagogy/propagation_manifest.json"
RENDERER = ROOT / "tools/render_visual_pedagogy_batch2_svg_candidates.py"
REVIEW = "https://github.com/grandchallenge/MATH-PROGRAMME/issues/452#issuecomment-5260912708"
MATRIX = "https://github.com/grandchallenge/MATH-PROGRAMME/issues/452#issuecomment-5260869772"

ORDER = [
    "docs/assets/documentaries/bsd/plate_bridge.svg",
    "docs/assets/documentaries/bsd/plate_harmony.svg",
    "docs/assets/documentaries/bsd/plate_frontier.svg",
    "docs/assets/documentaries/bsd/plate_overture.svg",
    "docs/assets/documentaries/hodge/cycles.svg",
    "docs/assets/documentaries/hodge/diamond.svg",
]
BLOBS = {
    ORDER[0]: "cf46ce8633c3d964ed21ced776494375c1c0cbff",
    ORDER[1]: "845fa10b8b13ec99a8d61dd6fb51543c113f43b3",
    ORDER[2]: "457c5de53b36d2de3cac0ab534e2545949084f57",
    ORDER[3]: "c151081594dcf3ae04f15863f85b8c3a32aa7440",
    ORDER[4]: "a89e4851b30ec7ac858da9f999328abed168eb90",
    ORDER[5]: "eb928bbf9a6d31e14b5eaa183805023d48f16ac2",
}


def sha256(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def renderer():
    spec = importlib.util.spec_from_file_location("batch2_renderer", RENDERER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Batch2CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads(MANIFEST.read_text())
        cls.s0 = json.loads(STAGE0.read_text())
        cls.by_id = {r["plate_id"]: r for r in cls.m["plates"]}

    def test_exact_scope_review_and_nonauthority(self):
        self.assertEqual(self.m["state"], "BATCH2_PLATE_REVIEW_COMPLETE__CANDIDATE_ADMISSION_IN_PROGRESS__NO_LIVE_REFERENCE_SWITCH")
        self.assertEqual(self.m["review_issue"], 452)
        self.assertEqual(self.m["review_evidence"], REVIEW)
        self.assertEqual(self.m["review_matrix_evidence"], MATRIX)
        self.assertEqual(self.m["review_outcome"], "APPROVED_ALL_SIX_WITH_NO_ADDITIONAL_RESERVATIONS")
        self.assertEqual(self.m["expected_plate_count"], 6)
        self.assertEqual([r["predecessor_path"] for r in self.m["plates"]], ORDER)
        self.assertEqual(self.s0["batches"]["2"], ORDER)
        self.assertTrue(self.m["authority"]["candidate_admission_recording"])
        self.assertFalse(self.m["authority"]["live_reference_switch"])
        self.assertFalse(self.m["authority"]["batch2_merge_authority"])
        self.assertFalse(self.m["authority"]["visual_is_evidence"])
        for r in self.m["plates"]:
            self.assertEqual(r["predecessor_blob"], BLOBS[r["predecessor_path"]])
            self.assertEqual(r["rollback_blob"], BLOBS[r["predecessor_path"]])
            self.assertEqual(git_blob(ROOT / r["predecessor_path"]), BLOBS[r["predecessor_path"]])
            self.assertTrue(r["independent_review_state"].startswith("reviewed"))
            self.assertFalse(r["live_reference_switched"])
            self.assertFalse(r["live_switch_eligibility"])
            self.assertFalse(r["visual_is_evidence"])

    def test_contracts_bind_exact_review_evidence(self):
        for r in self.m["plates"]:
            c = json.loads((ROOT / r["contract_path"]).read_text())
            self.assertEqual(c["predecessor"], r["predecessor_path"])
            self.assertFalse(c["claim_boundary"]["visual_is_evidence"])
            self.assertTrue(c["renderer"]["reproducible"])
            self.assertEqual(c["derivatives"][0]["path"], r["candidate_path"])
            self.assertEqual(c["derivatives"][0]["digest"], r["candidate_digest"])
            if r["candidate_origin"] == "batch2_new":
                self.assertEqual(c["independent_review"]["status"], "reviewed")
                self.assertEqual(c["independent_review"]["reviewer"], "jimsteeg")
                self.assertEqual(c["independent_review"]["evidence_refs"], [REVIEW])
            else:
                self.assertEqual(c["independent_review"]["status"], "reviewed")
                self.assertIn("batch2_adoption_review", c)
                self.assertEqual(c["batch2_adoption_review"]["status"], "reviewed")
                self.assertEqual(c["batch2_adoption_review"]["reviewer"], "jimsteeg")
                self.assertEqual(c["batch2_adoption_review"]["evidence_refs"], [REVIEW])
                self.assertEqual(c["batch2_adoption_review"]["matrix_ref"], MATRIX)

    def test_generator_and_superseded_history(self):
        generated = {str(p.relative_to(ROOT)): c for p, c in renderer().OUTPUTS.items()}
        active_new = [r for r in self.m["plates"] if r["candidate_origin"] == "batch2_new"]
        superseded = self.m["superseded_drafts"]
        self.assertEqual(len(active_new), 5)
        self.assertEqual(len(superseded), 1)
        expected = {r["candidate_path"] for r in active_new} | {superseded[0]["candidate_path"]}
        self.assertEqual(set(generated), expected)
        for r in active_new:
            p = ROOT / r["candidate_path"]
            self.assertEqual(p.read_text(), generated[r["candidate_path"]])
            self.assertEqual(r["candidate_digest"], sha256(p))
        d = superseded[0]
        p = ROOT / d["candidate_path"]
        self.assertEqual(p.read_text(), generated[d["candidate_path"]])
        self.assertEqual(d["candidate_digest"], sha256(p))
        self.assertEqual(d["disposition"], "SUPERSEDED_BEFORE_REVIEW")
        self.assertFalse(d["live_switch_eligibility"])

    def test_no_candidate_is_live_or_documentary_referenced(self):
        docs = "\n".join(p.read_text() for p in sorted((ROOT / "docs/documentaries").glob("*.md")))
        for r in self.m["plates"]:
            self.assertTrue(r["candidate_path"].startswith("governance/visual_pedagogy/review_candidates/"))
            self.assertNotIn(r["candidate_path"], docs)
            self.assertNotIn(Path(r["candidate_path"]).name, docs)
        self.assertFalse((ROOT / "governance/visual_pedagogy/plates/HODGE-CYCLES-PLATE-III.json").exists())

    def test_semantic_guardrails(self):
        checks = {
            "BSD-BRIDGE-PLATE-III": ["no single local factor determines", "BSD conjectures r_alg = r_an"],
            "BSD-HARMONY-PLATE-II": ["r_alg ?= r_an", "conjectural bridge"],
            "BSD-FRONTIER-PLATE-V": ["Analytic rank 0 or 1", "universal rank equality", "OPEN"],
            "BSD-OVERTURE-PLATE-IV": ["Three obligations remain logically distinct", "finiteness of Sha"],
            "HODGE-DIAMOND-PLATE-II": ["does not invent Hodge numbers", "necessary, but the general converse"],
        }
        for plate_id, needles in checks.items():
            text = (ROOT / self.by_id[plate_id]["candidate_path"]).read_text()
            for needle in needles:
                self.assertIn(needle, text)
        cycle = json.loads((ROOT / self.by_id["HC-CYCLE-CLASS-PLATE-III"]["contract_path"]).read_text())
        self.assertIn("General surjectivity", cycle["claim_boundary"]["not_claimed"])
        self.assertIn("The integral Hodge conjecture", cycle["claim_boundary"]["not_claimed"])


if __name__ == "__main__":
    unittest.main()
