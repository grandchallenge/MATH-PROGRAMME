from pathlib import Path
import unittest

from ci.external_intake_evidence_admission import (
    ControllerError,
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


    def test_admission_script_write_surface_is_merge_only(self):
        text = Path("ci/external_intake_evidence_admission.py").read_text(
            encoding="utf-8"
        )
        self.assertEqual(text.count('"PUT"'), 1)
        self.assertIn(
            'f"/repos/{OWNER}/{REPO}/pulls/{pr_number}/merge"',
            text,
        )
        self.assertNotIn('"PATCH"', text)
        self.assertNotIn('"DELETE"', text)
        self.assertNotIn('"/contents/', text)
        self.assertNotIn('"/git/refs/', text)
        self.assertNotIn('"/git/commits', text)
        self.assertNotIn('"/git/trees', text)
        self.assertNotIn('"/git/blobs', text)

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
