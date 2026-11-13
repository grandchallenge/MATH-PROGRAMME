import CMDGCondensedCM4P3DerivedCM5R0CechRelationEpi
import CMDGCondensedCM4P3DerivedCM5R0CechPotentialCriterion

/-!
# CM5: unconditional Čech-potential criterion for degree-one Ext vanishing

For arbitrary profinite T and S the actual Stonean Čech relation object
surjects onto the kernel of the free-module Stonean presentation.
Consequently, the existing kernel-morphism extension criterion does
not need an extra relation-epi hypothesis: a map K_T → G_S extends
along K_T → F_{P(T)} exactly when its explicit Čech relation functional
admits a potential on F_{P(T)}.

Combining this with the existing Ext¹/Hom-extension equivalence gives
an exact, unconditional reduction of Ext¹(F_T,G_S) vanishing to the
existence of these potentials for every kernel map.

This theorem is a criterion, *not* a construction of the potentials.
It does not assert infinite-profinite Ext¹ vanishing, derived solidity,
or that all arbitrary Čech cocycles are coboundaries.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The Stonean Čech-potential criterion for each individual kernel
morphism needs no additional epi assumption for any profinite T. -/
theorem solidKernelHom_extends_iff_cechPotential_unconditional
    (T S : Profinite.{u})
    (f : stoneanPresentationKernel T ⟶ underivedObject S) :
    (∃ g : ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) ⟶ underivedObject S,
        kernel.ι (freeStoneanPresentationMap T) ≫ g = f) ↔
    (∃ g : ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) ⟶ underivedObject S,
        stoneanCechDifference T ≫ g =
          stoneanCechSolidRelationFunctional T S f) := by
  letI : Epi (stoneanCechRelationToKernel T) :=
    stoneanCechRelationToKernel_epi T
  exact solidKernelHom_extends_iff_cechPotential T S f

/-- For every arbitrary profinite T and solid coefficient test G_S,
Ext¹(F_T,G_S) vanishes if and only if the explicit Čech-relation
functional induced by *every* actual kernel map has a potential.
No such potential is constructed by this equivalence. -/
theorem freeProfinite_extOne_vanishes_iff_all_solidCechPotentials
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext
        ((Condensed.profiniteFree Coeff).obj T) (underivedObject S) 1,
        e = 0) ↔
      (∀ f : stoneanPresentationKernel T ⟶ underivedObject S,
        ∃ g : ((Condensed.profiniteFree Coeff).obj
          (Stonean.toProfinite.obj T.presentation)) ⟶ underivedObject S,
          stoneanCechDifference T ≫ g =
            stoneanCechSolidRelationFunctional T S f) := by
  constructor
  · intro h f
    have hext :=
      (freeProfinite_extOne_vanishes_iff_kernel_hom_extends
        T (underivedObject S)).mp h
    exact (solidKernelHom_extends_iff_cechPotential_unconditional
      T S f).mp (hext f)
  · intro h
    apply (freeProfinite_extOne_vanishes_iff_kernel_hom_extends
      T (underivedObject S)).mpr
    intro f
    exact (solidKernelHom_extends_iff_cechPotential_unconditional
      T S f).mpr (h f)

#print axioms solidKernelHom_extends_iff_cechPotential_unconditional
#print axioms freeProfinite_extOne_vanishes_iff_all_solidCechPotentials

end CMDG.CondensedCM5R0
