import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberSigned

/-! The signed Eilenberg–Zilber comparison on external tensor products of
actual simplicial integer modules. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberAW
open CMDG.CondensedCM5R0.EilenbergZilberSigned
namespace CMDG.CondensedCM5R0.BreenDeligneTensorComparison

abbrev S := SimplicialObject ZMod
abbrev C (X : S) : Ch := (alternatingFaceMapComplex ZMod).obj X

def external (X Y : S) : Bi where
  obj t := X.obj t.1 ⊗ Y.obj t.2
  map f := X.map f.1 ⊗ₘ Y.map f.2
  map_id t := by simp
  map_comp f g := by simp [tensorHom_comp_tensorHom]

abbrev tensorDouble (K L : Ch) : HomologicalComplex₂ ZMod c c :=
  (((curriedTensor ZMod).mapBifunctorHomologicalComplex c c).obj K).obj L

set_option backward.isDefEq.respectTransparency false in
theorem external_vertical (X Y : S) (p q : ℕ) :
    ((double (external X Y)).X p).d (q+1) q =
      ((tensorDouble (C X) (C Y)).X p).d (q+1) q := by
  rw [ver_d,Functor.mapBifunctorHomologicalComplex_obj_obj_X_d]
  change (∑ i : Fin (q+2), (-1 : ℤ)^i.val •
    (X.map (𝟙 (d p)) ⊗ₘ Y.map (SimplexCategory.δ i).op)) =
      ((curriedTensor ZMod).obj (X.obj (d p))).map ((C Y).d (q+1) q)
  rw [alternatingFaceMapComplex_obj_d]
  unfold AlternatingFaceMapComplex.objD
  rw [Functor.map_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [Functor.map_zsmul,X.map_id]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem external_horizontal (X Y : S) (p q : ℕ) :
    ((double (external X Y)).d (p+1) p).f q =
      ((tensorDouble (C X) (C Y)).d (p+1) p).f q := by
  rw [hor_d,Functor.mapBifunctorHomologicalComplex_obj_obj_d_f]
  change (∑ i : Fin (p+2), (-1 : ℤ)^i.val •
    (X.map (SimplexCategory.δ i).op ⊗ₘ Y.map (𝟙 (d q)))) =
      ((curriedTensor ZMod).map ((C X).d (p+1) p)).app (Y.obj (d q))
  rw [alternatingFaceMapComplex_obj_d]
  unfold AlternatingFaceMapComplex.objD
  rw [Functor.map_sum]
  let F := (evaluation ZMod ZMod).obj (Y.obj (d q))
  change _ = F.map (∑ i : Fin (p+2), (curriedTensor ZMod).map
    ((-1 : ℤ)^i.val • X.δ i))
  rw [Functor.map_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [Functor.map_zsmul,Functor.map_zsmul,Y.map_id]
  rfl

set_option backward.isDefEq.respectTransparency false in
def externalColumnIso (X Y : S) (p : ℕ) :
    (double (external X Y)).X p ≅ (tensorDouble (C X) (C Y)).X p :=
  HomologicalComplex.Hom.isoOfComponents (fun _ => Iso.refl _) (by
    intro i j h
    change j+1=i at h
    subst i
    simp only [Iso.refl_hom,Category.id_comp,Category.comp_id]
    exact (external_vertical X Y p j).symm)

set_option backward.isDefEq.respectTransparency false in
def externalDoubleIso (X Y : S) :
    double (external X Y) ≅ tensorDouble (C X) (C Y) :=
  HomologicalComplex.Hom.isoOfComponents (externalColumnIso X Y) (by
    intro i j h
    change j+1=i at h
    subst i
    apply HomologicalComplex.Hom.ext
    funext q
    change 𝟙 _ ≫ ((tensorDouble (C X) (C Y)).d (j+1) j).f q =
      ((double (external X Y)).d (j+1) j).f q ≫ 𝟙 _
    rw [Category.id_comp,Category.comp_id,external_horizontal])

def externalComparison (X Y : S) :
    HomotopyEquiv (C (diagonal (external X Y))) (HomologicalComplex.tensorObj (C X) (C Y)) :=
  (signedEquiv (external X Y)).trans
    (HomotopyEquiv.ofIso (HomologicalComplex₂.total.mapIso (externalDoubleIso X Y) c))

#print axioms externalDoubleIso
#print axioms externalComparison
end CMDG.CondensedCM5R0.BreenDeligneTensorComparison
