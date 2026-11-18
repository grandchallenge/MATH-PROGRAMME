import CMDGCondensedCM4P3DerivedCM5R0FifthFaceCocycle
import CMDGCondensedCM4P3DerivedCM5R0GlobalThirdRelationEpi
import CMDGCondensedCM4P3DerivedCM5R0GSCondensedProduct
import CMDGCondensedCM4P3DerivedCM5R0ThirdRelationExtCriterion

/-!
# CMDG CM5 — unconditional Ext³ vanishing into the actual free-solid target

For all profinite T,S, establish Ext³(F_T,G_S)=0 where F_T is the
actual free condensed lifted-integer module and G_S is the genuine
free-solid object, not an assumed discrete coefficient substitute.

Use the PROTECTED natural isomorphism G_S ≅ ∏ᶜ Z_disc, prove automatic
five-face cocycle condition for every actual third-relation map,
apply genuine categorical fourth-boundary H³ exactness, and cancel
the protected global epimorphism F_{P(T)^4_T}↠M_T. The genuine
third-relation extension criterion then gives unconditional Ext³.
This does not prove unbounded higher Ext or all-shift derived solidity.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Every actual morphism from the true third Čech relation into the
true free-solid object extends along the true third kernel inclusion,
for *all* profinite sources and targets. -/
theorem genuineThirdRelationHom_extends_unconditional
    (T S : Profinite.{u})
    (f : stoneanCechThirdRelationKernel T ⟶ underivedObject S) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) ⟶ underivedObject S,
      kernel.ι (stoneanCechTripleToSecondRelation T) ≫ g = f := by
  let e : underivedObject S ≅
      ∏ᶜ (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff) :=
    gsFreeSolidToCoefficientProductIso S
  let h := stoneanCechFourthToThirdRelation T ≫ f ≫ e.hom
  have hc : stoneanCechClosedProductFiveCocycle T
      ((Condensed.profiniteFree Coeff).map
        (stoneanCechExplicitQuadrupleToAbstract T) ≫ h) := by
    change stoneanCechClosedProductFiveCocycle T
      ((Condensed.profiniteFree Coeff).map
        (stoneanCechExplicitQuadrupleToAbstract T) ≫
        (stoneanCechFourthToThirdRelation T ≫ (f ≫ e.hom)))
    exact stoneanCechThirdRelation_product_fiveCocycle T (f ≫ e.hom)
  obtain ⟨gprod, hgprod⟩ :=
    stoneanCechFourthBoundary_product_exact_ofClosedCocycle T h hc
  let g := gprod ≫ e.inv
  refine ⟨g, ?_⟩
  have heq : stoneanCechFourthToThirdRelation T ≫
      (kernel.ι (stoneanCechTripleToSecondRelation T) ≫ g) =
        stoneanCechFourthToThirdRelation T ≫ f := by
    calc
      stoneanCechFourthToThirdRelation T ≫
        (kernel.ι (stoneanCechTripleToSecondRelation T) ≫ g) =
        (stoneanCechFourthToThirdRelation T ≫
          kernel.ι (stoneanCechTripleToSecondRelation T)) ≫ g :=
            (Category.assoc _ _ _).symm
      _ = stoneanCechFourthBoundary T ≫ g := by
        rw [stoneanCechFourthToThirdRelation_comp_inclusion]
      _ = (stoneanCechFourthBoundary T ≫ gprod) ≫ e.inv :=
        (Category.assoc _ _ _).symm
      _ = h ≫ e.inv := by rw [hgprod]
      _ = stoneanCechFourthToThirdRelation T ≫ f := by
        simp [h, Category.assoc]
  haveI : Epi (stoneanCechFourthToThirdRelation T) :=
    stoneanCechFourthToThirdRelation_epi_unconditional T
  exact (cancel_epi (stoneanCechFourthToThirdRelation T)).1 heq

/-- Unconditional genuine degree-three Ext vanishing for every pair
of profinite T,S, with the *actual* protected free-solid target. -/
theorem freeSolid_extThree_vanishes_unconditional
    (T S : Profinite.{u}) :
    ∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T)
      (underivedObject S) 3, e = 0 := by
  apply (freeSolid_extThree_vanishes_iff_thirdRelation_hom_extends T S).2
  intro f
  exact genuineThirdRelationHom_extends_unconditional T S f

#print axioms genuineThirdRelationHom_extends_unconditional
#print axioms freeSolid_extThree_vanishes_unconditional
end CMDG.CondensedCM5R0
