import CMDGCondensedCM4P3GPointFunctional
import CMDGCondensedCM4P2EE2
import CMDGCondensedCM4P2EE3
import CMDGCondensedCM4P2EFiniteDualPushforward

/-!
# CMDG CM4-P3-G kernel weighted-local-constancy bridge

This successor fixture begins the exact bridge from a kernel candidate to the weighted Boolean
local-constancy hypotheses required by the certified finite-dependence theorem. The finite Boolean
measure probes are first made compatible under refinement of finite quotients; only after that
compatibility is certified may they be assembled through the protected right-Kan/limit model.

No injectivity, coefficient-solidity, or broader P3 closure claim is asserted here.
-/

namespace CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy

universe u

open CategoryTheory Limits Opposite
open scoped BigOperators

open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairingR
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3G.FiniteBooleanMeasureHom

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- The finite-set map induced by a refinement of discrete quotients. -/
noncomputable def finiteQuotientTransition
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) :
    (FiniteQuotientObject X j).obj → (FiniteQuotientObject X k).obj :=
  fun p => (X.fintypeDiagram.map f) p

/-- The quotient transition carries the projection to the refined projection. -/
theorem finiteQuotientTransition_proj
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) (x : X) :
    finiteQuotientTransition X f (j.proj x) = k.proj x := by
  change DiscreteQuotient.ofLE f.le (j.proj x) = k.proj x
  exact DiscreteQuotient.ofLE_proj f.le x

/-- Fiberwise summation of the finer quotient deltas recovers the coarser quotient delta. -/
theorem finiteDeltaPullbackR_fiber_sum_apply
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : (FiniteQuotientObject X k).obj) (x : X) :
    (∑ p : (FiniteQuotientObject X j).obj,
      if finiteQuotientTransition X f p = q then
        finiteDeltaPullbackR X j p
      else 0) x =
      finiteDeltaPullbackR X k q x := by
  classical
  by_cases hk : k.proj x = q
  · have ht : finiteQuotientTransition X f (j.proj x) = q := by
      rw [finiteQuotientTransition_proj]
      exact hk
    rw [Finset.sum_eq_single (j.proj x)]
    · simp [finiteDeltaPullbackR, ht, hk]
    · intro p hp hpne
      simp [finiteDeltaPullbackR, hpne]
    · simp
  · rw [finiteDeltaPullbackR]
    simp only [hk, if_false]
    apply Finset.sum_eq_zero
    intro p hp
    by_cases htp : finiteQuotientTransition X f p = q
    · have hxp : j.proj x ≠ p := by
        intro h
        subst p
        have := finiteQuotientTransition_proj X f x
        exact hk (this.symm.trans htp)
      simp [htp, finiteDeltaPullbackR, hxp]
    · simp [htp]

/-- Extensional form of finite-delta compatibility. -/
theorem finiteDeltaPullbackR_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : (FiniteQuotientObject X k).obj) :
    (∑ p : (FiniteQuotientObject X j).obj,
      if finiteQuotientTransition X f p = q then
        finiteDeltaPullbackR X j p
      else 0) =
      finiteDeltaPullbackR X k q := by
  ext x
  exact finiteDeltaPullbackR_fiber_sum_apply X f q x

/-- The lifted Nöbeling Boolean coefficients satisfy the same quotient-refinement law. -/
theorem finiteBooleanCoefficient_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : (FiniteQuotientObject X k).obj) :
    (∑ p : (FiniteQuotientObject X j).obj,
      if finiteQuotientTransition X f p = q then
        finiteBooleanCoefficient X j p
      else 0) =
      finiteBooleanCoefficient X k q := by
  classical
  let pairing :
      LocallyConstant X R.{u} →ₗ[R.{u}]
        LocallyConstant (IntegralBasisIndex X → Bool) R.{u} :=
    basisBooleanPairingR X
  change
    (∑ p : (FiniteQuotientObject X j).obj,
      if finiteQuotientTransition X f p = q then
        pairing (finiteDeltaPullbackR X j p)
      else 0) =
      pairing (finiteDeltaPullbackR X k q)
  rw [← map_sum]
  congr 1
  simpa only [map_zero] using finiteDeltaPullbackR_fiber_sum X f q

#check finiteQuotientTransition
#check finiteQuotientTransition_proj
#check finiteDeltaPullbackR_fiber_sum_apply
#check finiteDeltaPullbackR_fiber_sum
#check finiteBooleanCoefficient_fiber_sum

#print axioms finiteQuotientTransition_proj
#print axioms finiteDeltaPullbackR_fiber_sum
#print axioms finiteBooleanCoefficient_fiber_sum

end CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy
