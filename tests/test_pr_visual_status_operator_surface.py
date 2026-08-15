from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import pr_visual_status_workflow_operator_surface as operator  # noqa: E402

ARCHIVE_SHA = "a" * 40
NEW_ARCHIVE_SHA = "b" * 40
HEAD = "c" * 40
SOURCE = "d" * 64


def entry(
    archive_sha: str = ARCHIVE_SHA,
    state: str = "AUTHORIZATION_PENDING",
    freshness: str = "CURRENT",
) -> dict:
    pr = 99
    branch = f"{operator.ARCHIVE_BRANCH_PREFIX}{pr}"
    archive_dir = (
        "governance/pr_visual_status_archive/grandchallenge/"
        "MATH-PROGRAMME/pr-99/PRVSR-TEST-99"
    )
    base = "https://github.com/grandchallenge/MATH-PROGRAMME"
    blob = f"{base}/blob/{branch}/{archive_dir}"
    return {
        "pr_number": pr,
        "title": "Synthetic operator entry",
        "pr_url": f"{base}/pull/{pr}",
        "exact_head_sha": HEAD,
        "operative_state": state,
        "freshness": freshness,
        "required_checks": {"successful": 6, "total": 6},
        "independent_review": {
            "required": True,
            "state": "APPROVED",
            "actor": "reviewer",
        },
        "human_steward": {
            "required": True,
            "state": "PENDING",
            "actor": None,
        },
        "integration": {"merge_state": "OPEN", "readback_state": "PENDING"},
        "open_blockers": 0,
        "report_id": "PRVSR-TEST-99",
        "observed_at": "2026-08-12T23:00:00Z",
        "source_snapshot_sha256": SOURCE,
        "archive_branch": branch,
        "archive_commit_sha": archive_sha,
        "archive_dir": archive_dir,
        "report_url": f"{blob}/report.svg",
        "text_url": f"{blob}/report.txt",
        "receipt_url": f"{blob}/receipt.json",
        "archive_url": f"{base}/tree/{branch}/{archive_dir}",
    }


def manifest(items: list[dict] | None = None) -> dict:
    values = sorted(
        items if items is not None else [entry()], key=lambda x: x["pr_number"]
    )
    return operator.seal_manifest(
        {
            "schema_version": operator.MANIFEST_SCHEMA_VERSION,
            "generator_version": operator.GENERATOR_VERSION,
            "repository": operator.ALLOWED_REPOSITORY,
            "as_of": max((item["observed_at"] for item in values), default=None),
            "entries": values,
            "errors": [],
            "authority_boundary": dict(operator.AUTHORITY_BOUNDARY),
        }
    )


class NoWriteClient:
    def post(self, *_args, **_kwargs):
        raise AssertionError("idempotent publication must not POST")

    def patch(self, *_args, **_kwargs):
        raise AssertionError("idempotent publication must not PATCH")


class PRVisualStatusOperatorSurfaceTests(unittest.TestCase):
    def test_manifest_is_deterministic_and_tampering_fails(self) -> None:
        first = manifest()
        self.assertEqual(first, manifest())
        self.assertEqual(first, operator.validate_manifest(first))
        first["entries"][0]["operative_state"] = "PROTECTED_COMPLETE"
        with self.assertRaisesRegex(operator.OperatorSurfaceError, "digest"):
            operator.validate_manifest(first)

    def test_stale_and_unknown_states_are_preserved_not_recast_green(self) -> None:
        stale = manifest([entry(state="STALE", freshness="STALE")])
        unknown = manifest([entry(state="UNKNOWN")])
        self.assertEqual(
            "STALE",
            operator.validate_manifest(stale)["entries"][0]["operative_state"],
        )
        self.assertEqual(
            "UNKNOWN",
            operator.validate_manifest(unknown)["entries"][0]["operative_state"],
        )

    def test_project_projection_is_inactive_and_permission_neutral(self) -> None:
        projection = operator.build_project_projection(manifest())
        self.assertFalse(projection["active"])
        boundary = projection["authority_boundary"]
        self.assertFalse(boundary["project_mutation_active"])
        self.assertFalse(boundary["project_write_permission_requested"])
        self.assertTrue(boundary["requires_separate_authorization_to_activate"])

    def test_cache_reuse_only_for_same_archive_tip(self) -> None:
        refs = [
            {
                "pr_number": 99,
                "archive_branch": f"{operator.ARCHIVE_BRANCH_PREFIX}99",
                "archive_commit_sha": ARCHIVE_SHA,
            }
        ]
        with (
            mock.patch.object(operator, "list_archive_refs", return_value=refs),
            mock.patch.object(
                operator, "_load_cached_manifest", return_value=manifest()
            ),
            mock.patch.object(operator, "_load_verified_bundle") as loader,
        ):
            result = operator.build_manifest(object(), operator.ALLOWED_REPOSITORY)
        loader.assert_not_called()
        self.assertEqual(ARCHIVE_SHA, result["entries"][0]["archive_commit_sha"])

    def test_changed_tip_reverifies_and_invalid_bundle_becomes_error(self) -> None:
        refs = [
            {
                "pr_number": 99,
                "archive_branch": f"{operator.ARCHIVE_BRANCH_PREFIX}99",
                "archive_commit_sha": NEW_ARCHIVE_SHA,
            }
        ]
        with (
            mock.patch.object(operator, "list_archive_refs", return_value=refs),
            mock.patch.object(
                operator, "_load_cached_manifest", return_value=manifest()
            ),
            mock.patch.object(
                operator,
                "_load_verified_bundle",
                side_effect=operator.OperatorSurfaceError("invalidated receipt"),
            ) as loader,
        ):
            result = operator.build_manifest(object(), operator.ALLOWED_REPOSITORY)
        loader.assert_called_once()
        self.assertEqual([], result["entries"])
        self.assertEqual(
            "UNVERIFIABLE_RETAINED_STATE", result["errors"][0]["code"]
        )

    def test_idempotent_publication_writes_nothing(self) -> None:
        value = manifest()
        projection = operator.build_project_projection(value)
        with (
            mock.patch.object(
                operator, "_ensure_index_branch", return_value=ARCHIVE_SHA
            ),
            mock.patch.object(
                operator,
                "_current_index_bytes",
                side_effect=[
                    operator.canonical_bytes(value),
                    operator.canonical_bytes(projection),
                ],
            ),
        ):
            result = operator.publish_index(
                NoWriteClient(), operator.ALLOWED_REPOSITORY, value, projection
            )
        self.assertFalse(result["changed"])
        self.assertEqual(ARCHIVE_SHA, result["commit_sha"])

    def test_workflow_and_page_keep_operator_surface_advisory(self) -> None:
        workflow = (
            ROOT / ".github" / "workflows" / "pr-visual-status-advisory.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("Refresh bounded PRVSR operator index", workflow)
        self.assertIn("id: operator-index", workflow)
        self.assertIn("continue-on-error: true", workflow)
        self.assertNotIn("permission-projects:", workflow)
        self.assertNotIn("permission-organization-projects:", workflow)

        page = (
            ROOT / "docs" / "operator" / "prvsr" / "index.html"
        ).read_text(encoding="utf-8")
        self.assertIn("prvsr-operator-index", page)
        self.assertIn("<noscript>", page)
        self.assertIn("Manifest unavailable", page)
        self.assertIn("derived, advisory", page)


if __name__ == "__main__":
    unittest.main()
