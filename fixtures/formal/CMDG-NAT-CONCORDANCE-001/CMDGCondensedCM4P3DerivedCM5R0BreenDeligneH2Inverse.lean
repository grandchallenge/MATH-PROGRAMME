import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneH2Commutation


/-!
# CM5: generic Banach inverse preserves cocycle kernels

Given P:E→L E and Q:F→L F with Q nonexpansive, D:E→L F
intertwining D P=Q D, show that x−P(x)/2=f and D f=0 imply D x=0.
Proof: the genuine continuous-linear operator 1−Q/2 is invertible
by the norm<1 Banach Neumann criterion; injectivity proves the result.

This reusable analytic result has no domain-specific axiom, no
assumed image-closure, and no formal/nonconvergent infinite series.
-/
noncomputable section

namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains

variable {E F : Type*}
variable [NormedAddCommGroup E] [NormedSpace ℝ E]
variable [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]

theorem inverse_half_preserves_kernel
    (P : E →L[ℝ] E) (D : E →L[ℝ] F) (Q : F →L[ℝ] F)
    (hQ : ∀ y, ‖Q y‖ ≤ ‖y‖)
    (hcomm : ∀ x, D (P x) = Q (D x))
    (f x : E) (hf : D f = 0)
    (hx : x - (1/2 : ℝ) • P x = f) :
    D x = 0 := by
  let U : F →L[ℝ] F := (1/2 : ℝ) • Q
  have hU : ‖U‖ < 1 := by
    have hu : ‖U‖ ≤ (1/2 : ℝ) := by
      apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
      intro y
      calc
        ‖U y‖ = (1/2 : ℝ) * ‖Q y‖ := by
          simp [U,norm_smul]
        _ ≤ (1/2 : ℝ) * ‖y‖ :=
          mul_le_mul_of_nonneg_left (hQ y) (by norm_num)
    exact lt_of_le_of_lt hu (by norm_num)
  have hinj : Function.Injective
      ((1-U) : F →L[ℝ] F) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (isUnit_one_sub_of_norm_lt_one hU)).1
  apply hinj
  have heq : D x - U (D x) = 0 := by
    calc
      D x - U (D x) =
        D (x-(1/2:ℝ) • P x) := by
          rw [map_sub,map_smul]
          simp only [U,ContinuousLinearMap.smul_apply]
          rw [hcomm]
      _ = D f := by rw [hx]
      _ = 0 := hf
  simpa only [ContinuousLinearMap.sub_apply,
    ContinuousLinearMap.one_apply,map_zero,sub_zero] using heq

#print axioms inverse_half_preserves_kernel
end CMDG.CondensedCM5R0.BreenDeligneRealCochains
