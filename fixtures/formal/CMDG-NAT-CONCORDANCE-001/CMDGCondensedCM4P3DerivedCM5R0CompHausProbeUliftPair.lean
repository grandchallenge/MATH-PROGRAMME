import CMDGCondensedCM4P3DerivedCM5R0SplitFreeCechDegreeOne
import CMDGCondensedCM4P3DerivedCM5R0CompHausCechPullbackComparison

/-!
# CMDG CM5 — genuine site-level Čech pair versus the split free-set pair

Previous protected results show that for a Stonean probe U the real
CompHaus Hom set of R=P(T)×_T P(T) is a fiber product of Hom sets.
The genuine condensed-set representable presheaf at U uses the
UNIVERSE LIFT of those Hom sets. To compare its free-module
pair degree with the explicitly contracted free-set complex,
the lift must commute with the fiber product without replacing
the pair object by a surrogate.

This module proves that equivalence for ANY pair of set maps,
specializes it to the actual Stonean presentation, and checks
the two endpoint projections. It also maps the resulting
equivalence through the actual ModuleCat.free Coeff functor,
providing the true degree-one free-module comparison iso.

The corresponding degree-two triple and all three face-map
comparisons remain separate obligations. No unconditional
global Čech epi, Ext² vanishing, or solidity claimed.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Universe lifting commutes with *actual* compatible pairs,
for any two functions with the same target. -/
def uliftCompatiblePairEquiv {A B C : Type u}
    (f : A → C) (g : B → C) :
    ULift.{u + 1} {ab : A × B // f ab.1 = g ab.2} ≃
      {ab : ULift.{u + 1} A × ULift.{u + 1} B //
        ULift.up (f ab.1.down) = ULift.up (g ab.2.down)} where
  toFun z :=
    ⟨(ULift.up z.down.1.1, ULift.up z.down.1.2),
      congrArg ULift.up z.down.2⟩
  invFun ab :=
    ULift.up ⟨(ab.1.1.down, ab.1.2.down),
      congrArg ULift.down ab.2⟩
  left_inv := by
    rintro ⟨⟨⟨a, b⟩, hab⟩⟩
    rfl
  right_inv := by
    intro ab
    apply Subtype.ext
    apply Prod.ext
    · change ULift.up ab.1.1.down = ab.1.1
      exact ULift.up_down ab.1.1
    · change ULift.up ab.1.2.down = ab.1.2
      exact ULift.up_down ab.1.2

/-- Pair degree of the *actual* universe-lifted CompHaus
representable, identified with the compatible pairs of the
exact evaluated Stonean presentation morphism. -/
noncomputable def stoneanCompHausProbeCechPairUliftEquiv
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1}
        (U.compHaus ⟶ profiniteToCompHaus.obj
          (stoneanPresentationCechPairs T)) ≃
      splitFreeCechPair (stoneanCompHausProbePresentationMap T U) := by
  let p := Profinite.presentation.π T
  let A := U.compHaus ⟶ profiniteToCompHaus.obj
    (Stonean.toProfinite.obj T.presentation)
  let B := U.compHaus ⟶ profiniteToCompHaus.obj T
  let f : A → B := fun x => x ≫ profiniteToCompHaus.map p
  let e := stoneanCompHausProbeCechPairEquiv T U
  change ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechPairs T)) ≃
    {ab : ULift.{u + 1} A × ULift.{u + 1} A //
      ULift.up (f ab.1.down) = ULift.up (f ab.2.down)}
  exact
    (Equiv.ulift.trans e).trans
      (Equiv.ulift.symm.trans (uliftCompatiblePairEquiv f f))

/-- Comparison preserves x, the first *genuine* profinite
Čech pair endpoint, even after universe lift. -/
theorem stoneanCompHausProbeCechPairUlift_fst
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechPairs T))) :
    (stoneanCompHausProbeCechPairUliftEquiv T U z).1.1 =
      ULift.up (z.down ≫ profiniteToCompHaus.map
        (pullback.fst (Profinite.presentation.π T)
          (Profinite.presentation.π T))) := by
  rfl

/-- Comparison preserves y, the second genuine Čech pair endpoint. -/
theorem stoneanCompHausProbeCechPairUlift_snd
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechPairs T))) :
    (stoneanCompHausProbeCechPairUliftEquiv T U z).1.2 =
      ULift.up (z.down ≫ profiniteToCompHaus.map
        (pullback.snd (Profinite.presentation.π T)
          (Profinite.presentation.π T))) := by
  rfl

/-- The degree-one comparison lifts further to the *actual*
free coefficient modules, with the genuine universe level. -/
noncomputable def stoneanCompHausProbeFreePairIso
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
        (ULift.{u + 1}
          (U.compHaus ⟶ profiniteToCompHaus.obj
            (stoneanPresentationCechPairs T))) ≅
      (ModuleCat.free Coeff).obj
        (splitFreeCechPair (stoneanCompHausProbePresentationMap T U)) :=
  (ModuleCat.free Coeff).mapIso
    (stoneanCompHausProbeCechPairUliftEquiv T U).toIso

#check uliftCompatiblePairEquiv
#check stoneanCompHausProbeCechPairUliftEquiv
#check stoneanCompHausProbeFreePairIso

#print axioms uliftCompatiblePairEquiv
#print axioms stoneanCompHausProbeCechPairUlift_fst
#print axioms stoneanCompHausProbeCechPairUlift_snd
#print axioms stoneanCompHausProbeFreePairIso

end CMDG.CondensedCM5R0
