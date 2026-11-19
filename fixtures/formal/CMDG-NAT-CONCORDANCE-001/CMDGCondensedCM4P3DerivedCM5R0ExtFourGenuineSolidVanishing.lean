import CMDGCondensedCM4P3DerivedCM5R0SixthFaceCocycle
import CMDGCondensedCM4P3DerivedCM5R0GlobalFourthRelationEpi
import CMDGCondensedCM4P3DerivedCM5R0GSCondensedProduct
import CMDGCondensedCM4P3DerivedCM5R0ExtFourFourthRelationCriterion

/-!
# CMDG CM5 — unconditional Ext⁴ vanishing into the ACTUAL free-solid

For every profinite T,S, show Ext^4(F_T,G_S)=0. This requires:
- the protected actual G_S ≅ categorical product of discrete Z
- all-degree-four scalar closed fivefold H4 acyclicity
- real fifth categorical free-module boundary Hom exactness
- automatic SIX-face cocycle for every actual fourth relation Hom
- actual global fifth-to-fourth relation epi and exact Ext4 criterion.

No common finite coefficient quotient and no model substitution.
No unbounded derived solidity or independent public certification.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Every actual fourth-relation morphism into the genuine free-solid
object extends along the genuine fourth-relation kernel inclusion
for all profinite source/target objects. -/
theorem genuineFourthRelationHom_extends_unconditional
    (T S : Profinite.{u})
    (f : stoneanCechFourthRelationKernel T ⟶ underivedObject S) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)) ⟶ underivedObject S,
      kernel.ι (stoneanCechFourthToThirdRelation T) ≫ g = f := by
  let e : underivedObject S ≅
      ∏ᶜ (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff) :=
    gsFreeSolidToCoefficientProductIso S
  let h := stoneanCechFifthToFourthRelation T ≫ f ≫ e.hom
  have hc : stoneanCechClosedProductSixCocycle T h := by
    change stoneanCechClosedProductSixCocycle T
      (stoneanCechFifthToFourthRelation T ≫ (f ≫ e.hom))
    exact stoneanCechFourthRelation_product_sixCocycle
      T (f ≫ e.hom)
  obtain ⟨gprod, hgprod⟩ :=
    stoneanCechFifthBoundary_product_exact_ofClosedCocycle T h hc
  let g := gprod ≫ e.inv
  refine ⟨g, ?_⟩
  have heq : stoneanCechFifthToFourthRelation T ≫
      (kernel.ι (stoneanCechFourthToThirdRelation T) ≫ g) =
        stoneanCechFifthToFourthRelation T ≫ f := by
    calc
      stoneanCechFifthToFourthRelation T ≫
        (kernel.ι (stoneanCechFourthToThirdRelation T) ≫ g) =
        (stoneanCechFifthToFourthRelation T ≫
          kernel.ι (stoneanCechFourthToThirdRelation T)) ≫ g :=
            (Category.assoc _ _ _).symm
      _ = stoneanCechFifthBoundary T ≫ g := by
        rw [stoneanCechFifthToFourthRelation_comp_inclusion]
      _ = (stoneanCechFifthBoundary T ≫ gprod) ≫ e.inv :=
        (Category.assoc _ _ _).symm
      _ = h ≫ e.inv := by rw [hgprod]
      _ = stoneanCechFifthToFourthRelation T ≫ f := by
        simp [h, Category.assoc]
  haveI : Epi (stoneanCechFifthToFourthRelation T) :=
    stoneanCechFifthToFourthRelation_epi_unconditional T
  exact (cancel_epi (stoneanCechFifthToFourthRelation T)).1 heq

/-- Unconditional genuine Ext⁴(F_T,G_S)=0 for every profinite T,S,
with no substitute coefficient model and no external assumptions. -/
theorem freeSolid_extFour_vanishes_unconditional
    (T S : Profinite.{u}) :
    ∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T)
      (underivedObject S) 4, e = 0 := by
  apply (freeSolid_extFour_vanishes_iff_fourthRelation_hom_extends
    T S).2
  intro f
  exact genuineFourthRelationHom_extends_unconditional T S f

#print axioms genuineFourthRelationHom_extends_unconditional
#print axioms freeSolid_extFour_vanishes_unconditional
end CMDG.CondensedCM5R0
