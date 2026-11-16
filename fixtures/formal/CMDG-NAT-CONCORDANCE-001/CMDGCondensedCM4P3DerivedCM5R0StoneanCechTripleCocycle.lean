import CMDGCondensedCM4P3DerivedCM5R0DiscreteProductCechDifferential
import CMDGCondensedCM4P3DerivedCM5R0CechRelationEpi

/-!
# CMDG CM5 — genuine Stonean triple Čech relation cocycle

The Čech pair relation of the actual Stonean presentation has an honest
profinite triple object. We construct its three pair projections using
categorical pullbacks; the resulting three pullbacks of the *actual*
free-module difference satisfy the alternating sum identity.

Because the genuine relation-to-kernel morphism factors through the
monomorphism K_T → F_{P(T)}, the same identity holds in K_T. Hence every
genuine kernel-induced cochain with ANY target satisfies the true
categorical triple-cocycle law, including targets that have no scalar
product representation. This is stronger than merely assuming that
scalar candidate cochains satisfy a cocycle relation.

No potential for a G_S-valued kernel functional is constructed here.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Honest triple fiber relation (P ×_T P) ×_T P of the actual
Stonean presentation P(T) → T. -/
noncomputable abbrev stoneanPresentationCechTriples
    (T : Profinite.{u}) : Profinite.{u} :=
  pullback
    (pullback.fst (Profinite.presentation.π T)
      (Profinite.presentation.π T) ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)

/-- The first (x,y) pair. -/
noncomputable abbrev stoneanCechTripleXY
    (T : Profinite.{u}) :
    stoneanPresentationCechTriples T ⟶
      stoneanPresentationCechPairs T :=
  pullback.fst
    (pullback.fst (Profinite.presentation.π T)
      (Profinite.presentation.π T) ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)

/-- The third endpoint z. -/
noncomputable abbrev stoneanCechTripleZ
    (T : Profinite.{u}) :
    stoneanPresentationCechTriples T ⟶
      Stonean.toProfinite.obj T.presentation :=
  pullback.snd
    (pullback.fst (Profinite.presentation.π T)
      (Profinite.presentation.π T) ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)

/-- The (x,z) pair, constructed by the *actual* categorical
pullback universal property. -/
noncomputable def stoneanCechTripleXZ
    (T : Profinite.{u}) :
    stoneanPresentationCechTriples T ⟶
      stoneanPresentationCechPairs T := by
  let p := Profinite.presentation.π T
  refine pullback.lift
    (stoneanCechTripleXY T ≫ pullback.fst p p)
    (stoneanCechTripleZ T) ?_
  simpa only [Category.assoc] using
    (pullback.condition :
      stoneanCechTripleXY T ≫ (pullback.fst p p ≫ p) =
        stoneanCechTripleZ T ≫ p)

/-- The (y,z) pair, using the x/y pair relation to construct the
third pullback map. -/
noncomputable def stoneanCechTripleYZ
    (T : Profinite.{u}) :
    stoneanPresentationCechTriples T ⟶
      stoneanPresentationCechPairs T := by
  let p := Profinite.presentation.π T
  refine pullback.lift
    (stoneanCechTripleXY T ≫ pullback.snd p p)
    (stoneanCechTripleZ T) ?_
  calc
    (stoneanCechTripleXY T ≫ pullback.snd p p) ≫ p =
        stoneanCechTripleXY T ≫ (pullback.snd p p ≫ p) :=
      Category.assoc _ _ _
    _ = stoneanCechTripleXY T ≫ (pullback.fst p p ≫ p) := by
      rw [← pullback.condition]
    _ = stoneanCechTripleZ T ≫ p :=
      pullback.condition

/-- Free-module alternating difference on the genuine triple relation:
x-z = (x-y) + (y-z). -/
theorem stoneanCechDifference_triple
    (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).map (stoneanCechTripleXZ T) ≫
        stoneanCechDifference T =
      ((Condensed.profiniteFree Coeff).map (stoneanCechTripleXY T) ≫
        stoneanCechDifference T) +
      ((Condensed.profiniteFree Coeff).map (stoneanCechTripleYZ T) ≫
        stoneanCechDifference T) := by
  unfold stoneanCechDifference
  simp only [Preadditive.comp_sub, ← Functor.map_comp,
    stoneanCechTripleXZ, stoneanCechTripleYZ,
    pullback.lift_fst, pullback.lift_snd]
  abel

/-- The relation's genuine morphism into the Stonean kernel satisfies
the same triple relation: the kernel inclusion is monic and no
chosen scalar coefficient model is needed. -/
theorem stoneanCechRelationToKernel_triple
    (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).map (stoneanCechTripleXZ T) ≫
        stoneanCechRelationToKernel T =
      ((Condensed.profiniteFree Coeff).map (stoneanCechTripleXY T) ≫
        stoneanCechRelationToKernel T) +
      ((Condensed.profiniteFree Coeff).map (stoneanCechTripleYZ T) ≫
        stoneanCechRelationToKernel T) := by
  apply (cancel_mono (kernel.ι (freeStoneanPresentationMap T))).1
  simpa only [Category.assoc, Preadditive.add_comp,
    stoneanCechRelationToKernel_comp_ι] using
      stoneanCechDifference_triple T

/-- **Kernel-induced categorical cocycle law.**
For any ambient condensed-module target A and actual kernel map
f : K_T → A, its genuine Čech relation functional satisfies
c(x,z) = c(x,y) + c(y,z) as morphisms on the honest triple object. -/
theorem stoneanCechKernelCochain_triple
    (T : Profinite.{u}) (A : Ambient)
    (f : stoneanPresentationKernel T ⟶ A) :
    (Condensed.profiniteFree Coeff).map (stoneanCechTripleXZ T) ≫
        (stoneanCechRelationToKernel T ≫ f) =
      ((Condensed.profiniteFree Coeff).map (stoneanCechTripleXY T) ≫
        (stoneanCechRelationToKernel T ≫ f)) +
      ((Condensed.profiniteFree Coeff).map (stoneanCechTripleYZ T) ≫
        (stoneanCechRelationToKernel T ≫ f)) := by
  have h := congrArg
    (fun k : ((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechTriples T)) ⟶
          stoneanPresentationKernel T => k ≫ f)
    (stoneanCechRelationToKernel_triple T)
  simpa only [Category.assoc, Preadditive.add_comp] using h

#print axioms stoneanCechDifference_triple
#print axioms stoneanCechRelationToKernel_triple
#print axioms stoneanCechKernelCochain_triple

end CMDG.CondensedCM5R0
