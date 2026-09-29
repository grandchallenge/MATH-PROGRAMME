import unittest

from ci.openmath_intake_pr_controller import (
    ControllerError,
    derive_dispatch_id,
    dispatch_base,
    dispatch_path,
    expected_paths,
)


class OpenMathIntakePrControllerTests(unittest.TestCase):
    def test_branch_maps_to_exact_dispatch(self) -> None:
        self.assertEqual(
            derive_dispatch_id("intake/openmath-om26-h2-wp01-ia-001"),
            "OM26-H2-WP01-IA-001",
        )

    def test_non_openmath_branch_is_rejected(self) -> None:
        with self.assertRaises(ControllerError):
            derive_dispatch_id("intake/nsci-c2-b-coop-001")

    def test_dispatch_paths_are_exact(self) -> None:
        dispatch_id = "OM26-H2-WP01-IA-001"
        self.assertEqual(
            dispatch_base(dispatch_id),
            "contributions/OPENMATH-2026/OM26-H2/WP01",
        )
        self.assertEqual(
            dispatch_path(dispatch_id),
            "contributions/OPENMATH-2026/OM26-H2/WP01/dispatches/OM26-H2-WP01-IA-001.json",
        )
        raw, receipt = expected_paths(dispatch_id, 5883655827)
        self.assertEqual(
            raw,
            "contributions/OPENMATH-2026/OM26-H2/WP01/raw/OM26-H2-WP01-IA-001/github-comment-5883655827.md",
        )
        self.assertEqual(
            receipt,
            "contributions/OPENMATH-2026/OM26-H2/WP01/receipts/OM26-H2-WP01-IA-001/github-comment-5883655827.json",
        )


if __name__ == "__main__":
    unittest.main()
