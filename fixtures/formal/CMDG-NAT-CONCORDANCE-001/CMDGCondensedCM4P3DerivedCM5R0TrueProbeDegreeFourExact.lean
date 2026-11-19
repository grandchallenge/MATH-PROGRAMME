import CMDGCondensedCM4P3DerivedCM5R0SextupleFaceProbeComparison
import CMDGCondensedCM4P3DerivedCM5R0ProbeDegreeThreeExact
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

/-!
# CMDG CM5 — true represented sixth Čech degree-four exactness

The actual categorical sixth/fifth Profinite Čech fibre objects
are compared under every Stonean representable U to split free
Čech modules, with all six real deletion faces. Exactness
uses the section-appending contracting homotopy.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

noncomputable def stoneanCompHausProbeFreeSextupleIso
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T))) ≅
    (ModuleCat.free Coeff).obj
      (splitFreeCechSextuple (stoneanCompHausProbePresentationMap T U)) :=
  (ModuleCat.free Coeff).mapIso
    (stoneanCompHausProbeCechSextupleUliftEquiv T U).toIso

noncomputable def trueProbeSextFace0
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechSextuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T))

theorem trueProbeSextFace0_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeSextFace0 T U) ≫
      (stoneanCompHausProbeFreeQuintupleIso T U).hom =
    (stoneanCompHausProbeFreeSextupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechSextFace0
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeSextFace0 T U)
    (splitFreeCechSextFace0 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechSextupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechSextupleUlift_face0 T U z).symm)

noncomputable def trueProbeSextFace1
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechSextuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T))

theorem trueProbeSextFace1_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeSextFace1 T U) ≫
      (stoneanCompHausProbeFreeQuintupleIso T U).hom =
    (stoneanCompHausProbeFreeSextupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechSextFace1
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeSextFace1 T U)
    (splitFreeCechSextFace1 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechSextupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechSextupleUlift_face1 T U z).symm)

noncomputable def trueProbeSextFace2
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechSextuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T))

theorem trueProbeSextFace2_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeSextFace2 T U) ≫
      (stoneanCompHausProbeFreeQuintupleIso T U).hom =
    (stoneanCompHausProbeFreeSextupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechSextFace2
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeSextFace2 T U)
    (splitFreeCechSextFace2 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechSextupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechSextupleUlift_face2 T U z).symm)

noncomputable def trueProbeSextFace3
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechSextuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T))

theorem trueProbeSextFace3_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeSextFace3 T U) ≫
      (stoneanCompHausProbeFreeQuintupleIso T U).hom =
    (stoneanCompHausProbeFreeSextupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechSextFace3
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeSextFace3 T U)
    (splitFreeCechSextFace3 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechSextupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechSextupleUlift_face3 T U z).symm)

noncomputable def trueProbeSextFace4
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechSextuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T))

theorem trueProbeSextFace4_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeSextFace4 T U) ≫
      (stoneanCompHausProbeFreeQuintupleIso T U).hom =
    (stoneanCompHausProbeFreeSextupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechSextFace4
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeSextFace4 T U)
    (splitFreeCechSextFace4 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechSextupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechSextupleUlift_face4 T U z).symm)

noncomputable def trueProbeSextFace5
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechSextuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (pullback.fst
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)))

theorem trueProbeSextFace5_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeSextFace5 T U) ≫
      (stoneanCompHausProbeFreeQuintupleIso T U).hom =
    (stoneanCompHausProbeFreeSextupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechSextFace5
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeSextFace5 T U)
    (splitFreeCechSextFace5 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechSextupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechSextupleUlift_face5 T U z).symm)

noncomputable def trueProbeD5 (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T))) ⟶
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T))) :=
  (ModuleCat.free Coeff).map (↾trueProbeSextFace0 T U)
  - (ModuleCat.free Coeff).map (↾trueProbeSextFace1 T U)
  + (ModuleCat.free Coeff).map (↾trueProbeSextFace2 T U)
  - (ModuleCat.free Coeff).map (↾trueProbeSextFace3 T U)
  + (ModuleCat.free Coeff).map (↾trueProbeSextFace4 T U)
  - (ModuleCat.free Coeff).map (↾trueProbeSextFace5 T U)

theorem trueProbeD5_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeD5 T U ≫ (stoneanCompHausProbeFreeQuintupleIso T U).hom =
    (stoneanCompHausProbeFreeSextupleIso T U).hom ≫
      splitFreeCechD5 (stoneanCompHausProbePresentationMap T U) := by
  unfold trueProbeD5 splitFreeCechD5
  simp only [Preadditive.sub_comp, Preadditive.add_comp,
    Preadditive.comp_sub, Preadditive.comp_add]
  rw [trueProbeSextFace0_free_square,
    trueProbeSextFace1_free_square,
    trueProbeSextFace2_free_square,
    trueProbeSextFace3_free_square,
    trueProbeSextFace4_free_square,
    trueProbeSextFace5_free_square]


theorem trueProbeD5_comp_D4_zero
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeD5 T U ≫ trueProbeD4 T U = 0 := by
  apply (cancel_mono (stoneanCompHausProbeFreeQuadrupleIso T U).hom).1
  calc
    (trueProbeD5 T U ≫ trueProbeD4 T U) ≫
        (stoneanCompHausProbeFreeQuadrupleIso T U).hom =
      trueProbeD5 T U ≫
        (trueProbeD4 T U ≫
          (stoneanCompHausProbeFreeQuadrupleIso T U).hom) := Category.assoc _ _ _
    _ = trueProbeD5 T U ≫
        ((stoneanCompHausProbeFreeQuintupleIso T U).hom ≫
          splitFreeCechD4 (stoneanCompHausProbePresentationMap T U)) := by
            rw [trueProbeD4_free_square]
    _ = (trueProbeD5 T U ≫
        (stoneanCompHausProbeFreeQuintupleIso T U).hom) ≫
          splitFreeCechD4 (stoneanCompHausProbePresentationMap T U) :=
            (Category.assoc _ _ _).symm
    _ = ((stoneanCompHausProbeFreeSextupleIso T U).hom ≫
          splitFreeCechD5 (stoneanCompHausProbePresentationMap T U)) ≫
          splitFreeCechD4 (stoneanCompHausProbePresentationMap T U) := by
            rw [trueProbeD5_free_square]
    _ = 0 := by
      rw [Category.assoc, splitFreeCechD5_comp_D4_zero, comp_zero]

noncomputable def trueProbeDegreeFourComplex
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (trueProbeD5 T U) (trueProbeD4 T U)
    (trueProbeD5_comp_D4_zero T U)

noncomputable def trueProbeDegreeFourIsoSplit
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeDegreeFourComplex T U ≅
      splitFreeCechDegreeFourComplex
        (stoneanCompHausProbePresentationMap T U) := by
  refine ShortComplex.isoMk
    (stoneanCompHausProbeFreeSextupleIso T U)
    (stoneanCompHausProbeFreeQuintupleIso T U)
    (stoneanCompHausProbeFreeQuadrupleIso T U) ?_ ?_
  · exact (trueProbeD5_free_square T U).symm
  · simpa [trueProbeDegreeFourComplex,
      splitFreeCechDegreeFourComplex] using
        (trueProbeD4_free_square T U).symm

/-- Exactness at degree four on the ACTUAL categorical sixfold
and fivefold Profinite Čech representables, for every Stonean U. -/
theorem trueProbeDegreeFour_exact
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (trueProbeDegreeFourComplex T U).Exact := by
  let p := stoneanCompHausProbePresentationMap T U
  let sect := (stoneanCompHausProbePresentationSplitEpi T U).section_
  have hs : ∀ y, p (sect y) = y := by
    intro y
    have h := (stoneanCompHausProbePresentationSplitEpi T U).id
    have hh := congrArg (fun f => f y) h
    exact hh
  exact ShortComplex.exact_of_iso
    (trueProbeDegreeFourIsoSplit T U).symm
    (splitFreeCechDegreeFour_exact p sect hs)

#print axioms trueProbeD5_comp_D4_zero
#print axioms trueProbeDegreeFour_exact
#print axioms trueProbeD5_free_square
end CMDG.CondensedCM5R0
