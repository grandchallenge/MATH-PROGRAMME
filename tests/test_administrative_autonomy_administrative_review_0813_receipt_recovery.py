from __future__ import annotations

import base64
import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_autonomy_runtime_administrative_review_0813_receipt_recovery as recovery
from administrative_autonomy_receipt_stage import (
    STATE_PATH,
    advance_completion_state,
)
from autonomy_github import AutonomyError

CONTROL = ROOT / "governance" / "administrative_review_0813_receipt_recovery_control.json"
SCHEMA = ROOT / "schemas" / "administrative_review_0813_receipt_recovery_control.schema.json"
RUNTIME_ENTRY = ROOT / "ci" / "administrative_autonomy_runtime.py"
WORKFLOW = ROOT / ".github" / "workflows" / "administrative-maintenance-automation-validation.yml"


class FakeClient:
    def __init__(self, control: dict):
        occurrence = control["occurrence"]
        self.control = control
        self.issue = {
            "state": "closed",
            "state_reason": "completed",
            "body": f"<!-- administrative-candidate:{occurrence['occurrence_key']} -->",
        }
        self.pull = {
            "merged": True,
            "head": {"sha": occurrence["reviewed_head"]},
            "merge_commit_sha": occurrence["record_merge_commit"],
        }
        self.review = {
            "id": occurrence["independent_review"],
            "state": "APPROVED",
            "commit_id": occurrence["reviewed_head"],
            "user": {"login": "jimsteeg"},
            "author_association": "CONTRIBUTOR",
        }
        self.steward = {
            "id": occurrence["human_steward_disposition_comment"],
            "user": {"login": "fyremael"},
            "author_association": "CONTRIBUTOR",
            "body": (
                "AUTHORIZE_EXACT_HEAD_PROTECTED_MERGE__NO_OTHER_AUTHORITY\n"
                f"- occurrence: `{occurrence['occurrence_key']}`;\n"
                f"- PR: #{occurrence['candidate_pull_request']};\n"
                f"- exact candidate head: `{occurrence['reviewed_head']}`;\n"
                f"- protected main/base: `{occurrence['human_steward_bound_base']}`;\n"
                f"- independent non-author review: `jimsteeg`, `APPROVED`, review `{occurrence['independent_review']}`"
            ),
        }

    def get(self, path: str):
        occurrence = self.control["occurrence"]
        if path == f"/repos/grandchallenge/MATH-PROGRAMME/issues/{occurrence['candidate_issue']}":
            return self.issue
        if path == f"/repos/grandchallenge/MATH-PROGRAMME/pulls/{occurrence['candidate_pull_request']}":
            return self.pull
        if path == (
            f"/repos/grandchallenge/MATH-PROGRAMME/pulls/{occurrence['candidate_pull_request']}"
            "/reviews?per_page=100"
        ):
            return [self.review]
        if path == (
            f"/repos/grandchallenge/MATH-PROGRAMME/issues/{occurrence['candidate_issue']}"
            "/comments?per_page=100"
        ):
            return [self.steward]
        prefix = "/repos/grandchallenge/MATH-PROGRAMME/compare/"
        if path.startswith(prefix) and path.endswith("...main"):
            ancestor = path.removeprefix(prefix).removesuffix("...main")
            return {"merge_base_commit": {"sha": ancestor}}
        raise AssertionError(f"unexpected GET {path}")


class AdministrativeReview0813ReceiptRecoveryTests(unittest.TestCase):
    def load_control(self):
        return json.loads(CONTROL.read_text(encoding="utf-8"))

    def load_record(self):
        control = self.load_control()
        return json.loads((ROOT / control["occurrence"]["record_path"]).read_text(encoding="utf-8"))

    def load_manifest(self):
        control = self.load_control()
        return json.loads((ROOT / control["occurrence"]["manifest_path"]).read_text(encoding="utf-8"))

    def load_completion(self):
        return json.loads((ROOT / STATE_PATH).read_text(encoding="utf-8"))

    def predecessor_completion(self):
        control = self.load_control()
        prior = control["occurrence"]["expected_prior_frontier_utc"]
        current = copy.deepcopy(self.load_completion())
        procedure = current["procedures"]["administrative_review"]
        receipts = [
            item
            for item in procedure["receipts"]
            if item["scheduled_due_at"] <= prior
        ]
        self.assertTrue(receipts)
        self.assertEqual(max(item["scheduled_due_at"] for item in receipts), prior)
        procedure["receipts"] = receipts
        procedure["receipt_count"] = len(receipts)
        procedure["completed_through_utc"] = prior
        return current

    def raw_record(self, record=None):
        control = self.load_control()
        value = self.load_record() if record is None else record
        return {
            "sha": control["occurrence"]["record_blob_sha"],
            "content": base64.b64encode(json.dumps(value).encode("utf-8")).decode("ascii"),
        }

    def json_lookup(self, completion=None, manifest=None):
        control = self.load_control()
        current = self.predecessor_completion() if completion is None else completion
        source_manifest = self.load_manifest() if manifest is None else manifest

        def lookup(candidate, repo, path, ref):
            self.assertEqual(repo, "grandchallenge/MATH-PROGRAMME")
            self.assertEqual(ref, "main")
            if path == STATE_PATH:
                return copy.deepcopy(current)
            if path == control["occurrence"]["manifest_path"]:
                return copy.deepcopy(source_manifest)
            raise AssertionError(f"unexpected json_content path {path}")

        return lookup

    def target_receipt(self):
        return recovery._target_receipt(self.load_control(), self.load_record())

    def test_schema_and_authority_boundary(self):
        control = self.load_control()
        jsonschema.validate(control, json.loads(SCHEMA.read_text(encoding="utf-8")))
        occurrence = control["occurrence"]
        self.assertEqual(control["issue"], 554)
        self.assertEqual(occurrence["candidate_issue"], 475)
        self.assertEqual(occurrence["candidate_pull_request"], 476)
        self.assertEqual(occurrence["expected_prior_frontier_utc"], "2026-08-10T01:21:00Z")
        self.assertEqual(occurrence["expected_recovered_frontier_utc"], "2026-08-13T01:21:00Z")
        self.assertTrue(control["correction"]["ordinary_receipt_stage_required"])
        self.assertFalse(control["correction"]["issue_522_or_pr_523_execution_authorized"])
        self.assertTrue(control["authority_boundary"]["human_steward_exact_head_authorization_required"])
        self.assertFalse(control["authority_boundary"]["general_closed_issue_recovery_authority_created"])
        self.assertTrue(all(value is False for value in control["claim_boundaries"].values()))

    def test_exact_closed_target_is_re_admitted_before_other_closures(self):
        control = self.load_control()
        client = FakeClient(control)
        sentinel = [{"later": True}]
        with (
            patch.object(recovery, "json_content", side_effect=self.json_lookup()),
            patch.object(recovery, "content", return_value=self.raw_record()),
        ):
            result = recovery.pending_closures(
                client,
                "grandchallenge/MATH-PROGRAMME",
                {},
                "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: sentinel,
            )
        self.assertEqual(len(result), 1)
        self.assertNotEqual(result, sentinel)
        item = result[0]
        self.assertEqual(item["issue_number"], 475)
        self.assertEqual(item["pull_request"], 476)
        self.assertEqual(item["exact_head"], control["occurrence"]["reviewed_head"])
        self.assertEqual(item["record_merge_commit"], control["occurrence"]["record_merge_commit"])
        self.assertEqual(item["record_disposition_comment_id"], 5276363695)
        self.assertFalse(item["receipt_present"])

    def test_exact_receipt_present_makes_wrapper_transparent(self):
        control = self.load_control()
        client = FakeClient(control)
        completion = self.predecessor_completion()
        procedure = completion["procedures"]["administrative_review"]
        procedure["receipts"].append(self.target_receipt())
        procedure["receipts"].sort(key=lambda item: item["scheduled_due_at"])
        procedure["receipt_count"] = len(procedure["receipts"])
        procedure["completed_through_utc"] = control["occurrence"]["expected_recovered_frontier_utc"]
        sentinel = [{"later": True}]
        with (
            patch.object(recovery, "json_content", side_effect=self.json_lookup(completion=completion)),
            patch.object(recovery, "content", return_value=self.raw_record()),
        ):
            result = recovery.pending_closures(
                client,
                "grandchallenge/MATH-PROGRAMME",
                {},
                "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: sentinel,
            )
        self.assertEqual(result, sentinel)

    def test_predecessor_frontier_drift_fails_closed(self):
        control = self.load_control()
        client = FakeClient(control)
        completion = self.predecessor_completion()
        completion["procedures"]["administrative_review"]["completed_through_utc"] = "2026-08-11T01:21:00Z"
        with (
            patch.object(recovery, "json_content", side_effect=self.json_lookup(completion=completion)),
            patch.object(recovery, "content", return_value=self.raw_record()),
            self.assertRaisesRegex(AutonomyError, "predecessor frontier drift"),
        ):
            recovery.pending_closures(
                client,
                "grandchallenge/MATH-PROGRAMME",
                {},
                "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: [],
            )

    def test_protected_record_blob_and_identity_drift_fail_closed(self):
        control = self.load_control()
        client = FakeClient(control)
        bad_raw = self.raw_record()
        bad_raw["sha"] = "0" * 40
        with (
            patch.object(recovery, "json_content", side_effect=self.json_lookup()),
            patch.object(recovery, "content", return_value=bad_raw),
            self.assertRaisesRegex(AutonomyError, "record blob drift"),
        ):
            recovery.pending_closures(
                client, "grandchallenge/MATH-PROGRAMME", {}, "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: [],
            )

        record = self.load_record()
        record["record_id"] = "DRIFT"
        with (
            patch.object(recovery, "json_content", side_effect=self.json_lookup()),
            patch.object(recovery, "content", return_value=self.raw_record(record)),
            self.assertRaises(AutonomyError),
        ):
            recovery.pending_closures(
                client, "grandchallenge/MATH-PROGRAMME", {}, "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: [],
            )

    def test_pr_review_and_steward_mutations_fail_closed(self):
        control = self.load_control()
        for mutate, expected in (
            (lambda client: client.pull["head"].update({"sha": "0" * 40}), "protected PR identity drift"),
            (lambda client: client.review.update({"commit_id": "0" * 40}), "independent review drift"),
            (lambda client: client.steward.update({"author_association": "COLLABORATOR"}), "Human Steward disposition drift"),
            (lambda client: client.steward.update({"body": "wrong"}), "Human Steward disposition drift"),
        ):
            client = FakeClient(control)
            mutate(client)
            with (
                patch.object(recovery, "json_content", side_effect=self.json_lookup()),
                patch.object(recovery, "content", return_value=self.raw_record()),
                self.assertRaisesRegex(AutonomyError, expected),
            ):
                recovery.pending_closures(
                    client, "grandchallenge/MATH-PROGRAMME", {}, "github-actions[bot]",
                    base=lambda candidate, repo, runtime, referee: [],
                )

    def test_review_list_requires_exact_unique_review_id(self):
        control = self.load_control()
        client = FakeClient(control)
        client.review["id"] = int(control["occurrence"]["independent_review"]) + 1
        with (
            patch.object(recovery, "json_content", side_effect=self.json_lookup()),
            patch.object(recovery, "content", return_value=self.raw_record()),
            self.assertRaisesRegex(AutonomyError, "independent review identity drift"),
        ):
            recovery.pending_closures(
                client, "grandchallenge/MATH-PROGRAMME", {}, "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: [],
            )

        class DuplicateReviewClient(FakeClient):
            def get(self, path: str):
                occurrence = self.control["occurrence"]
                reviews_path = (
                    f"/repos/grandchallenge/MATH-PROGRAMME/pulls/{occurrence['candidate_pull_request']}"
                    "/reviews?per_page=100"
                )
                if path == reviews_path:
                    return [self.review, copy.deepcopy(self.review)]
                return super().get(path)

        duplicate = DuplicateReviewClient(control)
        with (
            patch.object(recovery, "json_content", side_effect=self.json_lookup()),
            patch.object(recovery, "content", return_value=self.raw_record()),
            self.assertRaisesRegex(AutonomyError, "independent review identity drift"),
        ):
            recovery.pending_closures(
                duplicate, "grandchallenge/MATH-PROGRAMME", {}, "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: [],
            )

    def test_ancestry_mutation_fails_closed(self):
        control = self.load_control()

        class BadAncestryClient(FakeClient):
            def get(self, path: str):
                if "/compare/" in path:
                    return {"merge_base_commit": {"sha": "0" * 40}}
                return super().get(path)

        with (
            patch.object(recovery, "json_content", side_effect=self.json_lookup()),
            patch.object(recovery, "content", return_value=self.raw_record()),
            self.assertRaisesRegex(AutonomyError, "ancestry failed"),
        ):
            recovery.pending_closures(
                BadAncestryClient(control),
                "grandchallenge/MATH-PROGRAMME",
                {},
                "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: [],
            )

    def test_ordinary_receipt_advance_changes_only_administrative_frontier(self):
        control = self.load_control()
        current = self.predecessor_completion()
        structural_before = copy.deepcopy(current["procedures"]["structural_sweep"])
        target = self.target_receipt()
        updated = advance_completion_state(
            current, target, control["occurrence"]["record_merge_commit"]
        )
        self.assertEqual(updated["procedures"]["structural_sweep"], structural_before)
        administrative = updated["procedures"]["administrative_review"]
        self.assertEqual(
            administrative["completed_through_utc"],
            control["occurrence"]["expected_recovered_frontier_utc"],
        )
        self.assertEqual(administrative["receipt_count"], 4)
        self.assertEqual(
            administrative["receipts"][-1]["scheduled_due_at"],
            "2026-08-13T01:21:00Z",
        )

    def test_prospective_aug13_receipt_tree_normalizes_to_predecessor_fixture(self):
        control = self.load_control()
        predecessor = self.predecessor_completion()
        prospective = advance_completion_state(
            predecessor,
            self.target_receipt(),
            control["occurrence"]["record_merge_commit"],
        )
        administrative = prospective["procedures"]["administrative_review"]
        self.assertEqual(administrative["receipt_count"], 4)
        self.assertEqual(
            administrative["completed_through_utc"],
            control["occurrence"]["expected_recovered_frontier_utc"],
        )
        with patch.object(self, "load_completion", return_value=prospective):
            normalized = self.predecessor_completion()
        normalized_administrative = normalized["procedures"]["administrative_review"]
        self.assertEqual(normalized_administrative["receipt_count"], 3)
        self.assertEqual(
            normalized_administrative["completed_through_utc"],
            control["occurrence"]["expected_prior_frontier_utc"],
        )
        self.assertNotIn(
            control["occurrence"]["expected_recovered_frontier_utc"],
            {item["scheduled_due_at"] for item in normalized_administrative["receipts"]},
        )

    def test_runtime_keeps_historical_aug13_overlay_non_effective_after_reactivation(self):
        text = RUNTIME_ENTRY.read_text(encoding="utf-8")
        self.assertIn("administrative_review_0813_receipt_pending_closures", text)
        for suspended in (
            "suspended_pending_closures",
            "suspended_stage_completion_receipt",
            "suspended_eligible_candidates",
        ):
            self.assertNotIn(suspended, text)
        self.assertNotIn("administrative_review_0813_receipt_recovery_eligible_candidates", text)
        self.assertNotIn("administrative_review_0813_receipt_advance_completion_state", text)
        self.assertNotIn("administrative_review_0813_receipt_wait_mirror_sync", text)

    def test_validation_workflow_runs_this_regression_module(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(
            "tests.test_administrative_autonomy_administrative_review_0813_receipt_recovery",
            text,
        )


if __name__ == "__main__":
    unittest.main()
