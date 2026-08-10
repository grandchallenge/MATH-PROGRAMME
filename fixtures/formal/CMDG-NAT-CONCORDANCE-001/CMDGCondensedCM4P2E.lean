import CMDGCondensedCM4P2D
import Mathlib.Condensed.Solid
import Mathlib.Condensed.Discrete.Colimit
import Mathlib.CategoryTheory.Functor.KanExtension.Basic
import Mathlib.CategoryTheory.Functor.KanExtension.Pointwise

/-!
# CMDG CM4-P2-E comparison audit

This fixture freezes the exact P2-E theorem target after protected admission of P2-D.
It records the finite-restriction and right-Kan-extension interfaces needed to identify the
protected canonical measure/dual functor with `Condensed.profiniteSolid`.

No natural equivalence is asserted in this audit fixture. The separately reviewed P2-E proof
must construct the finite-level comparison and the right-Kan-extension property before invoking
Kan-extension uniqueness.
-/

namespace CMDG.CondensedCM4P2E

universe u

open CategoryTheory

/-- The exact lifted integral coefficient ring inherited from protected P2-D. -/
abbrev R := CMDG.CondensedCM4P2D.R

/-- The protected P2-D canonical measure/dual functor. -/
noncomputable abbrev measureFunctor : Profinite.{u} ⥤ CondensedMod.{u} R :=
  CMDG.CondensedCM4P2D.measureFunctor

/-- The pinned solid functor to which P2-E must compare the protected P2-D functor. -/
noncomputable abbrev solidFunctor : Profinite.{u} ⥤ CondensedMod.{u} R :=
  Condensed.profiniteSolid R

/-- Restriction of the protected measure/dual functor to finite profinite sets. -/
noncomputable abbrev finiteMeasure : FintypeCat.{u} ⥤ CondensedMod.{u} R :=
  FintypeCat.toProfinite ⋙ measureFunctor

/-- The exact finite-free functor used by `Condensed.profiniteSolid`. -/
noncomputable abbrev finiteFree : FintypeCat.{u} ⥤ CondensedMod.{u} R :=
  Condensed.finFree R

/-- The finite comparison that P2-E must construct canonically and naturally. -/
abbrev FiniteComparisonTarget := finiteMeasure ≅ finiteFree

/-- The final P2-E theorem target. -/
abbrev ComparisonTarget := measureFunctor ≅ solidFunctor

#check CMDG.CondensedCM4P2D.measureFunctor
#check CMDG.CondensedCM4P2D.dualityHomEquiv
#check Condensed.finFree
#check Condensed.profiniteSolid
#check Condensed.profiniteSolidCounit
#check Condensed.profiniteSolidIsPointwiseRightKanExtension
#check Functor.rightKanExtensionUniqueOfIso
#check Functor.rightKanExtensionUnique
#check Condensed.isColimitLocallyConstantPresheafDiagram
#check Condensed.lanPresheafNatIso

end CMDG.CondensedCM4P2E
