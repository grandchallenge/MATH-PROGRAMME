"""Hostile tests for governed one-shot Colab allocation and receipt verification."""
import copy
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from ci import erdos_248_lean_colab_host as h

class Erdos248HostTests(unittest.TestCase):
    def identity(self):
        return {"source_sha256": "a"*64, "worker_sha256": "b"*64}

    def good(self):
        return {
          "schema": "GCL-ERDOS-248-LEAN-REPLAY/1",
          "job": h.JOB_ID, "toolchain": h.TOOLCHAIN,
          "external_commit": "8822f7ddef30fadbd92e1c6ab4ed897af356af5e",
          "mathlib_commit": "db584cd6d46c92f209a44c0f1c829460d327499d",
          "source_sha256": "a"*64, "worker_sha256": "b"*64,
          "status": "GREEN_KERNEL_REPLAY_UNADJUDICATED", "full_kernel_replay": True,
          "axioms_observed": True, "axiom_report": "axioms used: [propext]",
          "authority_effects": {
              "mathematical_certification": False, "publication": False,
              "protected_state_mutation": False, "source_adjudication": False},
          "steps": [{"stage": k, "exit_code": 0} for k in
                    ("git-fetch", "git-checkout", "lean-version",
                     "mathlib-cache", "lean-build", "axiom-audit")]
        }

    def test_valid_unaudjudicated_receipt(self):
        self.assertTrue(h.validate_receipt(self.good(), self.identity()))

    def test_red_or_forged_receipts_rejected(self):
        for mutate in (
            lambda d: d.update(status="RED"),
            lambda d: d.update(axioms_observed=False),
            lambda d: d.update(full_kernel_replay=False),
            lambda d: d["authority_effects"].update(mathematical_certification=True),
            lambda d: d.update(source_sha256="c"*64),
            lambda d: d.update(worker_sha256="c"*64),
            lambda d: d.update(axiom_report="axioms used: [sorryAx]"),
            lambda d: d["steps"].pop(),
            lambda d: d.update(mathlib_commit="0"*40)):
            data = copy.deepcopy(self.good())
            mutate(data)
            with self.assertRaises(ValueError):
                h.validate_receipt(data, self.identity())

    def test_failed_remote_exec_still_downloads_and_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            steps = []
            def record(argv, timeout=75):
                op = argv[2]
                steps.append(op)
                if op == "exec":
                    raise RuntimeError("red")
            with patch.object(h, "cli", side_effect=record):
                with self.assertRaisesRegex(RuntimeError, "red"):
                    h.launch("colab", Path(directory))
            self.assertEqual(steps, ["new", "upload", "upload", "exec",
                                      "download", "stop"])

    def test_success_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            actions = []
            with patch.object(h, "cli", side_effect=lambda argv, timeout=75:
                              actions.append(argv[2])):
                h.launch("colab", Path(directory))
            self.assertEqual(actions[-1], "stop")

    def test_queue_state_strict(self):
        rows = {"data": {"repository": {"issue": {
            "state": "OPEN", "labels": {"nodes": [
                {"name": "gcl-job"}, {"name": "gcl-state:available"},
                {"name": "gcl-role:verify"}]},
            "projectItems": {"nodes": [{"project": {"number": 2},
                "fieldValues": {"nodes": [
                    {"name": "Todo", "field": {"name": "Status"}},
                    {"name": "Mathematics", "field": {"name": "Queue Class"}}]}}]}}}}}
        import json
        class Response:
            returncode = 0
            stdout = json.dumps(rows)
            stderr = ""
        with patch.object(h.subprocess, "run", return_value=Response()):
            self.assertEqual(h.project_available()["project_fields"]["Status"], "Todo")
        rows["data"]["repository"]["issue"]["projectItems"]["nodes"][0][
          "fieldValues"]["nodes"][0]["name"] = "Done"
        Response.stdout = json.dumps(rows)
        with patch.object(h.subprocess, "run", return_value=Response()):
            with self.assertRaisesRegex(RuntimeError, "queue state changed"):
                h.project_available()

if __name__ == "__main__":
    unittest.main()
