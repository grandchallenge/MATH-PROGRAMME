import CMDGCondensedCM4P3DerivedCM5R0GSEnrichedCoordinates
import Mathlib.Algebra.Category.ModuleCat.Colimits

/-!
# CMDG CM5: compact-test coordinate equivalence for the infinite discrete sum

At each compact Hausdorff test X, compactness forces a locally constant
section into an arbitrary algebraic Finsupp sum to have one finite support.
The protected coordinate-extraction map is already linear and injective.

This successor assembles any finitely supported family of locally constant
coordinate sections by the finite Finsupp sum of the rank-one injections.
It proves that coordinate extraction is a linear equivalence at each X.

This is an objectwise linear equivalence. Naturality, the underlying
presheaf coproduct, enriched-Hom product comparison, and Ext¹ for actual
G_S are not claimed by this file.
-/

noncomputable section

universe u

namespace CMDG.CondensedCM5R0

private abbrev R : Type (u + 1) := CMDG.CondensedCM4P2D.R.{u}

/-- Assemble a finitely supported family of locally constant sections into
a locally constant section of the (possibly infinite) algebraic direct sum.
Every summand is the genuine rank-one Finsupp.lsingle inclusion. -/
noncomputable def gsLocallyConstantFinsupp_assembleLinear
    (X : CompHaus.{u}) (I : Type (u + 1)) :
    (I →₀ LocallyConstant X R.{u}) →ₗ[R.{u}]
      LocallyConstant X (I →₀ R.{u}) :=
  Finsupp.lsum R.{u} (fun i =>
    LocallyConstant.mapₗ R.{u}
      (Finsupp.lsingle i : R.{u} →ₗ[R.{u}] (I →₀ R.{u})))

/-- Coordinate extraction after finite assembly is the identity, for
arbitrary basis-index types. -/
theorem gsLocallyConstantFinsupp_coordinate_assemble
    (X : CompHaus.{u}) (I : Type (u + 1)) :
    (gsLocallyConstantFinsupp_coordinateLinear X I).comp
      (gsLocallyConstantFinsupp_assembleLinear X I) =
        LinearMap.id := by
  classical
  apply Finsupp.lhom_ext'
  intro i
  apply LinearMap.ext
  intro f
  ext j x
  simp [gsLocallyConstantFinsupp_assembleLinear,
    gsLocallyConstantFinsupp_coordinateLinear,
    gsLocallyConstantFinsupp_coordinateFamily_apply]
  by_cases hij : i = j
  · subst j
    simp
  · simp [Ne.symm hij]

/-- Every finite family of locally constant coordinate sections comes from
a locally constant section of the infinite discrete Finsupp sum. -/
theorem gsLocallyConstantFinsupp_coordinateLinear_surjective
    (X : CompHaus.{u}) (I : Type (u + 1)) :
    Function.Surjective (gsLocallyConstantFinsupp_coordinateLinear X I) := by
  intro f
  refine ⟨gsLocallyConstantFinsupp_assembleLinear X I f, ?_⟩
  have h := gsLocallyConstantFinsupp_coordinate_assemble X I
  exact congrArg (fun (t : (I →₀ LocallyConstant X R.{u}) →ₗ[R.{u}]
      (I →₀ LocallyConstant X R.{u})) => t f) h

/-- Pointwise compact-test equivalence: sections into an infinite algebraic
direct sum are precisely finitely supported families of sections.
The finite support may depend on X and on the section. -/
noncomputable def gsLocallyConstantFinsupp_coordinateEquiv
    (X : CompHaus.{u}) (I : Type (u + 1)) :
    LocallyConstant X (I →₀ R.{u}) ≃ₗ[R.{u}]
      (I →₀ LocallyConstant X R.{u}) :=
  LinearEquiv.ofBijective
    (gsLocallyConstantFinsupp_coordinateLinear X I)
    ⟨gsLocallyConstantFinsupp_coordinateLinear_injective X I,
      gsLocallyConstantFinsupp_coordinateLinear_surjective X I⟩

/-- Pullback of compact-test sections commutes with each extracted
coordinate. This naturality is essential for the presheaf-colimit bridge. -/
theorem gsLocallyConstantFinsupp_coordinateEquiv_naturality
    {X Y : CompHaus.{u}} (I : Type (u + 1))
    (f : C(X, Y)) (g : LocallyConstant Y (I →₀ R.{u})) (i : I) :
    (gsLocallyConstantFinsupp_coordinateEquiv X I
      (LocallyConstant.comap f g)) i =
        LocallyConstant.comap f
          ((gsLocallyConstantFinsupp_coordinateEquiv Y I g) i) := by
  ext x
  change ((gsLocallyConstantFinsupp_coordinateFamily X I
      (LocallyConstant.comap f g)) i x).down =
    ((gsLocallyConstantFinsupp_coordinateFamily Y I g) i (f x)).down
  simp only [gsLocallyConstantFinsupp_coordinateFamily_apply,
    LocallyConstant.coe_comap_apply]

#check gsLocallyConstantFinsupp_assembleLinear
#check gsLocallyConstantFinsupp_coordinate_assemble
#check gsLocallyConstantFinsupp_coordinateLinear_surjective
#check gsLocallyConstantFinsupp_coordinateEquiv
#check gsLocallyConstantFinsupp_coordinateEquiv_naturality

#print axioms gsLocallyConstantFinsupp_coordinate_assemble
#print axioms gsLocallyConstantFinsupp_coordinateLinear_surjective
#print axioms gsLocallyConstantFinsupp_coordinateEquiv
#print axioms gsLocallyConstantFinsupp_coordinateEquiv_naturality

end CMDG.CondensedCM5R0
