import CMDGCondensedCM4P2EPointProbe

/-!
# CMDG CM4-P2-E point-probe projection recovery

This auxiliary fixture assembles the certified point-probe geometry, coefficient pullback formulas,
and enriched-end naturality toward the reverse rank-one triangle. It begins with the two canonical
probe-naturality equations and makes no final equivalence claim on its own.
-/

namespace CMDG.CondensedCM4P2E.InternalHom

universe u

open CategoryTheory Opposite

lemma rankOnePointProbe_naturality
    (X : CompHaus.{u}) (k : Under (op X)) (y : k.right.unop)
    (φ : rankOneInternalHom.obj (op X))
    (h : coefficientPresheaf.obj k.right) :
    (show coefficientPresheaf.obj (rankOnePointProbeObject X k y).right from
      LocallyConstant.const (rankOnePointProbeObject X k y).right.unop
        ((show LocallyConstant k.right.unop R from
          rankOneProjectionEndomorphism X k φ h) y)) =
      rankOneProjectionEndomorphism X (rankOnePointProbeObject X k y) φ
        (show coefficientPresheaf.obj (rankOnePointProbeObject X k y).right from
          LocallyConstant.const (rankOnePointProbeObject X k y).right.unop
            ((show LocallyConstant k.right.unop R from h) y)) := by
  have hnat := rankOneProjection_naturality X (rankOnePointProbeFrom X k y) φ h
  change
    coefficientPresheaf.map (rankOnePointProbeFrom X k y).right
        (rankOneProjectionEndomorphism X k φ h) =
      rankOneProjectionEndomorphism X (rankOnePointProbeObject X k y) φ
        (coefficientPresheaf.map (rankOnePointProbeFrom X k y).right h) at hnat
  rw [coefficientPullback_pointProbe X k y
        (rankOneProjectionEndomorphism X k φ h),
      coefficientPullback_pointProbe X k y h] at hnat
  exact hnat

lemma rankOnePointProbe_identity_naturality
    (X : CompHaus.{u}) (k : Under (op X)) (y : k.right.unop)
    (φ : rankOneInternalHom.obj (op X)) :
    (show coefficientPresheaf.obj (rankOnePointProbeObject X k y).right from
      LocallyConstant.const (rankOnePointProbeObject X k y).right.unop
        ((show LocallyConstant X R from rankOneEvaluationApp X φ) (k.hom.unop y))) =
      rankOneProjectionEndomorphism X (rankOnePointProbeObject X k y) φ
        (show coefficientPresheaf.obj (rankOnePointProbeObject X k y).right from
          LocallyConstant.const (rankOnePointProbeObject X k y).right.unop (1 : R)) := by
  let one : coefficientAt X := LocallyConstant.const X (1 : R)
  have hnat := rankOneProjection_naturality X
    (rankOnePointProbeFromIdentity X k y) φ one
  change
    coefficientPresheaf.map (rankOnePointProbeFromIdentity X k y).right
        (rankOneProjectionEndomorphism X (Under.mk (𝟙 (op X))) φ one) =
      rankOneProjectionEndomorphism X (rankOnePointProbeObject X k y) φ
        (coefficientPresheaf.map (rankOnePointProbeFromIdentity X k y).right one) at hnat
  rw [coefficientPullback_pointProbeFromIdentity X k y
        (rankOneProjectionEndomorphism X (Under.mk (𝟙 (op X))) φ one),
      coefficientPullback_pointProbeFromIdentity_one X k y] at hnat
  rw [← rankOneEvaluationApp_apply X φ] at hnat
  exact hnat

lemma rankOnePointProbe_constant_recovery
    (X : CompHaus.{u}) (k : Under (op X)) (y : k.right.unop)
    (φ : rankOneInternalHom.obj (op X))
    (h : coefficientPresheaf.obj k.right) :
    (show coefficientPresheaf.obj (rankOnePointProbeObject X k y).right from
      LocallyConstant.const (rankOnePointProbeObject X k y).right.unop
        ((show LocallyConstant k.right.unop R from
          rankOneProjectionEndomorphism X k φ h) y)) =
      ((show LocallyConstant k.right.unop R from h) y) •
        (show coefficientPresheaf.obj (rankOnePointProbeObject X k y).right from
          LocallyConstant.const (rankOnePointProbeObject X k y).right.unop
            ((show LocallyConstant X R from rankOneEvaluationApp X φ) (k.hom.unop y))) := by
  let P : Under (op X) := rankOnePointProbeObject X k y
  let r : R := (show LocallyConstant k.right.unop R from h) y
  calc
    (show coefficientPresheaf.obj P.right from
      LocallyConstant.const P.right.unop
        ((show LocallyConstant k.right.unop R from
          rankOneProjectionEndomorphism X k φ h) y)) =
        rankOneProjectionEndomorphism X P φ
          (show coefficientPresheaf.obj P.right from
            LocallyConstant.const P.right.unop r) :=
      rankOnePointProbe_naturality X k y φ h
    _ = r • rankOneProjectionEndomorphism X P φ
          (show coefficientPresheaf.obj P.right from
            LocallyConstant.const P.right.unop (1 : R)) :=
      rankOneProjectionEndomorphism_const X P φ r
    _ = r •
          (show coefficientPresheaf.obj P.right from
            LocallyConstant.const P.right.unop
              ((show LocallyConstant X R from rankOneEvaluationApp X φ) (k.hom.unop y))) := by
      exact congrArg (fun q => r • q)
        (rankOnePointProbe_identity_naturality X k y φ).symm

#check rankOnePointProbe_naturality
#check rankOnePointProbe_identity_naturality
#check rankOnePointProbe_constant_recovery

#print axioms rankOnePointProbe_naturality
#print axioms rankOnePointProbe_identity_naturality
#print axioms rankOnePointProbe_constant_recovery

end CMDG.CondensedCM4P2E.InternalHom
