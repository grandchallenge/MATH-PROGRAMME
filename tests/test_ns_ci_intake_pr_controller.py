import unittest

from ci.ns_ci_intake_pr_controller import (
    ControllerError,
    derive_dispatch_id,
    expected_paths,
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

    def test_sha256_is_deterministic(self) -> None:
        self.assertEqual(
            sha256_text("evidence"),
            "eb2328a77c7b7a77bde2e1921b7c5544a3953ee5a0c80ec6bcb011d174b0a76f",
        )


if __name__ == "__main__":
    unittest.main()
