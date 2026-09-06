# Volume I RC1.1 — Gate 8 Independent Mathematical Review

This directory is the durable review docket for **Volume I — JUDGMENT: The Grammar of Computation**, RC1.1.

It exists to support the series transition

`RC_DURABLY_ADMITTED -> RC_REVIEW_QUALIFIED`

and does **not** itself complete that transition.

## Exact review target

- rebuild-core SHA-256: `013fd6b5f78a8bb45711bb9e167321f7ca58324b7a0ae3f0c7e594ba63a96e3b`
- exact `main.tex` SHA-256: `ceb02e6c84011615c7557c9bf4bba391290f43d6d54d9c5033dab9215af14d01`
- protected source-admission commit: `0b18341a7536d021b6ab007c033a72b32e3ff7e1`
- protected RC1.1 release tree: `3a7dbb5d0990b75ce15c70daa91b232138b3a9a0`
- durable-state record commit: `c2911113beaf58c17e2d88a908021d66dcf9a7bf`
- release path: `monographs/type-theory/volume-i-judgment/releases/RC1.1`
- tracking issue: `#859`

## Canonical review order

1. Read `GATE8_REVIEW_PACKET.md`.
2. Read `THEOREM_REVIEW_MATRIX.json`. It is a coverage/index document, not an endorsement of the internal proofs.
3. Reconstruct the exact rebuild core from the protected release with `releases/RC1.1/RECONSTRUCT_SOURCE.py`.
4. Verify the reconstructed archive size and SHA-256 before review.
5. Review the exact `main.tex`, complete solutions source, and plate sources. Use any separately obtained audit/evidence package only as secondary evidence, never as a substitute for mathematical checking.
6. Record findings in a copy of `REVIEW_RECORD_TEMPLATE.yaml`.
7. Submit the completed review record through protected repository controls, bound to the exact target identity above.

## Independence boundary

A review produced by the same composing process, a repeat internal audit, CI, regression tests, or machine-assisted checking alone does not satisfy Gate 8. The reviewer may use computational tools, but the final mathematical judgment must be attributable to a genuinely distinct reviewer who declares independence and conflicts.

## Durable-scope note

The durably admitted RC1.1 object is the exact **rebuild core**: manuscript source, solutions source, plate-folio source, all 42 plate sources, and an internal source manifest. The historical publication/exercise/cosmetic audits and executable evidence have separately pinned identities in `docs/monographs/type-theory-series/REFERENCE_BASELINE.json`, but are not duplicated inside this rebuild-core archive. A reviewer who does not obtain those secondary materials must record that limitation rather than infer their contents.

## State boundary

Until an independent review record is admitted and its exact revision binding is checked, Volume I remains:

- composition: `RC_COMPOSITION_COMPLETE`;
- durable admission: `RC_DURABLY_ADMITTED`;
- independent review: `PENDING_EXTERNAL_MATHEMATICAL_REVIEW`;
- publication authority: `NOT_GRANTED`.

Passing Gate 8 would permit only `RC_REVIEW_QUALIFIED`. Publication authority remains a separate transition.
