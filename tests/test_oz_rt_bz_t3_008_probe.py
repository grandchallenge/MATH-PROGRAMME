from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_008" / "producer.py"

spec = importlib.util.spec_from_file_location("t3_008_probe_producer", PRODUCER)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load T3-008 producer")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


class T3008Probe(unittest.TestCase):
    def test_emit_candidate_search_result(self) -> None:
        result = producer.compute_result()
        print("T3_008_PROBE=" + json.dumps(result, sort_keys=True, separators=(",", ":")))
        self.assertEqual(result["operation"], "OZ-RT-BZ-T3-008")
        self.assertEqual(result["route"], "SYMMETRIC_2D_RAW_JET_DIVERGENCE_001")
        self.assertEqual(len(result["stages"]), 3)


if __name__ == "__main__":
    unittest.main()
