import CMDGCondensedCM4P3GFiniteSupport

/-!
# CMDG CM4-P3-G Nöbeling basis separation

This successor fixture isolates the terminal algebraic step of the coefficient mapping-out
argument. Nöbeling freeness supplies a chosen integral basis for `C(X, ℤ)`; a finite coefficient
vector is therefore forced to vanish once its associated basis combination vanishes pointwise.
-/

namespace CMDG.CondensedCM4P3G.BasisSeparation

universe u

/-- The chosen Nöbeling-basis index type for integral locally constant functions. -/
abbrev IntegralBasisIndex (X : Profinite.{u}) :=
  Module.Free.ChooseBasisIndex ℤ (LocallyConstant X ℤ)

/-- A concrete basis supplied by the pinned Nöbeling freeness instance. -/
noncomputable def integralBasis (X : Profinite.{u}) :
    Basis (IntegralBasisIndex X) ℤ (LocallyConstant X ℤ) :=
  Module.Free.chooseBasis ℤ (LocallyConstant X ℤ)

/-- Reconstruct a locally constant integral function from a finite basis-coordinate vector. -/
noncomputable def basisCombination (X : Profinite.{u})
    (c : IntegralBasisIndex X →₀ ℤ) : LocallyConstant X ℤ :=
  (integralBasis X).repr.symm c

theorem basisCombination_eq_zero_iff (X : Profinite.{u})
    (c : IntegralBasisIndex X →₀ ℤ) :
    basisCombination X c = 0 ↔ c = 0 := by
  constructor
  · intro h
    have hr := congrArg (integralBasis X).repr h
    simpa [basisCombination] using hr
  · intro h
    subst c
    simp [basisCombination]

/-- Pointwise vanishing of a finite Nöbeling-basis combination forces every coefficient to be
zero. This is the exact linear-independence endpoint needed after finite support is extracted. -/
theorem basisCoefficients_eq_zero_of_pointwise_zero
    (X : Profinite.{u}) (c : IntegralBasisIndex X →₀ ℤ)
    (h : ∀ x : X, basisCombination X c x = 0) :
    c = 0 := by
  apply (basisCombination_eq_zero_iff X c).mp
  ext x
  simpa using h x

#print integralBasis
#print basisCombination
#print basisCoefficients_eq_zero_of_pointwise_zero
#print axioms basisCoefficients_eq_zero_of_pointwise_zero

end CMDG.CondensedCM4P3G.BasisSeparation
