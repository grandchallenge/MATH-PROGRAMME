import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverGluing

/-!
# CMDG CM5 — relative locally constant extension across closed pairs

If A and B are closed in any profinite X, and locally constant
integer functions f on A and g on B agree on A∩B, then there exists
a globally locally constant h:X→ℤ extending both f and g.
The proof glues over the actual closed union A∪B using the protected
finite closed-cover pasting theorem, then extends from the closed union
to X. No assumption that the closed sets are clopen, and no choice
of a discontinuous quotient section, is made. This is a reusable
relative extension ingredient for the next H³ finite-family induction.
-/
noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem locallyConstant_extend_compatible_closed_pair
    (X : Profinite.{u}) (A B : Set X)
    (hA : IsClosed A) (hB : IsClosed B)
    (f : LocallyConstant A ℤ)
    (g : LocallyConstant B ℤ)
    (hfg : ∀ x : X, (ha : x ∈ A) → (hb : x ∈ B) →
      f ⟨x, ha⟩ = g ⟨x, hb⟩) :
    ∃ h : LocallyConstant X ℤ,
      (∀ a : A, h a.val = f a) ∧
      (∀ b : B, h b.val = g b) := by
  classical
  let U : Set X := A ∪ B
  have hU : IsClosed U := hA.union hB
  let E : Bool → Set U := fun t =>
    if t then {z : U | z.val ∈ A} else {z : U | z.val ∈ B}
  have hE : ∀ t, IsClosed (E t) := by
    intro t
    cases t with
    | false =>
      change IsClosed ((fun z : U => z.val) ⁻¹' B)
      exact hB.preimage continuous_subtype_val
    | true =>
      change IsClosed ((fun z : U => z.val) ⁻¹' A)
      exact hA.preimage continuous_subtype_val
  have hcover : (⋃ t, E t) = (Set.univ : Set U) := by
    ext z
    constructor
    · intro _; trivial
    · intro _
      rcases z.property with hz | hz
      · apply Set.mem_iUnion.mpr
        exact ⟨true, hz⟩
      · apply Set.mem_iUnion.mpr
        exact ⟨false, hz⟩
  let F : (t : Bool) → LocallyConstant (E t) ℤ := by
    intro t
    cases t with
    | false =>
      exact g.comap
        (⟨fun z => (⟨z.val.val, z.property⟩ : B),
          (continuous_subtype_val.comp continuous_subtype_val).subtype_mk _⟩ :
            C(E false, B))
    | true =>
      exact f.comap
        (⟨fun z => (⟨z.val.val, z.property⟩ : A),
          (continuous_subtype_val.comp continuous_subtype_val).subtype_mk _⟩ :
            C(E true, A))
  have hagree : ∀ (i j : Bool) (x : U)
      (hi : x ∈ E i) (hj : x ∈ E j),
      F i ⟨x, hi⟩ = F j ⟨x, hj⟩ := by
    intro i j x hi hj
    cases i <;> cases j
    · rfl
    · change g ⟨x.val, hi⟩ = f ⟨x.val, hj⟩
      exact (hfg x.val hj hi).symm
    · change f ⟨x.val, hi⟩ = g ⟨x.val, hj⟩
      exact hfg x.val hi hj
    · rfl
  obtain ⟨k, hk⟩ :=
    locallyConstant_glue_finite_closed_cover
      E hE hcover F hagree
  obtain ⟨h, hh⟩ :=
    locallyConstant_extend_closed_subset X U hU k
  refine ⟨h, ?_, ?_⟩
  · intro a
    let z : U := ⟨a.val, Or.inl a.property⟩
    have hz : z ∈ E true := a.property
    calc
      h a.val = k z := hh z
      _ = F true ⟨z, hz⟩ := hk true z hz
      _ = f a := by
        change f ⟨a.val, a.property⟩ = f a
        rfl
  · intro b
    let z : U := ⟨b.val, Or.inr b.property⟩
    have hz : z ∈ E false := b.property
    calc
      h b.val = k z := hh z
      _ = F false ⟨z, hz⟩ := hk false z hz
      _ = g b := by
        change g ⟨b.val, b.property⟩ = g b
        rfl

#print axioms locallyConstant_extend_compatible_closed_pair
end CMDG.CondensedCM5R0
