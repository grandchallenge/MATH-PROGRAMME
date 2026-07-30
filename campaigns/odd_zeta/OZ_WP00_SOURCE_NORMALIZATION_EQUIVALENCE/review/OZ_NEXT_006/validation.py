"""Validate the OZ-NEXT-006 qualified WP00 closure and ordered lane authorization."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE"
PACKAGE = BASE / "review/OZ_NEXT_006"

EXPECTED_ROLES = {
    "Axiomatist",
    "Cartographer",
    "Grammarian",
    "Verifier",
    "Adversary",
    "Formalist",
    "Amanuensis",
    "Referee",
}
EXPECTED_ORDER = [
    "OZ-WP01",
    "OZ-WP02",
    "OZ-RT-APERY-BROW-001",
    "OZ-RT-LB-INSTANCE-001",
    "OZ-RT-BZ-T3-001",
    "OZ-RT-SHARP12-001",
]
EXPECTED_LITERATURE = {
    "OZ-LIT-B038": ("1508.00297v1", 671795, "b3694b4d597b48985fdd8ca77db115e30f9b3de0e0e4031d84af45400b71453d"),
    "OZ-LIT-B039": ("2102.11839v2", 314883, "520da4b0171128d22971d7398f79a1aa6cd760c2412b34a78ba5120adc371ee1"),
    "OZ-LIT-B040": ("2301.12248v1", 214378, "9f37cd0a5a1b972e138e621d70f85ec8f898e31ed32ed1daeadb1b73e3d04f95"),
    "OZ-LIT-B041": ("2011.03400v1", 198635, "3390126ece668d5dba1d13a63bfbc6c8d7da822b69770613a3a4ba1b3ee5f963"),
    "OZ-LIT-B042": ("2503.07625v2", 598544, "a95ce9f431c4783b3f51645be9a029e09787f15c0db5c7a9f9ca923a6a3581c3"),
}
EXPECTED_GIT_BLOBS = {
    "01_INTAKE_SOURCE_LOCK.yaml": "a2b55233a77ad05a49f55096864b7c98741411e3",
    "06_SOURCE_ACQUISITION_A004.yaml": "20771d4515f2238920ac46a8e0186a24c1c06275",
    "07_INDEPENDENT_REVIEW_OZ_NEXT_004.md": "69113003fdb170bb8d9cfb1ea78a58b3ed5d9514",
    "08_CORRECTIVE_SEQUENCE_OZ_NEXT_005.md": "119e53e9bbc3e494cef53531bb919333e82191c6",
}
EXPECTED_REVIEW_BLOB = "00efa2912b0111e2c500da483e1ece8acead845d"


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_yaml(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing package file: {path.relative_to(ROOT)}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.name}: root must be a mapping")
    return data


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def validate_package(root: Path = ROOT) -> list[str]:
    global ROOT, BASE, PACKAGE
    old = (ROOT, BASE, PACKAGE)
    ROOT = root
    BASE = ROOT / "campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE"
    PACKAGE = BASE / "review/OZ_NEXT_006"
    errors: list[str] = []
    try:
        closure = load_yaml(PACKAGE / "CLOSURE_REGISTER.yaml")
        lanes = load_yaml(PACKAGE / "LANE_AUTHORIZATION.yaml")
        summary = load_yaml(PACKAGE / "OBJECT_DISPOSITION_SUMMARY.yaml")
        literature = load_yaml(PACKAGE / "SUPPLEMENTAL_LITERATURE_ADMISSION.yaml")

        require(closure.get("closure_id") == "OZ-NEXT-006", "wrong closure_id")
        require(closure.get("closure_class") == "QUALIFIED_COMPLETE_NO_PROMOTION", "wrong closure class")
        findings = closure.get("closure_findings", {})
        require(findings.get("wp00_complete") is True, "WP00 must close in the closure overlay")
        require(findings.get("promotion_ready") is False, "qualified closure may not set promotion_ready")
        require(findings.get("exhaustive_novelty_search_complete") is False, "novelty search must remain incomplete")
        require(findings.get("all_open_mathematics_resolved") is False, "open mathematics must remain explicit")

        roles = closure.get("roles", [])
        require(isinstance(roles, list), "roles must be a list")
        role_names = {item.get("role") for item in roles if isinstance(item, dict)}
        require(role_names == EXPECTED_ROLES, f"role set mismatch: {sorted(role_names)}")
        referee = next(item for item in roles if item.get("role") == "Referee")
        require(referee.get("verdict") == "QUALIFIED_COMPLETE_NO_PROMOTION", "Referee verdict drift")

        debt = closure.get("open_research_debt", [])
        require(len(debt) == 8, "exactly eight open research-debt records are required")
        require(all(item.get("blocks") for item in debt), "every debt record must state blocked promotions")

        require(lanes.get("execution_order") == EXPECTED_ORDER, "ordered lane sequence drift")
        lane_records = lanes.get("lanes", [])
        require([item.get("id") for item in lane_records] == EXPECTED_ORDER, "lane records must follow execution_order")
        require(lane_records[0].get("status") == "AUTHORIZED_ON_OZ_NEXT_006_MERGE", "WP01 authorization drift")
        require(lane_records[-1].get("status") == "DEFERRED_UNTIL_BLOCKER_PACKETS_COMPLETE", "sharp-12 must remain deferred")
        for index, item in enumerate(lane_records):
            require(item.get("promotion_boundary"), f"{item.get('id')}: missing promotion boundary")
            require(item.get("required_outputs"), f"{item.get('id')}: missing required outputs")
            if index:
                require(
                    EXPECTED_ORDER[index - 1] in item.get("prerequisites", []),
                    f"{item.get('id')}: predecessor prerequisite missing",
                )

        counts = summary.get("record_counts", {})
        require(
            counts
            == {
                "non_literature": 43,
                "original_literature": 37,
                "supplemental_literature": 5,
                "total_governed_or_supplemental": 85,
            },
            "record-count summary drift",
        )
        novelty = summary.get("novelty", {})
        require(novelty.get("new_after_audit") == [], "NEW_AFTER_AUDIT is prohibited")
        require(novelty.get("priority_claims_authorized") is False, "priority claims remain unauthorized")
        irrationality = summary.get("irrationality", {})
        require(irrationality.get("open_bridge_count") == 8, "bridge count must remain eight")
        require(irrationality.get("promotion_authorized") is False, "irrationality promotion is prohibited")

        records = literature.get("records", [])
        require(len(records) == 5, "five supplemental literature records required")
        actual = {record.get("id"): record for record in records}
        require(set(actual) == set(EXPECTED_LITERATURE), "supplemental literature ID drift")
        for record_id, (version, size, digest) in EXPECTED_LITERATURE.items():
            record = actual[record_id]
            require(record.get("arxiv_version") == version, f"{record_id}: version drift")
            require(record.get("bytes") == size, f"{record_id}: byte length drift")
            require(record.get("sha256") == digest, f"{record_id}: SHA-256 drift")
            require(re.fullmatch(r"[0-9a-f]{64}", digest) is not None, f"{record_id}: invalid digest")
        require(
            literature.get("novelty_disposition", {}).get("new_after_audit_authorized") is False,
            "supplemental admission may not authorize novelty",
        )

        for relative, expected in EXPECTED_GIT_BLOBS.items():
            path = BASE / relative
            require(git_blob_sha(path) == expected, f"historical authority blob drift: {relative}")
        review_path = BASE / "review/OZ_NEXT_004/REVIEW_REGISTER.yaml"
        require(git_blob_sha(review_path) == EXPECTED_REVIEW_BLOB, "OZ-NEXT-004 review register blob drift")

        bridges = load_yaml(BASE / "03_IRRATIONALITY_BRIDGE_REGISTER.yaml")
        bridge_records = bridges.get("bridges", [])
        require(len(bridge_records) == 8, "bridge register must contain eight records")
        require(all(item.get("status") == "OPEN" for item in bridge_records), "all bridge obligations must remain OPEN")

        sharp12 = load_yaml(BASE / "review/OZ_NEXT_005/SHARP12_RECONCILIATION.yaml")
        require(sharp12.get("headline", {}).get("effective_status") == "STATED_ONLY", "sharp-12 status drift")
        require(sharp12.get("promotion", {}).get("eligible") is False, "sharp-12 promotion drift")

        prior = load_yaml(BASE / "review/OZ_NEXT_005/PRIOR_ART_ACQUISITION.yaml")
        old_records = {item["id"]: item for item in prior.get("sources", [])}
        mapping = literature.get("supersedes_temporary_ids", {})
        for old_id, new_id in mapping.items():
            require(old_records[old_id]["sha256"] == actual[new_id]["sha256"], f"{new_id}: inherited digest mismatch")
            require(old_records[old_id]["bytes"] == actual[new_id]["bytes"], f"{new_id}: inherited byte mismatch")

        quarantine = load_yaml(BASE / "review/OZ_NEXT_005/LEAN_QUARANTINE.yaml")
        require(len(quarantine.get("quarantined_targets", [])) == 5, "five Lean declarations must remain quarantined")
        require(
            quarantine.get("promotion", {}).get("downstream_compact_form_promotion") is False,
            "compact-form promotion must remain blocked",
        )

    except (ValidationError, KeyError, TypeError, StopIteration, yaml.YAMLError) as exc:
        errors.append(str(exc))
    finally:
        ROOT, BASE, PACKAGE = old
    return errors
