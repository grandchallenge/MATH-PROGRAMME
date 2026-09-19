#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "external_execution_profile",
    ROOT / "ci/validate_external_execution_profile.py",
)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

class ExternalExecutionProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = mod.load(mod.PROFILE)

    def test_profile_is_valid(self) -> None:
        mod.validate()

    def test_github_parallelism_cannot_expand_to_campaign_fanout(self) -> None:
        mutated = copy.deepcopy(self.profile)
        mutated["thresholds"]["max_parallel_per_github_workflow"] = 256
        with self.assertRaises(jsonschema.ValidationError):
            mod.validate_profile_object(mutated)

    def test_external_executor_cannot_receive_repository_write_credentials(self) -> None:
        manifest_schema = mod.load(mod.MANIFEST_SCHEMA)
        manifest = {
            "schema_version": "1.0.0",
            "record_type": "GCL_EXTERNAL_EXECUTION_MANIFEST",
            "campaign": "TEST",
            "operation": "TEST-001",
            "source": {
                "repository": "grandchallenge/QUANTUM-TECHNOLOGIES",
                "commit": "0" * 40,
                "source_payload_sha256": "1" * 64,
            },
            "authority": {"operation_ref": "issue:1", "scientific_execution_authorized": True},
            "provider": {
                "class": "slurm",
                "adapter": "test",
                "provider_selection_locked_before_execution": True,
                "repository_write_credentials": True,
            },
            "work_units": {
                "enumeration": "cartesian_product",
                "axes": [{"name": "shard", "integer_range": {"start": 0, "stop_exclusive": 2, "step": 1}}],
                "expected_total": 2,
                "work_unit_id_template": "shard-{shard}",
            },
            "scientific_invariants": {"frozen": True},
            "operational_parameters": {},
            "retry_policy": {"max_attempts": 2, "same_work_unit_identity": True, "same_scientific_inputs": True},
            "output_contract": {
                "receipt_record_type": "GCL_EXTERNAL_EXECUTION_RECEIPT",
                "required_artifacts": ["rows.jsonl"],
                "all_work_units_required_before_aggregation": True,
            },
            "claim_boundaries": {"promotion": False},
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(manifest, manifest_schema, cls=jsonschema.Draft202012Validator)

    def test_receipt_cannot_claim_promotion(self) -> None:
        schema = mod.load(mod.RECEIPT_SCHEMA)
        receipt = {
            "schema_version": "1.0.0",
            "record_type": "GCL_EXTERNAL_EXECUTION_RECEIPT",
            "manifest_sha256": "2" * 64,
            "work_unit_id": "shard-0",
            "source_commit": "0" * 40,
            "source_payload_sha256": "1" * 64,
            "provider": {"class": "slurm", "adapter": "test", "execution_id": "job-1", "attempt": 1},
            "status": "SUCCESS",
            "started_at": "2026-09-19T00:00:00Z",
            "finished_at": "2026-09-19T00:01:00Z",
            "returncode": 0,
            "output_artifacts": [],
            "scientific_semantics_changed": False,
            "promotion_claim": True,
            "repository_mutation_performed": False,
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(receipt, schema, cls=jsonschema.Draft202012Validator)

if __name__ == "__main__":
    unittest.main()
