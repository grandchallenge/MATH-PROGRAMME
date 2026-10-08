#!/usr/bin/env python3
"""Fail-closed invariants for known exposition chronology and theorem-scope regressions.

This checks source-facing assertions. It does not infer mathematical authority,
pedagogical quality, or GitHub issue state from text.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE1_MERGE = "183ff2a0adfbe5bd0ffd5f2e638089b94b868c54"


def errors(root: Path = ROOT) -> list[str]:
    out: list[str] = []
    def read(path: str) -> str:
        return (root / path).read_text(encoding="utf-8")

    documentary = read("docs/documentaries/union_closed.md")
    old_quantifiers = (
        "every finite nonempty union-closed family",
        "Let $\\mathcal F$ be a finite nonempty union-closed family.",
    )
    if any(s in documentary for s in old_quantifiers):
        out.append("Union-Closed documentary uses an invalid unqualified nonempty-family quantifier")
    if "nonempty support" not in documentary or "empty-only family" not in documentary:
        out.append("Union-Closed documentary missing the empty-support exception and exact edge case")

    domain = read("docs/domains/union_closed.md")
    candidates = json.loads(read("docs/documentaries/DOCUMENTARY_CANDIDATES.json"))
    manifest = json.loads(read("docs/documentaries/ARTIFACT_MANIFEST.json"))
    if not (root / "docs/documentaries/union_closed.edition.json").is_file():
        out.append("Union-Closed admitted edition missing")
    if not (root / "docs/documentaries/union_closed.md").is_file():
        out.append("Union-Closed admitted page missing")
    if '"slug": "union_closed"' not in json.dumps(manifest):
        out.append("Union-Closed documentary missing admitted manifest volume")
    if candidates.get("candidates") != []:
        out.append("Candidate-registry state changed; re-audit its admission semantics")
    if "admitted full-tier documentary" not in domain:
        out.append("Union-Closed domain page has not advanced to admitted documentary status")
    if "no Union-Closed browser page" in domain or "UC-DOC-WP01 may continue construction" in domain:
        out.append("Union-Closed domain page still asserts pre-admission status")

    gcd = read("docs/EUCLID_GCD_E2E_001_PROOF_TRACE.md")
    if STAGE1_MERGE not in gcd or "EUCLID_DIOPHANTINE_E2E_002_PROOF_TRACE.md" not in gcd:
        out.append("GCD primary page missing terminal Stage 1 or admitted Stage 2 lineage")
    if "pending this closeout" in gcd or "linear Diophantine theorem remains blocked" in gcd:
        out.append("GCD primary page still asserts pre-merge Stage 1 status")
    candidate = json.loads(read("governance/euclid_gcd_e2e_001_closeout.json"))
    if candidate["programme"].get("authority_state") != (
        "candidate_programme_closeout_pending_exact_head_review_and_protected_merge"
    ):
        out.append("Historical GCD candidate authority field was rewritten rather than preserved")

    rows = json.loads(read("governance/research_surfaces.json"))["surfaces"]
    ym = next((r for r in rows if r["campaign_id"] == "YM-001"), None)
    if ym is None:
        out.append("YM-001 registry surface missing")
    else:
        stale = {f"https://github.com/grandchallenge/MATHSOLVE/issues/{n}" for n in (716,717,718)}
        if stale.intersection(ym["live"]["active_children"]):
            out.append("YM-001 lists completed contribution issues as live active children")
    return out


if __name__ == "__main__":
    problems = errors()
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)
    print("PASS: public theorem quantifier, documentary/GCD chronology, and YM child-tracker integrity")
