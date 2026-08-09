import Mathlib.Condensed.Solid
import Mathlib.Condensed.Discrete.Module
import Mathlib.CategoryTheory.Sites.Monoidal
import Mathlib.Algebra.Category.ModuleCat.Monoidal.Closed
import Mathlib.Algebra.Module.ULift

/-!
# CMDG CM4-P2-D canonical measure/dual model

This fixture reconstructs the basis-free condensed-module dual of the discrete module of
locally constant integer-valued functions on a profinite set. It deliberately does not identify
that model with `Condensed.profiniteSolid`; that natural comparison is the separately governed
P2-E operation.
-/

namespace CMDG.CondensedCM4P2D

universe u

open CategoryTheory Opposite
open CategoryTheory.Enriched.FunctorCategory
open CategoryTheory.MonoidalCategory

/-- The exact lifted integral coefficient ring used by the pinned condensed construction. -/
abbrev R := ULift.{u + 1} ℤ

/-- Presheaves of lifted integral modules on compact Hausdorff spaces. -/
abbrev PresheafModule := CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R

/-- The discrete integral coefficient presheaf, presented by locally constant functions. -/
noncomputable abbrev coefficientPresheaf : PresheafModule :=
  (CondensedMod.LocallyConstant.functorToPresheaves R).obj (ModuleCat.of R R)

/-- Continuous `R`-valued functions on profinite sets, contravariantly functorial by pullback. -/
noncomputable abbrev continuousFunctions :
    Profinite.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R :=
  profiniteToCompHaus.op ⋙ coefficientPresheaf

/-- The discrete condensed-module presentation of `C(S,R)`, before taking the internal dual. -/
noncomputable abbrev discreteContinuousPresheaf :
    Profinite.{u}ᵒᵖ ⥤ PresheafModule :=
  continuousFunctions ⋙ CondensedMod.LocallyConstant.functorToPresheaves R

/--
The canonical basis-free internal-Hom presheaf
`underline Hom(C(S,R)_disc, R_disc)`.
-/
noncomputable def measurePresheafObj (S : Profinite.{u}) : PresheafModule :=
  functorEnrichedHom (ModuleCat.{u + 1} R)
    (discreteContinuousPresheaf.obj (op S)) coefficientPresheaf

/-- The internal-Hom presheaf is already a sheaf because its target is a sheaf. -/
theorem measurePresheafObj_isSheaf (S : Profinite.{u}) :
    Presheaf.IsSheaf (coherentTopology CompHaus.{u}) (measurePresheafObj S) := by
  apply Presheaf.isSheaf_functorEnrichedHom
  exact ((CondensedMod.LocallyConstant.functor R).obj (ModuleCat.of R R)).2

/--
The canonical measure/dual presheaf functor. A map `S ⟶ T` acts by pullback
`C(T,R) ⟶ C(S,R)` followed by contravariance of internal Hom in its first argument.
-/
noncomputable def measurePresheafFunctor : Profinite.{u} ⥤ PresheafModule := by
  letI : MonoidalClosed PresheafModule :=
    MonoidalClosed.FunctorCategory.monoidalClosed
  exact
    { obj := measurePresheafObj
      map := fun f ↦
        (MonoidalClosed.pre (discreteContinuousPresheaf.map f.op)).app coefficientPresheaf
      map_id := by
        intro S
        simp [measurePresheafObj]
      map_comp := by
        intro S T U f g
        simp [measurePresheafObj] }

/-- The canonical measure/dual condensed-module functor attached to profinite sets. -/
noncomputable def measureFunctor : Profinite.{u} ⥤ CondensedMod.{u} R :=
  ObjectProperty.lift _ measurePresheafFunctor measurePresheafObj_isSheaf

/--
The defining closed-monoidal duality interface. It characterizes `measurePresheafObj S`
without choosing a Nöbeling basis or replacing the internal Hom by an objectwise product.
-/
noncomputable def dualityHomEquiv (S : Profinite.{u}) (F : PresheafModule) :
    (discreteContinuousPresheaf.obj (op S) ⊗ F ⟶ coefficientPresheaf) ≃
      (F ⟶ measurePresheafObj S) :=
  MonoidalClosed.FunctorCategory.homEquiv

#check measureFunctor
#check dualityHomEquiv
#check Presheaf.isSheaf_functorEnrichedHom
#check ModuleCat.monoidalClosedHomEquiv

#print axioms measurePresheafObj_isSheaf
#print axioms measurePresheafFunctor
#print axioms measureFunctor
#print axioms dualityHomEquiv

end CMDG.CondensedCM4P2D
