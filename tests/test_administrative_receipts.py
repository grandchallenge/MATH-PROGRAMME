from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_receipts as receipts

HEAD = "a" * 40
MERGE = "b" * 40
REVIEWED = "c" * 40


class AdministrativeReceiptTests(unittest.TestCase):
    @patch("administrative_receipts.subprocess.run")
    def test_pre_floor_record_is_skipped_before_git_inspection(self, run_mock) -> None:
        run_mock.return_value.returncode = 0
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "governance" / "records" / "old.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"status": "COMPLETE", "scheduled_due_at": "2026-07-31T00:00:00Z"}))
            config = {
                "procedures": {
                    "structural_sweep": {
                        "record_globs": ["governance/records/*.json"],
                        "due_fields": ["scheduled_due_at"],
                        "receipt_floor_utc": "2026-08-05T00:00:00Z",
                    }
                },
                "bootstrap_receipts": [],
            }

            def runner(args: list[str]) -> str:
                raise AssertionError(f"pre-floor record must not invoke git: {args}")

            state = receipts.derive_completion_state(root, config, HEAD, runner)
            self.assertEqual(state["procedures"]["structural_sweep"]["receipt_count"], 0)

    @patch("administrative_receipts.subprocess.run")
    def test_qualifying_record_uses_first_parent_merge_receipt(self, run_mock) -> None:
        run_mock.return_value.returncode = 0
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "governance" / "records" / "current.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"status": "COMPLETE", "scheduled_due_at": "2026-08-05T22:57:00Z"}))
            config = {
                "procedures": {
                    "structural_sweep": {
                        "record_globs": ["governance/records/*.json"],
                        "due_fields": ["scheduled_due_at"],
                        "receipt_floor_utc": "2026-08-05T00:00:00Z",
                    }
                },
                "bootstrap_receipts": [],
            }
            commands: list[list[str]] = []

            def runner(args: list[str]) -> str:
                commands.append(args)
                if args[0] == "log":
                    return MERGE
                if "--format=%P" in args:
                    return f"{'d' * 40} {REVIEWED}"
                if "--format=%B" in args:
                    return f"Merge PR #230\n\nProtected merge authorized by Human Steward at exact head {REVIEWED}.\n\nDisposition: HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE."
                raise AssertionError(args)

            state = receipts.derive_completion_state(root, config, HEAD, runner)
            log_command = commands[0]
            self.assertIn("--first-parent", log_command)
            self.assertIn(HEAD, log_command)
            item = state["procedures"]["structural_sweep"]["receipts"][0]
            self.assertEqual(item["merge_commit"], MERGE)
            self.assertEqual(item["reviewed_head"], REVIEWED)
            self.assertEqual(item["pull_request"], 230)


if __name__ == "__main__":
    unittest.main()
