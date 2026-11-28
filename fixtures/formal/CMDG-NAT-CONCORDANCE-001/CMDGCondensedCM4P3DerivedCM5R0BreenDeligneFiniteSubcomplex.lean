import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteBar
import Mathlib.LinearAlgebra.FreeModule.PID
import Mathlib.RingTheory.Int.Basic

/-! A degreewise finite subcomplex capturing homology. Construct
finite terms recursively, lifting finitely many homology generators
and filling the finite module of boundaries in the preceding term.
No infinite-rank subgroup splitting is required. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneHomologyElements
namespace CMDG.CondensedCM5R0.BreenDeligneFiniteSubcomplex

theorem finite_lift {M N : Type} [AddCommGroup M] [AddCommGroup N]
    [Module ℤ M] [Module ℤ N] (f : M →ₗ[ℤ] N) (V : Submodule ℤ N)
    (hV : V.FG) (h : V ≤ LinearMap.range f) :
    ∃ U : Submodule ℤ M, U.FG ∧ U.map f = V := by
  obtain ⟨S,hS,hspan⟩ := Submodule.fg_def.mp hV
  have hl : ∀ x : S, ∃ y : M, f y = x.val := by
    intro x
    exact h (hspan ▸ Submodule.subset_span x.property)
  choose g hg using hl
  let T : Set M := Set.range g
  haveI : Finite S := hS.to_subtype
  refine ⟨Submodule.span ℤ T,Submodule.fg_span (Set.finite_range g),?_⟩
  rw [Submodule.map_span,← hspan]
  congr 1
  ext x
  constructor
  · rintro ⟨y,⟨t,rfl⟩,rfl⟩
    rw [hg]
    exact t.property
  · intro hx
    exact ⟨g ⟨x,hx⟩,⟨⟨x,hx⟩,rfl⟩,hg _⟩

variable (K : Ch) (h : ∀ n, Module.Finite ℤ (K.homology n))

def cycleLift (n : ℕ) : Submodule ℤ (K.cycles n) :=
  Classical.choose (finite_lift (K.homologyπ n).hom ⊤ (h n).fg_top
    (by rw [LinearMap.range_eq_top.mpr (class_surj K n)]))

theorem cycleLift_spec (n : ℕ) :
    (cycleLift K h n).FG ∧ (cycleLift K h n).map (K.homologyπ n).hom = ⊤ :=
  Classical.choose_spec (finite_lift (K.homologyπ n).hom ⊤ (h n).fg_top
    (by rw [LinearMap.range_eq_top.mpr (class_surj K n)]))

def cyclePart (n : ℕ) : Submodule ℤ (K.X n) :=
  (cycleLift K h n).map (K.iCycles n).hom

theorem cyclePart_fg (n : ℕ) : (cyclePart K h n).FG :=
  (cycleLift_spec K h n).1.map _

theorem cyclePart_closed (n : ℕ) :
    cyclePart K h n ≤ LinearMap.ker (K.d n (n-1)).hom := by
  rintro x ⟨z,hz,rfl⟩
  exact cycle_closed K n z

def boundaryPart (n : ℕ) (V : Submodule ℤ (K.X n)) : Submodule ℤ (K.X n) :=
  V ⊓ LinearMap.range (K.d (n+1) n).hom

def boundaryLift (n : ℕ) (V : Submodule ℤ (K.X n)) (hV : V.FG) :
    Submodule ℤ (K.X (n+1)) :=
  Classical.choose (finite_lift (K.d (n+1) n).hom (boundaryPart K n V)
    (hV.of_le inf_le_left) inf_le_right)

theorem boundaryLift_spec (n : ℕ) (V : Submodule ℤ (K.X n)) (hV : V.FG) :
    (boundaryLift K n V hV).FG ∧
    (boundaryLift K n V hV).map (K.d (n+1) n).hom = boundaryPart K n V :=
  Classical.choose_spec (finite_lift (K.d (n+1) n).hom (boundaryPart K n V)
    (hV.of_le inf_le_left) inf_le_right)

def finiteTerm : (n : ℕ) → {V : Submodule ℤ (K.X n) // V.FG}
  | 0 => ⟨cyclePart K h 0,cyclePart_fg K h 0⟩
  | n+1 =>
    let V := finiteTerm n
    ⟨cyclePart K h (n+1) ⊔ boundaryLift K n V.val V.property,
      (cyclePart_fg K h (n+1)).sup (boundaryLift_spec K n V.val V.property).1⟩

abbrev F (n : ℕ) := (finiteTerm K h n).val

theorem cyclePart_le (n : ℕ) : cyclePart K h n ≤ F K h n := by
  cases n with
  | zero => exact le_rfl
  | succ n => exact le_sup_left

theorem term_map (n : ℕ) :
    (F K h (n+1)).map (K.d (n+1) n).hom = boundaryPart K n (F K h n) := by
  change (cyclePart K h (n+1) ⊔ boundaryLift K n (F K h n)
    (finiteTerm K h n).property).map (K.d (n+1) n).hom = _
  rw [Submodule.map_sup,(boundaryLift_spec K n _ _).2]
  have hz : (cyclePart K h (n+1)).map (K.d (n+1) n).hom = ⊥ := by
    apply eq_bot_iff.mpr
    rintro x ⟨y,hy,rfl⟩
    rw [Submodule.mem_bot]
    exact cyclePart_closed K h (n+1) hy
  rw [hz,bot_sup_eq]

theorem term_closed (n : ℕ) (x : F K h (n+1)) :
    K.d (n+1) n x.val ∈ F K h n := by
  have hx : K.d (n+1) n x.val ∈ (F K h (n+1)).map (K.d (n+1) n).hom :=
    ⟨x.val,x.property,rfl⟩
  rw [term_map] at hx
  exact hx.1

theorem term_fills (n : ℕ) (x : F K h n) (z : K.X (n+1))
    (hz : K.d (n+1) n z = x.val) :
    ∃ y : F K h (n+1), K.d (n+1) n y.val = x.val := by
  have hx : x.val ∈ boundaryPart K n (F K h n) := ⟨x.property,⟨z,hz⟩⟩
  rw [← term_map K h n] at hx
  obtain ⟨y,hy,he⟩ := hx
  exact ⟨⟨y,hy⟩,he⟩

#print axioms finite_lift
#print axioms term_map
#print axioms term_fills
end CMDG.CondensedCM5R0.BreenDeligneFiniteSubcomplex
