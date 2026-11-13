import CMDGCondensedCM4P3DerivedCM5R0StoneanProjective
import Mathlib.Condensed.EffectiveEpi
import Mathlib.Topology.Category.Stonean.Basic
import Mathlib.CategoryTheory.Functor.EpiMono

/-!
# CM5: Stonean projective epimorphism onto every profinite free condensed module

For arbitrary profinite T, its pinned Stonean presentation P(T) → T is
surjective. Mapping this cover first to compact Hausdorff objects and
then to the Yoneda condensed set preserves epimorphisms. Finally,
the free condensed-module functor preserves epimorphisms as a left
adjoint. Thus the free condensed object on P(T) projects onto F_T.
The source is projective, as proved in the preceding Stonean module.

This proves a projective presentation, NOT projectivity of F_T or
vanishing of Ext from F_T. The kernel/syzygy is the next obligation.
-/

noncomputable section

universe u

open CategoryTheory

namespace CMDG.CondensedCM5R0

/-- The canonical map from a Stonean free condensed module to the
free module on its profinite quotient. -/
noncomputable def freeStoneanPresentationMap (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj (Stonean.toProfinite.obj T.presentation) ⟶
      (Condensed.profiniteFree Coeff).obj T :=
  (Condensed.profiniteFree Coeff).map (Profinite.presentation.π T)

/-- The Stonean free-module presentation surjects in the *actual*
abelian category of condensed ZLift-modules. -/
theorem freeStoneanPresentationMap_epi (T : Profinite.{u}) :
    Epi (freeStoneanPresentationMap T) := by
  have hcomp : Epi (profiniteToCompHaus.map (Profinite.presentation.π T)) := by
    rw [CompHaus.epi_iff_surjective]
    exact (Profinite.epi_iff_surjective _).mp (inferInstance : Epi (Profinite.presentation.π T))
  have hset : Epi (profiniteToCondensed.map (Profinite.presentation.π T)) := by
    change Epi (compHausToCondensed.map (profiniteToCompHaus.map (Profinite.presentation.π T)))
    letI : Epi (profiniteToCompHaus.map (Profinite.presentation.π T)) := hcomp
    infer_instance
  haveI : Epi (profiniteToCondensed.map (Profinite.presentation.π T)) := hset
  haveI : PreservesEpimorphisms (Condensed.free Coeff) :=
    preservesEpimorphisms_of_adjunction (Condensed.freeForgetAdjunction Coeff)
  change Epi ((Condensed.free Coeff).map
    (profiniteToCondensed.map (Profinite.presentation.π T)))
  infer_instance

/-- The source of the canonical projective presentation is
projective in the actual condensed-module category. -/
theorem freeStoneanPresentation_source_projective (T : Profinite.{u}) :
    Projective ((Condensed.profiniteFree Coeff).obj
      (Stonean.toProfinite.obj T.presentation)) :=
  freeStonean_projective T.presentation

#print axioms freeStoneanPresentationMap_epi
#print axioms freeStoneanPresentation_source_projective

end CMDG.CondensedCM5R0
