#!/usr/bin/env python3
"""Validate exact MATHFORGE provider and Formal Conjectures imports."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "mathforge_provider_imports.json"
SCHEMA_PATH = ROOT / "schemas" / "mathforge_provider_import.schema.json"
DOMAIN_REGISTRY_PATH = ROOT / "DOMAIN_REGISTRY.yaml"

EXPECTED_PROVIDER_COMMIT = "0faee396ffa56c568ee0ae6a348bdb43ca80ac4d"
EXPECTED_IMPORTS = {
    "BSD-001": ("retrospective", "provider_manifests/BSD-001.json", "c95e1f0ef8d2e662ca9bb3bb49317fa8aa7b2185"),
    "HC-001": ("native", "provider_manifests/HC-001.json", "1bce7ab1e2cc7daa8f125747c69bad262adc080f"),
    "NS-CI-001": ("native", "provider_manifests/NS-CI-001.json", "ed5220c31e38ba3458dc8a94a462c89c285fc22e"),
    "OZ-001": ("retrospective", "provider_manifests/OZ-001.json", "361da6642ff3ac7953b530ee0eb21659dc94fb65"),
    "PNP-001": ("retrospective", "provider_manifests/PNP-001.json", "dc7f740d91b5f69b22dd11af6737064d132d278a"),
    "RH-001": ("retrospective", "provider_manifests/RH-001.json", "adcbee2583e5da2b59babefbafec943c113ba4ed"),
    "UC-001": ("native", "provider_manifests/UC-001.json", "6d803633c2697f100d7d5b616ea1d6f16bff34bf"),
    "YM-001": ("retrospective", "provider_manifests/YM-001.json", "c84694d5885f94da70b8124063d1b8ee55534470"),
}
EXPECTED_ARTIFACTS = {
    "FC-GDM-001-LOCK": ("external_formal_source_lock", "formal_sources/formal_conjectures/source_lock.json", "0ef71adea9bcdfb63da78118f7fee053ccaa73ce"),
    "FC-GDM-001-NS-CI-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/NS-CI-001.json", "1ebe5de5194f48217dff3db02f389154af351592"),
    "FC-GDM-001-REGISTRY": ("external_formal_source_registry", "governance/external_formal_sources.json", "4680bee8e6b641956a5db2b453c94aab7cabb37b"),
    "FC-GDM-001-RH-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/RH-001.json", "7332c99795f810ca1d50dda8151c267855d851e7"),
    "FC-GDM-001-RH-NS-SNAPSHOT": ("formal_statement_snapshot", "formal_sources/formal_conjectures/snapshots/FC-GDM-001-RH-NS-PILOT.json", "c171b542a60956e59f4cac14fb9413bcdd7ede66"),
    "FC-GDM-002-BSD-COVERAGE": ("formal_source_coverage_record", "formal_sources/formal_conjectures/coverage/BSD-001.json", "82166625115162817551c9a6c6ce377e9e049c7e"),
    "FC-GDM-002-HC-COVERAGE": ("formal_source_coverage_record", "formal_sources/formal_conjectures/coverage/HC-001.json", "dc9dcdd8313c86298d9b4a15a712f0b9c7928a62"),
    "FC-GDM-002-INVENTORY-SCREEN": ("formal_source_inventory_screen", "formal_sources/formal_conjectures/replays/FC-GDM-002/FC-GDM-002-INVENTORY-SCREEN.json", "8dbe8d6769e842be72eb8be1e22cc605278c7561"),
    "FC-GDM-002-LOCK": ("external_formal_source_lock", "formal_sources/formal_conjectures/source_locks/FC-GDM-002.json", "9acd4a94538592a235bb302c1f31e5da11662643"),
    "FC-GDM-002-OZ-ODD-INFINITUDE-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/OZ-001-ODD-INFINITUDE.json", "2e1dd5320a6c19bd4b1515c2f7abdf9843050f48"),
    "FC-GDM-002-OZ-ODD-UNIVERSAL-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/OZ-001-ODD-UNIVERSAL.json", "06931337e40f3f7644b99470aca7939a5cd89a4f"),
    "FC-GDM-002-OZ-ZETA11-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/OZ-001-ZETA11.json", "5cdda19da72b5411b67bf378b9c83df2da28dfb5"),
    "FC-GDM-002-OZ-ZETA3-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/OZ-001-ZETA3.json", "a7ca853bd5638814078228b40e78283ae0e29b76"),
    "FC-GDM-002-OZ-ZETA5-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/OZ-001-ZETA5.json", "b4f5ef332025669c7202b83ea3a3cb13f2c8009e"),
    "FC-GDM-002-OZ-ZETA7-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/OZ-001-ZETA7.json", "34e28294097b1519b18c40a770e3cd3d8e81a15c"),
    "FC-GDM-002-OZ-ZETA9-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/OZ-001-ZETA9.json", "a6ba362e0160d92f7b609bcc12eea09b66810606"),
    "FC-GDM-002-OZ-ZUDILIN-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/OZ-001-ZUDILIN-5-11.json", "a17def6ccd96d4cdea6602336f2a09c5f66d188c"),
    "FC-GDM-002-PNP-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/PNP-001.json", "c88ac8ee7493a551670ca2a37385a9157b43c658"),
    "FC-GDM-002-REGISTRY": ("external_formal_source_registry", "governance/external_formal_sources.json", "4680bee8e6b641956a5db2b453c94aab7cabb37b"),
    "FC-GDM-002-REPLAY-MANIFEST": ("formal_source_replay_manifest", "formal_sources/formal_conjectures/replays/FC-GDM-002/REPLAY_MANIFEST.json", "d91c8ae08262791d248c9ba87837c4624c0b4cda"),
    "FC-GDM-002-SNAPSHOT-REFERENCE": ("formal_statement_replay_reference", "formal_sources/formal_conjectures/snapshots/FC-GDM-002-ACTIVE-CAMPAIGN-EXPANSION.replay.json", "1ad4250df912bf2c7cfcc7342fb0ad75e8d667e7"),
    "FC-GDM-002-TAG-RESOLUTION": ("formal_source_tag_resolution", "formal_sources/formal_conjectures/replays/FC-GDM-002/FC-GDM-002-TAG-RESOLUTION.json", "7dd39a995a789da583f8f2f0b15da2c30207f0f1"),
    "FC-GDM-002-UC-CONCORDANCE": ("statement_concordance", "formal_sources/formal_conjectures/concordance/UC-001.json", "8bba56b13978b36471e1cbafe358b82b571c2b95"),
    "FC-GDM-002-UPDATE-LEDGER": ("formal_source_update_ledger", "formal_sources/formal_conjectures/update_ledgers/FC-GDM-001-TO-FC-GDM-002.json", "ff2590e2a91b7d5ea5ea5a42c23c67c9745608a0"),
    "FC-GDM-002-YM-COVERAGE": ("formal_source_coverage_record", "formal_sources/formal_conjectures/coverage/YM-001.json", "84c25fe523e854cc0e64862fd3eb0bd866a2eac7"),
}
FC1_COMMON = ["FC-GDM-001-REGISTRY", "FC-GDM-001-LOCK", "FC-GDM-001-RH-NS-SNAPSHOT"]
FC2_COMMON = ["FC-GDM-002-REGISTRY", "FC-GDM-002-LOCK", "FC-GDM-002-SNAPSHOT-REFERENCE", "FC-GDM-002-UPDATE-LEDGER", "FC-GDM-002-REPLAY-MANIFEST", "FC-GDM-002-INVENTORY-SCREEN", "FC-GDM-002-TAG-RESOLUTION"]
EXPECTED_CAMPAIGN_ARTIFACT_IDS = {
    "BSD-001": FC2_COMMON + ["FC-GDM-002-BSD-COVERAGE"],
    "HC-001": FC2_COMMON + ["FC-GDM-002-HC-COVERAGE"],
    "NS-CI-001": FC1_COMMON + ["FC-GDM-001-NS-CI-CONCORDANCE"],
    "OZ-001": FC2_COMMON + ["FC-GDM-002-OZ-ZETA3-CONCORDANCE", "FC-GDM-002-OZ-ZETA5-CONCORDANCE", "FC-GDM-002-OZ-ZETA7-CONCORDANCE", "FC-GDM-002-OZ-ZETA9-CONCORDANCE", "FC-GDM-002-OZ-ZETA11-CONCORDANCE", "FC-GDM-002-OZ-ODD-UNIVERSAL-CONCORDANCE", "FC-GDM-002-OZ-ODD-INFINITUDE-CONCORDANCE", "FC-GDM-002-OZ-ZUDILIN-CONCORDANCE"],
    "PNP-001": FC2_COMMON + ["FC-GDM-002-PNP-CONCORDANCE"],
    "RH-001": FC1_COMMON + ["FC-GDM-001-RH-CONCORDANCE"],
    "UC-001": FC2_COMMON + ["FC-GDM-002-UC-CONCORDANCE"],
    "YM-001": FC2_COMMON + ["FC-GDM-002-YM-COVERAGE"],
}
EXPECTED_EXPANDED_EVIDENCE = {
    "source_id": "FC-GDM-002",
    "upstream_repository": "google-deepmind/formal-conjectures",
    "upstream_commit": "85f863718beeec7b58a3a1926ee92e3472bc2020",
    "replay": {"workflow_run_id": 30544600547, "artifact_id": 8761186970, "artifact_name": "formal-conjectures-expanded-replay", "archive_sha256": "1c74747519c17f873f323198a92104538667092f3274a667a09e1a6b219a7bcb"},
    "snapshot": {"member_name": "FC-GDM-002-ACTIVE-CAMPAIGN-EXPANSION.json", "byte_length": 52589, "sha256": "e7534f913160cc9cef4eb80a735c44b7b1a8ea4273f0f5236d82cc7b9dab042b", "canonical_sha256": "2b6bda841d15b022ec8c66bc332177d1283ca791f5d5f6e82323c304d1e6fdf6", "statement_count": 43},
    "inventory": {"member_name": "FC-GDM-002-FULL-INVENTORY.json", "byte_length": 1255363, "sha256": "2693de3b83c0990b0e7c62ab5032698c6dde6de0942441ba7d6cdb035625e687", "problem_count": 3232},
    "claim_boundary": "These identities pin the replay object and its selected statement and inventory members. They do not import theorem truth, status, novelty, or certification.",
}
PROVIDER_GATED_STAGES = frozenset({"WP00", "WP01", "PRIOR_ART", "RESTRICTED_TARGET"})


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def active_domain_campaign_ids() -> set[str]:
    registry = yaml.safe_load(DOMAIN_REGISTRY_PATH.read_text(encoding="utf-8"))
    return {"UC-001" if str(item["campaign_id"]) == "UC" else str(item["campaign_id"]) for item in registry.get("domains", []) if isinstance(item, dict) and item.get("status") == "ACTIVE"}


def schema_errors(instance: Any) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"governance/mathforge_provider_imports.json: {error.json_path}: {error.message}" for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))]


def supplemental_artifact_errors(campaign_id: str, entry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_ids = set(EXPECTED_CAMPAIGN_ARTIFACT_IDS.get(campaign_id, []))
    artifacts = entry.get("supplemental_artifacts", [])
    if not isinstance(artifacts, list):
        return [f"MATHFORGE imports: {campaign_id} supplemental artifacts are missing"]
    by_id = {str(item.get("artifact_id")): item for item in artifacts if isinstance(item, dict) and item.get("artifact_id")}
    ids = [str(item.get("artifact_id")) for item in artifacts if isinstance(item, dict)]
    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"MATHFORGE imports: {campaign_id} duplicate supplemental artifact {duplicate}")
    for missing in sorted(expected_ids - set(by_id)):
        errors.append(f"MATHFORGE imports: {campaign_id} supplemental artifact is missing: {missing}")
    for unknown in sorted(set(by_id) - expected_ids):
        errors.append(f"MATHFORGE imports: {campaign_id} unregistered supplemental artifact: {unknown}")
    for artifact_id in sorted(expected_ids & set(by_id)):
        kind, path, sha = EXPECTED_ARTIFACTS[artifact_id]
        item = by_id[artifact_id]
        if item.get("kind") != kind:
            errors.append(f"MATHFORGE imports: {campaign_id} {artifact_id} kind drift")
        if item.get("path") != path:
            errors.append(f"MATHFORGE imports: {campaign_id} {artifact_id} path drift")
        if item.get("git_blob_sha1") != sha:
            errors.append(f"MATHFORGE imports: {campaign_id} {artifact_id} identity drift")
    return errors


def mathforge_provider_import_errors(registry: dict[str, Any] | None = None, *, active_campaigns: set[str] | None = None) -> list[str]:
    instance = registry if registry is not None else load_json(REGISTRY_PATH)
    errors = schema_errors(instance)
    if instance.get("provider_repository") != "grandchallenge/MATHFORGE":
        errors.append("MATHFORGE imports: provider repository is not canonical")
    if instance.get("provider_commit") != EXPECTED_PROVIDER_COMMIT:
        errors.append("MATHFORGE imports: provider commit drift")
    if instance.get("expanded_evidence") != EXPECTED_EXPANDED_EVIDENCE:
        errors.append("MATHFORGE imports: expanded replay evidence identity drift")
    campaigns = instance.get("campaigns", [])
    ids = [str(item.get("campaign_id")) for item in campaigns if isinstance(item, dict)]
    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"MATHFORGE imports: duplicate campaign_id {duplicate}")
    by_id = {str(item.get("campaign_id")): item for item in campaigns if isinstance(item, dict) and item.get("campaign_id")}
    for missing in sorted(set(EXPECTED_IMPORTS) - set(by_id)):
        errors.append(f"MATHFORGE imports: registered campaign is uncovered: {missing}")
    for unknown in sorted(set(by_id) - set(EXPECTED_IMPORTS)):
        errors.append(f"MATHFORGE imports: unregistered provider authority: {unknown}")
    domain_ids = active_campaigns if active_campaigns is not None else active_domain_campaign_ids()
    for missing in sorted(domain_ids - set(by_id)):
        errors.append(f"MATHFORGE imports: ACTIVE domain campaign is uncovered: {missing}")
    manifest_paths: list[str] = []
    for campaign_id, (mode, path, sha) in EXPECTED_IMPORTS.items():
        entry = by_id.get(campaign_id)
        if not entry:
            continue
        if entry.get("disposition") != "import":
            if not isinstance(entry.get("waiver"), dict):
                errors.append(f"MATHFORGE imports: {campaign_id} has neither import nor valid waiver")
            continue
        if entry.get("coverage_mode") != mode:
            errors.append(f"MATHFORGE imports: {campaign_id} coverage mode drift")
        if entry.get("manifest_path") != path:
            errors.append(f"MATHFORGE imports: {campaign_id} manifest path drift")
        if entry.get("manifest_git_blob_sha1") != sha:
            errors.append(f"MATHFORGE imports: {campaign_id} manifest identity drift")
        manifest_paths.append(str(entry.get("manifest_path", "")))
        errors.extend(supplemental_artifact_errors(campaign_id, entry))
    for duplicate in sorted({item for item in manifest_paths if manifest_paths.count(item) > 1}):
        errors.append(f"MATHFORGE imports: duplicate manifest path {duplicate}")
    return errors


def provider_gate_errors(campaign_id: str, stage: str, registry: dict[str, Any] | None = None) -> list[str]:
    if stage not in PROVIDER_GATED_STAGES:
        return []
    canonical_id = "UC-001" if campaign_id == "UC" else campaign_id
    instance = registry if registry is not None else load_json(REGISTRY_PATH)
    entry = next((item for item in instance.get("campaigns", []) if item.get("campaign_id") == canonical_id), None)
    if not entry:
        return [f"{canonical_id} {stage}: no MATHFORGE import or approved waiver"]
    if entry.get("disposition") == "import":
        if any(not entry.get(field) for field in ("coverage_mode", "manifest_path", "manifest_git_blob_sha1")):
            return [f"{canonical_id} {stage}: incomplete MATHFORGE import fields"]
        if supplemental_artifact_errors(canonical_id, entry):
            return [f"{canonical_id} {stage}: invalid MATHFORGE supplemental import"]
        if canonical_id in EXPECTED_CAMPAIGN_ARTIFACT_IDS and instance.get("expanded_evidence") != EXPECTED_EXPANDED_EVIDENCE:
            return [f"{canonical_id} {stage}: invalid expanded replay evidence identity"]
        return []
    waiver = entry.get("waiver")
    if entry.get("disposition") == "waiver" and isinstance(waiver, dict):
        if all(waiver.get(field) for field in ("approved_by", "reason", "scope", "review_on")):
            return []
        return [f"{canonical_id} {stage}: incomplete MATHFORGE waiver fields"]
    return [f"{canonical_id} {stage}: invalid MATHFORGE provider disposition"]


def main() -> int:
    errors = mathforge_provider_import_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("MATHFORGE provider imports are pinned: 8 campaigns, exact merged commit, unchanged coverage modes, FC-GDM-001 RH/NS supplements, FC-GDM-002 expanded artifact identities, and promotion coverage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
