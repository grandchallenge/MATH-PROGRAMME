from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import pr_visual_status_operational as operational  # noqa: E402
import pr_visual_status_policy as policy  # noqa: E402


HEAD = "a" * 40
OLD_HEAD = "b" * 40


class FakeClient:
    def __init__(self, responses: dict[str, object]):
        self.responses = responses

    def get(self, path: str):
        normalized = path.replace("&page=1", "").replace("?per_page=100", "")
        normalized = normalized.replace("&per_page=100", "")
        if normalized in self.responses:
            return self.responses[normalized]
        if path in self.responses:
            return self.responses[path]
        raise AssertionError(f"unexpected GET {path}")


class PRVisualStatusOperationalTests(unittest.TestCase):
    def test_phase1_config_is_repository_bounded_and_advisory(self) -> None:
        cfg = operational.load_config(ROOT / "governance" / "pr_visual_status_phase1.json")
        self.assertEqual("grandchallenge/MATH-PROGRAMME", cfg["repository"])
        self.assertEqual("1.0.0", cfg["significance_profile_version"])
        self.assertTrue(cfg["authority_boundary"]["advisory_only"])
        self.assertFalse(cfg["authority_boundary"]["new_merge_gate"])
        self.assertFalse(cfg["authority_boundary"]["cross_repository_propagation"])
        self.assertFalse(cfg["authority_boundary"]["human_performance_claims_authorized"])

    def test_significance_profile_selects_workflow_and_not_ordinary_docs(self) -> None:
        pr = {"body": "ordinary change"}
        workflow = operational.significance_signals(
            pr, [{"filename": ".github/workflows/example.yml"}], None
        )
        ordinary = operational.significance_signals(
            pr, [{"filename": "docs/ordinary-note.md"}], None
        )
        self.assertTrue(policy.classify_significance(workflow)["significant"])
        self.assertFalse(policy.classify_significance(ordinary)["significant"])

    def test_manual_override_is_governed_not_free_form(self) -> None:
        signals = operational.significance_signals(
            {"body": "ordinary"},
            [{"filename": "docs/ordinary-note.md"}],
            {"authority": "Council", "reason": "Material governance relevance"},
        )
        classified = policy.classify_significance(signals)
        self.assertTrue(classified["significant"])
        self.assertEqual("Council", classified["manual_override"]["authority"])

    def test_ruleset_requiredness_extracts_checks_and_review_requirement(self) -> None:
        contexts, review = operational.ruleset_requirements(
            [
                {
                    "rules": [
                        {
                            "type": "required_status_checks",
                            "parameters": {
                                "required_status_checks": [
                                    {"context": "Programme policy checks"},
                                    {"context": "GCL conformance"},
                                ]
                            },
                        },
                        {
                            "type": "pull_request",
                            "parameters": {"required_approving_review_count": 1},
                        },
                    ]
                }
            ]
        )
        self.assertEqual({"Programme policy checks", "GCL conformance"}, contexts)
        self.assertIs(review, True)

    def test_absent_pull_request_ruleset_does_not_claim_review_not_required(self) -> None:
        contexts, review = operational.ruleset_requirements(
            [
                {
                    "rules": [
                        {
                            "type": "required_status_checks",
                            "parameters": {
                                "required_status_checks": [
                                    {"context": "Programme policy checks"}
                                ]
                            },
                        }
                    ]
                }
            ]
        )
        self.assertEqual({"Programme policy checks"}, contexts)
        self.assertIsNone(review)

    def test_review_authority_ignores_old_head_approval(self) -> None:
        client = FakeClient(
            {
                "/repos/grandchallenge/MATH-PROGRAMME/pulls/99/reviews?": [
                    {
                        "id": 1,
                        "state": "APPROVED",
                        "commit_id": OLD_HEAD,
                        "submitted_at": "2026-08-12T00:00:00Z",
                        "user": {"login": "reviewer"},
                    }
                ]
            }
        )
        pr = {"number": 99, "head": {"sha": HEAD}, "user": {"login": "author"}}
        authority, observed = operational.review_authority(
            client, "grandchallenge/MATH-PROGRAMME", pr, True
        )
        self.assertEqual("PENDING", authority["state"])
        self.assertIsNone(authority["commit_sha"])
        self.assertEqual(OLD_HEAD, observed[0]["commit_sha"])

    def test_review_authority_accepts_current_non_author_review(self) -> None:
        client = FakeClient(
            {
                "/repos/grandchallenge/MATH-PROGRAMME/pulls/99/reviews?": [
                    {
                        "id": 2,
                        "state": "APPROVED",
                        "commit_id": HEAD,
                        "submitted_at": "2026-08-12T00:01:00Z",
                        "user": {"login": "reviewer"},
                    }
                ]
            }
        )
        pr = {"number": 99, "head": {"sha": HEAD}, "user": {"login": "author"}}
        authority, _ = operational.review_authority(
            client, "grandchallenge/MATH-PROGRAMME", pr, True
        )
        self.assertEqual("APPROVED", authority["state"])
        self.assertEqual(HEAD, authority["commit_sha"])

    def test_human_steward_authority_requires_configured_actor_and_exact_head(self) -> None:
        client = FakeClient(
            {
                "/repos/grandchallenge/MATH-PROGRAMME/issues/99/comments?": [
                    {
                        "id": 10,
                        "body": f"HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE\n{OLD_HEAD}",
                        "created_at": "2026-08-12T00:00:00Z",
                        "user": {"login": "fyremael"},
                    },
                    {
                        "id": 11,
                        "body": f"HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE\n{HEAD}",
                        "created_at": "2026-08-12T00:01:00Z",
                        "user": {"login": "not-steward"},
                    },
                ]
            }
        )
        pr = {"number": 99, "head": {"sha": HEAD}}
        authority, observed = operational.steward_authority(
            client,
            "grandchallenge/MATH-PROGRAMME",
            pr,
            {"human_steward_logins": ["fyremael"]},
        )
        self.assertEqual("UNKNOWN", authority["state"])
        self.assertEqual(2, len(observed))

    def test_human_steward_authority_accepts_exact_configured_actor(self) -> None:
        client = FakeClient(
            {
                "/repos/grandchallenge/MATH-PROGRAMME/issues/99/comments?": [
                    {
                        "id": 12,
                        "body": f"HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE\n{HEAD}",
                        "created_at": "2026-08-12T00:02:00Z",
                        "user": {"login": "fyremael"},
                    }
                ]
            }
        )
        pr = {"number": 99, "head": {"sha": HEAD}}
        authority, _ = operational.steward_authority(
            client,
            "grandchallenge/MATH-PROGRAMME",
            pr,
            {"human_steward_logins": ["fyremael"]},
        )
        self.assertEqual("AUTHORIZED", authority["state"])
        self.assertEqual(HEAD, authority["commit_sha"])
        self.assertEqual(12, authority["comment_id"])

    def test_cross_repository_collection_is_rejected_before_source_reads(self) -> None:
        with self.assertRaisesRegex(operational.OperationalError, "outside Phase 1 authority"):
            operational.collect_report(
                FakeClient({}),
                "grandchallenge/MATHFORGE",
                99,
                "2026-08-12T00:00:00Z",
                {
                    "repository": "grandchallenge/MATH-PROGRAMME",
                    "manual_override_path_template": "x/{pr_number}.json",
                },
            )

    def test_workflow_is_nonblocking_and_checks_out_trusted_base(self) -> None:
        workflow_path = ROOT / ".github" / "workflows" / "pr-visual-status-advisory.yml"
        text = workflow_path.read_text(encoding="utf-8")
        self.assertIn("pull_request_target:", text)
        self.assertIn("ref: main", text)
        self.assertIn("persist-credentials: false", text)
        self.assertIn("continue-on-error: true", text)
        self.assertIn("ADVISORY_FAILURE__NO_MERGE_BLOCKER_CREATED", text)
        self.assertNotIn("github.event.pull_request.head.sha", text)
        self.assertNotIn("MATHFORGE", text)
        self.assertNotIn("required_status_checks", text)


if __name__ == "__main__":
    unittest.main()
