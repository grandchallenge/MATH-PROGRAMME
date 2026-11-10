# CMDG CM5-R0 — exact negative-shift source reduction and biduality gates 004

**Status:** SOURCE-PINNED RESEARCH-OBLIGATION REDUCTION. No Lean theorem or derived-solid certification is conferred by this note. The protected prior results are the zero/nonnegative shifted comparisons and all-shift comparisons for finite profinite probes.

## Source identity and scope

Peter Scholze, *Lectures on Condensed Mathematics*, **May 2026** stable edition, [publisher-hosted PDF](https://people.mpim-bonn.mpg.de/scholze/Condensed.pdf), printed page **35**, Proposition **5.7**, with Corollary **5.5** on printed page 34 and Theorem **4.3** cited in the proof. The downloaded 802,829-byte PDF had SHA-256:

`d422561285f3025a53ee71a497d350fc89afaefe28053de78e2255b2d521c69d`

This is an exact source-content identity observed 2026-11-10, **not** independent SOURCE-SEMANTIC approval of GCL's Lean object. Any later source change requires new source verification. Distinguish this edition's **Proposition 5.7** from historical GCL references to “0.5.7”; do not assume numbering equivalence alone.

The actual GCL target, for `S T : Profinite.{u}`, uses the protected universe-lifted integer coefficient `Coeff := ZLift`, the free condensed module `F_T := (Condensed.profiniteFree Coeff).obj T`, and the free solid candidate `G_T := (Condensed.profiniteSolid Coeff).obj T`. The morphism `F_T → G_T` is the pinned `Condensed.profiniteSolidification` component. The protected CM4 target is `A_S := G_S`. The **first negative source shift**, `comparisonAtShift S T (-1)`, is the existing derived-category map on morphisms induced by the shifted solidification arrow.

## What the source actually proves

Proposition 5.7 proves the stronger *derived/complex* solidity claim for the source objects. Its proof provides a specific strategy for **arbitrary** profinite `S,T`:

1. **Reduce the target to integers.** Corollary 5.5 writes the source free solid group on `S` as a product of copies of the integers. The required derived-Hom mapping into that product is reduced to the case of a **single target integer group**. The corresponding product/derived-Hom comparison and its universe realization must be independently established in Lean.
2. **Compute the ordinary free side.** The source identifies higher `Ext^i(Z[T], Z)` with `H^i(T,Z)`, zero for positive `i` for profinite `T`. Its degree-zero Hom is `C(T,Z)`, a free abelian group expressed as a direct sum of copies of the integers by the Nöbeling argument.
3. **Compute the solid free side.** The source identifies the free solid group on `T` with a product of integer groups, dual to the locally constant functions from `T` into the integers. The decisive map is the **canonical derived biduality map**, not merely some existence of an abstract isomorphism.
4. **Prove derived biduality using real coefficients.** The source uses the short exact sequence of products of condensed groups: products of integers into products of reals, followed by products of real-mod-integer circles. Theorem 4.3 supplies (i) derived Hom from the product of reals into integers is zero, and (ii) derived Hom from the product of real-mod-integer circles into integers is a direct sum of integers shifted by minus one. The resulting distinguished triangle computes derived Hom from a product of integers into the integers as the expected degree-zero direct sum.
5. **Verify the actual comparison map.** These computations must identify the map *induced by solidification* with the derived biduality equivalence. Isomorphic source and target groups alone do not prove that this particular comparison is an isomorphism. All naturality, variance, and integer-universe transport must be checked.

**Consequence of the source proof, not yet of GCL's Lean development:** for these special source/target families, both derived Hom complexes are concentrated in degree zero. Thus in particular the two degree-one Ext groups vanish and their comparison is bijective. The arbitrary-profinite first negative shift is therefore solvable by **two source-grounded vanishing calculations and a naturality comparison**, not by extrapolating the finite-test isomorphism.

## Actual pinned Lean status

The installed mathlib `79d0395a1825a6264ad5d269e35e60537518955e` provides `CategoryTheory.Abelian.Ext`, `Ext.mk₀`, `Ext.precomp`, `Ext.homEquiv`, and the canonical derived-category shift interfaces. GCL's protected CM5 proofs establish:

- `comparisonAtShift_zero_bijective`: actual zero-shift comparison.
- `comparisonAtShift_nonneg_bijective`: every nonnegative source shift.
- `comparisonAtShift_finite_bijective`: every integer shift **only for finite profinite test objects**.

The [Ext¹ comparison candidate PR #3195](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3195) defines the actual contravariant pullback of degree-one extensions along `F_T → G_T`, for arbitrary `T`. Its current status must be read from the PR, **not** inferred from this note. The equation identifying that map with `comparisonAtShift S T (-1)` through mathlib's `Ext.homEquiv` and canonical shift isomorphisms requires a separately compiled **naturality square**. No extension-class vanishing for infinite `T` is presently conferred.

## Smallest next proof obligations, ordered

| Gate | Exact result to obtain | Failure mode to test |
| --- | --- | --- |
| CM5-E1, API and naturality | Compile the explicit Ext¹ pullback and prove the **commuting square** with `comparisonAtShift ... (-1)` through the canonical shift equivalence | A bijection chosen abstractly rather than the solidification-induced one |
| CM5-E2, free-side vanishing | Show `Ext¹(F_T, ZLift)=0` for arbitrary profinite `T`, with the precise sheaf-cohomology equivalence `H¹(T,Z)=0` | Confusing a finite-probe result or generic condensed-module projectivity with arbitrary-profinite acyclicity |
| CM5-E3, solid-side vanishing | Prove the pinned version of derived biduality for `G_T` using the products-of-reals/real-mod-integers exact sequence and Theorem 4.3 dependencies | Assuming `RHom(R,Z)=0`, unproved exactness of products, or generalized coefficient claims |
| CM5-E4, transport | Reduce target `G_S` to products of integer targets via Corollary 5.5, including the derived Hom-to-product comparison, and combine E1–E3 to obtain n = -1 for arbitrary `S,T` | Dropping universe/cardinality restrictions, product exactness, or source-to-mathlib realization |
| CM5-E5, review and admission | Full pinned theorem-level compiler replay, axiom footprint, noncircular dependency audit, source-semantic review, and appropriate protected admission | Conflating source truth, Lean compilation, and external mathematical certification |

**No finite-to-infinite inference is permitted without E2–E4.** In particular, agreement of Ext¹ maps on all embedded finite sets does not prove the derived comparison for arbitrary profinite sets, nor does the exact one-point computation transfer to products without the product/derived-Hom bridge.

## Immediate executable successor

Finish PR #3195's exact-head Lean replay and protected integration *if valid*. Next build a minimal E1 Lean module with a natural equivalence from degree-one `Abelian.Ext` to `Hom(X[-1],Y[0])` and a proof that its solidification square commutes. In parallel, inventory exact mathlib declarations and source-locked witnesses needed for the E2 sheaf-acylcity and E3 derived-biduality steps; do not introduce free axioms or close E4 by assigning the conclusion as a hypothesis.

**Terminal boundary:** `CM5_R0_ARBITRARY_PROFINITE_NEGATIVE_SHIFT_UNPROVED`. Neither Proposition 5.7 nor Theorem 5.8 is claimed as newly proved by GCL.
