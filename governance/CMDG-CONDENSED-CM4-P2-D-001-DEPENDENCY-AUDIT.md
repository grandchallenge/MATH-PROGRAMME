# CMDG-CONDENSED-CM4-P2-D-001 — exact-tree dependency audit supplement

This supplement records one material dependency exposed by the successful exact-head P2-D kernel replay and is part of the governed P2-D evidence package.

## Sixth reconstruction locus — closed self-enrichment

`Mathlib/CategoryTheory/Monoidal/Closed/Enrichment.lean`  
blob `6083cfbfd92a9e274a6559de438d43e2a3ac600d`

Machine-usable declarations:

- `MonoidalClosed.enrichedCategorySelf`;
- `MonoidalClosed.enrichedOrdinaryCategorySelf`.

Role: the P2-D fixture activates `open scoped CategoryTheory.MonoidalClosed`. This supplies the self-enriched and enriched-ordinary structures required by `functorEnrichedHom` for the closed module category. The dependency is structural only; it introduces no new mathematical axiom, basis choice, product presentation, or P2-E comparison.

The exact P2-D replay on candidate head `b6c539dc2ff1697fe245897a3c79bb086f31fd0b` completed successfully under the pinned Lean/mathlib tree and printed the following declaration-level axiom sets:

- `measurePresheafObj_isSheaf`: `[propext, Classical.choice, Quot.sound]`;
- `measurePresheafFunctor`: `[propext, Classical.choice, Quot.sound]`;
- `measureFunctor`: `[propext, Classical.choice, Quot.sound]`;
- `dualityHomEquiv`: `[propext, Classical.choice, Quot.sound]`.

In particular, none depends on `sorryAx`.

This supplement does not change the candidate disposition `P2_D_RECONSTRUCTED_PENDING_PROTECTED_ADMISSION` and does not establish P2-E, close P2, or broaden any CM4/C04/C06/global CMDG claim.