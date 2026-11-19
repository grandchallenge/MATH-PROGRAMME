import CMDGCondensedCM4P3DerivedCM5R0ClosedQuadrupleScalarExtension
import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverH2CocycleInduction

/-!
# CMDG CM5 — finite closed-family scalar Čech H³ vanishing

For ANY profinite X and ANY finite family of closed subsets E_i,
not necessarily open, covering, or nonempty, every locally
constant integer-valued Čech 3-cocycle on genuine FOURFOLD
intersections is a coboundary of globally locally constant
triple-indexed 2-cochains. All repeated-index cases are included.

The mathematical proof constructs the global-cochain theorem
by induction on a finite subfamily. To adjoin index i, restrict
to the closed intersections D_j=E_j∩E_i. The degree-three
cocycle identity and previous primitive imply that
w_jkl=b_jkl-c_ijkl is a degree-two cocycle on D, so the
already protected finite-closed-family H² theorem supplies
a two-index primitive a_jk. For every triple containing the
new index i, define the new cochain from the cone formula
c_ijkl + (δa)_jkl; on the old triple faces keep b_jkl.
The H² witness makes these formulas agree on all overlaps.
A uniform four-face identity using the five-point H³
cocycle law resolves ALL index patterns, including repeats.

The local-fourfold-cochain theorem then extends cochains
from each closed fourfold domain to X, applies global
induction, and restricts the resulting primitive.

No arbitrary-profinite H³ acyclicity, finite fourfold
observation, global module Hom lift, Ext³ vanishing, or
derived solidity is asserted. These are separate obligations.
-/

noncomputable section
universe u v
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem integerFiniteClosedFamily_globalThreeCocycle_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : I → I → I → I → LocallyConstant X ℤ)
    (hc : ∀ (i j k l m : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l → x ∈ E m →
      c j k l m x - c i k l m x + c i j l m x -
        c i j k m x + c i j k l x = 0) :
    ∃ b : I → I → I → LocallyConstant X ℤ,
      ∀ (i j k l : I) (x : X),
        x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l →
        c i j k l x =
          b j k l x - b i k l x + b i j l x - b i j k x := by
  classical
  have aux : ∀ s : Finset I,
      ∃ b : I → I → I → LocallyConstant X ℤ,
        ∀ (j k l m : I), j ∈ s → k ∈ s → l ∈ s → m ∈ s →
          ∀ x : X, x ∈ E j → x ∈ E k → x ∈ E l → x ∈ E m →
            c j k l m x =
              b k l m x - b j l m x + b j k m x - b j k l x := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      refine ⟨fun _ _ _ => LocallyConstant.const X 0, ?_⟩
      intro j k l m hj
      simp at hj
    | @insert i s hnot ih =>
      obtain ⟨b, hb⟩ := ih
      let D : I → Set X := fun j => if j ∈ s then E j ∩ E i else ∅
      have hD : ∀ j, IsClosed (D j) := by
        intro j
        by_cases hj : j ∈ s
        · simpa [D, hj] using (hclosed j).inter (hclosed i)
        · simp [D, hj]
      let w : I → I → I → LocallyConstant X ℤ :=
        fun j k l => b j k l - c i j k l
      have hmem (j : I) (x : X) (hj : x ∈ D j) :
          j ∈ s ∧ x ∈ E j ∧ x ∈ E i := by
        by_cases hjs : j ∈ s
        · simpa [D, hjs] using
            (And.intro hjs (show x ∈ E j ∩ E i from by
              simpa [D,hjs] using hj))
        · simp [D,hjs] at hj
      have hinto (j : I) (x : X) (hjs : j ∈ s)
          (hj : x ∈ E j) (hi : x ∈ E i) : x ∈ D j := by
        simp [D, hjs, hj, hi]
      have hw : ∀ (j k l m : I) (x : X),
          x ∈ D j → x ∈ D k → x ∈ D l → x ∈ D m →
          w k l m x - w j l m x + w j k m x - w j k l x = 0 := by
        intro j k l m x hj hk hl hm
        obtain ⟨hjs, hjx, hix⟩ := hmem j x hj
        obtain ⟨hks, hkx, _⟩ := hmem k x hk
        obtain ⟨hls, hlx, _⟩ := hmem l x hl
        obtain ⟨hms, hmx, _⟩ := hmem m x hm
        have hOld := hb j k l m hjs hks hls hms x hjx hkx hlx hmx
        have hC := hc i j k l m x hix hjx hkx hlx hmx
        change c j k l m x =
          b k l m x - b j l m x + b j k m x - b j k l x at hOld
        change c j k l m x - c i k l m x + c i j l m x -
          c i j k m x + c i j k l x = 0 at hC
        change (b k l m x - c i k l m x) -
          (b j l m x - c i j l m x) +
          (b j k m x - c i j k m x) -
          (b j k l x - c i j k l x) = 0
        omega
      obtain ⟨a, ha⟩ :=
        integerFiniteClosedFamily_globalTwoCocycle_coboundary X D hD w hw
      let δa (j k l : I) : LocallyConstant X ℤ :=
        a k l - a j l + a j k
      let B (j k l : I) : LocallyConstant X ℤ :=
        if j ∈ s ∧ k ∈ s ∧ l ∈ s then b j k l
        else c i j k l + δa j k l
      refine ⟨B, ?_⟩
      intro j k l m hj hk hl hm x hjx hkx hlx hmx
      have hi_of_not_s (r : I) (hr : r ∈ insert i s)
          (hrns : r ∉ s) : r = i :=
        (Finset.mem_insert.mp hr).resolve_right hrns
      have hcase : i = j ∨ i = k ∨ i = l ∨ i = m ∨
          (j ∈ s ∧ k ∈ s ∧ l ∈ s ∧ m ∈ s) := by
        by_cases hjs : j ∈ s
        · by_cases hks : k ∈ s
          · by_cases hls : l ∈ s
            · by_cases hms : m ∈ s
              · exact Or.inr (Or.inr (Or.inr (Or.inr
                  ⟨hjs,hks,hls,hms⟩)))
              · exact Or.inr (Or.inr (Or.inr
                  (Or.inl (hi_of_not_s m hm hms).symm)))
            · exact Or.inr (Or.inr
                (Or.inl (hi_of_not_s l hl hls).symm))
          · exact Or.inr (Or.inl (hi_of_not_s k hk hks).symm)
        · exact Or.inl (hi_of_not_s j hj hjs).symm
      have hFace (r t u : I)
          (hr : r ∈ insert i s) (ht : t ∈ insert i s)
          (hu : u ∈ insert i s)
          (hrx : x ∈ E r) (htx : x ∈ E t) (hux : x ∈ E u)
          (hix : x ∈ E i) :
          B r t u x = c i r t u x + δa r t u x := by
        by_cases hrtu : r ∈ s ∧ t ∈ s ∧ u ∈ s
        · have ha' := ha r t u x
            (hinto r x hrtu.1 hrx hix)
            (hinto t x hrtu.2.1 htx hix)
            (hinto u x hrtu.2.2 hux hix)
          change b r t u x - c i r t u x =
            a t u x - a r u x + a r t x at ha'
          change B r t u x = c i r t u x +
            (a t u x - a r u x + a r t x)
          simp only [B, if_pos hrtu]
          omega
        · change B r t u x = c i r t u x +
            (a t u x - a r u x + a r t x)
          simp [B, hrtu, δa, LocallyConstant.sub_apply]
      have hNew (hix : x ∈ E i) :
          c j k l m x =
            B k l m x - B j l m x +
              B j k m x - B j k l x := by
        have h1 := hFace k l m hk hl hm hkx hlx hmx hix
        have h2 := hFace j l m hj hl hm hjx hlx hmx hix
        have h3 := hFace j k m hj hk hm hjx hkx hmx hix
        have h4 := hFace j k l hj hk hl hjx hkx hlx hix
        have hC := hc i j k l m x hix hjx hkx hlx hmx
        change c j k l m x - c i k l m x + c i j l m x -
          c i j k m x + c i j k l x = 0 at hC
        change c j k l m x =
          B k l m x - B j l m x + B j k m x - B j k l x
        rw [h1,h2,h3,h4]
        dsimp [δa]
        simp only [LocallyConstant.sub_apply] at *
        omega
      rcases hcase with hi_j | hi_k | hi_l | hi_m | hOld
      · exact hNew (hi_j ▸ hjx)
      · exact hNew (hi_k ▸ hkx)
      · exact hNew (hi_l ▸ hlx)
      · exact hNew (hi_m ▸ hmx)
      · simpa [B,hOld.1,hOld.2.1,hOld.2.2.1,hOld.2.2.2] using
          hb j k l m hOld.1 hOld.2.1 hOld.2.2.1 hOld.2.2.2
            x hjx hkx hlx hmx
  obtain ⟨b, hb⟩ := aux Finset.univ
  refine ⟨b, ?_⟩
  intro i j k l x hi hj hk hl
  exact hb i j k l (Finset.mem_univ _) (Finset.mem_univ _)
    (Finset.mem_univ _) (Finset.mem_univ _) x hi hj hk hl

/-- Genuine degree-three Čech cocycles on closed FOURFOLD
intersections of any finite closed family have globally defined
locally constant 2-cochain primitives. -/
theorem integerFiniteClosedFamily_threeCocycle_is_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : (i j k l : I) →
      LocallyConstant (↥(((E i ∩ E j) ∩ E k) ∩ E l)) ℤ)
    (hc : ∀ (i j k l m : I) (x : X)
      (hi : x ∈ E i) (hj : x ∈ E j)
      (hk : x ∈ E k) (hl : x ∈ E l) (hm : x ∈ E m),
        c j k l m ⟨x, ⟨⟨⟨hj,hk⟩,hl⟩,hm⟩⟩ -
        c i k l m ⟨x, ⟨⟨⟨hi,hk⟩,hl⟩,hm⟩⟩ +
        c i j l m ⟨x, ⟨⟨⟨hi,hj⟩,hl⟩,hm⟩⟩ -
        c i j k m ⟨x, ⟨⟨⟨hi,hj⟩,hk⟩,hm⟩⟩ +
        c i j k l ⟨x, ⟨⟨⟨hi,hj⟩,hk⟩,hl⟩⟩ = 0) :
    ∃ b : I → I → I → LocallyConstant X ℤ,
      ∀ (i j k l : I) (x : X)
        (hi : x ∈ E i) (hj : x ∈ E j)
        (hk : x ∈ E k) (hl : x ∈ E l),
        c i j k l ⟨x, ⟨⟨⟨hi,hj⟩,hk⟩,hl⟩⟩ =
          b j k l x - b i k l x + b i j l x - b i j k x := by
  classical
  have hext (i j k l : I) :
      ∃ C : LocallyConstant X ℤ,
        ∀ x : ↥(((E i ∩ E j) ∩ E k) ∩ E l),
          C x.val = c i j k l x := by
    exact locallyConstant_extend_closed_subset X
      (((E i ∩ E j) ∩ E k) ∩ E l)
      ((((hclosed i).inter (hclosed j)).inter (hclosed k)).inter (hclosed l))
      (c i j k l)
  choose C hC using hext
  have hc' : ∀ (i j k l m : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l → x ∈ E m →
      C j k l m x - C i k l m x + C i j l m x -
        C i j k m x + C i j k l x = 0 := by
    intro i j k l m x hi hj hk hl hm
    rw [hC j k l m ⟨x, ⟨⟨⟨hj,hk⟩,hl⟩,hm⟩⟩,
      hC i k l m ⟨x, ⟨⟨⟨hi,hk⟩,hl⟩,hm⟩⟩,
      hC i j l m ⟨x, ⟨⟨⟨hi,hj⟩,hl⟩,hm⟩⟩,
      hC i j k m ⟨x, ⟨⟨⟨hi,hj⟩,hk⟩,hm⟩⟩,
      hC i j k l ⟨x, ⟨⟨⟨hi,hj⟩,hk⟩,hl⟩⟩]
    exact hc i j k l m x hi hj hk hl hm
  obtain ⟨b, hb⟩ :=
    integerFiniteClosedFamily_globalThreeCocycle_coboundary
      X E hclosed C hc'
  refine ⟨b, ?_⟩
  intro i j k l x hi hj hk hl
  rw [← hC i j k l ⟨x, ⟨⟨⟨hi,hj⟩,hk⟩,hl⟩⟩]
  exact hb i j k l x hi hj hk hl

#print axioms integerFiniteClosedFamily_threeCocycle_is_coboundary

#print axioms integerFiniteClosedFamily_globalThreeCocycle_coboundary
end CMDG.CondensedCM5R0
