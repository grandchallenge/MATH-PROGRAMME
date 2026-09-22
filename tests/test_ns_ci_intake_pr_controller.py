import unittest

from ci.ns_ci_intake_pr_controller import (
    ControllerError,
    derive_dispatch_id,
    expected_paths,
    main_has_any_raw,
    sha256_text,
)


class NsCiIntakePrControllerTests(unittest.TestCase):
    def test_branch_maps_to_exact_dispatch(self) -> None:
        self.assertEqual(
            derive_dispatch_id("intake/nsci-c2-b-coop-001"),
            "NSCI-C2-B-COOP-001",
        )

    def test_non_dispatch_branch_is_rejected(self) -> None:
        with self.assertRaises(ControllerError):
            derive_dispatch_id("intake/not-a-dispatch")

    def test_comment_paths_are_dispatch_bound(self) -> None:
        raw, receipt = expected_paths("NSCI-C2-B-COOP-001", 12345)
        self.assertEqual(
            raw,
            "contributions/NS-CI-001/C2_MIX_DIRECTION_COMPRESSION_LEDGER_CHARGE/"
            "raw/NSCI-C2-B-COOP-001/github-comment-12345.md",
        )
        self.assertEqual(
            receipt,
            "contributions/NS-CI-001/C2_MIX_DIRECTION_COMPRESSION_LEDGER_CHARGE/"
            "receipts/NSCI-C2-B-COOP-001/github-comment-12345.json",
        )

    def test_dispatch_level_first_result_lock_detects_any_protected_raw(self) -> None:
        class FakeGithub:
            def get_optional(self, path):
                self.last_path = path
                return [
                    {"name": "github-comment-111.md"},
                    {"name": "other.txt"},
                ]

        gh = FakeGithub()
        self.assertTrue(main_has_any_raw(gh, "NSCI-C2-B-COOP-001"))
        self.assertIn("raw/NSCI-C2-B-COOP-001", gh.last_path)

    def test_dispatch_level_first_result_lock_allows_empty_directory(self) -> None:
        class FakeGithub:
            def get_optional(self, path):
                return None

        self.assertFalse(main_has_any_raw(FakeGithub(), "NSCI-C2-A-BLIND-001"))

    def test_sha256_is_deterministic(self) -> None:
        self.assertEqual(
            sha256_text("evidence"),
            "ee8250fb76e094b34b471f13a73dbbe51d1ae142e9df59d7c0d31ec20f0a0a8e",
        )


if __name__ == "__main__":
    unittest.main()
