import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRankOneBar
import Mathlib.Algebra.Category.ModuleCat.Adjunctions

/-! Homogeneous vertex tuples for the integer bar, with actual
alternating deletion and translation-equivariant cone identities. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBarObject
namespace CMDG.CondensedCM5R0.BreenDeligneIntegerVertices

abbrev Vtx (n : ℕ) := Fin (n+1) → ℤ
def vertices : SimplicialObject (Type 0) where
  obj Δ := Fin (Δ.unop.len+1) → ℤ
  map f := ↾fun x => x ∘ f.unop.toOrderHom
  map_id _ := rfl
  map_comp _ _ := rfl

abbrev V (n : ℕ) := (ModuleCat.free ℤ).obj (Vtx n)
abbrev gen {n : ℕ} (v : Vtx n) : V n := ModuleCat.freeMk v
abbrev D (n : ℕ) : V (n+1) ⟶ V n :=
  AlternatingFaceMapComplex.objD (vertices ⋙ ModuleCat.free ℤ) n

theorem D_gen (n : ℕ) (v : Vtx (n+1)) :
    D n (gen v) = ∑ i : Fin (n+2), (-1 : ℤ)^i.val • gen (i.removeNth v) := by
  simp only [D,AlternatingFaceMapComplex.objD,ModuleCat.hom_sum,LinearMap.sum_apply]
  apply Finset.sum_congr rfl
  intro i _
  change (-1 : ℤ)^i.val • ((ModuleCat.free ℤ).map (↾fun x : Vtx (n+1) =>
    i.removeNth x) (gen v)) = _
  rw [ModuleCat.free_map_apply]
  rfl

theorem D_sq (n : ℕ) : D (n+1) ≫ D n = 0 :=
  AlternatingFaceMapComplex.d_squared (vertices ⋙ ModuleCat.free ℤ) n

def tr (a : ℤ) {n : ℕ} (v : Vtx n) : Vtx n := fun i => a + v i
def T (a : ℤ) (n : ℕ) : V n ⟶ V n :=
  (ModuleCat.free ℤ).map (↾tr a)
theorem T_gen (a : ℤ) (n : ℕ) (v : Vtx n) : T a n (gen v) = gen (tr a v) :=
  ModuleCat.free_map_apply _ _
theorem T_D (a : ℤ) (n : ℕ) : T a (n+1) ≫ D n = D n ≫ T a n := by
  apply ModuleCat.free_hom_ext
  intro v
  change D n (T a (n+1) (gen v)) = T a n (D n (gen v))
  rw [T_gen,D_gen,D_gen,map_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [map_smul,T_gen]
  rfl

def cone (a : ℤ) (n : ℕ) : V n ⟶ V (n+1) :=
  (ModuleCat.free ℤ).map (↾fun v : Vtx n => (Fin.cons (α := fun _ => ℤ) a v : Vtx (n+1)))
theorem cone_gen (a : ℤ) (n : ℕ) (v : Vtx n) :
    cone a n (gen v) = gen (Fin.cons (α := fun _ => ℤ) a v) := ModuleCat.free_map_apply _ _

theorem cone_equiv (a b : ℤ) (n : ℕ) :
    cone a n ≫ T b (n+1) = T b n ≫ cone (b+a) n := by
  apply ModuleCat.free_hom_ext
  intro v
  change T b (n+1) (cone a n (gen v)) = cone (b+a) n (T b n (gen v))
  rw [cone_gen,T_gen,T_gen,cone_gen]
  congr 1
  funext i
  refine Fin.cases ?_ (fun j => ?_) i
  · simp [tr]
  · simp [tr]

theorem remove_cons_zero (n : ℕ) (a : ℤ) (v : Vtx n) :
    (0 : Fin (n+2)).removeNth (Fin.cons (α := fun _ => ℤ) a v) = v := by
  funext i
  simp [Fin.removeNth]

theorem remove_cons_succ (n : ℕ) (a : ℤ) (v : Vtx (n+1)) (i : Fin (n+2)) :
    i.succ.removeNth (Fin.cons (α := fun _ => ℤ) a v) = Fin.cons (α := fun _ => ℤ) a (i.removeNth v) := by
  funext j
  refine Fin.cases ?_ (fun k => ?_) j
  · simp [Fin.removeNth]
  · simp [Fin.removeNth,Fin.succ_succAbove_succ]

theorem cone_identity (a : ℤ) (n : ℕ) :
    cone a (n+1) ≫ D (n+1) + D n ≫ cone a n = 𝟙 _ := by
  apply ModuleCat.free_hom_ext
  intro v
  change D (n+1) (cone a (n+1) (gen v)) + cone a n (D n (gen v)) = gen v
  rw [cone_gen,D_gen,D_gen,map_sum,Fin.sum_univ_succ]
  simp only [Fin.val_zero,pow_zero,one_smul,remove_cons_zero,Fin.val_succ,pow_succ,
    mul_neg,mul_one,neg_smul,map_smul,cone_gen,remove_cons_succ,Finset.sum_neg_distrib]
  abel

#print axioms cone_identity
#print axioms cone_equiv
end CMDG.CondensedCM5R0.BreenDeligneIntegerVertices
