import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBarNormalization
import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberSigned

/-! The reduced bar diagonal and the actual normalized bar total
are compared by the explicit Alexander–Whitney and shuffle equivalence. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BreenDeligneNormalizedBar
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneBarNormalization
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberAW
open CMDG.CondensedCM5R0.EilenbergZilberSigned
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneBarDiagonalComparison

def barBi (X : SimplicialObject AGrp) : Bi :=
  CategoryTheory.Prod.swap _ _ ⋙ Functor.uncurry.obj
    (X ⋙ reducedBarFunctor ⋙ (SimplicialObject.whiskering AGrp ZMod).obj toZModule)

set_option backward.isDefEq.respectTransparency false in
theorem barBi_hor (X : SimplicialObject AGrp) {a b : Δ} (f : a ⟶ b) (q : Δ) :
    (barBi X).map (f ×ₘ 𝟙 q) = toZModule.map ((reducedBar (X.obj q)).map f) := by
  change toZModule.map ((reducedBarFunctor.map (X.map (𝟙 q))).app a) ≫
    toZModule.map ((reducedBar (X.obj q)).map f) = _
  rw [X.map_id,reducedBarFunctor.map_id]
  change toZModule.map (𝟙 _) ≫ _ = _
  rw [toZModule.map_id,Category.id_comp]

set_option backward.isDefEq.respectTransparency false in
theorem barBi_ver (X : SimplicialObject AGrp) {a b : Δ} (f : a ⟶ b) (p : Δ) :
    (barBi X).map (𝟙 p ×ₘ f) = toZModule.map ((reducedBarFunctor.map (X.map f)).app p) := by
  change toZModule.map ((reducedBarFunctor.map (X.map f)).app p) ≫
    toZModule.map ((reducedBar (X.obj b)).map (𝟙 p)) = _
  rw [← Functor.map_comp]
  apply congrArg (fun k => toZModule.map k)
  rw [(reducedBar (X.obj b)).map_id]
  exact Category.comp_id _

set_option backward.isDefEq.respectTransparency false in
theorem raw_hor (X : SimplicialObject AGrp) (p q : ℕ) :
    ((rawDouble X).d (p+1) p).f q = ((double (barBi X)).d (p+1) p).f q := by
  rw [hor_d]
  change toZModule.map (((alternatingFaceMapComplex AGrp).obj (reducedBar (X.obj (d q)))).d (p+1) p) = _
  rw [alternatingFaceMapComplex_obj_d]
  unfold AlternatingFaceMapComplex.objD
  rw [Functor.map_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [Functor.map_zsmul,barBi_hor]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem raw_ver (X : SimplicialObject AGrp) (p q : ℕ) :
    ((rawDouble X).X p).d (q+1) q = ((double (barBi X)).X p).d (q+1) q := by
  rw [ver_d]
  let F := HomologicalComplex.eval ZMod c p
  change F.map (((alternatingFaceMapComplex Ch).obj (X ⋙ horizontalAltZ)).d (q+1) q) = _
  rw [alternatingFaceMapComplex_obj_d]
  unfold AlternatingFaceMapComplex.objD
  rw [Functor.map_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [Functor.map_zsmul,barBi_ver]
  rfl

set_option backward.isDefEq.respectTransparency false in
def rawColumnIso (X : SimplicialObject AGrp) (p : ℕ) :
    (rawDouble X).X p ≅ (double (barBi X)).X p :=
  HomologicalComplex.Hom.isoOfComponents (fun _ => Iso.refl _) (by
    intro i j h
    change j+1=i at h
    subst i
    simp only [Iso.refl_hom,Category.id_comp,Category.comp_id]
    exact (raw_ver X p j).symm)

set_option backward.isDefEq.respectTransparency false in
def rawDoubleIso (X : SimplicialObject AGrp) : rawDouble X ≅ double (barBi X) :=
  HomologicalComplex.Hom.isoOfComponents (rawColumnIso X) (by
    intro i j h
    change j+1=i at h
    subst i
    apply HomologicalComplex.Hom.ext
    funext q
    change 𝟙 _ ≫ ((double (barBi X)).d (j+1) j).f q =
      ((rawDouble X).d (j+1) j).f q ≫ 𝟙 _
    rw [Category.id_comp,Category.comp_id,raw_hor])

set_option backward.isDefEq.respectTransparency false in
def barDiagIso (X : SimplicialObject AGrp) :
    barDiagonal X ⋙ reducedFree ⋙ toZModule ≅ diagonal (barBi X) :=
  NatIso.ofComponents (fun _ => Iso.refl _) (by
    intro a b f
    simp only [Iso.refl_hom,Category.id_comp,Category.comp_id]
    change toZModule.map (reducedFree.map ((barNat (X.map f)).app a ≫ (bar (X.obj b)).map f)) =
      toZModule.map (reducedFree.map ((barNat (X.map f)).app a)) ≫
        toZModule.map (reducedFree.map ((bar (X.obj b)).map f))
    rw [Functor.map_comp,Functor.map_comp])

def diagonalComparison (X : SimplicialObject AGrp) :
    HomotopyEquiv (diagonalReducedChains X) (barTotal X) :=
  (HomotopyEquiv.ofIso ((alternatingFaceMapComplex ZMod).mapIso (barDiagIso X))).trans
    ((signedEquiv (barBi X)).trans
      ((HomotopyEquiv.ofIso (HomologicalComplex₂.total.mapIso (rawDoubleIso X).symm c)).trans
        (normalizationEquiv X).symm))

#print axioms rawDoubleIso
#print axioms barDiagIso
#print axioms diagonalComparison
end CMDG.CondensedCM5R0.BreenDeligneBarDiagonalComparison
