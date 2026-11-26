import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneNormalizationNaturality

/-! Horizontal normalization of the actual reduced bar bicomplex,
including its natural contraction and totalized homotopies. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneNormalizedBar
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
open CMDG.CondensedCM5R0.BreenDeligneNormalizationNaturality
namespace CMDG.CondensedCM5R0.BreenDeligneBarNormalization

def horizontalAltZ : AGrp ⥤ Ch :=
  reducedBarFunctor ⋙ alternatingFaceMapComplex AGrp ⋙ toZModule.mapHomologicalComplex c

def rawDouble (X : SimplicialObject AGrp) : BC :=
  HomologicalComplex₂.flip ((alternatingFaceMapComplex Ch).obj (X ⋙ horizontalAltZ))

def inclNat : horizontalMooreZ ⟶ horizontalAltZ :=
  Functor.whiskerRight (Functor.whiskerLeft reducedBarFunctor (inclusionOfMooreComplex AGrp))
    (toZModule.mapHomologicalComplex c)

def projNat : horizontalAltZ ⟶ horizontalMooreZ :=
  Functor.whiskerRight (Functor.whiskerLeft reducedBarFunctor ({
    app := AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex
    naturality := fun _ _ f => AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex_naturality f
  } : alternatingFaceMapComplex AGrp ⟶ normalizedMooreComplex AGrp)) (toZModule.mapHomologicalComplex c)

def incl (X : SimplicialObject AGrp) : barDouble X ⟶ rawDouble X :=
  (HomologicalComplex₂.flipFunctor ZMod c c).map
    ((alternatingFaceMapComplex Ch).map (Functor.whiskerLeft X inclNat))

def proj (X : SimplicialObject AGrp) : rawDouble X ⟶ barDouble X :=
  (HomologicalComplex₂.flipFunctor ZMod c c).map
    ((alternatingFaceMapComplex Ch).map (Functor.whiskerLeft X projNat))

set_option backward.isDefEq.respectTransparency false in
theorem incl_proj (X : SimplicialObject AGrp) : incl X ≫ proj X = 𝟙 _ := by
  apply HomologicalComplex.Hom.ext
  funext p
  apply HomologicalComplex.Hom.ext
  funext q
  change toZModule.map (includeMoore (X.obj (op (SimplexCategory.mk q))) p) ≫
    toZModule.map (project (X.obj (op (SimplexCategory.mk q))) p) = 𝟙 _
  rw [← Functor.map_comp,include_project]
  exact toZModule.map_id _

def objectHomotopy (A : AGrp) :=
  toZModule.mapHomotopy (AlgebraicTopology.DoldKan.homotopyPInftyToId (reducedBar A))

set_option backward.isDefEq.respectTransparency false in
def rowHomotopy (X : SimplicialObject AGrp) (i j : ℕ) :
    (rawDouble X).X i ⟶ (rawDouble X).X j where
  f q := (objectHomotopy (X.obj (op (SimplexCategory.mk q)))).hom i j
  comm' q q' h := by
    change q'+1=q at h
    subst q
    -- evaluate the alternating face sum in each horizontal degree
    let F := HomologicalComplex.eval ZMod c j
    let G := HomologicalComplex.eval ZMod c i
    change _ ≫ F.map (((alternatingFaceMapComplex Ch).obj (X ⋙ horizontalAltZ)).d (q'+1) q') =
      G.map (((alternatingFaceMapComplex Ch).obj (X ⋙ horizontalAltZ)).d (q'+1) q') ≫ _
    rw [alternatingFaceMapComplex_obj_d]
    unfold AlternatingFaceMapComplex.objD
    rw [Functor.map_sum,Functor.map_sum,Preadditive.comp_sum,Preadditive.sum_comp]
    apply Finset.sum_congr rfl
    intro k _
    rw [Functor.map_zsmul,Functor.map_zsmul,Preadditive.comp_zsmul,Preadditive.zsmul_comp]
    congr 1
    change toZModule.map ((AlgebraicTopology.DoldKan.homotopyPInftyToId
      (reducedBar (X.obj (op (SimplexCategory.mk (q'+1)))))).hom i j) ≫
      toZModule.map ((reducedBarFunctor.map (X.δ k)).app (op (SimplexCategory.mk j))) =
      toZModule.map ((reducedBarFunctor.map (X.δ k)).app (op (SimplexCategory.mk i))) ≫
      toZModule.map ((AlgebraicTopology.DoldKan.homotopyPInftyToId
        (reducedBar (X.obj (op (SimplexCategory.mk q'))))).hom i j)
    rw [← Functor.map_comp,← Functor.map_comp]
    exact congrArg (fun k => toZModule.map k) (normalizationHomotopy_natural (reducedBarFunctor.map (X.δ k)) i j).symm

set_option backward.isDefEq.respectTransparency false in
def rawHomotopy (X : SimplicialObject AGrp) : Homotopy (proj X ≫ incl X) (𝟙 _) where
  hom := rowHomotopy X
  zero i j h := by
    apply HomologicalComplex.Hom.ext
    funext q
    change (objectHomotopy (X.obj (op (SimplexCategory.mk q)))).hom i j = 0
    exact (objectHomotopy _).zero i j h
  comm i := by
    apply HomologicalComplex.Hom.ext
    funext q
    let A := X.obj (op (SimplexCategory.mk q))
    have he := (objectHomotopy A).comm i
    change toZModule.map (project A i) ≫ toZModule.map (includeMoore A i) = _
    rw [← Functor.map_comp,project_include]
    cases i with
    | zero =>
      rw [Homotopy.dNext_zero_chainComplex,Homotopy.prevD_chainComplex] at he ⊢
      simp only [zero_add,HomologicalComplex.add_f_apply,HomologicalComplex.comp_f,
        HomologicalComplex.zero_f,HomologicalComplex.id_f,Functor.mapHomologicalComplex_map_f,
        toZModule.map_id] at he ⊢
      exact he
    | succ i =>
      rw [Homotopy.dNext_succ_chainComplex,Homotopy.prevD_chainComplex] at he ⊢
      simp only [HomologicalComplex.add_f_apply,HomologicalComplex.comp_f,
        HomologicalComplex.id_f,Functor.mapHomologicalComplex_map_f,toZModule.map_id] at he ⊢
      exact he

set_option backward.isDefEq.respectTransparency false in
def normalizationEquiv (X : SimplicialObject AGrp) :
    HomotopyEquiv (barTotal X) ((rawDouble X).total c) where
  hom := HomologicalComplex₂.total.map (incl X) c
  inv := HomologicalComplex₂.total.map (proj X) c
  homotopyHomInvId := Homotopy.ofEq (by
    rw [← HomologicalComplex₂.total.map_comp,incl_proj,HomologicalComplex₂.total.map_id]
    rfl)
  homotopyInvHomId := by
    rw [← HomologicalComplex₂.total.map_comp,← HomologicalComplex₂.total.map_id (rawDouble X) c]
    exact liftHomotopy (rawHomotopy X)

#print axioms incl_proj
#print axioms rowHomotopy
#print axioms rawHomotopy
#print axioms normalizationEquiv
end CMDG.CondensedCM5R0.BreenDeligneBarNormalization
