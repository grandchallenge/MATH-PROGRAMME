import CMDGCondensedCM4P3DerivedCM5R0FiniteFiberCocycle

/-!
# CM5: finite Čech potentials and their coherence under refinement

For a commuting square of surjections with a refined source and base,
pullback of a fiberwise additive cocycle preserves the cocycle law.
Its two *canonical* fiber-section potentials need not be literally
equal; their difference is an explicit base-side gauge.

The gauge is unique because the refined covering map is surjective.
For composable refinements, the resulting gauge corrections satisfy
the strict additive composition law. This is the finite-stage descent
compatibility calculation needed before attempting inverse-limit
potential constructions.

No inverse-limit compatibility is assumed or proved. These are
set-valued algebraic finite-stage statements: there is no assertion
that arbitrary condensed-module morphisms are represented by such
finite cocycles, or that arbitrary-profinite Ext¹ vanishes.
-/

noncomputable section

universe u v u' v' u'' v'' w

namespace CMDG.CondensedCM5R0

variable {α : Type u} {β : Type v}
  {α' : Type u'} {β' : Type v'}
  {M : Type w} [AddCommGroup M]

/-- A commuting refinement square sends pairs in a fiber of the
refined map to pairs in a fiber of the original map. -/
theorem fiberRefinement_preserves_fibers
    (p : α → β) (p' : α' → β')
    (r : α' → α) (s : β' → β)
    (hcomm : ∀ x : α', p (r x) = s (p' x))
    {x y : α'} (hxy : p' x = p' y) :
    p (r x) = p (r y) := by
  calc
    p (r x) = s (p' x) := hcomm x
    _ = s (p' y) := congrArg s hxy
    _ = p (r y) := (hcomm y).symm

/-- Pulling back a cocycle along a commuting refinement square
preserves the fiberwise cocycle identity. -/
theorem fiberCocycle_refinement_cocycle
    (p : α → β) (p' : α' → β')
    (r : α' → α) (s : β' → β)
    (hcomm : ∀ x : α', p (r x) = s (p' x))
    (c : α → α → M)
    (hc : ∀ x y z : α, p x = p y → p y = p z →
      c x z = c x y + c y z) :
    ∀ x y z : α', p' x = p' y → p' y = p' z →
      c (r x) (r z) = c (r x) (r y) + c (r y) (r z) := by
  intro x y z hxy hyz
  exact hc (r x) (r y) (r z)
    (fiberRefinement_preserves_fibers p p' r s hcomm hxy)
    (fiberRefinement_preserves_fibers p p' r s hcomm hyz)

/-- Under a commuting finite-stage refinement the canonical
section-based potential of the pulled-back cocycle differs from
the pullback of the original potential by a base-side gauge.
All types are unrestricted to keep the algebraic lemma reusable;
for finite discrete stages the sections are automatically continuous. -/
theorem fiberCocycle_refinement_potential_gauge
    (p : α → β) (hp : Function.Surjective p)
    (p' : α' → β') (hp' : Function.Surjective p')
    (r : α' → α) (s : β' → β)
    (hcomm : ∀ x : α', p (r x) = s (p' x))
    (c : α → α → M)
    (hc : ∀ x y z : α, p x = p y → p y = p z →
      c x z = c x y + c y z) :
    ∃ d : β' → M, ∀ x : α',
      fiberCocyclePotential p' hp'
          (fun a b => c (r a) (r b)) x =
        fiberCocyclePotential p hp c (r x) + d (p' x) := by
  let c' : α' → α' → M := fun x y => c (r x) (r y)
  let b : α → M := fiberCocyclePotential p hp c
  let b' : α' → M := fiberCocyclePotential p' hp' c'
  have hc' : ∀ x y z : α', p' x = p' y → p' y = p' z →
      c' x z = c' x y + c' y z :=
    fiberCocycle_refinement_cocycle p p' r s hcomm c hc
  have hb' : ∀ x y : α', p' x = p' y →
      c' x y = b' x - b' y := by
    intro x y hxy
    exact fiberCocyclePotential_coboundary p' hp' c' hc' x y hxy
  have hb : ∀ x y : α', p' x = p' y →
      c' x y = b (r x) - b (r y) := by
    intro x y hxy
    exact fiberCocyclePotential_coboundary p hp c hc
      (r x) (r y)
      (fiberRefinement_preserves_fibers p p' r s hcomm hxy)
  exact fiberCocyclePotentials_gauge p' hp' c' b'
    (fun x => b (r x)) hb' hb

/-- A gauge between fixed potentials is uniquely determined on the
quotient when the covering map is surjective. -/
theorem fiberPotential_gauge_unique
    (p : α → β) (hp : Function.Surjective p)
    (b b' : α → M) (d d' : β → M)
    (hd : ∀ x : α, b x = b' x + d (p x))
    (hd' : ∀ x : α, b x = b' x + d' (p x)) :
    d = d' := by
  funext t
  obtain ⟨x, hx⟩ := hp t
  have h : b' x + d (p x) = b' x + d' (p x) :=
    (hd x).symm.trans (hd' x)
  have heq : d (p x) = d' (p x) := add_left_cancel h
  simpa only [hx] using heq

/-- For a tower of two finite refinements, any three correctly
defined base-side gauge corrections necessarily compose additively.
This is the strict coherence law needed when comparing finite-level
potentials along a directed system. It does not construct a coherent
infinite family. -/
theorem fiberRefinement_gauge_compose
    {α₀ : Type u} {β₁ : Type v'}
    {α₁ : Type u'} {α₂ : Type u''} {β₂ : Type v''}
    (p₁ : α₁ → β₁) (p₂ : α₂ → β₂)
    (hp₂ : Function.Surjective p₂)
    (r₁₀ : α₁ → α₀) (r₂₁ : α₂ → α₁)
    (s₂₁ : β₂ → β₁)
    (hcomm₂₁ : ∀ x : α₂, p₁ (r₂₁ x) = s₂₁ (p₂ x))
    (b₀ : α₀ → M) (b₁ : α₁ → M) (b₂ : α₂ → M)
    (d₁₀ : β₁ → M) (d₂₁ d₂₀ : β₂ → M)
    (h₁₀ : ∀ x : α₁,
      b₁ x = b₀ (r₁₀ x) + d₁₀ (p₁ x))
    (h₂₁ : ∀ x : α₂,
      b₂ x = b₁ (r₂₁ x) + d₂₁ (p₂ x))
    (h₂₀ : ∀ x : α₂,
      b₂ x = b₀ (r₁₀ (r₂₁ x)) + d₂₀ (p₂ x)) :
    ∀ t : β₂, d₂₀ t = d₁₀ (s₂₁ t) + d₂₁ t := by
  intro t
  obtain ⟨x, hx⟩ := hp₂ t
  have h :
      b₀ (r₁₀ (r₂₁ x)) + d₂₀ (p₂ x) =
        b₀ (r₁₀ (r₂₁ x)) +
          (d₁₀ (s₂₁ (p₂ x)) + d₂₁ (p₂ x)) := by
    calc
      b₀ (r₁₀ (r₂₁ x)) + d₂₀ (p₂ x) =
          b₂ x := (h₂₀ x).symm
      _ = b₁ (r₂₁ x) + d₂₁ (p₂ x) := h₂₁ x
      _ = (b₀ (r₁₀ (r₂₁ x)) + d₁₀ (p₁ (r₂₁ x))) +
          d₂₁ (p₂ x) := by rw [h₁₀ (r₂₁ x)]
      _ = b₀ (r₁₀ (r₂₁ x)) +
          (d₁₀ (s₂₁ (p₂ x)) + d₂₁ (p₂ x)) := by
          rw [hcomm₂₁ x]
          abel
  have hd : d₂₀ (p₂ x) =
      d₁₀ (s₂₁ (p₂ x)) + d₂₁ (p₂ x) := add_left_cancel h
  simpa only [hx] using hd

#print axioms fiberRefinement_preserves_fibers
#print axioms fiberCocycle_refinement_cocycle
#print axioms fiberCocycle_refinement_potential_gauge
#print axioms fiberPotential_gauge_unique
#print axioms fiberRefinement_gauge_compose

end CMDG.CondensedCM5R0
