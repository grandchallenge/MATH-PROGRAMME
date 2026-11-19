import CMDGCondensedCM4P3DerivedCM5R0GenuineSixthBoundaryProductExact
import CMDGCondensedCM4P3DerivedCM5R0GlobalFifthRelationEpi
import CMDGCondensedCM4P3DerivedCM5R0GSCondensedProduct
import CMDGCondensedCM4P3DerivedCM5R0ExtFiveRelationReduction

/-!
# CMDG CM5 — unconditional Ext⁵ vanishing into ACTUAL free-solid G_S.

For all profinite T and S, Ext⁵(F_T,G_S)=0. Key dependencies:
- actual genuine free-solid G_S ≅ categorical product of discrete ℤ
- full scalar closed sixfold H5 and arbitrary-index product Hom primitives
- seven-face cocycle automatic for genuine fifth relation Hom
- actual global sixth-to-fifth relation epi
- exact degree-five Ext criterion (protected PR #3547)

This theorem makes NO claim about every higher degree, all-shift
derived solidity, independent public MATHCERT certification, or Liquid
Tensor.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Every actual fifth-relation morphism into the actual free-solid
G_S extends along the genuine fifth-relation kernel inclusion,
for arbitrary profinite T,S. -/
theorem genuineFifthRelationHom_extends_unconditional
    (T S : Profinite.{u})
    (f : stoneanCechFifthRelationKernel T ⟶ underivedObject S) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
        (stoneanCechExplicitQuintupleProfinite T)) ⟶
        underivedObject S,
      kernel.ι (stoneanCechFifthToFourthRelation T) ≫ g = f := by
  let e : underivedObject S ≅
      ∏ᶜ (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff) :=
    gsFreeSolidToCoefficientProductIso S
  let h := stoneanCechSixthToFifthRelation T ≫ f ≫ e.hom
  have hc : stoneanCechClosedProductSevenCocycle T h := by
    change stoneanCechClosedProductSevenCocycle T
      (stoneanCechSixthToFifthRelation T ≫ (f ≫ e.hom))
    exact stoneanCechFifthRelation_product_sevenCocycle
      T (f ≫ e.hom)
  obtain ⟨gprod, hgprod⟩ :=
    stoneanCechSixthBoundary_product_exact_ofClosedCocycle T h hc
  let g := gprod ≫ e.inv
  refine ⟨g, ?_⟩
  have heq : stoneanCechSixthToFifthRelation T ≫
      (kernel.ι (stoneanCechFifthToFourthRelation T) ≫ g) =
        stoneanCechSixthToFifthRelation T ≫ f := by
    calc
      stoneanCechSixthToFifthRelation T ≫
        (kernel.ι (stoneanCechFifthToFourthRelation T) ≫ g) =
        (stoneanCechSixthToFifthRelation T ≫
          kernel.ι (stoneanCechFifthToFourthRelation T)) ≫ g :=
            (Category.assoc _ _ _).symm
      _ = stoneanCechSixthBoundary T ≫ g := by
          rw [stoneanCechSixthToFifthRelation_comp_inclusion]
      _ = (stoneanCechSixthBoundary T ≫ gprod) ≫ e.inv :=
          (Category.assoc _ _ _).symm
      _ = h ≫ e.inv := by rw [hgprod]
      _ = stoneanCechSixthToFifthRelation T ≫ f := by
        simp [h, Category.assoc]
  haveI : Epi (stoneanCechSixthToFifthRelation T) :=
    stoneanCechSixthToFifthRelation_epi_unconditional T
  exact (cancel_epi (stoneanCechSixthToFifthRelation T)).1 heq

/-- Unconditional genuine Ext⁵(F_T,G_S)=0 for ALL profinite T,S,
with actual free-condensed source and protected free-solid target. -/
theorem freeSolid_extFive_vanishes_unconditional
    (T S : Profinite.{u}) :
    ∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T)
      (underivedObject S) 5, e = 0 := by
  apply (freeSolid_extFive_vanishes_iff_fifthRelation_hom_extends
    T S).2
  intro f
  exact genuineFifthRelationHom_extends_unconditional T S f

#print axioms genuineFifthRelationHom_extends_unconditional
#print axioms freeSolid_extFive_vanishes_unconditional
end CMDG.CondensedCM5R0
