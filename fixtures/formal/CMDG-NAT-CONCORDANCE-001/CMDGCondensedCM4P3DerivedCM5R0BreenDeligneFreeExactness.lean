import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneUniversalExtension
import Mathlib.LinearAlgebra.Finsupp.Supported

/-! Exactness of a natural polynomial complex on finite lattices
extends to all free modules by explicit finite support and retraction. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
open BreenDeligneProbe

variable {X : Type (u+1)}
abbrev freeM (X : Type (u+1)) : Mod.{u} := (ModuleCat.free Coeff).obj X

def finiteRankEquiv (F : Finset X) :
    Finsupp.supported Coeff.{u} Coeff.{u} (F : Set X) ≃ₗ[Coeff.{u}] rank.{u} F.card :=
  (Finsupp.supportedEquivFinsupp (R:=Coeff.{u}) (F : Set X)).trans
    (Finsupp.domLCongr (F.equivFin.trans Equiv.ulift.symm))

def retractTo (F : Finset X) : freeM X ⟶ rank.{u} F.card := by
  classical
  exact ModuleCat.ofHom ((finiteRankEquiv F).toLinearMap.comp
    (Finsupp.restrictDom Coeff.{u} Coeff.{u} (F : Set X)))

def includeFrom (F : Finset X) : rank.{u} F.card ⟶ freeM X :=
  ModuleCat.ofHom ((Submodule.subtype _).comp (finiteRankEquiv F).symm.toLinearMap)

theorem retract_include_fixed (F : Finset X) (x : freeM X)
    (h : (x : X →₀ Coeff.{u}).support ⊆ F) :
    includeFrom F (retractTo F x) = x := by
  classical
  change ((finiteRankEquiv F).symm ((finiteRankEquiv F)
    (Finsupp.restrictDom Coeff.{u} Coeff.{u} (F : Set X) x)) : X →₀ Coeff.{u}) = x
  rw [LinearEquiv.symm_apply_apply,Finsupp.restrictDom_apply]
  apply Finsupp.ext
  intro i
  rw [Finsupp.filter_apply]
  by_cases hi : i ∈ F
  · simp [hi]
  · have hz : (show X →₀ Coeff.{u} from x) i = 0 :=
      Finsupp.notMem_support_iff.mp (fun hx => hi (h hx))
    simp [hi,hz]

theorem polynomial_finite_retract {k : ℕ} (a : Fin k → ℕ)
    (x : (polynomial a).obj (freeM X)) :
    ∃ F : Finset X, (polynomial a).map (retractTo F ≫ includeFrom F) x = x := by
  classical
  let z : (tupleSet a).obj (freeM X) →₀ Coeff.{u} := x
  let F : Finset X := z.support.biUnion fun t =>
    Finset.univ.biUnion fun i : Fin (a t.1) => (t.2 i : X →₀ Coeff.{u}).support
  refine ⟨F,?_⟩
  change Finsupp.mapDomain ((tupleSet a).map (retractTo F ≫ includeFrom F)) z = z
  calc
    _ = Finsupp.mapDomain id z := ?_
    _ = z := Finsupp.mapDomain_id
  apply Finsupp.mapDomain_congr
  intro t ht
  apply Sigma.ext
  · rfl
  · apply heq_of_eq
    funext i
    change includeFrom F (retractTo F (t.2 i)) = t.2 i
    apply retract_include_fixed
    intro j hj
    exact Finset.mem_biUnion.mpr ⟨t,ht,Finset.mem_biUnion.mpr ⟨i,Finset.mem_univ _,hj⟩⟩

variable {k l : ℕ} {a : Fin k → ℕ} {b : Fin l → ℕ} {G : Mod.{u} ⥤ Mod.{u}}

theorem free_exact (f : polynomial a ⟶ polynomial b) (g : polynomial b ⟶ G)
    (hz : f ≫ g = 0)
    (h : ∀ n : ℕ, (ShortComplex.mk (f.app (rank n)) (g.app (rank n))
      (NatTrans.congr_app hz _)).Exact) (X : Type (u+1)) :
    (ShortComplex.mk (f.app (freeM X)) (g.app (freeM X))
      (NatTrans.congr_app hz _)).Exact := by
  apply (ShortComplex.moduleCat_exact_iff _).mpr
  intro x hx
  obtain ⟨F,hF⟩ := polynomial_finite_retract b x
  let y := (polynomial b).map (retractTo F) x
  have hy : g.app (rank F.card) y = 0 := by
    have hh := CategoryTheory.congr_fun (g.naturality (retractTo F)) x
    change g.app (rank F.card) y = G.map (retractTo F) (g.app (freeM X) x) at hh
    rw [hh,show g.app (freeM X) x = 0 from hx,map_zero]
  obtain ⟨v,hv⟩ := ((ShortComplex.moduleCat_exact_iff _).mp (h F.card)) y hy
  refine ⟨(polynomial a).map (includeFrom F) v,?_⟩
  have hh := CategoryTheory.congr_fun (f.naturality (includeFrom F)) v
  change f.app (freeM X) ((polynomial a).map (includeFrom F) v) =
    (polynomial b).map (includeFrom F) (f.app (rank F.card) v) at hh
  change f.app (rank F.card) v = y at hv
  rw [hh,hv]
  exact (CategoryTheory.congr_fun ((polynomial b).map_comp (retractTo F) (includeFrom F)) x).symm.trans hF

#print axioms polynomial_finite_retract
#print axioms free_exact
end CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
