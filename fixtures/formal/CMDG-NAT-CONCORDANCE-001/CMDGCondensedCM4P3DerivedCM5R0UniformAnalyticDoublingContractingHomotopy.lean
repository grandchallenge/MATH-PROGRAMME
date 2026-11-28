import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Analysis.Normed.Operator.Banach

/-!
# CM5 E3: the Banach-space contracting homotopy behind the doubling argument

This is the infinite geometric-series argument used in Theorem 4.3(ii) of
Scholze's Lectures on Condensed Mathematics, expressed as an independent,
reusable cochain-level statement. It does not identify any particular
condensed torus cochain complex with the Banach spaces in the statement.

The two norm bounds make `1 - T` and `1 - Tnext` genuinely invertible
in the Banach algebra of bounded operators; no formal or finite series
is substituted for analytic convergence.
-/

noncomputable section

universe u v w
namespace CMDG.CondensedCM5R0

variable {E : Type u} {F : Type v} {G : Type w}
variable [NormedAddCommGroup E] [NormedSpace ℝ E]
variable [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
variable [NormedAddCommGroup G] [NormedSpace ℝ G] [CompleteSpace G]

/-- A contracting chain endomorphism homotopic to the identity makes
all cocycles in the middle Banach degree into boundaries.

The `hhom` identity is the normalized form of Scholze's
`2 • id - [2]⁎ = d h + h d`; `T` and `Tnext` are normalized doubling
operators in adjacent cochain degrees. Their norms must genuinely be
strictly less than one, and they must commute with the differential.
This proves the analytic step from these explicit, verifiable hypotheses.
-/
theorem banach_closed_exact_of_contracting_doubling
    (d : E →L[ℝ] F) (δ : F →L[ℝ] G)
    (h : F →L[ℝ] E) (k : G →L[ℝ] F)
    (T : F →L[ℝ] F) (Tnext : G →L[ℝ] G)
    (hT : ‖T‖ < 1) (hTnext : ‖Tnext‖ < 1)
    (hcomm : δ.comp T = Tnext.comp δ)
    (hhom : ∀ x : F, d (h x) + k (δ x) = x - T x)
    (f : F) (hf : δ f = 0) :
    ∃ g : E, d g = f := by
  -- Banach completeness is used *here*: the Neumann geometric series
  -- yields a genuine inverse to 1 - T in the normed operator algebra.
  have hsurj : Function.Surjective ((1 - T) : F →L[ℝ] F) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (isUnit_one_sub_of_norm_lt_one hT)).2
  obtain ⟨x, hx⟩ := hsurj f
  have hx' : x - T x = f := by
    simpa only [ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply] using hx
  have hcomm_x : δ (T x) = Tnext (δ x) := by
    have ht := congrArg (fun l : F →L[ℝ] G => l x) hcomm
    simpa only [ContinuousLinearMap.comp_apply] using ht
  have hzero : δ x - Tnext (δ x) = 0 := by
    calc
      δ x - Tnext (δ x) = δ (x - T x) := by rw [map_sub, hcomm_x]
      _ = δ f := by rw [hx']
      _ = 0 := hf
  have hinj : Function.Injective ((1 - Tnext) : G →L[ℝ] G) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (isUnit_one_sub_of_norm_lt_one hTnext)).1
  have hδ : δ x = 0 := by
    apply hinj
    simpa only [ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply,
      map_zero, sub_zero] using hzero
  refine ⟨h x, ?_⟩
  have hy := hhom x
  simp only [hδ, map_zero, add_zero] at hy
  exact hy.trans hx'

#print axioms banach_closed_exact_of_contracting_doubling

end CMDG.CondensedCM5R0
