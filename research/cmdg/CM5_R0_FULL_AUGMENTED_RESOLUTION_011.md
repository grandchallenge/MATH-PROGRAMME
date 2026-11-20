# CMDG CM5 R0 — full augmented exactness of the genuine Stonean Čech free-module complex

**Status:** `ALL_DEGREES_AUGMENTED_EXACT_LEAN_VERIFIED__PROTECTED_CI_PENDING__EXT_ACYCLICITY_DISTINCT`.

## Actual categorical theorem

`uniformStoneanFreeCechFullAugmentedExact (T : Profinite)` is a Lean theorem in the actual abelian category of condensed modules, with NO unproved mathematical assumption. Let `P=P(T)` be the canonical Stonean presentation of any profinite `T`. For the genuine related-tuple objects `R_n(P/T)`, let `C_n=F(R_n)` and genuine all-face alternating free-module boundary `d_{n+1}:C_(n+1)→C_n`, with true augmentation `ε:C_0→F_T`. The theorem establishes all three simultaneously:

1. **All internal exactness:** `ShortComplex.Exact (C_(n+2)→C_(n+1)→C_n)` for every `n:ℕ`, proved in source-locked prior stacked PR #3581.
2. **Degree-zero augmentation exactness:** `ShortComplex.Exact (C_1→C_0→F_T)` in the genuine condensed-module category, newly formalized here.
3. **Epimorphic augmentation:** `Epi ε`, relying on the already protected canonical Stonean presentation.

The source also provides exact categorical complex `uniformFreeRelationChainComplex` and categorical `d²=0` from upstream PR #3579.

## Proof newly added at zero degree

- `UniformSplitCechAugmentation` constructs an actual free-module split Čech bar `C_1→C_0→Free(B)`. Its set-level section inserts the split lift into the first coordinate and proves `h_0d_1 + εs=1` on the ACTUAL module maps. `splitBarZeroShortExact` gives genuine `ShortComplex.Exact` for arbitrary split set map.
- `UniformAugmentationExactTransfer` proves signed presheaf augmentation and face compatibility, exact source-level Stonean restriction ⇒ actual internal condensed-module degree-zero exactness, using the protected exact sheafification and dense-site comparison.
- `UniformProbeAugmentationExact` identifies each true represented Stonean probe's degree-zero bar and augmentation with its split-set free bar, proves all-face and augmentation naturality, applies the protected split epi of the Hom-set presentation, and transfers true probe exactness to `uniformStoneanFreeCechAugmentationExact`. The combined `uniformStoneanFreeCechFullAugmentedExact` closes every term, including augmentation.

All three newly authored modules passed imported-module pinned Lean 4.33.0-rc1 replay, with `#print axioms` reporting `[propext, Classical.choice, Quot.sound]`; no `sorry`, `admit`, or new axiom. Exact full theorem source SHA256: `19366ea0a1aa6c45842b9a5ab41698d1700ebe9c8f4afbb0788a6fa04669231a`.

## What this does and does NOT finish

The **augmented resolution is now categorically exact**. But the relation terms `F(R_n)` are not asserted projective; products/fibre products of Stonean compact spaces are not automatically Stonean. To use this exact complex as a valid Ext-computing resolution for the actual free-solid target `G_S`, still prove **positive Ext-acyclicity of every term against `G_S`**, or construct a separate projective replacement with an independently verified comparison.

An available noncircular route: the protected `Ext¹(F_X,G_S)=0` for EVERY profinite `X` plus source-locked #3577 all-degree true free-solid Čech Hom exactness imply `Ext¹(K_n,G_S)=0` for every syzygy `K_n` of the *now exact augmented chain*: pull a kernel morphism back along the true epi `C_(n+1)↠K_n`, solve its actual Čech Hom cocycle via #3577, and descend the primitive by epic cancellation. Uniform induction on Ext degree using LES for successive syzygies then yields higher Ext vanishing for all profinite free terms, and hence each `C_n` is `G_S`-Ext-acyclic. This is a **mathematical proof route**, not yet certified or formalized as Lean higher-Ext vanishing in this PR. The existence, epi/exactness and LES bridges must be formally checked before an Ext-acyclic claim.

Independent source-semantic/MATHCERT and protected admission remain separate.

**Disposition:** `TRUE_AUGMENTED_CECH_FULLY_EXACT_LEAN_VERIFIED__HIGHER_EXT_ACYCLICITY_PROOF_PENDING`.
