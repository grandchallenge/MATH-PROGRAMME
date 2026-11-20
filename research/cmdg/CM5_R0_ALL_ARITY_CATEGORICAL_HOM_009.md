# CMDG CM5-R0 — genuine all-arity free-condensed Čech Hom exactness

**Status:** `LOCAL_LEAN_VERIFIED__PROTECTED_ADMISSION_AND_MATHCERT_PENDING`

## Exact mathematical assertion

For every profinite morphism `p:P⟶T`, every `n:ℕ` and every genuine closed equal-image relation `R_n(P/T)`, the formal module `CMDGCondensedCM4P3DerivedCM5R0UniformCategoricalCechHom.lean` constructs:

- `uniformRelationProfinite P T p n` — the actual profinite object of related tuples, together with a genuine homeomorphism to the original closed relation subtype.
- `uniformRelationFace P T p n k` — genuine Profinite morphisms deleting coordinate `k` of the related tuple.
- `uniformFreeRelationBoundary P T p n : F(R_(n+1)) ⟶ F(R_n)` — the signed sum of genuine free-condensed morphisms induced by those faces, for **all degrees and all index orders**.
- `uniformFreeRelationBoundary_integerHom_scalar` — the **natural** exact scalar identification of actual Hom-precomposition by this categorical boundary with the genuine locally constant Čech differential.
- `uniformRelationScalarEquiv_diff` — the categorical and closed-subtype scalar complexes agree under the canonical homeomorphisms.
- `uniformFreeRelationBoundary_integerHom_exact` — any `g : F(R_(n+2)) ⟶ Z_disc` satisfying `B_(n+1) ≫ g = 0` has an actual `f : F(R_(n+1)) ⟶ Z_disc` with `B_n ≫ f = g`.
- `uniformFreeRelationBoundary_discreteProductHom_exact` — the same **categorical** Hom exactness for **any** product index `ι : Type (u+1)`, with coefficient target `∏ᶜ (_ : ι), Z_disc`. A common finite observation across coefficient coordinates is **not** assumed.
- `uniformFreeRelationBoundary_integerHom_sq_zero` and `uniformFreeRelationBoundary_discreteProductHom_sq_zero` — composition of two categorical boundaries vanishes **after Hom into the named discrete coefficient targets**.
- `uniformFreeRelationBoundary_solidHom_exact_of_discreteProductModel` — a separate theorem makes the coefficient-isomorphism input completely explicit, without introducing hidden assumptions.
- `uniformFreeRelationBoundary_genuineSolidHom_exact` — **unconditional all-positive-degree Čech Hom exactness for the actual free-solid object** `(Condensed.profiniteSolid R).obj S`, obtained by applying the **already protected true coefficient product isomorphism** `gsFreeSolidToCoefficientProductIso S` from `CMDGCondensedCM4P3DerivedCM5R0GSCondensedProduct.lean`. The source uses the real canonical enriched basis coefficient product, not a fictitious scalar-product model.

Every result is fully compiled on the pinned Lean 4.33.0-rc1 toolchain with real imported modules and Mathlib; all printed axiom dependencies are `[propext, Classical.choice, Quot.sound]`. The new source module has SHA-256 `cb08b973babe55f3eefb74e11d9cc874c08e598e012b87e07440c24032c86a21`, 419 lines, and no `sorry`, `admit`, or new axioms.

## Source closure and delivery

The categorical module builds on protected `CMDGCondensedCM4P3DerivedCM5R0DiscreteProductCechDifferential.lean`, the genuine free-product scalar equivalence, the already protected genuine free-solid coefficient product isomorphism `gsFreeSolidToCoefficientProductIso`, and the all-degree scalar genuine relation complex from **PR #3576**. The branch starts at **the exact #3576 source head** `554ed9193106fb6f7f91a78274fa88f413780c59`; it adds one mathematical module plus this note. On admission of upstream PR #3576, the new material increment is only the categorical module and this ledger; no synthetic copy drift or branch-protection changes are intended.

## Remaining independent mathematical obligations

**This document does not claim all-degree categorical Ext vanishing or derived solidity. The *free-solid coefficient model* and the all-degree free-solid *Čech Hom* exactness are now formally established; their application to Ext is separately unproved.** The following remain substantive and independently gated:

1. Establish the actual **augmented Čech relation resolution**, its categorical exactness/epimorphisms at the relevant profinite or Stonean probes, and the valid route from this Hom complex to Ext for every degree. A positive Čech Hom calculation is not itself an Ext computation.
2. Prove the categorical derived mapping-out comparison with actual free-solid targets and its exact source/target naturality.
3. Subject source semantics, external mathematical novelty and public claims to the independent MATHCERT review/certification lane.

**Disposition:** `UNIFORM_GENUINE_SOLID_CECH_HOM_ACYCLICITY_LEAN_VERIFIED__EXT_RESOLUTION_AND_DERIVED_COMPARISON_OPEN`.
