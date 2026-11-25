import Erdos27Period
open scoped BigOperators
namespace Erdos27Correlation
open Erdos27CRT Erdos27Period

theorem compatible_iff (a c : ℕ) (r s : ℤ) :
    (∃ t : ℤ, t ≡ r [ZMOD (a : ℤ)] ∧ t ≡ s [ZMOD (c : ℤ)]) ↔
      (Nat.gcd a c : ℤ) ∣ s-r := by
  constructor
  · rintro ⟨t,ha,hc⟩
    have h1 := ha.of_dvd (Int.natCast_dvd_natCast.mpr (Nat.gcd_dvd_left a c))
    have h2 := hc.of_dvd (Int.natCast_dvd_natCast.mpr (Nat.gcd_dvd_right a c))
    exact Int.modEq_iff_dvd.mp (h1.symm.trans h2)
  · rintro ⟨k,hk⟩
    refine ⟨r+(a : ℤ)*Nat.gcdA a c*k,?_,?_⟩
    · rw [mul_assoc]
      exact Int.modEq_add_fac_self
    · have h := ((Int.gcd_a_modEq a c).mul_right k).add_left r
      have hs : r+(Nat.gcd a c : ℤ)*k=s := by omega
      rw [hs] at h
      exact h

theorem modEq_lcm (a c : ℕ) (x t : ℤ) :
    (x ≡ t [ZMOD (a : ℤ)] ∧ x ≡ t [ZMOD (c : ℤ)]) ↔
      x ≡ t [ZMOD (Nat.lcm a c : ℤ)] := by
  simpa [Int.lcm] using
    (Int.modEq_and_modEq_iff_modEq_lcm (a:=x) (b:=t) (m:=(a:ℤ)) (n:=(c:ℤ)))

theorem joint_residue_iff (M a c : ℕ) (ha : a ∣ M) (hc : c ∣ M)
    (r s t : ℤ) (hta : t ≡ r [ZMOD (a : ℤ)]) (htc : t ≡ s [ZMOD (c : ℤ)])
    (x : ZMod M) :
    (ZMod.castHom ha (ZMod a) x = (r : ZMod a) ∧
      ZMod.castHom hc (ZMod c) x = (s : ZMod c)) ↔
    ZMod.castHom (Nat.lcm_dvd ha hc) (ZMod (Nat.lcm a c)) x = (t : ZMod (Nat.lcm a c)) := by
  obtain ⟨z,rfl⟩ := ZMod.intCast_surjective x
  simp only [map_intCast,ZMod.intCast_eq_intCast_iff]
  rw [← modEq_lcm]
  exact and_congr (⟨fun h => h.trans hta.symm,fun h => h.trans hta⟩)
    (⟨fun h => h.trans htc.symm,fun h => h.trans htc⟩)

theorem joint_density (M a c : ℕ) [NeZero M] (ha : a ∣ M) (hc : c ∣ M)
    (r s : ℤ) :
    density (fun x : ZMod M => ZMod.castHom ha (ZMod a) x = (r : ZMod a) ∧
      ZMod.castHom hc (ZMod c) x = (s : ZMod c)) =
      if (Nat.gcd a c : ℤ) ∣ s-r then 1/(Nat.lcm a c : ℚ) else 0 := by
  classical
  let P := fun x : ZMod M => ZMod.castHom ha (ZMod a) x = (r : ZMod a) ∧
      ZMod.castHom hc (ZMod c) x = (s : ZMod c)
  by_cases h : (Nat.gcd a c : ℤ) ∣ s-r
  · rw [if_pos h]
    obtain ⟨t,hta,htc⟩ := (compatible_iff a c r s).mpr h
    have H : P = (fun x => ZMod.castHom (Nat.lcm_dvd ha hc) (ZMod (Nat.lcm a c)) x = (t : ZMod (Nat.lcm a c))) :=
      funext (fun x => propext (joint_residue_iff M a c ha hc r s t hta htc x))
    have : NeZero (Nat.lcm a c) := ⟨Nat.ne_of_gt (Nat.pos_of_dvd_of_pos (Nat.lcm_dvd ha hc) (Nat.pos_of_ne_zero (NeZero.ne M)))⟩
    change density P = _
    rw [H]
    exact common_residue_mass (Nat.lcm a c) M (Nat.lcm_dvd ha hc) (t : ZMod (Nat.lcm a c))
  · rw [if_neg h]
    have H : P = fun _ => False := by
      funext x
      apply propext
      constructor
      · intro hx
        obtain ⟨z,hz⟩ := ZMod.intCast_surjective x
        rw [← hz] at hx
        simp only [P,map_intCast,ZMod.intCast_eq_intCast_iff] at hx
        exact h ((compatible_iff a c r s).mp ⟨z,hx⟩)
      · exact False.elim
    change density P = _
    rw [H]
    unfold density count
    simp

theorem image_weight_le {α β : Type*} (S : Finset α) (f : α → β)
    (w : β → ℚ) (hw : ∀ x, 0 ≤ w x) [DecidableEq β] :
    ∑ x ∈ S.image f, w x ≤ ∑ x ∈ S, w (f x) := by
  classical
  induction S using Finset.induction_on with
  | empty => simp
  | @insert x S hx ih =>
    rw [Finset.image_insert, Finset.sum_insert hx]
    by_cases h : f x ∈ S.image f
    · rw [Finset.insert_eq_of_mem h]
      exact ih.trans (le_add_of_nonneg_left (hw _))
    · rw [Finset.sum_insert h]
      exact add_le_add_right ih _

def weight (u v : ℕ × ℤ) : ℚ :=
  if u ≠ v ∧ ¬ u.1.Coprime v.1 then 1/((u.1 : ℚ)*(v.1 : ℚ)) else 0

theorem weight_nonneg (u v : ℕ × ℤ) : 0 ≤ weight u v := by
  unfold weight
  split
  · exact div_nonneg zero_le_one (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _))
  · exact le_rfl

noncomputable def beta2 (S : Finset (ℕ × ℤ)) : ℚ :=
  ∑ p ∈ S ×ˢ S, weight p.1 p.2

theorem projection_bound {ι : Type*} (S : Finset ι) (f : ι → ℕ × ℤ) :
    beta2 (S.image f) ≤ ∑ p ∈ S ×ˢ S, weight (f p.1) (f p.2) := by
  classical
  let g : ι × ι → (ℕ × ℤ) × (ℕ × ℤ) := fun p => (f p.1,f p.2)
  have he : (S ×ˢ S).image g = S.image f ×ˢ S.image f := by
    apply Finset.ext
    rintro ⟨u,v⟩
    simp only [Finset.mem_image,Finset.mem_product,g,Prod.mk.injEq]
    constructor
    · rintro ⟨⟨i,j⟩,⟨hi,hj⟩,he1,he2⟩
      exact ⟨⟨i,hi,he1⟩,⟨j,hj,he2⟩⟩
    · rintro ⟨⟨i,hi,he1⟩,⟨j,hj,he2⟩⟩
      exact ⟨(i,j),⟨hi,hj⟩,he1,he2⟩
  unfold beta2
  rw [← he]
  exact image_weight_le (S ×ˢ S) g (fun p => weight p.1 p.2) (fun p => weight_nonneg p.1 p.2)

noncomputable def gated (P : Prop) (w : ℚ) : ℚ :=
  @ite ℚ P (Classical.propDecidable P) w 0

theorem gated_average (M : ℕ) [NeZero M] (P : ZMod M → Prop) (w : ℚ) :
    (∑ h : ZMod M, gated (P h) w)/(M : ℚ) = w * density P := by
  classical
  have H : (∑ h : ZMod M, gated (P h) w) =
      w * ∑ h : ZMod M, @ite ℚ (P h) (Classical.propDecidable _) 1 0 := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro h _
    by_cases hp : P h <;> simp [gated,hp]
  rw [H,Finset.sum_boole]
  unfold density count
  rw [@Fintype.card_subtype _ inferInstance P
    (@Subtype.fintype _ P (fun x => Classical.propDecidable (P x)) inferInstance)
    (fun x => Classical.propDecidable (P x))]
  rw [mul_div_assoc]

noncomputable def active {ι : Type*} [Fintype ι] {M : ℕ}
    (a : ι → ℕ) (r : ι → ℤ) (ha : ∀ i, a i ∣ M) (h : ZMod M) : Finset ι :=
  Finset.univ.filter (fun i => ZMod.castHom (ha i) (ZMod (a i)) h = (r i : ZMod (a i)))

theorem active_mem {ι : Type*} [Fintype ι] {M : ℕ}
    (a : ι → ℕ) (r : ι → ℤ) (ha : ∀ i, a i ∣ M) (h : ZMod M) (i : ι) :
    i ∈ active a r ha h ↔ ZMod.castHom (ha i) (ZMod (a i)) h = (r i : ZMod (a i)) := by
  classical
  unfold active
  rw [Finset.mem_filter]
  simp only [Finset.mem_univ,true_and]

theorem active_pair_sum {ι : Type*} [Fintype ι] {M : ℕ}
    (a : ι → ℕ) (r : ι → ℤ) (ha : ∀ i, a i ∣ M) (h : ZMod M) (w : ι × ι → ℚ) :
    ∑ p ∈ active a r ha h ×ˢ active a r ha h, w p =
      ∑ p : ι × ι, gated
        (ZMod.castHom (ha p.1) (ZMod (a p.1)) h = (r p.1 : ZMod (a p.1)) ∧
        ZMod.castHom (ha p.2) (ZMod (a p.2)) h = (r p.2 : ZMod (a p.2))) (w p) := by
  classical
  let S := active a r ha h ×ˢ active a r ha h
  have H (p : ι × ι) : p ∈ S ↔
        (ZMod.castHom (ha p.1) (ZMod (a p.1)) h = (r p.1 : ZMod (a p.1)) ∧
        ZMod.castHom (ha p.2) (ZMod (a p.2)) h = (r p.2 : ZMod (a p.2))) := by
    simp only [S,Finset.mem_product,active_mem]
  calc
    ∑ p ∈ S, w p = ∑ p ∈ S, gated (p ∈ S) (w p) := by
      apply Finset.sum_congr rfl
      intro p hp
      simp [gated,hp]
    _ = ∑ p : ι × ι, gated (p ∈ S) (w p) := by
      apply Finset.sum_subset (Finset.subset_univ S)
      intro p _ hp
      simp [gated,hp]
    _ = _ := by
      apply Finset.sum_congr rfl
      intro p _
      by_cases hp : p ∈ S
      · simp [gated,hp,(H p).mp hp]
      · rw [gated,if_neg hp,gated,if_neg (fun h' => hp ((H p).mpr h'))]

noncomputable def pairBound (a b : ℕ) (r s : ℤ) (w : ℚ) : ℚ :=
  w * gated ((Nat.gcd a b : ℤ) ∣ s-r) (1/(Nat.lcm a b : ℚ))

theorem indexed_average {ι : Type*} [Fintype ι] (M : ℕ) [NeZero M]
    (a : ι → ℕ) (r : ι → ℤ) (ha : ∀ i, a i ∣ M) (w : ι × ι → ℚ) :
    (∑ h : ZMod M, ∑ p ∈ active a r ha h ×ˢ active a r ha h, w p)/(M : ℚ) =
      ∑ p : ι × ι, pairBound (a p.1) (a p.2) (r p.1) (r p.2) (w p) := by
  classical
  simp only [active_pair_sum]
  rw [Finset.sum_comm, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro p _
  rw [gated_average M, joint_density M]
  unfold pairBound gated
  by_cases H : (Nat.gcd (a p.1) (a p.2) : ℤ) ∣ r p.2-r p.1
  · simp only [if_pos H]
  · simp only [if_neg H]

theorem mean_correlation_bound {ι : Type*} [Fintype ι] (M : ℕ) [NeZero M]
    (a b : ι → ℕ) (r : ι → ℤ) (ha : ∀ i, a i ∣ M) :
    (∑ h : ZMod M, beta2 ((active a r ha h).image (fun i => (b i,r i))))/(M : ℚ) ≤
      ∑ p : ι × ι, pairBound (a p.1) (a p.2) (r p.1) (r p.2)
        (weight (b p.1,r p.1) (b p.2,r p.2)) := by
  rw [← indexed_average M a r ha (fun p => weight (b p.1,r p.1) (b p.2,r p.2))]
  apply div_le_div_of_nonneg_right _ (Nat.cast_nonneg M)
  exact Finset.sum_le_sum (fun h _ => projection_bound (active a r ha h) (fun i => (b i,r i)))

noncomputable def beta (S : Finset (ℕ × ℤ)) : ℚ := beta2 S / 2

theorem pair_weight_upper {ι : Type*} (a b : ι → ℕ) (r : ι → ℤ) (p : ι × ι) :
    pairBound (a p.1) (a p.2) (r p.1) (r p.2)
      (weight (b p.1,r p.1) (b p.2,r p.2)) ≤
    gated (p.1 ≠ p.2 ∧ ¬ (b p.1).Coprime (b p.2))
      (1/((b p.1 : ℚ)*(b p.2 : ℚ))) *
    gated ((Nat.gcd (a p.1) (a p.2) : ℤ) ∣ r p.2-r p.1)
      (1/(Nat.lcm (a p.1) (a p.2) : ℚ)) := by
  unfold pairBound
  apply mul_le_mul_of_nonneg_right
  · unfold weight gated
    by_cases h : (b p.1,r p.1) ≠ (b p.2,r p.2) ∧ ¬ (b p.1).Coprime (b p.2)
    · have hn : p.1 ≠ p.2 := by
        intro he
        exact h.1 (by rw [he])
      rw [if_pos h,if_pos ⟨hn,h.2⟩]
    · rw [if_neg h]
      split
      · exact div_nonneg zero_le_one (mul_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _))
      · exact le_rfl
  · unfold gated
    split
    · exact div_nonneg zero_le_one (Nat.cast_nonneg _)
    · exact le_rfl

theorem lemma32_finite {ι : Type*} [Fintype ι] (M : ℕ) [NeZero M]
    (a b : ι → ℕ) (r : ι → ℤ) (ha : ∀ i, a i ∣ M) :
    (∑ h : ZMod M, beta ((active a r ha h).image (fun i => (b i,r i))))/(M : ℚ) ≤
      (∑ p : ι × ι, gated (p.1 ≠ p.2 ∧ ¬ (b p.1).Coprime (b p.2))
        (1/((b p.1 : ℚ)*(b p.2 : ℚ))) *
        gated ((Nat.gcd (a p.1) (a p.2) : ℤ) ∣ r p.2-r p.1)
        (1/(Nat.lcm (a p.1) (a p.2) : ℚ)))/2 := by
  unfold beta
  rw [← Finset.sum_div, div_div, mul_comm (2 : ℚ), ← div_div]
  apply div_le_div_of_nonneg_right _ (by norm_num)
  exact (mean_correlation_bound M a b r ha).trans
    (Finset.sum_le_sum (fun p _ => pair_weight_upper a b r p))

#print axioms pair_weight_upper
#print axioms lemma32_finite
#check lemma32_finite
#print axioms indexed_average
#print axioms mean_correlation_bound
#check mean_correlation_bound
#print axioms gated_average
#print axioms active_mem
#print axioms active_pair_sum

#print axioms image_weight_le
#print axioms weight_nonneg
#print axioms projection_bound
#print axioms compatible_iff
#print axioms modEq_lcm
#print axioms joint_residue_iff
#print axioms joint_density
end Erdos27Correlation
