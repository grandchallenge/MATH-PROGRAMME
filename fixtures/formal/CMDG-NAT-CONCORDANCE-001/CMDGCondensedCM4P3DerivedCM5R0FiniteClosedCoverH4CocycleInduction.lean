import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverH3CocycleInduction

/-!
# CM5: finite closed-family scalar Čech H⁴

For an arbitrary finite family of closed subsets of a profinite space,
prove every integer-valued locally constant 4-cocycle has a
locally constant 3-cochain primitive. This reduces by finite-family
induction to the already-proved closed-family H³ theorem. No
global unlimited-profinite H⁴ or Ext⁴ claim is built into this lemma.
-/

noncomputable section
universe u v
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem integerFiniteClosedFamily_globalFourCocycle_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : I → I → I → I → I → LocallyConstant X ℤ)
    (hc : ∀ (i j k l m n : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l →
      x ∈ E m → x ∈ E n →
      c j k l m n x - c i k l m n x + c i j l m n x -
        c i j k m n x + c i j k l n x - c i j k l m x = 0) :
    ∃ b : I → I → I → I → LocallyConstant X ℤ,
      ∀ (i j k l m : I) (x : X),
        x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l → x ∈ E m →
        c i j k l m x =
          b j k l m x - b i k l m x + b i j l m x -
            b i j k m x + b i j k l x := by
  classical
  have aux : ∀ s : Finset I,
      ∃ b : I → I → I → I → LocallyConstant X ℤ,
        ∀ (j k l m n : I), j ∈ s → k ∈ s → l ∈ s →
          m ∈ s → n ∈ s →
          ∀ x : X, x ∈ E j → x ∈ E k → x ∈ E l →
            x ∈ E m → x ∈ E n →
            c j k l m n x =
              b k l m n x - b j l m n x + b j k m n x -
                b j k l n x + b j k l m x := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      refine ⟨fun _ _ _ _ => LocallyConstant.const X 0, ?_⟩
      intro j k l m n hj
      simp at hj
    | @insert i s hnot ih =>
      obtain ⟨b, hb⟩ := ih
      let D : I → Set X := fun j => if j ∈ s then E j ∩ E i else ∅
      have hD : ∀ j, IsClosed (D j) := by
        intro j
        by_cases hj : j ∈ s
        · simpa [D, hj] using (hclosed j).inter (hclosed i)
        · simp [D, hj]
      let w : I → I → I → I → LocallyConstant X ℤ :=
        fun j k l m => b j k l m - c i j k l m
      have hmem (j : I) (x : X) (hj : x ∈ D j) :
          j ∈ s ∧ x ∈ E j ∧ x ∈ E i := by
        by_cases hjs : j ∈ s
        · simpa [D, hjs] using
            (And.intro hjs (show x ∈ E j ∩ E i from by
              simpa [D, hjs] using hj))
        · simp [D, hjs] at hj
      have hinto (j : I) (x : X) (hjs : j ∈ s)
          (hj : x ∈ E j) (hi : x ∈ E i) : x ∈ D j := by
        simp [D, hjs, hj, hi]
      have hw : ∀ (j k l m n : I) (x : X),
          x ∈ D j → x ∈ D k → x ∈ D l →
            x ∈ D m → x ∈ D n →
          w k l m n x - w j l m n x + w j k m n x -
            w j k l n x + w j k l m x = 0 := by
        intro j k l m n x hj hk hl hm hn
        obtain ⟨hjs, hjx, hix⟩ := hmem j x hj
        obtain ⟨hks, hkx, _⟩ := hmem k x hk
        obtain ⟨hls, hlx, _⟩ := hmem l x hl
        obtain ⟨hms, hmx, _⟩ := hmem m x hm
        obtain ⟨hns, hnx, _⟩ := hmem n x hn
        have hOld := hb j k l m n hjs hks hls hms hns
          x hjx hkx hlx hmx hnx
        have hC := hc i j k l m n x hix hjx hkx hlx hmx hnx
        change c j k l m n x = b k l m n x - b j l m n x +
          b j k m n x - b j k l n x + b j k l m x at hOld
        change c j k l m n x - c i k l m n x + c i j l m n x -
          c i j k m n x + c i j k l n x - c i j k l m x = 0 at hC
        change (b k l m n x - c i k l m n x) -
          (b j l m n x - c i j l m n x) +
          (b j k m n x - c i j k m n x) -
          (b j k l n x - c i j k l n x) +
          (b j k l m x - c i j k l m x) = 0
        omega
      obtain ⟨a, ha⟩ :=
        integerFiniteClosedFamily_globalThreeCocycle_coboundary X D hD w hw
      let δa (j k l m : I) : LocallyConstant X ℤ :=
        a k l m - a j l m + a j k m - a j k l
      let B (j k l m : I) : LocallyConstant X ℤ :=
        if j ∈ s ∧ k ∈ s ∧ l ∈ s ∧ m ∈ s then b j k l m
        else c i j k l m + δa j k l m
      refine ⟨B, ?_⟩
      intro j k l m n hj hk hl hm hn x hjx hkx hlx hmx hnx
      have hi_of_not_s (r : I) (hr : r ∈ insert i s)
          (hrns : r ∉ s) : r = i :=
        (Finset.mem_insert.mp hr).resolve_right hrns
      have hcase : i = j ∨ i = k ∨ i = l ∨ i = m ∨ i = n ∨
          (j ∈ s ∧ k ∈ s ∧ l ∈ s ∧ m ∈ s ∧ n ∈ s) := by
        by_cases hjs : j ∈ s
        · by_cases hks : k ∈ s
          · by_cases hls : l ∈ s
            · by_cases hms : m ∈ s
              · by_cases hns : n ∈ s
                · exact Or.inr (Or.inr (Or.inr (Or.inr
                    (Or.inr ⟨hjs,hks,hls,hms,hns⟩))))
                · exact Or.inr (Or.inr (Or.inr (Or.inr
                    (Or.inl (hi_of_not_s n hn hns).symm))))
              · exact Or.inr (Or.inr (Or.inr
                  (Or.inl (hi_of_not_s m hm hms).symm)))
            · exact Or.inr (Or.inr
                (Or.inl (hi_of_not_s l hl hls).symm))
          · exact Or.inr (Or.inl (hi_of_not_s k hk hks).symm)
        · exact Or.inl (hi_of_not_s j hj hjs).symm
      have hFace (r t u v : I)
          (hr : r ∈ insert i s) (ht : t ∈ insert i s)
          (hu : u ∈ insert i s) (hv : v ∈ insert i s)
          (hrx : x ∈ E r) (htx : x ∈ E t)
          (hux : x ∈ E u) (hvx : x ∈ E v)
          (hix : x ∈ E i) :
          B r t u v x = c i r t u v x + δa r t u v x := by
        by_cases hrtuv : r ∈ s ∧ t ∈ s ∧ u ∈ s ∧ v ∈ s
        · have ha' := ha r t u v x
            (hinto r x hrtuv.1 hrx hix)
            (hinto t x hrtuv.2.1 htx hix)
            (hinto u x hrtuv.2.2.1 hux hix)
            (hinto v x hrtuv.2.2.2 hvx hix)
          change b r t u v x - c i r t u v x =
            a t u v x - a r u v x + a r t v x - a r t u x at ha'
          change B r t u v x = c i r t u v x +
            (a t u v x - a r u v x + a r t v x - a r t u x)
          simp only [B, if_pos hrtuv]
          omega
        · change B r t u v x = c i r t u v x +
            (a t u v x - a r u v x + a r t v x - a r t u x)
          simp [B, hrtuv, δa, LocallyConstant.sub_apply]
      have hNew (hix : x ∈ E i) :
          c j k l m n x =
            B k l m n x - B j l m n x + B j k m n x -
              B j k l n x + B j k l m x := by
        have h1 := hFace k l m n hk hl hm hn hkx hlx hmx hnx hix
        have h2 := hFace j l m n hj hl hm hn hjx hlx hmx hnx hix
        have h3 := hFace j k m n hj hk hm hn hjx hkx hmx hnx hix
        have h4 := hFace j k l n hj hk hl hn hjx hkx hlx hnx hix
        have h5 := hFace j k l m hj hk hl hm hjx hkx hlx hmx hix
        have hC := hc i j k l m n x hix hjx hkx hlx hmx hnx
        change c j k l m n x - c i k l m n x +
          c i j l m n x - c i j k m n x +
          c i j k l n x - c i j k l m x = 0 at hC
        change c j k l m n x =
          B k l m n x - B j l m n x + B j k m n x -
            B j k l n x + B j k l m x
        rw [h1,h2,h3,h4,h5]
        dsimp [δa]
        simp only [LocallyConstant.sub_apply, LocallyConstant.add_apply] at *
        omega
      rcases hcase with hi_j | hi_k | hi_l | hi_m | hi_n | hOld
      · exact hNew (hi_j ▸ hjx)
      · exact hNew (hi_k ▸ hkx)
      · exact hNew (hi_l ▸ hlx)
      · exact hNew (hi_m ▸ hmx)
      · exact hNew (hi_n ▸ hnx)
      · simpa [B,hOld.1,hOld.2.1,hOld.2.2.1,
          hOld.2.2.2.1,hOld.2.2.2.2] using
            hb j k l m n hOld.1 hOld.2.1 hOld.2.2.1
              hOld.2.2.2.1 hOld.2.2.2.2 x hjx hkx hlx hmx hnx
  obtain ⟨b, hb⟩ := aux Finset.univ
  refine ⟨b, ?_⟩
  intro i j k l m x hi hj hk hl hm
  exact hb i j k l m (Finset.mem_univ _) (Finset.mem_univ _)
    (Finset.mem_univ _) (Finset.mem_univ _) (Finset.mem_univ _)
    x hi hj hk hl hm


/-- Closed-fivefold integer H4 cocycles have globally defined
four-index locally constant primitives on the profinite base. -/
theorem integerFiniteClosedFamily_fourCocycle_is_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : (i j k l m : I) →
      LocallyConstant (↥((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m)) ℤ)
    (hc : ∀ (i j k l m n : I) (x : X)
      (hi : x ∈ E i) (hj : x ∈ E j)
      (hk : x ∈ E k) (hl : x ∈ E l)
      (hm : x ∈ E m) (hn : x ∈ E n),
      c j k l m n ⟨x, ⟨⟨⟨⟨hj,hk⟩,hl⟩,hm⟩,hn⟩⟩ -
      c i k l m n ⟨x, ⟨⟨⟨⟨hi,hk⟩,hl⟩,hm⟩,hn⟩⟩ +
      c i j l m n ⟨x, ⟨⟨⟨⟨hi,hj⟩,hl⟩,hm⟩,hn⟩⟩ -
      c i j k m n ⟨x, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hm⟩,hn⟩⟩ +
      c i j k l n ⟨x, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hn⟩⟩ -
      c i j k l m ⟨x, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩⟩ = 0) :
    ∃ b : I → I → I → I → LocallyConstant X ℤ,
      ∀ (i j k l m : I) (x : X)
        (hi : x ∈ E i) (hj : x ∈ E j)
        (hk : x ∈ E k) (hl : x ∈ E l)
        (hm : x ∈ E m),
      c i j k l m ⟨x, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩⟩ =
        b j k l m x - b i k l m x + b i j l m x -
          b i j k m x + b i j k l x := by
  classical
  have hext (i j k l m : I) :
      ∃ C : LocallyConstant X ℤ,
        ∀ x : ↥((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m),
          C x.val = c i j k l m x := by
    exact locallyConstant_extend_closed_subset X
      ((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m)
      (((((hclosed i).inter (hclosed j)).inter (hclosed k)).inter
        (hclosed l)).inter (hclosed m))
      (c i j k l m)
  choose C hC using hext
  have hc' : ∀ (i j k l m n : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l →
      x ∈ E m → x ∈ E n →
      C j k l m n x - C i k l m n x + C i j l m n x -
        C i j k m n x + C i j k l n x - C i j k l m x = 0 := by
    intro i j k l m n x hi hj hk hl hm hn
    rw [hC j k l m n ⟨x, ⟨⟨⟨⟨hj,hk⟩,hl⟩,hm⟩,hn⟩⟩,
      hC i k l m n ⟨x, ⟨⟨⟨⟨hi,hk⟩,hl⟩,hm⟩,hn⟩⟩,
      hC i j l m n ⟨x, ⟨⟨⟨⟨hi,hj⟩,hl⟩,hm⟩,hn⟩⟩,
      hC i j k m n ⟨x, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hm⟩,hn⟩⟩,
      hC i j k l n ⟨x, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hn⟩⟩,
      hC i j k l m ⟨x, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩⟩]
    exact hc i j k l m n x hi hj hk hl hm hn
  obtain ⟨b, hb⟩ :=
    integerFiniteClosedFamily_globalFourCocycle_coboundary
      X E hclosed C hc'
  refine ⟨b, ?_⟩
  intro i j k l m x hi hj hk hl hm
  rw [← hC i j k l m ⟨x, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩⟩]
  exact hb i j k l m x hi hj hk hl hm

#print axioms integerFiniteClosedFamily_fourCocycle_is_coboundary
#print axioms integerFiniteClosedFamily_globalFourCocycle_coboundary
end CMDG.CondensedCM5R0
