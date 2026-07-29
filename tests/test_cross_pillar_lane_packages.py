from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_cross_pillar_lane_packages import LanePackageError, validate  # noqa: E402


class CrossPillarLanePackageTests(unittest.TestCase):
    def make_root(self) -> tempfile.TemporaryDirectory:
        directory = tempfile.TemporaryDirectory()
        target = Path(directory.name)
        (target / "governance").mkdir(parents=True)
        shutil.copy2(
            ROOT / "governance/cross_pillar_lane_packages.json",
            target / "governance/cross_pillar_lane_packages.json",
        )
        shutil.copytree(ROOT / "lanes", target / "lanes")
        shutil.copytree(ROOT / "docs/lanes", target / "docs/lanes")
        return directory

    def mutate_json(self, root: Path, path: str, mutator) -> None:
        target = root / path
        value = json.loads(target.read_text(encoding="utf-8"))
        mutator(value)
        target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def assert_rejected(self, mutator) -> None:
        directory = self.make_root()
        root = Path(directory.name)
        try:
            mutator(root)
            with self.assertRaises(LanePackageError):
                validate(root)
        finally:
            directory.cleanup()

    def test_current_repository_passes(self) -> None:
        validate(ROOT)

    def test_missing_doctrine_is_rejected(self) -> None:
        self.assert_rejected(
            lambda root: (root / "docs/lanes/INTERVAL_ARITHMETIC.md").unlink()
        )

    def test_invalid_fixture_input_is_rejected(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate_json(
                root,
                "lanes/interval_arithmetic/fixture.json",
                lambda value: value["input"].update(precision_bits=8),
            )
        )

    def test_handoff_status_outside_manifest_is_rejected(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate_json(
                root,
                "lanes/exact_finite_enumeration/lane.json",
                lambda value: value["allowed_statuses"].remove("replayed"),
            )
        )

    def test_toy_fixture_cannot_claim_certification(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate_json(
                root,
                "lanes/lean_formalization_handoff/fixture.json",
                lambda value: value["handoff"].update(
                    certification_state="certified_by_mathcert"
                ),
            )
        )

    def test_orphan_lane_package_is_rejected(self) -> None:
        def add_orphan(root: Path) -> None:
            orphan = root / "lanes/orphan"
            orphan.mkdir()
            (orphan / "lane.json").write_text(
                json.dumps(
                    {
                        "schema_version": "1.0.0",
                        "lane_id": "LANE-ORPHAN",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

        self.assert_rejected(add_orphan)

    def test_insufficient_rejection_policy_is_rejected(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate_json(
                root,
                "lanes/sat_smt_proof/lane.json",
                lambda value: value.update(rejection_policy=["one rule"]),
            )
        )

    def test_invalid_json_schema_is_rejected(self) -> None:
        self.assert_rejected(
            lambda root: self.mutate_json(
                root,
                "lanes/literature_status_spine/input.schema.json",
                lambda value: value.update(type="not-a-json-schema-type"),
            )
        )


if __name__ == "__main__":
    unittest.main()
