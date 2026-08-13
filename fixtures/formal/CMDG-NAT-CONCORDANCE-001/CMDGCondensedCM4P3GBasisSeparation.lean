import CMDGCondensedCM4P3GFiniteSupport

/-!
# CMDG CM4-P3-G Nöbeling basis separation

This successor fixture isolates the terminal algebraic step of the coefficient mapping-out
argument. Nöbeling freeness supplies a chosen integral basis for `C(X, ℤ)`; a finite coefficient
vector is therefore forced to vanish once its associated basis combination vanishes pointwise.
The final theorem packages the exact kernel-annihilation endpoint once finite coordinate
dependence and pointwise vanishing of that finite basis combination have been obtained.
-/

namespace CMDG.CondensedCM4P3G.BasisSeparation

universe u

open scoped BigOperators
open CMDG.CondensedCM4P3G.FiniteSupport

/-- The chosen Nöbeling-basis index type for integral locally constant functions. -/
abbrev IntegralBasisIndex (X : Profinite.{u}) :=
  Module.Free.ChooseBasisIndex ℤ (LocallyConstant X ℤ)

/-- A concrete basis supplied by the pinned Nöbeling freeness instance. -/
noncomputable def integralBasis (X : Profinite.{u}) :
    Module.Basis (IntegralBasisIndex X) ℤ (LocallyConstant X ℤ) :=
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

/-- Package the coordinate values of an additive functional on one finite index set as a
finitely supported Nöbeling coefficient vector. -/
noncomputable def finiteFunctionalCoefficients
    (X : Profinite.{u})
    (L : (IntegralBasisIndex X → ℤ) →+ ℤ)
    (I : Finset (IntegralBasisIndex X)) :
    IntegralBasisIndex X →₀ ℤ :=
  ∑ i ∈ I, Finsupp.single i (L (intIndicator i))

theorem finiteFunctionalCoefficients_apply_mem
    (X : Profinite.{u})
    (L : (IntegralBasisIndex X → ℤ) →+ ℤ)
    (I : Finset (IntegralBasisIndex X))
    {i : IntegralBasisIndex X} (hi : i ∈ I) :
    finiteFunctionalCoefficients X L I i = L (intIndicator i) := by
  classical
  simp [finiteFunctionalCoefficients, hi]

/-- Terminal algebraic kernel-annihilation lemma. If `L` is controlled by one finite coordinate
set `I`, and the Nöbeling combination whose coefficients are `L` on the standard coordinate
vectors vanishes pointwise, then `L` is identically zero. -/
theorem additiveFunctional_eq_zero_of_finiteDependence_and_basisCombination
    (X : Profinite.{u})
    (L : (IntegralBasisIndex X → ℤ) →+ ℤ)
    (I : Finset (IntegralBasisIndex X))
    (hfinite :
      ∀ a : IntegralBasisIndex X → ℤ,
        (∀ i ∈ I, a i = 0) →
        L a = 0)
    (hpoint :
      ∀ x : X,
        basisCombination X (finiteFunctionalCoefficients X L I) x = 0) :
    L = 0 := by
  classical
  have hc : finiteFunctionalCoefficients X L I = 0 :=
    basisCoefficients_eq_zero_of_pointwise_zero X
      (finiteFunctionalCoefficients X L I) hpoint
  have hcoord : ∀ i ∈ I, L (intIndicator i) = 0 := by
    intro i hi
    have hi0 := congrArg (fun c : IntegralBasisIndex X →₀ ℤ => c i) hc
    simpa [finiteFunctionalCoefficients_apply_mem X L I hi] using hi0
  ext a
  have hdiff :
      ∀ i ∈ I,
        (a - finiteTruncation a I) i = 0 := by
    intro i hi
    simp [finiteTruncation, hi]
  have hzero : L (a - finiteTruncation a I) = 0 :=
    hfinite (a - finiteTruncation a I) hdiff
  have heq : L a = L (finiteTruncation a I) := by
    have hsub : L a - L (finiteTruncation a I) = 0 := by
      simpa only [map_sub] using hzero
    exact sub_eq_zero.mp hsub
  rw [heq, finiteTruncation_eq_sum, map_sum]
  apply Finset.sum_eq_zero
  intro i hi
  rw [map_zsmul]
  simp [hcoord i hi]

#print integralBasis
#print basisCombination
#print basisCoefficients_eq_zero_of_pointwise_zero
#print finiteFunctionalCoefficients
#print additiveFunctional_eq_zero_of_finiteDependence_and_basisCombination
#print axioms basisCoefficients_eq_zero_of_pointwise_zero
#print axioms additiveFunctional_eq_zero_of_finiteDependence_and_basisCombination

end CMDG.CondensedCM4P3G.BasisSeparation
