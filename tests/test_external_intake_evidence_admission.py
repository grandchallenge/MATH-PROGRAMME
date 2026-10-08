from pathlib import Path
import unittest

from ci.external_intake_evidence_admission import (
    ControllerError,
    exact_clerk_approval_exists,
    merge_protected,
    validate_pr_binding,
)


class FakeGithub:
    def __init__(self):
        self.calls = []

    def request(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        if method == "GET" and path.endswith(
            "/git/ref/heads/intake/erdos-593-r1-ia-001"
        ):
            return {
                "object": {
                    "sha": "d041809826dfb92a4baf15607e62d6b7b65d9ee3"
                }
            }
        if method == "GET" and path == "/repos/grandchallenge/MATHSOLVE/pulls/919/reviews?per_page=100":
            return [
                {
                    "user": {"login": "gcl-council-clerk[bot]"},
                    "state": "APPROVED",
                    "commit_id": "d041809826dfb92a4baf15607e62d6b7b65d9ee3",
                }
            ]
        if method == "PUT" and path == "/repos/grandchallenge/MATHSOLVE/pulls/919/merge":
            return {"merged": True, "sha": "a" * 40, "message": "Pull Request successfully merged"}
        raise AssertionError((method, path, payload))


def candidate():
    return {
        "campaign": "ERDOS-OPEN-RECON",
        "dispatch_id": "ERDOS-593-R1-IA-001",
        "branch": "intake/erdos-593-r1-ia-001",
    }


def pull_request(**updates):
    value = {
        "number": 919,
        "node_id": "PR_node_919",
        "state": "open",
        "draft": False,
        "mergeable": True,
        "title": "ERDOS-OPEN intake: ERDOS-593-R1-IA-001",
        "user": {"login": "gcl-release-trust[bot]"},
        "base": {"ref": "main"},
        "head": {
            "ref": "intake/erdos-593-r1-ia-001",
            "sha": "d041809826dfb92a4baf15607e62d6b7b65d9ee3",
        },
    }
    value.update(updates)
    return value


class ExternalIntakeEvidenceAdmissionTests(unittest.TestCase):
    def test_exact_release_trust_pr_binding_is_accepted(self):
        gh = FakeGithub()
        result = validate_pr_binding(gh, candidate(), pull_request())
        self.assertEqual(result["pr_number"], 919)
        self.assertEqual(
            result["head_sha"],
            "d041809826dfb92a4baf15607e62d6b7b65d9ee3",
        )
        self.assertEqual(result["author"], "gcl-release-trust[bot]")

    def test_non_release_trust_author_is_rejected(self):
        gh = FakeGithub()
        with self.assertRaisesRegex(ControllerError, "author mismatch"):
            validate_pr_binding(
                gh,
                candidate(),
                pull_request(user={"login": "untrusted-user"}),
            )

    def test_head_sha_must_match_live_branch(self):
        gh = FakeGithub()
        with self.assertRaisesRegex(ControllerError, "head moved"):
            validate_pr_binding(
                gh,
                candidate(),
                pull_request(
                    head={
                        "ref": "intake/erdos-593-r1-ia-001",
                        "sha": "0" * 40,
                    }
                ),
            )

    def test_non_main_base_is_rejected(self):
        gh = FakeGithub()
        with self.assertRaisesRegex(ControllerError, "base is not main"):
            validate_pr_binding(
                gh,
                candidate(),
                pull_request(base={"ref": "other"}),
            )


    def test_exact_head_clerk_approval_is_required_and_detected(self):
        gh = FakeGithub()
        self.assertTrue(
            exact_clerk_approval_exists(
                gh,
                919,
                "d041809826dfb92a4baf15607e62d6b7b65d9ee3",
            )
        )

    def test_wrong_head_clerk_approval_is_not_accepted(self):
        gh = FakeGithub()
        self.assertFalse(
            exact_clerk_approval_exists(
                gh,
                919,
                "0" * 40,
            )
        )

    def test_admission_script_has_only_the_exact_merge_write_surface(self):
        """Guard the bounded contents-write credential against direct API writes."""
        source = Path("ci/external_intake_evidence_admission.py").read_text(
            encoding="utf-8"
        )
        self.assertEqual(source.count('"PUT"'), 1)
        self.assertIn(
            'f"/repos/{OWNER}/{REPO}/pulls/{pr_number}/merge"',
            source,
        )
        for forbidden in (
            '"POST"',
            '"PATCH"',
            '"DELETE"',
            '"/contents/',
            '"/git/refs/',
            '"/git/commits',
            '"/git/trees',
            '"/git/blobs',
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_protected_merge_is_expected_head_locked_and_squash_only(self):
        gh = FakeGithub()
        result = merge_protected(
            gh,
            919,
            "d041809826dfb92a4baf15607e62d6b7b65d9ee3",
            "ERDOS-593-R1-IA-001",
        )
        self.assertTrue(result["merged"])
        method, path, payload = gh.calls[-1]
        self.assertEqual(
            (method, path),
            ("PUT", "/repos/grandchallenge/MATHSOLVE/pulls/919/merge"),
        )
        self.assertEqual(
            payload["sha"],
            "d041809826dfb92a4baf15607e62d6b7b65d9ee3",
        )
        self.assertEqual(payload["merge_method"], "squash")
        self.assertNotIn("admin", str(payload).lower())


if __name__ == "__main__":
    unittest.main()
