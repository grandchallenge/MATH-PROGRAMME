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
        self.assertEqual(4665, len(data))
        self.assertEqual(
            "d05088cf0f88c7e3c0960ebb99973fac19001a2bdb6abff3e92f8a4fe0bc2ec0",
            hashlib.sha256(data).hexdigest(),
        )
        header = f"blob {len(data)}\0".encode()
        self.assertEqual(
            "206842583d15acf91eb0e363ddb12cbf124ab0a9",
            hashlib.sha1(header + data).hexdigest(),
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
