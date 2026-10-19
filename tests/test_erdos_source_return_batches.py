"""Fail-closed contracts for bounded Erdős source-return reconciliation."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ci import erdos_catalogue_queue_projection as p
from ci import verify_erdos_source_return_batches as a


class BatchingTests(unittest.TestCase):
    def setUp(self):
        self.report = {"tasks": [], "receipts": []}
        for i in range(130):
            n, problem = 1000 + i, 100 + i
            task = f"ERDOS-CATALOGUE-{problem:04d}-S01"
            self.report["tasks"].append(
                {"issue_number": n, "task_id": task, "structurally_valid_returns": 1})
            self.report["receipts"].append({
                "issue_number": n, "problem_id": problem, "task_id": task,
                "comment_id": n + 100000, "validation": "STRUCTURALLY_VALID_UNADJUDICATED",
                "event_action": "snapshot", "comment_body_sha256": "f" * 64})
        self.digest = hashlib.sha256(json.dumps(self.report).encode()).hexdigest()
        self.manifest = p.source_batch_manifest(self.report, 64, self.digest)

    def make_batches(self, root):
        with patch.dict(os.environ, {"GITHUB_RUN_ID": "123", "GITHUB_SHA": "a" * 40}):
            for entry in self.manifest["include"]:
                idx = entry["index"]
                ids, scope = p.select_source_batch(self.report, size=64, index=idx)
                def fake(_, issue, dry):
                    return {"issue": issue, "comment_id": issue + 100000,
                            "target": "RETURNED", "verified_status": "RETURNED",
                            "verified_gcl_state": "RETURNED", "available_removed": True,
                            "gcl_state_before": "AVAILABLE"}
                path = root / f"gcl-source-return-batch-{idx}-123-1" / "projection.json"
                def test_write(path, record):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(record))
                with patch.object(p, "reconcile", side_effect=fake), \
                     patch.object(p, "persist_projection_receipt", side_effect=test_write):
                    receipt, code = p.project_source_returns(
                        self.report, ids, dry_run=False, receipt_path=path,
                        report_digest=self.digest, batch_scope=scope)
                self.assertEqual((code, receipt["status"]), (0, "VERIFIED_BATCH"))
        return root

    def check(self, root):
        return a.verify(self.report, report_digest=self.digest,
                        manifest=self.manifest, root=root,
                        run_id="123", run_attempt="1", protected_head="a" * 40)

    def test_exact_partitions_and_aggregate(self):
        self.assertEqual([len(p.select_source_batch(self.report, size=64, index=i)[0])
                          for i in range(3)], [64, 64, 2])
        with tempfile.TemporaryDirectory() as t:
            result = self.check(self.make_batches(Path(t)))
            self.assertTrue(result["verified"])
            self.assertEqual(result["verified_issue_count"], 130)
            self.assertEqual(result["returned_readbacks"], 130)

    def test_oversized_invalid_and_duplicate(self):
        for size in (0, -1, 65):
            with self.assertRaises(ValueError):
                p.source_batch_manifest(self.report, size, self.digest)
        with self.assertRaises(ValueError):
            p.select_source_batch(self.report, size=64, index=3)
        bad = dict(self.report, tasks=self.report["tasks"] + self.report["tasks"][:1])
        with self.assertRaises(ValueError):
            p.eligible_issue_ids(bad)

    def test_missing_batch_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            root = self.make_batches(Path(t))
            (root / "gcl-source-return-batch-2-123-1" / "projection.json").unlink()
            with self.assertRaises(ValueError):
                self.check(root)

    def test_partial_receipt_and_wrong_content_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            root = self.make_batches(Path(t))
            path = root / "gcl-source-return-batch-0-123-1" / "projection.json"
            original = json.loads(path.read_text())
            for change in (
                {"status": "RUNNING", "verified": False},
                {"protected_head": "b" * 40},
                {"report_sha256": "0" * 64},
                {"verified_returned": 65},
            ):
                row = dict(original, **change)
                path.write_text(json.dumps(row))
                with self.assertRaises(ValueError):
                    self.check(root)
            row = dict(original)
            row["results"][0]["comment_id"] = 1
            path.write_text(json.dumps(row))
            with self.assertRaises(ValueError):
                self.check(root)

    def test_zero_work_one_explicit_batch(self):
        report = {"tasks": [], "receipts": []}
        self.assertEqual(len(p.source_batch_manifest(report, 64, "x")["include"]), 1)
        self.assertEqual(p.select_source_batch(report, size=64, index=0)[0], [])


if __name__ == "__main__":
    unittest.main()
