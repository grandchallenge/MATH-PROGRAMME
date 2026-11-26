import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntervalLift
import Mathlib.AlgebraicTopology.SimplexCategory.ToMkOne
import Mathlib.AlgebraicTopology.SimplicialObject.ChainHomotopy

/-! The prism homotopy in the actual linear simplicial cylinder. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.BreenDeligneInterval
open CMDG.CondensedCM5R0.BreenDeligneIntervalLift
namespace CMDG.CondensedCM5R0.BreenDeligneIntervalPrism

def step {n : ℕ} (i : Fin (n+1)) : I (d (n+1)) :=
  SimplexCategory.toMk₁ i.succ.castSucc

def prism (X : SimplicialObject ZMod) {n : ℕ} (i : Fin (n+1)) :
    X.obj (d n) ⟶ (cyl X).obj (d (n+1)) :=
  X.σ i ≫ inj X (d (n+1)) (d (n+1)) (step i)

set_option backward.isDefEq.respectTransparency false in
theorem prism_face (X : SimplicialObject ZMod) {n : ℕ}
    (i : Fin (n+1)) (j : Fin (n+2)) :
    prism X i ≫ (cyl X).δ j =
      X.σ i ≫ X.δ j ≫ inj X (d n) (d n) (SimplexCategory.δ j ≫ step i) := by
  unfold prism
  rw [Category.assoc]
  change X.σ i ≫ (inj X _ _ _ ≫ (cylinderBi X).map ((SimplexCategory.δ j).op ×ₘ (SimplexCategory.δ j).op)) = _
  rw [inj_map]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem prism_degeneracy (X : SimplicialObject ZMod) {n : ℕ}
    (i : Fin (n+1)) (j : Fin (n+2)) :
    prism X i ≫ (cyl X).σ j =
      X.σ i ≫ X.σ j ≫ inj X (d (n+2)) (d (n+2)) (SimplexCategory.σ j ≫ step i) := by
  unfold prism
  rw [Category.assoc]
  change X.σ i ≫ (inj X _ _ _ ≫ (cylinderBi X).map ((SimplexCategory.σ j).op ×ₘ (SimplexCategory.σ j).op)) = _
  rw [inj_map]
  rfl

theorem step_first (n : ℕ) :
    SimplexCategory.δ (0 : Fin (n+2)) ≫ step (0 : Fin (n+1)) = vertex (d n) 1 := by
  unfold step
  rw [SimplexCategory.δ_comp_toMk₁_of_lt _ _ (by simp)]
  apply SimplexCategory.Hom.ext
  apply OrderHom.ext
  funext k
  change SimplexCategory.toMk₁ _ k = 1
  apply SimplexCategory.toMk₁_of_le_castSucc
  simp

theorem step_last (n : ℕ) :
    SimplexCategory.δ (Fin.last (n+1)) ≫ step (Fin.last n) = vertex (d n) 0 := by
  unfold step
  rw [SimplexCategory.δ_comp_toMk₁_of_le _ _ (by simp [Fin.succ_last])]
  apply SimplexCategory.Hom.ext
  apply OrderHom.ext
  funext k
  change SimplexCategory.toMk₁ _ k = 0
  apply SimplexCategory.toMk₁_of_castSucc_lt
  apply Fin.lt_def.mpr
  simp
  omega

theorem step_face_left {n : ℕ} (i : Fin (n+2)) (j : Fin (n+1))
    (h : i ≤ j.castSucc) :
    SimplexCategory.δ i.castSucc ≫ step j.succ = step j := by
  change i.val ≤ j.val at h
  unfold step
  rw [SimplexCategory.δ_comp_toMk₁_of_lt _ _ (by
    change i.val < j.val+2
    omega)]
  congr 1

theorem step_face_right {n : ℕ} (i : Fin (n+2)) (j : Fin (n+1))
    (h : j.castSucc < i) :
    SimplexCategory.δ i.succ ≫ step j.castSucc = step j := by
  change j.val < i.val at h
  unfold step
  rw [SimplexCategory.δ_comp_toMk₁_of_le _ _ (by
    change j.val+1 ≤ i.val+1
    omega)]
  congr 1

theorem step_face_middle {n : ℕ} (j : Fin (n+1)) :
    SimplexCategory.δ j.castSucc.succ ≫ step j.succ =
      SimplexCategory.δ j.castSucc.succ ≫ step j.castSucc := by
  unfold step
  rw [SimplexCategory.δ_comp_toMk₁_of_lt _ _ (by
    change j.val+1 < j.val+2
    omega),
    SimplexCategory.δ_comp_toMk₁_of_le _ _ (by
    change j.val+1 ≤ j.val+1
    omega)]
  congr 1

theorem step_deg_left {n : ℕ} (i j : Fin (n+1)) (h : i ≤ j) :
    SimplexCategory.σ i.castSucc ≫ step j = step j.succ := by
  unfold step
  rw [SimplexCategory.σ_comp_toMk₁_of_lt _ _ (by
    change i.val < j.val+1
    omega)]
  congr 1

theorem step_deg_right {n : ℕ} (i j : Fin (n+1)) (h : j ≤ i) :
    SimplexCategory.σ i.succ ≫ step j = step j.castSucc := by
  unfold step
  rw [SimplexCategory.σ_comp_toMk₁_of_le _ _ (by
    change j.val+1 ≤ i.val+1
    omega)]
  congr 1

set_option backward.isDefEq.respectTransparency false in
def prismHomotopy (X : SimplicialObject ZMod) :
    SimplicialObject.Homotopy (endpoint X 0) (endpoint X 1) where
  h i := prism X i
  h_zero_comp_δ_zero n := by
    rw [prism_face,step_first,← Category.assoc]
    have he := X.δ_comp_σ_self (i := (0 : Fin (n+1)))
    change X.σ 0 ≫ X.δ 0 = 𝟙 _ at he
    rw [he,Category.id_comp]
    rfl
  h_last_comp_δ_last n := by
    rw [prism_face,step_last,← Category.assoc]
    have he := X.δ_comp_σ_succ (i := Fin.last n)
    rw [Fin.succ_last] at he
    rw [he,Category.id_comp]
    rfl
  h_succ_comp_δ_castSucc_of_lt i j h := by
    rw [prism_face,step_face_left i j h,← Category.assoc,X.δ_comp_σ_of_le h,Category.assoc]
    rfl
  h_succ_comp_δ_castSucc_succ j := by
    rw [prism_face,prism_face,step_face_middle,← Category.assoc,← Category.assoc]
    rw [← Fin.castSucc_succ,X.δ_comp_σ_self,Fin.castSucc_succ,X.δ_comp_σ_succ]
  h_castSucc_comp_δ_succ_of_lt i j h := by
    rw [prism_face,step_face_right i j h,← Category.assoc,X.δ_comp_σ_of_gt h,Category.assoc]
    rfl
  h_comp_σ_castSucc_of_le i j h := by
    rw [prism_degeneracy,step_deg_left i j h,← Category.assoc,X.σ_comp_σ h,Category.assoc]
    rfl
  h_comp_σ_succ_of_lt i j h := by
    rw [prism_degeneracy,step_deg_right i j h,← Category.assoc,← X.σ_comp_σ h,Category.assoc]
    rfl

def simplicialFromAlternating {X Y : SimplicialObject ZMod} {f g : X ⟶ Y}
    (H : Homotopy (K.map f) (K.map g)) : SimplicialObject.Homotopy f g := by
  have h := (prismHomotopy X).postcomp (cylinderMap H)
  rw [cylinder_endpoint H 0,cylinder_endpoint H 1] at h
  simpa using h

#print axioms prismHomotopy
#print axioms simplicialFromAlternating
end CMDG.CondensedCM5R0.BreenDeligneIntervalPrism
