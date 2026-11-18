import CMDGCondensedCM4P3DerivedCM5R0CompHausProbeActualTriple
import Mathlib.CategoryTheory.Preadditive.AdditiveFunctor

/-!
# CMDG CM5 — genuine Stonean-probe Čech short-complex exactness

At every Stonean probe U, use the **actual** represented CompHaus Čech pair
and triple of the canonical presentation P(T) → T, not a surrogate simplicial
object. The previously proved ULift comparison induces isomorphisms of the
free Coeff-modules in degrees two and one. We verify the three genuine face
maps and both pair endpoints at the level of ModuleCat, with explicit signs,
and construct a short-complex isomorphism to the split-set free Čech complex.
Stonean projectivity supplies a section *on U-points*, so the split complex
is exact and the actual represented short complex is exact.

This theorem establishes **objectwise exactness at each Stonean test U**.
The remaining global step is categorical identification with the restricted
CompHaus free-module presheaf short complex, naturality in U, and exact
sheafification/CondensedMod transfer. No global Ext², full derived solidity,
or MATHCERT certification is inferred from this module.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Lift a commutative square of set functions to the actual free modules. -/
theorem freeMap_square_of_equivs {A B C D : Type (u + 1)}
    (f : A → B) (g : C → D) (e : A ≃ C) (k : B ≃ D)
    (h : ∀ a, k (f a) = g (e a)) :
    (ModuleCat.free Coeff).map (↾f) ≫ (ModuleCat.free Coeff).map (↾k) =
      (ModuleCat.free Coeff).map (↾e) ≫ (ModuleCat.free Coeff).map (↾g) := by
  have hFunctions : (↾f : A ⟶ B) ≫ (↾k) = (↾e) ≫ (↾g) := by
    ext a
    exact h a
  calc
    (ModuleCat.free Coeff).map (↾f) ≫ (ModuleCat.free Coeff).map (↾k) =
      (ModuleCat.free Coeff).map ((↾f) ≫ (↾k)) := (Functor.map_comp _ _ _).symm
    _ = (ModuleCat.free Coeff).map ((↾e) ≫ (↾g)) := congrArg _ hFunctions
    _ = (ModuleCat.free Coeff).map (↾e) ≫ (ModuleCat.free Coeff).map (↾g) :=
      Functor.map_comp _ _ _

/-- Real represented CompHaus-site XY face on the correct universe-lifted Hom sets. -/
noncomputable def trueProbeTripleXY
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechTriples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechPairs T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map (stoneanCechTripleXY T))

/-- Actual and split free-module XY faces commute with genuine comparisons. -/
theorem trueProbeTripleXY_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeTripleXY T U) ≫
      (stoneanCompHausProbeFreePairIso T U).hom =
    (stoneanCompHausProbeFreeTripleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechTripleXY
        (stoneanCompHausProbePresentationMap T U)) := by
  change (ModuleCat.free Coeff).map (↾trueProbeTripleXY T U) ≫
    (ModuleCat.free Coeff).map (↾stoneanCompHausProbeCechPairUliftEquiv T U) =
    (ModuleCat.free Coeff).map (↾stoneanCompHausProbeCechTripleUliftEquiv T U) ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechTripleXY
        (stoneanCompHausProbePresentationMap T U))
  exact freeMap_square_of_equivs
    (trueProbeTripleXY T U)
    (splitFreeCechTripleXY (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechTripleUliftEquiv T U)
    (stoneanCompHausProbeCechPairUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechTripleUlift_xy T U z).symm)

/-- Real represented CompHaus-site XZ face on the correct universe-lifted Hom sets. -/
noncomputable def trueProbeTripleXZ
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechTriples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechPairs T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map (stoneanCechTripleXZ T))

/-- Actual and split free-module XZ faces commute with genuine comparisons. -/
theorem trueProbeTripleXZ_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeTripleXZ T U) ≫
      (stoneanCompHausProbeFreePairIso T U).hom =
    (stoneanCompHausProbeFreeTripleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechTripleXZ
        (stoneanCompHausProbePresentationMap T U)) := by
  change (ModuleCat.free Coeff).map (↾trueProbeTripleXZ T U) ≫
    (ModuleCat.free Coeff).map (↾stoneanCompHausProbeCechPairUliftEquiv T U) =
    (ModuleCat.free Coeff).map (↾stoneanCompHausProbeCechTripleUliftEquiv T U) ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechTripleXZ
        (stoneanCompHausProbePresentationMap T U))
  exact freeMap_square_of_equivs
    (trueProbeTripleXZ T U)
    (splitFreeCechTripleXZ (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechTripleUliftEquiv T U)
    (stoneanCompHausProbeCechPairUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechTripleUlift_xz T U z).symm)

/-- Real represented CompHaus-site YZ face on the correct universe-lifted Hom sets. -/
noncomputable def trueProbeTripleYZ
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechTriples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechPairs T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map (stoneanCechTripleYZ T))

/-- Actual and split free-module YZ faces commute with genuine comparisons. -/
theorem trueProbeTripleYZ_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeTripleYZ T U) ≫
      (stoneanCompHausProbeFreePairIso T U).hom =
    (stoneanCompHausProbeFreeTripleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechTripleYZ
        (stoneanCompHausProbePresentationMap T U)) := by
  change (ModuleCat.free Coeff).map (↾trueProbeTripleYZ T U) ≫
    (ModuleCat.free Coeff).map (↾stoneanCompHausProbeCechPairUliftEquiv T U) =
    (ModuleCat.free Coeff).map (↾stoneanCompHausProbeCechTripleUliftEquiv T U) ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechTripleYZ
        (stoneanCompHausProbePresentationMap T U))
  exact freeMap_square_of_equivs
    (trueProbeTripleYZ T U)
    (splitFreeCechTripleYZ (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechTripleUliftEquiv T U)
    (stoneanCompHausProbeCechPairUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechTripleUlift_yz T U z).symm)


/-- Actual first endpoint of the genuine Čech pair represented at U. -/
noncomputable def trueProbePairFst
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechPairs T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (Stonean.toProfinite.obj T.presentation)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (pullback.fst (Profinite.presentation.π T)
      (Profinite.presentation.π T)))

/-- Actual second endpoint of the genuine Čech pair represented at U. -/
noncomputable def trueProbePairSnd
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechPairs T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (Stonean.toProfinite.obj T.presentation)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (pullback.snd (Profinite.presentation.π T)
      (Profinite.presentation.π T)))

theorem trueProbePairFst_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbePairFst T U) =
      (stoneanCompHausProbeFreePairIso T U).hom ≫
        (ModuleCat.free Coeff).map (↾splitFreeCechPairFst
          (stoneanCompHausProbePresentationMap T U)) := by
  have heq :
      (↾trueProbePairFst T U :
        ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
          (stoneanPresentationCechPairs T)) ⟶ _) =
      (↾stoneanCompHausProbeCechPairUliftEquiv T U) ≫
        (↾splitFreeCechPairFst
          (stoneanCompHausProbePresentationMap T U)) := by
    apply ConcreteCategory.hom_ext
    intro z
    exact (stoneanCompHausProbeCechPairUlift_fst T U z).symm
  change (ModuleCat.free Coeff).map (↾trueProbePairFst T U) =
    (ModuleCat.free Coeff).map (↾stoneanCompHausProbeCechPairUliftEquiv T U) ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechPairFst
        (stoneanCompHausProbePresentationMap T U))
  rw [← Functor.map_comp]
  exact congrArg _ heq

theorem trueProbePairSnd_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbePairSnd T U) =
      (stoneanCompHausProbeFreePairIso T U).hom ≫
        (ModuleCat.free Coeff).map (↾splitFreeCechPairSnd
          (stoneanCompHausProbePresentationMap T U)) := by
  have heq :
      (↾trueProbePairSnd T U :
        ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
          (stoneanPresentationCechPairs T)) ⟶ _) =
      (↾stoneanCompHausProbeCechPairUliftEquiv T U) ≫
        (↾splitFreeCechPairSnd
          (stoneanCompHausProbePresentationMap T U)) := by
    apply ConcreteCategory.hom_ext
    intro z
    exact (stoneanCompHausProbeCechPairUlift_snd T U z).symm
  change (ModuleCat.free Coeff).map (↾trueProbePairSnd T U) =
    (ModuleCat.free Coeff).map (↾stoneanCompHausProbeCechPairUliftEquiv T U) ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechPairSnd
        (stoneanCompHausProbePresentationMap T U))
  rw [← Functor.map_comp]
  exact congrArg _ heq

/-- Actual represented d₁ with the protected x-y sign. -/
noncomputable def trueProbeD1
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechPairs T))) ⟶
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (Stonean.toProfinite.obj T.presentation))) :=
  (ModuleCat.free Coeff).map (↾trueProbePairFst T U) -
    (ModuleCat.free Coeff).map (↾trueProbePairSnd T U)

/-- Actual represented d₂ with the protected xz-xy-yz sign. -/
noncomputable def trueProbeD2
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T))) ⟶
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechPairs T))) :=
  (ModuleCat.free Coeff).map (↾trueProbeTripleXZ T U) -
    (ModuleCat.free Coeff).map (↾trueProbeTripleXY T U) -
    (ModuleCat.free Coeff).map (↾trueProbeTripleYZ T U)

theorem trueProbeD1_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeD1 T U =
      (stoneanCompHausProbeFreePairIso T U).hom ≫
        splitFreeCechD1 (stoneanCompHausProbePresentationMap T U) := by
  unfold trueProbeD1 splitFreeCechD1
  rw [trueProbePairFst_free_square, trueProbePairSnd_free_square]
  exact (Preadditive.comp_sub _ _ _).symm

theorem trueProbeD2_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeD2 T U ≫ (stoneanCompHausProbeFreePairIso T U).hom =
      (stoneanCompHausProbeFreeTripleIso T U).hom ≫
        splitFreeCechD2 (stoneanCompHausProbePresentationMap T U) := by
  unfold trueProbeD2 splitFreeCechD2
  simp only [Preadditive.sub_comp, Preadditive.comp_sub]
  rw [trueProbeTripleXZ_free_square,
    trueProbeTripleXY_free_square, trueProbeTripleYZ_free_square]

theorem trueProbeD2_comp_D1_zero
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeD2 T U ≫ trueProbeD1 T U = 0 := by
  rw [trueProbeD1_free_square, ← Category.assoc, trueProbeD2_free_square,
    Category.assoc, splitFreeCechD2_comp_D1_zero, comp_zero]

noncomputable def trueProbeDegreeOneComplex
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (trueProbeD2 T U) (trueProbeD1 T U)
    (trueProbeD2_comp_D1_zero T U)

noncomputable def trueProbeDegreeOneIsoSplit
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeDegreeOneComplex T U ≅
      splitFreeCechDegreeOneComplex
        (stoneanCompHausProbePresentationMap T U) := by
  refine ShortComplex.isoMk (stoneanCompHausProbeFreeTripleIso T U)
    (stoneanCompHausProbeFreePairIso T U) (Iso.refl _) ?_ ?_
  · exact (trueProbeD2_free_square T U).symm
  · simpa [trueProbeDegreeOneComplex, splitFreeCechDegreeOneComplex] using
        (trueProbeD1_free_square T U).symm

/-- Every Stonean probe sees exactness of the actual Čech d₂,d₁. -/
theorem trueProbeDegreeOne_exact
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (trueProbeDegreeOneComplex T U).Exact := by
  let p := stoneanCompHausProbePresentationMap T U
  let s := (stoneanCompHausProbePresentationSplitEpi T U).section_
  have hs : ∀ y, p (s y) = y := by
    intro y
    have h := (stoneanCompHausProbePresentationSplitEpi T U).id
    have := congrArg (fun f => f y) h
    exact this
  exact ShortComplex.exact_of_iso
    (trueProbeDegreeOneIsoSplit T U).symm
    (splitFreeCechDegreeOne_exact p s hs)

#print axioms trueProbeD2_free_square
#print axioms trueProbeDegreeOne_exact

#print axioms freeMap_square_of_equivs
#print axioms trueProbeTripleXY_free_square
#print axioms trueProbeTripleXZ_free_square
#print axioms trueProbeTripleYZ_free_square
#print axioms trueProbeD1_free_square
#print axioms trueProbeD2_comp_D1_zero
#print axioms trueProbeDegreeOneIsoSplit
end CMDG.CondensedCM5R0
