import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.Topology.ContinuousMap.Algebra
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Analysis.Normed.Operator.Banach
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Tactic.Abel
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FunProp
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Condensed.Functors

/-!
# CMDG CM5: actual Breen–Deligne torus real cochains and first positive-degree acyclicity

For any compact Hausdorff abelian A and compact probe P, defines the genuine
continuous real cochain Banach spaces C(A^r × P, ℝ), the first two cochain
differentials, explicit bounded doubling homotopy, and degree-one Neumann
contraction. Specializes to A=(ℝ/ℤ)^I and arbitrary profinite P. Proves
cochain H⁰=H¹=0 without new axioms. These cochain calculations do **not**
by themselves constitute the all-degree Breen–Deligne resolution or the
actual derived condensed RHom comparison, which remain distinct obligations.
-/

noncomputable section
universe u v
namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains
variable (A : Type u) (S : Type v)
variable [TopologicalSpace A] [CompactSpace A] [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]

abbrev C0 := C(A × S, ℝ)
abbrev C1 := C((A × A) × S, ℝ)

def pAdd : C((A × A) × S, A × S) :=
  ⟨fun p => (p.1.1+p.1.2,p.2),
    ((continuous_fst.comp continuous_fst).add
      (continuous_snd.comp continuous_fst)).prodMk continuous_snd⟩
def pFirst : C((A × A) × S, A × S) :=
  ⟨fun p => (p.1.1,p.2),
    (continuous_fst.comp continuous_fst).prodMk continuous_snd⟩
def pSecond : C((A × A) × S, A × S) :=
  ⟨fun p => (p.1.2,p.2),
    (continuous_snd.comp continuous_fst).prodMk continuous_snd⟩
def pDiag : C(A × S, (A × A) × S) :=
  ⟨fun p => ((p.1,p.1),p.2),
    (continuous_fst.prodMk continuous_fst).prodMk continuous_snd⟩
def pDouble0 : C(A × S, A × S) :=
  ⟨fun p => (p.1+p.1,p.2),
    (continuous_fst.add continuous_fst).prodMk continuous_snd⟩

def differential0 : C0 A S →L[ℝ] C1 A S :=
  ContinuousMap.compCLM ℝ ℝ (pAdd A S) -
  ContinuousMap.compCLM ℝ ℝ (pFirst A S) -
  ContinuousMap.compCLM ℝ ℝ (pSecond A S)
def hStar0 : C1 A S →L[ℝ] C0 A S :=
  -ContinuousMap.compCLM ℝ ℝ (pDiag A S)
def doubleStar0 : C0 A S →L[ℝ] C0 A S :=
  ContinuousMap.compCLM ℝ ℝ (pDouble0 A S)

theorem homotopy0 (f : C0 A S) :
    hStar0 A S (differential0 A S f) =
      f + f - doubleStar0 A S f := by
  ext p
  simp [hStar0,differential0,doubleStar0,
    pAdd,pFirst,pSecond,pDiag,pDouble0]
  abel

abbrev C2a := C((A × (A × A)) × S, ℝ)
abbrev C2 := C2a A S × C1 A S

def pBC : C((A × (A × A)) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.2.1,p.1.2.2),p.2), by fun_prop⟩
def pAB_C : C((A × (A × A)) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.1+p.1.2.1,p.1.2.2),p.2), by fun_prop⟩
def pA_BC : C((A × (A × A)) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.1,p.1.2.1+p.1.2.2),p.2), by fun_prop⟩
def pAB : C((A × (A × A)) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.1,p.1.2.1),p.2), by fun_prop⟩
def pSwap : C((A × A) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.2,p.1.1),p.2), by fun_prop⟩

def differential1 : C1 A S →L[ℝ] C2 A S :=
  ((ContinuousMap.compCLM ℝ ℝ (pBC A S) -
    ContinuousMap.compCLM ℝ ℝ (pAB_C A S) +
    ContinuousMap.compCLM ℝ ℝ (pA_BC A S) -
    ContinuousMap.compCLM ℝ ℝ (pAB A S)).prod
    (1 - ContinuousMap.compCLM ℝ ℝ (pSwap A S)))

def qAssoc1 : C((A × A) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.1,(p.1.1,p.1.2+p.1.2)),p.2), by fun_prop⟩
def qAssoc2 : C((A × A) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.1,(p.1.2,p.1.2)),p.2), by fun_prop⟩
def qAssoc3 : C((A × A) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.1,(p.1.2,p.1.1+p.1.2)),p.2), by fun_prop⟩
def qComm : C((A × A) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.1+p.1.2,p.1.2),p.2), by fun_prop⟩

def hStar1 : C2 A S →L[ℝ] C1 A S :=
  ( (ContinuousMap.compCLM ℝ ℝ (qAssoc1 A S) -
      ContinuousMap.compCLM ℝ ℝ (qAssoc2 A S) -
      ContinuousMap.compCLM ℝ ℝ (qAssoc3 A S)).comp
      (ContinuousLinearMap.fst ℝ (C2a A S) (C1 A S)) ) -
  ( (ContinuousMap.compCLM ℝ ℝ (qComm A S)).comp
      (ContinuousLinearMap.snd ℝ (C2a A S) (C1 A S)) )

def pDouble1 : C((A × A) × S, (A × A) × S) :=
  ⟨fun p => ((p.1.1+p.1.1,p.1.2+p.1.2),p.2), by fun_prop⟩
def doubleStar1 : C1 A S →L[ℝ] C1 A S :=
  ContinuousMap.compCLM ℝ ℝ (pDouble1 A S)

#check differential1
#check hStar1
#check doubleStar1

theorem differential_sq_zero (f : C0 A S) :
    differential1 A S (differential0 A S f) = 0 := by
  apply Prod.ext
  · ext p
    simp [differential0,differential1,pAdd,pFirst,pSecond,
      pBC,pAB_C,pA_BC,pAB,add_assoc]
    abel
  · ext p
    simp [differential0,differential1,pAdd,pFirst,pSecond,pSwap,add_comm]
    abel

theorem homotopy1 (f : C1 A S) :
    hStar1 A S (differential1 A S f) +
      differential0 A S (hStar0 A S f) =
        f + f - doubleStar1 A S f := by
  ext p
  simp [hStar1,differential1,differential0,hStar0,doubleStar1,
      pBC,pAB_C,pA_BC,pAB,pSwap,
      qAssoc1,qAssoc2,qAssoc3,qComm,
      pAdd,pFirst,pSecond,pDiag,pDouble1,add_assoc]
  abel

#print axioms differential_sq_zero
#print axioms homotopy1

#print axioms homotopy0
theorem circleTorus_differential_sq_zero
    (I : Type u) (P : Profinite.{v})
    (f : C((I → UnitAddCircle) × P, ℝ)) :
    differential1 (I → UnitAddCircle) P
      (differential0 (I → UnitAddCircle) P f) = 0 :=
  differential_sq_zero (I → UnitAddCircle) P f

theorem circleTorus_doubling_homotopy_degreeOne
    (I : Type u) (P : Profinite.{v})
    (f : C(((I → UnitAddCircle) × (I → UnitAddCircle)) × P, ℝ)) :
    hStar1 (I → UnitAddCircle) P
      (differential1 (I → UnitAddCircle) P f) +
    differential0 (I → UnitAddCircle) P
      (hStar0 (I → UnitAddCircle) P f) =
        f + f - doubleStar1 (I → UnitAddCircle) P f :=
  homotopy1 (I → UnitAddCircle) P f

/-- Every degree-zero real cochain cocycle is zero for a compact
abelian group: doubling forces an exact factor two whereas pullback
does not enlarge the supremum norm. This is a genuine H⁰=0 result
for the explicit Breen–Deligne real cochain differential. -/
theorem degreeZero_realCochain_cocycle_zero
    (f : C0 A S) (hf : differential0 A S f = 0) : f = 0 := by
  have h := homotopy0 A S f
  rw [hf, map_zero] at h
  have htwo : f + f = doubleStar0 A S f := by
    have hh : (0 : C0 A S) = f + f - doubleStar0 A S f := h
    exact (sub_eq_zero.mp hh.symm)
  have hbound : ‖doubleStar0 A S f‖ ≤ ‖f‖ := by
    change ‖f.comp (pDouble0 A S)‖ ≤ ‖f‖
    apply (ContinuousMap.norm_le (f.comp (pDouble0 A S)) (norm_nonneg f)).2
    intro p
    exact f.norm_coe_le_norm ((pDouble0 A S) p)
  have hnorm : ‖f + f‖ = 2 * ‖f‖ := by
    rw [← two_smul ℝ f, norm_smul]
    norm_num
  have hn : ‖f‖ = 0 := by
    have hle : 2 * ‖f‖ ≤ ‖f‖ := by
      rw [← hnorm, htwo]
      exact hbound
    nlinarith [norm_nonneg f]
  exact norm_eq_zero.mp hn

def pDouble2a : C((A × (A × A)) × S, (A × (A × A)) × S) :=
  ⟨fun p => ((p.1.1 + p.1.1,
    (p.1.2.1 + p.1.2.1, p.1.2.2 + p.1.2.2)), p.2), by fun_prop⟩

def doubleStar2 : C2 A S →L[ℝ] C2 A S :=
  ((ContinuousMap.compCLM ℝ ℝ (pDouble2a A S)).comp
    (ContinuousLinearMap.fst ℝ (C2a A S) (C1 A S))).prod
  ((doubleStar1 A S).comp
    (ContinuousLinearMap.snd ℝ (C2a A S) (C1 A S)))

theorem differential1_commutes_doubling (f : C1 A S) :
    differential1 A S (doubleStar1 A S f) =
      doubleStar2 A S (differential1 A S f) := by
  apply Prod.ext
  · ext p
    simp [differential1,doubleStar1,doubleStar2,pBC,pAB_C,pA_BC,
      pAB,pDouble1,pDouble2a,add_assoc]
    abel
  · ext p
    simp [differential1,doubleStar1,doubleStar2,pSwap,pDouble1,
      pDouble2a,add_assoc]

theorem doublingStar1_nonexpansive (f : C1 A S) :
    ‖doubleStar1 A S f‖ ≤ ‖f‖ := by
  change ‖f.comp (pDouble1 A S)‖ ≤ ‖f‖
  apply (ContinuousMap.norm_le (f.comp (pDouble1 A S)) (norm_nonneg f)).2
  intro p
  exact f.norm_coe_le_norm ((pDouble1 A S) p)

theorem doublingStar2_nonexpansive (f : C2 A S) :
    ‖doubleStar2 A S f‖ ≤ ‖f‖ := by
  have ha : ‖f.1.comp (pDouble2a A S)‖ ≤ ‖f.1‖ := by
    apply (ContinuousMap.norm_le _ (norm_nonneg f.1)).2
    intro p
    exact f.1.norm_coe_le_norm ((pDouble2a A S) p)
  have hb : ‖doubleStar1 A S f.2‖ ≤ ‖f.2‖ :=
    doublingStar1_nonexpansive A S f.2
  change max ‖f.1.comp (pDouble2a A S)‖
    ‖doubleStar1 A S f.2‖ ≤ max ‖f.1‖ ‖f.2‖
  exact max_le (ha.trans (le_max_left _ _))
    (hb.trans (le_max_right _ _))

theorem doublingStar1_opnorm_le_one :
    ‖doubleStar1 A S‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro f
  simpa only [one_mul] using doublingStar1_nonexpansive A S f

theorem doublingStar2_opnorm_le_one :
    ‖doubleStar2 A S‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro f
  simpa only [one_mul] using doublingStar2_nonexpansive A S f

/-- An unconditional positive-degree real cochain acyclicity theorem
for degree one in the *actual* compact continuous-function Banach complex.
The convergent Neumann inverse of 1-[2]* / 2 supplies a genuine primitive.
No all-degree or sheaf-derived comparison is assumed. -/
theorem degreeOne_realCochain_closed_exact (f : C1 A S)
    (hf : differential1 A S f = 0) :
    ∃ g : C0 A S, differential0 A S g = f := by
  let T : C1 A S →L[ℝ] C1 A S :=
    (1/2 : ℝ) • doubleStar1 A S
  let U : C2 A S →L[ℝ] C2 A S :=
    (1/2 : ℝ) • doubleStar2 A S
  have hT : ‖T‖ < 1 := by
    have hle : ‖T‖ ≤ (1/2 : ℝ) := by
      apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
      intro x
      calc
        ‖T x‖ = (1/2 : ℝ) * ‖doubleStar1 A S x‖ := by
          simp [T, norm_smul]
        _ ≤ (1/2 : ℝ) * ‖x‖ :=
          mul_le_mul_of_nonneg_left
            (doublingStar1_nonexpansive A S x) (by norm_num)
    exact lt_of_le_of_lt hle (by norm_num)
  have hU : ‖U‖ < 1 := by
    have hle : ‖U‖ ≤ (1/2 : ℝ) := by
      apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
      intro x
      calc
        ‖U x‖ = (1/2 : ℝ) * ‖doubleStar2 A S x‖ := by
          simp [U, norm_smul]
        _ ≤ (1/2 : ℝ) * ‖x‖ :=
          mul_le_mul_of_nonneg_left
            (doublingStar2_nonexpansive A S x) (by norm_num)
    exact lt_of_le_of_lt hle (by norm_num)
  have hsurj : Function.Surjective
      ((1 - T) : C1 A S →L[ℝ] C1 A S) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (isUnit_one_sub_of_norm_lt_one hT)).2
  obtain ⟨x,hx⟩ := hsurj f
  have hx' : x - T x = f := by
    simpa only [ContinuousLinearMap.sub_apply,
      ContinuousLinearMap.one_apply] using hx
  have hcomm_x : differential1 A S (T x) =
      U (differential1 A S x) := by
    simp only [T,U,ContinuousLinearMap.smul_apply,
      map_smul]
    rw [differential1_commutes_doubling]
  have hzero : differential1 A S x -
      U (differential1 A S x) = 0 := by
    calc
      differential1 A S x - U (differential1 A S x) =
        differential1 A S (x-T x) := by rw [map_sub,hcomm_x]
      _ = differential1 A S f := by rw [hx']
      _ = 0 := hf
  have hinj : Function.Injective
      ((1-U) : C2 A S →L[ℝ] C2 A S) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (isUnit_one_sub_of_norm_lt_one hU)).1
  have hd1x : differential1 A S x = 0 := by
    apply hinj
    simpa only [ContinuousLinearMap.sub_apply,
      ContinuousLinearMap.one_apply,map_zero,sub_zero] using hzero
  refine ⟨(1/2 : ℝ) • (hStar0 A S x), ?_⟩
  have hh := homotopy1 A S x
  rw [hd1x,map_zero,zero_add] at hh
  calc
    differential0 A S ((1/2 : ℝ) • (hStar0 A S x)) =
        (1/2 : ℝ) • differential0 A S (hStar0 A S x) := by
          rw [map_smul]
    _ = (1/2 : ℝ) • (x+x-doubleStar1 A S x) := by rw [hh]
    _ = x - T x := by
      rw [smul_sub, smul_add]
      have ht : (1/2 : ℝ) • x + (1/2 : ℝ) • x = x := by
        rw [← add_smul]
        norm_num
      rw [ht]
      rfl
    _ = f := hx'

#print axioms doublingStar1_opnorm_le_one
#print axioms doublingStar2_opnorm_le_one
/-- Explicit circle-torus degree-one real cochain acyclicity, uniform in
the circle-product index I and profinite parameter P. -/
theorem circleTorus_degreeOne_realCochain_closed_exact
    (I : Type u) (P : Profinite.{v})
    (f : C(((I → UnitAddCircle) × (I → UnitAddCircle)) × P, ℝ))
    (hf : differential1 (I → UnitAddCircle) P f = 0) :
    ∃ g : C((I → UnitAddCircle) × P, ℝ),
      differential0 (I → UnitAddCircle) P g = f :=
  degreeOne_realCochain_closed_exact (I → UnitAddCircle) P f hf

#print axioms circleTorus_degreeOne_realCochain_closed_exact

#print axioms degreeOne_realCochain_closed_exact

#print axioms doublingStar1_nonexpansive
#print axioms doublingStar2_nonexpansive

#print axioms differential1_commutes_doubling

#print axioms degreeZero_realCochain_cocycle_zero

#print axioms circleTorus_differential_sq_zero
#print axioms circleTorus_doubling_homotopy_degreeOne

end CMDG.CondensedCM5R0.BreenDeligneRealCochains
