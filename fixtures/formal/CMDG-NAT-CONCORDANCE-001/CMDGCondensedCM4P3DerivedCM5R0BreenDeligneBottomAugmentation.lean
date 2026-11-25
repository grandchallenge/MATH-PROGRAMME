import CMDGCondensedCM4P3DerivedCM5R0EilenbergMacLaneModel
import Mathlib.AlgebraicTopology.DoldKan.Equivalence
import Mathlib.Algebra.Homology.SingleHomology

/-! The canonical evaluation and normalization augmentation of the actual
reduced Dold-Kan chain complex, without assuming Hurewicz or stable homology. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology AlgebraicTopology.DoldKan
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation

abbrev AGrp := AddCommGrpCat.{0}

def evaluateFree : forgetFree ⟶ 𝟭 AGrp where
  app A := AddCommGrpCat.ofHom (FreeAbelianGroup.lift (fun x : A => x))
  naturality {A B} f := by
    apply AddCommGrpCat.hom_ext
    apply FreeAbelianGroup.lift_ext
    intro x
    change FreeAbelianGroup.lift (fun y : B => y)
      (FreeAbelianGroup.map (fun y : A => f y) (FreeAbelianGroup.of x)) =
      f (FreeAbelianGroup.lift (fun y : A => y) (FreeAbelianGroup.of x))
    simp [FreeAbelianGroup.map_of_apply]

def evaluateReduced : reducedFree ⟶ 𝟭 AGrp :=
  reducedInclusion ≫ evaluateFree

/-- Generator minus the identity generator in the actual reduced group. -/
def reducedGenerator (A : AGrp) (x : A) : reducedFree.obj A :=
  reducedProjectionApp A (FreeAbelianGroup.of x)

set_option backward.isDefEq.respectTransparency false in
theorem evaluateReduced_generator (A : AGrp) (x : A) :
    evaluateReduced.app A (reducedGenerator A x) = x := by
  have h := CategoryTheory.congr_fun (reducedProjectionApp_ι A) (FreeAbelianGroup.of x)
  change (evaluateFree.app A) (kernel.ι (augmentation A)
    (reducedProjectionApp A (FreeAbelianGroup.of x))) = x
  change kernel.ι (augmentation A) (reducedProjectionApp A (FreeAbelianGroup.of x)) =
    (𝟙 (forgetFree.obj A) - augmentation A ≫ basepoint A) (FreeAbelianGroup.of x) at h
  rw [h]
  change (FreeAbelianGroup.lift (fun y : A => y))
    (FreeAbelianGroup.of x - FreeAbelianGroup.of (0 : A)) = x
  simp

instance evaluateReduced_epi (A : AGrp) : Epi (evaluateReduced.app A) :=
  (AddCommGrpCat.epi_iff_surjective _).mpr fun x => ⟨reducedGenerator A x,
    evaluateReduced_generator A x⟩

def evaluateSimplicial (n : ℕ) :
    em n ⋙ (SimplicialObject.whiskering AGrp AGrp).obj reducedFree ⟶ em n where
  app A := Functor.whiskerLeft ((em n).obj A) evaluateReduced ≫
    (Functor.rightUnitor ((em n).obj A)).hom
  naturality {A B} f := by
    apply NatTrans.ext
    funext Δ
    exact evaluateReduced.naturality (((em n).map f).app Δ)

def normalizationProjection :
    alternatingFaceMapComplex AGrp ⟶ normalizedMooreComplex AGrp where
  app X := PInftyToNormalizedMooreComplex X
  naturality {_X _Y} f := PInftyToNormalizedMooreComplex_naturality f

abbrev DK : SimplicialObject AGrp ≌ ChainComplex AGrp ℕ :=
  CategoryTheory.Abelian.DoldKan.equivalence

/-- The canonical chain augmentation through evaluation, normalization and
the actual Dold-Kan counit. -/
def bottomAugmentation (n : ℕ) : reducedEMChains n ⟶ singleDegree n :=
  Functor.whiskerRight (evaluateSimplicial n) (alternatingFaceMapComplex AGrp) ≫
    Functor.whiskerLeft (em n) normalizationProjection ≫
    Functor.whiskerLeft (singleDegree n) DK.counitIso.hom

set_option backward.isDefEq.respectTransparency false in
theorem normalizationProjection_degree_epi (X : SimplicialObject AGrp) (m : ℕ) :
    Epi ((PInftyToNormalizedMooreComplex X).f m) := by
  have h : inclusionOfMooreComplexMap X ≫ PInftyToNormalizedMooreComplex X = 𝟙 _ :=
    (splitMonoInclusionOfMooreComplexMap X).id
  have h' : (inclusionOfMooreComplexMap X).f m ≫
      (PInftyToNormalizedMooreComplex X).f m = 𝟙 _ :=
    congrArg (fun f : (normalizedMooreComplex AGrp).obj X ⟶ _ => f.f m) h
  refine ⟨fun {Z} g g' hh => ?_⟩
  have he := congrArg (fun k => (inclusionOfMooreComplexMap X).f m ≫ k) hh
  simpa only [← Category.assoc, h', Category.id_comp] using he

set_option backward.isDefEq.respectTransparency false in
theorem bottomAugmentation_degree_epi (A : AGrp) (n m : ℕ) :
    Epi (((bottomAugmentation n).app A).f m) := by
  let X := (em n).obj A
  let K := (singleDegree n).obj A
  letI : Epi ((PInftyToNormalizedMooreComplex X).f m) :=
    normalizationProjection_degree_epi X m
  haveI : IsIso ((DK.counitIso.app K).hom.f m) := by
    change IsIso ((HomologicalComplex.eval AGrp (ComplexShape.down ℕ) m).map
      (DK.counitIso.app K).hom)
    infer_instance
  change Epi ((evaluateReduced.app (X.obj (op (SimplexCategory.mk m))) ≫
    (PInftyToNormalizedMooreComplex X).f m) ≫ (DK.counitIso.app K).hom.f m)
  infer_instance

theorem reducedHomology_below (A : AGrp) (n m : ℕ) (h : m < n) :
    IsZero (((reducedEMChains n).obj A).homology m) :=
  ShortComplex.isZero_homology_of_isZero_X₂ _ (reducedEMChains_below A n m h)

theorem reducedBottom_outgoing_zero (A : AGrp) (n : ℕ) :
    ((reducedEMChains n).obj A).d n ((ComplexShape.down ℕ).next n) = 0 := by
  cases n with
  | zero => rw [ChainComplex.next_nat_zero]; exact HomologicalComplex.shape _ _ _ (by simp)
  | succ n =>
    rw [ChainComplex.next_nat_succ]
    exact (reducedEMChains_below A (n+1) n (by omega)).eq_of_tgt _ _

set_option backward.isDefEq.respectTransparency false in
/-- Actual bottom-degree homology maps onto the original group.
Injectivity is the remaining bottom Hurewicz obligation. -/
theorem bottomHomologyMap_epi (A : AGrp) (n : ℕ) :
    Epi (HomologicalComplex.homologyMap ((bottomAugmentation n).app A) n) := by
  let K := (reducedEMChains n).obj A
  let L := (singleDegree n).obj A
  let f := (bottomAugmentation n).app A
  haveI : Epi (f.f n) := bottomAugmentation_degree_epi A n n
  haveI : IsIso (K.iCycles n) :=
    K.isIso_iCycles n _ rfl (reducedBottom_outgoing_zero A n)
  haveI : Epi (HomologicalComplex.cyclesMap f n ≫ L.iCycles n) := by
    rw [HomologicalComplex.cyclesMap_i]
    infer_instance
  haveI : IsIso (L.iCycles n) := L.isIso_iCycles n _ rfl (by
    change ((singleDegree n).obj A).d n _ = 0
    simp [singleDegree])
  haveI : Epi (HomologicalComplex.cyclesMap f n) :=
    (epi_comp_iff_of_isIso (HomologicalComplex.cyclesMap f n) (L.iCycles n)).mp
      inferInstance
  haveI : Epi (K.homologyπ n ≫ HomologicalComplex.homologyMap f n) := by
    rw [HomologicalComplex.homologyπ_naturality]
    infer_instance
  exact epi_of_epi (K.homologyπ n) (HomologicalComplex.homologyMap f n)

def bottomHomologyToGroup (A : AGrp) (n : ℕ) :
    ((reducedEMChains n).obj A).homology n ⟶ A :=
  HomologicalComplex.homologyMap ((bottomAugmentation n).app A) n ≫
    (HomologicalComplex.singleObjHomologySelfIso (ComplexShape.down ℕ) n A).hom

set_option backward.isDefEq.respectTransparency false in
instance bottomHomologyToGroup_epi (A : AGrp) (n : ℕ) :
    Epi (bottomHomologyToGroup A n) := by
  unfold bottomHomologyToGroup
  letI : Epi (HomologicalComplex.homologyMap ((bottomAugmentation n).app A) n) :=
    bottomHomologyMap_epi A n
  infer_instance

#print axioms evaluateReduced_generator
#print axioms bottomAugmentation
#print axioms reducedHomology_below
#print axioms bottomHomologyToGroup_epi
end CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
