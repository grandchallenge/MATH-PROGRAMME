import CMDGCondensedCM4P2EE1
import Mathlib.Condensed.Discrete.Characterization
import Mathlib.CategoryTheory.Monoidal.Closed.Braided

/-!
# CMDG CM4-P2-E E2 — measure-side right Kan reconstruction

This fixture is separate from the certified E1 layer.  It starts the E2 reconstruction by
identifying the P2-D continuous-function source as the filtered colimit of its finite quotients,
then transports that colimit through the canonical locally-constant condensed-module functor.

No E3 uniqueness statement or final comparison with `Condensed.profiniteSolid` is asserted here.
-/

namespace CMDG.CondensedCM4P2E.RightKanReconstruction

universe u

open CategoryTheory Limits Opposite

abbrev R := CMDG.CondensedCM4P2D.R.{u}
abbrev PresheafModule := CMDG.CondensedCM4P2D.PresheafModule

/-- The coefficient condensed module whose underlying presheaf is the protected P2-D coefficient
presheaf. -/
noncomputable abbrev coefficientCondensed : CondensedMod.{u} R :=
  (CondensedMod.LocallyConstant.functor R).obj (ModuleCat.of R R)

lemma coefficientCondensed_mem_locallyConstant :
    (CondensedMod.LocallyConstant.functor R).essImage coefficientCondensed :=
  ⟨ModuleCat.of R R, ⟨Iso.refl _⟩⟩

/-- The protected continuous-function module on a profinite set is the filtered colimit of the
continuous-function modules on its canonical finite quotients.  This is the module-valued form of
the pinned discrete-object characterization. -/
noncomputable def continuousFunctionsIsColimit (S : Profinite.{u}) :
    IsColimit
      (CMDG.CondensedCM4P2D.continuousFunctions.mapCocone S.asLimitCone.op) := by
  have h :=
    ((CondensedMod.isDiscrete_tfae R coefficientCondensed).out 3 6)
      coefficientCondensed_mem_locallyConstant
  change IsColimit
    ((profiniteToCompHaus.op ⋙ coefficientCondensed.obj).mapCocone S.asLimitCone.op)
  exact (h S).some

/-- The same finite-quotient colimit after applying the canonical locally-constant/discrete
condensed-module functor. -/
noncomputable abbrev discreteContinuousCondensed :
    Profinite.{u}ᵒᵖ ⥤ CondensedMod.{u} R :=
  CMDG.CondensedCM4P2D.continuousFunctions ⋙
    CondensedMod.LocallyConstant.functor R

noncomputable def discreteContinuousCondensedIsColimit (S : Profinite.{u}) :
    IsColimit (discreteContinuousCondensed.mapCocone S.asLimitCone.op) := by
  letI : (CondensedMod.LocallyConstant.functor R).IsLeftAdjoint :=
    (CondensedMod.LocallyConstant.adjunction R).isLeftAdjoint
  simpa [discreteContinuousCondensed] using
    (isColimitOfPreserves (CondensedMod.LocallyConstant.functor R)
      (continuousFunctionsIsColimit S))

/-- Forgetting the locally-constant condensed module recovers exactly the protected nested P2-D
presheaf. -/
example :
    discreteContinuousCondensed ⋙
        sheafToPresheaf (coherentTopology CompHaus.{u}) (ModuleCat.{u + 1} R) =
      CMDG.CondensedCM4P2D.discreteContinuousPresheaf := rfl

/-- Compiler gate for the objectwise finite-quotient colimit on the protected nested presheaf. -/
noncomputable def discreteContinuousPresheafIsColimit (S : Profinite.{u}) :
    IsColimit
      (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.mapCocone S.asLimitCone.op) := by
  have h := isColimitOfPreserves
    (sheafToPresheaf (coherentTopology CompHaus.{u}) (ModuleCat.{u + 1} R))
    (discreteContinuousCondensedIsColimit S)
  simpa [discreteContinuousCondensed] using h

#check continuousFunctionsIsColimit
#check discreteContinuousCondensedIsColimit
#check discreteContinuousPresheafIsColimit

#print axioms continuousFunctionsIsColimit
#print axioms discreteContinuousCondensedIsColimit
#print axioms discreteContinuousPresheafIsColimit

end CMDG.CondensedCM4P2E.RightKanReconstruction
