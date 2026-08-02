from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci" / "gcl.py"
SPEC = importlib.util.spec_from_file_location("gcl_tooling", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
gcl = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gcl
SPEC.loader.exec_module(gcl)


class GclToolingTests(unittest.TestCase):
    def load_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def manifest_root(self) -> tempfile.TemporaryDirectory:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        for relative in (
            "governance/gcl_truth_spine_registry.json",
            "governance/governed_campaign_registry.json",
            "schemas/governed_campaign_registry.schema.json",
        ):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        return temporary

    def identity_root(self) -> tempfile.TemporaryDirectory:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        for relative in (
            "governance/governed_campaign_registry.json",
            "schemas/gcl_local_identity_manifest.schema.json",
            "fixtures/gcl_tooling/governed_campaign_registry.identity.json",
        ):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        return temporary

    def test_repository_candidate_is_valid(self) -> None:
        self.assertEqual(gcl.validate_tooling(ROOT), [])

    def test_command_contract_has_exact_states(self) -> None:
        contract = self.load_json(ROOT / "governance/gcl_tooling_command_contract.json")
        states = {item["name"]: item["implementation_state"] for item in contract["commands"]}
        self.assertEqual(set(states), gcl.EXPECTED_COMMANDS)
        self.assertEqual(
            {name for name, state in states.items() if state == "implemented_candidate"},
            gcl.IMPLEMENTED_COMMANDS,
        )
        self.assertEqual(
            {name for name, state in states.items() if state == "planned_not_executable"},
            gcl.PLANNED_COMMANDS,
        )

    def test_valid_campaign_manifest_passes(self) -> None:
        with self.manifest_root() as temporary:
            root = Path(temporary)
            errors = gcl.validate_manifest_record(
                root=root,
                manifest_path=root / "governance/governed_campaign_registry.json",
                schema_path=root / "schemas/governed_campaign_registry.schema.json",
                record_class_id="campaign_manifest",
                repository="grandchallenge/MATH-PROGRAMME",
                relative_path="governance/governed_campaign_registry.json",
                truth_spine_path=root / "governance/gcl_truth_spine_registry.json",
            )
            self.assertEqual(errors, [])

    def test_unknown_record_class_fails_closed(self) -> None:
        with self.manifest_root() as temporary:
            root = Path(temporary)
            errors = gcl.validate_manifest_record(
                root=root,
                manifest_path=root / "governance/governed_campaign_registry.json",
                schema_path=root / "schemas/governed_campaign_registry.schema.json",
                record_class_id="invented_authority",
                repository="grandchallenge/MATH-PROGRAMME",
                relative_path="governance/governed_campaign_registry.json",
                truth_spine_path=root / "governance/gcl_truth_spine_registry.json",
            )
            self.assertTrue(any("unknown or duplicate record class" in item for item in errors))

    def test_wrong_authoritative_repository_fails(self) -> None:
        with self.manifest_root() as temporary:
            root = Path(temporary)
            errors = gcl.validate_manifest_record(
                root=root,
                manifest_path=root / "governance/governed_campaign_registry.json",
                schema_path=root / "schemas/governed_campaign_registry.schema.json",
                record_class_id="campaign_manifest",
                repository="grandchallenge/MATHFORGE",
                relative_path="governance/governed_campaign_registry.json",
                truth_spine_path=root / "governance/gcl_truth_spine_registry.json",
            )
            self.assertTrue(any("authority is" in item for item in errors))

    def test_noncanonical_path_fails(self) -> None:
        with self.manifest_root() as temporary:
            root = Path(temporary)
            wrong = root / "scratch/campaign.json"
            wrong.parent.mkdir()
            shutil.copyfile(root / "governance/governed_campaign_registry.json", wrong)
            errors = gcl.validate_manifest_record(
                root=root,
                manifest_path=wrong,
                schema_path=root / "schemas/governed_campaign_registry.schema.json",
                record_class_id="campaign_manifest",
                repository="grandchallenge/MATH-PROGRAMME",
                relative_path="scratch/campaign.json",
                truth_spine_path=root / "governance/gcl_truth_spine_registry.json",
            )
            self.assertTrue(any("outside the authoritative path class" in item for item in errors))

    def test_schema_invalid_manifest_fails(self) -> None:
        with self.manifest_root() as temporary:
            root = Path(temporary)
            manifest_path = root / "governance/governed_campaign_registry.json"
            manifest = self.load_json(manifest_path)
            manifest["schema_version"] = "999.0.0"
            self.write_json(manifest_path, manifest)
            errors = gcl.validate_manifest_record(
                root=root,
                manifest_path=manifest_path,
                schema_path=root / "schemas/governed_campaign_registry.schema.json",
                record_class_id="campaign_manifest",
                repository="grandchallenge/MATH-PROGRAMME",
                relative_path="governance/governed_campaign_registry.json",
                truth_spine_path=root / "governance/gcl_truth_spine_registry.json",
            )
            self.assertTrue(any("manifest schema" in item for item in errors))

    def test_valid_identity_manifest_passes(self) -> None:
        with self.identity_root() as temporary:
            root = Path(temporary)
            self.assertEqual(
                gcl.check_identity_manifest(
                    root=root,
                    identity_manifest_path=(
                        root / "fixtures/gcl_tooling/governed_campaign_registry.identity.json"
                    ),
                    identity_schema_path=root / "schemas/gcl_local_identity_manifest.schema.json",
                ),
                [],
            )

    def identity_mutation_errors(self, mutation) -> list[str]:
        with self.identity_root() as temporary:
            root = Path(temporary)
            path = root / "fixtures/gcl_tooling/governed_campaign_registry.identity.json"
            manifest = self.load_json(path)
            mutation(manifest)
            self.write_json(path, manifest)
            return gcl.check_identity_manifest(
                root=root,
                identity_manifest_path=path,
                identity_schema_path=root / "schemas/gcl_local_identity_manifest.schema.json",
            )

    def test_sha256_drift_fails(self) -> None:
        errors = self.identity_mutation_errors(
            lambda value: value["files"][0].__setitem__("sha256", "0" * 64)
        )
        self.assertTrue(any("SHA-256 mismatch" in item for item in errors))

    def test_git_blob_drift_fails(self) -> None:
        errors = self.identity_mutation_errors(
            lambda value: value["files"][0].__setitem__("git_blob_sha1", "0" * 40)
        )
        self.assertTrue(any("Git blob mismatch" in item for item in errors))

    def test_byte_length_drift_fails(self) -> None:
        errors = self.identity_mutation_errors(
            lambda value: value["files"][0].__setitem__(
                "bytes", value["files"][0]["bytes"] + 1
            )
        )
        self.assertTrue(any("byte-length mismatch" in item for item in errors))

    def test_duplicate_identity_path_fails(self) -> None:
        errors = self.identity_mutation_errors(
            lambda value: value["files"].append(copy.deepcopy(value["files"][0]))
        )
        self.assertTrue(any("duplicate file path" in item for item in errors))

    def test_missing_identity_subject_fails(self) -> None:
        def mutate(value: dict) -> None:
            value["files"][0]["path"] = "governance/missing.json"

        errors = self.identity_mutation_errors(mutate)
        self.assertTrue(any("missing file" in item for item in errors))

    def test_path_traversal_fails(self) -> None:
        errors = self.identity_mutation_errors(
            lambda value: value["files"][0].__setitem__("path", "../outside.json")
        )
        self.assertTrue(any("unsafe repository path" in item for item in errors))

    def test_planned_commands_refuse_execution(self) -> None:
        for command in sorted(gcl.PLANNED_COMMANDS):
            with self.subTest(command=command), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(gcl.main([command]), 1)

    def test_contract_cannot_authorize_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract = self.load_json(ROOT / "governance/gcl_tooling_command_contract.json")
            schema = self.load_json(ROOT / "schemas/gcl_tooling_command_contract.schema.json")
            truth = self.load_json(ROOT / "governance/gcl_truth_spine_registry.json")
            contract["claim_boundaries"]["promotion_authorized"] = True
            contract_path = root / "contract.json"
            schema_path = root / "schema.json"
            truth_path = root / "truth.json"
            self.write_json(contract_path, contract)
            self.write_json(schema_path, schema)
            self.write_json(truth_path, truth)
            errors = gcl.tooling_contract_errors(contract_path, schema_path, truth_path)
            self.assertTrue(errors)

    def test_output_boundary_is_explicit(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = gcl.main(["verify-promotion"])
        report = json.loads(stream.getvalue())
        self.assertEqual(result, 1)
        self.assertFalse(report["authority_boundary"]["may_authorize_promotion"])
        self.assertFalse(report["authority_boundary"]["may_modify_protected_records"])
        self.assertFalse(report["authority_boundary"]["aether_required"])


if __name__ == "__main__":
    unittest.main()
