import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneNormalizationNaturality

/-! Horizontal normalization of an arbitrary simplicial-group-valued diagram,
including its natural contraction and totalized homotopies. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneNormalizedBar
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
open CMDG.CondensedCM5R0.BreenDeligneNormalizationNaturality
namespace CMDG.CondensedCM5R0.BreenDeligneDiagramNormalization

variable (R : AGrp ⥤ SimplicialObject AGrp)

def horizontalMooreZ : AGrp ⥤ Ch := R ⋙ normalizedMooreComplex AGrp ⋙ toZModule.mapHomologicalComplex c

def normDouble (X : SimplicialObject AGrp) : BC :=
  HomologicalComplex₂.flip ((alternatingFaceMapComplex Ch).obj (X ⋙ horizontalMooreZ R))

def horizontalAltZ : AGrp ⥤ Ch :=
  R ⋙ alternatingFaceMapComplex AGrp ⋙ toZModule.mapHomologicalComplex c

def rawDouble (X : SimplicialObject AGrp) : BC :=
  HomologicalComplex₂.flip ((alternatingFaceMapComplex Ch).obj (X ⋙ horizontalAltZ R))

def inclNat : horizontalMooreZ R ⟶ horizontalAltZ R :=
  Functor.whiskerRight (Functor.whiskerLeft R (inclusionOfMooreComplex AGrp))
    (toZModule.mapHomologicalComplex c)

def projNat : horizontalAltZ R ⟶ horizontalMooreZ R :=
  Functor.whiskerRight (Functor.whiskerLeft R ({
    app := AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex
    naturality := fun _ _ f => AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex_naturality f
  } : alternatingFaceMapComplex AGrp ⟶ normalizedMooreComplex AGrp)) (toZModule.mapHomologicalComplex c)

def incl (X : SimplicialObject AGrp) : normDouble R X ⟶ rawDouble R X :=
  (HomologicalComplex₂.flipFunctor ZMod c c).map
    ((alternatingFaceMapComplex Ch).map (Functor.whiskerLeft X (inclNat R)))

def proj (X : SimplicialObject AGrp) : rawDouble R X ⟶ normDouble R X :=
  (HomologicalComplex₂.flipFunctor ZMod c c).map
    ((alternatingFaceMapComplex Ch).map (Functor.whiskerLeft X (projNat R)))

set_option backward.isDefEq.respectTransparency false in
theorem incl_proj (X : SimplicialObject AGrp) : incl R X ≫ proj R X = 𝟙 _ := by
  apply HomologicalComplex.Hom.ext
  funext p
  apply HomologicalComplex.Hom.ext
  funext q
  change toZModule.map ((inclusionOfMooreComplexMap (R.obj (X.obj (op (SimplexCategory.mk q))))).f p) ≫
    toZModule.map ((AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex (R.obj (X.obj (op (SimplexCategory.mk q))))).f p) = 𝟙 _
  rw [← Functor.map_comp]
  have h := congrArg (fun k => k.f p) (AlgebraicTopology.DoldKan.splitMonoInclusionOfMooreComplexMap (R.obj (X.obj (op (SimplexCategory.mk q))))).id
  change (inclusionOfMooreComplexMap (R.obj (X.obj (op (SimplexCategory.mk q))))).f p ≫
    (AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex (R.obj (X.obj (op (SimplexCategory.mk q))))).f p = 𝟙 _ at h
  exact (congrArg (fun k => toZModule.map k) h).trans (toZModule.map_id _)

def objectHomotopy (A : AGrp) :=
  toZModule.mapHomotopy (AlgebraicTopology.DoldKan.homotopyPInftyToId (R.obj A))

set_option backward.isDefEq.respectTransparency false in
def rowHomotopy (X : SimplicialObject AGrp) (i j : ℕ) :
    (rawDouble R X).X i ⟶ (rawDouble R X).X j where
  f q := (objectHomotopy R (X.obj (op (SimplexCategory.mk q)))).hom i j
  comm' q q' h := by
    change q'+1=q at h
    subst q
    -- evaluate the alternating face sum in each horizontal degree
    let F := HomologicalComplex.eval ZMod c j
    let G := HomologicalComplex.eval ZMod c i
    change _ ≫ F.map (((alternatingFaceMapComplex Ch).obj (X ⋙ horizontalAltZ R)).d (q'+1) q') =
      G.map (((alternatingFaceMapComplex Ch).obj (X ⋙ horizontalAltZ R)).d (q'+1) q') ≫ _
    rw [alternatingFaceMapComplex_obj_d]
    unfold AlternatingFaceMapComplex.objD
    rw [Functor.map_sum,Functor.map_sum,Preadditive.comp_sum,Preadditive.sum_comp]
    apply Finset.sum_congr rfl
    intro k _
    rw [Functor.map_zsmul,Functor.map_zsmul,Preadditive.comp_zsmul,Preadditive.zsmul_comp]
    congr 1
    change toZModule.map ((AlgebraicTopology.DoldKan.homotopyPInftyToId
      (R.obj (X.obj (op (SimplexCategory.mk (q'+1)))))).hom i j) ≫
      toZModule.map ((R.map (X.δ k)).app (op (SimplexCategory.mk j))) =
      toZModule.map ((R.map (X.δ k)).app (op (SimplexCategory.mk i))) ≫
      toZModule.map ((AlgebraicTopology.DoldKan.homotopyPInftyToId
        (R.obj (X.obj (op (SimplexCategory.mk q'))))).hom i j)
    rw [← Functor.map_comp,← Functor.map_comp]
    exact congrArg (fun k => toZModule.map k) (normalizationHomotopy_natural (R.map (X.δ k)) i j).symm

set_option backward.isDefEq.respectTransparency false in
def rawHomotopy (X : SimplicialObject AGrp) : Homotopy (proj R X ≫ incl R X) (𝟙 _) where
  hom := rowHomotopy R X
  zero i j h := by
    apply HomologicalComplex.Hom.ext
    funext q
    change (objectHomotopy R (X.obj (op (SimplexCategory.mk q)))).hom i j = 0
    exact (objectHomotopy R _).zero i j h
  comm i := by
    apply HomologicalComplex.Hom.ext
    funext q
    let A := X.obj (op (SimplexCategory.mk q))
    have he := (objectHomotopy R A).comm i
    change toZModule.map ((AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex (R.obj A)).f i) ≫ toZModule.map ((inclusionOfMooreComplexMap (R.obj A)).f i) = _
    rw [← Functor.map_comp]
    have h := congrArg (fun k : (alternatingFaceMapComplex AGrp).obj (R.obj A) ⟶ _ => k.f i) (AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex_comp_inclusionOfMooreComplexMap (R.obj A))
    change _ ≫ _ = _ at h
    rw [h]
    cases i with
    | zero =>
      rw [Homotopy.dNext_zero_chainComplex,Homotopy.prevD_chainComplex] at he ⊢
      simp only [zero_add,HomologicalComplex.add_f_apply,HomologicalComplex.comp_f,
        HomologicalComplex.id_f,Functor.mapHomologicalComplex_map_f,
        toZModule.map_id] at he ⊢
      exact he
    | succ i =>
      rw [Homotopy.dNext_succ_chainComplex,Homotopy.prevD_chainComplex] at he ⊢
      simp only [HomologicalComplex.add_f_apply,HomologicalComplex.comp_f,
        HomologicalComplex.id_f,Functor.mapHomologicalComplex_map_f,toZModule.map_id] at he ⊢
      exact he

set_option backward.isDefEq.respectTransparency false in
def normalizationEquiv (X : SimplicialObject AGrp) :
    HomotopyEquiv (((normDouble R X).total c)) ((rawDouble R X).total c) where
  hom := HomologicalComplex₂.total.map (incl R X) c
  inv := HomologicalComplex₂.total.map (proj R X) c
  homotopyHomInvId := Homotopy.ofEq (by
    rw [← HomologicalComplex₂.total.map_comp,incl_proj,HomologicalComplex₂.total.map_id]
    )
  homotopyInvHomId := by
    rw [← HomologicalComplex₂.total.map_comp,← HomologicalComplex₂.total.map_id (rawDouble R X) c]
    exact liftHomotopy (rawHomotopy R X)

#print axioms incl_proj
#print axioms rowHomotopy
#print axioms rawHomotopy
#print axioms normalizationEquiv
end CMDG.CondensedCM5R0.BreenDeligneDiagramNormalization
