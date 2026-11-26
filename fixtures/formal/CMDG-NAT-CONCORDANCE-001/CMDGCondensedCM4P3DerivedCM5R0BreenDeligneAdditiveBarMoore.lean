import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBarDiagonalComparison

/-! Ordinary additive bar normalization: only horizontal degree one
survives. This is not the normalization of the reduced free chains. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BreenDeligneBarTupleQuotient
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneAdditiveBarMoore

abbrev N (A : AGrp) := (normalizedMooreComplex AGrp).obj (bar A)
abbrev inc (A : AGrp) (p : ℕ) := (inclusionOfMooreComplexMap (bar A)).f p

theorem lastFace (A : AGrp) (m : ℕ) (x : Tuples A (m+1)) (j : Fin m) :
    (bar A).δ (Fin.last (m+1)) x j = x j.castSucc := by
  change Fin.partialSum x ((Fin.last (m+1)).succAbove j.succ) -
    Fin.partialSum x ((Fin.last (m+1)).succAbove j.castSucc) = _
  rw [Fin.succAbove_of_castSucc_lt _ _ (by
    change j.val+1<m+1
    have := j.isLt
    omega),Fin.succAbove_of_castSucc_lt _ _ (by
    change j.val<m+1
    have := j.isLt
    omega)]
  have h : j.succ.castSucc=j.castSucc.succ := Fin.ext rfl
  rw [h,Fin.partialSum_succ]
  abel

theorem penultimateFace (A : AGrp) (m : ℕ) (x : Tuples A (m+2)) :
    (bar A).δ ((Fin.last (m+1)).castSucc) x (Fin.last m) =
      x (Fin.last m).castSucc + x (Fin.last (m+1)) := by
  change Fin.partialSum x (((Fin.last (m+1)).castSucc).succAbove (Fin.last m).succ) -
    Fin.partialSum x (((Fin.last (m+1)).castSucc).succAbove (Fin.last m).castSucc) = _
  rw [Fin.succAbove_of_le_castSucc _ _ (by rfl),Fin.succAbove_of_castSucc_lt _ _ (by
    change m<m+1
    omega)]
  have h₁ : (Fin.last m).succ.succ= (Fin.last (m+1)).succ := Fin.ext rfl
  rw [h₁,Fin.partialSum_succ]
  -- express the intermediate vertex as the successor of the penultimate edge
  have h₃ : (Fin.last (m+1)).castSucc = (Fin.last m).castSucc.succ := Fin.ext rfl
  rw [h₃,Fin.partialSum_succ]
  abel

set_option backward.isDefEq.respectTransparency false in
instance inc_mono (A : AGrp) (p : ℕ) : Mono (inc A p) := by
  change Mono ((inclusionOfMooreComplexMap (bar A)).f p)
  rw [inclusionOfMooreComplexMap_f]
  infer_instance

theorem mooreZero (A : AGrp) : IsZero ((N A).X 0) := by
  apply IsZero.of_mono (inc A 0)
  apply (IsZero.iff_id_eq_zero _).mpr
  apply ConcreteCategory.hom_ext
  intro x
  funext i
  exact Fin.elim0 i

theorem highFaceZero (A : AGrp) (m : ℕ) (j : Fin (m+3)) (hj : j ≠ 0) :
    inc A (m+2) ≫ (bar A).δ j=0 :=
  (AlgebraicTopology.DoldKan.HigherFacesVanish.inclusionOfMooreComplexMap (X:=bar A) (m+1)).comp_δ_eq_zero j hj (by
    have h : 0<j.val := Fin.pos_iff_ne_zero.mpr hj
    omega)

theorem highIncZero (A : AGrp) (m : ℕ) : inc A (m+2) = 0 := by
  apply ConcreteCategory.hom_ext
  intro z
  let x : Tuples A (m+2) := inc A (m+2) z
  have hlast : (bar A).δ (Fin.last (m+2)) x = 0 :=
    CategoryTheory.congr_fun (highFaceZero A m _ (by simp)) z
  have hpen : (bar A).δ ((Fin.last (m+1)).castSucc) x = 0 :=
    CategoryTheory.congr_fun (highFaceZero A m _ (by
      intro h
      have he := congrArg Fin.val h
      change m+1=0 at he
      omega)) z
  have hpre (j : Fin (m+1)) : x j.castSucc=0 := by
    rw [← lastFace A (m+1) x j,hlast]
    rfl
  have hfin : x (Fin.last (m+1))=0 := by
    have he := congrFun hpen (Fin.last m)
    rw [penultimateFace,hpre,zero_add] at he
    exact he
  change x=0
  funext j
  refine Fin.lastCases ?_ hpre j
  exact hfin

theorem mooreHighZero (A : AGrp) (m : ℕ) : IsZero ((N A).X (m+2)) := by
  apply (IsZero.iff_id_eq_zero _).mpr
  apply (cancel_mono (inc A (m+2))).mp
  rw [Category.id_comp,zero_comp,highIncZero]

def tupleOneIso (A : AGrp) : barTerm A (op (SimplexCategory.mk 1)) ≅ A where
  hom := AddCommGrpCat.ofHom {
    toFun x := x 0
    map_zero' := rfl
    map_add' _ _ := rfl }
  inv := AddCommGrpCat.ofHom {
    toFun a _ := a
    map_zero' := rfl
    map_add' _ _ := rfl }
  hom_inv_id := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    have hi : i=0 := Subsingleton.elim _ _
    subst i
    rfl
  inv_hom_id := by
    apply ConcreteCategory.hom_ext
    intro a
    rfl

set_option backward.isDefEq.respectTransparency false in
theorem pOneId (A : AGrp) :
    (AlgebraicTopology.DoldKan.PInfty (X:=bar A)).f 1 = 𝟙 _ := by
  have h : AlgebraicTopology.DoldKan.HigherFacesVanish (X:=bar A) 1
      (𝟙 (barTerm A (op (SimplexCategory.mk 1)))) := by
    intro j _
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    exact Fin.elim0 i
  have he := h.comp_P_eq_self
  change (𝟙 ((alternatingFaceMapComplex AGrp).obj (bar A)).X 1) ≫
    (AlgebraicTopology.DoldKan.P 1 (X:=bar A)).f 1 = 𝟙 _ at he
  exact (Category.id_comp ((AlgebraicTopology.DoldKan.P 1 (X:=bar A)).f 1)).symm.trans he

def mooreOneIso (A : AGrp) : (N A).X 1 ≅ barTerm A (op (SimplexCategory.mk 1)) where
  hom := inc A 1
  inv := (AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex (bar A)).f 1
  hom_inv_id := congrArg (fun f : N A ⟶ N A => f.f 1)
    (AlgebraicTopology.DoldKan.splitMonoInclusionOfMooreComplexMap (bar A)).id
  inv_hom_id := by
    have h := congrArg (fun f : (alternatingFaceMapComplex AGrp).obj (bar A) ⟶ _ => f.f 1)
      (AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex_comp_inclusionOfMooreComplexMap (bar A))
    exact h.trans (pOneId A)

def mooreSingleComponent (A : AGrp) (p : ℕ) :
    (N A).X p ≅ ((singleDegree 1).obj A).X p := by
  by_cases hp : p=1
  · subst p
    exact mooreOneIso A ≪≫ tupleOneIso A ≪≫
      (HomologicalComplex.singleObjXSelf (ComplexShape.down ℕ) 1 A).symm
  · have hz : IsZero ((N A).X p) := by
      cases p with
      | zero => exact mooreZero A
      | succ p =>
        cases p with
        | zero => exact (hp rfl).elim
        | succ m => exact mooreHighZero A m
    exact hz.iso (HomologicalComplex.isZero_single_obj_X (ComplexShape.down ℕ) 1 A p hp)

def mooreSingleIso (A : AGrp) : N A ≅ (singleDegree 1).obj A :=
  HomologicalComplex.Hom.isoOfComponents (mooreSingleComponent A) (by
    intro i j h
    change j+1=i at h
    subst i
    cases j with
    | zero => exact (HomologicalComplex.isZero_single_obj_X (ComplexShape.down ℕ) 1 A 0 (by decide)).eq_of_tgt _ _
    | succ j => exact (mooreHighZero A j).eq_of_src _ _)

def additiveMoore : AGrp ⥤ ChainComplex AGrp ℕ :=
  barFunctor ⋙ normalizedMooreComplex AGrp

set_option backward.isDefEq.respectTransparency false in
theorem tupleOne_natural {A B : AGrp} (f : A ⟶ B) :
    (barNat f).app (op (SimplexCategory.mk 1)) ≫ (tupleOneIso B).hom =
      (tupleOneIso A).hom ≫ f := by
  apply ConcreteCategory.hom_ext
  intro x
  rfl

set_option backward.isDefEq.respectTransparency false in
def mooreSingleNatIso : additiveMoore ≅ singleDegree 1 :=
  NatIso.ofComponents mooreSingleIso (fun {A B} f => by
    apply HomologicalComplex.Hom.ext
    funext p
    by_cases hp : p=1
    · subst p
      change (additiveMoore.map f).f 1 ≫ (mooreSingleComponent B 1).hom =
        (mooreSingleComponent A 1).hom ≫ ((singleDegree 1).map f).f 1
      simp only [mooreSingleComponent]
      have hi := congrArg (fun k => k.f 1)
        ((inclusionOfMooreComplex AGrp).naturality (barNat f))
      change (additiveMoore.map f).f 1 ≫ inc B 1 =
        inc A 1 ≫ (barNat f).app (op (SimplexCategory.mk 1)) at hi
      change (additiveMoore.map f).f 1 ≫
          (inc B 1 ≫ (tupleOneIso B).hom ≫
            (HomologicalComplex.singleObjXSelf (ComplexShape.down ℕ) 1 B).inv) =
        (inc A 1 ≫ (tupleOneIso A).hom ≫
          (HomologicalComplex.singleObjXSelf (ComplexShape.down ℕ) 1 A).inv) ≫
          ((singleDegree 1).map f).f 1
      rw [← Category.assoc, ← Category.assoc,hi]
      simp only [Category.assoc]
      rw [← Category.assoc ((barNat f).app _) (tupleOneIso B).hom,tupleOne_natural]
      simp only [Category.assoc]
      congr 2
    · exact (HomologicalComplex.isZero_single_obj_X (ComplexShape.down ℕ) 1 B p hp).eq_of_tgt _ _)

#print axioms mooreSingleNatIso
#print axioms mooreHighZero
#print axioms mooreSingleIso
#print axioms lastFace
end CMDG.CondensedCM5R0.BreenDeligneAdditiveBarMoore
