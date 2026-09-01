from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_remediation_envelope as remediation
from administrative_protected_receipt_adapters import ConfigurationAdapter
from administrative_protected_receipt_live import (
    CONFIG_EVIDENCE_BASIS,
    CONFIG_EVIDENCE_CONTRACT,
    CONFIG_EVIDENCE_ENV,
    QualificationFailure,
    read_only_configuration_preflight,
)
from administrative_protected_receipt_model import ConfigState, sha256_json


class FakeAdminClient:
    def __init__(self, ruleset):
        self.ruleset = copy.deepcopy(ruleset)

    def get(self, path):
        if path != "/repos/grandchallenge/MATH-PROGRAMME/rulesets/17137629":
            raise AssertionError(path)
        return copy.deepcopy(self.ruleset)


class ConfigurationEvidenceTests(unittest.TestCase):
    def runtime(self):
        return {
            "ruleset_id": 17137629,
            "administrator_identity": {
                "login": "gcl-release-trust[bot]",
                "app_id": 4423678,
                "token_role": "ruleset-readback",
            },
        }

    def ruleset(self, *, include_actors: bool, actors=None):
        value = {
            "id": 17137629,
            "name": "main",
            "target": "branch",
            "enforcement": "active",
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
            "rules": [{"type": "pull_request"}],
        }
        if include_actors:
            value["bypass_actors"] = list(actors or [])
        return value

    def run_identity(self):
        return {
            "GITHUB_RUN_ID": "12345",
            "GITHUB_RUN_ATTEMPT": "1",
            "GITHUB_SHA": "a" * 40,
            "GITHUB_WORKFLOW_REF": (
                "grandchallenge/MATH-PROGRAMME/.github/workflows/"
                "administrative-protected-receipt-live-qualification.yml@refs/heads/main"
            ),
        }

    def evidence(self, raw):
        body_digest = sha256_json(
            {key: raw.get(key) for key in ConfigurationAdapter.BODY_KEYS}
        )
        identity = {
            "github_run_id": "12345",
            "github_run_attempt": "1",
            "github_sha": "a" * 40,
            "github_workflow_ref": (
                "grandchallenge/MATH-PROGRAMME/.github/workflows/"
                "administrative-protected-receipt-live-qualification.yml@refs/heads/main"
            ),
        }
        return {
            "schema_version": "1.1.0",
            "configuration_evidence_contract": CONFIG_EVIDENCE_CONTRACT,
            "ruleset_id": 17137629,
            "target_actor": {
                "actor_id": 4423678,
                "actor_login": "gcl-release-trust[bot]",
                "actor_type": "Integration",
                "bypass_mode": "pull_request",
            },
            "actor_present_after": True,
            "after_actor_set": [[4423678, "Integration", "pull_request"]],
            "after_ruleset_digest": "d" * 64,
            "before_body_digest": body_digest,
            "after_body_digest": body_digest,
            "existing_bypass_actors_preserved": True,
            "non_actor_fields_preserved": True,
            "direct_protected_push": False,
            "bypass_exercised": False,
            "receipt_mutation_performed": False,
            "ledger_mutation_performed": False,
            "mirror_mutation_performed": False,
            "reactivation_authorized": False,
            "run_identity": identity,
        }

    def observe_with_evidence(self, raw, evidence):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "reconciliation.json"
            path.write_text(json.dumps(evidence), encoding="utf-8")
            env = dict(self.run_identity())
            env[CONFIG_EVIDENCE_ENV] = str(path)
            with mock.patch.dict(os.environ, env, clear=False):
                return read_only_configuration_preflight(
                    FakeAdminClient(raw),
                    "grandchallenge/MATH-PROGRAMME",
                    self.runtime(),
                )

    def test_omitted_bypass_actor_field_accepts_exact_same_run_evidence(self):
        raw = self.ruleset(include_actors=False)
        observed = self.observe_with_evidence(raw, self.evidence(raw))
        self.assertEqual(ConfigState.CONVERGED, observed.state)
        self.assertTrue(observed.target_present)
        self.assertEqual(CONFIG_EVIDENCE_BASIS, observed.reason)

    def test_explicit_empty_actor_set_cannot_be_masked_by_evidence(self):
        raw = self.ruleset(include_actors=True, actors=[])
        observed = self.observe_with_evidence(raw, self.evidence(raw))
        self.assertEqual(ConfigState.DRIFTED, observed.state)
        self.assertFalse(observed.target_present)
        self.assertEqual("target actor missing", observed.reason)

    def test_stale_same_run_evidence_fails_closed(self):
        raw = self.ruleset(include_actors=False)
        evidence = self.evidence(raw)
        evidence["run_identity"]["github_sha"] = "b" * 40
        with self.assertRaisesRegex(QualificationFailure, "CONFIGURATION_EVIDENCE_INVALID"):
            self.observe_with_evidence(raw, evidence)

    def test_non_actor_body_mismatch_fails_closed(self):
        raw = self.ruleset(include_actors=False)
        evidence = self.evidence(raw)
        evidence["after_body_digest"] = "0" * 64
        with self.assertRaisesRegex(QualificationFailure, "CONFIGURATION_EVIDENCE_INVALID"):
            self.observe_with_evidence(raw, evidence)

    def test_direct_visible_actor_still_converges_without_evidence(self):
        raw = self.ruleset(
            include_actors=True,
            actors=[
                {
                    "actor_id": 4423678,
                    "actor_type": "Integration",
                    "bypass_mode": "pull_request",
                }
            ],
        )
        with mock.patch.dict(os.environ, {CONFIG_EVIDENCE_ENV: ""}, clear=False):
            observed = read_only_configuration_preflight(
                FakeAdminClient(raw),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime(),
            )
        self.assertEqual(ConfigState.CONVERGED, observed.state)
        self.assertTrue(observed.target_present)

    def test_reconciliation_emits_same_run_body_bound_evidence(self):
        raw = self.ruleset(
            include_actors=True,
            actors=[
                {
                    "actor_id": 4423678,
                    "actor_type": "Integration",
                    "bypass_mode": "pull_request",
                }
            ],
        )
        client = FakeAdminClient(raw)
        with tempfile.TemporaryDirectory() as td, mock.patch.object(
            remediation, "Client", return_value=client
        ), mock.patch.dict(os.environ, self.run_identity(), clear=False):
            report = remediation.reconcile_actor("token", Path(td) / "report.json")
        self.assertEqual(CONFIG_EVIDENCE_CONTRACT, report["configuration_evidence_contract"])
        self.assertEqual(report["before_body_digest"], report["after_body_digest"])
        self.assertTrue(report["actor_present_after"])
        self.assertFalse(report["mutation_performed"])

    def test_workflow_keeps_qualification_admin_token_read_only_and_binds_evidence(self):
        text = (
            ROOT
            / ".github"
            / "workflows"
            / "administrative-protected-receipt-live-qualification.yml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "ADMIN_TOKEN: ${{ steps.admin-read-token.outputs.token }}",
            text,
        )
        self.assertNotIn(
            "ADMIN_TOKEN: ${{ steps.admin-write-token.outputs.token }}",
            text,
        )
        self.assertIn(
            "GCL_PROTECTED_RECEIPT_CONFIG_EVIDENCE: administrative-remediation-ruleset-reconciliation.json",
            text,
        )
        self.assertEqual(1, text.count("permission-administration: write"))
        self.assertGreaterEqual(text.count("permission-administration: read"), 2)


if __name__ == "__main__":
    unittest.main()
