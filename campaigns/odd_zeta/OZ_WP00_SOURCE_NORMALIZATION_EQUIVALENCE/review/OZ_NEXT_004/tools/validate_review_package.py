#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load(name: str):
    p=ROOT/name
    if not p.is_file():
        raise SystemExit(f"missing review file: {p}")
    data=yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"invalid YAML root: {p}")
    return data

def main() -> int:
    register=load("REVIEW_REGISTER.yaml")
    index=load("CLAIM_COMPUTATION_INDEX.yaml")
    literature=load("THEOREM_LITERATURE_COMPARISON.yaml")
    if register.get("review_id") != "OZ-NEXT-004":
        raise SystemExit("wrong review_id")
    roles={r.get("role") for r in register.get("roles", [])}
    required={"Axiomatist","Cartographer","Grammarian","Verifier","Adversary","Formalist","Amanuensis","Referee"}
    if roles != required:
        raise SystemExit(f"role set mismatch: {sorted(roles)}")
    records=index.get("records", [])
    ids=[r.get("id") for r in records]
    if len(ids) != 43 or len(set(ids)) != 43:
        raise SystemExit(f"expected 43 unique non-literature records, got {len(ids)}")
    expected_counts={"OZ-MSS-":10,"OZ-REC-":3,"OZ-HAR-":4,"OZ-CON-":6,"OZ-L4-":8,"OZ-CER-":5,"OZ-CMP-":7}
    for prefix,count in expected_counts.items():
        actual=sum(1 for x in ids if isinstance(x,str) and x.startswith(prefix))
        if actual != count:
            raise SystemExit(f"{prefix} expected {count}, got {actual}")
    if literature.get("corpus_record_count") != 37 or len(literature.get("corpus_records", [])) != 37:
        raise SystemExit("literature corpus must contain 37 classified records")
    promotion=register.get("promotion", {})
    forbidden=(promotion.get("eligible"),promotion.get("wp00_complete"),promotion.get("novelty_authorized"),promotion.get("irrationality_claim_authorized"))
    if forbidden != (False,False,False,False):
        raise SystemExit("review must fail closed")
    sharp=next(r for r in records if r.get("id")=="OZ-MSS-S006")
    if sharp.get("independent_disposition") != "DOWNGRADE_REQUIRED":
        raise SystemExit("sharp-12 overstatement finding missing")
    print("OZ-NEXT-004 review package is structurally valid and fail-closed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
