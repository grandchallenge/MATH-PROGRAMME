import CMDGNatConcordance

namespace CMDG.EuclidBridge

open CMDG.NatConcordance
open ZFSet

/-- Relational greatest-common-divisor specification over the Lean/DTT natural numbers.
This deliberately avoids identifying the `Nat.gcd` function across foundations. -/
def DTTIsGCD (a b d : Nat) : Prop :=
  0 < d ∧ d ∣ a ∧ d ∣ b ∧ ∀ k : Nat, k ∣ a → k ∣ b → k ∣ d

/-- The same bounded relational specification on the chosen Type-category NNO carrier. -/
def NNOIsGCD (a b d : NNOCarrier) : Prop :=
  nnoLe (nnoSucc nnoZero) d ∧
  nnoDvd d a ∧ nnoDvd d b ∧
  ∀ k : NNOCarrier, nnoDvd k a → nnoDvd k b → nnoDvd k d

/-- Greatest-common-divisor specification only on the admitted finite von Neumann image.
The quantified common divisors are themselves encoded natural numbers; this is not a full
syntactic-ZFC arithmetic or model-theoretic claim. -/
def ZFCFiniteImageIsGCD (a b d : NNOCarrier) : Prop :=
  zLe (nnoToZfc (nnoSucc nnoZero)) (nnoToZfc d) ∧
  zDvd (nnoToZfc d) (nnoToZfc a) ∧
  zDvd (nnoToZfc d) (nnoToZfc b) ∧
  ∀ k : NNOCarrier,
    zDvd (nnoToZfc k) (nnoToZfc a) →
    zDvd (nnoToZfc k) (nnoToZfc b) →
    zDvd (nnoToZfc k) (nnoToZfc d)

/-- Operation-level NAT concordance transports the relational gcd specification from DTT to NNO. -/
theorem dtt_to_nno_gcd {a b d : Nat} :
    DTTIsGCD a b d ↔ NNOIsGCD (dttToNNO a) (dttToNNO b) (dttToNNO d) := by
  simp [DTTIsGCD, NNOIsGCD, dttToNNO, nnoZero, nnoSucc, nnoLe, nnoDvd]

/-- The admitted NNO-to-ZFSet operation transports give the finite-image relational gcd spec. -/
theorem nno_to_zfc_finite_image_gcd {a b d : NNOCarrier} :
    NNOIsGCD a b d ↔ ZFCFiniteImageIsGCD a b d := by
  simp [NNOIsGCD, ZFCFiniteImageIsGCD]

/-- Relational recovery of the protected Euclid fixture at the DTT natural-number locus. -/
theorem dtt_gcd_252_105_21 : DTTIsGCD 252 105 21 := by
  refine ⟨by norm_num, by norm_num, by norm_num, ?_⟩
  intro k hk252 hk105
  have hkg : k ∣ Nat.gcd 252 105 := Nat.dvd_gcd hk252 hk105
  norm_num at hkg ⊢
  exact hkg

/-- The Euclidean trace of EUCLID-GCD-E2E-001, reconstructed without importing MATHCERT. -/
theorem dtt_trace_252_105 :
    252 = 2 * 105 + 42 ∧
    105 = 2 * 42 + 21 ∧
    42 = 2 * 21 + 0 := by
  norm_num

/-- Trace transported across the admitted DTT-to-NNO arithmetic interface. -/
theorem nno_trace_252_105 :
    dttToNNO 252 = nnoAdd (nnoMul (dttToNNO 2) (dttToNNO 105)) (dttToNNO 42) ∧
    dttToNNO 105 = nnoAdd (nnoMul (dttToNNO 2) (dttToNNO 42)) (dttToNNO 21) ∧
    dttToNNO 42 = nnoAdd (nnoMul (dttToNNO 2) (dttToNNO 21)) (dttToNNO 0) := by
  norm_num [dttToNNO, nnoAdd, nnoMul]

/-- Trace represented on the admitted finite von Neumann image. -/
theorem zfc_finite_image_trace_252_105 :
    nnoToZfc 252 = zAdd (zMul (nnoToZfc 2) (nnoToZfc 105)) (nnoToZfc 42) ∧
    nnoToZfc 105 = zAdd (zMul (nnoToZfc 2) (nnoToZfc 42)) (nnoToZfc 21) ∧
    nnoToZfc 42 = zAdd (zMul (nnoToZfc 2) (nnoToZfc 21)) (nnoToZfc 0) := by
  simp [nnoToZfc, zAdd, zMul, zNat]

/-- The theorem-bearing bridge root. It transports only the relational natural-number gcd
specification and Euclidean trace. The original `Nat.gcd` functional theorem remains bound to its
MATHCERT environment, and the integer Bézout witness remains outside this NAT-only bridge. -/
theorem euclid_gcd_relational_bridge :
    DTTIsGCD 252 105 21 ∧
    NNOIsGCD (dttToNNO 252) (dttToNNO 105) (dttToNNO 21) ∧
    ZFCFiniteImageIsGCD (dttToNNO 252) (dttToNNO 105) (dttToNNO 21) ∧
    (252 = 2 * 105 + 42 ∧ 105 = 2 * 42 + 21 ∧ 42 = 2 * 21 + 0) := by
  have hdtt := dtt_gcd_252_105_21
  have hnno := dtt_to_nno_gcd.mp hdtt
  have hzfc := nno_to_zfc_finite_image_gcd.mp hnno
  exact ⟨hdtt, hnno, hzfc, dtt_trace_252_105⟩

end CMDG.EuclidBridge
