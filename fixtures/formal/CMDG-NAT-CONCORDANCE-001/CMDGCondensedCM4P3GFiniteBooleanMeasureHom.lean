import CMDGCondensedCM4P3GFiniteBooleanMeasure

/-!
# CMDG CM4-P3-G finite-stage Boolean measure morphisms

This fixture packages each concrete finite Boolean measure section through the generic
profinite-free/section equivalence. No compatibility or limit lift is asserted here.
-/

namespace CMDG.CondensedCM4P3G.FiniteBooleanMeasureHom

universe u

open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- The finite-stage universal Boolean measure family as a condensed-module morphism. -/
noncomputable def finiteBooleanMeasureHom
    (X : Profinite.{u}) (j : DiscreteQuotient X) :
    (Condensed.profiniteFree R).obj (basisBooleanCube X) ⟶
      CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j) :=
  (freeHomSectionsEquiv
      (basisBooleanCube X)
      (CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j))).symm
    (finiteBooleanMeasureSection X j)

#print finiteBooleanMeasureHom
#print axioms finiteBooleanMeasureHom

end CMDG.CondensedCM4P3G.FiniteBooleanMeasureHom
