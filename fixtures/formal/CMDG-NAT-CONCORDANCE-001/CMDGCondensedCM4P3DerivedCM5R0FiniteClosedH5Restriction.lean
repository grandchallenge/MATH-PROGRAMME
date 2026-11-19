import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedH5

/-! CM5 scalar H5 closed intersections: global ambient LC primitive. -/
noncomputable section
universe u v
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

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
      c j k l m n o ⟨x,⟨⟨⟨⟨⟨hj,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩ - c i k l m n o ⟨x,⟨⟨⟨⟨⟨hi,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩ + c i j l m n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩ - c i j k m n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hm⟩,hn⟩,ho⟩⟩ + c i j k l n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hn⟩,ho⟩⟩ - c i j k l m o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,ho⟩⟩ + c i j k l m n ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,hn⟩⟩ = 0) :
    ∃ b : I → I → I → I → I → LocallyConstant X ℤ,
      ∀ (i j k l m n : I) (x : X)
        (hi : x ∈ E i) (hj : x ∈ E j)
        (hk : x ∈ E k) (hl : x ∈ E l)
        (hm : x ∈ E m) (hn : x ∈ E n),
        c i j k l m n ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,hn⟩⟩ =
          b j k l m n x - b i k l m n x + b i j l m n x - b i j k m n x + b i j k l n x - b i j k l m x := by
  classical
  have hext (i j k l m n : I) :
      ∃ C : LocallyConstant X ℤ,
        ∀ x : ↥((((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m) ∩ E n)),
          C x.val = c i j k l m n x := by
    exact locallyConstant_extend_closed_subset X
      ((((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m) ∩ E n))
      ((((((hclosed i).inter (hclosed j)).inter (hclosed k)).inter (hclosed l)).inter (hclosed m)).inter (hclosed n))
      (c i j k l m n)
  choose C hC using hext
  have hc' : ∀ (i j k l m n o : I) (x : X),
      x ∈ E i → x ∈ E j → x ∈ E k →
        x ∈ E l → x ∈ E m → x ∈ E n → x ∈ E o →
        C j k l m n o x - C i k l m n o x + C i j l m n o x - C i j k m n o x + C i j k l n o x - C i j k l m o x + C i j k l m n x = 0 := by
    intro i j k l m n o x hi hj hk hl hm hn ho
    rw [hC j k l m n o ⟨x,⟨⟨⟨⟨⟨hj,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩, hC i k l m n o ⟨x,⟨⟨⟨⟨⟨hi,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩, hC i j l m n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩, hC i j k m n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hm⟩,hn⟩,ho⟩⟩, hC i j k l n o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hn⟩,ho⟩⟩, hC i j k l m o ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,ho⟩⟩, hC i j k l m n ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,hn⟩⟩]
    exact hc i j k l m n o x hi hj hk hl hm hn ho
  obtain ⟨b,hb⟩ :=
    integerFiniteClosedFamily_globalFiveCocycle_coboundary
      X E hclosed C hc'
  refine ⟨b, ?_⟩
  intro i j k l m n x hi hj hk hl hm hn
  rw [← hC i j k l m n ⟨x,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,hn⟩⟩]
  exact hb i j k l m n x hi hj hk hl hm hn

#print axioms integerFiniteClosedFamily_fiveCocycle_is_coboundary
end CMDG.CondensedCM5R0
