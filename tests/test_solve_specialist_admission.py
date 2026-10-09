from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from specialist_domains import (  # noqa: E402
    DomainRegistryError, domain_for_paths, load_domains, protected_path,
)
from specialist_receipt_adapter import (  # noqa: E402
    ReceiptError, material_fingerprint, protected_specialist_receipt,
)
from agent_routine_review import (  # noqa: E402
    RoutineReviewError, specialist_domain_for_file_manifest,
)
import specialist_admission_shadow as shadow  # noqa: E402


class SolveSpecialistTests(unittest.TestCase):
    def setUp(self):
        self.head = "a" * 40
        self.base = "b" * 40
        self.proof_blob = "c" * 40
        self.receipt_blob = "d" * 40
        self.source_head = "e" * 40
        self.capture_blob = "1" * 40
        self.replay_blob = "2" * 40
        self.adjudication_blob = "3" * 40
        self.result_hash = "f" * 64
        self.dispatch = "OM26-H1-WP64-IA-001"
        self.result_ref = "RESULT-EXACT-001"
        self.files = [{"filename": "governance/mathsolve_routing_audit.json",
                       "status": "modified", "sha": "9" * 40}]
        self.effects = {
            "mathematical_claim_effect": False, "certification_effect": False,
            "publication_effect": False, "source_semantic_effect": False,
            "security_authority_effect": False,
        }
        self.chain = {
            "schema_version": "1.0.0", "dispatch_id": self.dispatch,
            "result_ref": self.result_ref, "result_sha256": self.result_hash,
            "capture": {"path": "contributions/solve-test/capture.json",
                        "blob_sha": self.capture_blob},
            "replay": {"path": "contributions/solve-test/replay.json",
                       "blob_sha": self.replay_blob},
            "adjudication": {"path": "contributions/solve-test/adjudication.json",
                             "blob_sha": self.adjudication_blob},
            "claim_effects": copy.deepcopy(self.effects),
        }
        self.receipt = {
            "schema_version": "1.0.0",
            "record_type": "GCL_PROTECTED_SPECIALIST_ADMISSION_EVIDENCE",
            "authority_domain": "SOLUTION_INTEGRITY",
            "source_repository": "grandchallenge/MATHSOLVE",
            "subject": {
                "repository": "grandchallenge/MATH-PROGRAMME",
                "head_sha": self.head,
                "material_fingerprint": material_fingerprint(self.files),
            },
            "verdict": "ADMISSIBLE_FOR_PROTECTED_ADMISSION",
            "protected_evidence": {
                "path": "contributions/solve-test/review.json",
                "blob_sha": self.proof_blob,
            },
            "review_scope": "SOLVE_EXECUTION_INTEGRITY_ONLY",
            "solve_execution": copy.deepcopy(self.chain),
        }
        self.proof = {
            "record_type": "GCL_DOMAIN_ROLE_SCOPED_REVIEW_V1",
            "authority_domain": "SOLUTION_INTEGRITY",
            "subject_repository": "grandchallenge/MATH-PROGRAMME",
            "subject_sha": self.head,
            "material_fingerprint": material_fingerprint(self.files),
            "disposition": "ROLE_SCOPED_REVIEW_ACCEPTED",
            "reviewer_identity": "solve-specialist-agent",
            "review_independence": "ROLE_SCOPED_NON_AUTHOR_SPECIALIST",
            "review_scope": "SOLVE_EXECUTION_INTEGRITY_ONLY",
            "solve_execution": copy.deepcopy(self.chain),
            "review_anchor": {
                "source_pr_number": 902, "source_pr_head_sha": self.source_head,
                "review_id": 729, "reviewer_login": "solve-specialist-agent",
            },
        }
        self.capture = {
            "record_type": "GCL_SOLVE_CAPTURE_RECEIPT_V1",
            "dispatch_id": self.dispatch, "result_ref": self.result_ref,
            "result_sha256": self.result_hash,
        }
        self.replay = {
            "record_type": "GCL_SOLVE_REPLAY_RECEIPT_V1",
            "dispatch_id": self.dispatch, "result_ref": self.result_ref,
            "input_result_sha256": self.result_hash,
            "capture_blob_sha": self.capture_blob, "replay_pass": True,
        }
        self.adjudication = {
            "record_type": "GCL_SOLVE_ADJUDICATION_RECEIPT_V1",
            "dispatch_id": self.dispatch, "result_ref": self.result_ref,
            "replay_blob_sha": self.replay_blob,
            "adjudication_id": "SOLVE-ADJ-001",
            "adjudication_disposition": "REPLAYED_AND_ADJUDICATED",
            "claim_effects": copy.deepcopy(self.effects),
        }
        self.pr = {
            "head": {"sha": self.source_head}, "base": {"ref": "main"},
            "user": {"login": "independent-solve-evidence-author"},
            "merged_at": "2026-10-09T10:00:00Z", "changed_files": 1,
        }
        self.reviews = [{
            "id": 729, "state": "APPROVED", "commit_id": self.source_head,
            "submitted_at": "2026-10-09T10:11:00Z",
            "user": {"login": "solve-specialist-agent"},
        }]
        self.source_files = [{
            "filename": "contributions/solve-test/review.json",
            "status": "added", "sha": self.proof_blob,
        }]
        self.called = []

    def api(self, path: str):
        self.called.append(path)
        prefix = "/repos/grandchallenge/MATHSOLVE/"
        if not path.startswith(prefix):
            raise AssertionError("unexpected non-Solve authority: " + path)
        suffix = path[len(prefix):]
        if suffix == "git/ref/heads/main":
            return {"object": {"sha": self.base}}
        if suffix == "pulls/902":
            return self.pr
        if suffix == "pulls/902/files?per_page=100":
            return self.source_files
        if suffix == "pulls/902/reviews?per_page=100":
            return self.reviews
        if suffix.startswith("contents/"):
            if "material_admission_receipts" in suffix:
                value, sha = self.receipt, self.receipt_blob
            elif suffix.startswith("contents/contributions/solve-test/review.json"):
                value, sha = self.proof, self.proof_blob
            elif suffix.startswith("contents/contributions/solve-test/capture.json"):
                value, sha = self.capture, self.capture_blob
            elif suffix.startswith("contents/contributions/solve-test/replay.json"):
                value, sha = self.replay, self.replay_blob
            elif suffix.startswith("contents/contributions/solve-test/adjudication.json"):
                value, sha = self.adjudication, self.adjudication_blob
            else:
                raise AssertionError("unknown evidence: " + suffix)
            import base64
            payload = base64.b64encode(json.dumps(value).encode()).decode()
            return {"type": "file", "encoding": "base64", "sha": sha, "content": payload}
        raise AssertionError("unknown protected endpoint: " + suffix)

    def verify(self):
        return protected_specialist_receipt(
            head=self.head, files=self.files, domain="SOLUTION_INTEGRITY",
            api_get=self.api, candidate_author="fyremael",
        )

    def test_registry_contains_distinct_solve_domain(self):
        records = load_domains()
        self.assertEqual(set(records), {"MATHEMATICAL", "SOURCE_SEMANTIC",
                                         "SOLUTION_INTEGRITY", "PROTECTION"})
        solve = records["SOLUTION_INTEGRITY"]
        self.assertEqual(solve["repository"], "grandchallenge/MATHSOLVE")
        self.assertEqual(solve["review_scope"], "SOLVE_EXECUTION_INTEGRITY_ONLY")
        self.assertEqual(solve["review_record_type"], "GCL_DOMAIN_ROLE_SCOPED_REVIEW_V1")
        self.assertEqual(solve["independence"], "ROLE_SCOPED_NON_AUTHOR_SPECIALIST")

    def test_registered_solve_paths_are_consistent_in_both_controllers(self):
        for path in ("governance/mathsolve_routing_audit.json",
                     "governance/solution_integrity_001.json",
                     "governance/solve_execution_001.json"):
            with self.subTest(path=path):
                self.assertEqual(domain_for_paths([path]), "SOLUTION_INTEGRITY")
                self.assertEqual(shadow.specialist_domain([path]), "SOLUTION_INTEGRITY")
                self.assertEqual(specialist_domain_for_file_manifest(
                    [{"filename": path}]), "SOLUTION_INTEGRITY")

    def test_no_solve_review_can_override_math_or_security(self):
        self.assertEqual(domain_for_paths(["contributions/campaign/proof.lean"]),
                         "MATHEMATICAL")
        self.assertEqual(domain_for_paths([".github/workflows/unsafe.yml"]), "PROTECTION")
        self.assertTrue(protected_path("ci/specialist_domains.py"))
        for paths in (["governance/mathsolve_routing_audit.json", "docs/claim.md"],
                      ["governance/mathsolve_routing_audit.json", "ci/agent_routine_review.py"],
                      ["governance/mathsolve_routing_audit.json", "fixtures/formal/theorem.lean"],
                      ["work_packages/CMDG_CM4/WP.json"], ["docs/claim.md"]):
            with self.subTest(paths=paths):
                self.assertIsNone(domain_for_paths(paths))

    def test_unknown_domain_registry_tamper_rejected(self):
        with patch("specialist_domains.REGISTRY", ROOT / "nonexistent.json"):
            pass
        record = json.loads((ROOT / "governance/specialist_admission_domains.json").read_text())
        record["domains"][2]["review_scope"] = "MATHEMATICAL_PROOF_REVIEW"
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(record))
            with self.assertRaises(DomainRegistryError):
                load_domains(path)

    def test_valid_solve_chain_recognized_but_no_certification(self):
        out = self.verify()
        self.assertEqual(out["disposition"], "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED")
        self.assertEqual(out["source_repository"], "grandchallenge/MATHSOLVE")
        self.assertEqual(out["solve_execution_evidence"]["adjudication_id"], "SOLVE-ADJ-001")
        self.assertFalse(out["solve_execution_evidence"]["mathematical_certification"])
        self.assertFalse(out["authority"]["new_certification_created"])
        self.assertTrue(all("/repos/grandchallenge/MATHSOLVE/" in p for p in self.called))

    def test_missing_capture_fails_closed(self):
        self.chain.pop("capture")
        self.receipt["solve_execution"] = copy.deepcopy(self.chain)
        self.proof["solve_execution"] = copy.deepcopy(self.chain)
        with self.assertRaisesRegex(ReceiptError, "schema"):
            self.verify()

    def test_replay_must_bind_captured_result(self):
        self.replay["input_result_sha256"] = "0" * 64
        with self.assertRaisesRegex(ReceiptError, "replay"):
            self.verify()

    def test_replay_must_have_passed(self):
        self.replay["replay_pass"] = False
        with self.assertRaisesRegex(ReceiptError, "replay"):
            self.verify()

    def test_adjudication_cannot_omit_replay_lineage(self):
        self.adjudication["replay_blob_sha"] = "0" * 40
        with self.assertRaisesRegex(ReceiptError, "adjudication"):
            self.verify()

    def test_solve_cannot_promote_theorem_or_source(self):
        for effect in self.effects:
            with self.subTest(effect=effect):
                data = copy.deepcopy(self.effects)
                data[effect] = True
                self.receipt["solve_execution"]["claim_effects"] = data
                self.proof["solve_execution"]["claim_effects"] = data
                with self.assertRaisesRegex(ReceiptError, "promote"):
                    self.verify()
                self.receipt["solve_execution"]["claim_effects"] = copy.deepcopy(self.effects)
                self.proof["solve_execution"]["claim_effects"] = copy.deepcopy(self.effects)

    def test_proof_cannot_use_independent_theorem_type(self):
        self.proof["record_type"] = "GCL_DOMAIN_INDEPENDENT_REVIEW_V1"
        with self.assertRaisesRegex(ReceiptError, "positively bound"):
            self.verify()

    def test_proof_requires_role_scoped_disposition(self):
        self.proof["disposition"] = "INDEPENDENT_REVIEW_ACCEPTED"
        with self.assertRaisesRegex(ReceiptError, "positively bound"):
            self.verify()

    def test_proof_cannot_silently_replace_capture(self):
        self.proof["solve_execution"]["capture"]["blob_sha"] = "0" * 40
        with self.assertRaisesRegex(ReceiptError, "scope mismatch"):
            self.verify()

    def test_wrong_capture_blob_rejected(self):
        self.chain["capture"]["blob_sha"] = "0" * 40
        self.receipt["solve_execution"]["capture"]["blob_sha"] = "0" * 40
        self.proof["solve_execution"]["capture"]["blob_sha"] = "0" * 40
        with self.assertRaisesRegex(ReceiptError, "source lock"):
            self.verify()

    def test_non_author_review_and_exact_source_head_required(self):
        self.reviews[0]["state"] = "COMMENTED"
        with self.assertRaisesRegex(ReceiptError, "not approved"):
            self.verify()

    def test_independent_proof_required_if_math_domain(self):
        self.receipt["authority_domain"] = "MATHEMATICAL"
        with self.assertRaises(ReceiptError):
            self.verify()

    def test_merge_group_solve_scope_is_identified_but_not_approved(self):
        sha, base = "a" * 40, "b" * 40
        ref = "refs/heads/gh-readonly-queue/main/pr-solve-test"
        event = {"merge_group": {"head_sha": sha, "head_ref": ref,
                                  "base_ref": "refs/heads/main"}}
        env = {"GITHUB_SHA": sha, "GITHUB_REF": ref}
        def protected_git(root, *args, binary=False):
            if args[:2] == ("rev-parse", "HEAD"):
                return base
            if args[:2] == ("rev-parse", "refs/remotes/origin/gcl-shadow"):
                return sha
            if args[0] == "diff":
                return b"M\x00governance/mathsolve_routing_audit.json\x00"
            if args[0] == "show":
                return b"{}\\n"
            return ""
        with patch.object(shadow, "git", side_effect=protected_git):
            result = shadow.shadow_merge_group(event, Path("."), env)
        self.assertEqual(result["disposition"], "SPECIALIST_REVIEW_PENDING")
        self.assertEqual(result["specialist_domain_hint"], "SOLUTION_INTEGRITY")
        self.assertIn("not yet evaluated", result["reason"])

    def test_workflows_include_solve_readonly_and_no_cutover(self):
        for name in ("agent-routine-review.yml", "material-admission-shadow.yml"):
            workflow = (ROOT / ".github/workflows" / name).read_text()
            self.assertIn("MATHSOLVE", workflow)
            self.assertIn("permission-contents: read", workflow)
            self.assertIn("permission-pull-requests: read", workflow)
        shadow = (ROOT / ".github/workflows/material-admission-shadow.yml").read_text()
        self.assertNotIn("statuses: write", shadow)
        self.assertNotIn("pull-requests: write", shadow)


if __name__ == "__main__":
    unittest.main()
