import hashlib
import importlib.util
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "governance" / "visual_pedagogy" / "batch1_candidate_manifest.json"
AUDIT_PATH = ROOT / "governance" / "documentary_visual_pedagogy_pilot_audit.json"
CONTRACT_DIR = ROOT / "governance" / "visual_pedagogy" / "plates"
CANDIDATE_DIR = ROOT / "governance" / "visual_pedagogy" / "review_candidates" / "union_closed"
GENERATOR_PATH = ROOT / "tools" / "render_visual_pedagogy_batch1_svg_candidates.py"

EXPECTED_PLATES = [
    "UC-GARDEN-PLATE-I",
    "UC-ENTROPY-PLATE-III",
    "UC-LATTICE-PLATE-IV",
    "UC-FREQUENCY-PLATE-II",
    "UC-FRONTIER-PLATE-VI",
    "BSD-CURVE-PLATE-I",
]
EXPECTED_PREDECESSORS = {
    "docs/assets/documentaries/union_closed/plate_garden.svg": "112ef03623df543b4e1f9877b8727f7c0a149c34",
    "docs/assets/documentaries/union_closed/plate_entropy.svg": "e360b218de391458b07c740cffdb4837bcd1be5c",
    "docs/assets/documentaries/union_closed/plate_lattice.svg": "4fc0ee01f5a1cf9553528ace3fedfee927c26cea",
    "docs/assets/documentaries/union_closed/plate_frequency.svg": "dae5dd33339ad1eda3bd70160c868af65a8a0b5c",
    "docs/assets/documentaries/union_closed/plate_frontier.svg": "605dc66522f6b3bc4977c7101c6f038eeea0d6c6",
    "docs/assets/documentaries/bsd/plate_curve.svg": "88b010f956744a4303dfbfd04b9f95062dbdfe04",
}
UC_PLATES = set(EXPECTED_PLATES[:-1])
BSD_DIGEST = "sha256:971106fe6dba55335e707d4cb5c49a6ef32414ccd8d3ea2ffbe64c9e87cca13f"


def git_blob_sha(path):
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def sha256_digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_generator():
    spec = importlib.util.spec_from_file_location("batch1_renderer", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VisualPedagogyBatch1CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.by_id = {record["plate_id"]: record for record in cls.manifest["plates"]}
        cls.generator = load_generator()

    def test_authority_is_candidate_only(self):
        self.assertEqual(
            self.manifest["state"],
            "AUTHORIZED_FOR_BATCH1_CANDIDATE_CONSTRUCTION__NO_LIVE_REFERENCE_SWITCH",
        )
        self.assertTrue(self.manifest["authority"]["candidate_construction"])
        self.assertFalse(self.manifest["authority"]["live_reference_switch"])
        self.assertFalse(self.manifest["authority"]["batch1_merge_authority"])
        self.assertFalse(self.manifest["authority"]["visual_is_evidence"])
        self.assertTrue(self.manifest["candidate_policy"]["separate_live_switch_operation_required"])

    def test_exact_batch1_population_and_order(self):
        self.assertEqual(self.manifest["batch"], 1)
        self.assertEqual(self.manifest["expected_plate_count"], 6)
        self.assertEqual([record["plate_id"] for record in self.manifest["plates"]], EXPECTED_PLATES)
        self.assertEqual(set(self.by_id), set(EXPECTED_PLATES))
        predecessor_paths = [record["predecessor_path"] for record in self.manifest["plates"]]
        self.assertEqual(len(predecessor_paths), len(set(predecessor_paths)))
        self.assertEqual(set(predecessor_paths), set(EXPECTED_PREDECESSORS))

    def test_predecessor_and_rollback_blob_identities_are_exact(self):
        audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
        audit_rows = {}
        for family in audit["families"]:
            for asset in family["assets"]:
                audit_rows[asset["asset"]] = asset
        for record in self.manifest["plates"]:
            path = record["predecessor_path"]
            expected = EXPECTED_PREDECESSORS[path]
            self.assertEqual(record["predecessor_blob"], expected)
            self.assertEqual(record["rollback_blob"], expected)
            self.assertEqual(audit_rows[path]["blob_sha"], expected)
            self.assertEqual(audit_rows[path]["disposition"], "REDRAW")
            self.assertEqual(git_blob_sha(ROOT / path), expected)

    def test_candidates_are_non_live_and_distinct_from_predecessors(self):
        for record in self.manifest["plates"]:
            self.assertNotEqual(record["candidate_path"], record["predecessor_path"])
            self.assertFalse(record["live_reference_switched"])
            self.assertFalse(record["live_switch_eligibility"])
            self.assertFalse(record["visual_is_evidence"])
        docs_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "docs" / "documentaries").glob("*.md"))
        )
        for record in self.manifest["plates"]:
            self.assertNotIn(record["candidate_path"], docs_text)
            self.assertNotIn(Path(record["candidate_path"]).name, docs_text)

    def test_union_closed_candidates_match_deterministic_generator_byte_for_byte(self):
        expected_files = set(self.generator.RENDERERS)
        self.assertEqual(
            expected_files,
            {
                "plate_garden_successor.svg",
                "plate_entropy_successor.svg",
                "plate_lattice_successor.svg",
                "plate_frequency_successor.svg",
                "plate_frontier_successor.svg",
            },
        )
        for name, renderer in self.generator.RENDERERS.items():
            committed = (CANDIDATE_DIR / name).read_text(encoding="utf-8")
            self.assertEqual(committed, renderer())
            plate_record = next(
                record for record in self.manifest["plates"]
                if record["candidate_path"].endswith("/" + name)
            )
            self.assertEqual(plate_record["candidate_digest"], sha256_digest(CANDIDATE_DIR / name))

    def test_exact_family_is_union_closed_and_frequency_ledger_is_correct(self):
        family = tuple(self.generator.FAMILY)
        self.assertEqual(len(family), 6)
        for left in family:
            for right in family:
                self.assertIn(left | right, family)
        frequencies = self.generator.frequencies()
        self.assertEqual(frequencies, {"a": 4, "b": 3, "c": 2})
        self.assertEqual(sum(frequencies.values()), 9)
        self.assertEqual(sum(map(len, family)), 9)
        self.assertEqual(self.manifest["exact_example"]["half_threshold"], 3)

    def test_join_irreducibles_and_exact_joins(self):
        family = tuple(self.generator.FAMILY)
        irreducibles = []
        for candidate in family:
            if not candidate:
                continue
            reducible = any(
                left < candidate and right < candidate and (left | right) == candidate
                for left in family for right in family
            )
            if not reducible:
                irreducibles.append(candidate)
        self.assertEqual(
            set(irreducibles),
            {frozenset({"a"}), frozenset({"b"}), frozenset({"a", "c"})},
        )
        self.assertEqual(frozenset({"a"}) | frozenset({"b"}), frozenset({"a", "b"}))
        self.assertEqual(frozenset({"b"}) | frozenset({"a", "c"}), frozenset({"a", "b", "c"}))

    def test_entropy_example_marginals_are_exact(self):
        frequencies = self.generator.frequencies()
        p = {x: Fraction(frequencies[x], len(self.generator.FAMILY)) for x in self.generator.ELEMENTS}
        self.assertEqual(p, {"a": Fraction(2, 3), "b": Fraction(1, 2), "c": Fraction(1, 3)})
        q = {x: 1 - (1 - p[x]) ** 2 for x in p}
        self.assertEqual(q, {"a": Fraction(8, 9), "b": Fraction(3, 4), "c": Fraction(5, 9)})

    def test_union_closed_contracts_bind_semantics_accessibility_and_pending_review(self):
        for plate_id in UC_PLATES:
            record = self.by_id[plate_id]
            contract = json.loads((ROOT / record["contract_path"]).read_text(encoding="utf-8"))
            self.assertEqual(contract["plate_id"], plate_id)
            self.assertEqual(contract["audit_disposition"], "REDRAW")
            self.assertEqual(contract["predecessor"], record["predecessor_path"])
            self.assertFalse(contract["claim_boundary"]["visual_is_evidence"])
            self.assertEqual(contract["independent_review"], {"status": "pending", "evidence_refs": []})
            self.assertTrue(contract["renderer"]["reproducible"])
            self.assertEqual(contract["renderer"]["mode"], "programmatic-vector")
            self.assertTrue(contract["accessibility"]["alt_text"])
            self.assertTrue(contract["accessibility"]["long_description"])
            derivative = contract["derivatives"][0]
            self.assertEqual(derivative["path"], record["candidate_path"])
            self.assertEqual(derivative["digest"], record["candidate_digest"])

    def test_bsd_pilot_candidate_is_reused_without_erasing_review_history(self):
        record = self.by_id["BSD-CURVE-PLATE-I"]
        self.assertEqual(record["candidate_origin"], "protected_pilot_reuse")
        self.assertEqual(record["candidate_digest"], BSD_DIGEST)
        self.assertEqual(record["independent_review_state"], "inherited_pilot_reviewed")
        self.assertTrue(record["batch_confirmation_required"])
        contract = json.loads((ROOT / record["contract_path"]).read_text(encoding="utf-8"))
        self.assertEqual(contract["independent_review"]["status"], "reviewed")
        self.assertFalse(contract["claim_boundary"]["visual_is_evidence"])
        derivatives = {item["path"]: item for item in contract["derivatives"]}
        self.assertIn(record["candidate_path"], derivatives)
        self.assertEqual(derivatives[record["candidate_path"]]["digest"], BSD_DIGEST)

    def test_bsd_exact_arithmetic_replays(self):
        x = Fraction(25, 4)
        y = Fraction(75, 8)
        self.assertEqual(y * y, x * x * x - 25 * x)
        a = Fraction(3, 2)
        b = Fraction(20, 3)
        c = Fraction(41, 6)
        self.assertEqual(a * a + b * b, c * c)
        self.assertEqual(Fraction(1, 2) * a * b, 5)


if __name__ == "__main__":
    unittest.main()
