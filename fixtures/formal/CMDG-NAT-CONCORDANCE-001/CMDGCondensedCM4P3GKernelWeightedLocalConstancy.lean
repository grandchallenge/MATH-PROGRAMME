import CMDGCondensedCM4P3GFiniteBooleanMeasure
import CMDGCondensedCM4P2EFiniteDualPushforward

/-!
# CMDG CM4-P3-G finite quotient coefficient compatibility

This successor fixture isolates the finite quotient-refinement calculation required before any
right-Kan assembly or kernel-local-constancy argument. It proves that a delta pulled back from a
coarser finite quotient is the fiberwise sum of the deltas from a finer quotient, then transports
that identity through the already-certified lifted Nöbeling Boolean pairing.

No finite-measure cone, right-Kan assembly, injectivity, coefficient-solidity, or broader P3 closure
claim is asserted here.
-/

namespace CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy

universe u

open CategoryTheory
open scoped BigOperators

open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3G.BasisBooleanPairingR

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- Mathlib gives a compact discrete quotient a `Finite` instance. The finite sum below needs a
chosen `Fintype`; keep that noncomputable choice local to this exact fixture. -/
noncomputable local instance discreteQuotientFintype
    (X : Profinite.{u}) (j : DiscreteQuotient X) : Fintype j :=
  Fintype.ofFinite j

/-- Equality on a finite quotient is used only to form the explicit fiber indicator. -/
noncomputable local instance discreteQuotientDecidableEq
    (X : Profinite.{u}) (j : DiscreteQuotient X) : DecidableEq j :=
  Classical.decEq j

/-- The finite-set map induced by a refinement of discrete quotients. -/
noncomputable def finiteQuotientTransition
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) : j → k :=
  DiscreteQuotient.ofLE f.le

/-- The quotient transition carries the projection to the refined projection. -/
theorem finiteQuotientTransition_proj
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) (x : X) :
    finiteQuotientTransition X f (j.proj x) = k.proj x := by
  change DiscreteQuotient.ofLE f.le (j.proj x) = k.proj x
  exact DiscreteQuotient.ofLE_proj f.le x

/-- Pure scalar form of the quotient-fiber delta identity. At a fixed `x`, only the finer quotient
point `j.proj x` can contribute to the sum. -/
theorem finiteDeltaFiberScalar_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) (x : X) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        if j.proj x = p then (1 : R.{u}) else 0
      else 0) =
      if k.proj x = q then (1 : R.{u}) else 0 := by
  by_cases hx : k.proj x = q
  · have hpx : finiteQuotientTransition X f (j.proj x) = q := by
      calc
        finiteQuotientTransition X f (j.proj x) = k.proj x :=
          finiteQuotientTransition_proj X f x
        _ = q := hx
    rw [Finset.sum_eq_single (j.proj x)]
    · simp [hpx, hx]
    · intro p _ hp
      have hjp : j.proj x ≠ p := fun h => hp h.symm
      by_cases hpq : finiteQuotientTransition X f p = q
      · simp [hpq, hjp]
      · simp [hpq]
    · simp
  · rw [if_neg hx]
    apply Finset.sum_eq_zero
    intro p _
    by_cases hpq : finiteQuotientTransition X f p = q
    · have hjp : j.proj x ≠ p := by
        intro h
        apply hx
        calc
          k.proj x = finiteQuotientTransition X f (j.proj x) :=
            (finiteQuotientTransition_proj X f x).symm
          _ = finiteQuotientTransition X f p := congrArg (finiteQuotientTransition X f) h
          _ = q := hpq
      simp [hpq, hjp]
    · simp [hpq]

/-- Fiberwise summation of the finer quotient deltas recovers the coarser quotient delta at each
point of `X`. -/
theorem finiteDeltaPullbackR_fiber_sum_apply
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) (x : X) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        finiteDeltaPullbackR X j p
      else 0) x =
      finiteDeltaPullbackR X k q x := by
  change
    (LocallyConstant.evalRingHom x)
        (∑ p : j,
          if finiteQuotientTransition X f p = q then
            finiteDeltaPullbackR X j p
          else 0) =
      (LocallyConstant.evalRingHom x) (finiteDeltaPullbackR X k q)
  calc
    (LocallyConstant.evalRingHom x)
        (∑ p : j,
          if finiteQuotientTransition X f p = q then
            finiteDeltaPullbackR X j p
          else 0) =
        ∑ p : j,
          (LocallyConstant.evalRingHom x)
            (if finiteQuotientTransition X f p = q then
              finiteDeltaPullbackR X j p
            else 0) := by
              rw [map_sum]
    _ = ∑ p : j,
          if finiteQuotientTransition X f p = q then
            if j.proj x = p then (1 : R.{u}) else 0
          else 0 := by
            apply Finset.sum_congr rfl
            intro p _
            by_cases hpq : finiteQuotientTransition X f p = q
            · simp [hpq, finiteDeltaPullbackR]
            · simp [hpq]
    _ = if k.proj x = q then (1 : R.{u}) else 0 :=
      finiteDeltaFiberScalar_sum X f q x
    _ = (LocallyConstant.evalRingHom x) (finiteDeltaPullbackR X k q) := by
      simp [finiteDeltaPullbackR]

/-- Extensional form of finite-delta compatibility. -/
theorem finiteDeltaPullbackR_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        finiteDeltaPullbackR X j p
      else 0) =
      finiteDeltaPullbackR X k q := by
  apply LocallyConstant.ext
  intro x
  exact finiteDeltaPullbackR_fiber_sum_apply X f q x

/-- Linearity of the lifted Nöbeling Boolean pairing transports finite-delta compatibility to the
Boolean coefficient functions. -/
theorem basisBooleanPairingR_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X j p)
      else 0) =
      basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X k q) := by
  calc
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X j p)
      else 0) =
        basisBooleanPairingR.{u, u, u, u} X
          (∑ p : j,
            if finiteQuotientTransition X f p = q then
              finiteDeltaPullbackR X j p
            else 0) := by
              rw [map_sum]
              apply Finset.sum_congr rfl
              intro p _
              by_cases hpq : finiteQuotientTransition X f p = q
              · rw [if_pos hpq, if_pos hpq]
              · rw [if_neg hpq, if_neg hpq, map_zero]
    _ = basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X k q) := by
      rw [finiteDeltaPullbackR_fiber_sum X f q]

/-- The concrete Boolean coefficient family therefore satisfies the same refinement law. This is
the coefficient-level compatibility required before transport through the finite measure-family
isomorphisms and right-Kan assembly. -/
theorem finiteBooleanCoefficient_fiber_sum
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k)
    (q : k) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        finiteBooleanCoefficient X j p
      else 0) =
      finiteBooleanCoefficient X k q := by
  change
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X j p)
      else 0) =
      basisBooleanPairingR.{u, u, u, u} X (finiteDeltaPullbackR X k q)
  exact basisBooleanPairingR_fiber_sum X f q

#check finiteQuotientTransition
#check finiteQuotientTransition_proj
#check finiteDeltaFiberScalar_sum
#check finiteDeltaPullbackR_fiber_sum_apply
#check finiteDeltaPullbackR_fiber_sum
#check basisBooleanPairingR_fiber_sum
#check finiteBooleanCoefficient_fiber_sum

#print axioms finiteQuotientTransition_proj
#print axioms finiteDeltaFiberScalar_sum
#print axioms finiteDeltaPullbackR_fiber_sum_apply
#print axioms finiteDeltaPullbackR_fiber_sum
#print axioms basisBooleanPairingR_fiber_sum
#print axioms finiteBooleanCoefficient_fiber_sum

end CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy
