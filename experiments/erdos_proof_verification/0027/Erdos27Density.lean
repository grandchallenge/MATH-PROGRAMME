import Erdos27Sequence
open scoped BigOperators
namespace Erdos27Density
open Erdos27CRT Erdos27Period

variable (T : ℕ) [NeZero T] (Q : ZMod T → Prop)

noncomputable def indicator (i : ℕ) : ℕ := @ite ℕ (Q (i : ZMod T)) (Classical.propDecidable _) 1 0
noncomputable def prefixCount (N : ℕ) : ℕ := ∑ i ∈ Finset.range N, indicator T Q i

omit [NeZero T] in
theorem indicator_le (i : ℕ) : indicator T Q i ≤ 1 := by
  unfold indicator
  split <;> omega

omit [NeZero T] in
theorem indicator_shift (k i : ℕ) : indicator T Q (k*T+i) = indicator T Q i := by
  have h : ((k*T+i : ℕ) : ZMod T) = (i : ZMod T) := by
    simp [Nat.cast_add,Nat.cast_mul]
  by_cases hq : Q (i : ZMod T)
  · have hq' : Q ((k*T+i : ℕ) : ZMod T) := h.symm ▸ hq
    simp only [indicator, if_pos hq, if_pos hq']
  · have hq' : ¬ Q ((k*T+i : ℕ) : ZMod T) := h.symm ▸ hq
    simp only [indicator, if_neg hq, if_neg hq']

omit [NeZero T] in
theorem prefix_le (N : ℕ) : prefixCount T Q N ≤ N := by
  unfold prefixCount
  calc
    _ ≤ ∑ i ∈ Finset.range N, (1 : ℕ) := Finset.sum_le_sum (fun i _ => indicator_le T Q i)
    _ = N := by simp

omit [NeZero T] in
theorem prefix_add (k N : ℕ) :
    prefixCount T Q (k*T+N) = prefixCount T Q (k*T) + prefixCount T Q N := by
  induction N with
  | zero => simp [prefixCount]
  | succ N ih =>
    rw [show k*T+(N+1)=k*T+N+1 by omega]
    simp only [prefixCount,Finset.sum_range_succ] at ih ⊢
    rw [ih,indicator_shift]
    omega

omit [NeZero T] in
theorem prefix_blocks (k : ℕ) : prefixCount T Q (k*T) = k * prefixCount T Q T := by
  induction k with
  | zero => simp [prefixCount]
  | succ k ih =>
    rw [Nat.succ_mul,prefix_add,ih,Nat.succ_mul]

omit [NeZero T] in
theorem prefix_decompose (N : ℕ) :
    prefixCount T Q N = (N/T)*prefixCount T Q T + prefixCount T Q (N%T) := by
  have h : N/T*T+N%T=N := by
    rw [Nat.mul_comm (N/T) T, Nat.add_comm]
    exact Nat.mod_add_div N T
  conv_lhs => rw [← h]
  rw [prefix_add,prefix_blocks]

theorem period_prefix_count : prefixCount T Q T = count Q := by
  classical
  unfold prefixCount
  rw [← Fin.sum_univ_eq_sum_range]
  have h := Fintype.sum_equiv (residueFin T).symm
    (fun i : Fin T => indicator T Q i.val)
    (fun x : ZMod T => if Q x then (1 : ℕ) else 0) (by intro i; rfl)
  rw [h,Finset.sum_boole]
  unfold count
  rw [@Fintype.card_subtype _ inferInstance Q
    (@Subtype.fintype _ Q (fun x => Classical.propDecidable (Q x)) inferInstance)
    (fun x => Classical.propDecidable (Q x))]
  rfl

theorem density_range : 0 ≤ density Q ∧ density Q ≤ 1 := by
  unfold density
  have ht : (0 : ℚ) < T := by exact_mod_cast Nat.pos_of_ne_zero (NeZero.ne T)
  constructor
  · exact div_nonneg (Nat.cast_nonneg _) ht.le
  · apply (div_le_iff₀ ht).2
    rw [one_mul,← period_prefix_count T Q]
    exact_mod_cast prefix_le T Q T

theorem discrepancy (N : ℕ) :
    (prefixCount T Q N : ℚ) - (N : ℚ)*density Q =
      (prefixCount T Q (N%T) : ℚ) - ((N%T : ℕ) : ℚ)*density Q := by
  have hN : (N : ℚ) = ((N/T : ℕ) : ℚ)*(T : ℚ) + ((N%T : ℕ) : ℚ) := by
    exact_mod_cast (show N = N/T*T+N%T by
      rw [Nat.mul_comm (N/T) T,Nat.add_comm]
      exact (Nat.mod_add_div N T).symm)
  have hT : (T : ℚ) * density Q = (prefixCount T Q T : ℚ) := by
    rw [density,← period_prefix_count T Q]
    have ht : (T : ℚ) ≠ 0 := by exact_mod_cast NeZero.ne T
    rw [mul_comm,div_mul_cancel₀ _ ht]
  rw [prefix_decompose T Q N]
  push_cast
  conv_lhs => rw [hN]
  rw [add_mul,mul_assoc,hT]
  simp

theorem discrepancy_bound (N : ℕ) :
    |(prefixCount T Q N : ℚ) - (N : ℚ)*density Q| ≤ (T : ℚ) := by
  rw [discrepancy T Q,abs_le]
  have hr : ((N%T : ℕ) : ℚ) ≤ (T : ℚ) := by
    exact_mod_cast (Nat.mod_lt N (Nat.pos_of_ne_zero (NeZero.ne T))).le
  have hc : (prefixCount T Q (N%T) : ℚ) ≤ ((N%T : ℕ) : ℚ) := by
    exact_mod_cast prefix_le T Q (N%T)
  have hd := density_range T Q
  have hm : ((N%T : ℕ) : ℚ)*density Q ≤ (T : ℚ) :=
    (mul_le_mul_of_nonneg_left hd.2 (Nat.cast_nonneg _)).trans (by rwa [mul_one])
  constructor
  · have hh := sub_le_sub_right (Nat.cast_nonneg (α := ℚ) (prefixCount T Q (N%T))) (((N%T : ℕ) : ℚ)*density Q)
    rw [zero_sub] at hh
    exact (neg_le_neg hm).trans hh
  · exact (sub_le_self _ (mul_nonneg (Nat.cast_nonneg _) hd.1)).trans (hc.trans hr)

theorem frequency_error (N : ℕ) (hn : 0 < N) :
    |(prefixCount T Q N : ℚ)/(N : ℚ) - density Q| ≤ (T : ℚ)/(N : ℚ) := by
  have hN : (0 : ℚ) < N := by exact_mod_cast hn
  have h := discrepancy_bound T Q N
  rw [abs_le] at h ⊢
  constructor
  · rw [← neg_div,le_sub_iff_add_le]
    apply (le_div_iff₀ hN).2
    have H := (le_sub_iff_add_le).mp h.1
    rw [add_mul,div_mul_cancel₀ _ hN.ne',mul_comm (density Q)]
    exact H
  · rw [sub_le_iff_le_add]
    apply (div_le_iff₀ hN).2
    have H := (sub_le_iff_le_add).mp h.2
    rw [add_mul,div_mul_cancel₀ _ hN.ne',mul_comm (density Q)]
    exact H

theorem rational_natural_density (eps : ℚ) (he : 0 < eps) :
    ∃ K : ℕ, ∀ N : ℕ, K ≤ N →
      |(prefixCount T Q N : ℚ)/(N : ℚ) - density Q| < eps := by
  refine ⟨T*eps.den+1, ?_⟩
  intro N hN
  have hn : 0 < N := by omega
  have hd : (0 : ℚ) < eps.den := by exact_mod_cast eps.den_pos
  have hq : (0 : ℚ) < N := by exact_mod_cast hn
  have hprod : (T : ℚ)*(eps.den : ℚ) < (N : ℚ) := by
    exact_mod_cast (show T*eps.den < N by omega)
  have hnum : (1 : ℚ) ≤ (eps.num : ℚ) := by
    exact_mod_cast (show (1 : ℤ) ≤ eps.num from Rat.num_pos.mpr he)
  have hsmall : (T : ℚ)/(N : ℚ) < 1/(eps.den : ℚ) :=
    (div_lt_div_iff₀ hq hd).2 (by rw [one_mul]; exact hprod)
  have hlarge : 1/(eps.den : ℚ) ≤ eps := by
    calc
      _ ≤ (eps.num : ℚ)/(eps.den : ℚ) := div_le_div_of_nonneg_right hnum hd.le
      _ = eps := Rat.num_div_den eps
  exact (frequency_error T Q N hn).trans_lt (hsmall.trans_le hlarge)

theorem count_eq_indicator_sum :
    count Q = ∑ x : ZMod T, @ite ℕ (Q x) (Classical.propDecidable _) 1 0 := by
  classical
  rw [Finset.sum_boole]
  unfold count
  rw [@Fintype.card_subtype _ inferInstance Q
    (@Subtype.fintype _ Q (fun x => Classical.propDecidable (Q x)) inferInstance)
    (fun x => Classical.propDecidable (Q x))]
  rfl

theorem count_shift (a : ZMod T) : count (fun x => Q (x+a)) = count Q := by
  rw [count_eq_indicator_sum, count_eq_indicator_sum]
  apply Fintype.sum_equiv (Equiv.addRight a)
  intro x
  rfl

noncomputable def positiveCount (N : ℕ) : ℕ :=
  ∑ i ∈ Finset.range N, indicator T Q (i+1)

omit [NeZero T] in
theorem positiveCount_shift (N : ℕ) :
    positiveCount T Q N = prefixCount T (fun x => Q (x+1)) N := by
  unfold positiveCount prefixCount
  apply Finset.sum_congr rfl
  intro i _
  unfold indicator
  have h : ((i+1 : ℕ) : ZMod T) = (i : ZMod T)+1 := by simp
  by_cases hq : Q ((i : ZMod T)+1)
  · have hq' : Q ((i+1 : ℕ) : ZMod T) := h.symm ▸ hq
    simp only [if_pos hq,if_pos hq']
  · have hq' : ¬ Q ((i+1 : ℕ) : ZMod T) := h.symm ▸ hq
    simp only [if_neg hq,if_neg hq']

theorem positive_frequency_error (N : ℕ) (hn : 0 < N) :
    |(positiveCount T Q N : ℚ)/(N : ℚ) - density Q| ≤ (T : ℚ)/(N : ℚ) := by
  rw [positiveCount_shift]
  have h := frequency_error T (fun x => Q (x+1)) N hn
  unfold density at h ⊢
  rw [count_shift T Q 1] at h
  exact h

theorem positive_natural_density (eps : ℚ) (he : 0 < eps) :
    ∃ K : ℕ, ∀ N : ℕ, K ≤ N →
      |(positiveCount T Q N : ℚ)/(N : ℚ) - density Q| < eps := by
  obtain ⟨K,hK⟩ := rational_natural_density T (fun x => Q (x+1)) eps he
  refine ⟨K,fun N hN => ?_⟩
  rw [positiveCount_shift]
  have h := hK N hN
  unfold density at h ⊢
  rw [count_shift T Q 1] at h
  exact h

omit [NeZero T] in
theorem avoidance_cast (m : ℕ) (hm : m ∣ T) (r : ℤ) (a : ℕ) :
    (ZMod.castHom hm (ZMod m) (a : ZMod T) ≠ (r : ZMod m)) ↔
      ¬ ((a : ℤ) ≡ r [ZMOD (m : ℤ)]) := by
  rw [map_natCast, ← ZMod.intCast_eq_intCast_iff]
  simp

omit [NeZero T] in
theorem positive_avoidance_count (m : ℕ → ℕ) (r : ℕ → ℤ) (n : ℕ)
    (hd : ∀ i < n, m i ∣ T) (N : ℕ) :
    positiveCount T (fun x : ZMod T => ∀ i : Fin n,
      ZMod.castHom (hd i.val i.isLt) (ZMod (m i.val)) x ≠ (r i.val : ZMod (m i.val))) N =
    ∑ a ∈ Finset.range N, @ite ℕ
      (∀ i : Fin n, ¬ (((a+1 : ℕ) : ℤ) ≡ r i.val [ZMOD (m i.val : ℤ)]))
      (Classical.propDecidable _) 1 0 := by
  unfold positiveCount
  apply Finset.sum_congr rfl
  intro a _
  unfold indicator
  have h : (∀ i : Fin n, ZMod.castHom (hd i.val i.isLt) (ZMod (m i.val)) ((a+1 : ℕ) : ZMod T) ≠ (r i.val : ZMod (m i.val))) ↔
    (∀ i : Fin n, ¬ (((a+1 : ℕ) : ℤ) ≡ r i.val [ZMOD (m i.val : ℤ)])) :=
    forall_congr' (fun i => avoidance_cast T (m i.val) (hd i.val i.isLt) (r i.val) (a+1))
  by_cases H : ∀ i : Fin n, ¬ (((a+1 : ℕ) : ℤ) ≡ r i.val [ZMOD (m i.val : ℤ)])
  · rw [if_pos (h.mpr H),if_pos H]
  · rw [if_neg (fun h' => H (h.mp h')),if_neg H]

theorem lemma21_eventual_lower (m : ℕ → ℕ) (r : ℕ → ℤ) (n : ℕ)
    (hd : ∀ i < n, m i ∣ T) (eps : ℚ) (he : 0 < eps) :
    ∃ K : ℕ, ∀ N : ℕ, K ≤ N →
    (∏ i ∈ Finset.range n, (1 - 1/(m i : ℚ))) -
      (∑ j ∈ Finset.range n, ∑ i ∈ Erdos27Sequence.bad m j, 1/((m i : ℚ)*(m j : ℚ))) - eps <
    (positiveCount T (fun x : ZMod T => ∀ i : Fin n,
      ZMod.castHom (hd i.val i.isLt) (ZMod (m i.val)) x ≠ (r i.val : ZMod (m i.val))) N : ℚ)/(N : ℚ) := by
  let Q' : ZMod T → Prop := fun x => ∀ i : Fin n,
      ZMod.castHom (hd i.val i.isLt) (ZMod (m i.val)) x ≠ (r i.val : ZMod (m i.val))
  have h := Erdos27Sequence.finite_lemma21 T m r n hd
  obtain ⟨K,hK⟩ := positive_natural_density T Q' eps he
  refine ⟨K,fun N hN => ?_⟩
  have hclose := (abs_lt.mp (hK N hN)).1
  have hstrict := (lt_sub_iff_add_lt).mp hclose
  have hbound : density Q' - eps < (positiveCount T Q' N : ℚ)/(N : ℚ) := by
    rw [sub_eq_add_neg,add_comm]
    exact hstrict
  exact (sub_le_sub_right h eps).trans_lt hbound

#print axioms avoidance_cast
#print axioms positive_avoidance_count
#print axioms lemma21_eventual_lower
#check lemma21_eventual_lower
#print axioms count_eq_indicator_sum
#print axioms count_shift
#print axioms positiveCount_shift
#print axioms positive_frequency_error
#print axioms positive_natural_density
#print axioms rational_natural_density
#check frequency_error
#check rational_natural_density
#print axioms density_range
#print axioms discrepancy
#print axioms discrepancy_bound
#print axioms frequency_error
#print axioms prefix_le
#print axioms indicator_shift
#print axioms prefix_add
#print axioms prefix_blocks
#print axioms prefix_decompose
#print axioms period_prefix_count
end Erdos27Density
