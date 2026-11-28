import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCechDescent
import Mathlib.LinearAlgebra.FreeModule.PID
import Mathlib.RingTheory.Int.Basic

/-! Over the actual lifted integer coefficient ring a finitely
generated module has a finite free cover. Every Čech relation
module is finite free, so the exactness descent is unconditional
once exactness on finite lattices is given. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
open BreenDeligneProbe
local instance : IsDomain Coeff.{u} := (ULift.ringEquiv : Coeff.{u} ≃+* ℤ).toMulEquiv.isDomain ℤ
local instance : IsPrincipalIdealRing Coeff.{u} :=
  IsPrincipalIdealRing.of_surjective (ULift.ringEquiv.symm : ℤ ≃+* Coeff.{u})
    ULift.ringEquiv.symm.surjective

theorem finite_cover (A : Mod.{u}) [Module.Finite Coeff.{u} A] :
    ∃ n : ℕ, ∃ p : rank.{u} n ⟶ A, Function.Surjective p := by
  obtain ⟨n,x,hx⟩ := Module.Finite.exists_fin (R:=Coeff.{u}) (M:=A)
  refine ⟨n,tupleMap x,?_⟩
  apply LinearMap.range_eq_top.mp
  apply top_unique
  rw [← hx]
  apply Submodule.span_le.mpr
  rintro _ ⟨i,rfl⟩
  exact ⟨generic n i,tupleMap_generic x i⟩

theorem relation_finite_free (n : ℕ) {A : Mod.{u}} (p : rank.{u} n ⟶ A) (j : ℕ) :
    ∃ m : ℕ, Nonempty (rank.{u} m ≅ rel p j) := by
  letI : Module.Finite Coeff.{u} (rank.{u} n) :=
    Module.Finite.of_basis (Finsupp.basisSingleOne (R:=Coeff.{u}) (ι:=ULift.{u+1} (Fin n)))
  letI : Module.Finite Coeff.{u} (relSub p j) := inferInstance
  letI : Module.IsTorsionFree Coeff.{u} (rank.{u} n) := by
    change Module.IsTorsionFree Coeff.{u} (ULift.{u+1} (Fin n) →₀ Coeff.{u})
    infer_instance
  letI : Module.IsTorsionFree Coeff.{u} (Fin (j+1) → rank.{u} n) := by
    apply Module.IsTorsionFree.of_smul_eq_zero
    intro r x hx
    by_cases hr : r = 0
    · exact Or.inl hr
    · right
      funext i
      have hh := congrFun hx i
      change r • x i = 0 at hh
      exact (smul_eq_zero.mp hh).resolve_left hr
  letI : Module.IsTorsionFree Coeff.{u} (relSub p j) := inferInstance
  obtain ⟨m,b⟩ := Module.basisOfFiniteTypeTorsionFree' (R:=Coeff.{u}) (M:=relSub p j)
  refine ⟨m,⟨?_⟩⟩
  exact ((Finsupp.domLCongr (R:=Coeff.{u}) (M:=Coeff.{u})
    (Equiv.ulift : ULift.{u+1} (Fin m) ≃ Fin m)).trans b.repr.symm).toModuleIso

theorem PolynomialComplex.exact_finite (C : PolynomialComplex.{u})
    (h : ∀ n : ℕ, C.ExactAt (rank.{u} n)) (A : Mod.{u})
    [Module.Finite Coeff.{u} A] : C.ExactAt A := by
  obtain ⟨n,p,hp⟩ := finite_cover A
  apply C.cech_descend p hp
  intro j
  obtain ⟨m,⟨e⟩⟩ := relation_finite_free n p j
  exact C.exact_iso e (h m)

#print axioms relation_finite_free
#print axioms PolynomialComplex.exact_finite
end CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
