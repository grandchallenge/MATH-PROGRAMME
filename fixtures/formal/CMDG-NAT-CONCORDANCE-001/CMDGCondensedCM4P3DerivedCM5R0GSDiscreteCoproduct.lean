import CMDGCondensedCM4P3DerivedCM5R0GSMeasureBasisTransport
import CMDGCondensedCM4P3DerivedCM5R0DiscreteCoefficientCechBridge
import Mathlib.Algebra.Category.ModuleCat.Colimits
import Mathlib.CategoryTheory.Limits.Shapes.Coproducts
import Mathlib.Condensed.Limits

/-!
# CMDG CM5: genuine condensed coproduct of the Nöbeling discrete coefficient source

The protected source basis identifies C(S,R) with a Finsupp-indexed
direct sum of rank-one R-modules. This file lifts the actual colimiting
Finsupp cocone, *not merely the objectwise group direct sum*, through
the left adjoint discrete condensed-module functor.

The resulting proof is that the basis-indexed source is a genuine
categorical coproduct of rank-one discrete coefficient sheaves in
CondensedMod. This is precisely the colimit input needed for the next
enriched internal-Hom coproduct-to-product theorem.

It does not claim that enriched internal-Hom sends this coproduct to
a product without proof, or that higher derived Ext vanishes.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

private abbrev R : Type (u + 1) := CMDG.CondensedCM4P2D.R.{u}

/-- The actual basis-indexed discrete-source object in CondensedMod. -/
noncomputable def gsBasisDiscreteSourceCondensed (S : Profinite.{u}) :
    CondensedMod.{u} R.{u} :=
  (CondensedMod.LocallyConstant.functor R.{u}).obj
    (ModuleCat.of R.{u} (LiftedSourceBasisIndex S →₀ R.{u}))

/-- Exact Finsupp coproduct in ModuleCat: no finiteness assumption
on the index type is made. -/
noncomputable def gsBasisModuleFinsuppCoconeIsColimit
    (S : Profinite.{u}) :
    IsColimit
      (ModuleCat.finsuppCocone R.{u} R.{u} (LiftedSourceBasisIndex S)) :=
  ModuleCat.finsuppCoconeIsColimit R.{u} R.{u} (LiftedSourceBasisIndex S)

/-- Transport the true colimiting Finsupp cocone through the
left-adjoint discrete condensed-module functor. -/
noncomputable def gsBasisDiscreteCondensedCoconeIsColimit
    (S : Profinite.{u}) :
    IsColimit
      ((CondensedMod.LocallyConstant.functor R.{u}).mapCocone
        (ModuleCat.finsuppCocone R.{u} R.{u}
          (LiftedSourceBasisIndex S))) := by
  letI : (CondensedMod.LocallyConstant.functor R.{u}).IsLeftAdjoint :=
    (CondensedMod.LocallyConstant.adjunction R.{u}).isLeftAdjoint
  exact isColimitOfPreserves
    (CondensedMod.LocallyConstant.functor R.{u})
    (gsBasisModuleFinsuppCoconeIsColimit S)

/-- The Nöbeling source is genuinely a categorical coproduct in
the actual condensed-module category, not only in underlying modules.
The canonical rank-one summands are the exact discrete integer
coefficient sheaves consumed by the protected Ext¹ theorem. -/
noncomputable def gsBasisDiscreteSourceCoproductIso
    (S : Profinite.{u}) :
    (∐ (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff)) ≅
      gsBasisDiscreteSourceCondensed S := by
  letI : (CondensedMod.LocallyConstant.functor R.{u}).IsLeftAdjoint :=
    (CondensedMod.LocallyConstant.adjunction R.{u}).isLeftAdjoint
  exact
    (colimit.isColimit
      (Discrete.functor
        (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff)))
      .coconePointUniqueUpToIso
        (gsBasisDiscreteCondensedCoconeIsColimit S)

#print axioms gsBasisModuleFinsuppCoconeIsColimit
#print axioms gsBasisDiscreteCondensedCoconeIsColimit
#print axioms gsBasisDiscreteSourceCoproductIso

end CMDG.CondensedCM5R0
