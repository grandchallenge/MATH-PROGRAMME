import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberTotalSide

/-! The actual degree-zero AW and shuffle maps are inverse. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberModels
open CMDG.CondensedCM5R0.EilenbergZilberNatural
open CMDG.CondensedCM5R0.EilenbergZilberHomotopy
open CMDG.CondensedCM5R0.EilenbergZilberShuffle
namespace CMDG.CondensedCM5R0.EilenbergZilberZero

def emptyPath : Path 0 0 :=
  ⟨(OrderHom.id,OrderHom.id),by intro i; fin_cases i; rfl⟩

instance : Subsingleton (Path 0 0) where
  allEq u v := by
    apply Subtype.ext
    apply Prod.ext <;> apply OrderHom.ext <;> funext i <;> apply Fin.ext <;> omega

theorem pathSign_empty : pathSign emptyPath = 1 := by
  simp [pathSign]

set_option backward.isDefEq.respectTransparency false in
theorem shufflePart_zero (B : Bi) : shufflePart B 0 0 = 𝟙 (B.obj (EilenbergZilberModels.pair 0 0)) := by
  unfold shufflePart
  rw [Finset.sum_eq_single emptyPath]
  · rw [pathSign_empty,one_smul]
    exact B.map_id _
  · intro b _ h
    exact (h (Subsingleton.elim _ _)).elim
  · simp

set_option backward.isDefEq.respectTransparency false in
theorem awDegree_zero (B : Bi) :
    awDegree B 0 = (double B).ιTotal c 0 0 0 rfl := by
  unfold awDegree
  rw [Fin.sum_univ_one]
  unfold awTerm
  have h : (SimplexCategory.subinterval 0 0 (by decide : 0+0≤0) :
    SimplexCategory.mk 0 ⟶ SimplexCategory.mk 0) = 𝟙 _ := by
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext i
    apply Fin.ext
    have ha := ((SimplexCategory.subinterval 0 0 (by decide : 0+0≤0)).toOrderHom i).isLt
    have hb := ((SimplexCategory.Hom.toOrderHom (𝟙 (SimplexCategory.mk 0))) i).isLt
    change _ < 1 at ha hb
    omega
  change B.map ((SimplexCategory.subinterval 0 0 (by decide : 0+0≤0)).op ×ₘ
    (SimplexCategory.subinterval 0 0 (by decide : 0+0≤0)).op) ≫ _ = _
  rw [h]
  change B.map (𝟙 (EilenbergZilberModels.pair 0 0)) ≫ _ = _
  rw [B.map_id,Category.id_comp]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem aw_shuffle_zero (B : Bi) :
    awDegree B 0 ≫ shuffleDegree B 0 = 𝟙 ((D.obj B).X 0) := by
  rw [awDegree_zero,shuffleDegree_summand,shufflePart_zero]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem shuffle_aw_zero (B : Bi) :
    shuffleDegree B 0 ≫ awDegree B 0 = 𝟙 ((Tot.obj B).X 0) := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  change p+q=0 at h
  have hp : p=0 := by omega
  have hq : q=0 := by omega
  subst p
  subst q
  rw [← Category.assoc,shuffleDegree_summand,shufflePart_zero,awDegree_zero]
  change 𝟙 (((double B).X 0).X 0) ≫ (double B).ιTotal c 0 0 0 rfl =
    (double B).ιTotal c 0 0 0 rfl ≫ 𝟙 ((double B).total c |>.X 0)
  rw [Category.id_comp,Category.comp_id]

#print axioms aw_shuffle_zero
#print axioms shuffle_aw_zero
end CMDG.CondensedCM5R0.EilenbergZilberZero
