from __future__ import annotations

import copy
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_autonomy_low_friction_persistent_sync as persistent


SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def low_namespace(*, synchronize, receipt):
    return SimpleNamespace(
        EXPECTED_REPOSITORY="grandchallenge/MATH-PROGRAMME",
        EXPECTED_REFEREE_LOGIN="github-actions[bot]",
        EXPECTED_CANDIDATE_LOGIN="gcl-release-trust[bot]",
        EXPECTED_BASE="main",
        SHA_RE=SHA_RE,
        synchronize_behind=synchronize,
        record_terminal_receipt=receipt,
    )


class FakeClient:
    def __init__(self, *, comments=None, commits=None):
        self.comments = copy.deepcopy(comments or [])
        self.commits = copy.deepcopy(commits or [])
        self.posts = []

    def get(self, path):
        if "/comments?per_page=100" in path:
            return copy.deepcopy(self.comments)
        if "/commits?per_page=100" in path:
            return copy.deepcopy(self.commits)
        raise AssertionError(f"unexpected GET {path}")

    def post(self, path, payload):
        self.posts.append((path, copy.deepcopy(payload)))
        item = {
            "id": 9001 + len(self.comments),
            "body": payload["body"],
            "user": {"login": "github-actions[bot]"},
        }
        self.comments.append(copy.deepcopy(item))
        return item


def sync_commit(previous="a" * 40, synchronized="c" * 40, base="b" * 40):
    return {
        "sha": synchronized,
        "author": {"login": "gcl-release-trust[bot]"},
        "commit": {
            "message": "Merge branch 'main' into routine/low-friction/qualification-persistent"
        },
        "parents": [{"sha": previous}, {"sha": base}],
    }


class PersistentSyncTests(unittest.TestCase):
    def test_history_recovers_sync_when_process_memory_is_empty(self):
        low = low_namespace(synchronize=lambda *args: None, receipt=lambda *args: None)
        referee = FakeClient(commits=[sync_commit()])
        events = persistent.persistent_sync_events(
            low,
            referee,
            7,
            "routine/low-friction/qualification-persistent",
        )
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["previous_head"], "a" * 40)
        self.assertEqual(events[0]["synchronized_head"], "c" * 40)
        self.assertEqual(events[0]["evidence_source"], "candidate_merge_commit")

    def test_synchronize_records_referee_evidence(self):
        event = {
            "previous_head": "a" * 40,
            "synchronized_head": "c" * 40,
            "expected_head_used": True,
        }

        def base_sync(candidate, observer, pull, control):
            return copy.deepcopy(event)

        low = low_namespace(synchronize=base_sync, receipt=lambda *args: None)
        persistent.install(low)
        referee = FakeClient(commits=[sync_commit()])
        pull = {
            "number": 7,
            "head": {"ref": "routine/low-friction/qualification-persistent"},
        }
        observed = low.synchronize_behind(object(), referee, pull, {})
        self.assertEqual(observed["evidence_comment_id"], 9001)
        self.assertEqual(len(referee.posts), 1)
        self.assertIn(persistent.SYNC_EVENT_PREFIX, referee.posts[0][1]["body"])

    def test_later_run_terminal_receipt_uses_persistent_history(self):
        captured = {}

        def base_receipt(
            referee,
            classification,
            disposition_id,
            checks,
            sync_events,
            readback,
            trace,
        ):
            captured["sync_events"] = copy.deepcopy(sync_events)
            return {"id": 77}

        low = low_namespace(synchronize=lambda *args: None, receipt=base_receipt)
        persistent.install(low)
        referee = FakeClient(commits=[sync_commit()])
        classification = SimpleNamespace(
            pr=7,
            branch="routine/low-friction/qualification-persistent",
        )
        result = low.record_terminal_receipt(
            referee,
            classification,
            12,
            {"policy": "success"},
            [],
            {"merge_sha": "d" * 40},
            SimpleNamespace(state="TERMINAL"),
        )
        self.assertEqual(result["id"], 77)
        self.assertEqual(len(captured["sync_events"]), 1)
        self.assertEqual(
            captured["sync_events"][0]["synchronized_head"],
            "c" * 40,
        )

    def test_comment_and_commit_evidence_are_deduplicated(self):
        previous = "a" * 40
        synchronized = "c" * 40
        comment = {
            "id": 42,
            "user": {"login": "github-actions[bot]"},
            "body": (
                f"{persistent.SYNC_EVENT_PREFIX}\n\n"
                f"- previous head: `{previous}`;\n"
                f"- synchronized head: `{synchronized}`;\n"
                "- expected-head update: `true`;"
            ),
        }
        low = low_namespace(synchronize=lambda *args: None, receipt=lambda *args: None)
        referee = FakeClient(comments=[comment], commits=[sync_commit()])
        events = persistent.persistent_sync_events(
            low,
            referee,
            7,
            "routine/low-friction/qualification-persistent",
        )
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["evidence_comment_id"], 42)
        self.assertEqual(events[0]["evidence_source"], "referee_comment")

    def test_install_is_idempotent(self):
        base_sync = lambda *args: {
            "previous_head": "a" * 40,
            "synchronized_head": "c" * 40,
            "expected_head_used": True,
        }
        base_receipt = lambda *args: {"id": 1}
        low = low_namespace(synchronize=base_sync, receipt=base_receipt)
        persistent.install(low)
        first_sync = low.synchronize_behind
        first_receipt = low.record_terminal_receipt
        persistent.install(low)
        self.assertIs(low.synchronize_behind, first_sync)
        self.assertIs(low.record_terminal_receipt, first_receipt)


if __name__ == "__main__":
    unittest.main()
