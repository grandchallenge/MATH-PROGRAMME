import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Logic.Equiv.Basic
import Mathlib.Algebra.Field.Rat
import Mathlib.Algebra.BigOperators.Field

open scoped BigOperators
namespace Erdos27CRT

noncomputable def count {α : Type*} [Fintype α] (P : α → Prop) : ℕ := by
  classical
  exact Fintype.card {x : α // P x}

def prodFibreEquiv {β γ : Type*} (P : β → γ → Prop) :
    {x : β × γ // P x.1 x.2} ≃ Σ b : β, {c : γ // P b c} where
  toFun x := ⟨x.1.1, ⟨x.1.2, x.2⟩⟩
  invFun x := ⟨(x.1, x.2.1), x.2.2⟩
  left_inv := by rintro ⟨⟨b, c⟩, h⟩; rfl
  right_inv := by rintro ⟨b, ⟨c, h⟩⟩; rfl

noncomputable def fibreEquiv {α β γ : Type*} (e : α ≃ β × γ)
    (P : β → γ → Prop) :
    {x : α // P (e x).1 (e x).2} ≃ Σ b : β, {c : γ // P b c} :=
  (Equiv.subtypeEquivOfSubtype (p := fun x : β × γ => P x.1 x.2) e).trans
    (prodFibreEquiv P)

theorem count_fibres {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (e : α ≃ β × γ) (P : β → γ → Prop) :
    count (fun x => P (e x).1 (e x).2) = ∑ b : β, count (P b) := by
  classical
  unfold count
  rw [Fintype.card_congr (fibreEquiv e P), Fintype.card_sigma]

theorem crt_count_fibres (M B : ℕ) [NeZero M] [NeZero B]
    (cop : M.Coprime B) (P : ZMod M → ZMod B → Prop) :
    count (fun x : ZMod (M * B) =>
      P (ZMod.chineseRemainder cop x).1 (ZMod.chineseRemainder cop x).2) =
      ∑ h : ZMod M, count (P h) :=
  count_fibres (ZMod.chineseRemainder cop).toEquiv P

theorem crt_intCast (M B : ℕ) (cop : M.Coprime B) (x : ℤ) :
    ZMod.chineseRemainder cop (x : ZMod (M * B)) =
      ((x : ZMod M), (x : ZMod B)) := by
  apply Prod.ext <;> simp

theorem congruence_split (a b : ℕ) (cop : a.Coprime b) (x r : ℤ) :
    (x : ZMod (a * b)) = (r : ZMod (a * b)) ↔
      ((x : ZMod a) = (r : ZMod a) ∧ (x : ZMod b) = (r : ZMod b)) := by
  simp only [ZMod.intCast_eq_intCast_iff, Nat.cast_mul]
  exact (Int.modEq_and_modEq_iff_modEq_mul (by simpa using cop)).symm

def originalAvoid {ι : Type*} {M B : ℕ} (a b : ι → ℕ) (r : ι → ℤ)
    (ha : ∀ i, a i ∣ M) (hb : ∀ i, b i ∣ B) (x : ZMod (M * B)) : Prop :=
  ∀ i, ZMod.castHom (Nat.mul_dvd_mul (ha i) (hb i)) (ZMod (a i * b i)) x ≠
    (r i : ZMod (a i * b i))

def fibreAvoid {ι : Type*} {M B : ℕ} (a b : ι → ℕ) (r : ι → ℤ)
    (ha : ∀ i, a i ∣ M) (hb : ∀ i, b i ∣ B) (h : ZMod M) (y : ZMod B) : Prop :=
  ∀ i, ZMod.castHom (ha i) (ZMod (a i)) h = (r i : ZMod (a i)) →
    ZMod.castHom (hb i) (ZMod (b i)) y ≠ (r i : ZMod (b i))

theorem avoid_intCast_iff {ι : Type*} {M B : ℕ} (a b : ι → ℕ) (r : ι → ℤ)
    (ha : ∀ i, a i ∣ M) (hb : ∀ i, b i ∣ B) (hc : ∀ i, (a i).Coprime (b i))
    (cop : M.Coprime B) (x : ℤ) :
    originalAvoid a b r ha hb (x : ZMod (M * B)) ↔
      fibreAvoid a b r ha hb (ZMod.chineseRemainder cop (x : ZMod (M * B))).1
        (ZMod.chineseRemainder cop (x : ZMod (M * B))).2 := by
  unfold originalAvoid fibreAvoid
  rw [crt_intCast]
  simp only [map_intCast]
  constructor
  · intro H i hA hB
    exact H i ((congruence_split (a i) (b i) (hc i) x (r i)).2 ⟨hA,hB⟩)
  · intro H i hAB
    have hh := (congruence_split (a i) (b i) (hc i) x (r i)).1 hAB
    exact H i hh.1 hh.2

theorem avoid_iff {ι : Type*} {M B : ℕ} [NeZero M] [NeZero B]
    (a b : ι → ℕ) (r : ι → ℤ) (ha : ∀ i, a i ∣ M) (hb : ∀ i, b i ∣ B)
    (hc : ∀ i, (a i).Coprime (b i)) (cop : M.Coprime B) (x : ZMod (M * B)) :
    originalAvoid a b r ha hb x ↔
      fibreAvoid a b r ha hb (ZMod.chineseRemainder cop x).1
        (ZMod.chineseRemainder cop x).2 := by
  rw [← ZMod.natCast_zmod_val x]
  exact_mod_cast avoid_intCast_iff a b r ha hb hc cop (x.val : ℤ)

theorem covering_count {ι : Type*} {M B : ℕ} [NeZero M] [NeZero B]
    (a b : ι → ℕ) (r : ι → ℤ) (ha : ∀ i, a i ∣ M) (hb : ∀ i, b i ∣ B)
    (hc : ∀ i, (a i).Coprime (b i)) (cop : M.Coprime B) :
    count (originalAvoid a b r ha hb) =
      ∑ h : ZMod M, count (fibreAvoid a b r ha hb h) := by
  have H : originalAvoid a b r ha hb = fun x =>
      fibreAvoid a b r ha hb (ZMod.chineseRemainder cop x).1
        (ZMod.chineseRemainder cop x).2 := by
    funext x
    exact propext (avoid_iff a b r ha hb hc cop x)
  rw [H, crt_count_fibres]

theorem covering_density {ι : Type*} {M B : ℕ} [NeZero M] [NeZero B]
    (a b : ι → ℕ) (r : ι → ℤ) (ha : ∀ i, a i ∣ M) (hb : ∀ i, b i ∣ B)
    (hc : ∀ i, (a i).Coprime (b i)) (cop : M.Coprime B) :
    (count (originalAvoid a b r ha hb) : ℚ) / ((M * B : ℕ) : ℚ) =
      (∑ h : ZMod M, (count (fibreAvoid a b r ha hb h) : ℚ) / (B : ℚ)) / (M : ℚ) := by
  rw [covering_count a b r ha hb hc cop]
  push_cast
  rw [← Finset.sum_div, div_div, mul_comm (B : ℚ) (M : ℚ)]

#print axioms covering_density
#print axioms count_fibres
#print axioms crt_count_fibres
#print axioms congruence_split
#print axioms avoid_iff
#print axioms covering_count
#print covering_count
#check covering_density

end Erdos27CRT
