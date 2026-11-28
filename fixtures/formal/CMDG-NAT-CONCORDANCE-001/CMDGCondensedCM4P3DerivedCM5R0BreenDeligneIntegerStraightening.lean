import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntegerLine

/-! Equivariant straightening onto the two-term oriented line.
The homotopy is built on tuple generators by filling a cycle
with the cone at its first vertex. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneIntegerVertices
open CMDG.CondensedCM5R0.BreenDeligneIntegerLine
namespace CMDG.CondensedCM5R0.BreenDeligneIntegerStraightening

def E : (n : ℕ) → V n ⟶ V n
  | 0 => 𝟙 _
  | 1 => ModuleCat.freeDesc (↾fun v : Vtx 1 => linePath (v 0) (v 1))
  | _+2 => 0

theorem E_one (v : Vtx 1) : E 1 (gen v) = linePath (v 0) (v 1) :=
  ModuleCat.freeDesc_apply _ _

theorem E_D (n : ℕ) : E (n+1) ≫ D n = D n ≫ E n := by
  cases n with
  | zero =>
    apply ModuleCat.free_hom_ext
    intro v
    change D 0 (E 1 (gen v)) = D 0 (gen v)
    rw [E_one,linePath_boundary]
    have hv : v = BreenDeligneIntegerLine.pair (v 0) (v 1) := by
      funext i
      fin_cases i <;> rfl
    conv_rhs => rw [hv,edge_boundary]
  | succ n =>
    cases n with
    | zero =>
      change (0 : V 2 ⟶ V 2) ≫ D 1 = D 1 ≫ E 1
      rw [zero_comp]
      apply ModuleCat.free_hom_ext
      intro v
      change 0 = E 1 (D 1 (gen v))
      rw [D_gen,map_sum,Fin.sum_univ_succ,Fin.sum_univ_two]
      simp only [map_smul,E_one]
      have h0 : ((0 : Fin 3).removeNth v) 0 = v 1 := rfl
      have h1 : ((0 : Fin 3).removeNth v) 1 = v 2 := rfl
      have h2 : ((0 : Fin 2).succ.removeNth v) 0 = v 0 := rfl
      have h3 : ((0 : Fin 2).succ.removeNth v) 1 = v 2 := rfl
      have h4 : ((1 : Fin 2).succ.removeNth v) 0 = v 0 := rfl
      have h5 : ((1 : Fin 2).succ.removeNth v) 1 = v 1 := rfl
      rw [h0,h1,h2,h3,h4,h5]
      simp only [Fin.val_zero,Fin.val_succ,Fin.val_one,pow_zero,pow_one,pow_succ,
        mul_neg,mul_one,neg_mul,neg_neg,one_smul,neg_one_zsmul]
      have he := linePath_add (v 0) (v 1) (v 2)
      rw [← he]
      abel
    | succ n =>
      change (0 : V (n+3) ⟶ V (n+3)) ≫ D (n+2) = D (n+2) ≫ 0
      rw [zero_comp,comp_zero]

theorem E_T (a : ℤ) (n : ℕ) : E n ≫ T a n = T a n ≫ E n := by
  rcases n with _ | (_ | n)
  · exact (Category.id_comp _).trans (Category.comp_id _).symm
  · apply ModuleCat.free_hom_ext
    intro v
    change T a 1 (E 1 (gen v)) = E 1 (T a 1 (gen v))
    rw [E_one,T_gen,E_one,linePath_shift]
    rfl
  · simp [E]

def H : (n : ℕ) → V n ⟶ V (n+1)
  | 0 => 0
  | n+1 => ModuleCat.freeDesc (↾fun v : Vtx (n+1) =>
      cone (v 0) (n+1) (((𝟙 (V (n+1)) - E (n+1) - (D n ≫ H n)) : V (n+1) ⟶ V (n+1)) (gen v)))

def R (n : ℕ) : V (n+1) ⟶ V (n+1) :=
  𝟙 _ - E (n+1) - (D n ≫ H n)

theorem H_gen (n : ℕ) (v : Vtx (n+1)) :
    H (n+1) (gen v) = cone (v 0) (n+1) (R n (gen v)) :=
  ModuleCat.freeDesc_apply _ _

theorem H_identity (n : ℕ) :
    H (n+1) ≫ D (n+1) + D n ≫ H n = 𝟙 _ - E (n+1) := by
  induction n with
  | zero =>
    have hR : R 0 ≫ D 0 = 0 := by
      unfold R
      rw [Preadditive.sub_comp,Preadditive.sub_comp,Category.id_comp,E_D]
      simp [H,E]
    have he : H 1 ≫ D 1 = R 0 := by
      apply ModuleCat.free_hom_ext
      intro v
      change D 1 (H 1 (gen v)) = R 0 (gen v)
      rw [H_gen]
      have h := CategoryTheory.congr_fun (cone_identity (v 0) 0) (R 0 (gen v))
      have hz := CategoryTheory.congr_fun hR (gen v)
      change D 0 (R 0 (gen v)) = 0 at hz
      change D 1 (cone (v 0) 1 (R 0 (gen v))) +
        cone (v 0) 0 (D 0 (R 0 (gen v))) = R 0 (gen v) at h
      rw [hz,map_zero,add_zero] at h
      exact h
    rw [he]
    unfold R
    abel
  | succ n ih =>
    have hR : R (n+1) ≫ D (n+1) = 0 := by
      unfold R
      rw [Preadditive.sub_comp,Preadditive.sub_comp,Category.id_comp,E_D,Category.assoc]
      have hh := congrArg (fun f => D (n+1) ≫ f) ih
      rw [Preadditive.comp_add,Preadditive.comp_sub,Category.comp_id,
        ← Category.assoc (D (n+1)) (D n) (H n), D_sq,zero_comp,add_zero] at hh
      rw [hh]
      abel
    have he : H (n+2) ≫ D (n+2) = R (n+1) := by
      apply ModuleCat.free_hom_ext
      intro v
      change D (n+2) (H (n+2) (gen v)) = R (n+1) (gen v)
      rw [H_gen]
      have h := CategoryTheory.congr_fun (cone_identity (v 0) (n+1)) (R (n+1) (gen v))
      have hz := CategoryTheory.congr_fun hR (gen v)
      change D (n+1) (R (n+1) (gen v)) = 0 at hz
      change D (n+2) (cone (v 0) (n+2) (R (n+1) (gen v))) +
        cone (v 0) (n+1) (D (n+1) (R (n+1) (gen v))) = R (n+1) (gen v) at h
      rw [hz,map_zero,add_zero] at h
      exact h
    rw [he]
    unfold R
    abel

theorem H_T (a : ℤ) (n : ℕ) : H n ≫ T a (n+1) = T a n ≫ H n := by
  induction n with
  | zero => simp [H]
  | succ n ih =>
    have hR : R n ≫ T a (n+1) = T a (n+1) ≫ R n := by
      unfold R
      rw [Preadditive.sub_comp,Preadditive.sub_comp,Category.id_comp,E_T,
        Category.assoc,ih,← Category.assoc,← T_D]
      simp only [Preadditive.comp_sub,Category.comp_id,Category.assoc]
    apply ModuleCat.free_hom_ext
    intro v
    change T a (n+2) (H (n+1) (gen v)) = H (n+1) (T a (n+1) (gen v))
    rw [H_gen,T_gen,H_gen]
    have hc := CategoryTheory.congr_fun (cone_equiv (v 0) a (n+1)) (R n (gen v))
    change T a (n+2) (cone (v 0) (n+1) (R n (gen v))) =
      cone (a+v 0) (n+1) (T a (n+1) (R n (gen v))) at hc
    rw [hc]
    have hr := CategoryTheory.congr_fun hR (gen v)
    change T a (n+1) (R n (gen v)) = R n (T a (n+1) (gen v)) at hr
    rw [hr,T_gen]
    rfl

#print axioms E_D
#print axioms H_identity
#print axioms H_T
end CMDG.CondensedCM5R0.BreenDeligneIntegerStraightening
