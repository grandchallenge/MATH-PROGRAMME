# CMDG CM5 R0 — actual derived comparison morphisms and mapping-out equivalence

**Status:** `LOCAL_LEAN_VERIFIED__EXACT_HEAD_CI_REPLAY_PENDING__MATHCERT_PENDING`. A substantive derived-equivalence claim must not be promoted to a completed Lean certificate until its exact new source compiles and is read back. The standing upstream exact augmented resolution and all-positive Ext-acyclicity certificate are in PR #3584, exact head `94e65cd5c8c6ee75262080113c430352cb381b2b`; its formal-validation run `44697822181` succeeded. Protected admission and MATHCERT are separate.

## Objects and actual maps

Let `Ambient` denote the abelian category of genuine condensed modules over the pinned integer coefficient ring. For each profinite space `T`, let `P(T) -> T` be its canonical Stonean presentation and `R_n(T)` its genuine equal-image tuple spaces of cardinality `n+1`. Define `C_n(T) = F(R_n(T))`, with the already formalized true alternating face-map differential `d_n : C_(n+1)(T) -> C_n(T)` and the categorical augmentation `epsilon_T : C_0(T) -> F_T`. Let `G_S = (Condensed.profiniteSolid R).obj S`, an actual condensed-module object.

The exact comparison morphism of nonnegative chain complexes is

```text
epsilon_T^chain : C_*(T) -> F_T[0]
degree 0: epsilon_T
degree n>0: zero
```

The morphism property holds because `d_0 >> epsilon_T = 0` was established as an actual equality of condensed-module morphisms in PR #3579. The new generic Lean constructor `chainAugmentation` uses `ChainComplex.toSingle₀Equiv` to produce this map, while `cechDerivedMap` specializes it to genuine Stonean free-condensed objects, not scalar section complexes.

## Quasi-isomorphism and localized inverse

The upstream `uniformStoneanFreeCechFullAugmentedExact T` proves all triples `C_(n+2) -> C_(n+1) -> C_n` are internally exact, `C_1 -> C_0 -> F_T` is exact, and `epsilon_T` is epi. Therefore the component at homology degree zero is an isomorphism and the positive homology objects of `C_*(T)` vanish. Since the target `F_T[0]` has the identical degree-zero homology and zero higher homology, `epsilon_T^chain` is a quasi-isomorphism at EVERY degree.

Its image under the canonical localization functor `Q` from nonnegative chain complexes into the localization at quasi-isomorphisms is consequently invertible:

$$
Q(\epsilon_T^{\mathrm{chain}}):
Q(C_*(T))\xrightarrow{\ \cong\ } Q(F_T[0]).
$$

This is a genuine map and actual derived-localized equivalence, not only an equality of Ext groups. The locally compiled Lean theorems are `chainAugmentation_quasiIso`, `localizedDerivedComparison_isIso`, `cechDerivedMap_quasiIso`, and `cechDerivedMap_localized_isIso`. The last is an isomorphism in the localization of NONNEGATIVE chain complexes; transfer to the usual unrestricted `D(Ambient)` via the appropriate canonical functor is a distinct API bridge, not silently presumed.

## Mapping-out comparison: explicit roof and why it is an equivalence

Choose a genuine injective resolution `G_S -> I^*` in `Ambient`. Write `Hom^*(C_*(T), I^*)` for the product-totalized Hom double complex with degree `p+q` terms `Hom(C_p(T), I^q)`; the chosen nonnegative gradings give a first-quadrant bicomplex, so each total degree has finitely many summands. Let `Hom^*(C_*(T),G_S)` denote the ordinary cochain complex of categorical maps into `G_S`.

Construct the following actual arrows of cochain complexes (not simply cohomology-group isomorphisms):

$$
\mathrm{Hom}^{*}(C_*(T),G_S)
\xrightarrow{\ i_*\ }
\mathrm{Tot}\mathrm{Hom}(C_*(T),I^{*})
\xleftarrow{\ \epsilon_T^*\ }
\mathrm{Hom}(F_T,I^{*}).
$$

The left arrow is a quasi-isomorphism because `Ext^q(C_p(T),G_S)=0` for every `p` and every `q>0` (upstream `cechTerm_extPositive_genuineSolid_zero`), so the vertical-cohomology spectral sequence of the first-quadrant Hom bicomplex degenerates at the `q=0` row. The right arrow is a quasi-isomorphism because `epsilon_T^chain` is a quasi-isomorphism and `I^*` is a K-injective target; applying `Hom(-,I^*)` sends quasi-isomorphisms to quasi-isomorphisms. The spectral sequence convergence is ordinary first-quadrant convergence; there is no hidden unbounded-product assumption.

Invert the right arrow *in the derived category of abelian groups* to obtain the canonical, explicitly defined roof:

$$
\Phi_{T,S}
=(\epsilon_T^*)^{-1}\circ i_* :
\mathrm{Hom}^{*}(C_*(T),G_S)
\xrightarrow{\ \cong\ }
\mathbf R\mathrm{Hom}(F_T,G_S).
$$

Its inverse is represented by the reverse roof. Independence of the chosen injective resolution is guaranteed by the canonical derived-functor comparison maps between injective resolutions. This mathematical construction is valid for arbitrary profinite `T,S`. The statement applies only to `G_S` and, by analogous evidence, to other coefficient objects shown to be acyclic against every term. It is NOT a blanket claim about all coefficients.

## What the comparison does NOT prove

1. The new `C_*(T) -> F_T[0]` map is the **Čech augmentation**, not the entirely distinct **solidification unit** `F_T -> G_T`. The latter need not be an isomorphism in the ambient derived category, so promoting it as such is mathematically incorrect.
2. The asserted RHom roof is proved here as a standard exact-resolution and acyclic-resolution argument. Its construction as a morphism of actual Lean `DerivedCategory` Hom complexes, with chain-level injective-resolution naturality, is a distinct **remaining Lean-formalization obligation**. Formalizing only the localization of the Čech augmentation is NOT by itself Lean verification of the entire RHom roof.
3. The target `G_S` is not automatically equipped with a proved `CondensedMod.IsSolid` instance in the upstream library; its solidarity and the full unit-induced derived mapping-out equivalence must be addressed separately.
4. No genuine projectivity is assumed for `C_n` when `n>0`; the prior proof gives Ext-acyclicity RELATIVE to `G_S` instead.
5. Source-semantic independent MATHCERT review, protected merge, and unrestricted derived solidification remain separate gates.

**Operational:** Source-locked Lean modules `CMDGCondensedCM4P3DerivedCM5R0UniformDerivedComparisonGeneric.lean` and `CMDGCondensedCM4P3DerivedCM5R0UniformDerivedComparisonActual.lean` are pinned to the `cmdg-cm4-p3` formal lane; the routing classifies new formal files in that fixture tree. The local compiler was successful; exact-GitHub-head replay is independently required before protected admission. Treat compiler failures as repair and replay targets, not as proof of this theorem.

