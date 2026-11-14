import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverGluing
import Mathlib.Topology.LocallyConstant.Algebra

/-!
# CM5: constructive H¹ vanishing for finite closed-cover scalar cocycles

For *every* finite family of closed subsets of an arbitrary profinite X,
an integer-valued locally constant 1-cocycle on the pairwise
intersections has a locally constant family of potentials.

This is a potential-EXISTENCE result, not a restatement of an
Ext-obstruction quotient. It uses finite induction, actual finite
closed-cover gluing, and extension from a closed subset of a profinite
space. It does NOT assume that a finite closed cover is a clopen cover.

We first prove a strong globally-defined-transitions version; then
we use the protected closed-subset extension theorem to eliminate
that global assumption and work with actual intersection cochains.

Outstanding: finite rectangular clopen refinement of a scalar
Stonean relation cochain; application of this lemma to the Stonean
Čech relation; comparison with genuine condensed discrete integer
coefficients; solid coefficient product model; higher derived
comparison. No unconditional ambient Ext¹ or derived solidity
is claimed by this file.
-/

noncomputable section

universe u v

open CategoryTheory Limits Set

namespace CMDG.CondensedCM5R0

/-- A compatible finite family of GLOBAL locally constant functions
on CLOSED subsets extends to one global function realizing every
prescribed restriction. The union need not cover X. -/
theorem locallyConstant_extend_finite_closed_family
    (X : Profinite.{u}) {J : Type v} [Finite J]
    (C : J → Set X)
    (hC : ∀ j, IsClosed (C j))
    (f : J → LocallyConstant X ℤ)
    (hcompat : ∀ (j k : J) (x : X),
      x ∈ C j → x ∈ C k → f j x = f k x) :
    ∃ g : LocallyConstant X ℤ,
      ∀ (j : J) (x : X), x ∈ C j → g x = f j x := by
  classical
  let H : Set X := ⋃ j, C j
  have hH : IsClosed H := isClosed_iUnion_of_finite hC
  let D : J → Set (↥H) := fun j => Subtype.val ⁻¹' C j
  have hD : ∀ j : J, IsClosed (D j) := by
    intro j
    exact (hC j).preimage continuous_subtype_val
  have hcover : (⋃ j, D j) = Set.univ := by
    ext x
    simp only [Set.mem_iUnion, Set.mem_univ, iff_true]
    change ∃ j, (x : X) ∈ C j
    simpa only [H, Set.mem_iUnion] using x.property
  let ff : (j : J) → LocallyConstant (D j) ℤ :=
    fun j => (f j).comap
      (⟨(fun x : D j => (x.val.val : X)),
        continuous_subtype_val.comp continuous_subtype_val⟩ :
        C(D j, X))
  have hff : ∀ (j k : J) (x : H)
      (hj : x ∈ D j) (hk : x ∈ D k),
      ff j ⟨x, hj⟩ = ff k ⟨x, hk⟩ := by
    intro j k x hj hk
    change f j x.val = f k x.val
    exact hcompat j k x.val hj hk
  obtain ⟨gH, hgH⟩ :=
    locallyConstant_glue_finite_closed_cover D hD hcover ff hff
  obtain ⟨g, hg⟩ := locallyConstant_extend_closed_subset X H hH gH
  refine ⟨g, ?_⟩
  intro j x hx
  have hxH : x ∈ H := Set.mem_iUnion.mpr ⟨j, hx⟩
  calc
    g x = gH ⟨x, hxH⟩ := hg ⟨x, hxH⟩
    _ = ff j ⟨⟨x, hxH⟩, hx⟩ := hgH j ⟨x, hxH⟩ hx
    _ = f j x := rfl

/-- Constructive finite-closed-family H¹ vanishing, first for
transition functions that are locally constant on the AMBIENT
profinite space and only satisfy the cocycle law on triple
intersections. There is no cover or nonemptiness hypothesis. -/
theorem integerFiniteClosedFamily_globalTransitions_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : I → I → LocallyConstant X ℤ)
    (hc : ∀ (i j k : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k →
        c i k x = c i j x + c j k x) :
    ∃ a : I → LocallyConstant X ℤ,
      ∀ (i j : I) (x : X),
        x ∈ E i → x ∈ E j → c i j x = a i x - a j x := by
  classical
  have cdiag (i : I) (x : X) (hi : x ∈ E i) :
      c i i x = 0 := by
    have h := hc i i i x hi hi hi
    omega
  have canti (i j : I) (x : X) (hi : x ∈ E i) (hj : x ∈ E j) :
      c i j x = - c j i x := by
    have h := hc i j i x hi hj hi
    have hz := cdiag i x hi
    omega
  have aux : ∀ s : Finset I,
      ∃ a : I → LocallyConstant X ℤ,
        ∀ (i : I), i ∈ s →
          ∀ (j : I), j ∈ s →
            ∀ (x : X), x ∈ E i → x ∈ E j →
              c i j x = a i x - a j x := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      refine ⟨fun _ => LocallyConstant.const X 0, ?_⟩
      intro i hi
      simp at hi
    | @insert i s hnot ih =>
      obtain ⟨a, ha⟩ := ih
      let J := {j : I // j ∈ s}
      let C : J → Set X := fun j => E i ∩ E j.val
      have hC : ∀ j : J, IsClosed (C j) := by
        intro j
        exact (hclosed i).inter (hclosed j.val)
      let f : J → LocallyConstant X ℤ :=
        fun j => a j.val - c j.val i
      have hcompat (j k : J) (x : X)
          (hj : x ∈ C j) (hk : x ∈ C k) :
          f j x = f k x := by
        rcases hj with ⟨hiX, hjX⟩
        rcases hk with ⟨_, hkX⟩
        have hprev := ha j.val j.property k.val k.property x hjX hkX
        have htrans := hc j.val k.val i x hjX hkX hiX
        change a j.val x - c j.val i x =
          a k.val x - c k.val i x
        rw [htrans, hprev]
        abel
      obtain ⟨b, hb⟩ :=
        locallyConstant_extend_finite_closed_family X C hC f hcompat
      refine ⟨fun j => if j = i then b else a j, ?_⟩
      intro j hj k hk x hxj hxk
      by_cases hji : j = i
      · subst j
        by_cases hki : k = i
        · subst k
          simpa using (cdiag i x hxj)
        · have hks : k ∈ s := (Finset.mem_insert.mp hk).resolve_left hki
          have hbk := hb (⟨k, hks⟩ : J) x ⟨hxj, hxk⟩
          change b x = a k x - c k i x at hbk
          have hanti := canti i k x hxj hxk
          have : c i k x = b x - a k x := by omega
          simpa [hki] using this
      · have hjs : j ∈ s := (Finset.mem_insert.mp hj).resolve_left hji
        by_cases hki : k = i
        · subst k
          have hbj := hb (⟨j, hjs⟩ : J) x ⟨hxk, hxj⟩
          change b x = a j x - c j i x at hbj
          have : c j i x = a j x - b x := by omega
          simpa [hji] using this
        · have hks : k ∈ s := (Finset.mem_insert.mp hk).resolve_left hki
          have hprev := ha j hjs k hks x hxj hxk
          simpa [hji, hki] using hprev
  obtain ⟨a, ha⟩ := aux Finset.univ
  refine ⟨a, ?_⟩
  intro i j x hi hj
  exact ha i (Finset.mem_univ i) j (Finset.mem_univ j) x hi hj

/-- **Actual finite closed-cover scalar cocycle induction.**
The transition cochains are locally constant only on their
respective closed INTERSECTIONS, and the cocycle law is required
only on triple overlaps. The theorem constructs genuine globally
locally constant potentials; the family need not cover X.

This is the finite-stage potential EXISTENCE theorem needed for
the scalar Stonean Čech argument, not a formal equivalence to
vanishing of Ext. -/
theorem integerFiniteClosedFamily_cocycle_is_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : (i j : I) → LocallyConstant (↥(E i ∩ E j)) ℤ)
    (hc : ∀ (i j k : I) (x : X)
      (hi : x ∈ E i) (hj : x ∈ E j) (hk : x ∈ E k),
      c i k ⟨x, ⟨hi, hk⟩⟩ =
        c i j ⟨x, ⟨hi, hj⟩⟩ +
          c j k ⟨x, ⟨hj, hk⟩⟩) :
    ∃ a : I → LocallyConstant X ℤ,
      ∀ (i j : I) (x : X)
        (hi : x ∈ E i) (hj : x ∈ E j),
        c i j ⟨x, ⟨hi, hj⟩⟩ = a i x - a j x := by
  classical
  have hext (i j : I) :
      ∃ g : LocallyConstant X ℤ,
        ∀ x : ↥(E i ∩ E j), g x.val = c i j x := by
    exact locallyConstant_extend_closed_subset X (E i ∩ E j)
      ((hclosed i).inter (hclosed j)) (c i j)
  choose C hC using hext
  have htrans : ∀ (i j k : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k →
        C i k x = C i j x + C j k x := by
    intro i j k x hi hj hk
    have hik := hC i k (⟨x, ⟨hi, hk⟩⟩ : ↥(E i ∩ E k))
    have hij := hC i j (⟨x, ⟨hi, hj⟩⟩ : ↥(E i ∩ E j))
    have hjk := hC j k (⟨x, ⟨hj, hk⟩⟩ : ↥(E j ∩ E k))
    rw [hik, hij, hjk]
    exact hc i j k x hi hj hk
  obtain ⟨a, ha⟩ :=
    integerFiniteClosedFamily_globalTransitions_coboundary
      X E hclosed C htrans
  refine ⟨a, ?_⟩
  intro i j x hi hj
  have h := hC i j (⟨x, ⟨hi, hj⟩⟩ : ↥(E i ∩ E j))
  rw [← h]
  exact ha i j x hi hj

#print axioms locallyConstant_extend_finite_closed_family
#print axioms integerFiniteClosedFamily_globalTransitions_coboundary
#print axioms integerFiniteClosedFamily_cocycle_is_coboundary

end CMDG.CondensedCM5R0
