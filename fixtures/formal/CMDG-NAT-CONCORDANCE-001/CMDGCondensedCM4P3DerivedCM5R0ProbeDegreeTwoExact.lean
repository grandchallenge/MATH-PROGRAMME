import CMDGCondensedCM4P3DerivedCM5R0QuadrupleProbeComparison
import CMDGCondensedCM4P3DerivedCM5R0CompHausProbeTrueDegreeOneExact

/-!
# CMDG CM5 — degree-two exactness of the actual represented Čech
free-module complex at every genuine Stonean probe

For any profinite T and every Stonean U, compare the four genuine
representable CompHaus free-module face maps with the compatible
split-set quadruple complex through actual universe-correct
pullback equivalences. The full alternating d₃ square and d₂
square commute, yielding an isomorphism of short complexes.

Stonean projectivity splits P(T)(U)→T(U) on U-points. The
previously Lean-checked section-based degree-two contracting
homotopy then implies that the genuine represented free-module
complex is exact at its triple term.

This is probe-level exactness. We do NOT claim that evaluation
of sheafified free condensed modules automatically equals the
un-sheafified free module on represented Hom sets. Natural
presheaf/sheafification comparison and global exactness
F_{P(T)^4_T}→M_T remain open.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

noncomputable def stoneanCompHausProbeFreeQuadrupleIso
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T))) ≅
    (ModuleCat.free Coeff).obj
      (splitFreeCechQuadruple (stoneanCompHausProbePresentationMap T U)) :=
  (ModuleCat.free Coeff).mapIso
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U).toIso

private noncomputable abbrev quadProbeXYZ (T : Profinite.{u}) :
    stoneanPresentationCechQuadruples T ⟶
    stoneanPresentationCechTriples T :=
  pullback.fst
    (stoneanCechTripleXY T ≫
      pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T) ≫
      Profinite.presentation.π T)
    (Profinite.presentation.π T)

noncomputable def trueProbeQuadXYZ (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map (quadProbeXYZ T))

noncomputable def trueProbeQuadXYW (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map (quadFaceXYW T))

noncomputable def trueProbeQuadXZW (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map (quadFaceXZW T))

noncomputable def trueProbeQuadYZW (T : Profinite.{u}) (U : Stonean.{u}) :
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T)) →
    ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T)) :=
  fun z => ULift.up (z.down ≫ profiniteToCompHaus.map (quadFaceYZW T))

theorem trueProbeQuadXYZ_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeQuadXYZ T U) ≫
      (stoneanCompHausProbeFreeTripleIso T U).hom =
    (stoneanCompHausProbeFreeQuadrupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechQuadXYZ
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeQuadXYZ T U)
    (splitFreeCechQuadXYZ (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    (stoneanCompHausProbeCechTripleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechQuadrupleUlift_xyz T U z).symm)

theorem trueProbeQuadXYW_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeQuadXYW T U) ≫
      (stoneanCompHausProbeFreeTripleIso T U).hom =
    (stoneanCompHausProbeFreeQuadrupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechQuadXYW
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeQuadXYW T U)
    (splitFreeCechQuadXYW (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    (stoneanCompHausProbeCechTripleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechQuadrupleUlift_xyw T U z).symm)

theorem trueProbeQuadXZW_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeQuadXZW T U) ≫
      (stoneanCompHausProbeFreeTripleIso T U).hom =
    (stoneanCompHausProbeFreeQuadrupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechQuadXZW
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeQuadXZW T U)
    (splitFreeCechQuadXZW (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    (stoneanCompHausProbeCechTripleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechQuadrupleUlift_xzw T U z).symm)

theorem trueProbeQuadYZW_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).map (↾trueProbeQuadYZW T U) ≫
      (stoneanCompHausProbeFreeTripleIso T U).hom =
    (stoneanCompHausProbeFreeQuadrupleIso T U).hom ≫
      (ModuleCat.free Coeff).map (↾splitFreeCechQuadYZW
        (stoneanCompHausProbePresentationMap T U)) := by
  exact freeMap_square_of_equivs
    (trueProbeQuadYZW T U)
    (splitFreeCechQuadYZW (stoneanCompHausProbePresentationMap T U))
    (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    (stoneanCompHausProbeCechTripleUliftEquiv T U)
    (fun z => (stoneanCompHausProbeCechQuadrupleUlift_yzw T U z).symm)

noncomputable def trueProbeD3 (T : Profinite.{u}) (U : Stonean.{u}) :
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuadruples T))) ⟶
    (ModuleCat.free Coeff).obj
      (ULift.{u + 1} (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechTriples T))) :=
  (ModuleCat.free Coeff).map (↾trueProbeQuadYZW T U) -
    (ModuleCat.free Coeff).map (↾trueProbeQuadXZW T U) +
    (ModuleCat.free Coeff).map (↾trueProbeQuadXYW T U) -
    (ModuleCat.free Coeff).map (↾trueProbeQuadXYZ T U)

theorem trueProbeD3_free_square
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeD3 T U ≫ (stoneanCompHausProbeFreeTripleIso T U).hom =
    (stoneanCompHausProbeFreeQuadrupleIso T U).hom ≫
      splitFreeCechD3 (stoneanCompHausProbePresentationMap T U) := by
  unfold trueProbeD3 splitFreeCechD3
  simp only [Preadditive.sub_comp, Preadditive.add_comp,
    Preadditive.comp_sub, Preadditive.comp_add]
  rw [trueProbeQuadYZW_free_square, trueProbeQuadXZW_free_square,
    trueProbeQuadXYW_free_square, trueProbeQuadXYZ_free_square]

theorem trueProbeD3_comp_D2_zero
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeD3 T U ≫ trueProbeD2 T U = 0 := by
  apply (cancel_mono (stoneanCompHausProbeFreePairIso T U).hom).1
  calc
    (trueProbeD3 T U ≫ trueProbeD2 T U) ≫
        (stoneanCompHausProbeFreePairIso T U).hom =
      trueProbeD3 T U ≫
        (trueProbeD2 T U ≫
          (stoneanCompHausProbeFreePairIso T U).hom) := Category.assoc _ _ _
    _ = trueProbeD3 T U ≫
        ((stoneanCompHausProbeFreeTripleIso T U).hom ≫
          splitFreeCechD2 (stoneanCompHausProbePresentationMap T U)) := by
            rw [trueProbeD2_free_square]
    _ = (trueProbeD3 T U ≫
        (stoneanCompHausProbeFreeTripleIso T U).hom) ≫
          splitFreeCechD2 (stoneanCompHausProbePresentationMap T U) :=
            (Category.assoc _ _ _).symm
    _ = ((stoneanCompHausProbeFreeQuadrupleIso T U).hom ≫
          splitFreeCechD3 (stoneanCompHausProbePresentationMap T U)) ≫
          splitFreeCechD2 (stoneanCompHausProbePresentationMap T U) := by
            rw [trueProbeD3_free_square]
    _ = 0 := by
      rw [Category.assoc, splitFreeCechD3_comp_D2_zero, comp_zero]

noncomputable def trueProbeDegreeTwoComplex
    (T : Profinite.{u}) (U : Stonean.{u}) :
    ShortComplex (ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (trueProbeD3 T U) (trueProbeD2 T U)
    (trueProbeD3_comp_D2_zero T U)

noncomputable def trueProbeDegreeTwoIsoSplit
    (T : Profinite.{u}) (U : Stonean.{u}) :
    trueProbeDegreeTwoComplex T U ≅
      splitFreeCechDegreeTwoComplex
        (stoneanCompHausProbePresentationMap T U) := by
  refine ShortComplex.isoMk
    (stoneanCompHausProbeFreeQuadrupleIso T U)
    (stoneanCompHausProbeFreeTripleIso T U)
    (stoneanCompHausProbeFreePairIso T U) ?_ ?_
  · exact (trueProbeD3_free_square T U).symm
  · simpa [trueProbeDegreeTwoComplex,
      splitFreeCechDegreeTwoComplex] using
        (trueProbeD2_free_square T U).symm

theorem trueProbeDegreeTwo_exact
    (T : Profinite.{u}) (U : Stonean.{u}) :
    (trueProbeDegreeTwoComplex T U).Exact := by
  let p := stoneanCompHausProbePresentationMap T U
  let s := (stoneanCompHausProbePresentationSplitEpi T U).section_
  have hs : ∀ y, p (s y) = y := by
    intro y
    have h := (stoneanCompHausProbePresentationSplitEpi T U).id
    have := congrArg (fun f => f y) h
    exact this
  exact ShortComplex.exact_of_iso
    (trueProbeDegreeTwoIsoSplit T U).symm
    (splitFreeCechDegreeTwo_exact p s hs)

#print axioms trueProbeD3_free_square
#print axioms trueProbeD3_comp_D2_zero
#print axioms trueProbeDegreeTwo_exact
end CMDG.CondensedCM5R0
