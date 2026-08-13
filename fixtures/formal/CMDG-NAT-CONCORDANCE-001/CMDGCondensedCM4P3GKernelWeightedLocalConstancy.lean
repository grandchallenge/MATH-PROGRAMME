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
  DiscreteQuotient.ofLE f.le

/-- The quotient transition carries the projection to the refined projection. -/
theorem finiteQuotientTransition_proj
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) (x : X) :
    finiteQuotientTransition X f (j.proj x) = k.proj x := by
  simpa [finiteQuotientTransition] using DiscreteQuotient.ofLE_proj f.le x

/-- Fiberwise summation of the finer quotient deltas recovers the coarser quotient delta at each
point of `X`. Evaluation is made explicit before the finite sum is reduced, so the proof does not
rely on rewriting a sum in the `LocallyConstant` function space. -/
theorem finiteDeltaPullbackR_fiber_sum_apply
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : (FiniteQuotientObject X k).obj) (x : X) :
    (∑ p : (FiniteQuotientObject X j).obj,
      if finiteQuotientTransition X f p = q then
        finiteDeltaPullbackR X j p
      else 0) x =
      finiteDeltaPullbackR X k q x := by
  classical
  let ev : LocallyConstant X R.{u} →+ R.{u} :=
    { toFun := fun v => v x
      map_zero' := rfl
      map_add' := fun _ _ => rfl }
  change
    ev (∑ p : (FiniteQuotientObject X j).obj,
      if finiteQuotientTransition X f p = q then
        finiteDeltaPullbackR X j p
      else 0) =
      finiteDeltaPullbackR X k q x
  rw [map_sum]
  rw [Finset.sum_eq_single (j.proj x)]
  · simp [ev, finiteQuotientTransition_proj, finiteDeltaPullbackR]
  · intro p hp hne
    have hne' : j.proj x ≠ p := Ne.symm hne
    simp [ev, finiteDeltaPullbackR, hne']
  · simp

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

/-- The certified lifted Nöbeling pairing preserves the finite quotient-refinement identity. -/
theorem basisBooleanPairingR_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : (FiniteQuotientObject X k).obj) :
    (∑ p : (FiniteQuotientObject X j).obj,
      if finiteQuotientTransition X f p = q then
        basisBooleanPairingR X (finiteDeltaPullbackR X j p)
      else 0) =
      basisBooleanPairingR X (finiteDeltaPullbackR X k q) := by
  classical
  calc
    (∑ p : (FiniteQuotientObject X j).obj,
      if finiteQuotientTransition X f p = q then
        basisBooleanPairingR X (finiteDeltaPullbackR X j p)
      else 0) =
        basisBooleanPairingR X
          (∑ p : (FiniteQuotientObject X j).obj,
            if finiteQuotientTransition X f p = q then
              finiteDeltaPullbackR X j p
            else 0) := by
              rw [map_sum]
              apply Finset.sum_congr rfl
              intro p hp
              by_cases h : finiteQuotientTransition X f p = q <;> simp [h]
    _ = basisBooleanPairingR X (finiteDeltaPullbackR X k q) := by
      rw [finiteDeltaPullbackR_fiber_sum X f q]

/-- The lifted Nöbeling Boolean coefficients satisfy the same quotient-refinement law. -/
theorem finiteBooleanCoefficient_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : (FiniteQuotientObject X k).obj) :
    (∑ p : (FiniteQuotientObject X j).obj,
      if finiteQuotientTransition X f p = q then
        finiteBooleanCoefficient X j p
      else 0) =
      finiteBooleanCoefficient X k q := by
  simpa [finiteBooleanCoefficient] using basisBooleanPairingR_fiber_sum X f q

#check finiteQuotientTransition
#check finiteQuotientTransition_proj
#check finiteDeltaPullbackR_fiber_sum_apply
#check finiteDeltaPullbackR_fiber_sum
#check basisBooleanPairingR_fiber_sum
#check finiteBooleanCoefficient_fiber_sum

#print axioms finiteQuotientTransition_proj
#print axioms finiteDeltaPullbackR_fiber_sum
#print axioms basisBooleanPairingR_fiber_sum
#print axioms finiteBooleanCoefficient_fiber_sum

end CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy
