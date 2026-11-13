import CMDGCondensedCM4P3DerivedCM5R0StoneanPresentation
import Mathlib.Condensed.EffectiveEpi
import Mathlib.Topology.Category.Profinite.EffectiveEpi

/-!
# CM5: the exact Stonean presentation is an effective epi of condensed sets

The Stonean presentation P(T) → T of an arbitrary profinite T
is an effective epimorphism in Profinite. The profinite-to-CompHaus
and CompHaus-to-condensed Yoneda functors preserve effective epis.

Consequently the actual condensed-set morphism
  P(T).toCondensed → T.toCondensed
is an effective epimorphism: descent from its Čech nerve is governed
by a universal coequalizer rather than an unsupported finite-test
extrapolation.

**Boundary:** the theorem is in CondensedSet, not the derived
CondensedMod Ext category, and it does not yet identify the
Stonean free-module kernel with the image of its Čech relation
module or show integer cocycles are coboundaries.
-/

noncomputable section

universe u

open CategoryTheory

namespace CMDG.CondensedCM5R0

/-- The actual profinite Stonean cover is an effective epimorphism,
even when the profinite base is infinite. -/
theorem stoneanPresentation_effectiveEpi_profinite
    (T : Profinite.{u}) :
    EffectiveEpi (Profinite.presentation.π T) := by
  exact ((Profinite.effectiveEpi_tfae (Profinite.presentation.π T)).out 1 0).mp
    (inferInstance : Epi (Profinite.presentation.π T))

/-- The same cover becomes an effective epi of *condensed sets* after
applying the exact universe-lifted profinite Yoneda embedding. -/
theorem stoneanPresentation_effectiveEpi_condensed
    (T : Profinite.{u}) :
    EffectiveEpi
      (profiniteToCondensed.map (Profinite.presentation.π T)) := by
  letI : EffectiveEpi (Profinite.presentation.π T) :=
    stoneanPresentation_effectiveEpi_profinite T
  haveI : EffectiveEpi
      (profiniteToCompHaus.map (Profinite.presentation.π T)) :=
    inferInstance
  change EffectiveEpi (compHausToCondensed.map
    (profiniteToCompHaus.map (Profinite.presentation.π T)))
  infer_instance

/-- For any actual CM5 solid target G_S, a condensed-set map
from the Stonean covering probe descends *constructively* whenever
it respects the effective-epi Čech relation. This is a degree-zero
set-valued descent construction, not the missing arbitrary-kernel
module morphism extension. -/
noncomputable def descendStoneanCoverToSolidUnderlying
    (T S : Profinite.{u})
    (e : (Stonean.toProfinite.obj T.presentation).toCondensed ⟶
      (Condensed.forget Coeff).obj (underivedObject S))
    (h : ∀ {Z : CondensedSet.{u}}
      (g₁ g₂ : Z ⟶ (Stonean.toProfinite.obj T.presentation).toCondensed),
        g₁ ≫ profiniteToCondensed.map (Profinite.presentation.π T) =
        g₂ ≫ profiniteToCondensed.map (Profinite.presentation.π T) →
        g₁ ≫ e = g₂ ≫ e) :
    T.toCondensed ⟶ (Condensed.forget Coeff).obj (underivedObject S) := by
  letI : EffectiveEpi (profiniteToCondensed.map (Profinite.presentation.π T)) :=
    stoneanPresentation_effectiveEpi_condensed T
  exact EffectiveEpi.desc
    (profiniteToCondensed.map (Profinite.presentation.π T)) e h

/-- The constructed descended map restricts to the original
compatible solid-target section on the Stonean presentation. -/
theorem descendStoneanCoverToSolidUnderlying_fac
    (T S : Profinite.{u})
    (e : (Stonean.toProfinite.obj T.presentation).toCondensed ⟶
      (Condensed.forget Coeff).obj (underivedObject S))
    (h : ∀ {Z : CondensedSet.{u}}
      (g₁ g₂ : Z ⟶ (Stonean.toProfinite.obj T.presentation).toCondensed),
        g₁ ≫ profiniteToCondensed.map (Profinite.presentation.π T) =
        g₂ ≫ profiniteToCondensed.map (Profinite.presentation.π T) →
        g₁ ≫ e = g₂ ≫ e) :
    profiniteToCondensed.map (Profinite.presentation.π T) ≫
      descendStoneanCoverToSolidUnderlying T S e h = e := by
  letI : EffectiveEpi (profiniteToCondensed.map (Profinite.presentation.π T)) :=
    stoneanPresentation_effectiveEpi_condensed T
  exact EffectiveEpi.fac (profiniteToCondensed.map (Profinite.presentation.π T)) e h

#print axioms descendStoneanCoverToSolidUnderlying_fac
#print axioms stoneanPresentation_effectiveEpi_profinite
#print axioms stoneanPresentation_effectiveEpi_condensed

end CMDG.CondensedCM5R0
