import CMDGCondensedCM4P3DerivedCM5R0UniformAnalyticDoublingContractingHomotopy
import Mathlib.Tactic

/-!
# CMDG CM5 E3: normalization of the source doubling operator

This translates the *exact* E3 doubling equation
`d h + h δ = 2 id - [2]^*` into the verified strict-contraction
form, using the operator norm bound at most one in every degree.
It remains necessary to construct these maps on the actual condensed
torus cochains and prove the source hypotheses there.
-/

noncomputable section
universe u v w
namespace CMDG.CondensedCM5R0

variable {E : Type u} {F : Type v} {G : Type w}
variable [NormedAddCommGroup E] [NormedSpace ℝ E]
variable [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
variable [NormedAddCommGroup G] [NormedSpace ℝ G] [CompleteSpace G]

/-- Source-form contraction with the literal factor 2 and bounded doubling.
This corollary retains *all* operator assumptions rather than assuming
the resulting closed-cochain exactness. -/
theorem banach_closed_exact_of_source_doubling_homotopy
    (d : E →L[ℝ] F) (δ : F →L[ℝ] G)
    (h : F →L[ℝ] E) (k : G →L[ℝ] F)
    (B : F →L[ℝ] F) (Bnext : G →L[ℝ] G)
    (hB : ‖B‖ ≤ 1) (hBnext : ‖Bnext‖ ≤ 1)
    (hcomm : δ.comp B = Bnext.comp δ)
    (hhom : ∀ x : F, d (h x) + k (δ x) = (2 : ℝ) • x - B x)
    (f : F) (hf : δ f = 0) :
    ∃ g : E, d g = f := by
  let T : F →L[ℝ] F := (1/2 : ℝ) • B
  let Tnext : G →L[ℝ] G := (1/2 : ℝ) • Bnext
  let h' : F →L[ℝ] E := (1/2 : ℝ) • h
  let k' : G →L[ℝ] F := (1/2 : ℝ) • k
  have hT : ‖T‖ < 1 := by
    calc
      ‖T‖ = (1/2 : ℝ) * ‖B‖ := by simp [T, norm_smul]
      _ ≤ 1/2 := by nlinarith [norm_nonneg B]
      _ < 1 := by norm_num
  have hTnext : ‖Tnext‖ < 1 := by
    calc
      ‖Tnext‖ = (1/2 : ℝ) * ‖Bnext‖ := by simp [Tnext, norm_smul]
      _ ≤ 1/2 := by nlinarith [norm_nonneg Bnext]
      _ < 1 := by norm_num
  have hc : δ.comp T = Tnext.comp δ := by
    ext x
    dsimp [T, Tnext]
    simp only [ContinuousLinearMap.comp_apply, ContinuousLinearMap.smul_apply, map_smul]
    have h0 := congrArg (fun l : F →L[ℝ] G => l x) hcomm
    simpa only [ContinuousLinearMap.comp_apply] using
      congrArg (fun y : G => (1/2 : ℝ) • y) h0
  have hh : ∀ x : F, d (h' x) + k' (δ x) = x - T x := by
    intro x
    calc
      d (h' x) + k' (δ x) = (1/2 : ℝ) • (d (h x) + k (δ x)) := by
        simp [h', k', smul_add]
      _ = (1/2 : ℝ) • ((2 : ℝ) • x - B x) := by rw [hhom x]
      _ = x - T x := by simp [T, smul_sub, smul_smul]
  exact banach_closed_exact_of_contracting_doubling
    d δ h' k' T Tnext hT hTnext hc hh f hf

#print axioms banach_closed_exact_of_source_doubling_homotopy
end CMDG.CondensedCM5R0
