import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.Topology.ContinuousMap.Algebra
import Mathlib.Analysis.Normed.Operator.Basic
import Mathlib.Tactic.Abel
import Mathlib.Tactic.FunProp
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Condensed.Functors

/-!
# Breen–Deligne low-degree real Banach cochains on actual compact-torus probes

This is the genuine continuous-real cochain model C(A^r × P, ℝ) used
in the source derivation of Scholze's Theorem 4.3. We define actual
continuous linear differentials and homotopies in degrees zero and one,
prove d¹d⁰=0 and dH+Hd=2 id−[2]* for all cochains, and specialize
to A=(ℝ/ℤ)^I with arbitrary profinite P. The maps are bounded by their
ContinuousLinearMap types. The all-degree Breen–Deligne resolution and
comparison to derived internal Hom in CondensedAb are NOT proved here.
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

#print axioms circleTorus_differential_sq_zero
#print axioms circleTorus_doubling_homotopy_degreeOne

end CMDG.CondensedCM5R0.BreenDeligneRealCochains
