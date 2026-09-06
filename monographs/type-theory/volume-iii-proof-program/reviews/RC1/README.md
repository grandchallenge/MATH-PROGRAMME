# Volume III RC1 - Gate 8 Independent Mathematical Review

This is the reviewer landing page for **Volume III - PROOF / PROGRAM: Logic Becomes Executable**, RC1.

## Start here

**You do not need to compile the TeX.** The camera-ready manuscript PDF is the primary mathematical review surface. Source reconstruction and recompilation are optional verification/reproducibility paths.

- [Read the manuscript PDF](assets/01_PROOF_PROGRAM_RC1.pdf)
- [Read the solutions companion](assets/02_SOLUTIONS_COMPANION_RC1.pdf)
- [Read the 42-plate folio](assets/03_PLATE_FOLIO_RC1.pdf)
- [Read the reviewer start guide](REVIEWER_START_HERE.md)
- [Download the complete reviewer bundle](assets/GCL_Type_Theory_Volume_III_PROOF_PROGRAM_RC1_Reviewer_Bundle.zip)

The complete bundle contains the exact PDFs, the exact source archive, review packet, theorem-review matrix, review-record template, and optional build instructions.

## Recommended review order

1. Read `assets/01_PROOF_PROGRAM_RC1.pdf`.
2. Consult the solutions and plate folio where they bear on a claim.
3. Read `GATE8_REVIEW_PACKET.md`.
4. Use `THEOREM_REVIEW_MATRIX.json` as a coverage checklist only; do not inherit candidate conclusions.
5. Inspect source only when useful. If you use the source archive, verify SHA-256 `70c9ffedefa795cf40e2536c45db8a7f3fb0223719d4c6cf24f921e7637d7a62`.
6. Rebuild only if you want reproducibility evidence; compilation is not a Gate 8 prerequisite.
7. Return a completed copy of `REVIEW_RECORD_TEMPLATE.yaml`.

## Exact target

- source archive SHA-256: `70c9ffedefa795cf40e2536c45db8a7f3fb0223719d4c6cf24f921e7637d7a62`
- protected RC1 admission commit: `69fe9e649ea59c5bc1c27f816bb65f52c2627d79`
- protected RC1 admission release tree: `fd8ad170e47ef68ae4745d12b27a4200cc1e6be8`
- manuscript PDF SHA-256: `caf12162ff052db869356c8c0d0fa96dce77b8c40de3bf576e61a2fce30574f3`
- solutions PDF SHA-256: `2e1eae3596f7cb386dc2c93064bcc3d1c85f9511f46f49431ed9ede62836677e`
- plate folio PDF SHA-256: `ae718ef486fbee4a89fe5d498a48228d5499100d9e84d04bf67517fb520a0de0`
- reviewer bundle SHA-256: `17318481fdcf7ffbb10edf0d74ffe71397e609f15ab92f565bfed6c9baa679f3`
- review tracking issue: `#871`

`REVIEWER_ASSET_MANIFEST.json` records all reviewer-facing convenience-asset identities.

## Independence boundary

A review produced by the composing process, a repeat internal audit, CI, regression tests, rendered inspection, or machine-assisted checking alone does not satisfy Gate 8. Tools may support the review, but the final mathematical judgment must be attributable to a genuinely distinct reviewer who declares independence and conflicts.

## State boundary

Volume III remains `RC_DURABLY_ADMITTED` with `PENDING_EXTERNAL_MATHEMATICAL_REVIEW`. A successful Gate 8 disposition may support only `RC_REVIEW_QUALIFIED`; publication authority remains a separate Gate 9 transition and is `NOT_GRANTED`.
