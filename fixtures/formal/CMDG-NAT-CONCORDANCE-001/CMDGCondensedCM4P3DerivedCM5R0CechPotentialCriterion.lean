import CMDGCondensedCM4P3DerivedCM5R0CechKernelRelation
import CMDGCondensedCM4P3DerivedCM5R0KernelHomExtension

/-!
# CM5: actual Čech-potential criterion for extensions into solid targets

For arbitrary profinite T and S, an actual condensed-module morphism
f:K_T→G_S induces the genuine relation functional
F_{P×_T P}→G_S. If this relation-to-kernel map is epi, any
potential g:F_P→G_S satisfying the Čech difference identity must
extend f on the entire kernel; this is proven by cancellation of
the exact relation epi, not by finite-level extrapolation.

This translates the missing kernel extension into precisely typed
Čech data. The epi premise for arbitrary T is NOT discharged.
Nor is a potential g constructed for non-Stonean T.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Under the precisely identified Čech relation generation hypothesis,
an actual solid-target potential with the correct Čech difference
extends the original morphism from the entire Stonean kernel. -/
theorem solidCechPotential_restricts_to_kernel
    (T S : Profinite.{u})
    [Epi (stoneanCechRelationToKernel T)]
    (f : stoneanPresentationKernel T ⟶ underivedObject S)
    (g : ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) ⟶ underivedObject S)
    (hg : stoneanCechDifference T ≫ g =
      stoneanCechSolidRelationFunctional T S f) :
    kernel.ι (freeStoneanPresentationMap T) ≫ g = f := by
  apply (cancel_epi (stoneanCechRelationToKernel T)).1
  calc
    stoneanCechRelationToKernel T ≫
        (kernel.ι (freeStoneanPresentationMap T) ≫ g) =
      (stoneanCechRelationToKernel T ≫
        kernel.ι (freeStoneanPresentationMap T)) ≫ g :=
      (Category.assoc _ _ _).symm
    _ = stoneanCechDifference T ≫ g := by
      rw [stoneanCechRelationToKernel_comp_ι]
    _ = stoneanCechSolidRelationFunctional T S f := hg
    _ = stoneanCechRelationToKernel T ≫ f := rfl

/-- The actual solid-target extension problem is equivalent to
constructing a Čech potential with the prescribed relation
functional, provided the relation map generates K_T. This
equivalence makes no claim that this premise holds for all T. -/
theorem solidKernelHom_extends_iff_cechPotential
    (T S : Profinite.{u})
    [Epi (stoneanCechRelationToKernel T)]
    (f : stoneanPresentationKernel T ⟶ underivedObject S) :
    (∃ g : ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) ⟶ underivedObject S,
        kernel.ι (freeStoneanPresentationMap T) ≫ g = f) ↔
    (∃ g : ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) ⟶ underivedObject S,
        stoneanCechDifference T ≫ g =
          stoneanCechSolidRelationFunctional T S f) := by
  constructor
  · rintro ⟨g, hg⟩
    refine ⟨g, ?_⟩
    unfold stoneanCechSolidRelationFunctional
    rw [← hg, ← Category.assoc, stoneanCechRelationToKernel_comp_ι]
  · rintro ⟨g, hg⟩
    exact ⟨g, solidCechPotential_restricts_to_kernel T S f g hg⟩

#print axioms solidCechPotential_restricts_to_kernel
#print axioms solidKernelHom_extends_iff_cechPotential

end CMDG.CondensedCM5R0
