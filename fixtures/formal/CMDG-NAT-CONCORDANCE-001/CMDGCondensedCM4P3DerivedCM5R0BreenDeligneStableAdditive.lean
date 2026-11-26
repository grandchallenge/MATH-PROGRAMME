import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCrossEffect
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneReducedNext

/-! Stable reduced homology is additive, by annihilation of its quadratic
cross effect. No finite-free restriction is required. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.BreenDeligneTensorComparison
open CMDG.CondensedCM5R0.BreenDeligneCrossEffect
namespace CMDG.CondensedCM5R0.BreenDeligneStableAdditive

abbrev red (X : SimplicialObject AGrp) := X ⋙ R
abbrev T (X : SimplicialObject AGrp) := diagonal (external (red X) (red X))
abbrev K := alternatingFaceMapComplex ZMod

def qNat (X : SimplicialObject AGrp) : red X ⟶ T X where
  app a := quadratic (X.obj a)
  naturality {_ _} f := quadratic_natural (X.map f)

def cNat (X : SimplicialObject AGrp) : T X ⟶ red X where
  app a := cross (X.obj a)
  naturality {_ _} f := cross_natural (X.map f)

def redMap {X Y : SimplicialObject AGrp} (f : X ⟶ Y) : red X ⟶ red Y :=
  Functor.whiskerRight f R

def mixed {X Y : SimplicialObject AGrp} (f g : X ⟶ Y) : T X ⟶ T Y where
  app a := R.map (f.app a) ⊗ₘ R.map (g.app a)
  naturality {_ _} h := by
    change (R.map (X.map h) ⊗ₘ R.map (X.map h)) ≫
      (R.map (f.app _) ⊗ₘ R.map (g.app _)) =
      (R.map (f.app _) ⊗ₘ R.map (g.app _)) ≫
      (R.map (Y.map h) ⊗ₘ R.map (Y.map h))
    rw [tensorHom_comp_tensorHom,tensorHom_comp_tensorHom,← R.map_comp,← R.map_comp,
      ← R.map_comp,← R.map_comp,f.naturality,g.naturality]

theorem redDefect {X Y : SimplicialObject AGrp} (f g : X ⟶ Y) :
    redMap (f+g)-redMap f-redMap g = qNat X ≫ mixed f g ≫ cNat Y := by
  apply NatTrans.ext
  funext a
  change R.map (f.app a + g.app a) - R.map (f.app a) - R.map (g.app a) = _
  exact additive_defect (f.app a) (g.app a)

theorem chainDefect {X Y : SimplicialObject AGrp} (f g : X ⟶ Y) :
    K.map (redMap (f+g))-K.map (redMap f)-K.map (redMap g) =
      K.map (qNat X) ≫ K.map (mixed f g) ≫ K.map (cNat Y) := by
  rw [← K.map_sub,← K.map_sub,redDefect,K.map_comp,K.map_comp]

def redFunctor : SimplicialObject AGrp ⥤ Ch :=
  (SimplicialObject.whiskering AGrp ZMod).obj R ⋙ K

theorem tensorHomologyZero (X : SimplicialObject AGrp) (n j : ℕ)
    (hs : SupportedFrom (K.obj (red X)) n) (hj : j<2*n) :
    IsZero ((K.obj (T X)).homology j) := by
  have hz := tensor_supported _ _ n n hs hs j (by omega)
  exact IsZero.of_iso (ShortComplex.isZero_homology_of_isZero_X₂ _ hz)
    ((externalComparison (red X) (red X)).toHomologyIso j)

set_option backward.isDefEq.respectTransparency false in
theorem homologyAdd {X Y : SimplicialObject AGrp} (f g : X ⟶ Y) (n j : ℕ)
    (hs : SupportedFrom (K.obj (red X)) n) (hj : j<2*n) :
    HomologicalComplex.homologyMap (K.map (redMap (f+g))) j =
      HomologicalComplex.homologyMap (K.map (redMap f)) j +
      HomologicalComplex.homologyMap (K.map (redMap g)) j := by
  let H := HomologicalComplex.homologyFunctor ZMod c j
  have h := congrArg H.map (chainDefect f g)
  rw [H.map_sub,H.map_sub,H.map_comp,H.map_comp] at h
  have hz := tensorHomologyZero X n j hs hj
  have he : H.map (K.map (qNat X)) = 0 := hz.eq_of_tgt _ _
  rw [he,zero_comp] at h
  change H.map (K.map (redMap (f+g))) = H.map (K.map (redMap f)) + H.map (K.map (redMap g))
  exact sub_eq_zero.mp (by simpa only [sub_add_eq_sub_sub] using h)

def stableFunctor (n k : ℕ) : AGrp ⥤ ZMod :=
  em n ⋙ redFunctor ⋙ HomologicalComplex.homologyFunctor ZMod c (n+k)

set_option backward.isDefEq.respectTransparency false in
theorem stableFunctor_additive (n k : ℕ) (hk : k<n) :
    (stableFunctor n k).Additive where
  map_add {A B} f g := by
    change HomologicalComplex.homologyMap
      (K.map (redMap ((em n).map (f+g)))) (n+k) = _
    have he : (em n).map (f+g) = (em n).map f + (em n).map g := by
      apply NatTrans.ext
      funext a
      obtain ⟨m,rfl⟩ : ∃ m : ℕ, op (SimplexCategory.mk m) = a := ⟨a.unop.len, by cases a; rfl⟩
      have h := (emDegreeIso n m).hom.naturality (f+g)
      have h₁ := (emDegreeIso n m).hom.naturality f
      have h₂ := (emDegreeIso n m).hom.naturality g
      have hp : (activePower n m).map (f+g) = (activePower n m).map f + (activePower n m).map g := by
        apply Sigma.hom_ext
        intro i
        simp [activePower,Preadditive.comp_add,Preadditive.add_comp]
      apply (cancel_epi ((emDegreeIso n m).hom.app A)).mp
      change _ ≫ (emDegree n m).map (f+g) = _ ≫ ((emDegree n m).map f + (emDegree n m).map g)
      rw [← h,hp,Preadditive.add_comp,h₁,h₂,Preadditive.comp_add]
    rw [he]
    apply homologyAdd _ _ n _ _ (by omega)
    intro m hm
    exact toZModule.map_isZero (reducedEMChains_below A n m hm)

#print axioms homologyAdd
#print axioms stableFunctor_additive
end CMDG.CondensedCM5R0.BreenDeligneStableAdditive
