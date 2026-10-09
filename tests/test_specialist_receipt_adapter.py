from __future__ import annotations

import base64
import copy
import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ci"))
from agent_routine_review import (  # noqa: E402
    RoutineReviewError, exact_specialist_disposition,
    specialist_domain_for_file_manifest, review_body,
)
from specialist_receipt_adapter import (  # noqa: E402
    ReceiptError, material_fingerprint, protected_specialist_receipt,
)


class ProtectedSpecialistReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.head = "a" * 40
        self.source = "b" * 40
        self.receipt_blob = "c" * 40
        self.proof_blob = "d" * 40
        self.files = [{"filename": "fixtures/formal/CM4.lean",
                       "status": "modified", "sha": "e" * 40}]
        self.receipt = {
            "schema_version": "1.0.0",
            "record_type": "GCL_PROTECTED_SPECIALIST_ADMISSION_EVIDENCE",
            "authority_domain": "MATHEMATICAL",
            "source_repository": "grandchallenge/MATHCERT",
            "subject": {"repository": "grandchallenge/MATH-PROGRAMME",
                        "head_sha": self.head,
                        "material_fingerprint": material_fingerprint(self.files)},
            "verdict": "ADMISSIBLE_FOR_PROTECTED_ADMISSION",
            "protected_evidence": {"path": "certificates/CM4-review.json",
                                   "blob_sha": self.proof_blob},
            "review_scope": "Exact source-bound CM4 theorem evidence, no new claims",
        }
        self.proof = {
            "record_type": "GCL_DOMAIN_INDEPENDENT_REVIEW_V1",
            "authority_domain": "MATHEMATICAL",
            "subject_repository": "grandchallenge/MATH-PROGRAMME",
            "subject_sha": self.head,
            "material_fingerprint": material_fingerprint(self.files),
            "disposition": "INDEPENDENT_REVIEW_ACCEPTED",
            "reviewer_identity": "gcl-independent-mathematical-referee",
            "review_independence": "INDEPENDENT_NON_AUTHOR",
            "review_scope": self.receipt["review_scope"],
        }

    def api(self, path: str):
        if path == "/repos/grandchallenge/MATHCERT/git/ref/heads/main":
            return {"object": {"sha": self.source}}
        if path.startswith("/repos/grandchallenge/MATHCERT/contents/"):
            content = self.receipt if "material_admission_receipts" in path else self.proof
            sha = self.receipt_blob if "material_admission_receipts" in path else self.proof_blob
            return {"type": "file", "encoding": "base64", "sha": sha,
                    "content": base64.b64encode(json.dumps(content).encode()).decode()}
        raise AssertionError("unadmitted API path " + path)

    def verify(self, fetch=None):
        return protected_specialist_receipt(
            head=self.head, files=self.files, domain="MATHEMATICAL",
            api_get=fetch or self.api, candidate_author="fyremael")

    def test_exact_protected_record_recognized_with_no_new_certification(self):
        result = self.verify()
        self.assertEqual(result["disposition"], "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED")
        self.assertEqual(result["subject_sha"], self.head)
        self.assertFalse(result["authority"]["new_certification_created"])
        self.assertEqual(result["material_fingerprint"], material_fingerprint(self.files))

    def test_candidate_forged_review_not_consulted(self):
        # Only the MATHCERT protected main API is ever called.
        visited = []
        def read(path):
            visited.append(path)
            return self.api(path)
        self.verify(read)
        self.assertTrue(visited)
        self.assertTrue(all("/repos/grandchallenge/MATHCERT/" in x for x in visited))

    def test_wrong_authority_domain_fail_closed(self):
        with self.assertRaises(ReceiptError):
            protected_specialist_receipt(head=self.head, files=self.files,
                                         domain="MODEL_USER_APPROVED", api_get=self.api,
                                         candidate_author="fyremael")

    def test_changed_candidate_blob_invalidates_review(self):
        files = copy.deepcopy(self.files)
        files[0]["sha"] = "f" * 40
        with self.assertRaisesRegex(ReceiptError, "candidate material"):
            protected_specialist_receipt(head=self.head, files=files,
                                         domain="MATHEMATICAL", api_get=self.api,
                                         candidate_author="fyremael")

    def test_changed_candidate_head_invalidates_review(self):
        with self.assertRaisesRegex(ReceiptError, "candidate material"):
            protected_specialist_receipt(head="f" * 40, files=self.files,
                                         domain="MATHEMATICAL", api_get=self.api,
                                         candidate_author="fyremael")

    def test_refuted_or_pending_specialist_evidence_is_not_approved(self):
        self.receipt["verdict"] = "PENDING"
        with self.assertRaisesRegex(ReceiptError, "positive"):
            self.verify()

    def test_proof_with_wrong_reviewed_bytes_rejected(self):
        self.proof["material_fingerprint"] = "0" * 64
        with self.assertRaisesRegex(ReceiptError, "not positively bound"):
            self.verify()

    def test_proof_missing_independence_rejected(self):
        self.proof["review_independence"] = "ROLE_SCOPED_NON_AUTHOR_SPECIALIST"
        with self.assertRaisesRegex(ReceiptError, "independence"):
            self.verify()

    def test_candidate_cannot_serve_as_independent_reviewer(self):
        self.proof["reviewer_identity"] = "fyremael"
        with self.assertRaisesRegex(ReceiptError, "candidate author"):
            self.verify()

    def test_proof_with_wrong_review_role_rejected(self):
        self.proof["authority_domain"] = "SOURCE_SEMANTIC"
        with self.assertRaisesRegex(ReceiptError, "not positively bound"):
            self.verify()

    def test_proof_with_missing_reviewer_identity_rejected(self):
        self.proof["reviewer_identity"] = ""
        with self.assertRaisesRegex(ReceiptError, "identity"):
            self.verify()

    def test_proof_with_changed_claim_scope_rejected(self):
        self.proof["review_scope"] = "Unrelated theorem"
        with self.assertRaisesRegex(ReceiptError, "scope differs"):
            self.verify()

    def test_noncertifying_source_path_rejected(self):
        self.receipt["protected_evidence"]["path"] = "docs/CM4-review.json"
        with self.assertRaisesRegex(ReceiptError, "source path"):
            self.verify()

    def test_source_identity_mismatch_rejected(self):
        self.receipt["source_repository"] = "grandchallenge/MATHSOLVE"
        with self.assertRaisesRegex(ReceiptError, "not authoritative"):
            self.verify()

    def test_underlying_evidence_changed_rejected(self):
        self.receipt["protected_evidence"]["blob_sha"] = "f" * 40
        with self.assertRaisesRegex(ReceiptError, "byte identity"):
            self.verify()

    def test_self_reference_rejected(self):
        self.receipt["protected_evidence"]["path"] = (
            "governance/material_admission_receipts/MATH-PROGRAMME-" + self.head + ".json"
        )
        with self.assertRaises(ReceiptError):
            self.verify()

    def test_live_main_advance_fails_closed(self):
        count = 0
        def moving(path):
            nonlocal count
            if path.endswith("/git/ref/heads/main"):
                count += 1
                return {"object": {"sha": "f" * 40 if count == 2 else self.source}}
            return self.api(path)
        with self.assertRaisesRegex(ReceiptError, "moved"):
            self.verify(moving)

    def test_missing_protected_receipt_fails_closed(self):
        def missing(path):
            if "material_admission_receipts" in path:
                raise ReceiptError("HTTP 404 no admitted receipt")
            return self.api(path)
        with self.assertRaises(ReceiptError):
            self.verify(missing)

    def test_missing_or_duplicate_material_manifest_not_trusted(self):
        for manifest in ([], self.files * 2):
            with self.subTest(manifest=manifest), self.assertRaises(ReceiptError):
                material_fingerprint(manifest)

    def test_material_fingerprint_order_independent(self):
        rows = self.files + [{"filename": "docs/CM4.md",
                              "status": "modified", "sha": "f" * 40}]
        self.assertEqual(material_fingerprint(rows), material_fingerprint(list(reversed(rows))))

    def test_unknown_manifest_status_rejected(self):
        rows = [{"filename": "docs/foo.md", "status": "evil", "sha": "f" * 40}]
        with self.assertRaises(ReceiptError):
            material_fingerprint(rows)


    def test_multi_file_governance_specialist_accepted_only_with_protected_receipt(self):
        head = self.head
        files = [
            {"filename": "ci/agent_routine_review.py", "status": "modified", "sha": "e" * 40},
            {"filename": "ci/specialist_admission_shadow.py", "status": "modified", "sha": "f" * 40},
        ]
        pr = {
            "state": "open", "draft": False, "changed_files": 2,
            "head": {"sha": head, "repo": {"full_name": "grandchallenge/MATH-PROGRAMME"}},
            "base": {"ref": "main", "sha": "b" * 40},
            "user": {"login": "fyremael"},
        }
        witness = {"disposition": "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED",
                   "domain": "PROTECTION", "subject_sha": head}
        with patch.dict("os.environ", {"SPECIALIST_READ_TOKEN": "read-domain-token"}), \
             patch("agent_routine_review.protected_specialist_receipt", return_value=witness) as verified:
            finding = exact_specialist_disposition(pr, files, head, read_token="programme-token")
        self.assertEqual(finding, witness)
        self.assertEqual(verified.call_args.kwargs["domain"], "PROTECTION")
        body = review_body(head, {"disposition": "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED",
                                  "material_evidence": witness})
        self.assertIn("separately protected", body)
        self.assertNotIn("Verifier and Adversary are non-authoring", body)

    def test_unclassified_mixed_paths_rejected_without_domain_lookup(self):
        with self.assertRaisesRegex(RoutineReviewError, "unresolved or mixed"):
            specialist_domain_for_file_manifest([
                {"filename": "ci/agent_routine_review.py"},
                {"filename": "docs/CM4.md"},
            ])

    def test_workflow_scopes_only_read_to_specialist_domains(self):
        workflow = (Path(__file__).resolve().parents[1] /
                    ".github/workflows/agent-routine-review.yml").read_text(encoding="utf-8")
        self.assertIn("SPECIALIST_READ_TOKEN", workflow)
        self.assertIn("permission-contents: read", workflow)
        self.assertEqual(workflow.count("permission-pull-requests: write"), 1)
        self.assertIn("MATHCERT", workflow)
        self.assertIn("MATHFORGE", workflow)
        self.assertIn("INTELLECT", workflow)

    def test_specialist_cannot_self_approve(self):
        pr = {
            "state": "open", "draft": False, "changed_files": 1,
            "head": {"sha": self.head,
                     "repo": {"full_name": "grandchallenge/MATH-PROGRAMME"}},
            "base": {"ref": "main", "sha": self.source},
            "user": {"login": "gcl-release-trust[bot]"},
        }
        with self.assertRaisesRegex(RoutineReviewError, "self-authorship"):
            exact_specialist_disposition(pr, [
                {"filename": "ci/agent_routine_review.py", "status": "modified",
                 "sha": "e" * 40}
            ], self.head, read_token="reader")


if __name__ == "__main__":
    unittest.main()
