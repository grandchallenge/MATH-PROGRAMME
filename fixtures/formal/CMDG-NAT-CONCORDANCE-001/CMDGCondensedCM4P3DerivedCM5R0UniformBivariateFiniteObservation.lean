import CMDGCondensedCM4P3DerivedCM5R0ScalarClopenRectangleFactorization

/-!
# Heterogeneous finite rectangular observation
A locally constant scalar function of two arbitrary profinite spaces
factors through one finite Boolean signature on each side, even if
the factors differ. This is the inductive product-arity input.
-/

noncomputable section
universe u
open CategoryTheory Limits Set TopologicalSpace
namespace CMDG.CondensedCM5R0

theorem integerLocallyConstant_heterogeneousProduct_finiteRectangles
    (P Q : Profinite.{u})
    (f : LocallyConstant (P × Q) ℤ) :
    ∃ (I : Type u) (hI : Fintype I)
      (qP : LocallyConstant P I) (qQ : LocallyConstant Q I)
      (d : I → I → ℤ),
      ∀ x : P, ∀ y : Q, f (x, y) = d (qP x) (qQ y) := by
  classical
  let R := Set.range (f : P × Q → ℤ)
  haveI : Finite R := f.range_finite.to_subtype
  letI : Fintype R := Fintype.ofFinite R
  let W (r : R) : Clopens (P × Q) :=
    ⟨{z | f z = r.val}, f.isLocallyConstant.isClopen_fiber r.val⟩
  have hboxes (r : R) :
      ∃ Bs : Finset (Clopens P × Clopens Q),
        W r = Bs.sup (fun k => k.1 ×ˢ k.2) :=
    TopologicalSpace.Clopens.exists_finset_eq_sup_prod (W r)
  choose Bs hBs using hboxes
  let all : Finset (Clopens P × Clopens Q) :=
    Finset.univ.biUnion Bs
  let I : Type u := (↥all → Bool)
  let sigP (x : P) : I := fun k =>
    clopenIndicator P k.val.1 x
  let sigQ (y : Q) : I := fun k =>
    clopenIndicator Q k.val.2 y
  have hsigP : IsLocallyConstant sigP := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro t
    have hfiber :
        sigP ⁻¹' {t} =
          ⋂ k : ↥all, ((fun x : P =>
            clopenIndicator P k.val.1 x) ⁻¹' {t k}) := by
      ext x
      simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_iInter]
      exact funext_iff
    rw [hfiber]
    exact isOpen_iInter_of_finite (fun k =>
      (locallyConstant_decide_clopen P k.val.1).isOpen_fiber (t k))
  have hsigQ : IsLocallyConstant sigQ := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro t
    have hfiber :
        sigQ ⁻¹' {t} =
          ⋂ k : ↥all, ((fun y : Q =>
            clopenIndicator Q k.val.2 y) ⁻¹' {t k}) := by
      ext y
      simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_iInter]
      exact funext_iff
    rw [hfiber]
    exact isOpen_iInter_of_finite (fun k =>
      (locallyConstant_decide_clopen Q k.val.2).isOpen_fiber (t k))
  let qP : LocallyConstant P I := ⟨sigP, hsigP⟩
  let qQ : LocallyConstant Q I := ⟨sigQ, hsigQ⟩
  have hstable (x x' : P) (y y' : Q)
      (hx : qP x = qP x') (hy : qQ y = qQ y') :
      f (x, y) = f (x', y') := by
    let r : R := ⟨f (x, y), ⟨(x, y), rfl⟩⟩
    have hw : (x, y) ∈ W r := rfl
    have hw' : (x, y) ∈
        (↑((Bs r).sup (fun k => k.1 ×ˢ k.2)) :
          Set (P × Q)) := by
      rw [← hBs r]
      exact hw
    rw [TopologicalSpace.Clopens.coe_finset_sup] at hw'
    obtain ⟨k, hk, hxy⟩ := Set.mem_iUnion₂.mp hw'
    have hxk : x ∈ (k.1 : Set P) := hxy.1
    have hyk : y ∈ (k.2 : Set Q) := hxy.2
    have hkall : k ∈ all :=
      Finset.mem_biUnion.mpr ⟨r, Finset.mem_univ _, hk⟩
    let kk : ↥all := ⟨k, hkall⟩
    have hxl := congrFun hx kk
    have hyr := congrFun hy kk
    change clopenIndicator P k.1 x =
      clopenIndicator P k.1 x' at hxl
    change clopenIndicator Q k.2 y =
      clopenIndicator Q k.2 y' at hyr
    have hxk' : x' ∈ (k.1 : Set P) := by
      by_contra hn
      simp [clopenIndicator, hxk, hn] at hxl
    have hyk' : y' ∈ (k.2 : Set Q) := by
      by_contra hn
      simp [clopenIndicator, hyk, hn] at hyr
    have hw2' : (x', y') ∈
        (↑((Bs r).sup (fun k => k.1 ×ˢ k.2)) :
          Set (P × Q)) := by
      rw [TopologicalSpace.Clopens.coe_finset_sup]
      apply Set.mem_iUnion₂.mpr
      exact ⟨k, hk, ⟨hxk', hyk'⟩⟩
    have hw2 : (x', y') ∈ W r := by
      rw [hBs r]
      exact hw2'
    have hf2 : f (x', y') = r.val := hw2
    exact hf2.symm
  let d (i j : I) : ℤ :=
    if h : ∃ z : P × Q, qP z.1 = i ∧ qQ z.2 = j then
      f (Classical.choose h)
    else 0
  letI : Fintype I := Fintype.ofFinite I
  refine ⟨I, inferInstance, qP, qQ, d, ?_⟩
  intro x y
  have h : ∃ z : P × Q,
      qP z.1 = qP x ∧ qQ z.2 = qQ y :=
    ⟨(x, y), rfl, rfl⟩
  have hz := Classical.choose_spec h
  have hconst := hstable x (Classical.choose h).1
    y (Classical.choose h).2 hz.1.symm hz.2.symm
  change f (x, y) = d (qP x) (qQ y)
  dsimp [d]
  rw [dif_pos h]
  exact hconst

#print axioms integerLocallyConstant_heterogeneousProduct_finiteRectangles
end CMDG.CondensedCM5R0
