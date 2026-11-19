import CMDGCondensedCM4P3DerivedCM5R0UniformBivariateFiniteObservation
import CMDGCondensedCM4P3DerivedCM5R0AllArityClosedCechRelation

/-!
# Arbitrary-arity finite coordinate observation

Every integer locally constant map on a finite product P^(n+1)
factors through ONE finite locally constant observation q:P→J
applied separately to each coordinate. No arity bound, nonempty
P assumption, or choice of a common observation across different
cochains is required.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem integerLocallyConstant_allFiniteArity_finiteObservation
    (P : Profinite.{u}) :
    ∀ n : ℕ, ∀ f : LocallyConstant (Fin (n + 1) → P) ℤ,
      ∃ (J : Type u) (hJ : Fintype J)
        (q : LocallyConstant P J)
        (d : (Fin (n + 1) → J) → ℤ),
        ∀ xs : Fin (n + 1) → P,
          f xs = d (fun k => q (xs k)) := by
  classical
  intro n
  induction n with
  | zero =>
    intro f
    let δ : P → (Fin 1 → P) := fun x _ => x
    have hδ : Continuous δ := by
      apply continuous_pi
      intro j
      exact continuous_id
    let fP : LocallyConstant P ℤ :=
      f.comap ⟨δ, hδ⟩
    let J : Type u := ULift.{u} (Set.range (fP : P → ℤ))
    haveI : Fintype J := by
      letI : Finite (Set.range (fP : P → ℤ)) :=
        fP.range_finite.to_subtype
      exact Fintype.ofFinite J
    let q : LocallyConstant P J := ⟨fun x =>
      ULift.up ⟨fP x, ⟨x,rfl⟩⟩, by
        apply IsLocallyConstant.iff_isOpen_fiber.mpr
        intro j
        have hfiber :
            (fun x : P => (ULift.up
              (⟨fP x, ⟨x,rfl⟩⟩ : Set.range (fP : P → ℤ)) : J)) ⁻¹' {j} =
                {x : P | fP x = j.down.val} := by
          ext x
          simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_setOf_eq]
          constructor
          · intro h
            exact congrArg (fun t : J => t.down.val) h
          · intro h
            apply ULift.ext
            apply Subtype.ext
            exact h
        rw [hfiber]
        exact fP.isLocallyConstant.isOpen_fiber j.down.val⟩
    let d : (Fin 1 → J) → ℤ := fun σ => (σ 0).down.val
    refine ⟨J, inferInstance, q, d, ?_⟩
    intro xs
    have hs : δ (xs 0) = xs := by
      funext j
      fin_cases j
      rfl
    change f xs = fP (xs 0)
    rw [show fP (xs 0) = f xs from by
      change f (δ (xs 0)) = f xs
      rw [hs]]
  | succ n ih =>
    intro f
    let Q : Profinite.{u} := Profinite.of (Fin (n + 1) → P)
    let ψ : P × Q → (Fin (n + 2) → P) :=
      fun z => Fin.cons z.1 z.2
    have hψ : Continuous ψ := by
      apply continuous_pi
      intro k
      refine Fin.cases ?_ ?_ k
      · exact continuous_fst
      · intro i
        exact (continuous_apply i).comp continuous_snd
    let fpair : LocallyConstant (P × Q) ℤ :=
      f.comap ⟨ψ,hψ⟩
    obtain ⟨I, finitI, qP, qQ, dPair, hpair⟩ :=
      integerLocallyConstant_heterogeneousProduct_finiteRectangles
        P Q fpair
    letI : Fintype I := finitI
    let inj : I → ℤ := fun i =>
      ((Fintype.equivFin I i).val : ℤ)
    have hinj : Function.Injective inj := by
      intro a b h
      apply (Fintype.equivFin I).injective
      apply Fin.ext
      change ((Fintype.equivFin I a).val : ℤ) =
        ((Fintype.equivFin I b).val : ℤ) at h
      exact_mod_cast h
    let fTail : LocallyConstant (Fin (n + 1) → P) ℤ :=
      LocallyConstant.map inj qQ
    obtain ⟨J, finitJ, qR, dR, hR⟩ := ih fTail
    letI : Fintype J := finitJ
    let q : LocallyConstant P (I × J) :=
      ⟨(fun x => (qP x, qR x)),
        qP.isLocallyConstant.prodMk qR.isLocallyConstant⟩
    have hstable (xs ys : Fin (n + 2) → P)
        (hobs : ∀ k : Fin (n + 2), q (xs k) = q (ys k)) :
        f xs = f ys := by
      have hfirst : qP (xs 0) = qP (ys 0) :=
        congrArg Prod.fst (hobs 0)
      have htailQ (k : Fin (n + 1)) :
          qR (xs k.succ) = qR (ys k.succ) :=
        congrArg Prod.snd (hobs k.succ)
      have htailTags : (fun k : Fin (n + 1) =>
          qR ((Fin.tail xs) k)) =
          (fun k : Fin (n + 1) => qR ((Fin.tail ys) k)) := by
        funext k
        exact htailQ k
      have hQ : qQ (Fin.tail xs) = qQ (Fin.tail ys) := by
        apply hinj
        calc
          inj (qQ (Fin.tail xs)) = fTail (Fin.tail xs) := rfl
          _ = dR (fun k => qR ((Fin.tail xs) k)) :=
            hR (Fin.tail xs)
          _ = dR (fun k => qR ((Fin.tail ys) k)) := by
            rw [htailTags]
          _ = fTail (Fin.tail ys) := (hR (Fin.tail ys)).symm
          _ = inj (qQ (Fin.tail ys)) := rfl
      have hx := hpair (xs 0) (Fin.tail xs)
      have hy := hpair (ys 0) (Fin.tail ys)
      change f (Fin.cons (xs 0) (Fin.tail xs)) =
        dPair (qP (xs 0)) (qQ (Fin.tail xs)) at hx
      change f (Fin.cons (ys 0) (Fin.tail ys)) =
        dPair (qP (ys 0)) (qQ (Fin.tail ys)) at hy
      rw [Fin.cons_self_tail] at hx hy
      calc
        f xs = dPair (qP (xs 0)) (qQ (Fin.tail xs)) := hx
        _ = dPair (qP (ys 0)) (qQ (Fin.tail ys)) := by
          rw [hfirst,hQ]
        _ = f ys := hy.symm
    let D (σ : Fin (n + 2) → I × J) : ℤ :=
      if h : ∃ xs : Fin (n + 2) → P,
          (fun k => q (xs k)) = σ
      then f (Classical.choose h)
      else 0
    refine ⟨I × J, inferInstance, q, D, ?_⟩
    intro xs
    have h : ∃ ys : Fin (n + 2) → P,
        (fun k => q (ys k)) = (fun k => q (xs k)) := ⟨xs,rfl⟩
    have hy := Classical.choose_spec h
    have heq : f xs = f (Classical.choose h) :=
      hstable xs (Classical.choose h) (fun k =>
        congrFun hy k |>.symm)
    change f xs = D (fun k => q (xs k))
    dsimp [D]
    rw [dif_pos h]
    exact heq

#print axioms integerLocallyConstant_allFiniteArity_finiteObservation
end CMDG.CondensedCM5R0
