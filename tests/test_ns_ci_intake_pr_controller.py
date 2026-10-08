import unittest

from ci.ns_ci_intake_pr_controller import (
    ControllerError,
    derive_dispatch_id,
    expected_paths,
    list_intake_branches,
    main_has_any_raw,
    profile_for_dispatch,
    sha256_text,
)


class ExternalIntakePrControllerTests(unittest.TestCase):
    def test_ns_branch_maps_to_exact_dispatch(self) -> None:
        self.assertEqual(
            derive_dispatch_id("intake/nsci-c2-b-coop-001"),
            "NSCI-C2-B-COOP-001",
        )

    def test_uc_branch_maps_to_exact_dispatch(self) -> None:
        self.assertEqual(
            derive_dispatch_id("intake/uc-wp08-d004-wp01-ia-001"),
            "UC-WP08-D004-WP01-IA-001",
        )

    def test_erdos_branch_maps_to_exact_dispatch(self) -> None:
        self.assertEqual(
            derive_dispatch_id("intake/erdos-593-r1-ia-001"),
            "ERDOS-593-R1-IA-001",
        )

    def test_non_dispatch_branch_is_rejected(self) -> None:
        with self.assertRaises(ControllerError):
            derive_dispatch_id("intake/not-a-dispatch")

    def test_ns_comment_paths_are_dispatch_bound(self) -> None:
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

    def test_uc_comment_paths_are_dispatch_bound(self) -> None:
        raw, receipt = expected_paths("UC-WP08-D004-WP03-IA-001", 24680)
        self.assertEqual(
            raw,
            "contributions/UC-001/WP08_D004_INCIDENCE_INTERFACE/"
            "raw/UC-WP08-D004-WP03-IA-001/github-comment-24680.md",
        )
        self.assertEqual(
            receipt,
            "contributions/UC-001/WP08_D004_INCIDENCE_INTERFACE/"
            "receipts/UC-WP08-D004-WP03-IA-001/github-comment-24680.json",
        )

    def test_erdos_comment_paths_are_dispatch_bound(self) -> None:
        raw, receipt = expected_paths("ERDOS-593-R1-IA-001", 6005661923)
        self.assertEqual(
            raw,
            "contributions/ERDOS-OPEN-001/RECON_TRANCHE_001/"
            "raw/ERDOS-593-R1-IA-001/github-comment-6005661923.md",
        )
        self.assertEqual(
            receipt,
            "contributions/ERDOS-OPEN-001/RECON_TRANCHE_001/"
            "receipts/ERDOS-593-R1-IA-001/github-comment-6005661923.json",
        )

    def test_registered_profile_schema_versions_are_explicit(self) -> None:
        self.assertEqual(
            profile_for_dispatch("NSCI-C2-B-COOP-001").receipt_schema_version,
            "0.2-pilot",
        )
        self.assertEqual(
            profile_for_dispatch("UC-WP08-D004-WP05-IA-001").receipt_schema_version,
            "1.0.0",
        )
        self.assertEqual(
            profile_for_dispatch("ERDOS-1052-S1-IA-001").receipt_schema_version,
            "1.0.0",
        )

    def test_discovers_evidence_branch_before_any_pr_exists(self) -> None:
        class FakeGithub:
            def request(self, method, path):
                self.assert_method = method
                if "/branches?" in path:
                    return [
                        {"name": "intake/gcl-e2e-canary-003-ia-001"},
                        {"name": "intake/unregistered-branch"},
                        {"name": "main"},
                    ]
                if "/pulls?" in path:
                    return []
                raise AssertionError(path)

        self.assertEqual(
            list_intake_branches(FakeGithub()),
            ["intake/gcl-e2e-canary-003-ia-001"],
        )

    def test_branch_discovery_paginates_and_deduplicates(self) -> None:
        class FakeGithub:
            def request(self, method, path):
                if "/branches?" in path:
                    if "&page=1" in path:
                        return [{"name": "unrelated-" + str(i)} for i in range(100)]
                    if "&page=2" in path:
                        return [{"name": "intake/gcl-e2e-canary-003-ia-001"}]
                    return []
                if "/pulls?" in path:
                    return [{"head": {"ref": "intake/gcl-e2e-canary-003-ia-001"}}]
                raise AssertionError(path)

        self.assertEqual(
            list_intake_branches(FakeGithub()),
            ["intake/gcl-e2e-canary-003-ia-001"],
        )

    def test_branch_discovery_fails_closed_on_malformed_listing(self) -> None:
        class FakeGithub:
            def request(self, method, path):
                return {"unexpected": "value"} if "/branches?" in path else []

        with self.assertRaises(ControllerError):
            list_intake_branches(FakeGithub())

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

    def test_uc_dispatch_level_first_result_lock_uses_uc_root(self) -> None:
        class FakeGithub:
            def get_optional(self, path):
                self.last_path = path
                return [{"name": "github-comment-222.md"}]

        gh = FakeGithub()
        self.assertTrue(main_has_any_raw(gh, "UC-WP08-D004-WP02-IA-001"))
        self.assertIn(
            "contributions/UC-001/WP08_D004_INCIDENCE_INTERFACE/raw/"
            "UC-WP08-D004-WP02-IA-001",
            gh.last_path,
        )

    def test_erdos_dispatch_level_first_result_lock_uses_erdos_root(self) -> None:
        class FakeGithub:
            def get_optional(self, path):
                self.last_path = path
                return [{"name": "github-comment-6005661923.md"}]

        gh = FakeGithub()
        self.assertTrue(main_has_any_raw(gh, "ERDOS-593-R1-IA-001"))
        self.assertIn(
            "contributions/ERDOS-OPEN-001/RECON_TRANCHE_001/raw/"
            "ERDOS-593-R1-IA-001",
            gh.last_path,
        )

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
