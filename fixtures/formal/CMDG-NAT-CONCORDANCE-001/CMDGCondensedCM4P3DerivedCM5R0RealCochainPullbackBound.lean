import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.Topology.ContinuousMap.Algebra
import Mathlib.Analysis.Normed.Operator.Basic

/-!
# CMDG CM5 E3: the actual compact-continuous real cochain pullback bound

Theorem 4.3(ii) of the May-2026 Scholze lectures computes a compact-torus
derived real Hom via Banach cochains C(A^r × S, ℝ). Each pullback by the
doubling map has operator norm at most one. This file proves that norm claim
in the genuine compact-continuous-map Banach spaces of pinned mathlib,
and records compatibility with composition.

This is not a construction of the Breen–Deligne resolution, the complete
condensed derived-Hom comparison, or the homotopy 2-id ~ [2]^*.
-/

noncomputable section

universe u v w

namespace CMDG.CondensedCM5R0

variable {X : Type u} {Y : Type v} {Z : Type w}
variable [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z]
variable [CompactSpace X] [CompactSpace Y] [CompactSpace Z]

/-- Pullback of real cochains between compact spaces is nonexpansive in
the actual supremum norm. In particular no surjectivity or openness
of the compact map is needed. -/
theorem realCompactCochain_comp_norm_le (g : C(X, Y)) (f : C(Y, ℝ)) :
    ‖f.comp g‖ ≤ ‖f‖ := by
  apply (ContinuousMap.norm_le (f.comp g) (norm_nonneg f)).2
  intro x
  exact f.norm_coe_le_norm (g x)

/-- The *continuous linear* pullback operator on the Banach cochain spaces
is bounded by one in operator norm. This is the genuine analytic input to
the Banach doubling contraction, not a bare pointwise boundedness claim. -/
theorem realCompactCochain_compCLM_norm_le_one (g : C(X, Y)) :
    ‖(ContinuousMap.compCLM ℝ ℝ g : C(Y, ℝ) →L[ℝ] C(X, ℝ))‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro f
  simpa only [one_mul, ContinuousMap.compCLM_apply] using
    realCompactCochain_comp_norm_le g f

/-- The genuine pullback operators compose contravariantly, as required
to transport simplicial face identities to compact real cochains. -/
theorem realCompactCochain_compCLM_comp
    (f : C(X, Y)) (g : C(Y, Z)) :
    (ContinuousMap.compCLM ℝ ℝ (g.comp f) :
      C(Z, ℝ) →L[ℝ] C(X, ℝ)) =
      (ContinuousMap.compCLM ℝ ℝ f).comp (ContinuousMap.compCLM ℝ ℝ g) := by
  ext h x
  rfl

/-- The topological doubling map of a compact topological abelian group. -/
def compactDoublingMap (A : Type u)
    [TopologicalSpace A] [AddCommGroup A] [ContinuousAdd A] :
    C(A, A) :=
  ⟨fun a => a + a, continuous_id.add continuous_id⟩

/-- The exact source-shaped doubling pullback has operator norm <= 1
on the compact-space supremum Banach real cochains. This applies to
every compact torus A = (ℝ/ℤ)^I and to its finite powers times S,
by the compact doubling map. For the external probe S, use the
separate parameter-preserving doubling theorem below. No derived-Hom vanishing is inferred. -/
theorem compactDoubling_realCochain_norm_le_one
    (A : Type u) [TopologicalSpace A] [CompactSpace A]
    [AddCommGroup A] [ContinuousAdd A] :
    ‖(ContinuousMap.compCLM ℝ ℝ (compactDoublingMap A) :
      C(A, ℝ) →L[ℝ] C(A, ℝ))‖ ≤ 1 :=
  realCompactCochain_compCLM_norm_le_one (compactDoublingMap A)


/-- Doubling on a compact abelian group while keeping an arbitrary compact
parameter S unchanged. This is the exact map on A^r × S used by the
Breen–Deligne real cochains. The probe S need not carry a group structure. -/
def compactParametricDoublingMap
    (A : Type u) (S : Type v)
    [TopologicalSpace A] [AddCommGroup A] [ContinuousAdd A]
    [TopologicalSpace S] : C(A × S, A × S) :=
  ⟨fun p => (p.1 + p.1, p.2),
    (continuous_fst.add continuous_fst).prodMk continuous_snd⟩

/-- The source-shaped doubling operator on C(A^r × S, ℝ) is
nonexpansive for every compact parameter S, not just the group itself. -/
theorem compactParametricDoubling_realCochain_norm_le_one
    (A : Type u) (S : Type v)
    [TopologicalSpace A] [CompactSpace A]
    [AddCommGroup A] [ContinuousAdd A]
    [TopologicalSpace S] [CompactSpace S] :
    ‖(ContinuousMap.compCLM ℝ ℝ (compactParametricDoublingMap A S) :
      C(A × S, ℝ) →L[ℝ] C(A × S, ℝ))‖ ≤ 1 :=
  realCompactCochain_compCLM_norm_le_one
    (compactParametricDoublingMap A S)


/-- A finite integer/real linear combination of actual pullbacks is a
bounded operator. This is the degreewise analytic boundedness mechanism
for the finite-support homotopies in a Breen–Deligne resolution.
The quantitative operator bound is the sum of the absolute coefficients. -/
theorem realCompactCochain_finiteWeightedPullbacks_norm_le
    {ι : Type*} (s : Finset ι) (c : ι → ℝ) (g : ι → C(X, Y)) :
    ‖∑ i ∈ s, c i •
        (ContinuousMap.compCLM ℝ ℝ (g i) :
          C(Y, ℝ) →L[ℝ] C(X, ℝ))‖ ≤ ∑ i ∈ s, |c i| := by
  calc
    ‖∑ i ∈ s, c i •
        (ContinuousMap.compCLM ℝ ℝ (g i) :
          C(Y, ℝ) →L[ℝ] C(X, ℝ))‖
        ≤ ∑ i ∈ s, ‖c i •
          (ContinuousMap.compCLM ℝ ℝ (g i) :
            C(Y, ℝ) →L[ℝ] C(X, ℝ))‖ := norm_sum_le _ _
    _ ≤ ∑ i ∈ s, |c i| := by
      apply Finset.sum_le_sum
      intro i hi
      rw [norm_smul, Real.norm_eq_abs]
      calc
        |c i| * ‖(ContinuousMap.compCLM ℝ ℝ (g i) :
            C(Y, ℝ) →L[ℝ] C(X, ℝ))‖
            ≤ |c i| * 1 :=
              mul_le_mul_of_nonneg_left
                (realCompactCochain_compCLM_norm_le_one (g i))
                (abs_nonneg _)
        _ = |c i| := mul_one _

#print axioms realCompactCochain_comp_norm_le
#print axioms realCompactCochain_compCLM_norm_le_one
#print axioms realCompactCochain_compCLM_comp
#print axioms realCompactCochain_finiteWeightedPullbacks_norm_le
#print axioms compactDoubling_realCochain_norm_le_one
#print axioms compactParametricDoubling_realCochain_norm_le_one

end CMDG.CondensedCM5R0
