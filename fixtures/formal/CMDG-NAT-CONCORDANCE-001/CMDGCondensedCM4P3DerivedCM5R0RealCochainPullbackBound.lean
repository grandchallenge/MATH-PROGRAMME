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
    ‖(ContinuousMap.compCLM ℝ g : C(Y, ℝ) →L[ℝ] C(X, ℝ))‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro f
  simpa only [one_mul, ContinuousMap.compCLM_apply] using
    realCompactCochain_comp_norm_le g f

/-- The genuine pullback operators compose contravariantly, as required
to transport simplicial face identities to compact real cochains. -/
theorem realCompactCochain_compCLM_comp
    (f : C(X, Y)) (g : C(Y, Z)) :
    (ContinuousMap.compCLM ℝ (g.comp f) :
      C(Z, ℝ) →L[ℝ] C(X, ℝ)) =
      (ContinuousMap.compCLM ℝ f).comp (ContinuousMap.compCLM ℝ g) := by
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
once the corresponding compact topological abelian-group instance
is chosen. No derived-Hom vanishing is inferred. -/
theorem compactDoubling_realCochain_norm_le_one
    (A : Type u) [TopologicalSpace A] [CompactSpace A]
    [AddCommGroup A] [ContinuousAdd A] :
    ‖(ContinuousMap.compCLM ℝ (compactDoublingMap A) :
      C(A, ℝ) →L[ℝ] C(A, ℝ))‖ ≤ 1 :=
  realCompactCochain_compCLM_norm_le_one (compactDoublingMap A)

#print axioms realCompactCochain_comp_norm_le
#print axioms realCompactCochain_compCLM_norm_le_one
#print axioms realCompactCochain_compCLM_comp
#print axioms compactDoubling_realCochain_norm_le_one

end CMDG.CondensedCM5R0
