from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import pr_visual_status_policy as policy  # noqa: E402
import pr_visual_status_transport as transport  # noqa: E402


HEAD = "a" * 40


def base_report() -> dict:
    report = {
        "report_id": "PRVSR-ARCHIVE-TEST-001",
        "identity": {
            "repository": "grandchallenge/MATH-PROGRAMME",
            "pr_number": 999,
            "title": "Synthetic archive transport test",
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
            }
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
    return policy.seal_report(report)


class PRVisualStatusTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "pr_visual_status_archive_receipt.schema.json"
            ).read_text(encoding="utf-8")
        )

    def test_archive_bundle_is_deterministic_and_schema_valid(self) -> None:
        report = base_report()
        first = transport.build_archive_bundle(
            report,
            target_head_before=HEAD,
            target_head_after=HEAD,
        )
        second = transport.build_archive_bundle(
            report,
            target_head_before=HEAD,
            target_head_after=HEAD,
        )
        self.assertEqual(first, second)
        receipt = json.loads(first["receipt.json"])
        jsonschema.validate(receipt, self.receipt_schema)
        self.assertFalse(receipt["target_pr_head_mutated"])
        self.assertTrue(receipt["authority_boundary"]["advisory_only"])
        self.assertFalse(receipt["authority_boundary"]["new_merge_gate"])

    def test_archive_writes_json_text_svg_and_receipt(self) -> None:
        report = base_report()
        with tempfile.TemporaryDirectory() as tmp:
            bundle_dir = transport.write_archive_bundle(
                report,
                Path(tmp),
                target_head_before=HEAD,
                target_head_after=HEAD,
            )
            self.assertEqual(
                {"report.json", "report.txt", "report.svg", "receipt.json"},
                {path.name for path in bundle_dir.iterdir()},
            )
            receipt = transport.verify_archive_bundle(bundle_dir)
            self.assertEqual(report["report_id"], receipt["report_id"])

    def test_target_head_movement_fails_closed(self) -> None:
        with self.assertRaisesRegex(transport.TransportError, "changed during"):
            transport.build_archive_bundle(
                base_report(),
                target_head_before=HEAD,
                target_head_after="b" * 40,
            )

    def test_wrong_before_head_fails_closed(self) -> None:
        with self.assertRaisesRegex(transport.TransportError, "before transport"):
            transport.build_archive_bundle(
                base_report(),
                target_head_before="b" * 40,
                target_head_after="b" * 40,
            )

    def test_stale_report_is_retained_as_stale_not_recast_green(self) -> None:
        report = base_report()
        unsealed = json.loads(json.dumps(report))
        unsealed["identity"]["current_head_sha"] = "c" * 40
        unsealed.pop("derived")
        unsealed["provenance"] = {"observed_at": "2026-08-11T09:05:00Z"}
        stale = policy.seal_report(unsealed)
        self.assertEqual("STALE", stale["derived"]["operative_state"])
        bundle = transport.build_archive_bundle(
            stale,
            target_head_before=HEAD,
            target_head_after=HEAD,
        )
        receipt = json.loads(bundle["receipt.json"])
        self.assertEqual("STALE", receipt["operative_state"])
        self.assertEqual("STALE", receipt["freshness"])

    def test_transport_comment_uses_full_sha_digest_and_advisory_boundary(self) -> None:
        bundle = transport.build_archive_bundle(
            base_report(),
            target_head_before=HEAD,
            target_head_after=HEAD,
        )
        receipt = json.loads(bundle["receipt.json"])
        comment = transport.render_pr_comment(receipt)
        self.assertIn(HEAD, comment)
        self.assertIn(receipt["source_snapshot_sha256"], comment)
        self.assertIn(receipt["archive_dir"], comment)
        self.assertIn("derived, advisory", comment)
        self.assertIn("target PR head was not modified", comment)

    def test_tampered_artifact_fails_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle_dir = transport.write_archive_bundle(
                base_report(),
                Path(tmp),
                target_head_before=HEAD,
                target_head_after=HEAD,
            )
            (bundle_dir / "report.txt").write_text("tampered\n", encoding="utf-8")
            with self.assertRaisesRegex(transport.TransportError, "digest mismatch"):
                transport.verify_archive_bundle(bundle_dir)

    def test_unsafe_report_id_cannot_escape_archive_root(self) -> None:
        report = base_report()
        unsealed = json.loads(json.dumps(report))
        unsealed["report_id"] = "../../escape"
        unsealed.pop("derived")
        unsealed["provenance"] = {"observed_at": "2026-08-11T09:10:00Z"}
        sealed = policy.seal_report(unsealed)
        with self.assertRaisesRegex(transport.TransportError, "unsafe path"):
            transport.archive_relative_dir(sealed)

    def test_receipt_tampering_of_non_mutating_invariant_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle_dir = transport.write_archive_bundle(
                base_report(),
                Path(tmp),
                target_head_before=HEAD,
                target_head_after=HEAD,
            )
            receipt_path = bundle_dir / "receipt.json"
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["target_pr_head_mutated"] = True
            receipt_path.write_text(
                json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                transport.TransportError, "non-mutating target invariant"
            ):
                transport.verify_archive_bundle(bundle_dir)


if __name__ == "__main__":
    unittest.main()
