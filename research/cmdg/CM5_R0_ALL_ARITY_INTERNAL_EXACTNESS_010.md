# CMDG CM5 R0 — all-degree internal exactness of genuine Stonean Čech free modules

**Source status:** `LOCAL_LEAN_VERIFIED__PROTECTED_EXACT_HEAD_AND_MATHCERT_PENDING`. Separate from a completed augmented/Ext resolution.

## Actual theorem

For each profinite `T`, its protected canonical Stonean presentation `p : P(T) ⟶ T`, and **every** natural number `n`, the genuine all-tuples closed equal-image relation free-condensed Čech sequence

`F(R_(n+3)(P(T)/T)) → F(R_(n+2)(P(T)/T)) → F(R_(n+1)(P(T)/T))`

is exact **internally in the actual abelian category of condensed modules**. The genuine categorical alternating face boundaries are imported directly from the upstream all-degree chain complex. The endpoint is `uniformStoneanFreeCechInternalExact`, with `ShortComplex.Exact` type in `Ambient`, not a pointwise or scalar Hom surrogate.

The proof works uniformly in `n`; it does not interpolate from the individually proved degrees one–four.

## Proof ladder and sources

1. `UniformShortExactFromHomotopy`: a middle-term categorical identity `h ≫ f + g ≫ k = 𝟙` implies the **actual** kernel/cokernel criterion for `ShortComplex.Exact`.
2. `UniformSplitCechTuple`: all-arity compatible tuples for any surjective split set map `A → B`, face deletion, inserted-section extra degeneracy, both simplicial interaction identities.
3. `UniformSplitCechBarExact`: actual free-module alternating differential squares to zero; the explicit signed homotopy contracts the degree-uniform bar and proves every middle term exact in `ModuleCat`.
4. `UniformProbeTupleComparison`: for **any** Stonean test `U` and any profinite `P ⟶ T`, a genuine equivalence `Hom(U,R_n) ≃ compatible tuples(Hom(U,P) → Hom(U,T))` in **every degree**, and verification that **each face** commutes. No fake identification between sheafified sections and the un-sheafified free module is made.
5. `UniformStoneanInternalExact`: the protected Stonean projectivity supplies a section of `Hom(U,P(T)) → Hom(U,T)`; the actual represented free-module probe short complex is isomorphic to the split bar at all degrees. The genuinely restricted presheaf short complex is therefore exact objectwise on **every** Stonean probe.
6. `UniformInternalExactnessTransfer`: exact Stonean sheafification and the pinned Stonean/CompHaus dense-site equivalence transfer the preceding source-level short-complex exactness to the **genuine free condensed modules**. Face signs and naturality are checked for arbitrary degree; not assumed.

All six new source modules were freshly compiled as imported Lean 4.33.0-rc1 modules, in dependency order. The main theorem's `#print axioms` reports only `[propext, Classical.choice, Quot.sound]`; no `sorry`, `admit`, or introduced axiom. The exact main proof-module SHA-256 is `17fc17d23a4ead1c30a8446dd299ce941d7dc9db312e6cb3ee37a58ddd7c3bd0`.

## Still substantive

**Augmented exactness at degree zero:** the immediate upstream chain/augmentation module proves `F(R_0) ↠ F_T` and `d_1 ≫ augmentation = 0`. A separate formal proof of `im(d_1)=ker(augmentation)` remains to close the augmented complex, using either the same Stonean-site contraction with a degree-(-1) section or the protected genuine relation-to-kernel epimorphism and comparison.

**Derived Ext validity:** the relation terms `F(R_n)` are not claimed projective. A legitimate **relative `G_S`-Ext-acyclic resolution** requires proving all positive Ext from *each* term into `G_S` vanish (using internal exactness and the already protected Ext¹ theorem plus the all-degree genuine solid Čech Hom exactness), or establishing a genuine projective replacement with a fully proved comparison. No derived-solid conclusion is claimed here.

**Disposition:** `TRUE_INTERNAL_EXACTNESS_ALL_DEGREES_LEAN_VERIFIED__AUGMENTATION_DEGREE_ZERO_AND_EXT_ACYCLICITY_OPEN`.
