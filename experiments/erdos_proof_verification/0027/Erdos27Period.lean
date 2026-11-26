import Erdos27Independence
import Erdos27Weighted
namespace Erdos27Period
open Erdos27CRT Erdos27Independence
def residueFin (n : ℕ) [NeZero n] : ZMod n ≃ Fin n where
  toFun x := ⟨x.val,ZMod.val_lt x⟩
  invFun x := (x.val : ZMod n)
  left_inv := ZMod.natCast_zmod_val
  right_inv x := Fin.ext (ZMod.val_natCast_of_lt x.isLt)

def splitFin (k P : ℕ) [NeZero P] : Fin (k*P) ≃ Fin k × Fin P where
  toFun x := (⟨x.val/P, (Nat.div_lt_iff_lt_mul (Nat.pos_of_ne_zero (NeZero.ne P))).2 x.isLt⟩,
    ⟨x.val%P, Nat.mod_lt _ (Nat.pos_of_ne_zero (NeZero.ne P))⟩)
  invFun x := ⟨x.2.val + P*x.1.val, by
    calc
      x.2.val + P*x.1.val < P + P*x.1.val := Nat.add_lt_add_right x.2.isLt _
      _ = (x.1.val+1)*P := by rw [Nat.add_mul, one_mul, Nat.mul_comm P x.1.val, Nat.add_comm]
      _ ≤ k*P := Nat.mul_le_mul_right P x.1.isLt⟩
  left_inv x := Fin.ext (Nat.mod_add_div x.val P)
  right_inv := by
    rintro ⟨x,y⟩
    apply Prod.ext
    · apply Fin.ext
      change (y.val + P*x.val)/P = x.val
      rw [Nat.add_mul_div_left _ _ (Nat.pos_of_ne_zero (NeZero.ne P)), Nat.div_eq_of_lt y.isLt, zero_add]
    · apply Fin.ext
      change (y.val + P*x.val)%P = y.val
      rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt y.isLt]

def periodEquiv (k P : ℕ) [NeZero k] [NeZero P] :
    ZMod (k*P) ≃ Fin k × ZMod P :=
  (residueFin (k*P)).trans ((splitFin k P).trans (Equiv.prodCongr (Equiv.refl _) (residueFin P).symm))

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

noncomputable def density {T : ℕ} [NeZero T] (Q : ZMod T → Prop) : ℚ :=
  (count Q : ℚ) / (T : ℚ)

theorem density_lift (P T : ℕ) [NeZero P] [NeZero T] (h : P ∣ T)
    (Q : ZMod P → Prop) :
    density (fun x : ZMod T => Q (ZMod.castHom h (ZMod P) x)) = density Q := by
  have hT : T ≠ 0 := NeZero.ne T
  obtain ⟨k,hk⟩ := h
  rw [Nat.mul_comm] at hk
  cases hk
  have : NeZero k := ⟨by
    intro h0
    exact hT (by simp [h0])⟩
  unfold density
  exact period_density k P Q

theorem cast_chain {a b c : ℕ} (ha : a ∣ b) (hb : b ∣ c) (x : ZMod c) :
    ZMod.castHom ha (ZMod a) (ZMod.castHom hb (ZMod b) x) =
      ZMod.castHom (ha.trans hb) (ZMod a) x := by
  obtain ⟨z,rfl⟩ := ZMod.intCast_surjective x
  simp only [map_intCast]

theorem common_residue_mass (M T : ℕ) [NeZero M] [NeZero T] (h : M ∣ T)
    (r : ZMod M) :
    density (fun x : ZMod T => ZMod.castHom h (ZMod M) x = r) = 1/(M : ℚ) := by
  rw [density_lift M T h (fun y => y = r)]
  unfold density
  rw [count_eq]
  rfl

theorem common_family_independent {ι : Type*} (M B T : ℕ) [NeZero M] [NeZero B] [NeZero T]
    (cop : M.Coprime B) (hP : M*B ∣ T) (r : ZMod M)
    (a : ι → ℕ) (s : ι → ℤ) (ha : ∀ i, a i ∣ B) :
    density (fun x : ZMod T =>
      ZMod.castHom ((Nat.dvd_mul_right M B).trans hP) (ZMod M) x = r ∧
      ∀ i, ZMod.castHom (((ha i).trans (Nat.dvd_mul_left B M)).trans hP) (ZMod (a i)) x ≠ (s i : ZMod (a i))) =
    (1/(M : ℚ)) * density (fun x : ZMod T =>
      ∀ i, ZMod.castHom (((ha i).trans (Nat.dvd_mul_left B M)).trans hP) (ZMod (a i)) x ≠ (s i : ZMod (a i))) := by
  let A : ZMod (M*B) → Prop := fun x => ZMod.castHom (Nat.dvd_mul_right M B) (ZMod M) x = r
  let I : ZMod (M*B) → Prop := fun x => ∀ i, ZMod.castHom ((ha i).trans (Nat.dvd_mul_left B M)) (ZMod (a i)) x ≠ (s i : ZMod (a i))
  have h1 := density_lift (M*B) T hP (fun x => A x ∧ I x)
  have h2 := density_lift (M*B) T hP I
  simp only [A,I,cast_chain] at h1 h2
  rw [h1,h2]
  exact congruence_family_independent M B cop r a s ha

theorem coprime_lcm {ι : Type*} (M : ℕ) (S : Finset ι) (a : ι → ℕ)
    (hc : ∀ i ∈ S, M.Coprime (a i)) : M.Coprime (S.lcm a) := by
  classical
  induction S using Finset.induction_on with
  | empty => simp
  | @insert i S hi ih =>
    rw [Finset.lcm_insert]
    change M.Coprime (Nat.lcm (a i) (S.lcm a))
    have h1 := hc i (Finset.mem_insert_self i S)
    have h2 := ih (fun j hj => hc j (Finset.mem_insert_of_mem hj))
    exact (h1.mul_right h2).of_dvd_right
      (Nat.lcm_dvd (Nat.dvd_mul_right _ _) (Nat.dvd_mul_left _ _))

theorem finite_family_independent {ι : Type*} [Fintype ι] (M T : ℕ) [NeZero M] [NeZero T]
    (hm : M ∣ T) (r : ZMod M) (a : ι → ℕ) (s : ι → ℤ)
    (ha : ∀ i, a i ∣ T) (hc : ∀ i, M.Coprime (a i)) :
    density (fun x : ZMod T => ZMod.castHom hm (ZMod M) x = r ∧
      ∀ i, ZMod.castHom (ha i) (ZMod (a i)) x ≠ (s i : ZMod (a i))) =
      (1/(M : ℚ)) * density (fun x : ZMod T =>
      ∀ i, ZMod.castHom (ha i) (ZMod (a i)) x ≠ (s i : ZMod (a i))) := by
  classical
  let B := Finset.univ.lcm a
  have hb : B ∣ T := Finset.lcm_dvd (fun i _ => ha i)
  have hB : NeZero B := ⟨by
    intro hz
    rw [hz] at hb
    exact NeZero.ne T (by simpa using hb)⟩
  have hcop : M.Coprime B := coprime_lcm M Finset.univ a (fun i _ => hc i)
  have hP := hcop.mul_dvd_of_dvd_of_dvd hm hb
  exact common_family_independent M B T hcop hP r a s (fun i => Finset.dvd_lcm (Finset.mem_univ i))

noncomputable def predSet {T : ℕ} [NeZero T] (Q : ZMod T → Prop) : Finset (ZMod T) :=
  @Finset.filter _ Q (fun x => Classical.propDecidable (Q x)) Finset.univ

theorem predSet_mass {T : ℕ} [NeZero T] (Q : ZMod T → Prop) :
    Erdos27Weighted.mass T (predSet Q) = density Q := by
  classical
  unfold Erdos27Weighted.mass density count predSet
  rw [@Fintype.card_subtype _ inferInstance Q (@Subtype.fintype _ Q (fun x => Classical.propDecidable (Q x)) inferInstance)
    (fun x => Classical.propDecidable (Q x))]

theorem predSet_inter {T : ℕ} [NeZero T] (A I : ZMod T → Prop) :
    predSet A ∩ predSet I = predSet (fun x => A x ∧ I x) := by
  classical
  ext x
  simp [predSet]

theorem arithmetic_step {ι : Type*} [Fintype ι] (M T : ℕ) [NeZero M] [NeZero T]
    (hm : M ∣ T) (r : ZMod M) (a : ι → ℕ) (s : ι → ℤ)
    (ha : ∀ i, a i ∣ T) (hc : ∀ i, M.Coprime (a i))
    (L : List (Finset (ZMod T))) :
    let A := predSet (fun x : ZMod T => ZMod.castHom hm (ZMod M) x = r)
    let I := predSet (fun x : ZMod T => ∀ i, ZMod.castHom (ha i) (ZMod (a i)) x ≠ (s i : ZMod (a i)))
    (1-1/(M : ℚ))*Erdos27Weighted.mass T (I \ Erdos27Weighted.badUnion L) -
      (1/(M : ℚ))*Erdos27Weighted.badMass T L ≤
        Erdos27Weighted.mass T ((I \ Erdos27Weighted.badUnion L) \ A) := by
  dsimp only
  apply Erdos27Weighted.finite_step_list
  · exact div_nonneg zero_le_one (Nat.cast_nonneg M)
  · rw [predSet_inter, predSet_mass, predSet_mass]
    exact finite_family_independent M T hm r a s ha hc

#print axioms predSet_mass
#print axioms predSet_inter
#print axioms arithmetic_step
#print axioms coprime_lcm
#print axioms finite_family_independent
#print axioms density_lift
#print axioms cast_chain
#print axioms common_residue_mass
#print axioms common_family_independent
#print axioms period_projection
#print axioms period_count
#print axioms period_density
#check finite_family_independent
#check arithmetic_step
end Erdos27Period
