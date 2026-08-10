import CMDGCondensedCM4P2EReverseTriangle

/-!
# CMDG CM4-P2-E rank-one internal-Hom natural isomorphism

This auxiliary fixture packages the two certified objectwise inverse laws for the rank-one
internal-Hom comparison and proves naturality in the compact-Hausdorff variable. The resulting
presheaf isomorphism is the exact E1 rank-one boundary.

It does not transport this isomorphism through the finite algebraic/discrete/free comparison chain
and does not assert the E1 finite comparison or the final P2-E equivalence.
-/

namespace CMDG.CondensedCM4P2E.InternalHom

universe u

open CategoryTheory Limits Opposite
open CategoryTheory.Enriched.FunctorCategory
open scoped CategoryTheory.MonoidalClosed

noncomputable def rankOneObjectIso (X : CompHaus.{u}) :
    rankOneInternalHom.obj (op X) ≅ coefficientPresheaf.obj (op X) where
  hom := rankOneEvaluationApp X
  inv := rankOneMultiplicationApp X
  hom_inv_id := rankOneEvaluation_multiplication X
  inv_hom_id := rankOneMultiplication_evaluation X

lemma rankOneInternalHom_map_identityProjection
    {X Y : CompHaus.{u}} (f : X ⟶ Y) :
    rankOneInternalHom.map f.op ≫ rankOneIdentityProjection X =
      enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op Y) ⋙ coefficientPresheaf)
        (Under.forget (op Y) ⋙ coefficientPresheaf)
        (Under.mk f.op) := by
  change
    (functorEnrichedHom
        (ModuleCat.{u + 1} R)
        coefficientPresheaf coefficientPresheaf).map f.op ≫
      enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op X) ⋙ coefficientPresheaf)
        (Under.forget (op X) ⋙ coefficientPresheaf)
        (Under.mk (𝟙 (op X))) =
      enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op Y) ⋙ coefficientPresheaf)
        (Under.forget (op Y) ⋙ coefficientPresheaf)
        (Under.mk f.op)
  simp only [functorEnrichedHom_map, end_.lift_π, Iso.refl_inv, NatTrans.id_app,
    eHomWhiskerRight_id, Iso.refl_hom, eHomWhiskerLeft_id, comp_id]
  congr 1
  simp [Under.map, Comma.mapLeft]
  rfl

lemma coefficientPullback_one
    {X Y : CompHaus.{u}} (f : X ⟶ Y) :
    coefficientPresheaf.map f.op
        (show coefficientPresheaf.obj (op Y) from LocallyConstant.const Y (1 : R)) =
      (show coefficientPresheaf.obj (op X) from LocallyConstant.const X (1 : R)) := by
  rfl

lemma rankOneProjection_evalOne_naturality
    {X Y : CompHaus.{u}} (f : X ⟶ Y) :
    enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op Y) ⋙ coefficientPresheaf)
        (Under.forget (op Y) ⋙ coefficientPresheaf)
        (Under.mk f.op) ≫
      rankOneEndomorphismEvalOne X =
    rankOneIdentityProjection Y ≫ rankOneEndomorphismEvalOne Y ≫
      coefficientPresheaf.map f.op := by
  apply ModuleCat.hom_injective
  ext φ
  change
    rankOneProjectionEndomorphism Y (Under.mk f.op) φ
        (show coefficientPresheaf.obj (op X) from LocallyConstant.const X (1 : R)) =
      coefficientPresheaf.map f.op
        (rankOneProjectionEndomorphism Y (Under.mk (𝟙 (op Y))) φ
          (show coefficientPresheaf.obj (op Y) from LocallyConstant.const Y (1 : R)))
  have h := rankOneProjection_naturality Y
    (Under.homMk f.op : Under.mk (𝟙 (op Y)) ⟶ Under.mk f.op)
    φ
    (show coefficientPresheaf.obj (op Y) from LocallyConstant.const Y (1 : R))
  rw [coefficientPullback_one f] at h
  exact h.symm

lemma rankOneEvaluationApp_naturality
    {X Y : CompHaus.{u}} (f : X ⟶ Y) :
    rankOneInternalHom.map f.op ≫ rankOneEvaluationApp X =
      rankOneEvaluationApp Y ≫ coefficientPresheaf.map f.op := by
  unfold rankOneEvaluationApp
  rw [Category.assoc, rankOneInternalHom_map_identityProjection]
  exact rankOneProjection_evalOne_naturality f

noncomputable def rankOneInternalHomNatIso : RankOneTarget :=
  NatIso.ofComponents
    (fun X => rankOneObjectIso X.unop)
    (by
      intro X Y f
      simpa using rankOneEvaluationApp_naturality f.unop)

#check rankOneObjectIso
#check rankOneInternalHom_map_identityProjection
#check coefficientPullback_one
#check rankOneProjection_evalOne_naturality
#check rankOneEvaluationApp_naturality
#check rankOneInternalHomNatIso

#print axioms rankOneObjectIso
#print axioms rankOneInternalHom_map_identityProjection
#print axioms coefficientPullback_one
#print axioms rankOneProjection_evalOne_naturality
#print axioms rankOneEvaluationApp_naturality
#print axioms rankOneInternalHomNatIso

end CMDG.CondensedCM4P2E.InternalHom
