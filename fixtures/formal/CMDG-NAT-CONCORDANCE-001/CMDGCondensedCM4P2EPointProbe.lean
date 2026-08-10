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

#check coefficientPullback_const
#print axioms coefficientPullback_const

end CMDG.CondensedCM4P2E.InternalHom
