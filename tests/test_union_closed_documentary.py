from __future__ import annotations

import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/documentaries"


class UnionClosedDocumentaryAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(
            (DOCS / "ARTIFACT_MANIFEST.json").read_text(encoding="utf-8")
        )
        cls.volume = next(
            volume for volume in cls.manifest["volumes"] if volume["slug"] == "union_closed"
        )
        cls.edition = json.loads(
            (DOCS / cls.volume["edition_record"]).read_text(encoding="utf-8")
        )
        cls.page = (DOCS / cls.volume["web_page"]).read_text(encoding="utf-8")

    def test_atomic_manifest_admission(self) -> None:
        self.assertEqual(8, len(self.manifest["volumes"]))
        self.assertEqual("UC", self.volume["domain_id"])
        self.assertEqual("UC", self.volume["campaign_id"])
        self.assertEqual("campaign_documentary", self.volume["scope_relation"])
        self.assertEqual("full", self.volume["documentary_tier"])
        self.assertEqual("open", self.volume["claim_status"])
        self.assertEqual("open_conjecture", self.volume["problem_class"])
        self.assertEqual("Open conjecture", self.volume["display_status"])
        self.assertTrue((DOCS / self.volume["source_record"]).is_file())
        self.assertTrue((DOCS / self.volume["edition_record"]).is_file())
        self.assertTrue((DOCS / self.volume["web_page"]).is_file())

    def test_edition_schema_and_depth(self) -> None:
        schema = json.loads(
            (DOCS / "documentary_web.schema.json").read_text(encoding="utf-8")
        )
        errors = list(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(
                self.edition
            )
        )
        self.assertEqual([], errors)
        self.assertGreaterEqual(len(self.edition["plates"]), 6)
        self.assertGreaterEqual(len(self.edition["chapters"]), 6)
        self.assertGreaterEqual(len(self.edition["appendices"]), 5)
        self.assertIn("Open conjecture", self.edition["status"])

    def test_non_millennium_open_status_is_exact(self) -> None:
        self.assertGreaterEqual(self.page.count("Open conjecture"), 2)
        self.assertNotIn("Open Millennium Prize Problem", self.page)
        self.assertNotIn("Open Millennium Prize Problem", self.edition["status"])
        self.assertIn("Frankl’s conjecture remains open", self.page)

    def test_claim_surfaces_and_boundary(self) -> None:
        for marker in (
            'class="definition-box"',
            'class="theorem-box"',
            'class="conjecture-box"',
            'class="imported-box"',
            'class="warning-box"',
        ):
            self.assertIn(marker, self.page)
        self.assertIn(self.edition["claim_boundary"], self.page)
        for forbidden in (
            "proves Frankl",
            "solves Frankl",
            "Frankl's conjecture is proved",
        ):
            self.assertNotIn(forbidden, self.page)

    def test_native_plates_are_accessible_and_pedagogical(self) -> None:
        seen = set()
        ns = {"svg": "http://www.w3.org/2000/svg"}
        for plate in self.edition["plates"]:
            self.assertEqual("pedagogical_orientation_only", plate["authority"])
            self.assertGreaterEqual(len(plate["alt"]), 20)
            self.assertNotIn(plate["asset"], seen)
            seen.add(plate["asset"])
            path = ROOT / "docs" / plate["asset"]
            self.assertTrue(path.is_file(), path)
            root = ET.parse(path).getroot()
            self.assertIsNotNone(root.find("svg:title", ns))
            self.assertIsNotNone(root.find("svg:desc", ns))
            self.assertIn(plate["asset"], self.page)

    def test_release_identities_are_preserved(self) -> None:
        expected = {
            "rendered_pdf": (
                3343773,
                "6ea03bef444f19ae8013e80c76a5112fda9c6b740d61387c2bfeea5921ac71dc",
            ),
            "latex_source": (
                50548,
                "e889079fc77163e57b0c239e8f25ae29a3ded640b32120f65d1f3708c05dfdde",
            ),
            "authoritative_source_bundle": (
                3100936,
                "3a1fcf16dee92c6bbf5fd8285702e31c828aa6d1666e5605e8981346f4bd2daf",
            ),
        }
        for key, (size, digest) in expected.items():
            self.assertEqual(size, self.volume[key]["bytes"])
            self.assertEqual(digest, self.volume[key]["sha256"])
            self.assertEqual("metadata_only", self.volume[key]["availability"])
            self.assertIsNone(self.volume[key]["release_locator"])
            self.assertIn(f"{size:,}", self.page)
            self.assertIn(digest, self.page)

    def test_review_record_conforms(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/agent_review.schema.json").read_text(encoding="utf-8")
        )
        review = yaml.safe_load(
            (ROOT / "reviews/union_closed/UC-DOC-WP01.agent_review.yaml").read_text(
                encoding="utf-8"
            )
        )
        errors = list(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(
                review
            )
        )
        self.assertEqual([], errors)
        self.assertTrue(review["promotion"]["ready_for_next_stage"])
        self.assertEqual([], review["promotion"]["blockers"])


if __name__ == "__main__":
    unittest.main()
