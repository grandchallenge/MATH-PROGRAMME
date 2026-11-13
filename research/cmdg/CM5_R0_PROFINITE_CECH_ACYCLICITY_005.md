# CMDG CM5 — profinite Čech acyclicity and the precise free-side Ext bridge

**Disposition:** classical topological argument recorded; **not** a new Lean proof of condensed Ext vanishing, not a source-semantic certification, and not CM5 closure.

**Exact governing target:** for any `T : Profinite`, prove `Extⁱ_{CondensedMod ZLift}(F_T,ZLift)=0` for `i>0`, with `F_T=(Condensed.profiniteFree ZLift).obj T`. The source-pinned route is Scholze, *Lectures on Condensed Mathematics* (May 2026), Proposition 5.7, the ordinary free-side part of the proof. Preserve the pinned source hash and provenance from [CM5_R0_NEGATIVE_SHIFT_BIDUALITY_SOURCE_004.md](CM5_R0_NEGATIVE_SHIFT_BIDUALITY_SOURCE_004.md).

## 1. A fully explicit disjoint-clopen refinement lemma

**Lemma.** Every open cover `𝒰` of a profinite space `T` has a finite partition `{P₁,…,Pₘ}` into pairwise-disjoint clopen sets such that each `Pⱼ` is contained in some member of `𝒰`.

**Proof.** Because `T` is compact Hausdorff and totally disconnected, it is zero-dimensional: the clopen sets form a basis. For every point `x∈T`, choose an open `Uₓ∈𝒰` containing `x`, and a clopen `Cₓ` with `x∈Cₓ⊆Uₓ`. Compactness yields finitely many `C₁,…,Cₘ` covering `T`. Put
```
P₁ = C₁,
Pⱼ = Cⱼ \ (C₁ ∪ ⋯ ∪ Cⱼ₋₁),  j = 2,…,m.
```
Each `Pⱼ` is clopen (a finite Boolean combination of clopens); the `Pⱼ` are pairwise disjoint, their union is `T`, and `Pⱼ⊆Cⱼ⊆Uⱼ`. Omit empty `Pⱼ`. This construction is valid for *arbitrary infinite profinite T*; only the refining partition is finite. ∎

The finite disjoint partition is stronger than merely a finite clopen subcover: its distinct nonempty intersections vanish, allowing immediate higher Čech cochain cancellation.

## 2. Consequence for ordinary sheaf cohomology on T

Let `\underline{\mathbb Z}_T` denote the constant sheaf of abelian groups on the **ordinary topological space T**. For a disjoint clopen partition `𝒫={Pⱼ}`, its normalized Čech complex has no nonzero cochains in positive degrees: all intersections of distinct partition members are empty, hence their sections are zero. Thus
```
\check H^q(𝒫, \underline{ℤ}_T) = 0, q>0.
```
Every open cover admits such a refinement. Taking the filtered colimit over open covers gives `\check H^q(T,\underline{ℤ}_T)=0` for `q>0`. A compact Hausdorff space is paracompact; the classical Čech-to-derived sheaf-cohomology comparison for abelian sheaves on paracompact Hausdorff spaces therefore yields
```
H^q(T, \underline{ℤ}_T) = 0,  q>0.
```
This proves the classical *topological* acyclicity statement. It does not alone prove the GCL condensed-category Ext assertion.

**Formal status of the partition lemma (already solved in pinned mathlib):** at mathlib commit `79d0395a1825a6264ad5d269e35e60537518955e`, `Mathlib/Topology/Separation/DisjointCover.lean` proves `TopologicalSpace.IsOpenCover.exists_finite_nonempty_disjoint_clopen_cover`: for an open cover of any compact Hausdorff totally disconnected space, there exist finitely many nonempty pairwise-disjoint clopens covering the space and each subordinate to an original open. The theorem applies to arbitrary profinite `T` with no finite-cardinality restriction. The proof in §1 is an independent mathematical explanation of an *already formally available* fact, not an unformalized partition theorem. The pinned profinite finite-quotient / locally constant factorization API also appears in `Mathlib/Topology/Category/Profinite/CofilteredLimit.lean` and `.../Extend.lean`; Nöbeling freeness is formalized in `Mathlib/Topology/Category/Profinite/Nobeling/Induction.lean`. Neither the Čech acyclicity chain nor the Čech-to-derived-sections bridge for GCL's exact condensed site has been established in the present CM5 Lean closure.

## 3. The *missing* categorical identification: no illicit transfer

The actual next implication must be a **canonical natural identification**
```
Ext^q_{CondensedMod ZLift}(F_T, ZLift)
    ≃ H^q(T, \underline{ℤ}_T),   q>0,
```
or a direct replacement proof of `Ext^q(F_T,ZLift)=0` using an exact projective/acyclic resolution in the *condensed* category. The identity here is **not** a restatement of Nöbeling freeness and is **not** implied by the fully faithful ordinary-to-condensed discrete functor. Full faithfulness on Hom (degree zero) cannot be promoted to higher Ext without a separate derived comparison.

Required source-to-Lean gates:

1. Bind `F_T`, `ZLift`, coefficient universes, and the exact target discrete integer condensed module. In particular `LocallyConstant T ℤ` as an ordinary module is *not* literally `F_T` in the condensed category.
2. Construct the derived adjunction / evaluation interface that relates `RHom_{Condensed}(F_T,ZLift)` to derived sections on `T`; prove the comparison is canonical, natural, and of the asserted variance.
3. **Reuse**, rather than reprove, pinned mathlib's `IsOpenCover.exists_finite_nonempty_disjoint_clopen_cover`; formalize the corresponding Čech contracting/acyclicity argument (or an equivalent resolution) in the *actual* sheaf site. A statement about ordinary topological sheaf cohomology cannot silently substitute for derived condensed-site cohomology.
4. Transport through the exact coefficient `ZLift` realization, rather than replace it with unlifted integers by notation.
5. Preserve the *solid-side* derived biduality and *target-product* Ext transport as independent outstanding obligations. In particular, never infer solid-side vanishing from free-side vanishing or from CM4 underived solidity.

## 4. New machine-checked Nöbeling input and evidence boundary

Candidate MATH-PROGRAMME PR [#3270](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3270), exact Lean head `d076f59c532838488ab921515da3f4ce5f509cda`, proves for all profinite `T`:
```
Projective_{ModuleCat ℤ}(LocallyConstant T ℤ),
Ext^(n+1)_{ModuleCat ℤ}(LocallyConstant T ℤ, M) = 0.
```
The exact-head `cmdg-cm4-p3` replay `43368379363` succeeded with only `propext, Classical.choice, Quot.sound`. This is an **ordinary algebraic** consequence of Nöbeling and constitutes a genuine derived-biduality input, but **not** the missing `Ext^q_{Condensed}(F_T,ZLift)` theorem. The PR's merge status must be read live, not inferred from this note.

## 5. Terminal proof frontier

**Classical topology:** disjoint-clopen refinement and resulting ordinary sheaf acyclicity are justified above.

**Formal CMDG gap:** `CM5_FREE_PROFINITE_DERIVED_SECTIONS_BRIDGE_OPEN` — canonical Ext-to-cohomology equivalence in the actual universe-lifted condensed abelian category and its exact source/target identification.

**Independent solid gap:** `CM5_SOLID_PROFINITE_DERIVED_BIDUALITY_OPEN`, including the products-of-real and real-mod-integer exact sequence, Theorem 4.3 inputs, and identification of the actual solidification-induced comparison.

**No derived-solid certification or arbitrary-profinite shifted-comparison bijectivity is claimed.**
