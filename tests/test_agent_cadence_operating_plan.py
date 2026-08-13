from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ci.validate_agent_cadence_operating_plan import DEFAULT_MANIFEST, validate


class AgentCadenceOperatingPlanTests(unittest.TestCase):
    def test_canonical_transform_is_exact(self) -> None:
        self.assertEqual(validate(), [])

    def test_non_exact_phase_fails(self) -> None:
        value = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        value["phase_durations"][1]["target_seconds"] += 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transform.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertTrue(any("phase stabilize_and_specify" in item for item in validate(path)))

    def test_authority_requirement_cannot_be_compressed_away(self) -> None:
        value = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        value["noncompressed_requirements"].remove("reserved_human_authority")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transform.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertTrue(any("reserved_human_authority" in item for item in validate(path)))


if __name__ == "__main__":
    unittest.main()
