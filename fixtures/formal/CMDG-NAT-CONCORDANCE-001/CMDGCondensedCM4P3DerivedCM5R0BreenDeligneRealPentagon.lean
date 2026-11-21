import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealCochains
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Abel
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith


/-!
# CMDG CM5: bounded real pentagon cochains on actual compact probes

Construct C(A⁴×S,ℝ) and the continuous-linear alternating five-face
pullback from C(A³×S,ℝ). Prove its composite with the protected
degree-one differential vanishes. Quantitatively prove its operator
norm is at most 5, the new doubling pullback has norm at most 1, and
doubling commutes with this new differential. Specialize to all
circle products A=(ℝ/ℤ)^I and profinite S.

This is an analytic interface for one explicit degree-three summand,
not the all-degree finite-type resolution or a derived internal-Hom
comparison. No full H²/H³ vanishing is asserted.
-/
noncomputable section
universe u v
namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains

variable (A : Type u) (S : Type v)
variable [TopologicalSpace A] [CompactSpace A] [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]

abbrev A4p := A × (A × (A × A))
abbrev C3p := C((A4p A) × S, ℝ)

def pface0 : C((A4p A) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.2.1,(p.1.2.2.1,p.1.2.2.2)),p.2),by fun_prop⟩
def pface1 : C((A4p A) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.1+p.1.2.1,(p.1.2.2.1,p.1.2.2.2)),p.2),by fun_prop⟩
def pface2 : C((A4p A) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.1,(p.1.2.1+p.1.2.2.1,p.1.2.2.2)),p.2),by fun_prop⟩
def pface3 : C((A4p A) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.1,(p.1.2.1,p.1.2.2.1+p.1.2.2.2)),p.2),by fun_prop⟩
def pface4 : C((A4p A) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.1,(p.1.2.1,p.1.2.2.1)),p.2),by fun_prop⟩

def pentagonCochainDifferential : C2a A S →L[ℝ] C3p A S :=
  ContinuousMap.compCLM ℝ ℝ (pface0 A S) -
    ContinuousMap.compCLM ℝ ℝ (pface1 A S) +
    ContinuousMap.compCLM ℝ ℝ (pface2 A S) -
    ContinuousMap.compCLM ℝ ℝ (pface3 A S) +
    ContinuousMap.compCLM ℝ ℝ (pface4 A S)

/-- Real cochain face of the genuine CondensedAb pentagon syzygy. -/
theorem pentagonCochainDifferential_comp_differential1_zero
    (f : C1 A S) :
    pentagonCochainDifferential A S ((differential1 A S f).1) = 0 := by
  ext p
  simp [pentagonCochainDifferential, differential1,
      pface0,pface1,pface2,pface3,pface4,
      pBC,pAB_C,pA_BC,pAB,add_assoc]
  abel

private theorem five_term_real_norm_le (a b c d e : ℝ) :
    ‖a - b + c - d + e‖ ≤
      ‖a‖ + ‖b‖ + ‖c‖ + ‖d‖ + ‖e‖ := by
  have h0 := norm_sub_le a b
  have h1 := norm_add_le (a-b) c
  have h2 := norm_sub_le (a-b+c) d
  have h3 := norm_add_le (a-b+c-d) e
  linarith

theorem pentagonCochainDifferential_norm_le (f : C2a A S) :
    ‖pentagonCochainDifferential A S f‖ ≤ 5 * ‖f‖ := by
  apply (ContinuousMap.norm_le _ (by positivity)).2
  intro p
  change ‖f ((pface0 A S) p) -
      f ((pface1 A S) p) + f ((pface2 A S) p) -
      f ((pface3 A S) p) + f ((pface4 A S) p)‖ ≤ 5 * ‖f‖
  have h0 := f.norm_coe_le_norm ((pface0 A S) p)
  have h1 := f.norm_coe_le_norm ((pface1 A S) p)
  have h2 := f.norm_coe_le_norm ((pface2 A S) p)
  have h3 := f.norm_coe_le_norm ((pface3 A S) p)
  have h4 := f.norm_coe_le_norm ((pface4 A S) p)
  have hs := five_term_real_norm_le
    (f ((pface0 A S) p))
    (f ((pface1 A S) p))
    (f ((pface2 A S) p))
    (f ((pface3 A S) p))
    (f ((pface4 A S) p))
  nlinarith

theorem pentagonCochainDifferential_opnorm_le_five :
    ‖pentagonCochainDifferential A S‖ ≤ 5 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro f
  exact pentagonCochainDifferential_norm_le A S f

#print axioms pentagonCochainDifferential_norm_le
#print axioms pentagonCochainDifferential_opnorm_le_five

#print axioms pentagonCochainDifferential_comp_differential1_zero
def pDouble3 : C((A4p A) × S, (A4p A) × S) :=
  ⟨fun p => ((p.1.1+p.1.1,
      (p.1.2.1+p.1.2.1,
      (p.1.2.2.1+p.1.2.2.1,p.1.2.2.2+p.1.2.2.2))),p.2),
    by fun_prop⟩

def doubleStar3 : C3p A S →L[ℝ] C3p A S :=
  ContinuousMap.compCLM ℝ ℝ (pDouble3 A S)

def doubleStar2Assoc : C2a A S →L[ℝ] C2a A S :=
  ContinuousMap.compCLM ℝ ℝ (pDouble2a A S)

theorem doubleStar3_nonexpansive (f : C3p A S) :
    ‖doubleStar3 A S f‖ ≤ ‖f‖ := by
  change ‖f.comp (pDouble3 A S)‖ ≤ ‖f‖
  apply (ContinuousMap.norm_le _ (norm_nonneg f)).2
  intro p
  exact f.norm_coe_le_norm ((pDouble3 A S) p)

theorem doubleStar3_opnorm_le_one :
    ‖doubleStar3 A S‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro f
  simpa only [one_mul] using doubleStar3_nonexpansive A S f

theorem pentagon_differential_commutes_doubling (f : C2a A S) :
    pentagonCochainDifferential A S (doubleStar2Assoc A S f) =
    doubleStar3 A S (pentagonCochainDifferential A S f) := by
  ext p
  simp [pentagonCochainDifferential,doubleStar2Assoc,doubleStar3,
    pDouble3,pDouble2a,pface0,pface1,pface2,pface3,pface4,
    add_assoc]
  abel

#print axioms doubleStar3_nonexpansive
#print axioms doubleStar3_opnorm_le_one
#print axioms pentagon_differential_commutes_doubling

theorem circleTorus_pentagonCochain_differential_sq_zero
    (I : Type u) (P : Profinite.{v})
    (f : C1 (I → UnitAddCircle) P) :
    pentagonCochainDifferential (I → UnitAddCircle) P
      ((differential1 (I → UnitAddCircle) P f).1) = 0 :=
  pentagonCochainDifferential_comp_differential1_zero
    (I → UnitAddCircle) P f

theorem circleTorus_pentagonCochain_opnorm_le_five
    (I : Type u) (P : Profinite.{v}) :
    ‖pentagonCochainDifferential (I → UnitAddCircle) P‖ ≤ 5 :=
  pentagonCochainDifferential_opnorm_le_five (I → UnitAddCircle) P

#print axioms circleTorus_pentagonCochain_differential_sq_zero
#print axioms circleTorus_pentagonCochain_opnorm_le_five

end CMDG.CondensedCM5R0.BreenDeligneRealCochains
