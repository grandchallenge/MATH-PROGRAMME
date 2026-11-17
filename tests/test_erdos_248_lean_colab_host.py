"""Hostile tests for governed one-shot Colab allocation and receipt verification."""
import copy
import hashlib
import tarfile
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from ci import erdos_248_lean_colab_host as h
from colab import erdos_248_lean_worker as w

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
          "theorem_type_observed": True, "theorem_audit_log_sha256": "f"*64,
          "log_archive_sha256": "f"*64,
          "source_mode": "PINNED_PROVIDER_WITH_DECLARED_COMPATIBILITY_PATCHES",
          "compatibility_patch_plan": [
              {"dependency": d, "patch": n, "git_blob": blob}
              for d, n, blob in w.COMPATIBILITY_PATCHES
          ],
          "compatibility_patch_effects": {
              d: {"commit": sha, "modified_files": (
                  ["BoundedGaps/BoundedGaps/Maynard/FaceDecomposition.lean",
                   "BoundedGaps/BoundedGaps/Maynard/ImprovedGPY/S2Pair.lean"]
                  if d == "BoundedGaps" else ["Example.lean"])}
              for d, sha in w.PINNED_DEPENDENCIES.items()
          },
          "authority_effects": {
              "mathematical_certification": False, "publication": False,
              "protected_state_mutation": False, "source_adjudication": False},
          "steps": [{"stage": k, "exit_code": 0} for k in
                    ("git-fetch", "git-checkout", "lean-version",
                     "mathlib-cache", "compat-post-update", "lean-build", "axiom-audit") +
                    tuple(f"compat-{i:02d}-{a}" for i in range(9)
                          for a in ("check", "apply"))]
        }

    def test_lean_four_axiom_receipt(self):
        report = self.good()
        report["axiom_report"] = "'Erdos248.erdos_248' depends on axioms: [propext]"
        self.assertTrue(h.validate_receipt(report, self.identity()))

    def test_valid_unaudjudicated_receipt(self):
        self.assertTrue(h.validate_receipt(self.good(), self.identity()))

    def test_red_or_forged_receipts_rejected(self):
        for mutate in (
            lambda d: d.update(status="RED"),
            lambda d: d.update(axioms_observed=False),
            lambda d: d.update(theorem_type_observed=False),
            lambda d: d.update(log_archive_sha256=None),
            lambda d: d.update(source_mode="PINNED_UNPATCHED"),
            lambda d: d["compatibility_patch_plan"].pop(),
            lambda d: d["compatibility_patch_effects"]["BoundedGaps"].update(
                commit="0"*40),
            lambda d: d["compatibility_patch_effects"]["BoundedGaps"].update(
                modified_files=["Other.lean"]),
            lambda d: d.update(full_kernel_replay=False),
            lambda d: d["authority_effects"].update(mathematical_certification=True),
            lambda d: d.update(source_sha256="c"*64),
            lambda d: d.update(worker_sha256="c"*64),
            lambda d: d.update(axiom_report="axioms used: [sorryAx]"),
            lambda d: d["steps"].pop(),
            lambda d: d["steps"].__setitem__(
                slice(None), [s for s in d["steps"]
                              if s["stage"] != "compat-05-apply"]),
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
                                      "download", "download", "stop"])

    def test_success_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            actions = []
            with patch.object(h, "cli", side_effect=lambda argv, timeout=75:
                              actions.append(argv[2])):
                h.launch("colab", Path(directory))
            self.assertEqual(actions[-1], "stop")

    def test_registered_runtime_budget_drift_rejected(self):
        import json
        self.assertEqual(h.MAX_RUNTIME_SECONDS, 15000)
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "JOBS.json"
            p.write_text(json.dumps({"jobs": [{
                "id": h.JOB_ID, "review_issue": h.ISSUE, "problem_id": 248,
                "toolchain": h.TOOLCHAIN,
                "authority": "UNADJUDICATED_COMPUTATIONAL_EVIDENCE_ONLY",
                "accelerator": "CPU",
                "launcher": "ci.erdos_248_lean_colab_host",
                "max_runtime_seconds": 4500
            }]}))
            with patch.object(h, "REGISTRY", p):
                with self.assertRaisesRegex(ValueError, "CPU runtime budget mismatch"):
                    h.registered_identity()

    def test_colab_exec_timeout_matches_protected_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            calls = []
            def record(argv, timeout=75):
                calls.append((argv, timeout))
            with patch.object(h, "cli", side_effect=record):
                h.launch("colab", Path(directory))
            exact = [(argv, duration) for argv, duration in calls if argv[2] == "exec"]
            self.assertEqual(len(exact), 1)
            argv, duration = exact[0]
            self.assertEqual(argv[argv.index("--timeout") + 1], "15000")
            self.assertEqual(duration, 15200)
            self.assertEqual(calls[-1][0][2], "stop")

    def test_archive_log_digest_check(self):
        import io
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = self.good()
            report["steps"] = [
                {"stage": "axiom-audit", "exit_code": 0,
                 "stdout_sha256": hashlib.sha256(b"checked").hexdigest(),
                 "stderr_sha256": hashlib.sha256(b"").hexdigest()}
            ]
            audit = b"import ErdosProblems.Erdos248"
            report["audit_source_sha256"] = hashlib.sha256(audit).hexdigest()
            archive = root / "logs.tar.gz"
            with tarfile.open(archive, mode="w:gz") as tar:
                for name, data in (("logs/axiom-audit.out", b"checked"),
                                   ("logs/axiom-audit.err", b""),
                                   ("Erdos248ReplayAudit.lean", audit)):
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    tar.addfile(info, io.BytesIO(data))
            report["log_archive_sha256"] = h.digest(archive)
            report["log_archive_bytes"] = archive.stat().st_size
            self.assertTrue(h.validate_log_archive(report, archive))
            report["steps"][0]["stdout_sha256"] = "0"*64
            with self.assertRaisesRegex(ValueError, "digest mismatch"):
                h.validate_log_archive(report, archive)

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
