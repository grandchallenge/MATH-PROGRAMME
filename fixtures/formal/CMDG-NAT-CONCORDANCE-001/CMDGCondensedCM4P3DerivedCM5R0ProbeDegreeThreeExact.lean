import CMDGCondensedCM4P3DerivedCM5R0QuintupleProbeComparison
import CMDGCondensedCM4P3DerivedCM5R0ProbeDegreeTwoExact

/-!
# CM5: true represented fifth Čech degree-three exactness

For all profinite T and Stonean U, compare the actual represented
fivefold and fourfold Čech free modules with the compatible split-set
fivefold and fourfold modules, preserving ALL five faces. Transfer
the section-contracted split-degree-three exactness at every Stonean
probe. Sheafification and global epi remain different obligations.
-/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

noncomputable def stoneanCompHausProbeFreeQuintupleIso
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T))) ≅
    (ModuleCat.free Coeff).obj
      (splitFreeCechQuintuple (stoneanCompHausProbePresentationMap T U)) :=
  (ModuleCat.free Coeff).mapIso
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U).toIso


noncomputable def trueProbeQuintFace0
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace0 T))

theorem trueProbeQuintFace0_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeQuintFace0 T U) ≫
      (stoneanCompHausProbeFreeQuadrupleIso T U).hom =
    (stoneanCompHausProbeFreeQuintupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechQuintFace0
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeQuintFace0 T U)
    (splitFreeCechQuintFace0 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechQuintupleUlift_face0 T U z).symm)

noncomputable def trueProbeQuintFace1
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace1 T))

theorem trueProbeQuintFace1_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeQuintFace1 T U) ≫
      (stoneanCompHausProbeFreeQuadrupleIso T U).hom =
    (stoneanCompHausProbeFreeQuintupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechQuintFace1
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeQuintFace1 T U)
    (splitFreeCechQuintFace1 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechQuintupleUlift_face1 T U z).symm)

noncomputable def trueProbeQuintFace2
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace2 T))

theorem trueProbeQuintFace2_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeQuintFace2 T U) ≫
      (stoneanCompHausProbeFreeQuadrupleIso T U).hom =
    (stoneanCompHausProbeFreeQuintupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechQuintFace2
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeQuintFace2 T U)
    (splitFreeCechQuintFace2 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechQuintupleUlift_face2 T U z).symm)

noncomputable def trueProbeQuintFace3
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace3 T))

theorem trueProbeQuintFace3_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeQuintFace3 T U) ≫
      (stoneanCompHausProbeFreeQuadrupleIso T U).hom =
    (stoneanCompHausProbeFreeQuintupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechQuintFace3
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeQuintFace3 T U)
    (splitFreeCechQuintFace3 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechQuintupleUlift_face3 T U z).symm)

noncomputable def trueProbeQuintFace4
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuadruples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace4 T))

theorem trueProbeQuintFace4_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeQuintFace4 T U) ≫
      (stoneanCompHausProbeFreeQuadrupleIso T U).hom =
    (stoneanCompHausProbeFreeQuintupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechQuintFace4
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeQuintFace4 T U)
    (splitFreeCechQuintFace4 (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U)
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechQuintupleUlift_face4 T U z).symm)

noncomputable def trueProbeD4 (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T))) ⟶
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T))) :=
  (ModuleCat.free Coeff).map (↾trueProbeQuintFace0 T U) -
    (ModuleCat.free Coeff).map (↾trueProbeQuintFace1 T U) +
    (ModuleCat.free Coeff).map (↾trueProbeQuintFace2 T U) -
    (ModuleCat.free Coeff).map (↾trueProbeQuintFace3 T U) +
    (ModuleCat.free Coeff).map (↾trueProbeQuintFace4 T U)

theorem trueProbeD4_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeD4 T U ≫ (stoneanCompHausProbeFreeQuadrupleIso T U).hom =
    (stoneanCompHausProbeFreeQuintupleIso T U).hom ≫
      splitFreeCechD4 (stoneanCompHausProbePresentationMap T U) := by
  unfold trueProbeD4 splitFreeCechD4
  simp only [Preadditive.sub_comp, Preadditive.add_comp,
    Preadditive.comp_sub, Preadditive.comp_add]
  rw [trueProbeQuintFace0_free_square,
    trueProbeQuintFace1_free_square,
    trueProbeQuintFace2_free_square,
    trueProbeQuintFace3_free_square,
    trueProbeQuintFace4_free_square]

theorem trueProbeD4_comp_D3_zero
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeD4 T U ≫ trueProbeD3 T U = 0 := by
  apply (cancel_mono (stoneanCompHausProbeFreeTripleIso T U).hom).1
  calc
    (trueProbeD4 T U ≫ trueProbeD3 T U) ≫
        (stoneanCompHausProbeFreeTripleIso T U).hom =
      trueProbeD4 T U ≫
        (trueProbeD3 T U ≫
          (stoneanCompHausProbeFreeTripleIso T U).hom) := Category.assoc _ _ _
    _ = trueProbeD4 T U ≫
        ((stoneanCompHausProbeFreeQuadrupleIso T U).hom ≫
          splitFreeCechD3 (stoneanCompHausProbePresentationMap T U)) := by
            rw [trueProbeD3_free_square]
    _ = (trueProbeD4 T U ≫
        (stoneanCompHausProbeFreeQuadrupleIso T U).hom) ≫
          splitFreeCechD3 (stoneanCompHausProbePresentationMap T U) :=
            (Category.assoc _ _ _).symm
    _ = ((stoneanCompHausProbeFreeQuintupleIso T U).hom ≫
          splitFreeCechD4 (stoneanCompHausProbePresentationMap T U)) ≫
          splitFreeCechD3 (stoneanCompHausProbePresentationMap T U) := by
            rw [trueProbeD4_free_square]
    _ = 0 := by
      rw [Category.assoc, splitFreeCechD4_comp_D3_zero, comp_zero]

noncomputable def trueProbeDegreeThreeComplex
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (trueProbeD4 T U) (trueProbeD3 T U)
    (trueProbeD4_comp_D3_zero T U)

noncomputable def trueProbeDegreeThreeIsoSplit
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeDegreeThreeComplex T U ≅
      splitFreeCechDegreeThreeComplex
        (stoneanCompHausProbePresentationMap T U) := by
  refine ShortComplex.isoMk
    (stoneanCompHausProbeFreeQuintupleIso T U)
    (stoneanCompHausProbeFreeQuadrupleIso T U)
    (stoneanCompHausProbeFreeTripleIso T U) ?_ ?_
  · exact (trueProbeD4_free_square T U).symm
  · simpa [trueProbeDegreeThreeComplex,
      splitFreeCechDegreeThreeComplex] using
        (trueProbeD3_free_square T U).symm

theorem trueProbeDegreeThree_exact
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (trueProbeDegreeThreeComplex T U).Exact := by
  let p := stoneanCompHausProbePresentationMap T U
  let s := (stoneanCompHausProbePresentationSplitEpi T U).section_
  have hs : ∀ y, p (s y) = y := by
    intro y
    have h := (stoneanCompHausProbePresentationSplitEpi T U).id
    have hh := congrArg (fun f => f y) h
    exact hh
  exact ShortComplex.exact_of_iso
    (trueProbeDegreeThreeIsoSplit T U).symm
    (splitFreeCechDegreeThree_exact p s hs)

#print axioms trueProbeD4_free_square
#print axioms trueProbeD4_comp_D3_zero
#print axioms trueProbeDegreeThree_exact
end CMDG.CondensedCM5R0
