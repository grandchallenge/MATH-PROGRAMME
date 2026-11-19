import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedH4

/-!
# CM5: finite closed-family scalar Čech H⁵ acyclicity

Six-index five-cocycles are solved by induction on finite closed
families using the protected closed-family H⁴ theorem.
No clopen hypothesis, open-cover assumption, or presentation section.
Not a global condensed Ext⁵ claim.
-/
noncomputable section
universe u v
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem integerFiniteClosedFamily_globalFiveCocycle_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : (i j k l m n : I) → LocallyConstant X ℤ)
    (hc : ∀ (i j k l m n o : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l →
        x ∈ E m → x ∈ E n → x ∈ E o →
      c j k l m n o x - c i k l m n o x + c i j l m n o x - c i j k m n o x + c i j k l n o x - c i j k l m o x + c i j k l m n x = 0) :
    ∃ b : (i j k l m : I) → LocallyConstant X ℤ,
      ∀ (i j k l m n : I) (x : X),
        x ∈ E i → x ∈ E j → x ∈ E k →
          x ∈ E l → x ∈ E m → x ∈ E n →
        c i j k l m n x = b j k l m n x - b i k l m n x + b i j l m n x - b i j k m n x + b i j k l n x - b i j k l m x := by
  classical
  have aux : ∀ s : Finset I,
      ∃ b : (i j k l m : I) → LocallyConstant X ℤ,
        ∀ (j k l m n o : I),
          j ∈ s → k ∈ s → l ∈ s → m ∈ s → n ∈ s → o ∈ s →
          ∀ x : X, x ∈ E j → x ∈ E k → x ∈ E l →
            x ∈ E m → x ∈ E n → x ∈ E o →
          c j k l m n o x = b k l m n o x - b j l m n o x + b j k m n o x - b j k l n o x + b j k l m o x - b j k l m n x := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      refine ⟨fun _ _ _ _ _ => LocallyConstant.const X 0, ?_⟩
      intro j k l m n o hj
      simp at hj
    | @insert i s hnot ih =>
      obtain ⟨b, hb⟩ := ih
      let D : I → Set X := fun j => if j ∈ s then E j ∩ E i else ∅
      have hD : ∀ j, IsClosed (D j) := by
        intro j
        by_cases hj : j ∈ s
        · simpa [D, hj] using (hclosed j).inter (hclosed i)
        · simp [D, hj]
      let w : (j k l m n : I) → LocallyConstant X ℤ :=
        fun j k l m n => b j k l m n - c i j k l m n
      have hmem (j : I) (x : X) (hj : x ∈ D j) :
          j ∈ s ∧ x ∈ E j ∧ x ∈ E i := by
        by_cases hjs : j ∈ s
        · simpa [D, hjs] using
            (And.intro hjs (show x ∈ E j ∩ E i from by
              simpa [D,hjs] using hj))
        · simp [D,hjs] at hj
      have hinto (j : I) (x : X) (hjs : j ∈ s)
          (hj : x ∈ E j) (hi : x ∈ E i) : x ∈ D j := by
        simp [D,hjs,hj,hi]
      have hw : ∀ (j k l m n o : I) (x : X),
          x ∈ D j → x ∈ D k → x ∈ D l →
            x ∈ D m → x ∈ D n → x ∈ D o →
          w k l m n o x - w j l m n o x + w j k m n o x - w j k l n o x + w j k l m o x - w j k l m n x = 0 := by
        intro j k l m n o x hj hk hl hm hn ho
        obtain ⟨hjs, hjx, hix⟩ := hmem j x hj
        obtain ⟨hks, hkx, _⟩ := hmem k x hk
        obtain ⟨hls, hlx, _⟩ := hmem l x hl
        obtain ⟨hms, hmx, _⟩ := hmem m x hm
        obtain ⟨hns, hnx, _⟩ := hmem n x hn
        obtain ⟨hos, hox, _⟩ := hmem o x ho
        have hOld := hb j k l m n o hjs hks hls hms hns hos x
          hjx hkx hlx hmx hnx hox
        have hC := hc i j k l m n o x hix hjx hkx hlx hmx hnx hox
        change c j k l m n o x = b k l m n o x - b j l m n o x + b j k m n o x - b j k l n o x + b j k l m o x - b j k l m n x at hOld
        change c j k l m n o x - c i k l m n o x + c i j l m n o x - c i j k m n o x + c i j k l n o x - c i j k l m o x + c i j k l m n x = 0 at hC
        change w k l m n o x - w j l m n o x + w j k m n o x - w j k l n o x + w j k l m o x - w j k l m n x = 0
        dsimp [w]
        simp only [LocallyConstant.sub_apply]
        omega
      obtain ⟨a, ha⟩ :=
        integerFiniteClosedFamily_globalFourCocycle_coboundary X D hD w hw
      let δa (j k l m n : I) : LocallyConstant X ℤ :=
        a k l m n - a j l m n + a j k m n - a j k l n + a j k l m
      let B (j k l m n : I) : LocallyConstant X ℤ :=
        if j ∈ s ∧ k ∈ s ∧ l ∈ s ∧ m ∈ s ∧ n ∈ s then b j k l m n
        else c i j k l m n + δa j k l m n
      refine ⟨B, ?_⟩
      intro j k l m n o hj hk hl hm hn ho x hjx hkx hlx hmx hnx hox
      have hi_of_not_s (r : I) (hr : r ∈ insert i s)
          (hrns : r ∉ s) : r = i :=
        (Finset.mem_insert.mp hr).resolve_right hrns
      have hcase : i = j ∨ i = k ∨ i = l ∨ i = m ∨ i = n ∨ i = o ∨
          (j ∈ s ∧ k ∈ s ∧ l ∈ s ∧ m ∈ s ∧ n ∈ s ∧ o ∈ s) := by
        by_cases hjs : j ∈ s
        ·
          by_cases hks : k ∈ s
          ·
            by_cases hls : l ∈ s
            ·
              by_cases hms : m ∈ s
              ·
                by_cases hns : n ∈ s
                ·
                  by_cases hos : o ∈ s
                  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (⟨hjs,hks,hls,hms,hns,hos⟩))))))
                  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (hi_of_not_s o ho (hos)).symm)))))
                · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (hi_of_not_s n hn (hns)).symm))))
              · exact Or.inr (Or.inr (Or.inr (Or.inl (hi_of_not_s m hm (hms)).symm)))
            · exact Or.inr (Or.inr (Or.inl (hi_of_not_s l hl (hls)).symm))
          · exact Or.inr (Or.inl (hi_of_not_s k hk (hks)).symm)
        · exact Or.inl (hi_of_not_s j hj (hjs)).symm
      have hFace (r t u v q : I)
          (hr : r ∈ insert i s) (ht : t ∈ insert i s)
          (hu : u ∈ insert i s) (hv : v ∈ insert i s)
          (hq : q ∈ insert i s)
          (hrx : x ∈ E r) (htx : x ∈ E t)
          (hux : x ∈ E u) (hvx : x ∈ E v)
          (hqx : x ∈ E q) (hix : x ∈ E i) :
          B r t u v q x = c i r t u v q x + δa r t u v q x := by
        by_cases hrtuvq : r ∈ s ∧ t ∈ s ∧ u ∈ s ∧ v ∈ s ∧ q ∈ s
        · have ha' := ha r t u v q x
            (hinto r x hrtuvq.1 hrx hix)
            (hinto t x hrtuvq.2.1 htx hix)
            (hinto u x hrtuvq.2.2.1 hux hix)
            (hinto v x hrtuvq.2.2.2.1 hvx hix)
            (hinto q x hrtuvq.2.2.2.2 hqx hix)
          change b r t u v q x - c i r t u v q x =
            a t u v q x - a r u v q x + a r t v q x - a r t u q x + a r t u v x at ha'
          change B r t u v q x = c i r t u v q x +
            (a t u v q x - a r u v q x + a r t v q x - a r t u q x + a r t u v x)
          simp only [B, if_pos hrtuvq]
          omega
        · change B r t u v q x = c i r t u v q x +
            (a t u v q x - a r u v q x + a r t v q x - a r t u q x + a r t u v x)
          simp [B, hrtuvq, δa, LocallyConstant.sub_apply]
      have hNew (hix : x ∈ E i) :
          c j k l m n o x = B k l m n o x - B j l m n o x + B j k m n o x - B j k l n o x + B j k l m o x - B j k l m n x := by
        have h1 := hFace k l m n o hk hl hm hn ho hkx hlx hmx hnx hox hix
        have h2 := hFace j l m n o hj hl hm hn ho hjx hlx hmx hnx hox hix
        have h3 := hFace j k m n o hj hk hm hn ho hjx hkx hmx hnx hox hix
        have h4 := hFace j k l n o hj hk hl hn ho hjx hkx hlx hnx hox hix
        have h5 := hFace j k l m o hj hk hl hm ho hjx hkx hlx hmx hox hix
        have h6 := hFace j k l m n hj hk hl hm hn hjx hkx hlx hmx hnx hix
        have hC := hc i j k l m n o x hix hjx hkx hlx hmx hnx hox
        change c j k l m n o x - c i k l m n o x + c i j l m n o x - c i j k m n o x + c i j k l n o x - c i j k l m o x + c i j k l m n x = 0 at hC
        change c j k l m n o x = B k l m n o x - B j l m n o x + B j k m n o x - B j k l n o x + B j k l m o x - B j k l m n x
        rw [h1,h2,h3,h4,h5,h6]
        dsimp [δa]
        simp only [LocallyConstant.sub_apply, LocallyConstant.add_apply] at *
        omega
      rcases hcase with hi_j | hi_k | hi_l | hi_m | hi_n | hi_o | hOld
      · exact hNew (hi_j ▸ hjx)
      · exact hNew (hi_k ▸ hkx)
      · exact hNew (hi_l ▸ hlx)
      · exact hNew (hi_m ▸ hmx)
      · exact hNew (hi_n ▸ hnx)
      · exact hNew (hi_o ▸ hox)
      · simpa [B,hOld.1,hOld.2.1,hOld.2.2.1,hOld.2.2.2.1,hOld.2.2.2.2.1,hOld.2.2.2.2.2] using
          hb j k l m n o hOld.1 hOld.2.1 hOld.2.2.1 hOld.2.2.2.1 hOld.2.2.2.2.1 hOld.2.2.2.2.2
            x hjx hkx hlx hmx hnx hox
  obtain ⟨b, hb⟩ := aux Finset.univ
  refine ⟨b, ?_⟩
  intro i j k l m n x hi hj hk hl hm hn
  exact hb i j k l m n (Finset.mem_univ _) (Finset.mem_univ _) (Finset.mem_univ _) (Finset.mem_univ _) (Finset.mem_univ _) (Finset.mem_univ _)
    x hi hj hk hl hm hn



/-- A locally constant integer five-cocycle on genuine sixfold
intersections of any finite CLOSED family admits an everywhere-defined
four-cochain primitive. Each closed-fibre cochain is extended before
the global induction, so this does not assume clopen fibres. -/
theorem integerFiniteClosedFamily_fiveCocycle_is_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : (i j k l m n : I) →
      LocallyConstant (↥((((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m) ∩ E n))) ℤ)
    (hc : ∀ (i j k l m n o : I) (x : X)
      (hi : x ∈ E i) (hj : x ∈ E j)
      (hk : x ∈ E k) (hl : x ∈ E l)
      (hm : x ∈ E m) (hn : x ∈ E n)
      (ho : x ∈ E o),
      c j k l m n o ⟨x,⟨⟨⟨⟨⟨hj,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩  - c i k l m n o ⟨x,⟨⟨⟨⟨⟨hi,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩  + c i j l m n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩  - c i j k m n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hm⟩,hn⟩,ho⟩⟩  + c i j k l n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hn⟩,ho⟩⟩  - c i j k l m o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,ho⟩⟩  + c i j k l m n ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,hn⟩⟩ = 0) :
    ∃ b : (i j k l m : I) → LocallyConstant X ℤ,
      ∀ (i j k l m n : I) (x : X)
        (hi : x ∈ E i) (hj : x ∈ E j)
        (hk : x ∈ E k) (hl : x ∈ E l)
        (hm : x ∈ E m) (hn : x ∈ E n),
        c i j k l m n ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,hn⟩⟩ =
          b j k l m n x  - b i k l m n x  + b i j l m n x  - b i j k m n x  + b i j k l n x  - b i j k l m x := by
  classical
  have hext (i j k l m n : I) :
      ∃ C : LocallyConstant X ℤ,
        ∀ x : ↥((((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m) ∩ E n)),
          C x.val = c i j k l m n x := by
    exact locallyConstant_extend_closed_subset X
      (((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m) ∩ E n)
      ((((((hclosed i).inter (hclosed j)).inter (hclosed k)).inter (hclosed l)).inter (hclosed m)).inter (hclosed n))
      (c i j k l m n)
  choose C hC using hext
  have hc' : ∀ (i j k l m n o : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l →
        x ∈ E m → x ∈ E n → x ∈ E o →
      C j k l m n o x  - C i k l m n o x  + C i j l m n o x  - C i j k m n o x  + C i j k l n o x  - C i j k l m o x  + C i j k l m n x = 0 := by
    intro i j k l m n o x hi hj hk hl hm hn ho
    rw [hC j k l m n o ⟨x,⟨⟨⟨⟨⟨hj,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩,
      hC i k l m n o ⟨x,⟨⟨⟨⟨⟨hi,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩,
      hC i j l m n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩,
      hC i j k m n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hm⟩,hn⟩,ho⟩⟩,
      hC i j k l n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hn⟩,ho⟩⟩,
      hC i j k l m o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,ho⟩⟩,
      hC i j k l m n ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,hn⟩⟩]
    exact hc i j k l m n o x hi hj hk hl hm hn ho
  obtain ⟨b, hb⟩ :=
    integerFiniteClosedFamily_globalFiveCocycle_coboundary
      X E hclosed C hc'
  refine ⟨b, ?_⟩
  intro i j k l m n x hi hj hk hl hm hn
  rw [← hC i j k l m n ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,hn⟩⟩]
  exact hb i j k l m n x hi hj hk hl hm hn

#print axioms integerFiniteClosedFamily_fiveCocycle_is_coboundary

#print axioms integerFiniteClosedFamily_globalFiveCocycle_coboundary
end CMDG.CondensedCM5R0
