import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedH4

/-! CM5: finite closed-family H5 acyclicity in locally constant integers.
The induction uses the already-proved closed-family H4 theorem.
No clopen cover or finite quotient is assumed. -/
noncomputable section
universe u v
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem integerFiniteClosedFamily_globalFiveCocycle_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : I → I → I → I → I → I → LocallyConstant X ℤ)
    (hc : ∀ (i j k l m n o : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k → x ∈ E l →
        x ∈ E m → x ∈ E n → x ∈ E o →
      c j k l m n o x - c i k l m n o x + c i j l m n o x - c i j k m n o x + c i j k l n o x - c i j k l m o x + c i j k l m n x = 0) :
    ∃ b : I → I → I → I → I → LocallyConstant X ℤ,
      ∀ (j k l m n o : I) (x : X),
        x ∈ E j → x ∈ E k → x ∈ E l → x ∈ E m →
          x ∈ E n → x ∈ E o →
        c j k l m n o x = b k l m n o x - b j l m n o x + b j k m n o x - b j k l n o x + b j k l m o x - b j k l m n x := by
  classical
  have aux : ∀ ss : Finset I,
      ∃ b : I → I → I → I → I → LocallyConstant X ℤ,
        ∀ (j k l m n o : I), j ∈ ss → k ∈ ss → l ∈ ss →
          m ∈ ss → n ∈ ss → o ∈ ss →
          ∀ x : X, x ∈ E j → x ∈ E k → x ∈ E l →
            x ∈ E m → x ∈ E n → x ∈ E o →
          c j k l m n o x = b k l m n o x - b j l m n o x + b j k m n o x - b j k l n o x + b j k l m o x - b j k l m n x := by
    intro ss
    induction ss using Finset.induction_on with
    | empty =>
      refine ⟨fun _ _ _ _ _ => LocallyConstant.const X 0, ?_⟩
      intro j k l m n o hj
      simp at hj
    | @insert i ss hnot ih =>
      obtain ⟨b, hb⟩ := ih
      let D : I → Set X := fun z => if z ∈ ss then E z ∩ E i else ∅
      have hD : ∀ z, IsClosed (D z) := by
        intro z
        by_cases hz : z ∈ ss
        · simpa [D, hz] using (hclosed z).inter (hclosed i)
        · simp [D, hz]
      let w : I → I → I → I → I → LocallyConstant X ℤ :=
        fun j k l m n => b j k l m n - c i j k l m n
      have hmem (z : I) (x : X) (hz : x ∈ D z) :
          z ∈ ss ∧ x ∈ E z ∧ x ∈ E i := by
        by_cases hzs : z ∈ ss
        · simpa [D, hzs] using
            (And.intro hzs (show x ∈ E z ∩ E i from by
              simpa [D, hzs] using hz))
        · simp [D, hzs] at hz
      have hinto (z : I) (x : X) (hz : z ∈ ss)
          (hEx : x ∈ E z) (hi : x ∈ E i) : x ∈ D z := by
        simp [D, hz, hEx, hi]
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
        have hC := hc i j k l m n o x hix
          hjx hkx hlx hmx hnx hox
        change c j k l m n o x = b k l m n o x - b j l m n o x + b j k m n o x - b j k l n o x + b j k l m o x - b j k l m n x at hOld
        change c j k l m n o x - c i k l m n o x + c i j l m n o x - c i j k m n o x + c i j k l n o x - c i j k l m o x + c i j k l m n x = 0 at hC
        change (b k l m n o x - c i k l m n o x) - (b j l m n o x - c i j l m n o x) + (b j k m n o x - c i j k m n o x) - (b j k l n o x - c i j k l n o x) + (b j k l m o x - c i j k l m o x) - (b j k l m n x - c i j k l m n x) = 0
        omega
      obtain ⟨a, ha⟩ :=
        integerFiniteClosedFamily_globalFourCocycle_coboundary
          X D hD w hw
      let δa (j k l m n : I) : LocallyConstant X ℤ :=
        a k l m n - a j l m n + a j k m n - a j k l n + a j k l m
      let B (j k l m n : I) : LocallyConstant X ℤ :=
        if j ∈ ss ∧ k ∈ ss ∧ l ∈ ss ∧ m ∈ ss ∧ n ∈ ss then b j k l m n
        else c i j k l m n + δa j k l m n
      refine ⟨B, ?_⟩
      intro j k l m n o hj hk hl hm hn ho x hjx hkx hlx hmx hnx hox
      have hi_of_not_ss (z : I) (hz : z ∈ insert i ss)
          (hzns : z ∉ ss) : z = i :=
        (Finset.mem_insert.mp hz).resolve_right hzns
      have hcase :
          i = j ∨ i = k ∨ i = l ∨ i = m ∨ i = n ∨ i = o ∨
          (j ∈ ss ∧ k ∈ ss ∧ l ∈ ss ∧ m ∈ ss ∧ n ∈ ss ∧ o ∈ ss) := by
        by_cases hjs : j ∈ ss
        · by_cases hks : k ∈ ss
          · by_cases hls : l ∈ ss
            · by_cases hms : m ∈ ss
              · by_cases hns : n ∈ ss
                · by_cases hos : o ∈ ss
                  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (⟨hjs,hks,hls,hms,hns,hos⟩))))))
                  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (hi_of_not_ss o ho (by simpa using hos)).symm)))))
                · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (hi_of_not_ss n hn (by simpa using hns)).symm))))
              · exact Or.inr (Or.inr (Or.inr (Or.inl (hi_of_not_ss m hm (by simpa using hms)).symm)))
            · exact Or.inr (Or.inr (Or.inl (hi_of_not_ss l hl (by simpa using hls)).symm))
          · exact Or.inr (Or.inl (hi_of_not_ss k hk (by simpa using hks)).symm)
        · exact Or.inl (hi_of_not_ss j hj (by simpa using hjs)).symm
      have hFace (r t v w q : I)
          (hr : r ∈ insert i ss) (ht : t ∈ insert i ss)
          (hv : v ∈ insert i ss) (hw' : w ∈ insert i ss)
          (hq : q ∈ insert i ss)
          (hrx : x ∈ E r) (htx : x ∈ E t)
          (hvx : x ∈ E v) (hwx : x ∈ E w)
          (hqx : x ∈ E q)
          (hix : x ∈ E i) :
          B r t v w q x = c i r t v w q x + δa r t v w q x := by
        by_cases hrtvwq : r ∈ ss ∧ t ∈ ss ∧ v ∈ ss ∧ w ∈ ss ∧ q ∈ ss
        · rcases hrtvwq with ⟨hrs,hts,hvs,hws,hqs⟩
          have ha' := ha r t v w q x
            (hinto r x hrs hrx hix)
            (hinto t x hts htx hix)
            (hinto v x hvs hvx hix)
            (hinto w x hws hwx hix)
            (hinto q x hqs hqx hix)
          change b r t v w q x - c i r t v w q x =
            a t v w q x - a r v w q x + a r t w q x - a r t v q x + a r t v w x at ha'
          change B r t v w q x = c i r t v w q x +
            (a t v w q x - a r v w q x + a r t w q x - a r t v q x + a r t v w x)
          simp only [B, if_pos (show r ∈ ss ∧ t ∈ ss ∧ v ∈ ss ∧ w ∈ ss ∧ q ∈ ss from
            ⟨hrs,hts,hvs,hws,hqs⟩)]
          omega
        · change B r t v w q x = c i r t v w q x +
            (a t v w q x - a r v w q x + a r t w q x - a r t v q x + a r t v w x)
          simp [B, hrtvwq, δa, LocallyConstant.sub_apply,
            LocallyConstant.add_apply]
      have hNew (hix : x ∈ E i) :
          c j k l m n o x = B k l m n o x - B j l m n o x + B j k m n o x - B j k l n o x + B j k l m o x - B j k l m n x := by
        have h1 := hFace k l m n o hk hl hm hn ho hkx hlx hmx hnx hox hix
        have h2 := hFace j l m n o hj hl hm hn ho hjx hlx hmx hnx hox hix
        have h3 := hFace j k m n o hj hk hm hn ho hjx hkx hmx hnx hox hix
        have h4 := hFace j k l n o hj hk hl hn ho hjx hkx hlx hnx hox hix
        have h5 := hFace j k l m o hj hk hl hm ho hjx hkx hlx hmx hox hix
        have h6 := hFace j k l m n hj hk hl hm hn hjx hkx hlx hmx hnx hix
        have hC := hc i j k l m n o x hix
          hjx hkx hlx hmx hnx hox
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
      · rcases hOld with ⟨hjs,hks,hls,hms,hns,hos⟩
        simpa [B,hjs,hks,hls,hms,hns,hos] using
          hb j k l m n o hjs hks hls hms hns hos
            x hjx hkx hlx hmx hnx hox
  obtain ⟨b,hb⟩ := aux Finset.univ
  refine ⟨b, ?_⟩
  intro j k l m n o x hj hk hl hm hn ho
  exact hb j k l m n o (Finset.mem_univ _)
    (Finset.mem_univ _) (Finset.mem_univ _)
    (Finset.mem_univ _) (Finset.mem_univ _)
    (Finset.mem_univ _) x hj hk hl hm hn ho

#print axioms integerFiniteClosedFamily_globalFiveCocycle_coboundary
end CMDG.CondensedCM5R0
