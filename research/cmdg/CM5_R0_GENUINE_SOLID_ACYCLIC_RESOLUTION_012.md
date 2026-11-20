# CMDG CM5 R0 — valid Ext-acyclic Stonean Čech resolution relative to the genuine free-solid target

**Claim status:** `LOCAL_LEAN_VERIFIED__PROTECTED_EXACT_HEAD_CI_AND_MATHCERT_PENDING`. Mathematical source claims are evidence-qualified until protected admission and independent certification. Underived target, derived category, and public theorem status are separate.

## Exact final Lean theorem

`uniformStoneanCech_validGSAcyclicResolution T S` establishes for arbitrary profinite `T,S` in the **actual condensed-module abelian category**:

1. The true free-condensed `C_n(T) = F(R_n(P(T)/T))` genuine all-tuple relation Čech chain complex is internally exact at every positive term (all natural `n`).
2. Its genuine degree-zero augmentation `C_0(T) → F_T` has `im d_1 = ker ε` and is a categorical epimorphism.
3. Each and every Čech term `C_n(T)` is **acyclic against the actual free-solid target** `G_S = (Condensed.profiniteSolid R).obj S`:
   `∀ n q : ℕ, ∀ e : Abelian.Ext (C_n(T)) G_S (q+1), e=0`.

Thus the augmented complex is a **valid relative `G_S`-Ext-acyclic resolution**, *not* asserted to be a projective resolution. Higher Čech terms are not assumed projective and no false Stonean property of fibre products is used.

The stronger separate proved theorem `freeProfinite_extPositive_genuineSolid_zero T S q` states for ALL profinite `T,S` and positive degrees `q+1`:
`∀ e : Abelian.Ext (F_T) G_S (q+1), e=0`.

## Noncircular induction/proof dependency

- Full augmented categorical exactness: exact source-locked PR #3582 (itself stacked on #3581, #3579, #3577, #3576). Stonean-probe contracting homotopy and exact dense-site sheafification, including augmentation.
- Protected degree-one theorem: `freeProfinite_extOne_genuineSolid_vanishes`; actual coefficient product model `gsFreeSolidToCoefficientProductIso` and exact free-solid Hom identification.
- Actual every-degree categorical Hom exactness: `uniformFreeRelationBoundary_genuineSolidHom_exact` imported from #3577.
- `UniformKernelFactorShortExact`: factorization through a genuine epi followed by mono yields a real short exact sequence of kernel, middle, and quotient.
- `UniformCechSyzygyTower`: define actual syzygies `K_n(T)`, epis `C_(n+1)↠K_n`, and SES `0→K_(n+1)→C_(n+1)→K_n→0`. For every `K_(n+1)→G_S`, pull back along that epi, use actual categorical Čech Hom cocycle exactness, and descend the primitive by epi cancellation. This proves every such syzygy map extends to the adjacent Čech term.
- `UniformExtLongExactShift`: formalize the actual `Abelian.Ext` contravariant long exact sequence, proving (i) Ext¹ of quotient vanishes when Ext¹ of middle vanishes and left Hom extends, and (ii) higher Ext of quotient vanishes when the next Ext of middle and preceding Ext of left vanish.
- **Ext¹ base case:** protected Ext¹(F_X,G_S)=0 for any profinite X; every middle term C_n is such F_X. All syzygy Ext¹ follows by the genuine short exact sequences and extension lemma.
- **Successor induction q→q+1:** first show Ext^(q+2)(F_T,G_S)=0 using the true augmentation SES `0→K_0→C_0→F_T→0`, prior-degree syzygy vanishing, and **projectivity of C_0 alone**, proved via its actual canonical profinite isomorphism to the Stonean P(T) free module. Then show Ext^(q+2)(K_n,G_S)=0 for all n, using the syzygy SES, prior-degree `K_(n+1)` vanishing and the **already established current-degree** universal free-object vanishing for each related-tuple object. No use of the current-degree syzygy result in its own proof.
- Since each Čech term is `F_X` with X profinite, the universal free-object result proves its all-degree `G_S`-acyclicity.

## Exact local check / downstream gates

Four newly authored Lean modules were recompiled afresh in imported-module dependency order with the pinned Lean v4.33.0-rc1 and exact previously checked source dependencies. No `sorry`, `admit`, or new axioms. For `uniformStoneanCech_validGSAcyclicResolution`, `freeAndCechSyzygy_extPositive_genuineSolid_zero`, `freeProfinite_extPositive_genuineSolid_zero`, and `cechTerm_extPositive_genuineSolid_zero`, Lean's `#print axioms` gives only `[propext, Classical.choice, Quot.sound]`.

Exact source SHA-256 values:
- `UniformExtLongExactShift`: `86a8131603d04c38ea32b43eb18cf616c279321b7856f0cded4e9ee2d031e669`
- `UniformKernelFactorShortExact`: `2bdcf76511ef64d4814abbeee85b1efd22df3b3dae46a6b4a31999ef33f53aa6`
- `UniformCechSyzygyTower`: `850353867a30823bcaedd3d16b65da00d793bdbb74010ccbeb71d18a77c6da58`
- **`UniformGenuineSolidExtAcyclic`**: **`1f2eceda02f201f3be6a50244da46b855de5d077fe09616cd24b1b320069e707`**

## Precisely not asserted

No projectivity of general Čech terms or of Stonean presentation kernels. This result establishes **positive Ext vanishing** and a **valid relative Ext-acyclic resolution** for `G_S`, but it does not by itself establish the full functorial *derived mapping-out object*, the derived unit/counit map for solidity, or unrestricted public derived solidity. The related categorical derived comparison, source-semantic review, and MATHCERT independent public certification remain separate obligations. Do not confuse local Lean checking with protected source admission or external mathematical certification.

**Disposition:** `TRUE_FULL_AUGMENTED_GS_ACYCLIC_RESOLUTION_LEAN_VERIFIED__PROTECTED_ADMISSION_PENDING__DERIVED_COMPARISON_SEPARATE`.
