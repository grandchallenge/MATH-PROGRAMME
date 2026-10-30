from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ci"))
from agent_routine_review import (  # noqa: E402
    APP_REVIEWER, REMOVE_EXACTLY, REQUIRED_HEAD_CONTEXTS, REPOSITORY,
    RoutineReviewError, candidate_number, eligible_image_removal,
    removed_patch_text, required_contexts_green,
    specialist_domain_for_file_manifest, bounded_oai26_editorial_not_applicable,
)


class RoutineAgentReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.head = "a" * 40
        self.pr = {
            "state": "open", "draft": False, "changed_files": 1,
            "head": {"sha": self.head, "repo": {"full_name": REPOSITORY}},
            "base": {"ref": "main"},
            "user": {"login": "fyremael"},
        }
        self.files = [{
            "filename": "docs/index.md", "status": "modified",
            "additions": 0, "deletions": 6,
            "patch": "@@ -1,10 +1,4 @@ context\n"
                + "".join("-" + line for line in REMOVE_EXACTLY.splitlines(keepends=True))
                + " context unchanged\n",
        }]

    def test_queue_controller_is_protection_not_mathematical(self) -> None:
        files = [{"filename": name} for name in (
            ".ghos-routing/workflows.json",
            ".github/workflows/erdos-catalogue-queue-projection.yml",
            "ci/erdos_catalogue_queue_projection.py",
            "tests/test_erdos_catalogue_queue_projection.py",
            "ci/agent_routine_review.py",
            "tests/test_agent_routine_review.py",
        )]
        self.assertEqual(specialist_domain_for_file_manifest(files), "PROTECTION")

    def test_unknown_queue_related_file_still_fails_closed(self) -> None:
        with self.assertRaisesRegex(RoutineReviewError, "unresolved or mixed"):
            specialist_domain_for_file_manifest([
                {"filename": "ci/erdos_catalogue_queue_projection.py"},
                {"filename": "ci/other_unclassified_controller.py"},
            ])

    def test_action_pin_support_files_require_protection_review(self) -> None:
        files = [{"filename": name} for name in (
            ".github/workflows/ci.yml",
            ".github/workflows/erdos-rolling-review-completion.yml",
            "ci/validate_workflow_coverage_v2.py",
            "governance/administrative_maintenance_trigger_registry.json",
            "schemas/administrative_maintenance_trigger_registry.schema.json",
            "tests/test_release_trust_admin.py",
        )]
        self.assertEqual(specialist_domain_for_file_manifest(files), "PROTECTION")

    def test_unlisted_action_pin_auxiliary_file_still_fails_closed(self) -> None:
        with self.assertRaisesRegex(RoutineReviewError, "unresolved or mixed"):
            specialist_domain_for_file_manifest([
                {"filename": ".github/workflows/ci.yml"},
                {"filename": "ci/unregistered_action_pin_assertions.py"},
            ])

    def test_oai26_single_editorial_is_not_automatic_review(self) -> None:
        self.assertTrue(bounded_oai26_editorial_not_applicable(
            self.pr,
            [{"filename": "governance/oai26_compendium/editorial/001.md",
              "status": "added"}],
            self.head,
        ))
        for path in ("governance/oai26_compendium/editorial/../../x.md",
                     "governance/oai26_compendium/editorial/001.json",
                     "governance/oai26_compendium/editorial/001.md/evil"):
            self.assertFalse(bounded_oai26_editorial_not_applicable(
                self.pr, [{"filename": path, "status": "added"}], self.head,
            ))
        self.assertFalse(bounded_oai26_editorial_not_applicable(
            self.pr, [{"filename": "governance/oai26_compendium/editorial/001.md",
                       "status": "added", "previous_filename": "x.md"}], self.head,
        ))
        self.assertFalse(bounded_oai26_editorial_not_applicable(
            self.pr, [{"filename": "governance/oai26_compendium/editorial/001.md",
                       "status": "added"}, {"filename": "docs/index.md",
                       "status": "modified"}], self.head,
        ))

    def test_exact_image_removal_is_routine(self) -> None:
        eligible_image_removal(self.pr, self.files, self.head)
        self.assertEqual(removed_patch_text(self.files[0]["patch"]), REMOVE_EXACTLY)

    def test_adversarial_claim_deletion_is_rejected(self) -> None:
        files = copy.deepcopy(self.files)
        files[0]["patch"] = files[0]["patch"].replace(
            "-## The GCL continuity fabric", "-## Proof of the Riemann hypothesis"
        )
        with self.assertRaisesRegex(RoutineReviewError, "deletion content"):
            eligible_image_removal(self.pr, files, self.head)

    def test_adversarial_added_claim_is_rejected(self) -> None:
        files = copy.deepcopy(self.files)
        files[0]["patch"] += "+Theorem CM4 proved by this edit.\n"
        with self.assertRaisesRegex(RoutineReviewError, "unexpected added"):
            eligible_image_removal(self.pr, files, self.head)

    def test_unknown_file_fails_closed(self) -> None:
        files = copy.deepcopy(self.files)
        files[0]["filename"] = "fixtures/formal/CMDG-NAT-CONCORDANCE-001/test.lean"
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(self.pr, files, self.head)

    def test_unsafe_multi_file_scope_fails_closed(self) -> None:
        pr = copy.deepcopy(self.pr)
        pr["changed_files"] = 2
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(pr, self.files, self.head)

    def test_reviewer_does_not_review_own_work(self) -> None:
        pr = copy.deepcopy(self.pr)
        pr["user"]["login"] = APP_REVIEWER
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(pr, self.files, self.head)

    def test_stale_head_fails_closed(self) -> None:
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(self.pr, self.files, "b" * 40)

    def test_external_fork_fails_closed(self) -> None:
        pr = copy.deepcopy(self.pr)
        pr["head"]["repo"]["full_name"] = "random/MATH-PROGRAMME"
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(pr, self.files, self.head)

    def test_missing_context_fails_closed(self) -> None:
        checks = [
            {"name": name, "status": "completed", "conclusion": "success"}
            for name in REQUIRED_HEAD_CONTEXTS if name != "routing-enforcement"
        ]
        with self.assertRaisesRegex(RoutineReviewError, "missing"):
            required_contexts_green(checks, [])

    def test_pending_context_fails_closed(self) -> None:
        checks = [
            {"name": name, "status": "completed", "conclusion": "success"}
            for name in REQUIRED_HEAD_CONTEXTS if name != "validate-json"
        ]
        checks.append({"name": "validate-json", "status": "in_progress"})
        with self.assertRaisesRegex(RoutineReviewError, "failed_or_pending"):
            required_contexts_green(checks, [])

    def test_all_checks_and_routing_green(self) -> None:
        checks = [
            {"name": name, "status": "completed", "conclusion": "success"}
            for name in REQUIRED_HEAD_CONTEXTS if name != "routing-enforcement"
        ]
        required_contexts_green(
            checks, [{"context": "routing-enforcement", "state": "success"}]
        )

    def test_workflow_event_must_bind_one_sha_and_one_pr(self) -> None:
        self.assertEqual(
            candidate_number({
                "workflow_run": {
                    "event": "pull_request", "conclusion": "success",
                    "head_sha": self.head,
                    "repository": {"full_name": REPOSITORY},
                    "pull_requests": [{"number": 1246}],
                },
            }, "workflow_run"), (1246, self.head),
        )
        self.assertIsNone(candidate_number({
            "workflow_run": {"event": "pull_request", "conclusion": "success",
                             "head_sha": self.head,
                             "repository": {"full_name": REPOSITORY},
                             "pull_requests": []},
        }, "workflow_run"))

    def test_ready_event_binds_internal_pr_to_immutable_head(self) -> None:
        pr = {
            "number": 1265, "draft": False,
            "head": {"sha": self.head, "repo": {"full_name": REPOSITORY}},
            "base": {"ref": "main"},
        }
        event = {"action": "ready_for_review", "number": 1265, "pull_request": pr}
        self.assertEqual(candidate_number(event, "pull_request_target"), (1265, self.head))

    def test_ready_replay_rejects_fork_draft_and_stale_action(self) -> None:
        pr = {
            "number": 1265, "draft": False,
            "head": {"sha": self.head, "repo": {"full_name": REPOSITORY}},
            "base": {"ref": "main"},
        }
        event = {"action": "ready_for_review", "number": 1265, "pull_request": pr}
        for operation, changed in (
            ("fork", {"head": {"sha": self.head, "repo": {"full_name": "other/fork"}}}),
            ("draft", {"draft": True}),
            ("wrong_base", {"base": {"ref": "develop"}}),
            ("unbound_head", {"head": {"sha": "nope", "repo": {"full_name": REPOSITORY}}}),
        ):
            with self.subTest(operation=operation):
                sample = {**pr, **changed}
                self.assertIsNone(candidate_number({**event, "pull_request": sample},
                                                   "pull_request_target"))
        self.assertIsNone(candidate_number({**event, "action": "labeled"},
                                           "pull_request_target"))

    def test_workflow_run_uses_pr_linked_head_not_synthetic_merge_sha(self) -> None:
        event = {"workflow_run": {
            "event": "pull_request", "conclusion": "success",
            "repository": {"full_name": REPOSITORY},
            "head_sha": "b" * 40,
            "pull_requests": [{"number": 1265, "head": {"sha": self.head}}],
        }}
        self.assertEqual(candidate_number(event, "workflow_run"), (1265, self.head))

    def test_workflow_run_multiple_prs_fails_closed(self) -> None:
        event = {"workflow_run": {
            "event": "pull_request", "conclusion": "success",
            "repository": {"full_name": REPOSITORY},
            "head_sha": "b" * 40,
            "pull_requests": [{"number": 1}, {"number": 2}],
        }}
        self.assertIsNone(candidate_number(event, "workflow_run"))

    def test_protected_workflow_has_no_candidate_checkout(self) -> None:
        workflow = (Path(__file__).resolve().parents[1] /
                    ".github/workflows/agent-routine-review.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request_target:", workflow)
        self.assertIn("ready_for_review", workflow)
        self.assertIn("ref: main", workflow)
        self.assertIn("permission-pull-requests: write", workflow)
        self.assertNotIn("ref: ${{ github.event.pull_request.head.sha }}", workflow)



if __name__ == "__main__":
    unittest.main()

# GCL-ARC-001: protection-grade role evidence, one real transport login.
from agent_role_receipt import AgentRoleError, LEGACY_V1, verify_agent_role_receipt  # noqa: E402


class ProtectedAgentRoleReceiptTests(unittest.TestCase):
    def setUp(self):
        # The only historical V1 specimen eligible for replay is byte-pinned.
        self.head = LEGACY_V1["subject_head"]
        self.source_head = LEGACY_V1["source_head"]
        self.blob = LEGACY_V1["dossier_blob"]
        self.digest = LEGACY_V1["material_sha256"]
        self.path = "governance/agent_execution/reviews/MATH-PROGRAMME-" + self.head + ".json"
        self.subject = {"repository": "grandchallenge/MATH-PROGRAMME",
                        "head_sha": self.head, "material_sha256": self.digest}
        self.receipt = {
            "schema_version": "2.0.0",
            "record_type": "GCL_PROTECTED_AGENT_ROLE_ADMISSION_EVIDENCE_V1",
            "source_repository": "grandchallenge/INTELLECT",
            "authority_domain": "PROTECTION",
            "subject": self.subject,
            "verdict": "ADMISSIBLE_FOR_PROTECTED_ADMISSION",
            "protected_evidence": {"path": self.path, "blob_sha": self.blob},
            "source_review_anchor": {
                "source_pr_number": LEGACY_V1["source_pr"],
                "source_pr_head_sha": self.source_head,
                "review_dossier_blob_sha": self.blob,
            }
        }
        self.dossier = {
            "record_type": "GCL_AGENT_REVIEW_DOSSIER_V1",
            "subject": self.subject, "work_class": "MATERIAL_CONTROL",
            "transport_login": "fyremael",
            "claimed_effects": {"mathematical_certification": False,
                                "reserved_authorization": False,
                                "credential_escalation": False},
            "passes": [
                {"role": role, "logical_pass_id": "PASS-" + role,
                 "reviewer_system_id": "same-agent",
                 "transport_login": "fyremael",
                 "subject_head_sha": self.head,
                 "mode": "non_authoring_read_only", "write_set": [],
                 "read_set": ["source exact H"],
                 "checks": [{"command": "python -m unittest",
                             "exit_code": 0, "receipt_sha256": self.digest}],
                 "negative_controls": ["forged-metadata-rejected"]
                      if role == "ADVERSARY" else [],
                 "finding": "ACCEPT_BOUNDED", "unresolved": []}
                for role in ("VERIFIER", "ADVERSARY", "REFEREE")
            ]
        }
        self.pr = {"merged_at": "2026-10-15T08:00:00Z",
                   "head": {"sha": self.source_head}, "base": {"ref": "main"},
                   "changed_files": 1}
        self.source_files = [
            {"filename": self.path, "sha": self.blob, "status": "added"}]
        self.runs = [
            {"name": name, "conclusion": "success", "head_sha": self.source_head}
            for name in ("test (3.11.14)", "test (3.12.13)",
                         "policy / policy", "security / action-policy",
                         "routing-enforcement")
        ]

    def read(self, repo, path, revision):
        self.assertEqual(repo, "grandchallenge/INTELLECT")
        self.assertEqual(path, self.path)
        self.assertEqual(revision, "e"*40)
        return self.dossier, self.blob

    def api(self, path):
        prefix = "/repos/grandchallenge/INTELLECT"
        responses = {
            prefix + "/pulls/121": self.pr,
            prefix + "/pulls/121/files?per_page=100": self.source_files,
            prefix + "/commits/" + self.source_head +
                "/check-runs?per_page=100":
                {"total_count": len(self.runs), "check_runs": self.runs},
            prefix + "/git/ref/heads/main": {"object": {"sha": "e"*40}}
        }
        return responses[path]

    def evaluate(self):
        return verify_agent_role_receipt(
            receipt=self.receipt, receipt_path="governance/material_admission_receipts/"
              "MATH-PROGRAMME-" + self.head + ".json",
            receipt_blob=LEGACY_V1["receipt_blob"],
            read_protected_json=self.read, api_get=self.api,
            protected_sha="e"*40, subject_head=self.head,
            material_digest=self.digest, actual_actor="fyremael")

    def test_version_two_dispatch_before_legacy_schema(self):
        # End-to-end dispatch must reach the protected ARC1 verifier.
        from unittest.mock import patch
        import specialist_receipt_adapter as legacy
        fs = [{"filename": "ci/erdos_catalogue_queue_projection.py",
               "status": "modified", "sha": "e" * 40}]
        new_receipt = dict(self.receipt)
        new_receipt["subject"] = {
            "repository": "grandchallenge/MATH-PROGRAMME",
            "head_sha": self.head,
            "material_sha256": legacy.material_fingerprint(fs)}
        ref_url = "/repos/grandchallenge/INTELLECT/git/ref/heads/main"
        with patch.object(legacy, "_protected_json", return_value=(new_receipt, "f"*40)):
            with patch.object(legacy, "verify_agent_role_receipt",
                              return_value={"disposition": "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED"}) as verifier:
                result = legacy.protected_specialist_receipt(
                    head=self.head, files=fs, domain="PROTECTION",
                    api_get=lambda url: {"object": {"sha": "f"*40}}
                        if url == ref_url else {},
                    candidate_author="fyremael")
                self.assertEqual(result["disposition"],
                                 "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED")
                verifier.assert_called_once()

    def test_version_two_for_other_domain_rejected(self):
        # This lane must not re-interpret MATHCERT or other specialist receipts.
        from unittest.mock import patch
        import specialist_receipt_adapter as legacy
        fs = [{"filename": "ci/erdos_catalogue_queue_projection.py",
               "status": "modified", "sha": "e" * 40}]
        with patch.object(legacy, "_protected_json", return_value=(self.receipt,"f"*40)):
            with patch.object(legacy, "verify_agent_role_receipt") as verifier:
                with self.assertRaises(legacy.ReceiptError):
                    legacy.protected_specialist_receipt(
                        head=self.head, files=fs, domain="MATHEMATICAL",
                        api_get=lambda url: {"object": {"sha": "f"*40}},
                        candidate_author="fyremael")
                verifier.assert_not_called()

    def test_valid_shared_login_three_real_role_passes(self):
        r = self.evaluate()
        self.assertEqual(r["disposition"], "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED")
        self.assertEqual(r["authenticated_review_origin"]["agent_roles_verified"],
                         ["VERIFIER", "ADVERSARY", "REFEREE"])
        self.assertFalse(r["authority"]["new_certification_created"])

    def test_wrong_candidate_head_rejected(self):
        self.receipt["subject"]["head_sha"] = "9"*40
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_changed_dossier_blob_rejected(self):
        self.receipt["protected_evidence"]["blob_sha"] = "9"*40
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_review_mode_cannot_write(self):
        self.dossier["passes"][0]["write_set"].append("main")
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_cloned_pass_id_rejected(self):
        self.dossier["passes"][1]["logical_pass_id"] = "PASS-VERIFIER"
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_adversary_without_negative_controls_rejected(self):
        self.dossier["passes"][1]["negative_controls"] = []
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_referee_revise_is_a_blocker(self):
        self.dossier["passes"][2]["finding"] = "REVISE"
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_failed_check_is_a_blocker(self):
        self.dossier["passes"][0]["checks"][0]["exit_code"] = 1
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_never_embed_own_pr_head_in_dossier(self):
        self.dossier["source_pr_head_sha"] = self.source_head
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_protected_source_merge_required(self):
        self.pr["merged_at"] = None
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_source_pr_must_contain_actual_blob(self):
        self.source_files[0]["sha"] = "9"*40
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_every_protected_ci_check_required(self):
        self.runs[0]["conclusion"] = "failure"
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_source_main_moved_readback_rejected(self):
        original = self.api
        def moved(path):
            if path.endswith("/git/ref/heads/main"):
                return {"object": {"sha": "9"*40}}
            return original(path)
        self.api = moved
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_forged_github_actor_rejected(self):
        self.dossier["transport_login"] = "fake-reviewer"
        with self.assertRaises(AgentRoleError): self.evaluate()

    def test_claim_certification_rejected(self):
        self.dossier["claimed_effects"]["mathematical_certification"] = True
        with self.assertRaises(AgentRoleError): self.evaluate()


class ResearchOnlyDelegatedReviewAbstentionTests(unittest.TestCase):
    """No App approval is invented when a mathematical PR is not routine."""

    def setUp(self):
        self.head = "e" * 40
        self.pr = {
            "state": "open", "draft": False, "changed_files": 4,
            "head": {"sha": self.head,
                     "repo": {"full_name": "grandchallenge/MATH-PROGRAMME"}},
            "base": {"ref": "main", "sha": "f" * 40},
            "user": {"login": "fyremael"},
        }
        self.files = [
            {"filename": "research/erdos-41-density/ONE.md",
             "status": "added"},
            {"filename": "research/erdos-41-density/TWO.md",
             "status": "added"},
            {"filename": "tests/test_erdos41_one.py",
             "status": "added"},
            {"filename": "tests/test_erdos41_two.py",
             "status": "added"},
        ]

    def test_exact_research_with_tests_is_non_delegable_not_approval(self):
        from agent_routine_review import bounded_research_not_applicable
        self.assertTrue(bounded_research_not_applicable(
            self.pr, self.files, self.head))

    def test_nonresearch_and_mixed_are_not_marked_not_applicable(self):
        from agent_routine_review import bounded_research_not_applicable
        for bad in (
            {"filename": "ci/agent_routine_review.py", "status": "modified"},
            {"filename": "docs/index.md", "status": "modified"},
            {"filename": "fixtures/formal/demo.lean", "status": "added"},
            {"filename": ".github/workflows/agent-routine-review.yml",
             "status": "modified"},
            {"filename": "tests/test_agent_routine_review.py",
             "status": "modified"},
            {"filename": "research/erdos-41-density/PATH.md",
             "status": "removed"},
            {"filename": "research/erdos-41-density/PATH.md",
             "status": "renamed", "previous_filename": "old.md"},
        ):
            with self.subTest(filename=bad["filename"]):
                self.pr["changed_files"] = 5
                self.assertFalse(bounded_research_not_applicable(
                    self.pr, self.files + [bad], self.head))
        self.pr["changed_files"] = 4

    def test_tests_alone_are_not_a_proof_packet(self):
        from agent_routine_review import bounded_research_not_applicable
        self.pr["changed_files"] = 1
        self.assertFalse(bounded_research_not_applicable(
            self.pr, [self.files[2]], self.head))

    def test_malformed_manifest_and_stale_head_still_fail_closed(self):
        from agent_routine_review import (
            bounded_research_not_applicable, RoutineReviewError,
        )
        self.pr["changed_files"] = 7
        with self.assertRaisesRegex(RoutineReviewError, "inventory"):
            bounded_research_not_applicable(self.pr, self.files, self.head)
        self.pr["changed_files"] = 4
        with self.assertRaisesRegex(RoutineReviewError, "head mismatch"):
            bounded_research_not_applicable(self.pr, self.files, "9" * 40)

    def test_explicit_not_applicable_summary_never_claims_review(self):
        import os
        import tempfile
        from unittest.mock import patch
        from agent_routine_review import report_delegated_review_not_applicable
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "summary.md")
            with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": path}):
                report_delegated_review_not_applicable(self.head, self.files, "jimsteeg")
            with open(path, encoding="utf-8") as src:
                message = src.read()
            self.assertIn("NOT_APPLICABLE", message)
            self.assertIn("No automated approval", message)
            self.assertIn(self.head, message)

    def test_nonauthor_provenance_is_exact_head_and_latest_state(self):
        from unittest.mock import patch
        import agent_routine_review as mod
        reviews = [
            {"id": 1, "user": {"login": "jimsteeg"},
             "state": "APPROVED", "commit_id": self.head,
             "submitted_at": "2026-10-21T12:00:00Z"},
        ]
        with patch.object(mod, "api", return_value=reviews):
            self.assertEqual(mod.exact_head_nonauthor_review(
                self.pr, 2808, self.head, token="read",
                prefix="/repos/grandchallenge/MATH-PROGRAMME"), "jimsteeg")
        hostile = [
            [{"id": 1, "user": {"login": "fyremael"},
              "state": "APPROVED", "commit_id": self.head}],
            [{"id": 1, "user": {"login": "jimsteeg"},
              "state": "APPROVED", "commit_id": "f" * 40}],
            [{"id": 1, "user": {"login": "jimsteeg"},
              "state": "COMMENTED", "commit_id": self.head}],
            [{"id": 1, "user": {"login": "gcl-release-trust[bot]"},
              "state": "APPROVED", "commit_id": self.head}],
            [],
            [reviews[0], {"id": 2, "user": {"login": "jimsteeg"},
                          "state": "DISMISSED", "commit_id": self.head,
                          "submitted_at": "2026-10-21T14:00:00Z"}],
        ]
        for returned in hostile:
            with self.subTest(reviews=returned):
                with patch.object(mod, "api", return_value=returned):
                    with self.assertRaises(mod.RoutineReviewError):
                        mod.exact_head_nonauthor_review(
                            self.pr, 2808, self.head, token="read",
                            prefix="/repos/grandchallenge/MATH-PROGRAMME")

    def test_research_not_applicable_without_review_is_failure_not_green(self):
        import json
        import os
        import tempfile
        from unittest.mock import patch
        import agent_routine_review as mod
        with tempfile.TemporaryDirectory() as d:
            event = os.path.join(d, "event.json")
            with open(event, "w", encoding="utf-8") as out:
                json.dump({"inputs": {"pr_number": 2808}}, out)
            def fake_api(method, path, *, token, payload=None):
                self.assertEqual(method, "GET")
                if path.endswith("/pulls/2808"):
                    return self.pr
                if path.endswith("/pulls/2808/files?per_page=100"):
                    return self.files
                if path.endswith("/pulls/2808/reviews?per_page=100"):
                    return []
                raise AssertionError("unexpected request")
            with patch.dict(os.environ, {
                "GITHUB_EVENT_PATH": event,
                "GITHUB_EVENT_NAME": "workflow_dispatch",
                "GITHUB_TOKEN": "read-token",
            }):
                with patch.object(mod, "api", side_effect=fake_api):
                    with patch.object(mod, "delegated_classification",
                                      side_effect=mod.RoutineReviewError(
                                          "unknown or multifile material closure")):
                        with patch.object(mod, "exact_specialist_disposition") as sp:
                            with self.assertRaisesRegex(
                                    mod.RoutineReviewError,
                                    "lacks current-head non-author"):
                                mod.main()
                            sp.assert_not_called()

    def test_research_only_runtime_stops_before_domain_call_or_review_post(self):
        import json
        import os
        import tempfile
        from unittest.mock import patch
        import agent_routine_review as mod
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "event.json")
            summary = os.path.join(d, "summary.md")
            with open(path, "w", encoding="utf-8") as out:
                json.dump({"inputs": {"pr_number": 2808}}, out)
            def fake_api(method, path, *, token, payload=None):
                self.assertEqual(method, "GET", "No GitHub POST may occur")
                if path.endswith("/pulls/2808"):
                    return self.pr
                if path.endswith("/pulls/2808/files?per_page=100"):
                    return self.files
                if path.endswith("/pulls/2808/reviews?per_page=100"):
                    return [{
                        "id": 3, "user": {"login": "jimsteeg"},
                        "state": "APPROVED", "commit_id": self.head,
                        "submitted_at": "2026-10-21T23:28:04Z",
                    }]
                raise AssertionError("unexpected GitHub request: " + path)
            with patch.dict(os.environ, {
                "GITHUB_EVENT_PATH": path,
                "GITHUB_EVENT_NAME": "workflow_dispatch",
                "GITHUB_TOKEN": "test-read-token",
                "GITHUB_STEP_SUMMARY": summary,
            }):
                with patch.object(mod, "api", side_effect=fake_api) as api_mock:
                    with patch.object(mod, "delegated_classification",
                                      side_effect=mod.RoutineReviewError(
                                          "unknown or multifile material closure")):
                        with patch.object(mod, "exact_specialist_disposition") as specialist:
                            self.assertEqual(mod.main(), 0)
                            specialist.assert_not_called()
                    self.assertEqual(api_mock.call_count, 3)
            with open(summary, encoding="utf-8") as src:
                self.assertIn("NOT_APPLICABLE", src.read())
