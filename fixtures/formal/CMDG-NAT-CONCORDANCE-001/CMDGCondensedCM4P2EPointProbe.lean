import CMDGCondensedCM4P2EInternalHom

/-!
# CMDG CM4-P2-E point-probe recovery layer

This auxiliary fixture isolates the constant-map pullback facts needed for the reverse rank-one
internal-Hom triangle. It imports the certified internal-Hom checkpoint and adds no equivalence
claim on its own.
-/

namespace CMDG.CondensedCM4P2E.InternalHom

universe u

open CategoryTheory Opposite

lemma coefficientPullback_const
    {Y Z : CompHaus.{u}} (f : Y ⟶ Z) (z : Z)
    (hf : ∀ y, f y = z)
    (h : coefficientPresheaf.obj (op Z)) :
    coefficientPresheaf.map f.op h =
      (show coefficientPresheaf.obj (op Y) from
        LocallyConstant.const Y ((show LocallyConstant Z R from h) z)) := by
  change
    LocallyConstant.comap f.hom.hom (show LocallyConstant Z R from h) =
      LocallyConstant.const Y ((show LocallyConstant Z R from h) z)
  exact congrArg
    (fun q => q (show LocallyConstant Z R from h))
    (LocallyConstant.comap_const f.hom.hom z hf)

lemma coefficientPullback_const_op
    {Y Z : CompHaus.{u}ᵒᵖ} (f : Y ⟶ Z) (y : Y.unop)
    (hf : ∀ z : Z.unop, f.unop z = y)
    (h : coefficientPresheaf.obj Y) :
    coefficientPresheaf.map f h =
      (show coefficientPresheaf.obj Z from
        LocallyConstant.const Z.unop
          ((show LocallyConstant Y.unop R from h) y)) := by
  change
    LocallyConstant.comap f.unop.hom.hom (show LocallyConstant Y.unop R from h) =
      LocallyConstant.const Z.unop ((show LocallyConstant Y.unop R from h) y)
  exact congrArg
    (fun q => q (show LocallyConstant Y.unop R from h))
    (LocallyConstant.comap_const f.unop.hom.hom y hf)

lemma coefficientPullback_pointProbe
    (X : CompHaus.{u}) (k : Under (op X)) (y : k.right.unop)
    (h : coefficientPresheaf.obj k.right) :
    coefficientPresheaf.map (rankOnePointProbeFrom X k y).right h =
      (show coefficientPresheaf.obj (rankOnePointProbeObject X k y).right from
        LocallyConstant.const (rankOnePointProbeObject X k y).right.unop
          ((show LocallyConstant k.right.unop R from h) y)) := by
  apply coefficientPullback_const_op
  intro z
  rfl

lemma coefficientPullback_pointProbeFromIdentity
    (X : CompHaus.{u}) (k : Under (op X)) (y : k.right.unop)
    (h : coefficientAt X) :
    coefficientPresheaf.map (rankOnePointProbeFromIdentity X k y).right h =
      (show coefficientPresheaf.obj (rankOnePointProbeObject X k y).right from
        LocallyConstant.const (rankOnePointProbeObject X k y).right.unop
          ((show LocallyConstant X R from h) (k.hom.unop y))) := by
  apply coefficientPullback_const_op
  intro z
  rfl

#check coefficientPullback_const
#check coefficientPullback_const_op
#check coefficientPullback_pointProbe
#check coefficientPullback_pointProbeFromIdentity

#print axioms coefficientPullback_const
#print axioms coefficientPullback_const_op
#print axioms coefficientPullback_pointProbe
#print axioms coefficientPullback_pointProbeFromIdentity

end CMDG.CondensedCM4P2E.InternalHom
