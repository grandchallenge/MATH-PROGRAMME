from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / "campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK"
SOURCE = ROOT / "docs/documentaries/sources/the_element_in_half_the_worlds.tex"
LOCK = WP / "artifacts/UC-DOC-WP00_SOURCE_LOCK.json"
MANIFEST = ROOT / "docs/documentaries/ARTIFACT_MANIFEST.json"


class UnionClosedDocumentarySourceLockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_work_package_bundle_is_complete(self) -> None:
        required = [
            "00_README.md", "01_RESULT_STATUS.json", "02_LAY_COMPANION.md",
            "03_OBJECT_AND_OBSTRUCTION.md", "04_PROBLEM_AND_STATUS_AUDIT.md",
            "05_THEOREM_SPINE.md", "06_DEPENDENCY_DAG.json",
            "07_PROOFS_AND_COMPUTATIONS.md", "08_FAILURE_AND_NEGATIVE_RESULTS.md",
            "09_PROOF_DEBT.json", "10_CLAIM_LEDGER.yaml", "11_CERT_HANDOFF.md",
            "12_NEXT_EXECUTABLE_STEP.md", "artifacts/UC-DOC-WP00_SOURCE_LOCK.json",
        ]
        for relative in required:
            self.assertTrue((WP / relative).is_file(), relative)

    def test_release_identities_match_source_record(self) -> None:
        for key, label in (
            ("latex_source", "Complete LaTeX source"),
            ("rendered_pdf", "Rendered PDF"),
            ("authoritative_source_bundle", "Authoritative complete illustrated source bundle"),
        ):
            artifact = self.lock["release_artifacts"][key]
            self.assertIn(f"% {label} bytes: {artifact['bytes']}", self.source)
            self.assertIn(f"% {label} SHA-256: {artifact['sha256']}", self.source)
            self.assertRegex(artifact["sha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(artifact["bytes"], 0)
            self.assertEqual("metadata_only", artifact["availability"])

    def test_open_claim_boundary_is_explicit(self) -> None:
        readme = (WP / "00_README.md").read_text(encoding="utf-8")
        audit = (WP / "04_PROBLEM_AND_STATUS_AUDIT.md").read_text(encoding="utf-8")
        boundary = self.lock["claim_boundary"]
        self.assertIn("Frankl's conjecture open", readme)
        self.assertIn("Status: `OPEN`", audit)
        self.assertIn("does not prove Frankl's conjecture", boundary)
        for forbidden in ("Frankl's conjecture is proved", "solves Frankl", "new proof of Frankl"):
            self.assertNotIn(forbidden, readme + audit + self.source)

    def test_manifest_admission_is_deferred_fail_closed(self) -> None:
        slugs = {volume["slug"] for volume in self.manifest["volumes"]}
        editions = {volume["edition_record"] for volume in self.manifest["volumes"]}
        self.assertNotIn("union_closed", slugs)
        self.assertNotIn("union_closed.edition.json", editions)
        self.assertFalse((ROOT / "docs/documentaries/union_closed.edition.json").exists())
        self.assertFalse((ROOT / "docs/documentaries/union_closed.md").exists())
        self.assertEqual("deferred_to_UC-DOC-WP01", self.lock["manifest_admission"]["state"])
        self.assertFalse(self.lock["manifest_admission"]["manifest_member"])

    def test_plate_authority_and_inventory(self) -> None:
        plates = self.lock["plate_inventory"]
        self.assertEqual(7, len(plates))
        self.assertEqual(len(plates), len({plate["id"] for plate in plates}))
        for plate in plates:
            self.assertEqual("pedagogical_orientation_only", plate["authority"])

    def test_source_record_fields(self) -> None:
        expected = {
            "title": "The Element in Half the Worlds",
            "subject": "Frankl's Union-Closed Sets Conjecture",
            "pages": "48",
            "date": "2026-07-27",
        }
        for key, value in expected.items():
            label = {"title": "Title", "subject": "Subject", "pages": "Pages", "date": "Source-lock date"}[key]
            self.assertRegex(self.source, rf"(?m)^% {re.escape(label)}: {re.escape(value)}$")


if __name__ == "__main__":
    unittest.main()
