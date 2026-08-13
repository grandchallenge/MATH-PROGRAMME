from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ci.validate_agent_cadence_operating_plan import DEFAULT_MANIFEST, duration_seconds, validate


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

    def test_duration_label_must_match_seconds(self) -> None:
        value = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        value["milestone_offsets"][1]["target_duration"] = "P2DT11H"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transform.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertTrue(any("target_duration does not match" in item for item in validate(path)))

    def test_ops_a_is_required_for_every_execution_gate(self) -> None:
        value = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        value["dependency_contract"]["dependencies"]["CMDG-A"] = []
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transform.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertTrue(any("CMDG-A does not depend on OPS-A" in item for item in validate(path)))

    def test_terminal_sequence_must_be_ordered(self) -> None:
        value = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        value["terminal_sequence"][2]["seconds"] = value["terminal_sequence"][1]["seconds"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transform.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertTrue(any("terminal sequence" in item for item in validate(path)))

    def test_supported_iso_duration_parser(self) -> None:
        self.assertEqual(duration_seconds("P2DT7H12M"), 198720)
        with self.assertRaises(ValueError):
            duration_seconds("P2DT25H")


if __name__ == "__main__":
    unittest.main()
