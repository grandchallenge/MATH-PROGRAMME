import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntegerVertices

/-! Integer-line paths are finite signed chains of consecutive edges.
The path coefficients telescope and are translation invariant. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneIntegerVertices
namespace CMDG.CondensedCM5R0.BreenDeligneIntegerLine

def cut (b k : ℤ) : ℤ := if k < b then 1 else 0

def path (a b : ℤ) : ℤ →₀ ℤ :=
  Finsupp.onFinset ((Finset.range (max a b - min a b).toNat).image
    (fun i : ℕ => min a b + (i : ℤ))) (fun k => cut b k - cut a k) (by
    intro k hk
    have h : min a b ≤ k ∧ k < max a b := by
      unfold cut at hk
      split at hk <;> split at hk <;> omega
    refine Finset.mem_image.mpr ⟨(k-min a b).toNat, Finset.mem_range.mpr ?_,?_⟩
    · omega
    · omega)

theorem path_apply (a b k : ℤ) : path a b k = cut b k - cut a k := rfl

theorem path_add (a b c : ℤ) : path a b + path b c = path a c := by
  ext k
  simp only [Finsupp.add_apply,path_apply]
  abel

theorem path_self (a : ℤ) : path a a = 0 := by
  ext k
  simp [path_apply]

theorem path_step (a : ℤ) : path a (a+1) = Finsupp.single a 1 := by
  ext k
  rw [path_apply,Finsupp.single_apply]
  unfold cut
  split <;> split <;> split <;> omega

theorem path_shift (a b c : ℤ) :
    Finsupp.mapDomain (fun k : ℤ => c+k) (path a b) = path (c+a) (c+b) := by
  ext k
  have h : k=c+(k-c) := by omega
  conv_lhs => rw [h]
  rw [Finsupp.mapDomain_apply (fun x y he => by omega),path_apply,path_apply]
  unfold cut
  split <;> split <;> split <;> split <;> omega

def pair (a b : ℤ) : Vtx 1 := Fin.cons (α := fun _ => ℤ) a (fun _ => b)
def vertex (a : ℤ) : Vtx 0 := fun _ => a

def edgeLift : (ModuleCat.free ℤ).obj ℤ ⟶ V 1 :=
  (ModuleCat.free ℤ).map (↾fun k => pair k (k+1))

def linePath (a b : ℤ) : V 1 := edgeLift (path a b)

theorem linePath_add (a b c : ℤ) : linePath a b + linePath b c = linePath a c := by
  unfold linePath
  rw [← map_add]
  exact congrArg edgeLift (path_add a b c)

theorem linePath_self (a : ℤ) : linePath a a = 0 := by
  unfold linePath
  rw [path_self,map_zero]

theorem linePath_step (a : ℤ) : linePath a (a+1) = gen (pair a (a+1)) := by
  unfold linePath
  rw [path_step]
  exact ModuleCat.free_map_apply _ _

theorem edge_boundary (a b : ℤ) : D 0 (gen (pair a b)) = gen (vertex b) - gen (vertex a) := by
  rw [D_gen,Fin.sum_univ_two]
  simp only [Fin.val_zero,pow_zero,one_smul,Fin.val_one,pow_one,neg_one_zsmul]
  have h0 : (0 : Fin 2).removeNth (pair a b) = vertex b := by
    funext i
    have hi : i = 0 := Subsingleton.elim _ _
    subst i
    rfl
  have h1 : (1 : Fin 2).removeNth (pair a b) = vertex a := by
    funext i
    have hi : i = 0 := Subsingleton.elim _ _
    subst i
    rfl
  rw [h0,h1,sub_eq_add_neg]

set_option maxHeartbeats 1000000 in
theorem linePath_boundary (a b : ℤ) :
    D 0 (linePath a b) = gen (vertex b) - gen (vertex a) := by
  let P : ℤ → Prop := fun k => D 0 (linePath a k) = gen (vertex k) - gen (vertex a)
  have h₀ : P a := by simp [P,linePath_self]
  have hs (k : ℤ) : P k ↔ P (k+1) := by
    have h := congrArg (D 0) (linePath_add a k (k+1))
    rw [map_add,linePath_step,edge_boundary] at h
    dsimp [P]
    constructor
    · intro he
      rw [he] at h
      rw [← h]
      abel
    · intro he
      rw [he] at h
      exact add_right_cancel (show D 0 (linePath a k) + (gen (vertex (k+1)) - gen (vertex k)) =
        (gen (vertex k) - gen (vertex a)) + (gen (vertex (k+1)) - gen (vertex k)) by
          rw [h]; abel)
  have H (k : ℤ) : P (a+k) := by
    induction k using Int.induction_on with
    | zero => simpa only [add_zero] using h₀
    | succ k hk =>
      rw [← add_assoc]
      exact (hs (a+k)).mp hk
    | pred k hk =>
      rw [← sub_eq_add_neg,← add_sub_assoc] at *
      apply (hs (a + -(k : ℤ) - 1)).mpr
      rw [show a + -(k : ℤ) - 1 + 1 = a - (k : ℤ) by omega]
      exact hk
  have he : a+(b-a)=b := by omega
  exact he ▸ H (b-a)


theorem linePath_shift (a b c : ℤ) :
    T c 1 (linePath a b) = linePath (c+a) (c+b) := by
  let t : (ModuleCat.free ℤ).obj ℤ ⟶ (ModuleCat.free ℤ).obj ℤ :=
    (ModuleCat.free ℤ).map (↾fun k => c+k)
  have h : edgeLift ≫ T c 1 = t ≫ edgeLift := by
    apply ModuleCat.free_hom_ext
    intro k
    change T c 1 (edgeLift (ModuleCat.freeMk k)) = edgeLift (t (ModuleCat.freeMk k))
    unfold edgeLift t
    rw [ModuleCat.free_map_apply,ModuleCat.free_map_apply,T_gen,ModuleCat.free_map_apply]
    congr 1
    funext i
    refine Fin.cases ?_ (fun j => ?_) i
    · rfl
    · have hj : j=0 := Subsingleton.elim _ _
      subst j
      simp [tr,pair,add_assoc]
  have he := CategoryTheory.congr_fun h (path a b)
  change T c 1 (linePath a b) = edgeLift (Finsupp.mapDomain (fun k => c+k) (path a b)) at he
  rw [he,path_shift]
  rfl

#print axioms linePath_boundary
#print axioms linePath_shift
end CMDG.CondensedCM5R0.BreenDeligneIntegerLine
