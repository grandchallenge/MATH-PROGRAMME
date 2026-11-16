import CMDGCondensedCM4P3DerivedCM5R0StoneanLocalCechHomotopy
import Mathlib.Condensed.Epi
import Mathlib.AlgebraicTopology.ExtraDegeneracy

/-!
# CMDG CM5 — Stonean-probe Čech homotopy and exact global-epi test

For every profinite T and Stonean U, projectivity supplies a **function**
assigning a continuous lift U → P(T) to every continuous q : U → T.
Thus the actual map of hom SETS
  Hom(U,P(T)) → Hom(U,T)
has a section, even though P(T) → T need not split in Profinite.

This file builds that genuine function, its split-epimorphism structure
in Type, and its full augmented Čech-nerve contraction after applying the
free-module functor ModuleCat.free. The hom SETS used here are exactly the
representable probes of the Stonean presentation; a categorical comparison
to the original pair fiber product is also proved.

IMPORTANT: free modules on the hom sets are NOT silently identified with
evaluations of free CONDENSED modules. Sheafification can contribute
clopen-locally defined sections. Mathlib's true CondensedMod epimorphism
criterion reduces the missing global proof to surjectivity of the ACTUAL
sheaf-valued map on every Stonean probe. That comparison remains open.
The all-degree hom-set contraction is genuine, but does NOT establish
Ext^2 vanishing or global Čech exactness.
-/

noncomputable section

universe u

open CategoryTheory Limits Opposite

namespace CMDG.CondensedCM5R0

/-- The genuine map on Stonean-probe hom SETS induced by the canonical
Stonean presentation. Lift universe to match the pinned ModuleCat.free. -/
noncomputable def stoneanProbePresentationMap
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (Stonean.toProfinite.obj U ⟶
      Stonean.toProfinite.obj T.presentation) ⟶
    ULift.{u + 1} (Stonean.toProfinite.obj U ⟶ T) :=
  ↾fun z => ULift.up (z.down ≫ Profinite.presentation.π T)

/-- A Stonean test object provides an explicit section of the induced
map on Hom sets; this does NOT imply P(T) → T has a global section. -/
noncomputable def stoneanProbePresentationSplitEpi
    (T : Profinite.{u}) (U : Stonean.{u}) :
    SplitEpi (stoneanProbePresentationMap T U) := by
  let p := Profinite.presentation.π T
  refine {
    section_ := ↾fun z => ULift.up (Profinite.lift z.down p)
    id := ?_
  }
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro z
  rcases z with ⟨q⟩
  exact congrArg ULift.up (Profinite.lift_lifts q p)

/-- The ordinary SET-valued augmented Čech nerve of the *actual
Stonean-probe hom-map*, with the correct universe-lifted Hom sets. -/
noncomputable def stoneanProbePresentationCechNerve
    (T : Profinite.{u}) (U : Stonean.{u}) :=
  (Arrow.mk (stoneanProbePresentationMap T U)).augmentedCechNerve

/-- All-dimensional contracting extra degeneracy of the genuine
Stonean-probe Čech nerve. -/
noncomputable def stoneanProbePresentationExtraDegeneracy
    (T : Profinite.{u}) (U : Stonean.{u}) :=
  Arrow.AugmentedCechNerve.extraDegeneracy
    (Arrow.mk (stoneanProbePresentationMap T U))
    (stoneanProbePresentationSplitEpi T U)

/-- The same contraction after applying the actual functor taking
a set to its free ULift ℤ-module. -/
noncomputable def stoneanProbeFreeExtraDegeneracy
    (T : Profinite.{u}) (U : Stonean.{u}) :=
  (stoneanProbePresentationExtraDegeneracy T U).map
    (ModuleCat.free Coeff)

/-- Exact all-degree chain-homotopy equivalence for the Stonean-probe
bar complex of *free modules on the Hom sets*. -/
noncomputable def stoneanProbeFreeCechHomotopyEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :=
  (stoneanProbeFreeExtraDegeneracy T U).homotopyEquiv

/-- The actual original Čech pair space represents the set-theoretic
kernel pair of the Stonean-probe Hom map. No hypothetical relation
space or axiom of descent enters this comparison. -/
noncomputable def stoneanProbeCechPairEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (Stonean.toProfinite.obj U ⟶
      stoneanPresentationCechPairs T) ≃
      { xy : (Stonean.toProfinite.obj U ⟶
          Stonean.toProfinite.obj T.presentation) ×
          (Stonean.toProfinite.obj U ⟶
          Stonean.toProfinite.obj T.presentation) //
        xy.1 ≫ Profinite.presentation.π T =
        xy.2 ≫ Profinite.presentation.π T } where
  toFun z :=
    ⟨⟨z ≫ pullback.fst _ _, z ≫ pullback.snd _ _⟩, by
      simp only [Category.assoc]
      exact congrArg (fun a => z ≫ a)
        (pullback.condition :
          pullback.fst (Profinite.presentation.π T)
              (Profinite.presentation.π T) ≫
              Profinite.presentation.π T =
          pullback.snd (Profinite.presentation.π T)
              (Profinite.presentation.π T) ≫
              Profinite.presentation.π T)⟩
  invFun xy := pullback.lift xy.1.1 xy.1.2 xy.2
  left_inv z := by
    apply pullback.hom_ext
    · exact pullback.lift_fst _ _ _
    · exact pullback.lift_snd _ _ _
  right_inv xy := by
    apply Subtype.ext
    apply Prod.ext
    · exact pullback.lift_fst _ _ _
    · exact pullback.lift_snd _ _ _

/-- The **exact** remaining global second-relation obligation, expressed
in the pinned Mathlib Stonean evaluation criterion for actual condensed
modules, not in the non-sheafified free-module bar complex above. -/
theorem stoneanCechTripleToSecondRelation_epi_iff_stonean_surjective
    (T : Profinite.{u}) :
    Epi (stoneanCechTripleToSecondRelation T) ↔
      ∀ U : Stonean.{u},
        Function.Surjective
          ((stoneanCechTripleToSecondRelation T).hom.app
            (op U.compHaus)) := by
  exact CondensedMod.epi_iff_surjective_on_stonean Coeff
    (stoneanCechTripleToSecondRelation T)

#check stoneanProbePresentationSplitEpi
#check stoneanProbePresentationCechNerve
#check stoneanProbeFreeCechHomotopyEquiv
#check stoneanProbeCechPairEquiv
#check stoneanCechTripleToSecondRelation_epi_iff_stonean_surjective

#print axioms stoneanProbePresentationSplitEpi
#print axioms stoneanProbePresentationExtraDegeneracy
#print axioms stoneanProbeFreeExtraDegeneracy
#print axioms stoneanProbeFreeCechHomotopyEquiv
#print axioms stoneanProbeCechPairEquiv
#print axioms stoneanCechTripleToSecondRelation_epi_iff_stonean_surjective

end CMDG.CondensedCM5R0
