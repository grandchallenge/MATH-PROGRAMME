import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealCochains
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Abel
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity


/-!
# CMDG CM5: bounded hexagon, symmetry and diagonal real cochains

Starting from the actual Breen–Deligne compact Banach cochain complex
C(A^r×S,ℝ), construct continuous-linear operators dual to the genuine
compact-polynomial hexagon, pair-swap involution, and strict diagonal
CondensedAb syzygies. Prove separately that each operator composed
with the protected first differential is zero.

Establish quantitative operator-norm estimates:
  ‖D_hex‖≤6, ‖D_sym‖≤2, ‖D_diag‖≤1.
Prove the corresponding statements for A=(ℝ/ℤ)^I and arbitrary
profinite probe S. The sibling pentagon has operator norm ≤5.

These are genuine analytic degree-three *candidate* cochain maps,
not a proof of exactness or H² vanishing, and not the source's
all-degree pseudocoherent Breen–Deligne resolution nor derived
real/circle sheaf comparison. No new axioms or assumptions.
-/
noncomputable section
universe u v
namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains

variable (A : Type u) (S : Type v)
variable [TopologicalSpace A] [CompactSpace A] [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]

def pHexSwap : C((A × (A × A)) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.2.1,(p.1.1,p.1.2.2)),p.2),by fun_prop⟩
def pHexRotate : C((A × (A × A)) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.2.1,(p.1.2.2,p.1.1)),p.2),by fun_prop⟩
def pHexPair0 : C((A × (A × A)) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.1,p.1.2.1+p.1.2.2),p.2),by fun_prop⟩
def pHexPair1 : C((A × (A × A)) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.1,p.1.2.1),p.2),by fun_prop⟩
def pHexPair2 : C((A × (A × A)) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.1,p.1.2.2),p.2),by fun_prop⟩

def hexAssocStar : C2a A S →L[ℝ] C2a A S :=
  1 - ContinuousMap.compCLM ℝ ℝ (pHexSwap A S) +
    ContinuousMap.compCLM ℝ ℝ (pHexRotate A S)
def hexCommStar : C1 A S →L[ℝ] C2a A S :=
  -ContinuousMap.compCLM ℝ ℝ (pHexPair0 A S) +
    ContinuousMap.compCLM ℝ ℝ (pHexPair1 A S) +
    ContinuousMap.compCLM ℝ ℝ (pHexPair2 A S)

/-- The dual of the genuine compact-source hexagon relation. -/
def hexRealDifferential : C2 A S →L[ℝ] C2a A S :=
  (hexAssocStar A S).comp
    (ContinuousLinearMap.fst ℝ (C2a A S) (C1 A S)) +
  (hexCommStar A S).comp
    (ContinuousLinearMap.snd ℝ (C2a A S) (C1 A S))

def symRealDifferential : C2 A S →L[ℝ] C1 A S :=
  (1 + ContinuousMap.compCLM ℝ ℝ (pSwap A S)).comp
    (ContinuousLinearMap.snd ℝ (C2a A S) (C1 A S))

def diagonalRealDifferential : C2 A S →L[ℝ] C0 A S :=
  (ContinuousMap.compCLM ℝ ℝ (pDiag A S)).comp
    (ContinuousLinearMap.snd ℝ (C2a A S) (C1 A S))

theorem hexRealDifferential_comp_differential1_zero (f : C1 A S) :
    hexRealDifferential A S (differential1 A S f) = 0 := by
  ext p
  simp [hexRealDifferential,hexAssocStar,hexCommStar,
    differential1,pBC,pAB_C,pA_BC,pAB,pSwap,
    pHexSwap,pHexRotate,pHexPair0,pHexPair1,pHexPair2,
    add_assoc]
  abel

theorem symRealDifferential_comp_differential1_zero (f : C1 A S) :
    symRealDifferential A S (differential1 A S f) = 0 := by
  ext p
  simp [symRealDifferential,differential1,pSwap]

theorem diagonalRealDifferential_comp_differential1_zero (f : C1 A S) :
    diagonalRealDifferential A S (differential1 A S f) = 0 := by
  ext p
  simp [diagonalRealDifferential,differential1,pSwap,pDiag]

private theorem norm_sub_add_le_three (a b c : ℝ) :
    ‖a-b+c‖ ≤ ‖a‖+‖b‖+‖c‖ := by
  linarith [norm_sub_le a b, norm_add_le (a-b) c]

private theorem norm_neg_add_add_le_three (a b c : ℝ) :
    ‖-a+b+c‖ ≤ ‖a‖+‖b‖+‖c‖ := by
  have h := norm_sub_add_le_three b a c
  have hh : (-a+b+c) = b-a+c := by abel
  rw [hh]
  linarith

theorem diagonalRealDifferential_norm_le_one (f : C2 A S) :
    ‖diagonalRealDifferential A S f‖ ≤ ‖f‖ := by
  change ‖f.2.comp (pDiag A S)‖ ≤ ‖f‖
  have h : ‖f.2.comp (pDiag A S)‖ ≤ ‖f.2‖ := by
    apply (ContinuousMap.norm_le _ (norm_nonneg f.2)).2
    intro p
    exact f.2.norm_coe_le_norm ((pDiag A S) p)
  exact h.trans (le_max_right _ _)

theorem symRealDifferential_norm_le_two (f : C2 A S) :
    ‖symRealDifferential A S f‖ ≤ 2 * ‖f‖ := by
  apply (ContinuousMap.norm_le _ (by positivity)).2
  intro p
  have h0 := f.2.norm_coe_le_norm p
  have h1 := f.2.norm_coe_le_norm ((pSwap A S) p)
  have hbound : ‖f.2‖ ≤ ‖f‖ := le_max_right _ _
  change ‖f.2 p + f.2 ((pSwap A S) p)‖ ≤ 2 * ‖f‖
  linarith [norm_add_le (f.2 p) (f.2 ((pSwap A S) p))]

theorem hexRealDifferential_norm_le_six (f : C2 A S) :
    ‖hexRealDifferential A S f‖ ≤ 6 * ‖f‖ := by
  apply (ContinuousMap.norm_le _ (by positivity)).2
  intro p
  let a := f.1 p
  let b := f.1 ((pHexSwap A S) p)
  let c := f.1 ((pHexRotate A S) p)
  let d := f.2 ((pHexPair0 A S) p)
  let e := f.2 ((pHexPair1 A S) p)
  let g := f.2 ((pHexPair2 A S) p)
  have ha : ‖a‖ ≤ ‖f.1‖ := f.1.norm_coe_le_norm _
  have hb : ‖b‖ ≤ ‖f.1‖ := f.1.norm_coe_le_norm _
  have hc : ‖c‖ ≤ ‖f.1‖ := f.1.norm_coe_le_norm _
  have hd : ‖d‖ ≤ ‖f.2‖ := f.2.norm_coe_le_norm _
  have he : ‖e‖ ≤ ‖f.2‖ := f.2.norm_coe_le_norm _
  have hg : ‖g‖ ≤ ‖f.2‖ := f.2.norm_coe_le_norm _
  have hm1 : ‖f.1‖ ≤ ‖f‖ := le_max_left _ _
  have hm2 : ‖f.2‖ ≤ ‖f‖ := le_max_right _ _
  change ‖(a-b+c)+(-d+e+g)‖ ≤ 6 * ‖f‖
  have hl := norm_sub_add_le_three a b c
  have hr := norm_neg_add_add_le_three d e g
  linarith [norm_add_le (a-b+c) (-d+e+g)]

theorem diagonalRealDifferential_opnorm_le_one :
    ‖diagonalRealDifferential A S‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro f
  simpa only [one_mul] using diagonalRealDifferential_norm_le_one A S f

theorem symRealDifferential_opnorm_le_two :
    ‖symRealDifferential A S‖ ≤ 2 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro f
  exact symRealDifferential_norm_le_two A S f

theorem hexRealDifferential_opnorm_le_six :
    ‖hexRealDifferential A S‖ ≤ 6 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro f
  exact hexRealDifferential_norm_le_six A S f

#print axioms diagonalRealDifferential_opnorm_le_one
#print axioms symRealDifferential_opnorm_le_two
#print axioms hexRealDifferential_opnorm_le_six

#print axioms hexRealDifferential_comp_differential1_zero
#print axioms symRealDifferential_comp_differential1_zero
#print axioms diagonalRealDifferential_comp_differential1_zero
theorem circleTorus_hexRealDifferential_comp_differential1_zero
    (I : Type u) (P : Profinite.{v})
    (f : C1 (I → UnitAddCircle) P) :
    hexRealDifferential (I → UnitAddCircle) P
      (differential1 (I → UnitAddCircle) P f) = 0 :=
  hexRealDifferential_comp_differential1_zero (I → UnitAddCircle) P f

theorem circleTorus_symRealDifferential_comp_differential1_zero
    (I : Type u) (P : Profinite.{v})
    (f : C1 (I → UnitAddCircle) P) :
    symRealDifferential (I → UnitAddCircle) P
      (differential1 (I → UnitAddCircle) P f) = 0 :=
  symRealDifferential_comp_differential1_zero (I → UnitAddCircle) P f

theorem circleTorus_diagonalRealDifferential_comp_differential1_zero
    (I : Type u) (P : Profinite.{v})
    (f : C1 (I → UnitAddCircle) P) :
    diagonalRealDifferential (I → UnitAddCircle) P
      (differential1 (I → UnitAddCircle) P f) = 0 :=
  diagonalRealDifferential_comp_differential1_zero (I → UnitAddCircle) P f

theorem circleTorus_hexRealDifferential_norm_le_six
    (I : Type u) (P : Profinite.{v}) :
    ‖hexRealDifferential (I → UnitAddCircle) P‖ ≤ 6 :=
  hexRealDifferential_opnorm_le_six (I → UnitAddCircle) P

theorem circleTorus_symRealDifferential_norm_le_two
    (I : Type u) (P : Profinite.{v}) :
    ‖symRealDifferential (I → UnitAddCircle) P‖ ≤ 2 :=
  symRealDifferential_opnorm_le_two (I → UnitAddCircle) P

theorem circleTorus_diagonalRealDifferential_norm_le_one
    (I : Type u) (P : Profinite.{v}) :
    ‖diagonalRealDifferential (I → UnitAddCircle) P‖ ≤ 1 :=
  diagonalRealDifferential_opnorm_le_one (I → UnitAddCircle) P

#print axioms circleTorus_hexRealDifferential_comp_differential1_zero
#print axioms circleTorus_hexRealDifferential_norm_le_six

end CMDG.CondensedCM5R0.BreenDeligneRealCochains
