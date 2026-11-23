import CMDGCondensedCM4P3DerivedCM5R0RealCircleSheafExact
import Mathlib.CategoryTheory.Abelian.ShortExact
import Mathlib.CategoryTheory.Abelian.FunctorCategory
import Mathlib.CategoryTheory.Sites.Abelian

noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf
open CMDG.CondensedCM5R0.RealCircleSheafExact

namespace CMDG.CondensedCM5R0.RealCircleSheafExact

variable (I : Type u)
local instance (I : Type u) :
    IsTopologicalAddGroup (ULift.{u+1,u} (I → UnitAddCircle)) := ⟨⟩

def sheafSeq :
    ShortComplex
      (Sheaf (coherentTopology Stonean.{u})
        (ModuleCat.{u+1} (ULift.{u+1} ℤ))) :=
  ShortComplex.mk
    (stoneanSheafMap (ULift.{u+1,u} (I → ℤ))
      (intProductTopHom I) (intProductTopHom_continuous I))
    (stoneanSheafMap (ULift.{u+1,u} (I → ℝ))
      (realProductTopHom I) (realProductTopHom_continuous I))
    (stoneanSheafMap_comp_zero
      (ULift.{u+1,u} (I → ℤ))
      (intProductTopHom I) (intProductTopHom_continuous I)
      (realProductTopHom I) (realProductTopHom_continuous I)
      (realProductTopHom_comp_intProductTopHom I))

theorem sheafSeq_shortExact :
    (sheafSeq I).ShortExact := by
  let F := sheafToPresheaf (coherentTopology Stonean.{u})
       (ModuleCat.{u+1} (ULift.{u+1} ℤ))
  apply CategoryTheory.ShortExact.reflects_shortExact_of_faithful F
  change (presheafSeq I).ShortExact
  exact presheafSeq_shortExact I

theorem realCircleCondensedSequence_shortExact :
    (realCircleCondensedSequence I).ShortExact := by
  letI : HasLimitsOfSize.{u,u+1}
      (ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
    hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  let E := Condensed.StoneanCompHaus.equivalence
    (ModuleCat.{u+1} (ULift.{u+1} ℤ))
  have h := ShortComplex.ShortExact.map_of_exact (sheafSeq_shortExact I) E.functor
  exact h

#print axioms realCircleCondensedSequence_shortExact

#print axioms sheafSeq_shortExact
end CMDG.CondensedCM5R0.RealCircleSheafExact
