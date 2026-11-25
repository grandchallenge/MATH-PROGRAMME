import Erdos27Independence
import Mathlib.Logic.Equiv.Fin.Basic
namespace Erdos27Period
open Erdos27CRT Erdos27Independence
def residueFin (n : ℕ) [NeZero n] : ZMod n ≃ Fin n where
  toFun x := ⟨x.val,ZMod.val_lt x⟩
  invFun x := (x.val : ZMod n)
  left_inv := ZMod.natCast_zmod_val
  right_inv x := Fin.ext (ZMod.val_natCast_of_lt x.isLt)

def periodEquiv (k P : ℕ) [NeZero k] [NeZero P] :
    ZMod (k*P) ≃ Fin k × ZMod P :=
  (residueFin (k*P)).trans (finProdFinEquiv.symm.trans (Equiv.prodCongr (Equiv.refl _) (residueFin P).symm))

theorem period_projection (k P : ℕ) [NeZero k] [NeZero P] (x : ZMod (k*P)) :
    (periodEquiv k P x).2 = ZMod.castHom (Nat.dvd_mul_left P k) (ZMod P) x := by
  change ((x.val % P : ℕ) : ZMod P) = _
  have h : ZMod.castHom (Nat.dvd_mul_left P k) (ZMod P) x = (x.val : ZMod P) := by
    conv_lhs => rw [← ZMod.natCast_zmod_val x]
    exact map_natCast _ _
  rw [h]
  apply ZMod.val_injective P
  rw [ZMod.val_natCast, ZMod.val_natCast, Nat.mod_mod]

theorem period_count (k P : ℕ) [NeZero k] [NeZero P] (Q : ZMod P → Prop) :
    count (fun x : ZMod (k*P) => Q (ZMod.castHom (Nat.dvd_mul_left P k) (ZMod P) x)) = k * count Q := by
  have h := count_and (periodEquiv k P) (fun _ => True) Q
  have H : (fun x : ZMod (k*P) => True ∧ Q (periodEquiv k P x).2) =
      (fun x => Q (ZMod.castHom (Nat.dvd_mul_left P k) (ZMod P) x)) := by
    funext x
    rw [true_and, period_projection]
  rw [H, count_all, Fintype.card_fin] at h
  exact h

theorem period_density (k P : ℕ) [NeZero k] [NeZero P] (Q : ZMod P → Prop) :
    (count (fun x : ZMod (k*P) => Q (ZMod.castHom (Nat.dvd_mul_left P k) (ZMod P) x)) : ℚ) / ((k*P : ℕ) : ℚ) =
      (count Q : ℚ) / (P : ℚ) := by
  rw [period_count k P]
  push_cast
  have hk : (k : ℚ) ≠ 0 := by exact_mod_cast NeZero.ne k
  rw [mul_div_mul_left _ _ hk]

#print axioms period_projection
#print axioms period_count
#print axioms period_density
end Erdos27Period
