import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "governance" / "visual_pedagogy" / "batch2_candidate_manifest.json"
STAGE0_PATH = ROOT / "governance" / "visual_pedagogy" / "propagation_manifest.json"
GENERATOR_PATH = ROOT / "tools" / "render_visual_pedagogy_batch2_svg_candidates.py"

EXPECTED_ORDER = [
    "BSD-BRIDGE-PLATE-III",
    "BSD-HARMONY-PLATE-II",
    "BSD-FRONTIER-PLATE-V",
    "BSD-OVERTURE-PLATE-IV",
    "HODGE-CYCLES-PLATE-III",
    "HODGE-DIAMOND-PLATE-II",
]
EXPECTED_PREDECESSORS = [
    "docs/assets/documentaries/bsd/plate_bridge.svg",
    "docs/assets/documentaries/bsd/plate_harmony.svg",
    "docs/assets/documentaries/bsd/plate_frontier.svg",
    "docs/assets/documentaries/bsd/plate_overture.svg",
    "docs/assets/documentaries/hodge/cycles.svg",
    "docs/assets/documentaries/hodge/diamond.svg",
]
EXPECTED_BLOBS = {
    "docs/assets/documentaries/bsd/plate_bridge.svg": "cf46ce8633c3d964ed21ced776494375c1c0cbff",
    "docs/assets/documentaries/bsd/plate_harmony.svg": "845fa10b8b13ec99a8d61dd6fb51543c113f43b3",
    "docs/assets/documentaries/bsd/plate_frontier.svg": "457c5de53b36d2de3cac0ab534e2545949084f57",
    "docs/assets/documentaries/bsd/plate_overture.svg": "c151081594dcf3ae04f15863f85b8c3a32aa7440",
    "docs/assets/documentaries/hodge/cycles.svg": "a89e4851b30ec7ac858da9f999328abed168eb90",
    "docs/assets/documentaries/hodge/diamond.svg": "eb928bbf9a6d31e14b5eaa183805023d48f16ac2",
}


def load_generator():
    spec = importlib.util.spec_from_file_location("batch2_renderer", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def git_blob_sha(path):
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def sha256_digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


class VisualPedagogyBatch2CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.stage0 = json.loads(STAGE0_PATH.read_text(encoding="utf-8"))
        cls.generator = load_generator()
        cls.by_id = {record["plate_id"]: record for record in cls.manifest["plates"]}

    def test_authority_is_candidate_only(self):
        self.assertEqual(
            self.manifest["state"],
            "AUTHORIZED_FOR_BATCH2_CANDIDATE_CONSTRUCTION__NO_LIVE_REFERENCE_SWITCH",
        )
        self.assertTrue(self.manifest["authority"]["candidate_construction"])
        self.assertFalse(self.manifest["authority"]["live_reference_switch"])
        self.assertFalse(self.manifest["authority"]["batch2_merge_authority"])
        self.assertFalse(self.manifest["authority"]["visual_is_evidence"])
        self.assertTrue(self.manifest["candidate_policy"]["separate_live_switch_operation_required"])

    def test_exact_stage0_batch2_population_and_order(self):
        self.assertEqual(self.manifest["batch"], 2)
        self.assertEqual(self.manifest["expected_plate_count"], 6)
        self.assertEqual([r["plate_id"] for r in self.manifest["plates"]], EXPECTED_ORDER)
        predecessors = [r["predecessor_path"] for r in self.manifest["plates"]]
        self.assertEqual(predecessors, EXPECTED_PREDECESSORS)
        self.assertEqual(self.stage0["batches"]["2"], EXPECTED_PREDECESSORS)

    def test_predecessor_and_rollback_blobs_are_exact(self):
        for record in self.manifest["plates"]:
            path = record["predecessor_path"]
            expected = EXPECTED_BLOBS[path]
            self.assertEqual(record["predecessor_blob"], expected)
            self.assertEqual(record["rollback_blob"], expected)
            self.assertEqual(git_blob_sha(ROOT / path), expected)
            self.assertFalse(record["live_reference_switched"])
            self.assertFalse(record["live_switch_eligibility"])
            self.assertFalse(record["visual_is_evidence"])

    def test_candidates_match_generator_byte_for_byte_and_digest(self):
        generated = {
            str(path.relative_to(ROOT)): content
            for path, content in self.generator.OUTPUTS.items()
        }
        self.assertEqual(set(generated), {r["candidate_path"] for r in self.manifest["plates"]})
        for record in self.manifest["plates"]:
            path = ROOT / record["candidate_path"]
            self.assertEqual(path.read_text(encoding="utf-8"), generated[record["candidate_path"]])
            self.assertEqual(record["candidate_digest"], sha256_digest(path))

    def test_candidates_are_non_live_and_not_referenced_by_documentary_pages(self):
        docs_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "docs" / "documentaries").glob("*.md"))
        )
        for record in self.manifest["plates"]:
            self.assertTrue(record["candidate_path"].startswith("governance/visual_pedagogy/review_candidates/"))
            self.assertNotEqual(record["candidate_path"], record["predecessor_path"])
            self.assertNotIn(record["candidate_path"], docs_text)
            self.assertNotIn(Path(record["candidate_path"]).name, docs_text)

    def test_contracts_bind_pending_review_semantics_accessibility_and_nonauthority(self):
        for record in self.manifest["plates"]:
            contract = json.loads((ROOT / record["contract_path"]).read_text(encoding="utf-8"))
            self.assertEqual(contract["plate_id"], record["plate_id"])
            self.assertEqual(contract["audit_disposition"], "REDRAW")
            self.assertEqual(contract["predecessor"], record["predecessor_path"])
            self.assertEqual(contract["representation_class"], "schematic")
            self.assertFalse(contract["claim_boundary"]["visual_is_evidence"])
            self.assertEqual(contract["independent_review"]["status"], "pending")
            self.assertEqual(contract["independent_review"]["evidence_refs"], [])
            self.assertTrue(contract["renderer"]["reproducible"])
            self.assertEqual(contract["renderer"]["mode"], "programmatic-vector")
            self.assertTrue(contract["accessibility"]["alt_text"])
            self.assertTrue(contract["accessibility"]["long_description"])
            derivative = contract["derivatives"][0]
            self.assertEqual(derivative["path"], record["candidate_path"])
            self.assertEqual(derivative["digest"], record["candidate_digest"])

    def test_garden_rendering_lessons_are_enforced(self):
        forbidden_math_glyphs = {"∅", "∪", "ℚ", "ℤ", "⊕", "∏", "Ω"}
        for record in self.manifest["plates"]:
            text = (ROOT / record["candidate_path"]).read_text(encoding="utf-8")
            self.assertFalse(forbidden_math_glyphs.intersection(text))
            self.assertIn("visual_is_evidence: false", text)

        bridge = (ROOT / self.by_id["BSD-BRIDGE-PLATE-III"]["candidate_path"]).read_text(encoding="utf-8")
        self.assertIn("no single local factor determines", bridge)
        self.assertIn("BSD conjectures r_alg = r_an", bridge)

        harmony = (ROOT / self.by_id["BSD-HARMONY-PLATE-II"]["candidate_path"]).read_text(encoding="utf-8")
        self.assertIn("r_alg ?= r_an", harmony)
        self.assertIn("conjectural bridge", harmony)

        frontier = (ROOT / self.by_id["BSD-FRONTIER-PLATE-V"]["candidate_path"]).read_text(encoding="utf-8")
        self.assertGreaterEqual(frontier.count("ESTABLISHED"), 3)
        self.assertGreaterEqual(frontier.count(">OPEN<"), 3)
        self.assertIn("Analytic rank 0 or 1", frontier)

        overture = (ROOT / self.by_id["BSD-OVERTURE-PLATE-IV"]["candidate_path"]).read_text(encoding="utf-8")
        self.assertIn("Three obligations remain logically distinct", overture)
        self.assertIn("finiteness of Sha", overture)

        cycles = (ROOT / self.by_id["HODGE-CYCLES-PLATE-III"]["candidate_path"]).read_text(encoding="utf-8")
        self.assertIn("open general converse", cycles)
        self.assertIn("integral analogue", cycles)
        self.assertIn("rational coefficients are structural", cycles)

        diamond = (ROOT / self.by_id["HODGE-DIAMOND-PLATE-II"]["candidate_path"]).read_text(encoding="utf-8")
        self.assertIn("does not invent Hodge numbers", diamond)
        self.assertIn("necessary, but the general converse", diamond)


if __name__ == "__main__":
    unittest.main()
