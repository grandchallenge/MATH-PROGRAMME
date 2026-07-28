from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / "campaigns/union_closed/UC_DOC_WP00_DOCUMENTARY_SOURCE_LOCK"
SOURCE = WP / "artifacts/the_element_in_half_the_worlds.tex"
LOCK = WP / "artifacts/UC-DOC-WP00_SOURCE_LOCK.json"
RESULT = WP / "01_RESULT_STATUS.json"
CLAIM_LEDGER = WP / "10_CLAIM_LEDGER.yaml"
MANIFEST = ROOT / "docs/documentaries/ARTIFACT_MANIFEST.json"
CANDIDATES = ROOT / "docs/documentaries/DOCUMENTARY_CANDIDATES.json"
REVIEW = ROOT / "reviews/union_closed/UC-DOC-WP00.agent_review.yaml"


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
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
        cls.claim_ledger = yaml.safe_load(CLAIM_LEDGER.read_text(encoding="utf-8"))

    def test_work_package_bundle_is_complete(self) -> None:
        required = [
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
        for relative in required:
            self.assertTrue((WP / relative).is_file(), relative)

    def test_release_identities_agree_across_governing_records(self) -> None:
        readme = (WP / "00_README.md").read_text(encoding="utf-8")
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
            self.assertIn(f"% {label} bytes: {artifact['bytes']}", self.source)
            self.assertIn(f"% {label} SHA-256: {artifact['sha256']}", self.source)
            self.assertIn(f"{artifact['bytes']:,}", readme)
            self.assertIn(artifact["sha256"], readme)
            self.assertRegex(artifact["sha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(artifact["bytes"], 0)
            self.assertEqual("metadata_only", artifact["availability"])
            self.assertIsNone(artifact["release_locator"])

    def test_open_claim_boundary_is_explicit(self) -> None:
        readme = (WP / "00_README.md").read_text(encoding="utf-8")
        audit = (WP / "04_PROBLEM_AND_STATUS_AUDIT.md").read_text(encoding="utf-8")
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

    def test_candidate_registry_is_schema_valid_and_authoritative(self) -> None:
        self.assertEqual(
            [],
            validation_errors(
                self.candidates,
                ROOT / "schemas/documentary_candidate_registry.schema.json",
            ),
        )
        candidate = next(
            item for item in self.candidates["candidates"] if item["slug"] == "union_closed"
        )
        self.assertEqual(self.lock["source_record"], candidate["source_record"])
        self.assertEqual(self.lock["release_artifacts"], candidate["release_artifacts"])
        self.assertEqual("open", candidate["claim_status"])
        self.assertEqual("open_conjecture", candidate["problem_class"])
        self.assertFalse(candidate["manifest_member"])
        self.assertEqual(
            "metadata_public_source_record_repository_only",
            candidate["public_copy_policy"],
        )

    def test_manifest_admission_is_deferred_fail_closed(self) -> None:
        slugs = {volume["slug"] for volume in self.manifest["volumes"]}
        editions = {volume["edition_record"] for volume in self.manifest["volumes"]}
        self.assertNotIn("union_closed", slugs)
        self.assertNotIn("union_closed.edition.json", editions)
        self.assertFalse((ROOT / "docs/documentaries/union_closed.edition.json").exists())
        self.assertFalse((ROOT / "docs/documentaries/union_closed.md").exists())
        self.assertEqual(
            "source_locked_web_admission_pending",
            self.lock["manifest_admission"]["state"],
        )
        self.assertTrue(self.lock["manifest_admission"]["candidate_member"])
        self.assertFalse(self.lock["manifest_admission"]["manifest_member"])

    def test_pre_admission_source_record_is_not_publicly_copied(self) -> None:
        self.assertTrue(SOURCE.is_file())
        self.assertFalse(
            (ROOT / "docs/documentaries/sources/the_element_in_half_the_worlds.tex").exists()
        )
        self.assertIn(
            "% Public copy policy: repository_only_until_manifest_admission",
            self.source,
        )

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

    def test_agent_review_is_schema_valid_and_promotable(self) -> None:
        review = yaml.safe_load(REVIEW.read_text(encoding="utf-8"))
        self.assertEqual(
            [],
            validation_errors(review, ROOT / "schemas/agent_review.schema.json"),
        )
        self.assertTrue(review["promotion"]["ready_for_next_stage"])
        self.assertEqual([], review["promotion"]["blockers"])
        for role in (
            "Axiomatist",
            "Cartographer",
            "Verifier",
            "Adversary",
            "Formalist",
            "Amanuensis",
            "Referee",
        ):
            self.assertEqual("reviewed", review["council_review"][role]["status"])


if __name__ == "__main__":
    unittest.main()
