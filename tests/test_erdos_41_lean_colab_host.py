"""Host-side contract tests ensure the Lean launcher is a governed CI entrypoint."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from ci import erdos_41_lean_colab_host as host

class LeanColabHostTests(unittest.TestCase):
    def test_source_and_worker_are_locked(self):
        self.assertEqual(len(host.digest(host.SOURCE)),64)
        self.assertEqual(len(host.digest(host.WORKER)),64)
        self.assertEqual(host.TOOLCHAIN,"leanprover/lean4:v4.29.1")
    def test_download_and_cleanup(self):
        with tempfile.TemporaryDirectory() as td:
            calls=[]
            def record(argv,timeout=100):
                calls.append(argv)
                if "download" in argv:
                    Path(td,"receipt.json").write_text(json.dumps({"status":"RED"}))
            with patch.object(host,"cli",side_effect=record):
                host.launch("colab",Path(td))
            self.assertEqual([a[2] for a in calls],["new","upload","upload","exec","download","stop"])
    def test_stop_on_remote_failure(self):
        with tempfile.TemporaryDirectory() as td:
            operations=[]
            def record(argv,timeout=100):
                operations.append(argv[2])
                if argv[2]=="exec": raise RuntimeError("remote fail")
            with patch.object(host,"cli",side_effect=record):
                with self.assertRaisesRegex(RuntimeError,"remote fail"):
                    host.launch("colab",Path(td))
            self.assertEqual(operations[-1],"stop")
    def test_version_guard(self):
        self.assertEqual(host.TOOLCHAIN,"leanprover/lean4:v4.29.1")
if __name__=="__main__": unittest.main()
