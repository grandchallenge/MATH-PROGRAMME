from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
WP00 = ROOT / "campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK"
WP01 = ROOT / "campaigns/union_closed/UC_DOC_WP01_WEB_ADMISSION"
SOURCE = ROOT / "docs/documentaries/sources/the_element_in_half_the_worlds.tex"
LOCK = WP00 / "artifacts/UC-DOC-WP00_SOURCE_LOCK.json"
RESULT = WP00 / "01_RESULT_STATUS.json"
CLAIM_LEDGER = WP00 / "10_CLAIM_LEDGER.yaml"
ADMISSION = WP01 / "artifacts/UC-DOC-WP01_ADMISSION.json"
MANIFEST = ROOT / "docs/documentaries/ARTIFACT_MANIFEST.json"
CANDIDATES = ROOT / "docs/documentaries/DOCUMENTARY_CANDIDATES.json"
REVIEW_SCHEMA = ROOT / "schemas/agent_review.schema.json"


def validation_errors(instance: object, schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


class UnionClosedDocumentarySourceLockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        cls.result = json.loads(RESULT.read_text(encoding="utf-8"))
        cls.admission = json.loads(ADMISSION.read_text(encoding="utf-8"))
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
        cls.claim_ledger = yaml.safe_load(CLAIM_LEDGER.read_text(encoding="utf-8"))
        cls.volume = next(
            volume for volume in cls.manifest["volumes"] if volume["slug"] == "union_closed"
        )

    def test_work_package_bundles_are_complete(self) -> None:
        wp00_required = [
            "00_README.md",
            "01_RESULT_STATUS.json",
            "02_LAY_COMPANION.md",
            "03_OBJECT_AND_OBSTRUCTION.md",
            "04_PROBLEM_AND_STATUS_AUDIT.md",
            "05_THEOREM_SPINE.md",
            "06_DEPENDENCY_DAG.json",
            "07_PROOFS_AND_COMPUTATIONS.md",
            "08_FAILURE_AND_NEGATIVE_RESULTS.md",
            "09_PROOF_DEBT.json",
            "10_CLAIM_LEDGER.yaml",
            "11_CERT_HANDOFF.md",
            "12_NEXT_EXECUTABLE_STEP.md",
            "artifacts/UC-DOC-WP00_SOURCE_LOCK.json",
            "artifacts/the_element_in_half_the_worlds.tex",
        ]
        for relative in wp00_required:
            self.assertTrue((WP00 / relative).is_file(), relative)
        for relative in (
            "00_README.md",
            "01_RESULT_STATUS.json",
            "artifacts/UC-DOC-WP01_ADMISSION.json",
        ):
            self.assertTrue((WP01 / relative).is_file(), relative)

    def test_release_identities_agree_across_governing_records(self) -> None:
        for key, label in (
            ("latex_source", "Complete LaTeX source"),
            ("rendered_pdf", "Rendered PDF"),
            (
                "authoritative_source_bundle",
                "Authoritative complete illustrated source bundle",
            ),
        ):
            artifact = self.lock["release_artifacts"][key]
            self.assertEqual(artifact, self.result["release_artifacts"][key])
            self.assertEqual(artifact, self.admission["release_artifacts"][key])
            self.assertEqual(artifact, self.volume[key])
            self.assertIn(f"% {label} bytes: {artifact['bytes']}", self.source)
            self.assertIn(f"% {label} SHA-256: {artifact['sha256']}", self.source)
            self.assertRegex(artifact["sha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(artifact["bytes"], 0)
            self.assertEqual("metadata_only", artifact["availability"])
            self.assertIsNone(artifact["release_locator"])

    def test_open_claim_boundary_is_explicit(self) -> None:
        readme = (WP00 / "00_README.md").read_text(encoding="utf-8")
        audit = (WP00 / "04_PROBLEM_AND_STATUS_AUDIT.md").read_text(encoding="utf-8")
        boundary = self.lock["claim_boundary"]
        self.assertEqual("open", self.lock["claim_status"])
        self.assertEqual("open_conjecture", self.lock["problem_class"])
        self.assertEqual("Open conjecture", self.lock["display_status"])
        self.assertIn("Frankl's conjecture open", readme)
        self.assertIn("Status: `OPEN`", audit)
        self.assertIn("does not prove Frankl's conjecture", boundary)
        for forbidden in (
            "Frankl's conjecture is proved",
            "solves Frankl",
            "new proof of Frankl",
        ):
            self.assertNotIn(forbidden, readme + audit + self.source)

    def test_claim_ledger_is_canonical_and_schema_valid(self) -> None:
        self.assertEqual("1.1.0", self.claim_ledger["schema_version"])
        self.assertEqual("canonical_claim_ledger", self.claim_ledger["ledger_contract"])
        self.assertEqual("UC-DOC-WP00-CLAIMS", self.claim_ledger["ledger_id"])
        self.assertEqual(
            [],
            validation_errors(
                self.claim_ledger,
                ROOT / "schemas/claim_ledger.schema.json",
            ),
        )
        claim_ids = [claim["claim_id"] for claim in self.claim_ledger["claims"]]
        self.assertEqual(len(claim_ids), len(set(claim_ids)))
        self.assertIn("UC-DOC-C001", claim_ids)
        self.assertIn("UC-DOC-C010", claim_ids)

    def test_atomic_admission_is_complete_and_candidate_is_removed(self) -> None:
        self.assertEqual("deferred_to_UC-DOC-WP01", self.lock["manifest_admission"]["state"])
        self.assertFalse(self.lock["manifest_admission"]["manifest_member"])
        self.assertEqual([], self.candidates["candidates"])
        self.assertEqual("admitted_by_UC-DOC-WP01", self.admission["state"])
        self.assertEqual("full", self.volume["documentary_tier"])
        self.assertEqual("open", self.volume["claim_status"])
        self.assertEqual("open_conjecture", self.volume["problem_class"])
        self.assertEqual("Open conjecture", self.volume["display_status"])
        self.assertEqual("union_closed.edition.json", self.volume["edition_record"])
        self.assertEqual("union_closed.md", self.volume["web_page"])
        self.assertEqual(
            "campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK/"
            "artifacts/UC-DOC-WP00_SOURCE_LOCK.json",
            self.volume["source_lock"],
        )
        self.assertTrue((ROOT / "docs/documentaries/union_closed.edition.json").is_file())
        self.assertTrue((ROOT / "docs/documentaries/union_closed.md").is_file())
        self.assertIn("% Manifest membership: admitted by UC-DOC-WP01", self.source)

    def test_plate_authority_and_inventory(self) -> None:
        plates = self.lock["plate_inventory"]
        self.assertEqual(7, len(plates))
        self.assertEqual(len(plates), len({plate["id"] for plate in plates}))
        for plate in plates:
            self.assertEqual("pedagogical_orientation_only", plate["authority"])
            self.assertTrue(
                (ROOT / "docs/assets/documentaries/union_closed" / plate["file"]).is_file()
            )

    def test_source_record_fields(self) -> None:
        expected = {
            "title": "The Element in Half the Worlds",
            "subject": "Frankl's Union-Closed Sets Conjecture",
            "pages": "48",
            "date": "2026-07-27",
        }
        labels = {
            "title": "Title",
            "subject": "Subject",
            "pages": "Pages",
            "date": "Source-lock date",
        }
        for key, value in expected.items():
            self.assertRegex(
                self.source,
                rf"(?m)^% {re.escape(labels[key])}: {re.escape(value)}$",
            )

    def test_agent_reviews_are_schema_valid_and_promotable(self) -> None:
        for relative in (
            "reviews/union_closed/UC-DOC-WP00.agent_review.yaml",
            "reviews/union_closed/UC-DOC-WP01.agent_review.yaml",
        ):
            review = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
            self.assertEqual([], validation_errors(review, REVIEW_SCHEMA), relative)
            self.assertTrue(review["promotion"]["ready_for_next_stage"], relative)
            self.assertEqual([], review["promotion"]["blockers"], relative)
            for role in (
                "Axiomatist",
                "Cartographer",
                "Verifier",
                "Adversary",
                "Formalist",
                "Amanuensis",
                "Referee",
            ):
                self.assertEqual(
                    "reviewed", review["council_review"][role]["status"], relative
                )


if __name__ == "__main__":
    unittest.main()
