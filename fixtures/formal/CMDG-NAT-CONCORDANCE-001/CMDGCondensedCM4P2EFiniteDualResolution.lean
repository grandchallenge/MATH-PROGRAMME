import CMDGCondensedCM4P2EFiniteDualTriangles

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed BigOperators
attribute [local instance] FintypeCat.fintype

noncomputable local instance : MonoidalClosed
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  MonoidalClosed.FunctorCategory.monoidalClosed

lemma monoidalClosed_pre_finset_sum
    {ι : Type*}
    (A B : CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u})
    (s : Finset ι) (f : ι → (B ⟶ A)) :
    MonoidalClosed.pre (∑ i in s, f i) = ∑ i in s, MonoidalClosed.pre (f i) := by
  classical
  induction s using Finset.induction_on with
  | empty =>
      simpa using monoidalClosed_pre_zero A B
  | @insert a s ha ih =>
      rw [Finset.sum_insert ha]
      rw [monoidalClosed_pre_add A B]
      rw [Finset.sum_insert ha]
      rw [ih]

lemma finiteCoordinatePre_inclusion_projection
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoordinatePreInclusionNamed X x ≫ finiteCoordinatePreProjectionNamed X x =
      (MonoidalClosed.pre
          (finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x)).app
        CMDG.CondensedCM4P2D.coefficientPresheaf := by
  change
    (MonoidalClosed.pre (finiteCoordinateInclusion X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre (finiteCoordinateProjection X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf =
      (MonoidalClosed.pre
          (finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x)).app
        CMDG.CondensedCM4P2D.coefficientPresheaf
  have h := congrArg
    (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf)
    (MonoidalClosed.pre_map
      (finiteCoordinateProjection X x) (finiteCoordinateInclusion X x))
  simpa only [NatTrans.comp_app] using h.symm

lemma finiteFamilyPre_resolution
    (X : FintypeCat.{u}) :
    (∑ x, finiteCoordinatePreInclusionNamed X x ≫ finiteCoordinatePreProjectionNamed X x) =
      𝟙 (finiteFamilyInternalHom X) := by
  classical
  calc
    (∑ x, finiteCoordinatePreInclusionNamed X x ≫ finiteCoordinatePreProjectionNamed X x) =
        ∑ x,
          (MonoidalClosed.pre
              (finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x)).app
            CMDG.CondensedCM4P2D.coefficientPresheaf := by
              apply Finset.sum_congr rfl
              intro x hx
              exact finiteCoordinatePre_inclusion_projection X x
    _ =
        (∑ x,
          MonoidalClosed.pre
            (finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf := by
            rw [NatTrans.app_sum]
    _ =
        (MonoidalClosed.pre
          (∑ x, finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf := by
            have h := monoidalClosed_pre_finset_sum
              (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X)
              (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X)
              Finset.univ
              (fun x => finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x)
            exact congrArg
              (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf) h.symm
    _ =
        (MonoidalClosed.pre
          (𝟙 (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X))).app
          CMDG.CondensedCM4P2D.coefficientPresheaf := by
            rw [finiteCoordinate_resolution]
    _ = 𝟙 (finiteFamilyInternalHom X) := by
          rw [MonoidalClosed.pre_id]
          unfold finiteFamilyInternalHom
          rfl

#check monoidalClosed_pre_finset_sum
#check finiteCoordinatePre_inclusion_projection
#check finiteFamilyPre_resolution

#print axioms monoidalClosed_pre_finset_sum
#print axioms finiteCoordinatePre_inclusion_projection
#print axioms finiteFamilyPre_resolution

end CMDG.CondensedCM4P2E.FiniteDualTransport
