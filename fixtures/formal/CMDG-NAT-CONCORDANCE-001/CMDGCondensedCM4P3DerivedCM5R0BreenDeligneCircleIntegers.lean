import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Connected.TotallyDisconnected
import Mathlib.Topology.ContinuousMap.Basic
import Mathlib.Topology.Algebra.Group.Basic
import Mathlib.Tactic.Abel

/-!
# CMDG CM5: honest degree-zero circle-to-discrete-integers calculation

For arbitrary index set I, the genuine compact connected torus
A=(ℝ/ℤ)^I admits no nonzero continuous additive map to discrete ℤ.
The same vanishing holds for P-parametrized families of continuous
integer functions which are additive along A, for any topological
parameter P. Hence the degree-zero *continuous* Hom vanishing holds.
This is not the higher derived condensed claim RHom(A,ℤ)=⊕_Iℤ[-1];
that requires the genuine Čech/sheaf-derived comparison in all degrees.
-/

universe u v
noncomputable section
namespace CMDG.CondensedCM5R0.BreenDeligneCircleIntegers
variable (I : Type u)

theorem circleTorus_continuous_integer_hom_zero
    (f : (I → UnitAddCircle) →+ ℤ)
    (hf : Continuous (f : (I → UnitAddCircle) → ℤ)) : f = 0 := by
  apply AddMonoidHom.ext
  intro x
  have hconst : f x = f 0 :=
    PreconnectedSpace.constant (inferInstance : PreconnectedSpace (I → UnitAddCircle)) hf
  simpa using hconst

theorem circleTorus_parametric_integer_hom_zero
    (P : Type v) [TopologicalSpace P]
    (f : C((I → UnitAddCircle) × P, ℤ))
    (hadd : ∀ (a b : I → UnitAddCircle) (p : P),
      f (a+b,p) = f (a,p) + f (b,p)) :
    ∀ (a : I → UnitAddCircle) (p : P), f (a,p) = 0 := by
  intro a p
  have hcontinuous : Continuous (fun a : I → UnitAddCircle => f (a,p)) :=
    f.continuous.comp (continuous_id.prodMk continuous_const)
  have hconst : f (a,p) = f (0,p) :=
    PreconnectedSpace.constant (inferInstance : PreconnectedSpace (I → UnitAddCircle)) hcontinuous
  have hzero : f (0,p) = 0 := by
    have h := hadd 0 0 p
    simp only [zero_add] at h
    omega
  exact hconst.trans hzero

#print axioms circleTorus_continuous_integer_hom_zero
#print axioms circleTorus_parametric_integer_hom_zero
end CMDG.CondensedCM5R0.BreenDeligneCircleIntegers
