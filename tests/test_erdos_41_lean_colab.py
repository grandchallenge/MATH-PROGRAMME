import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from colab import erdos_41_lean_worker as worker

class LeanWorkerTests(unittest.TestCase):
    def test_nonzero_lean_is_red(self):
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"t.lean";source.write_text("theorem x : True := by trivial")
            receipt=Path(td)/"receipt.json"
            class Result:
                def __init__(self,returncode,stdout="",stderr=""):
                    self.returncode,self.stdout,self.stderr=returncode,stdout,stderr
            with patch.object(worker,"provision_elan",return_value=("elan","preinstalled_version_checked",None)), patch.object(worker.subprocess,"run",side_effect=[Result(0,"Lean (version 4.29.1, x86_64-unknown-linux-gnu)"),Result(1,"","error")]):
                self.assertEqual(worker.execute(source,receipt),1)
            self.assertEqual(json.loads(receipt.read_text())["status"],"RED_LEAN")
    def test_success_is_not_certification(self):
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"t.lean";source.write_text("theorem x : True := by trivial")
            receipt=Path(td)/"receipt.json"
            class Result:
                def __init__(self,returncode,stdout="",stderr=""):
                    self.returncode,self.stdout,self.stderr=returncode,stdout,stderr
            with patch.object(worker,"provision_elan",return_value=("elan","preinstalled_version_checked",None)), patch.object(worker.subprocess,"run",side_effect=[Result(0,"Lean (version 4.29.1, x86_64-unknown-linux-gnu)"),Result(0)]):
                self.assertEqual(worker.execute(source,receipt),0)
            data=json.loads(receipt.read_text())
            self.assertEqual(data["status"],"GREEN_LEAN_CHECKED_UNADJUDICATED")
            self.assertFalse(any(data["authority_effects"].values()))
if __name__=="__main__":unittest.main()
