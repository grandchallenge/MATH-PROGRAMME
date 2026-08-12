import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance/visual_pedagogy/batch3_candidate_manifest.json"
STAGE0 = ROOT / "governance/visual_pedagogy/propagation_manifest.json"
RENDERER = ROOT / "tools/render_visual_pedagogy_batch3_svg_candidates.py"
ORDER = ['docs/assets/documentaries/navier_stokes/field.svg', 'docs/assets/documentaries/navier_stokes/frontier.svg', 'docs/assets/documentaries/poincare/plate_extinction.svg', 'docs/assets/documentaries/riemann/euler.svg', 'docs/assets/documentaries/riemann/evidence.svg']
BLOBS = {'docs/assets/documentaries/navier_stokes/field.svg': '93c4b4d5f102217897592f0ff2efb78dbb22243c', 'docs/assets/documentaries/navier_stokes/frontier.svg': 'daff90cadc34999442acd796382917fd92f3c10d', 'docs/assets/documentaries/poincare/plate_extinction.svg': '0c0b57a053b998bdde9f834f588d2a6b77f29e33', 'docs/assets/documentaries/riemann/euler.svg': 'e4d08996162a6bf8a8a78598757fd1653f8c62cd', 'docs/assets/documentaries/riemann/evidence.svg': '17fad1662dc26a7e8b584eceb230606ed9b55c40'}

def sha256(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def renderer():
    spec = importlib.util.spec_from_file_location("batch3_renderer", RENDERER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class Batch3CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads(MANIFEST.read_text())
        cls.s0 = json.loads(STAGE0.read_text())
        cls.by_id = {r["plate_id"]: r for r in cls.m["plates"]}

    def test_exact_scope_and_nonauthority(self):
        self.assertEqual(self.m["state"], "AUTHORIZED_FOR_BATCH3_CANDIDATE_CONSTRUCTION__NO_LIVE_REFERENCE_SWITCH")
        self.assertEqual(self.m["implementation_issue"], 466)
        self.assertEqual(self.m["expected_plate_count"], 5)
        self.assertEqual([r["predecessor_path"] for r in self.m["plates"]], ORDER)
        self.assertEqual(self.s0["batches"]["3"], ORDER)
        self.assertTrue(self.m["authority"]["candidate_construction"])
        self.assertFalse(self.m["authority"]["live_reference_switch"])
        self.assertFalse(self.m["authority"]["batch3_merge_authority"])
        self.assertFalse(self.m["authority"]["visual_is_evidence"])
        for r in self.m["plates"]:
            self.assertEqual(r["predecessor_blob"], BLOBS[r["predecessor_path"]])
            self.assertEqual(r["rollback_blob"], BLOBS[r["predecessor_path"]])
            self.assertEqual(git_blob(ROOT / r["predecessor_path"]), BLOBS[r["predecessor_path"]])
            self.assertEqual(r["independent_review_state"], "pending")
            self.assertFalse(r["live_reference_switched"])
            self.assertFalse(r["live_switch_eligibility"])
            self.assertFalse(r["visual_is_evidence"])

    def test_contracts_pending_and_schema_shaped(self):
        for r in self.m["plates"]:
            c = json.loads((ROOT / r["contract_path"]).read_text())
            self.assertEqual(c["predecessor"], r["predecessor_path"])
            self.assertEqual(c["audit_disposition"], "REDRAW")
            self.assertFalse(c["claim_boundary"]["visual_is_evidence"])
            self.assertTrue(c["renderer"]["reproducible"])
            self.assertEqual(c["derivatives"][0]["path"], r["candidate_path"])
            self.assertEqual(c["derivatives"][0]["digest"], r["candidate_digest"])
            self.assertEqual(c["independent_review"]["status"], "pending")
            self.assertEqual(c["independent_review"]["evidence_refs"], [])

    def test_generator_is_byte_exact(self):
        generated = {str(p.relative_to(ROOT)): c for p, c in renderer().OUTPUTS.items()}
        self.assertEqual(set(generated), {r["candidate_path"] for r in self.m["plates"]})
        for r in self.m["plates"]:
            p = ROOT / r["candidate_path"]
            self.assertEqual(p.read_text(), generated[r["candidate_path"]])
            self.assertEqual(r["candidate_digest"], sha256(p))

    def test_candidates_are_non_live(self):
        docs = "\n".join(p.read_text() for p in sorted((ROOT / "docs/documentaries").glob("*.md")))
        for r in self.m["plates"]:
            self.assertTrue(r["candidate_path"].startswith("governance/visual_pedagogy/review_candidates/"))
            self.assertNotIn(r["candidate_path"], docs)
            self.assertNotIn(Path(r["candidate_path"]).name, docs)

    def test_semantic_guardrails(self):
        checks = {
            "NS-FIELD-PLATE-I": ["not a numerical simulation", "does not prove global smoothness"],
            "NS-FRONTIER-PLATE-IV": ["CONTINUATION CRITERIA", "PARTIAL REGULARITY", "OPEN"],
            "PC-EXTINCTION-PLATE-IV": ["REVERSE BOOKKEEPING", "is not a proof of extinction"],
            "RH-EULER-PLATE-I": ["Re(s) &gt; 1", "critical strip"],
            "RH-EVIDENCE-PLATE-IV": ["FINITE VERIFICATION", "STATUS: OPEN", "universal statement"],
        }
        for plate_id, needles in checks.items():
            text = (ROOT / self.by_id[plate_id]["candidate_path"]).read_text()
            for needle in needles:
                self.assertIn(needle, text)

if __name__ == "__main__":
    unittest.main()
