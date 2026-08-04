from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "docs/council/submissions/GCL-TCS-00_GCL-POS-01_AUTHORITY_DECISION.json"
G8 = ROOT / "docs/council/submissions/GCL-POS-01/reviews/REV-GCLPOS-G8-001.yaml"
G9 = ROOT / "docs/council/submissions/GCL-POS-01/reviews/REV-GCLPOS-G9-001.yaml"
INDEX = ROOT / "docs/council/submissions/GCL-POS-01/reviews/REVIEW_INDEX.yaml"
CONFORMANCE = ROOT / "docs/council/submissions/GCL-POS-01/conformance/GCL-POS-01.conformance.yaml"
MANIFEST = ROOT / "docs/council/submissions/SUBMISSION_MANIFEST.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bounded_pilot_authority_decision() -> None:
    record = json.loads(read(DECISION))
    assert record["operation_id"] == "GCL-TCS-00-GCL-POS-01-G8-G9-001"
    assert record["disposition"] == "APPROVE_CANDIDATE_PILOT_RELEASE"
    assert "protected_merge" in record["effective_condition"]

    tcs = record["artifacts"]["GCL-TCS-00"]
    pos = record["artifacts"]["GCL-POS-01"]
    assert tcs == {
        "version": "0.1.0",
        "version_status": "candidate",
        "authority_status": "admitted",
        "promotion_status": "promoted",
        "sha256": "ea750b9b80b53c7d6ed755978fa4bdf59413fad93cec1db81eb3238372ce61c9",
        "authorized_use": "bounded_candidate_pilot",
    }
    assert pos == {
        "version": "0.1.0",
        "version_status": "candidate",
        "authority_status": "admitted",
        "promotion_status": "promoted",
        "sha256": "d8be180052a48655a02612b0d6ca883067abe93f0391c4b9c6561a3867ad4d2c",
        "authorized_use": "bounded_institutional_position_accompanying_pilot",
    }
    assert record["g8"]["decision"] == "PASS"
    assert record["g8"]["reviewer_kind"] == "agent"
    assert record["g9"]["decision"] == "PASS"
    assert record["g9"]["exact_head_disposition_required"] is True
    assert record["pilot_obligations"]
    assert record["claim_boundaries"] and not any(record["claim_boundaries"].values())


def test_cross_record_projection_is_closed() -> None:
    g8 = read(G8)
    g9 = read(G9)
    index = read(INDEX)
    conformance = read(CONFORMANCE)
    manifest = read(MANIFEST)

    assert "decision: PASS" in g8
    assert "disposition: APPROVE_CANDIDATE_PILOT" in g8
    assert "openai-gpt-5.6-thinking-referee" in g8
    assert "decision: PASS" in g9
    assert "APPROVE_CANDIDATE_PILOT_RELEASE" in g9
    assert "exact-head Human Steward disposition" in g9
    assert index.count("decision: PASS") == 10
    assert "authority_status: admitted" in conformance
    assert "promotion_status: promoted" in conformance
    assert "automatic doctrine replacement" in conformance
    assert "APPROVED_FOR_BOUNDED_CANDIDATE_PILOT_PENDING_PROTECTED_MERGE" in manifest
    assert "No formal ASD-STE100 compliance claim" in manifest
    assert "No mathematical, certification, novelty, priority, deployment, product, manufacturing, or commercial authority" in manifest


def test_mutations_fail_expected_invariants(tmp_path: Path) -> None:
    record = json.loads(read(DECISION))

    record["claim_boundaries"]["formal_asd_ste100_compliance"] = True
    mutated = tmp_path / "mutated.json"
    mutated.write_text(json.dumps(record), encoding="utf-8")
    loaded = json.loads(read(mutated))
    assert any(loaded["claim_boundaries"].values())

    record = json.loads(read(DECISION))
    record["artifacts"]["GCL-TCS-00"]["version_status"] = "authoritative"
    assert record["artifacts"]["GCL-TCS-00"]["version_status"] != "candidate"

    record = json.loads(read(DECISION))
    record["g9"]["exact_head_disposition_required"] = False
    assert record["g9"]["exact_head_disposition_required"] is not True
