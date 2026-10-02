#!/usr/bin/env python3
from __future__ import annotations

import copy

import policy_impact as impact


def main() -> int:
    impact.validate_control()

    docs = impact.classify_paths(["docs/governance/example.md"])
    assert docs["policy_shards"] == ["core", "docs"]

    handoff = impact.classify_paths(["handoffs/GHOS-ESTATE-ROLLOUT-001/PHASE1/HANDOFF.md"])
    assert handoff["policy_shards"] == ["core", "administrative", "campaigns", "docs"]
    assert not handoff["unknown_paths"]

    cmdg = impact.classify_paths(["fixtures/cmdg/extractor_001/log_gcd.json"])
    assert "fixtures" in cmdg["policy_shards"]
    assert "cmdg" in cmdg["policy_shards"]
    assert "repository-regression" not in cmdg["policy_shards"]

    oz = impact.classify_paths(["tests/test_oz_rt_bz_t3.py"])
    assert oz["policy_shards"] == ["core", "oz"]
    assert not oz["unknown_paths"]

    fixture_test = impact.classify_paths(["tests/test_ns_wp06_halting_gate_fixture.py"])
    assert fixture_test["policy_shards"] == ["core", "fixtures"]
    assert not fixture_test["unknown_paths"]

    contract_test = impact.classify_paths(["tests/test_documentary_visual_pedagogy.py"])
    assert contract_test["policy_shards"] == ["core", "contracts", "docs"]
    assert not contract_test["unknown_paths"]

    unknown_test = impact.classify_paths(["tests/test_new_unclassified_research.py"])
    assert unknown_test["policy_shards"] == list(impact.ALL_SHARDS)
    assert unknown_test["unknown_paths"] == ["tests/test_new_unclassified_research.py"]

    req = impact.classify_paths(["requirements/policy.txt"])
    assert req["policy_shards"] == ["core", "contracts"]

    admin = impact.classify_paths(["ci/administrative_autonomy_runtime.py"])
    assert admin["policy_shards"] == ["core", "administrative"]

    release_trust = impact.classify_paths([
        "ci/release_trust_admin.py",
        "governance/release_trust_admin_contract.json",
        "tests/test_intellect_profile_admin.py",
    ])
    assert release_trust["policy_shards"] == ["core", "administrative", "contracts"]
    assert not release_trust["unknown_paths"]

    runner_control = impact.classify_paths(["ci/run_unittest_modules.py", "ci/run_policy_shard.py"])
    assert runner_control["policy_shards"] == ["core", "contracts"]
    assert not runner_control["unknown_paths"]

    classifier_control = impact.classify_paths(["ci/policy_impact.py", "ci/test_policy_impact.py"])
    assert classifier_control["policy_shards"] == list(impact.ALL_SHARDS)
    assert not classifier_control["unknown_paths"]

    formal_control = impact.classify_paths(["ci/formal_validation.py"])
    assert formal_control["policy_shards"] == list(impact.ALL_SHARDS)

    visual = impact.classify_paths(["tools/render_visual_pedagogy_batch3_svg_candidates.py"])
    assert visual["policy_shards"] == ["core", "contracts", "docs"]
    assert "repository-regression" not in visual["policy_shards"]
    assert not visual["unknown_paths"]

    full = impact.classify_paths([".github/workflows/ci.yml"])
    assert full["policy_shards"] == list(impact.ALL_SHARDS)

    unknown = impact.classify_paths(["brand-new-policy-domain/data.bin"])
    assert unknown["policy_shards"] == list(impact.ALL_SHARDS)
    assert unknown["unknown_paths"]

    assert impact.normalize_paths(["./docs/x.md"]) == ["docs/x.md"]
    for unsafe in ("../escape", "/absolute", "a/../escape", ".."):
        try:
            impact.normalize_paths([unsafe])
        except impact.ImpactError:
            pass
        else:
            raise AssertionError(f"unsafe changed path accepted: {unsafe}")

    control = impact.load_json(impact.CONTROL_PATH)
    sentinel = impact.classify_paths(
        [], event_name="schedule", schedule=control["policy_dag"]["full_policy_sentinel_cron"]
    )
    assert sentinel["event_mode"] == "full_policy_sentinel"
    assert sentinel["policy_shards"] == list(impact.ALL_SHARDS)

    unknown_schedule = impact.classify_paths([], event_name="schedule", schedule="17 */6 * * *")
    assert unknown_schedule["event_mode"] == "unknown_schedule"
    assert unknown_schedule["policy_shards"] == list(impact.ALL_SHARDS)

    manual = impact.classify_paths([], event_name="workflow_dispatch")
    assert manual["event_mode"] == "manual_full"
    assert manual["policy_shards"] == list(impact.ALL_SHARDS)

    merge_group = impact.classify_paths([], event_name="merge_group")
    assert merge_group["event_mode"] == "merge_group_full"
    assert merge_group["policy_shards"] == list(impact.ALL_SHARDS)
    assert not merge_group["unknown_paths"]

    pushed = impact.classify_paths(["docs/governance/example.md"], event_name="push")
    assert pushed["policy_shards"] == ["core", "docs"]

    original_loader = impact.load_json
    protected_control = original_loader(impact.CONTROL_PATH)
    protected_registry = original_loader(impact.REGISTRY_PATH)
    mutations = []

    mutated = copy.deepcopy(protected_control)
    mutated["classifier"]["unknown_path_behavior"] = "IGNORE"
    mutations.append(mutated)

    mutated = copy.deepcopy(protected_control)
    mutated["formal_validation"]["required_context"] = "campaign-specific-context"
    mutations.append(mutated)

    mutated = copy.deepcopy(protected_control)
    mutated["formal_validation"]["protected_sentinel"]["attestation_substitution"] = True
    mutations.append(mutated)

    mutated = copy.deepcopy(protected_control)
    mutated["authority_boundary"]["required_checks_removed_without_equivalent_successor"] = True
    mutations.append(mutated)

    mutated = copy.deepcopy(protected_control)
    mutated["claim_boundaries"]["mathematical_authority_created"] = True
    mutations.append(mutated)

    for candidate in mutations:
        def loader(path, candidate=candidate):
            if path == impact.CONTROL_PATH:
                return candidate
            if path == impact.REGISTRY_PATH:
                return protected_registry
            if path == impact.CONTROL_SCHEMA:
                return original_loader(path)
            if path == impact.REGISTRY_SCHEMA:
                return original_loader(path)
            return original_loader(path)

        impact.load_json = loader
        try:
            impact.validate_control()
        except (impact.ImpactError, impact.jsonschema.ValidationError):
            pass
        else:
            raise AssertionError("unsafe policy-impact control mutation was accepted")
        finally:
            impact.load_json = original_loader

    print("policy impact gating rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
