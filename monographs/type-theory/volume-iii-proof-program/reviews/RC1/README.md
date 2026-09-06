# Volume III RC1 — Gate 8 Independent Mathematical Review

This directory is the durable review docket for **Volume III — PROOF / PROGRAM: Logic Becomes Executable**, RC1.

It supports the possible transition

`RC_DURABLY_ADMITTED -> RC_REVIEW_QUALIFIED`

and does **not** itself complete that transition.

## Exact review target

- source archive SHA-256: `70c9ffedefa795cf40e2536c45db8a7f3fb0223719d4c6cf24f921e7637d7a62`
- protected admission commit: `69fe9e649ea59c5bc1c27f816bb65f52c2627d79`
- protected RC1 admission release tree: `fd8ad170e47ef68ae4745d12b27a4200cc1e6be8`
- release path: `monographs/type-theory/volume-iii-proof-program/releases/RC1`
- review tracking issue: `#871`

## Canonical review order

1. Read `GATE8_REVIEW_PACKET.md`.
2. Read `THEOREM_REVIEW_MATRIX.json` as a navigation scaffold only; do not inherit the internal audit's conclusions.
3. Reconstruct the exact source archive from the protected release with `releases/RC1/RECONSTRUCT_SOURCE.py`.
4. Verify the reconstructed archive size and SHA-256 before substantive review.
5. Review `main.tex`, chapter sources, `CLAIMS_LEDGER.md`, `THEOREM_AUDIT.md`, and the relevant laboratory/evidence files.
6. Independently check imported theorem dependencies and the manuscript's explicit non-result boundaries.
7. Record findings in a copy of `REVIEW_RECORD_TEMPLATE.yaml`.
8. Submit the completed review record through protected repository controls, bound to the exact target identity above.

## Independence boundary

A review produced by the composing process, a repeat internal audit, CI, regression tests, rendered inspection, or machine-assisted checking alone does not satisfy Gate 8. Computational tools may support the work, but the final mathematical judgment must be attributable to a genuinely distinct reviewer who declares independence and conflicts.

## State boundary

Until an independent review record is admitted and its exact target binding is checked, Volume III remains:

- composition: `RC_COMPOSITION_COMPLETE`;
- durable admission: `RC_DURABLY_ADMITTED`;
- independent review: `PENDING_EXTERNAL_MATHEMATICAL_REVIEW`;
- publication authority: `NOT_GRANTED`.

A successful Gate 8 disposition may support only `RC_REVIEW_QUALIFIED`. Publication authority remains a separate Gate 9 transition.
