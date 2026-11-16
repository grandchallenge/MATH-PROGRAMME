import CMDGCondensedCM4P3DerivedCM5R0GSDiscreteBasis
import CMDGCondensedCM4P2EE3
import Mathlib.CategoryTheory.Sites.Monoidal

/-!
# CM5: actual free-solid target transported to the Nöbeling-basis internal Hom

The previous exact-head Lean theorem constructed the R-module and
presheaf isomorphism C(S,R)_disc ≅ (⊕_(i∈I_S) R)_disc.
The protected CM4-P2-D target is the *enriched internal Hom* out of
precisely that source presheaf. We transport the source isomorphism
contravariantly through internalHom, prove that the resulting target
is itself a sheaf, and use protected CM4-P2-E right-Kan uniqueness
to obtain a genuine isomorphism IN CondensedMod from G_S to this
basis-indexed enriched-Hom target.

It does not yet assert enrichedHom(⊕ R_disc, R_disc) ≅ ∏ R_disc.
This remaining coproduct-to-product bridge is a substantive separate
mathematical theorem, and higher derived Ext is not addressed here.
-/

noncomputable section

universe u

open CategoryTheory Opposite
open CategoryTheory.Enriched.FunctorCategory
open scoped CategoryTheory.MonoidalClosed

namespace CMDG.CondensedCM5R0

noncomputable local instance : MonoidalClosed
    CMDG.CondensedCM4P2D.PresheafModule.{u} :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- The exact discrete basis-source presheaf in the protected P2-D model. -/
noncomputable def gsBasisDiscreteSourcePresheaf (S : Profinite.{u}) :
    CMDG.CondensedCM4P2D.PresheafModule.{u} :=
  (CondensedMod.LocallyConstant.functorToPresheaves
    CMDG.CondensedCM4P2D.R.{u}).obj
      (ModuleCat.of CMDG.CondensedCM4P2D.R.{u}
        (LiftedSourceBasisIndex S →₀ CMDG.CondensedCM4P2D.R.{u}))

/-- The candidate basis-dual presheaf: this remains the genuine
enriched internal Hom, with its naturality end, not an objectwise
ordinary module Hom substituted without proof. -/
noncomputable def gsBasisInternalHomPresheaf (S : Profinite.{u}) :
    CMDG.CondensedCM4P2D.PresheafModule.{u} :=
  (MonoidalClosed.internalHom.obj
    (op (gsBasisDiscreteSourcePresheaf S))).obj
      CMDG.CondensedCM4P2D.coefficientPresheaf

/-- Transport the certified basis source isomorphism contravariantly
through the actual presheaf-category internal Hom. -/
noncomputable def measureToBasisInternalHomPresheafIso
    (S : Profinite.{u}) :
    CMDG.CondensedCM4P2D.measurePresheafObj S ≅
      gsBasisInternalHomPresheaf S := by
  change
    (MonoidalClosed.internalHom.obj
      (op (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj (op S)))).obj
        CMDG.CondensedCM4P2D.coefficientPresheaf ≅
      (MonoidalClosed.internalHom.obj
        (op (gsBasisDiscreteSourcePresheaf S))).obj
          CMDG.CondensedCM4P2D.coefficientPresheaf
  exact ((MonoidalClosed.internalHom).mapIso
    (liftedSourcePresheafIso S).symm.op).app
      CMDG.CondensedCM4P2D.coefficientPresheaf

/-- The resulting enriched-Hom object is still an actual sheaf. -/
theorem gsBasisInternalHom_isSheaf (S : Profinite.{u}) :
    Presheaf.IsSheaf (coherentTopology CompHaus.{u})
      (gsBasisInternalHomPresheaf S) := by
  change Presheaf.IsSheaf (coherentTopology CompHaus.{u})
    (functorEnrichedHom (ModuleCat.{u + 1}
      CMDG.CondensedCM4P2D.R.{u})
      (gsBasisDiscreteSourcePresheaf S)
      CMDG.CondensedCM4P2D.coefficientPresheaf)
  apply Presheaf.isSheaf_functorEnrichedHom
  exact ((CondensedMod.LocallyConstant.functor
    CMDG.CondensedCM4P2D.R.{u}).obj
      (ModuleCat.of CMDG.CondensedCM4P2D.R.{u}
        CMDG.CondensedCM4P2D.R.{u})).2

/-- The basis-dual enriched-Hom sheaf, as an actual condensed module. -/
noncomputable def gsBasisInternalHomCondensed (S : Profinite.{u}) :
    CondensedMod.{u} CMDG.CondensedCM4P2D.R.{u} :=
  ⟨gsBasisInternalHomPresheaf S, gsBasisInternalHom_isSheaf S⟩

/-- The protected measure object is isomorphic to the basis-dual
target inside CondensedMod, not merely as groups of global sections. -/
noncomputable def measureToBasisInternalHomCondensedIso
    (S : Profinite.{u}) :
    CMDG.CondensedCM4P2D.measureFunctor.obj S ≅
      gsBasisInternalHomCondensed S :=
  ObjectProperty.isoMk
    (Presheaf.IsSheaf (coherentTopology CompHaus.{u}))
    (measureToBasisInternalHomPresheafIso S)

/-- Genuine comparison from the ACTUAL free solid target G_S to the
Nöbeling-basis enriched-Hom condensed module. This is an unconditional
categorical isomorphism, but the RHS is not YET a product. -/
noncomputable def freeSolidToBasisInternalHomCondensedIso
    (S : Profinite.{u}) :
    (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S ≅
      gsBasisInternalHomCondensed S :=
  (CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness
    .measureProfiniteSolidNatIso.app S).symm ≪≫
      measureToBasisInternalHomCondensedIso S

#check gsBasisDiscreteSourcePresheaf
#check gsBasisInternalHomPresheaf
#check measureToBasisInternalHomPresheafIso
#check gsBasisInternalHom_isSheaf
#check gsBasisInternalHomCondensed
#check measureToBasisInternalHomCondensedIso
#check freeSolidToBasisInternalHomCondensedIso

#print axioms measureToBasisInternalHomPresheafIso
#print axioms gsBasisInternalHom_isSheaf
#print axioms gsBasisInternalHomCondensed
#print axioms measureToBasisInternalHomCondensedIso
#print axioms freeSolidToBasisInternalHomCondensedIso

end CMDG.CondensedCM5R0
