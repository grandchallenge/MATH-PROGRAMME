import Erdos27CRT
import Mathlib.Algebra.Order.Field.Rat
namespace Erdos27Independence
open Erdos27CRT
noncomputable def andEquiv {α β : Type*} (P : α → Prop) (Q : β → Prop) :
    {x : α × β // P x.1 ∧ Q x.2} ≃ {a : α // P a} × {b : β // Q b} where
  toFun x := (⟨x.1.1,x.2.1⟩,⟨x.1.2,x.2.2⟩)
  invFun x := ⟨(x.1.1,x.2.1),x.1.2,x.2.2⟩
  left_inv := by rintro ⟨⟨a,b⟩,ha,hb⟩; rfl
  right_inv := by rintro ⟨⟨a,ha⟩,⟨b,hb⟩⟩; rfl

theorem count_and {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (e : γ ≃ α × β) (P : α → Prop) (Q : β → Prop) :
    count (fun x => P (e x).1 ∧ Q (e x).2) = count P * count Q := by
  classical
  let P' : γ → Prop := fun x => P (e x).1 ∧ Q (e x).2
  let f : Fintype {x // P' x} := @Subtype.fintype γ P' (fun x => Classical.propDecidable (P' x)) inferInstance
  let g : Fintype {x // P x} := @Subtype.fintype α P (fun x => Classical.propDecidable (P x)) inferInstance
  let h : Fintype {x // Q x} := @Subtype.fintype β Q (fun x => Classical.propDecidable (Q x)) inferInstance
  exact (@Fintype.card_congr _ _ f (@instFintypeProd _ _ g h)
    ((Equiv.subtypeEquivOfSubtype (p := fun x : α × β => P x.1 ∧ Q x.2) e).trans (andEquiv P Q))).trans
      (@Fintype.card_prod _ _ g h)

theorem count_eq {α : Type*} [Fintype α] (r : α) : count (fun x => x = r) = 1 := by
  classical
  unfold count
  have h : Unique {x : α // x = r} := ⟨⟨⟨r,rfl⟩⟩, fun x => Subtype.ext x.property⟩
  exact @Fintype.card_unique _ h (@Subtype.fintype α (fun x => x = r) (fun x => Classical.propDecidable (x = r)) inferInstance)

theorem joint_count (M B : ℕ) [NeZero M] [NeZero B]
    (cop : M.Coprime B) (r : ZMod M) (Q : ZMod B → Prop) :
    count (fun x : ZMod (M*B) => (ZMod.chineseRemainder cop x).1 = r ∧ Q (ZMod.chineseRemainder cop x).2) = count Q := by
  have h := count_and (ZMod.chineseRemainder cop).toEquiv (fun x => x = r) Q
  rw [count_eq, one_mul] at h
  exact h

theorem right_count (M B : ℕ) [NeZero M] [NeZero B]
    (cop : M.Coprime B) (Q : ZMod B → Prop) :
    count (fun x : ZMod (M*B) => Q (ZMod.chineseRemainder cop x).2) = M * count Q := by
  have h := count_and (ZMod.chineseRemainder cop).toEquiv (fun _ => True) Q
  have htop : count (fun _ : ZMod M => True) = M := by
    classical
    unfold count
    calc
      _ = Fintype.card (ZMod M) := @Fintype.card_congr _ _ (@Subtype.fintype (ZMod M) (fun _ => True) (fun _ => Classical.propDecidable True) inferInstance) inferInstance (Equiv.subtypeUnivEquiv (p := fun _ : ZMod M => True) (fun _ => trivial))
      _ = M := ZMod.card M
  have hP : (fun x : ZMod (M*B) => True ∧ Q ((ZMod.chineseRemainder cop).toEquiv x).2) = (fun x => Q (ZMod.chineseRemainder cop x).2) := by
    funext x
    exact true_and _
  rw [hP, htop] at h
  exact h

theorem joint_density (M B : ℕ) [NeZero M] [NeZero B]
    (cop : M.Coprime B) (r : ZMod M) (Q : ZMod B → Prop) :
    (count (fun x : ZMod (M*B) => (ZMod.chineseRemainder cop x).1 = r ∧ Q (ZMod.chineseRemainder cop x).2) : ℚ) / ((M*B : ℕ) : ℚ) =
    (1/(M : ℚ)) * ((count (fun x : ZMod (M*B) => Q (ZMod.chineseRemainder cop x).2) : ℚ) / ((M*B : ℕ) : ℚ)) := by
  rw [joint_count M B cop, right_count M B cop]
  push_cast
  have hm : (M : ℚ) ≠ 0 := by exact_mod_cast NeZero.ne M
  rw [← mul_div_assoc, ← mul_assoc, div_mul_cancel₀ 1 hm, one_mul]

def avoids {ι : Type*} {B : ℕ} (a : ι → ℕ) (r : ι → ℤ)
    (ha : ∀ i, a i ∣ B) (y : ZMod B) : Prop :=
  ∀ i, ZMod.castHom (ha i) (ZMod (a i)) y ≠ (r i : ZMod (a i))

theorem left_cast (M B : ℕ) [NeZero M] [NeZero B]
    (cop : M.Coprime B) (x : ZMod (M*B)) :
    ZMod.castHom (Nat.dvd_mul_right M B) (ZMod M) x = (ZMod.chineseRemainder cop x).1 := by
  have h (k : ℤ) : ZMod.castHom (Nat.dvd_mul_right M B) (ZMod M) (k : ZMod (M*B)) = (ZMod.chineseRemainder cop (k : ZMod (M*B))).1 := by
    rw [Erdos27CRT.crt_intCast]
    simp only [map_intCast]
  rw [← ZMod.natCast_zmod_val x]
  exact_mod_cast h (x.val : ℤ)

theorem right_cast_divisor (M B a : ℕ) [NeZero M] [NeZero B]
    (cop : M.Coprime B) (ha : a ∣ B) (x : ZMod (M*B)) :
    ZMod.castHom (ha.trans (Nat.dvd_mul_left B M)) (ZMod a) x =
      ZMod.castHom ha (ZMod a) (ZMod.chineseRemainder cop x).2 := by
  have h (k : ℤ) : ZMod.castHom (ha.trans (Nat.dvd_mul_left B M)) (ZMod a) (k : ZMod (M*B)) = ZMod.castHom ha (ZMod a) (ZMod.chineseRemainder cop (k : ZMod (M*B))).2 := by
    rw [Erdos27CRT.crt_intCast]
    simp only [map_intCast]
  rw [← ZMod.natCast_zmod_val x]
  exact_mod_cast h (x.val : ℤ)

theorem congruence_family_independent {ι : Type*} (M B : ℕ) [NeZero M] [NeZero B]
    (cop : M.Coprime B) (r : ZMod M) (a : ι → ℕ) (s : ι → ℤ)
    (ha : ∀ i, a i ∣ B) :
    (count (fun x : ZMod (M*B) =>
      ZMod.castHom (Nat.dvd_mul_right M B) (ZMod M) x = r ∧
      ∀ i, ZMod.castHom ((ha i).trans (Nat.dvd_mul_left B M)) (ZMod (a i)) x ≠ (s i : ZMod (a i))) : ℚ) / ((M*B : ℕ) : ℚ) =
    (1/(M : ℚ)) * ((count (fun x : ZMod (M*B) =>
      ∀ i, ZMod.castHom ((ha i).trans (Nat.dvd_mul_left B M)) (ZMod (a i)) x ≠ (s i : ZMod (a i))) : ℚ) / ((M*B : ℕ) : ℚ)) := by
  have h := joint_density M B cop r (avoids a s ha)
  unfold avoids at h
  have H (i : ι) (x : ZMod (M*B)) := right_cast_divisor M B (a i) cop (ha i) x
  simp only [left_cast M B cop, H]
  exact h

theorem count_all {α : Type*} [Fintype α] : count (fun _ : α => True) = Fintype.card α := by
  classical
  exact @Fintype.card_congr _ _ (@Subtype.fintype α (fun _ => True) (fun _ => Classical.propDecidable True) inferInstance) inferInstance
    (Equiv.subtypeUnivEquiv (p := fun _ : α => True) (fun _ => trivial))

theorem residue_count (M B : ℕ) [NeZero M] [NeZero B]
    (cop : M.Coprime B) (r : ZMod M) :
    count (fun x : ZMod (M*B) => ZMod.castHom (Nat.dvd_mul_right M B) (ZMod M) x = r) = B := by
  have h := joint_count M B cop r (fun _ => True)
  have H : (fun x : ZMod (M*B) => (ZMod.chineseRemainder cop x).1 = r ∧ True) =
      (fun x => ZMod.castHom (Nat.dvd_mul_right M B) (ZMod M) x = r) := by
    funext x
    rw [and_true, left_cast M B cop]
  rw [H, count_all, ZMod.card] at h
  exact h

theorem residue_mass (M B : ℕ) [NeZero M] [NeZero B]
    (cop : M.Coprime B) (r : ZMod M) :
    (count (fun x : ZMod (M*B) => ZMod.castHom (Nat.dvd_mul_right M B) (ZMod M) x = r) : ℚ) / ((M*B : ℕ) : ℚ) = 1/(M : ℚ) := by
  rw [residue_count M B cop]
  push_cast
  have hb : (B : ℚ) ≠ 0 := by exact_mod_cast NeZero.ne B
  rw [mul_comm (M : ℚ), ← div_div, div_self hb]

#print axioms count_all
#print axioms residue_count
#print axioms residue_mass
#print axioms congruence_family_independent
#print axioms left_cast
#print axioms right_cast_divisor
#print axioms count_and
#print axioms joint_count
#print axioms right_count
#print axioms joint_density
#check congruence_family_independent
#check residue_mass
end Erdos27Independence
