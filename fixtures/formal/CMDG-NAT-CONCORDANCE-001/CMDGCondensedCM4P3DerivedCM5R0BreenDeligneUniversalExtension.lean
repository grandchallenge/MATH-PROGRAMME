import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneUniversalTransport
import Mathlib.CategoryTheory.InducedCategory

/-! Universal formulas on finite free modules extend uniquely to all
modules, in the precise universe and polynomial functors of UniversalBD. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
open BreenDeligneProbe

abbrev rank (n : ℕ) : Mod.{u} :=
  (ModuleCat.free Coeff).obj (ULift.{u+1} (Fin n))

abbrev Latt := InducedCategory Mod.{u} (rank.{u})
abbrev incl : Latt.{u} ⥤ Mod.{u} := inducedFunctor rank.{u}

def generic (n : ℕ) (i : Fin n) : rank.{u} n :=
  ModuleCat.freeMk (ULift.up i)

def tupleMap {M : Mod.{u}} {n : ℕ} (x : Fin n → M) : rank.{u} n ⟶ M :=
  ModuleCat.freeDesc (↾fun i : ULift.{u+1} (Fin n) => x i.down)

theorem tupleMap_generic {M : Mod.{u}} {n : ℕ} (x : Fin n → M) (i : Fin n) :
    tupleMap x (generic n i) = x i :=
  ModuleCat.freeDesc_apply _ _

theorem tupleMap_comp {M N : Mod.{u}} {n : ℕ} (x : Fin n → M) (f : M ⟶ N) :
    tupleMap x ≫ f = tupleMap (fun i => f (x i)) := by
  apply ModuleCat.free_hom_ext
  intro i
  change f (tupleMap x (generic n i.down)) = tupleMap (fun i => f (x i)) (generic n i.down)
  rw [tupleMap_generic,tupleMap_generic]

theorem tupleMap_generic_id (n : ℕ) : tupleMap (generic.{u} n) = 𝟙 _ := by
  apply ModuleCat.free_hom_ext
  intro i
  exact tupleMap_generic (generic n) i.down

variable {k : ℕ} (a : Fin k → ℕ)

def gen (j : Fin k) : (polynomial a).obj (rank.{u} (a j)) :=
  ModuleCat.freeMk (⟨j,generic (a j)⟩ : (tupleSet a).obj (rank (a j)))

theorem polynomial_map_gen {M : Mod.{u}} (j : Fin k) (x : Fin (a j) → M) :
    (polynomial a).map (tupleMap x) (gen a j) =
      ModuleCat.freeMk (⟨j,x⟩ : (tupleSet a).obj M) := by
  change (ModuleCat.free Coeff).map ((tupleSet a).map (tupleMap x)) (gen a j) = _
  rw [gen,ModuleCat.free_map_apply]
  congr 1
  apply Sigma.ext
  · rfl
  · apply heq_of_eq
    funext i
    exact tupleMap_generic x i

variable {G : Mod.{u} ⥤ Mod.{u}}

def extendAt (v : incl ⋙ polynomial a ⟶ incl ⋙ G) (M : Mod.{u}) :
    (polynomial a).obj M ⟶ G.obj M :=
  ModuleCat.freeDesc (↾fun z : (tupleSet a).obj M =>
    G.map (tupleMap z.2) (v.app (a z.1) (gen a z.1)))

theorem extendAt_gen (v : incl ⋙ polynomial a ⟶ incl ⋙ G) (M : Mod.{u})
    (j : Fin k) (x : Fin (a j) → M) :
    extendAt a v M (ModuleCat.freeMk (⟨j,x⟩ : (tupleSet a).obj M)) =
      G.map (tupleMap x) (v.app (a j) (gen a j)) :=
  ModuleCat.freeDesc_apply _ _

def extend (v : incl ⋙ polynomial a ⟶ incl ⋙ G) : polynomial a ⟶ G where
  app := extendAt a v
  naturality := by
    intro M N f
    apply ModuleCat.free_hom_ext
    rintro ⟨j,x⟩
    change extendAt a v N ((ModuleCat.free Coeff).map ((tupleSet a).map f)
      (ModuleCat.freeMk (⟨j,x⟩ : (tupleSet a).obj M))) =
      G.map f (extendAt a v M (ModuleCat.freeMk (⟨j,x⟩ : (tupleSet a).obj M)))
    rw [ModuleCat.free_map_apply]
    change extendAt a v N (ModuleCat.freeMk (⟨j,fun i => f (x i)⟩ : (tupleSet a).obj N)) = _
    rw [extendAt_gen,extendAt_gen,← tupleMap_comp,Functor.map_comp]
    rfl

theorem extend_restrict (v : incl ⋙ polynomial a ⟶ incl ⋙ G) :
    Functor.whiskerLeft incl (extend a v) = v := by
  apply NatTrans.ext
  funext n
  apply ModuleCat.free_hom_ext
  rintro ⟨j,x⟩
  change extendAt a v (rank n) (ModuleCat.freeMk (⟨j,x⟩ : (tupleSet a).obj (rank n))) = _
  rw [extendAt_gen]
  let f : Quiver.Hom (V := Latt.{u}) (a j) n := InducedCategory.homMk (tupleMap x)
  have h := CategoryTheory.congr_fun (v.naturality f) (gen a j)
  change v.app n ((polynomial a).map (tupleMap x) (gen a j)) =
    G.map (tupleMap x) (v.app (a j) (gen a j)) at h
  rw [polynomial_map_gen] at h
  exact h.symm

theorem restrict_injective : Function.Injective
    (fun v : polynomial a ⟶ G => Functor.whiskerLeft incl v) := by
  intro v w h
  apply NatTrans.ext
  funext M
  apply ModuleCat.free_hom_ext
  rintro ⟨j,x⟩
  have hv := CategoryTheory.congr_fun (v.naturality (tupleMap x)) (gen a j)
  have hw := CategoryTheory.congr_fun (w.naturality (tupleMap x)) (gen a j)
  rw [show (v.app (rank (a j))) = w.app (rank (a j)) from NatTrans.congr_app h (a j)] at hv
  change v.app M ((polynomial a).map (tupleMap x) (gen a j)) = _ at hv
  change w.app M ((polynomial a).map (tupleMap x) (gen a j)) = _ at hw
  rw [polynomial_map_gen] at hv hw
  exact hv.trans hw.symm

def restrictionEquiv : (polynomial a ⟶ G) ≃ (incl ⋙ polynomial a ⟶ incl ⋙ G) where
  toFun v := Functor.whiskerLeft incl v
  invFun := extend a
  left_inv v := restrict_injective a (extend_restrict a _)
  right_inv := extend_restrict a

theorem zero_of_restrict_zero (v : polynomial a ⟶ G)
    (h : Functor.whiskerLeft incl v = 0) : v = 0 := by
  apply restrict_injective a
  exact h

#print axioms restrictionEquiv
#print axioms zero_of_restrict_zero
end CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
