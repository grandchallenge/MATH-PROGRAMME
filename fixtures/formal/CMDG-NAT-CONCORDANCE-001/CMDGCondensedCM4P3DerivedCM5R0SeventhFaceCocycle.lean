import CMDGCondensedCM4P3DerivedCM5R0SeventhBoundaryScalarHom
import CMDGCondensedCM4P3DerivedCM5R0GlobalFifthRelationEpi
import CMDGCondensedCM4P3DerivedCM5R0ExtFiveRelationReduction

/-!
# Actual seventh-face cocycle of a fifth-relation kernel morphism.

The object is the genuine free condensed sixfold Čech module and its
genuine seventh Profinite relation. Seven-face cancellation is derived
from d7*d6=0 and the true kernel mono; not an external assumption.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

def stoneanCechClosedProductSevenCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSextupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) : Prop :=
  ∀ (i : ι) (r : stoneanCechExplicitSeptupleProfinite T),
    (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace0 T).hom.hom r) - (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace1 T).hom.hom r) + (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace2 T).hom.hom r) - (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace3 T).hom.hom r) + (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace4 T).hom.hom r) - (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace5 T).hom.hom r) + (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace6 T).hom.hom r) = 0

/-- Any genuine seventh-boundary-zero product Hom has
the actual pointwise seven-face scalar cocycle. -/
theorem stoneanCechClosedProductSevenCocycle_ofSeventhZero
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSextupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hz : stoneanCechSeventhBoundary T ≫ f = 0) :
    stoneanCechClosedProductSevenCocycle T f := by
  intro i r
  have h := stoneanCechSeventhBoundary_product_scalar_atPoint T f i r
  rw [hz] at h
  have hdiff := freeProfiniteDiscreteIntegerHomScalarEquiv_sub
    (stoneanCechExplicitSeptupleProfinite T)
    (0 : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSeptupleProfinite T)) ⟶ discreteIntegerCoeff)
    0
  have hs : freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSeptupleProfinite T) 0 = 0 := by
    simp only [sub_self] at hdiff
    exact hdiff
  have hzero : (freeProfiniteDiscreteProductHomScalarEquiv
       (stoneanCechExplicitSeptupleProfinite T)
       (0 : ((Condensed.profiniteFree Coeff).obj
         (stoneanCechExplicitSeptupleProfinite T)) ⟶
           ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) i) r = 0 := by
    change (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSeptupleProfinite T)
      ((0 : ((Condensed.profiniteFree Coeff).obj
        (stoneanCechExplicitSeptupleProfinite T)) ⟶
          ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) ≫
        Pi.π (fun _ : ι => discreteIntegerCoeff) i)) r = 0
    rw [zero_comp, hs]
    rfl
  rw [hzero] at h
  exact h.symm

theorem stoneanCechSeventhBoundary_comp_fifthRelation_zero
    (T : Profinite.{u}) :
    stoneanCechSeventhBoundary T ≫
      stoneanCechSixthToFifthRelation T = 0 := by
  apply (cancel_mono
    (kernel.ι (stoneanCechFifthToFourthRelation T))).1
  rw [Category.assoc,
    stoneanCechSixthToFifthRelation_comp_inclusion,
    zero_comp]
  exact stoneanCechSeventhBoundary_comp_sixthBoundary_zero T

/-- All genuine fifth-relation Hom maps automatically satisfy
the scalar seven-face cocycle; no cohomological hypothesis. -/
theorem stoneanCechFifthRelation_product_sevenCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : stoneanCechFifthRelationKernel T ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) :
    stoneanCechClosedProductSevenCocycle T
      (stoneanCechSixthToFifthRelation T ≫ f) := by
  apply stoneanCechClosedProductSevenCocycle_ofSeventhZero
  rw [← Category.assoc,
    stoneanCechSeventhBoundary_comp_fifthRelation_zero, zero_comp]

#print axioms stoneanCechFifthRelation_product_sevenCocycle
end CMDG.CondensedCM5R0
