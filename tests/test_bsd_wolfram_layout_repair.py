from __future__ import annotations

import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BSDWolframLayoutRepairTests(unittest.TestCase):
    def test_fail_closed_verifier(self):
        subprocess.run(
            [sys.executable, str(ROOT / "ci/verify_bsd_wolfram_layout_repair.py")],
            cwd=ROOT,
            check=True,
        )

    def test_semantic_master_is_unchanged(self):
        data = (ROOT / "tools/bsd_wolfram_semantic_master.wl").read_bytes()
        self.assertEqual(4263, len(data))
        self.assertEqual(
            "41b9e926d0edda8fbb65ead57d54fd0985689ca73ac1715731818843cc013936",
            hashlib.sha256(data).hexdigest(),
        )

    def test_shared_documentary_runtime_not_touched_by_repair(self):
        data = (ROOT / "docs/javascripts/documentary.js").read_bytes()
        header = f"blob {len(data)}\0".encode()
        self.assertEqual(
            "b53dce8861e9eee78ced01758220b3ed3110a22f",
            hashlib.sha1(header + data).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
