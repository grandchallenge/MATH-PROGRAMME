import CMDGCondensedCM4P3DerivedCM5R0KernelHomExtension
import Mathlib.Algebra.Group.Defs
import Mathlib.Data.Fintype.Basic

/-!
# CM5: explicit finite-fiber integer-product cocycle primitives

This is an algebraic building block for constructing kernel extensions
into the source-pinned product-of-integers coefficient model.

For a surjective finite map p : α → β, a group-valued 1-cocycle
c(x,y) on pairs in a common p-fiber is the coboundary of an explicit
potential b(x) := c(x,s(p(x))), where s is a chosen section of p.

The result holds for arbitrary additive abelian coefficient groups,
notably products of copies of ℤ with arbitrary index type.  The
discrete finite-stage case does not require a continuity argument.

**Open bridge:** for arbitrary profinite T, the actual condensed
kernel map K_T → G_S must first be represented by compatible such
finite-fiber cocycles, and the resulting potentials must descend
compatibly in the condensed site. This theorem alone does not give
that representation or prove arbitrary-profinite Ext¹ vanishing.
-/

noncomputable section

universe u v w

namespace CMDG.CondensedCM5R0

variable {α : Type u} {β : Type v} {M : Type w} [AddCommGroup M]

/-- A chosen section of a surjection. At finite discrete stages this
selection is automatically continuous. -/
noncomputable def fiberSection (p : α → β) (hp : Function.Surjective p) :
    β → α :=
  fun b => Classical.choose (hp b)

theorem fiberSection_spec (p : α → β) (hp : Function.Surjective p) (b : β) :
    p (fiberSection p hp b) = b :=
  Classical.choose_spec (hp b)

/-- Explicit candidate potential for a cocycle on a surjection's
equivalence relation. -/
noncomputable def fiberCocyclePotential
    (p : α → β) (hp : Function.Surjective p) (c : α → α → M) :
    α → M :=
  fun x => c x (fiberSection p hp (p x))

/-- The constructive fiberwise coboundary identity, valid for any
additive abelian coefficient group. -/
theorem fiberCocyclePotential_coboundary
    (p : α → β) (hp : Function.Surjective p)
    (c : α → α → M)
    (hc : ∀ x y z : α, p x = p y → p y = p z →
      c x z = c x y + c y z)
    (x y : α) (hxy : p x = p y) :
    c x y =
      fiberCocyclePotential p hp c x -
        fiberCocyclePotential p hp c y := by
  have hz : p y = p (fiberSection p hp (p x)) := by
    calc
      p y = p x := hxy.symm
      _ = p (fiberSection p hp (p x)) :=
        (fiberSection_spec p hp (p x)).symm
  have h := hc x y (fiberSection p hp (p x)) hxy hz
  have hs : fiberSection p hp (p x) = fiberSection p hp (p y) :=
    congrArg (fiberSection p hp) hxy
  change c x y = c x (fiberSection p hp (p x)) -
    c y (fiberSection p hp (p y))
  rw [← hs]
  exact eq_sub_iff_add_eq.mpr h.symm

/-- Finite-fiber cocycles with arbitrary products of integer
coefficients have explicitly constructed simultaneous potentials.
No restriction on the number of integer coordinates. -/
theorem finiteFiberIntegerProduct_cocycle_is_coboundary
    {ι : Type w}
    [Fintype α] [Fintype β]
    (p : α → β) (hp : Function.Surjective p)
    (c : α → α → (ι → ℤ))
    (hc : ∀ x y z : α, p x = p y → p y = p z →
      c x z = c x y + c y z) :
    ∃ b : α → (ι → ℤ),
      ∀ x y, p x = p y → c x y = b x - b y := by
  refine ⟨fiberCocyclePotential p hp c, ?_⟩
  intro x y hxy
  exact fiberCocyclePotential_coboundary p hp c hc x y hxy

/-- Two potentials with the same fiberwise coboundary differ by
a function pulled back from the quotient. The explicit base-side
correction is obtained by evaluating their difference on a chosen
section of the quotient.

This is the finite-refinement gauge freedom needed when arranging
compatible potentials across finite quotients. It makes no assertion
that compatible potentials exist across an *infinite* inverse system.
-/
theorem fiberCocyclePotentials_gauge
    (p : α → β) (hp : Function.Surjective p)
    (c : α → α → M)
    (b b' : α → M)
    (hb : ∀ x y, p x = p y → c x y = b x - b y)
    (hb' : ∀ x y, p x = p y → c x y = b' x - b' y) :
    ∃ d : β → M, ∀ x : α, b x = b' x + d (p x) := by
  let s : β → α := fiberSection p hp
  refine ⟨fun t => b (s t) - b' (s t), ?_⟩
  intro x
  have hxs : p x = p (s (p x)) := by
    exact (fiberSection_spec p hp (p x)).symm
  have h1 := hb x (s (p x)) hxs
  have h2 := hb' x (s (p x)) hxs
  have heq : b x - b (s (p x)) = b' x - b' (s (p x)) :=
    h1.symm.trans h2
  change b x = b' x + (b (s (p x)) - b' (s (p x)))
  calc
    b x = (b x - b (s (p x))) + b (s (p x)) := by abel
    _ = (b' x - b' (s (p x))) + b (s (p x)) := by rw [heq]
    _ = b' x + (b (s (p x)) - b' (s (p x))) := by abel

#print axioms fiberCocyclePotentials_gauge
#print axioms fiberCocyclePotential_coboundary
#print axioms finiteFiberIntegerProduct_cocycle_is_coboundary

end CMDG.CondensedCM5R0
