import Mathlib.Condensed.Solid
import Mathlib.Condensed.Discrete.Module
import Mathlib.CategoryTheory.Sites.Monoidal
import Mathlib.Algebra.Category.ModuleCat.Monoidal.Closed
import Mathlib.Algebra.Module.ULift

/-!
# CMDG CM4-P2-D canonical measure/dual model

This fixture reconstructs the basis-free condensed-module dual of the discrete module of
locally constant integer-valued functions on a profinite set.  It deliberately does not identify
that model with `Condensed.profiniteSolid`; that natural comparison is the separately governed
P2-E operation.
-/

namespace CMDG.CondensedCM4P2D

universe u

open CategoryTheory Opposite
open CategoryTheory.Enriched.FunctorCategory

/-- The exact lifted integral coefficient ring used by `Condensed.profiniteSolid`. -/
abbrev R := ULift.{u + 1} ℤ

/-- The discrete integral coefficient presheaf, presented by locally constant functions. -/
noncomputable abbrev coefficientPresheaf :
    CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R :=
  (CondensedMod.LocallyConstant.functorToPresheaves R).obj (ModuleCat.of R R)

/-- Continuous `R`-valued functions on profinite sets, contravariantly functorial by pullback. -/
noncomputable abbrev continuousFunctions :
    Profinite.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R :=
  profiniteToCompHaus.op ⋙ coefficientPresheaf

/-- The discrete condensed-module presentation of `C(S,R)`, before taking the internal dual. -/
noncomputable abbrev discreteContinuousPresheaf :
    Profinite.{u}ᵒᵖ ⥤ (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R) :=
  continuousFunctions ⋙ CondensedMod.LocallyConstant.functorToPresheaves R

/--
The canonical basis-free internal-Hom presheaf
`underline Hom(C(S,R)_disc, R_disc)`.
-/
noncomputable def measurePresheafObj (S : Profinite.{u}) :
    CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R :=
  functorEnrichedHom (ModuleCat.{u + 1} R)
    (discreteContinuousPresheaf.obj (op S)) coefficientPresheaf

/-- The internal-Hom presheaf is already a sheaf because its target is a sheaf. -/
theorem measurePresheafObj_isSheaf (S : Profinite.{u}) :
    Presheaf.IsSheaf (coherentTopology CompHaus.{u}) (measurePresheafObj S) := by
  apply Presheaf.isSheaf_functorEnrichedHom
  exact ((CondensedMod.LocallyConstant.functor R).obj (ModuleCat.of R R)).2

/-- The canonical measure/dual condensed module attached to `S`. -/
noncomputable def measureObj (S : Profinite.{u}) : CondensedMod.{u} R :=
  ⟨measurePresheafObj S, measurePresheafObj_isSheaf S⟩

#check measureObj
#check Presheaf.isSheaf_functorEnrichedHom
#check ModuleCat.monoidalClosedHomEquiv

end CMDG.CondensedCM4P2D
