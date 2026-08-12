from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import pr_visual_status_policy as policy  # noqa: E402


HEAD = "a" * 40
MERGE = "b" * 40


def base_report() -> dict:
    return {
        "report_id": "PRVSR-TEST-001",
        "identity": {
            "repository": "grandchallenge/MATH-PROGRAMME",
            "pr_number": 999,
            "title": "Synthetic governed test",
            "exact_head_sha": HEAD,
            "current_head_sha": HEAD,
        },
        "significance": policy.classify_significance(
            {"governance_or_control_plane": True}
        ),
        "authority": {
            "independent_review": {
                "required": True,
                "state": "APPROVED",
                "review_id": 1001,
                "actor": "independent-reviewer",
                "commit_sha": HEAD,
            },
            "human_steward": {
                "required": True,
                "state": "AUTHORIZED",
                "comment_id": 2001,
                "actor": "human-steward",
                "commit_sha": HEAD,
                "disposition": "HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
            },
        },
        "checks": [
            {
                "name": "Programme policy checks",
                "required": True,
                "status": "completed",
                "conclusion": "success",
                "run_id": 3001,
                "head_sha": HEAD,
            },
            {
                "name": "Optional diagnostic",
                "required": False,
                "status": "completed",
                "conclusion": "success",
                "run_id": 3002,
                "head_sha": HEAD,
            },
        ],
        "integration": {
            "merge_state": "OPEN",
            "merge_commit_sha": None,
            "protected_readback": {
                "required": True,
                "state": "PENDING",
                "main_sha": None,
            },
        },
        "blockers": [],
        "nonclaims": [
            "No programme-wide mandatory reporting authority.",
            "Visual status is derived and non-authoritative.",
        ],
        "history": [
            {
                "at": "2026-08-11T08:00:00Z",
                "event": "earlier-check",
                "outcome": "FAILURE_RETAINED_FOR_HISTORY",
            }
        ],
        "modules": {"governance": {"docket": 426}},
        "provenance": {"observed_at": "2026-08-11T09:00:00Z"},
    }


class PRVisualStatusPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report_schema = json.loads(
            (ROOT / "schemas" / "pr_visual_status_report.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.manifest_schema = json.loads(
            (
                ROOT / "schemas" / "pr_visual_status_pilot_manifest.schema.json"
            ).read_text(encoding="utf-8")
        )

    def test_sealed_report_validates_and_verifies(self) -> None:
        sealed = policy.seal_report(base_report())
        jsonschema.validate(sealed, self.report_schema)
        policy.verify_report(sealed)
        self.assertEqual(
            "AUTHORIZED_FOR_PROTECTED_MERGE",
            sealed["derived"]["operative_state"],
        )

    def test_pilot_manifest_validates_and_preserves_advisory_boundary(self) -> None:
        manifest = json.loads(
            (
                ROOT
                / "governance"
                / "pr_visual_status_reporting_pilot_manifest.json"
            ).read_text(encoding="utf-8")
        )
        jsonschema.validate(manifest, self.manifest_schema)
        self.assertTrue(manifest["enforcement"]["advisory_only"])
        self.assertFalse(manifest["enforcement"]["new_merge_gate"])
        self.assertFalse(manifest["evaluation"]["propagation_authority_created"])

    def test_stale_head_overrides_otherwise_green_state(self) -> None:
        report = base_report()
        report["identity"]["current_head_sha"] = "c" * 40
        sealed = policy.seal_report(report)
        self.assertEqual("STALE", sealed["derived"]["operative_state"])

    def test_unknown_current_head_fails_closed(self) -> None:
        report = base_report()
        report["identity"]["current_head_sha"] = None
        sealed = policy.seal_report(report)
        self.assertEqual("UNKNOWN", sealed["derived"]["operative_state"])

    def test_required_failure_cannot_be_masked_by_optional_success(self) -> None:
        report = base_report()
        report["checks"][0]["conclusion"] = "failure"
        sealed = policy.seal_report(report)
        self.assertEqual("BLOCKED", sealed["derived"]["operative_state"])

    def test_required_check_on_old_head_blocks(self) -> None:
        report = base_report()
        report["checks"][0]["head_sha"] = "d" * 40
        sealed = policy.seal_report(report)
        self.assertEqual("BLOCKED", sealed["derived"]["operative_state"])

    def test_old_head_review_blocks(self) -> None:
        report = base_report()
        report["authority"]["independent_review"]["commit_sha"] = "d" * 40
        sealed = policy.seal_report(report)
        self.assertEqual("BLOCKED", sealed["derived"]["operative_state"])

    def test_old_head_human_authorization_blocks(self) -> None:
        report = base_report()
        report["authority"]["human_steward"]["commit_sha"] = "d" * 40
        sealed = policy.seal_report(report)
        self.assertEqual("BLOCKED", sealed["derived"]["operative_state"])

    def test_changes_requested_is_distinct_state(self) -> None:
        report = base_report()
        report["authority"]["independent_review"]["state"] = "CHANGES_REQUESTED"
        sealed = policy.seal_report(report)
        self.assertEqual("CHANGES_REQUESTED", sealed["derived"]["operative_state"])

    def test_open_blocker_blocks(self) -> None:
        report = base_report()
        report["blockers"].append(
            {"id": "B-1", "status": "OPEN", "summary": "Synthetic blocker"}
        )
        sealed = policy.seal_report(report)
        self.assertEqual("BLOCKED", sealed["derived"]["operative_state"])

    def test_merged_without_required_readback_remains_pending(self) -> None:
        report = base_report()
        report["integration"]["merge_state"] = "MERGED"
        report["integration"]["merge_commit_sha"] = MERGE
        sealed = policy.seal_report(report)
        self.assertEqual(
            "MERGED_READBACK_PENDING",
            sealed["derived"]["operative_state"],
        )

    def test_readback_mismatch_blocks(self) -> None:
        report = base_report()
        report["integration"]["merge_state"] = "MERGED"
        report["integration"]["merge_commit_sha"] = MERGE
        report["integration"]["protected_readback"] = {
            "required": True,
            "state": "COMPLETE",
            "main_sha": "c" * 40,
        }
        sealed = policy.seal_report(report)
        self.assertEqual("BLOCKED", sealed["derived"]["operative_state"])

    def test_exact_protected_readback_completes(self) -> None:
        report = base_report()
        report["integration"]["merge_state"] = "MERGED"
        report["integration"]["merge_commit_sha"] = MERGE
        report["integration"]["protected_readback"] = {
            "required": True,
            "state": "COMPLETE",
            "main_sha": MERGE,
        }
        sealed = policy.seal_report(report)
        self.assertEqual("PROTECTED_COMPLETE", sealed["derived"]["operative_state"])

    def test_significance_profile_is_narrow_and_governable(self) -> None:
        ordinary = policy.classify_significance({})
        governed = policy.classify_significance(
            {"repository_policy_or_workflow": True}
        )
        manual = policy.classify_significance(
            {
                "manual_override": {
                    "enabled": True,
                    "authority": "Referee",
                    "reason": "Material cross-repository review risk",
                }
            }
        )
        self.assertFalse(ordinary["significant"])
        self.assertTrue(governed["significant"])
        self.assertTrue(manual["significant"])

    def test_manual_override_requires_governed_authority(self) -> None:
        with self.assertRaisesRegex(policy.ReportError, "governed authority"):
            policy.classify_significance(
                {
                    "manual_override": {
                        "enabled": True,
                        "authority": "random-bot",
                        "reason": "No authority",
                    }
                }
            )

    def test_renderer_is_deterministic_and_has_textual_equivalent(self) -> None:
        sealed = policy.seal_report(base_report())
        text_a = policy.render_text(sealed)
        text_b = policy.render_text(sealed)
        svg_a = policy.render_svg(sealed)
        svg_b = policy.render_svg(sealed)
        self.assertEqual(text_a, text_b)
        self.assertEqual(svg_a, svg_b)
        self.assertIn("AUTHORIZED_FOR_PROTECTED_MERGE", text_a)
        self.assertIn("AUTHORIZED_FOR_PROTECTED_MERGE", svg_a)
        self.assertIn("FAILURE_RETAINED_FOR_HISTORY", text_a)

    def test_svg_escapes_untrusted_title(self) -> None:
        report = base_report()
        report["identity"]["title"] = "<script>alert(1)</script>"
        sealed = policy.seal_report(report)
        svg = policy.render_svg(sealed)
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)

    def test_tampered_source_fails_digest_verification(self) -> None:
        sealed = policy.seal_report(base_report())
        sealed["identity"]["title"] = "tampered after sealing"
        with self.assertRaisesRegex(policy.ReportError, "digest mismatch"):
            policy.verify_report(sealed)

    def test_tampered_derived_state_fails_verification(self) -> None:
        sealed = policy.seal_report(base_report())
        sealed["derived"]["operative_state"] = "PROTECTED_COMPLETE"
        with self.assertRaisesRegex(policy.ReportError, "derived status"):
            policy.verify_report(sealed)


if __name__ == "__main__":
    unittest.main()
