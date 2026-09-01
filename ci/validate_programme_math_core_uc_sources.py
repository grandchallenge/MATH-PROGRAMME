#!/usr/bin/env python3
"""Verify vendored UC-001 pilot evidence is byte-identical to pinned provider Git blobs."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import validate_programme_math_core as core

BASE = core.ROOT / "governance/math_core_01/pilots/UC-001/source_bytes"
SOURCES = {
    "mathsolve_handoff": (
        BASE / "mathsolve_cert_handoff_UC-001.json",
        "8369bc21e45be6af71d2a0cdb0c5ab3cb5313bfb",
    ),
    "mathsolve_claim_ledger": (
        BASE / "mathsolve_claim_ledger_UC-001.json",
        "05c5b58f603a923fd6e66b44411ffd7c53559d55",
    ),
    "mathsolve_obligation_dag": (
        BASE / "mathsolve_proof_obligation_dag_UC-001.json",
        "5cc706c23636dadd83ab859246c412918c605f15",
    ),
    "mathcert_two_element_theorem": (
        BASE / "MathCert_Domains_UnionClosed_TwoElementCase.lean",
        "3caf5a7f2c0a2399970ed260f49daa01b3eb2ca4",
    ),
    "mathcert_qualification": (
        BASE / "mathcert_MC-UC-WP04-QUAL-001.json",
        "265c185d6b2b2970dc675729efa3fc4860f29204",
    ),
}


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    framed = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(framed).hexdigest()


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise core.ProtocolError(f"expected JSON object: {path.relative_to(core.ROOT)}")
    return value


def claim_by_id(ledger: dict, claim_id: str) -> dict:
    matches = [row for row in ledger.get("claims", []) if isinstance(row, dict) and row.get("claim_id") == claim_id]
    if len(matches) != 1:
        raise core.ProtocolError(f"vendored UC-001 ledger claim identity is not unique: {claim_id}")
    return matches[0]


def validate_source_bytes() -> None:
    for label, (path, expected) in SOURCES.items():
        if not path.is_file():
            raise core.ProtocolError(f"vendored UC-001 source missing: {label}")
        actual = git_blob_sha1(path)
        if actual != expected:
            raise core.ProtocolError(
                f"vendored UC-001 source bytes drifted for {label}: expected {expected}, got {actual}"
            )

    handoff = load_object(SOURCES["mathsolve_handoff"][0])
    ledger = load_object(SOURCES["mathsolve_claim_ledger"][0])
    dag = load_object(SOURCES["mathsolve_obligation_dag"][0])
    qualification = load_object(SOURCES["mathcert_qualification"][0])
    theorem_text = SOURCES["mathcert_two_element_theorem"][0].read_text(encoding="utf-8")

    if handoff.get("handoff_id") != "MC-HANDOFF-UC-001" or handoff.get("status") != "ready":
        raise core.ProtocolError("vendored UC-001 handoff identity/status drift")
    target_ids = {row.get("claim_id") for row in handoff.get("target_claims", []) if isinstance(row, dict)}
    if "UC-WP04-L001" not in target_ids:
        raise core.ProtocolError("vendored UC-001 handoff lost restricted theorem target")
    if handoff.get("claim_boundary") != "Restricted Lean theorems and finite replay through n <= 4 do not prove Frankl's conjecture.":
        raise core.ProtocolError("vendored UC-001 handoff boundary drift")

    restricted = claim_by_id(ledger, "UC-WP04-L001")
    universal = claim_by_id(ledger, "UC-FRANKL")
    if restricted.get("status") != "CERTIFIED_RESTRICTED":
        raise core.ProtocolError("vendored UC-001 restricted theorem status drift")
    if universal.get("status") != "OPEN_PROBLEM":
        raise core.ProtocolError("vendored UC-FRANKL target is no longer explicitly open")
    prohibited = set(ledger.get("prohibited_promotion", []))
    if "Restricted Lean theorems do not imply Frankl's conjecture." not in prohibited:
        raise core.ProtocolError("vendored UC-001 ledger lost restricted-to-universal promotion boundary")

    nodes = {row.get("id"): row for row in dag.get("nodes", []) if isinstance(row, dict) and isinstance(row.get("id"), str)}
    if nodes.get("UC-P04", {}).get("status") != "open":
        raise core.ProtocolError("vendored UC-P04 bridge is no longer open")
    terminal = dag.get("terminal_target", {})
    if terminal.get("id") != "UC-P04" or terminal.get("status") != "OPEN_PROBLEM":
        raise core.ProtocolError("vendored UC-001 terminal target boundary drift")

    if "/-- UC-WP04-L001: the two-element-member special case. -/" not in theorem_text:
        raise core.ProtocolError("vendored MATHCERT theorem lost UC-WP04-L001 identity")
    if "theorem two_element_case" not in theorem_text:
        raise core.ProtocolError("vendored MATHCERT two-element theorem is missing")

    if qualification.get("certificate_id") != "MC-UC-WP04-QUAL-001":
        raise core.ProtocolError("vendored MATHCERT qualification identity drift")
    if qualification.get("disposition") != "qualified_restricted_claims_only":
        raise core.ProtocolError("vendored MATHCERT qualification disposition drift")
    if qualification.get("mathematical_target_proved") is not False:
        raise core.ProtocolError("vendored MATHCERT qualification incorrectly promotes the mathematical target")
    if set(qualification.get("unresolved_obligations", [])) != {"UC-P04", "UC-FRANKL"}:
        raise core.ProtocolError("vendored MATHCERT qualification lost unresolved universal obligations")
    qualified = {
        row.get("claim_id"): row
        for row in qualification.get("qualified_claims", [])
        if isinstance(row, dict) and isinstance(row.get("claim_id"), str)
    }
    uc = qualified.get("UC-WP04-L001", {})
    evidence = uc.get("evidence", {}) if isinstance(uc, dict) else {}
    if uc.get("disposition") != "qualified_restricted_theorem":
        raise core.ProtocolError("vendored MATHCERT restricted qualification drift")
    if evidence.get("digest") != SOURCES["mathcert_two_element_theorem"][1]:
        raise core.ProtocolError("vendored MATHCERT qualification theorem digest drift")
    if qualification.get("solve_provider", {}).get("handoff", {}).get("digest") != SOURCES["mathsolve_handoff"][1]:
        raise core.ProtocolError("vendored MATHCERT qualification handoff digest drift")


def main() -> int:
    try:
        validate_source_bytes()
        print("MATH-CORE-01 UC-001 sources: vendored Git blobs match pinned MATHSOLVE/MATHCERT identities")
        print("MATH-CORE-01 UC-001 sources: restricted qualification preserved")
        print("MATH-CORE-01 UC-001 sources: UC-FRANKL and UC-P04 remain explicitly open")
        return 0
    except (OSError, json.JSONDecodeError, core.ProtocolError) as exc:
        print(f"MATH-CORE-01 UC-001 source validation error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
