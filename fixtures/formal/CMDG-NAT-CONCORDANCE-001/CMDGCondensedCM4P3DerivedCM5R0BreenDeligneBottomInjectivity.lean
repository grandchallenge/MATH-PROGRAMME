import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneAdditiveBoundary

noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology AlgebraicTopology.DoldKan
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBoundary
namespace CMDG.CondensedCM5R0.BreenDeligneBottomInjectivity
section Quotient
set_option maxHeartbeats 200000
set_option maxRecDepth 400
variable (A : AGrp) (k : ℕ)
abbrev E := (EilenbergMacLaneModel.em (k+1)).obj A
abbrev K := (reducedEMChains (k+1)).obj A
abbrev H := (K A k).homology (k+1)
abbrev S := simplex (E A k) (k+1)

def classMap : reducedFree.obj (S A k) ⟶ H A k :=
  ((K A k).iCyclesIso (k+1) _ rfl (reducedBottom_outgoing_zero A (k+1))).inv ≫
    (K A k).homologyπ (k+1)

set_option backward.isDefEq.respectTransparency false in
instance classMap_epi : Epi (classMap A k) := by
  unfold classMap
  infer_instance

set_option backward.isDefEq.respectTransparency false in
theorem boundary_class_zero :
    (K A k).d (k+2) (k+1) ≫ classMap A k = 0 := by
  unfold classMap
  rw [← (K A k).toCycles_i (k+2) (k+1)]
  rw [Category.assoc, HomologicalComplex.iCyclesIso_hom_inv_id_assoc,
    HomologicalComplex.toCycles_comp_homologyπ]

def classOf (x : S A k) : H A k :=
  classMap A k (reducedGenerator (S A k) x)

theorem classOf_zero : classOf A k 0 = 0 := by
  unfold classOf
  rw [generator_zero]
  exact map_zero (classMap A k).hom

set_option backward.isDefEq.respectTransparency false in
theorem classOf_add (a b : S A k) : classOf A k (a+b) = classOf A k a + classOf A k b := by
  have hw := witness_boundary (E A k) k (emBelow_isZero A (k+1) k (by omega)) a b
  change (K A k).d (k+2) (k+1)
      (reducedGenerator (simplex (E A k) (k+2)) (witness (E A k) k a b)) = _ at hw
  have h := CategoryTheory.congr_fun (boundary_class_zero A k)
      (reducedGenerator (simplex (E A k) (k+2)) (witness (E A k) k a b))
  change classMap A k ((K A k).d (k+2) (k+1) _) = 0 at h
  rw [hw] at h
  change (classMap A k).hom _ = 0 at h
  rw [map_add, map_sub] at h
  change classOf A k a - classOf A k (a+b) + classOf A k b = 0 at h
  exact (sub_eq_zero.mp (by simpa [sub_add_eq_add_sub] using h)).symm

def classHom : S A k ⟶ H A k := AddCommGrpCat.ofHom {
  toFun := classOf A k
  map_zero' := classOf_zero A k
  map_add' := classOf_add A k }

set_option backward.isDefEq.respectTransparency false in
theorem class_factor : evaluateReduced.app (S A k) ≫ classHom A k = classMap A k := by
  have hp : reducedInclusion.app (S A k) ≫ reducedProjectionApp (S A k) = 𝟙 _ :=
    congrArg (fun t => t.app (S A k)) reducedRetract_eq
  haveI : Epi (reducedProjectionApp (S A k)) := epi_of_epi_fac hp
  apply (cancel_epi (reducedProjectionApp (S A k))).mp
  apply AddCommGrpCat.hom_ext
  apply FreeAbelianGroup.lift_ext
  intro x
  change classHom A k (evaluateReduced.app (S A k) (reducedGenerator (S A k) x)) =
    classMap A k (reducedGenerator (S A k) x)
  rw [evaluateReduced_generator]
  rfl

set_option backward.isDefEq.respectTransparency false in
instance classHom_epi : Epi (classHom A k) :=
  epi_of_epi_fac (class_factor A k)

set_option backward.isDefEq.respectTransparency false in
/-- The Moore projector is the identity in the first nonzero simplex degree. -/
theorem bottom_PInfty :
    (PInfty : (alternatingFaceMapComplex AGrp).obj (E A k) ⟶ _).f (k+1) = 𝟙 _ := by
  rw [PInfty_f]
  have h : HigherFacesVanish (k+1) (𝟙 (S A k)) := by
    intro j _
    rw [Category.id_comp]
    exact (emBelow_isZero A (k+1) k (by omega)).eq_of_tgt _ _
  have hh := h.comp_P_eq_self
  change 𝟙 (S A k) ≫ (P (k+1) : (alternatingFaceMapComplex AGrp).obj (E A k) ⟶ _).f (k+1) = 𝟙 (S A k) at hh
  rw [Category.id_comp] at hh
  exact hh

set_option backward.isDefEq.respectTransparency false in
theorem bottomNormalization_iso :
    IsIso ((PInftyToNormalizedMooreComplex (E A k)).f (k+1)) := by
  let X := E A k
  let n := k+1
  -- Extract the degreewise identity from the chain-map equation.
  have hc : (PInftyToNormalizedMooreComplex X).f n ≫
      (inclusionOfMooreComplexMap X).f n = 𝟙 _ :=
    (congrArg (fun f : (alternatingFaceMapComplex AGrp).obj X ⟶ _ => f.f n)
      (PInftyToNormalizedMooreComplex_comp_inclusionOfMooreComplexMap X)).trans
      (bottom_PInfty A k)
  have hd : (inclusionOfMooreComplexMap X).f n ≫
      (PInftyToNormalizedMooreComplex X).f n = 𝟙 _ :=
    congrArg (fun f : (normalizedMooreComplex AGrp).obj X ⟶ _ => f.f n)
      (splitMonoInclusionOfMooreComplexMap X).id
  exact ⟨⟨(inclusionOfMooreComplexMap X).f n, hc, hd⟩⟩

/-- Actual comparison from the bottom simplex to the input group. -/
def simplexToGroup : S A k ⟶ A :=
  (PInftyToNormalizedMooreComplex (E A k)).f (k+1) ≫
    (DK.counitIso.app ((singleDegree (k+1)).obj A)).hom.f (k+1) ≫
      (HomologicalComplex.singleObjXSelf (ComplexShape.down ℕ) (k+1) A).hom

set_option backward.isDefEq.respectTransparency false in
instance simplexToGroup_iso : IsIso (simplexToGroup A k) := by
  unfold simplexToGroup
  haveI := bottomNormalization_iso A k
  haveI : IsIso ((DK.counitIso.app ((singleDegree (k+1)).obj A)).hom.f (k+1)) := by
    change IsIso ((HomologicalComplex.eval AGrp (ComplexShape.down ℕ) (k+1)).map
      (DK.counitIso.app ((singleDegree (k+1)).obj A)).hom)
    infer_instance
  infer_instance

set_option backward.isDefEq.respectTransparency false in
theorem classMap_comparison :
    classMap A k ≫ bottomHomologyToGroup A (k+1) =
      evaluateReduced.app (S A k) ≫ simplexToGroup A k := by
  let n := k+1
  let L := (singleDegree n).obj A
  let f := (bottomAugmentation n).app A
  let e := (K A k).iCyclesIso n _ rfl (reducedBottom_outgoing_zero A n)
  change (e.inv ≫ (K A k).homologyπ n) ≫
      (HomologicalComplex.homologyMap f n ≫
        (HomologicalComplex.singleObjHomologySelfIso (ComplexShape.down ℕ) n A).hom) = _
  rw [Category.assoc, HomologicalComplex.homologyπ_naturality_assoc]
  have hh : L.homologyπ n ≫
      (HomologicalComplex.singleObjHomologySelfIso (ComplexShape.down ℕ) n A).hom =
      L.iCycles n ≫ (HomologicalComplex.singleObjXSelf (ComplexShape.down ℕ) n A).hom :=
    HomologicalComplex.homologyπ_singleObjHomologySelfIso_hom (C := AGrp) (c := ComplexShape.down ℕ) (j := n) (A := A)
  rw [hh]
  rw [← Category.assoc, Category.assoc e.inv, ← Category.assoc (HomologicalComplex.cyclesMap f n)]
  -- The remaining cycle inclusion identifies the actual degreewise comparison.
  rw [HomologicalComplex.cyclesMap_i]
  have he : e.inv ≫ (K A k).iCycles n = 𝟙 _ := e.inv_hom_id
  change (e.inv ≫ (K A k).iCycles n ≫ f.f n) ≫ _ = _
  rw [← Category.assoc e.inv, he, Category.id_comp]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem classHom_comparison :
    classHom A k ≫ bottomHomologyToGroup A (k+1) = simplexToGroup A k := by
  apply (cancel_epi (evaluateReduced.app (S A k))).mp
  rw [← Category.assoc, class_factor, classMap_comparison]

set_option backward.isDefEq.respectTransparency false in
theorem bottomHomologyToGroup_iso : IsIso (bottomHomologyToGroup A (k+1)) := by
  haveI : IsIso (classHom A k ≫ bottomHomologyToGroup A (k+1)) := by
    rw [classHom_comparison]
    infer_instance
  haveI : Mono (classHom A k) := mono_of_mono _ (bottomHomologyToGroup A (k+1))
  haveI : IsIso (classHom A k) := isIso_of_mono_of_epi _
  have h : bottomHomologyToGroup A (k+1) =
      inv (classHom A k) ≫ (classHom A k ≫ bottomHomologyToGroup A (k+1)) := by simp
  rw [h]
  infer_instance

end Quotient
set_option backward.isDefEq.respectTransparency false in
/-- The exact positive-degree homology comparison is natural in the input group. -/
def bottomHomologyNaturalIso (k : ℕ) :
    reducedEMChains (k+1) ⋙ HomologicalComplex.homologyFunctor AGrp
      (ComplexShape.down ℕ) (k+1) ≅ 𝟭 AGrp :=
  NatIso.ofComponents (fun A => by
    letI := bottomHomologyToGroup_iso A k
    exact asIso (bottomHomologyToGroup A (k+1))) (fun {A B} f => by
    let n := k+1
    change HomologicalComplex.homologyMap ((reducedEMChains n).map f) n ≫
      bottomHomologyToGroup B n = bottomHomologyToGroup A n ≫ f
    unfold bottomHomologyToGroup
    rw [← HomologicalComplex.homologyMap_comp_assoc,
      (bottomAugmentation n).naturality f, HomologicalComplex.homologyMap_comp_assoc]
    have h : HomologicalComplex.homologyMap ((singleDegree n).map f) n ≫
        (HomologicalComplex.singleObjHomologySelfIso (ComplexShape.down ℕ) n B).hom =
        (HomologicalComplex.singleObjHomologySelfIso (ComplexShape.down ℕ) n A).hom ≫ f :=
      HomologicalComplex.singleObjHomologySelfIso_hom_naturality (c := ComplexShape.down ℕ) (j := n) f
    rw [h, Category.assoc])

#print axioms class_factor
#print axioms classHom_epi
#print axioms bottomHomologyToGroup_iso
#print axioms bottomHomologyNaturalIso
end CMDG.CondensedCM5R0.BreenDeligneBottomInjectivity
