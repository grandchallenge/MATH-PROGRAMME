import CMDGCondensedCM4P3DerivedCM5R0ProbeDegreeThreeExact
import CMDGCondensedCM4P3DerivedCM5R0GlobalThirdRelationEpi
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

/-!
# CMDG CM5 — fifth Čech differential and global fourth relation

The genuine iterated categorical fifth Čech pullback is connected to
the closed fivefold relation by a proved isomorphism. Its five-face
boundary is transported into real condensed-module morphisms and
presheaf modules before the Stonean restriction exactness argument.
-/

noncomputable section
universe u
open CategoryTheory Limits CategoryTheory.Functor
namespace CMDG.CondensedCM5R0

noncomputable def stoneanCechCategoricalFifthBoundary
    (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuintuples T) ⟶
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T) :=
  (Condensed.profiniteFree Coeff).map
    (stoneanCechCategoricalQuintupleToExplicit T) ≫
      stoneanCechFifthBoundary T

theorem stoneanCechCategoricalFifthBoundary_comp_fourth_zero
    (T : Profinite.{u}) :
    stoneanCechCategoricalFifthBoundary T ≫
      stoneanCechFourthBoundary T = 0 := by
  unfold stoneanCechCategoricalFifthBoundary
  rw [Category.assoc, stoneanCechFifthBoundary_comp_fourthBoundary_zero,
    comp_zero]

noncomputable def presheafStoneanCechFifthBoundary
    (T : Profinite.{u}) :
    freeCompHausModulePresheaf (stoneanPresentationCechQuintuples T) ⟶
      freeCompHausModulePresheaf (stoneanPresentationCechQuadruples T) :=
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace0 T) -
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace1 T) +
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace2 T) -
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace3 T) +
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalQuintupleToExplicit T ≫
      stoneanCechFifthFace4 T)

theorem presheafStoneanCechFifthBoundary_sheafify
    (T : Profinite.{u}) :
    moduleSheafification.map (presheafStoneanCechFifthBoundary T) =
      stoneanCechCategoricalFifthBoundary T := by
  unfold presheafStoneanCechFifthBoundary
    stoneanCechCategoricalFifthBoundary stoneanCechFifthBoundary
  rw [Functor.map_add, Functor.map_sub, Functor.map_add, Functor.map_sub]
  simp only [Functor.map_comp, Preadditive.comp_add,
    Preadditive.comp_sub]
  rfl

theorem presheafStoneanCechFifthBoundary_comp_fourth_zero
    (T : Profinite.{u}) :
    presheafStoneanCechFifthBoundary T ≫
      presheafStoneanCechFourthBoundary T = 0 := by
  have hFourth : presheafStoneanCechFourthBoundary T =
      freeCompHausModulePresheafFunctor.map (quadFaceYZW T) -
      freeCompHausModulePresheafFunctor.map (quadFaceXZW T) +
      freeCompHausModulePresheafFunctor.map (quadFaceXYW T) -
      freeCompHausModulePresheafFunctor.map (stoneanCechQuadFaceXYZ T) := by
        rfl
  rw [hFourth]
  unfold presheafStoneanCechFifthBoundary
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.comp_add, Preadditive.comp_sub,
    ← Functor.map_comp]
  let B := stoneanCechCategoricalQuintupleToExplicit T
  have h01 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace01_commute T)
  have h02 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace02_commute T)
  have h03 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace03_commute T)
  have h04 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace04_commute T)
  have h12 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace12_commute T)
  have h13 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace13_commute T)
  have h14 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace14_commute T)
  have h23 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace23_commute T)
  have h24 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace24_commute T)
  have h34 := congrArg
    (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechTriples T => B ≫ m)
    (stoneanCechFifthFace34_commute T)
  simp only [Category.assoc] at *
  dsimp only [B] at h01 h02 h03 h04 h12 h13 h14 h23 h24 h34
  rw [h01, h02, h03, h04, h12, h13, h14, h23, h24, h34]
  simp only [sub_eq_add_neg]
  abel


noncomputable def presheafStoneanCechDegreeThreeComplex (T : Profinite.{u}) :
    ShortComplex (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (presheafStoneanCechFifthBoundary T)
    (presheafStoneanCechFourthBoundary T)
    (presheafStoneanCechFifthBoundary_comp_fourth_zero T)

noncomputable abbrev stoneanRestrictedCechDegreeThreeComplex
    (T : Profinite.{u}) :
    ShortComplex (Stonean.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  (presheafStoneanCechDegreeThreeComplex T).map
    stoneanPresheafRestriction

theorem stoneanRestrictedCechDegreeThree_exact
    (T : Profinite.{u}) :
    (stoneanRestrictedCechDegreeThreeComplex T).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro U
  change (trueProbeDegreeThreeComplex T U.unop).Exact
  exact trueProbeDegreeThree_exact T U.unop

noncomputable def stoneanCechDegreeThreeComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk (stoneanCechCategoricalFifthBoundary T)
    (stoneanCechFourthBoundary T)
    (stoneanCechCategoricalFifthBoundary_comp_fourth_zero T)

theorem stoneanCechDegreeThree_exact_unconditional
    (T : Profinite.{u}) :
    (stoneanCechDegreeThreeComplex T).Exact := by
  let S := presheafStoneanCechDegreeThreeComplex T
  let R := stoneanPresheafRestriction
  let A := stoneanModuleSheafification
  let E := (Condensed.StoneanCompHaus.equivalence
    (ModuleCat Coeff)).inverse
  haveI : PreservesFiniteLimits A := by
    change PreservesFiniteLimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  haveI : PreservesFiniteColimits A := by
    change PreservesFiniteColimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  have hStonean : ((S.map R).map A).Exact :=
    (stoneanRestrictedCechDegreeThree_exact T).map A
  have hStonean' : (S.map (R ⋙ A)).Exact := by
    simpa only [ShortComplex.map_comp] using hStonean
  have hTransport :
      (S.map (moduleSheafification ⋙ E)).Exact :=
    ShortComplex.exact_of_iso
      (S.mapNatIso stoneanCompHausSheafificationCompatibility)
      hStonean'
  have hTransport' :
      ((S.map moduleSheafification).map E).Exact := by
    simpa only [ShortComplex.map_comp] using hTransport
  have hComp : (S.map moduleSheafification).Exact :=
    E.reflects_exact_of_faithful _ hTransport'
  have hZero :
      kernel.ι ((S.map moduleSheafification).g) ≫
      cokernel.π ((S.map moduleSheafification).f) = 0 :=
    ((S.map moduleSheafification).exact_iff_kernel_ι_comp_cokernel_π_zero).1 hComp
  have hZero' :
      kernel.ι (stoneanCechFourthBoundary T) ≫
      cokernel.π (stoneanCechCategoricalFifthBoundary T) = 0 := by
    rw [← presheafStoneanCechFourthBoundary_sheafify T,
      ← presheafStoneanCechFifthBoundary_sheafify T]
    exact hZero
  exact ((stoneanCechDegreeThreeComplex T).exact_iff_kernel_ι_comp_cokernel_π_zero).2 hZero'

#print axioms stoneanRestrictedCechDegreeThree_exact

theorem stoneanCechCategoricalFifthBoundary_comp_thirdRelation_zero
    (T : Profinite.{u}) :
    stoneanCechCategoricalFifthBoundary T ≫
      stoneanCechFourthToThirdRelation T = 0 := by
  apply (cancel_mono
    (kernel.ι (stoneanCechTripleToSecondRelation T))).1
  rw [Category.assoc, stoneanCechFourthToThirdRelation_comp_inclusion,
    zero_comp]
  exact stoneanCechCategoricalFifthBoundary_comp_fourth_zero T

noncomputable def stoneanCechDegreeThreeKernelComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk
    (stoneanCechCategoricalFifthBoundary T)
    (stoneanCechFourthToThirdRelation T)
    (stoneanCechCategoricalFifthBoundary_comp_thirdRelation_zero T)

noncomputable def stoneanCechDegreeThreeKernelComparison
    (T : Profinite.{u}) :
    stoneanCechDegreeThreeKernelComplex T ⟶
      stoneanCechDegreeThreeComplex T :=
  ShortComplex.homMk
    (𝟙 _) (𝟙 _) (kernel.ι (stoneanCechTripleToSecondRelation T))
    (by dsimp [stoneanCechDegreeThreeKernelComplex,
      stoneanCechDegreeThreeComplex]; simp)
    (by dsimp [stoneanCechDegreeThreeKernelComplex,
      stoneanCechDegreeThreeComplex]
        simpa only [Category.id_comp] using
          (stoneanCechFourthToThirdRelation_comp_inclusion T).symm)

theorem stoneanCechCategoricalFifthToFourthRelation_epi
    (T : Profinite.{u}) :
    Epi (kernel.lift (stoneanCechFourthToThirdRelation T)
      (stoneanCechCategoricalFifthBoundary T)
      (stoneanCechCategoricalFifthBoundary_comp_thirdRelation_zero T)) := by
  haveI : Epi (stoneanCechDegreeThreeKernelComparison T).τ₁ := by
    change Epi (𝟙 ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuintuples T)))
    infer_instance
  haveI : IsIso (stoneanCechDegreeThreeKernelComparison T).τ₂ := by
    change IsIso (𝟙 ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)))
    infer_instance
  haveI : Mono (stoneanCechDegreeThreeKernelComparison T).τ₃ := by
    change Mono (kernel.ι (stoneanCechTripleToSecondRelation T))
    infer_instance
  have hk : (stoneanCechDegreeThreeKernelComplex T).Exact :=
    (ShortComplex.exact_iff_of_epi_of_isIso_of_mono
      (stoneanCechDegreeThreeKernelComparison T)).mpr
        (stoneanCechDegreeThree_exact_unconditional T)
  exact ((stoneanCechDegreeThreeKernelComplex T).exact_iff_epi_kernel_lift).mp hk

theorem stoneanCechFifthToFourthRelation_epi_unconditional
    (T : Profinite.{u}) :
    Epi (stoneanCechFifthToFourthRelation T) := by
  let B := stoneanCechCategoricalQuintupleToExplicit T
  let F := (Condensed.profiniteFree Coeff).map B
  let h := kernel.lift (stoneanCechFourthToThirdRelation T)
    (stoneanCechCategoricalFifthBoundary T)
    (stoneanCechCategoricalFifthBoundary_comp_thirdRelation_zero T)
  have hEq : F ≫ stoneanCechFifthToFourthRelation T = h := by
    apply (cancel_mono (kernel.ι (stoneanCechFourthToThirdRelation T))).1
    rw [Category.assoc, stoneanCechFifthToFourthRelation_comp_inclusion,
      kernel.lift_ι]
    rfl
  haveI : Epi h := stoneanCechCategoricalFifthToFourthRelation_epi T
  haveI : IsIso F := by
    change IsIso ((Condensed.profiniteFree Coeff).map
      (stoneanCechExplicitQuintupleIso T).inv)
    infer_instance
  haveI : Epi (stoneanCechFifthToFourthRelation T) :=
    (epi_comp_iff_of_epi (F) (stoneanCechFifthToFourthRelation T)).mp
      (by rw [hEq]; infer_instance)
  infer_instance

#print axioms stoneanCechCategoricalFifthToFourthRelation_epi
#print axioms stoneanCechFifthToFourthRelation_epi_unconditional
#print axioms stoneanCechDegreeThree_exact_unconditional
#print axioms presheafStoneanCechFifthBoundary_comp_fourth_zero
#print axioms stoneanCechCategoricalFifthBoundary_comp_fourth_zero
#print axioms presheafStoneanCechFifthBoundary_sheafify
end CMDG.CondensedCM5R0
