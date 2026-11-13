import CMDGCondensedCM4P3DerivedCM5R0StoneanSolidTargetExtension
import Mathlib.Topology.Category.Profinite.Limits

/-!
# CM5: actual Čech fiber-product relations inside the Stonean kernel

For every profinite T, let p:P(T)→T be the canonical Stonean
surjection. The difference of the two free-condensed maps from the
fiber product P(T)×_T P(T) to P(T) maps to zero in F_T.
This gives an actual, canonical morphism from the free condensed
relation object to the kernel K_T in CondensedMod ZLift.

Composing this morphism with f:K_T→G_S constructs the concrete
solid-coefficient relation functional on the Čech pair object for
arbitrary profinite T and S.

**Not claimed:** the resulting relation-to-kernel map is an epi;
identifying K_T as the image of the relation map is a new
effective-descent/coequalizer obligation. The relation functional
has not yet been shown to be representable by compatible finite
quotient cocycles, nor does it itself construct an extension to F_P.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Profinite pullback of the actual Stonean presentation with itself. -/
noncomputable abbrev stoneanPresentationCechPairs (T : Profinite.{u}) :
    Profinite.{u} :=
  pullback (Profinite.presentation.π T) (Profinite.presentation.π T)

/-- The two endpoints of a Čech pair give a difference in the actual
free condensed module on the Stonean source. -/
noncomputable def stoneanCechDifference (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj (stoneanPresentationCechPairs T) ⟶
      (Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation) :=
  (Condensed.profiniteFree Coeff).map
      (pullback.fst (Profinite.presentation.π T) (Profinite.presentation.π T)) -
    (Condensed.profiniteFree Coeff).map
      (pullback.snd (Profinite.presentation.π T) (Profinite.presentation.π T))

/-- The Čech difference has zero composite with the canonical free
Stonean presentation epi. -/
theorem stoneanCechDifference_comp_zero (T : Profinite.{u}) :
    stoneanCechDifference T ≫ freeStoneanPresentationMap T = 0 := by
  unfold stoneanCechDifference freeStoneanPresentationMap
  rw [Preadditive.sub_comp, ← Functor.map_comp, ← Functor.map_comp,
    pullback.condition, sub_self]

/-- Canonical map from the free condensed Čech relation object into
the *actual* Stonean presentation kernel in CondensedMod ZLift. -/
noncomputable def stoneanCechRelationToKernel (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj (stoneanPresentationCechPairs T) ⟶
      stoneanPresentationKernel T :=
  kernel.lift (freeStoneanPresentationMap T)
    (stoneanCechDifference T) (stoneanCechDifference_comp_zero T)

/-- The Čech-to-kernel map agrees with the explicit difference map
after composing with the kernel inclusion. -/
theorem stoneanCechRelationToKernel_comp_ι (T : Profinite.{u}) :
    stoneanCechRelationToKernel T ≫
      kernel.ι (freeStoneanPresentationMap T) = stoneanCechDifference T := by
  simp [stoneanCechRelationToKernel]

/-- The actual solid coefficient target can be evaluated on the
canonical Čech relation object: this is a constructed morphism,
not a postulated finite-stage representative. -/
noncomputable def stoneanCechSolidRelationFunctional
    (T S : Profinite.{u})
    (f : stoneanPresentationKernel T ⟶ underivedObject S) :
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechPairs T) ⟶ underivedObject S :=
  stoneanCechRelationToKernel T ≫ f

#print axioms stoneanCechDifference_comp_zero
#print axioms stoneanCechRelationToKernel_comp_ι
#print axioms stoneanCechSolidRelationFunctional

end CMDG.CondensedCM5R0
