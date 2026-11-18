import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverCocycleInduction

/-!
# CMDG CM5 — finite closed-family scalar Čech H² vanishing

For an arbitrary profinite X and an arbitrary finite family (E_i) of
closed subsets (no open-cover, cover, or nonempty intersection assumption),
a locally constant integer Čech two-cocycle on genuine TRIPLE overlaps
has a primitive consisting of globally locally constant pair cochains.
The differential convention is
  (δb)_{ijk} = b_{jk} - b_{ik} + b_{ij}.
The four-index cocycle law is the actual alternating degree-three boundary.

The proof first contracts globally defined triple transition functions via
finite induction. On adjoining index i, the discrepancy b_{jk}-c_{jki}
is a genuine closed-cover one-cocycle on (E_j ∩ E_i), so the already
protected finite closed-family H¹ theorem supplies the needed potentials.
Repeated-index cases are handled explicitly (not silently normalized).
The general result then extends each locally constant triple-overlap
cochain from its closed domain and invokes the global-transition theorem.

This is a substantive scalar finite-closed-family H² result. It does NOT
assert continuous sections of arbitrary profinite quotients, scalar H²
acyclicity of their actual Čech nerves without the finite-observation
reduction, Ext² vanishing for condensed-module targets, derived solidity,
or mathematical certification. Those interfaces remain open.
-/

noncomputable section

universe u v

open CategoryTheory Limits Set

namespace CMDG.CondensedCM5R0

/-- Every *globally-defined*, locally constant integer-valued 2-cocycle
on the nerve of a finite closed family is a Cech coboundary on all triple
intersections. The family need not cover X. -/
theorem integerFiniteClosedFamily_globalTwoCocycle_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : I → I → I → LocallyConstant X ℤ)
    (hc : ∀ (i j k l : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l →
      c j k l x - c i k l x + c i j l x - c i j k x = 0) :
    ∃ b : I → I → LocallyConstant X ℤ,
      ∀ (i j k : I) (x : X),
        x ∈ E i → x ∈ E j → x ∈ E k →
        c i j k x = b j k x - b i k x + b i j x := by
  classical
  have aux : ∀ s : Finset I,
      ∃ b : I → I → LocallyConstant X ℤ,
        ∀ (j k l : I), j ∈ s → k ∈ s → l ∈ s →
          ∀ (x : X), x ∈ E j → x ∈ E k → x ∈ E l →
            c j k l x = b k l x - b j l x + b j k x := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
        refine ⟨fun _ _ => LocallyConstant.const X 0, ?_⟩
        intro j k l hj
        simp at hj
    | @insert i s hnot ih =>
        obtain ⟨b, hb⟩ := ih
        let D : I → Set X := fun j =>
          if j ∈ s then E j ∩ E i else ∅
        have hD : ∀ j, IsClosed (D j) := by
          intro j
          by_cases hj : j ∈ s
          · simpa [D, hj] using (hclosed j).inter (hclosed i)
          · simp [D, hj]
        let w : I → I → LocallyConstant X ℤ :=
          fun j k => b j k - c j k i
        have hmem (j : I) (x : X) (hj : x ∈ D j) :
            j ∈ s ∧ x ∈ E j ∧ x ∈ E i := by
          by_cases hjs : j ∈ s
          · simpa [D, hjs] using And.intro hjs (show x ∈ E j ∩ E i from by simpa [D, hjs] using hj)
          · simp [D, hjs] at hj
        have hinto (j : I) (x : X) (hjs : j ∈ s)
            (hj : x ∈ E j) (hi : x ∈ E i) : x ∈ D j := by
          simp [D, hjs, hj, hi]
        have hw : ∀ (j k l : I) (x : X),
            x ∈ D j → x ∈ D k → x ∈ D l →
            w j l x = w j k x + w k l x := by
          intro j k l x hj hk hl
          obtain ⟨hjs, hjx, hix⟩ := hmem j x hj
          obtain ⟨hks, hkx, _⟩ := hmem k x hk
          obtain ⟨hls, hlx, _⟩ := hmem l x hl
          have hh := hb j k l hjs hks hls x hjx hkx hlx
          have hcc := hc j k l i x hjx hkx hlx hix
          change c j k l x = b k l x - b j l x + b j k x at hh
          change c k l i x - c j l i x + c j k i x -
              c j k l x = 0 at hcc
          change b j l x - c j l i x =
            (b j k x - c j k i x) + (b k l x - c k l i x)
          omega
        obtain ⟨a, ha⟩ :=
          integerFiniteClosedFamily_globalTransitions_coboundary
            X D hD w hw
        let B : I → I → LocallyConstant X ℤ := fun j k =>
          if j = i then
            if k = i then c i i i else c i k i + c i i i - a k
          else if k = i then a j else b j k
        refine ⟨B, ?_⟩
        intro j k l hj hk hl x hjx hkx hlx
        have hjs (h : j ≠ i) : j ∈ s :=
          (Finset.mem_insert.mp hj).resolve_left h
        have hks (h : k ≠ i) : k ∈ s :=
          (Finset.mem_insert.mp hk).resolve_left h
        have hls (h : l ≠ i) : l ∈ s :=
          (Finset.mem_insert.mp hl).resolve_left h
        by_cases hji : j = i
        · subst j
          by_cases hki : k = i
          · subst k
            by_cases hli : l = i
            · subst l
              simp [B]
            · have hcc := hc i i i l x hjx hjx hjx hlx
              simp [B, hli] at *
              omega
          · by_cases hli : l = i
            · subst l
              simp [B, hki]
              change c i k i x =
                a k x - c i i i x +
                  (c i k i x + c i i i x - a k x)
              omega
            · have hA := ha k l x
                (hinto k x (hks hki) hkx hjx)
                (hinto l x (hls hli) hlx hjx)
              have hcc := hc i k l i x hjx hkx hlx hjx
              change b k l x - c k l i x = a k x - a l x at hA
              simp [B, hki, hli]
              change c i k l x =
                b k l x -
                  (c i l i x + c i i i x - a l x) +
                  (c i k i x + c i i i x - a k x)
              omega
        · by_cases hki : k = i
          · subst k
            by_cases hli : l = i
            · subst l
              have hcc := hc j i i i x hjx hkx hkx hkx
              simp [B, hji] at *
              omega
            · have hA := ha j l x
                (hinto j x (hjs hji) hjx hkx)
                (hinto l x (hls hli) hlx hkx)
              have hc1 := hc j i l i x hjx hkx hlx hkx
              have hc2 := hc j i i i x hjx hkx hkx hkx
              change b j l x - c j l i x = a j x - a l x at hA
              simp [B, hji, hli]
              change c j i l x =
                (c i l i x + c i i i x - a l x) - b j l x + a j x
              omega
          · by_cases hli : l = i
            · subst l
              have hA := ha j k x
                (hinto j x (hjs hji) hjx hlx)
                (hinto k x (hks hki) hkx hlx)
              change b j k x - c j k i x = a j x - a k x at hA
              simp [B, hji, hki]
              omega
            · have hh := hb j k l (hjs hji) (hks hki) (hls hli)
                  x hjx hkx hlx
              simpa [B, hji, hki, hli] using hh
  obtain ⟨b, hb⟩ := aux Finset.univ
  refine ⟨b, ?_⟩
  intro i j k x hi hj hk
  exact hb i j k (Finset.mem_univ _) (Finset.mem_univ _)
    (Finset.mem_univ _) x hi hj hk


/-- Finite *closed-overlap* H² vanishing: the 2-cocycle is required to
be locally constant only on its genuine triple intersections.
The primitive is represented by globally locally constant pair cochains. -/
theorem integerFiniteClosedFamily_twoCocycle_is_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : (i j k : I) →
      LocallyConstant (↥((E i ∩ E j) ∩ E k)) ℤ)
    (hc : ∀ (i j k l : I) (x : X)
      (hi : x ∈ E i) (hj : x ∈ E j)
      (hk : x ∈ E k) (hl : x ∈ E l),
        c j k l ⟨x, ⟨⟨hj, hk⟩, hl⟩⟩ -
        c i k l ⟨x, ⟨⟨hi, hk⟩, hl⟩⟩ +
        c i j l ⟨x, ⟨⟨hi, hj⟩, hl⟩⟩ -
        c i j k ⟨x, ⟨⟨hi, hj⟩, hk⟩⟩ = 0) :
    ∃ b : I → I → LocallyConstant X ℤ,
      ∀ (i j k : I) (x : X)
        (hi : x ∈ E i) (hj : x ∈ E j) (hk : x ∈ E k),
        c i j k ⟨x, ⟨⟨hi, hj⟩, hk⟩⟩ =
          b j k x - b i k x + b i j x := by
  classical
  have hext (i j k : I) :
      ∃ C : LocallyConstant X ℤ,
        ∀ x : ↥((E i ∩ E j) ∩ E k),
          C x.val = c i j k x := by
    exact locallyConstant_extend_closed_subset X
      ((E i ∩ E j) ∩ E k)
      (((hclosed i).inter (hclosed j)).inter (hclosed k))
      (c i j k)
  choose C hC using hext
  have hc' : ∀ (i j k l : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l →
      C j k l x - C i k l x + C i j l x - C i j k x = 0 := by
    intro i j k l x hi hj hk hl
    rw [hC j k l ⟨x, ⟨⟨hj, hk⟩, hl⟩⟩,
      hC i k l ⟨x, ⟨⟨hi, hk⟩, hl⟩⟩,
      hC i j l ⟨x, ⟨⟨hi, hj⟩, hl⟩⟩,
      hC i j k ⟨x, ⟨⟨hi, hj⟩, hk⟩⟩]
    exact hc i j k l x hi hj hk hl
  obtain ⟨b, hb⟩ :=
    integerFiniteClosedFamily_globalTwoCocycle_coboundary
      X E hclosed C hc'
  refine ⟨b, ?_⟩
  intro i j k x hi hj hk
  rw [← hC i j k ⟨x, ⟨⟨hi, hj⟩, hk⟩⟩]
  exact hb i j k x hi hj hk

#print axioms integerFiniteClosedFamily_globalTwoCocycle_coboundary
#print axioms integerFiniteClosedFamily_twoCocycle_is_coboundary

end CMDG.CondensedCM5R0
