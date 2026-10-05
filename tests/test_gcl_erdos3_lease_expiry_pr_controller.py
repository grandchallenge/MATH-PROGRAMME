import unittest

from ci.gcl_erdos3_lease_expiry_pr_controller import (
    BRANCH_RE,
    ControllerError,
    open_pr,
    parse_utc,
)


class GclErdos3LeaseExpiryPrControllerTests(unittest.TestCase):
    def test_exact_branch_identity(self) -> None:
        m = BRANCH_RE.fullmatch(
            "maintenance/gcl-erdos3-lease-expiry-gcl-erdos3-e3-v03-ia-004-e4"
        )
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "004")
        self.assertEqual(m.group(2), "4")

    def test_unregistered_branch_is_rejected_by_pattern(self) -> None:
        self.assertIsNone(
            BRANCH_RE.fullmatch(
                "maintenance/gcl-erdos3-lease-expiry-gcl-erdos3-e3-v02-ia-004-e4"
            )
        )

    def test_utc_parser_requires_z(self) -> None:
        with self.assertRaises(ControllerError):
            parse_utc("2026-10-04T16:38:54+00:00", "clock")

    def test_pr_creation_is_only_pull_request_post(self) -> None:
        class FakeGithub:
            def __init__(self):
                self.calls = []
            def request(self, method, path, payload=None):
                self.calls.append((method, path, payload))
                return {"number": 99, "html_url": "https://example.invalid/pr/99"}

        gh = FakeGithub()
        item = {
            "dispatch_id": "GCL-ERDOS3-E3-V03-IA-004",
            "lease_epoch": 4,
            "activation_comment_id": 5981972291,
            "lease_started_at": "2026-10-04T16:13:54Z",
            "lease_expires_at": "2026-10-04T16:38:54Z",
            "branch": "maintenance/gcl-erdos3-lease-expiry-gcl-erdos3-e3-v03-ia-004-e4",
        }
        pr = open_pr(gh, item)
        self.assertEqual(pr["number"], 99)
        self.assertEqual(len(gh.calls), 1)
        method, path, payload = gh.calls[0]
        self.assertEqual(method, "POST")
        self.assertEqual(path, "/repos/grandchallenge/MATHSOLVE/pulls")
        self.assertEqual(payload["head"], item["branch"])
        self.assertEqual(payload["base"], "main")
        self.assertIn("canonical claim effect: NONE", payload["body"])
        self.assertIn("frontier promotion effect: NONE", payload["body"])


if __name__ == "__main__":
    unittest.main()
