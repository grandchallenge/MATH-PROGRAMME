#!/usr/bin/env python3
"""Protected-main, exact-evidence decisions for competing current valid returns.

An arbitration selects a bounded *queue source*, never mathematical truth or
theorem certification. All competing comments remain preserved. A source-review
specialist must first supply a substantive, falsifiable comparison in a
protected PR; worker claims and raw issue comments are not admission authority.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"governance/erdos_catalogue/RETURN_ARBITRATIONS.json"
SCHEMA="GCL-ERDOS-RETURN-ARBITRATION/1"


def read_decisions(path=REGISTRY):
    doc=json.loads(Path(path).read_text())
    if (doc.get("schema")!=SCHEMA or
        doc.get("authority")!="PROTECTED_MAIN_SOURCE_REVIEW_ONLY" or
        doc.get("mathematical_certification") is not False or
        doc.get("source_semantics_accepted") is not False or
        not isinstance(doc.get("decisions"),list)):
        raise ValueError("arbitration registry authority drift")
    out={}
    for decision in doc["decisions"]:
        issue=decision.get("issue_number")
        if type(issue) is not int or issue<1 or issue in out:
            raise ValueError("duplicate or invalid arbitration issue")
        out[issue]=decision
    return out


def choose(issue, current_rows, *, decisions=None):
    """No newest-wins or first-return rule; reject absent/stale adjudication."""
    choices={r["comment_id"]:r["comment_body_sha256"] for r in current_rows}
    if len(choices)!=len(current_rows) or len(choices)<2:
        raise ValueError("arbitration requires distinct current valid comments")
    ledger=read_decisions() if decisions is None else decisions
    decision=ledger.get(issue)
    if decision is None:
        raise ValueError(f"#{issue}: multiple valid returns; protected source arbitration missing")
    expected={str(cid):digest for cid,digest in sorted(choices.items())}
    comparison=decision.get("comparative_review","")
    specialist=decision.get("source_specialist","")
    rationale=decision.get("selection_rationale","")
    if (decision.get("disposition")!="SELECT_FOR_QUEUE_ONLY"
        or decision.get("candidate_comment_sha256")!=expected
        or decision.get("selected_comment_id") not in choices
        or not isinstance(specialist,str) or len(specialist)<3
        or not isinstance(comparison,str) or len(comparison.strip())<160
        or not isinstance(rationale,str) or len(rationale.strip())<80
        or decision.get("protected_review_pr","").startswith(
                "https://github.com/grandchallenge/MATH-PROGRAMME/pull/") is False
        or decision.get("source_claim_accepted") is not False
        or decision.get("mathematical_certification") is not False):
        raise ValueError(f"#{issue}: protected specialist decision absent, stale, or incomplete")
    return next(r for r in current_rows if r["comment_id"]==decision["selected_comment_id"])
