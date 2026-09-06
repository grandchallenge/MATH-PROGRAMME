# Volume II RC1 — Gate 8 Independent Mathematical Review

This directory is the durable review docket for **Volume II — COMPREHENSION: How Computational Worlds Are Built**, RC1.

It exists to support the series transition

`RC_DURABLY_ADMITTED -> RC_REVIEW_QUALIFIED`

and does **not** itself complete that transition.

## Exact review target

- source archive SHA-256: `1e1f4ae917e50514dc0a74fa706d30ad0d1c3dbf9ac2f45d7c8ad2445f3fd95a`
- protected admission commit: `3615be3114ea3aceec14e02231e3a1647faa44b4`
- protected RC1 release tree: `8fae441820506bb6902e36c048cc475dc56242d5`
- release path: `monographs/type-theory/volume-ii-comprehension/releases/RC1`
- tracking issue: `#853`

## Canonical review order

1. Read `GATE8_REVIEW_PACKET.md`.
2. Read `THEOREM_REVIEW_MATRIX.json` without inheriting the internal audit's conclusions.
3. Reconstruct the exact source archive from the protected release using `releases/RC1/RECONSTRUCT_SOURCE.py`.
4. Verify the reconstructed archive size and SHA-256 before review.
5. Review `main.tex`, chapter sources, `CLAIMS_LEDGER.md`, `THEOREM_AUDIT.md`, and the relevant laboratory/evidence files.
6. Record findings in a copy of `REVIEW_RECORD_TEMPLATE.yaml`.
7. Submit the completed review record through protected repository controls, bound to the exact target identity above.

## Independence boundary

A review produced by the same composing process, a repeat internal audit, CI, regression tests, or machine-assisted checking alone does not satisfy Gate 8. The reviewer may use computational tools, but the final mathematical judgment must be attributable to a genuinely distinct reviewer who declares independence and conflicts.

## State boundary

Until an independent review record is admitted and the exact revision binding is checked, Volume II remains:

- composition: `RC_COMPOSITION_COMPLETE`;
- durable admission: `RC_DURABLY_ADMITTED`;
- independent review: `PENDING_EXTERNAL_MATHEMATICAL_REVIEW`;
- publication authority: `NOT_GRANTED`.

Passing Gate 8 would permit only `RC_REVIEW_QUALIFIED`. Publication authority remains a separate Gate 9 transition.