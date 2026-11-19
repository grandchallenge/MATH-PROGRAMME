import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedH4
import CMDGCondensedCM4P3DerivedCM5R0QuadrupleFiniteBoxes

/-!
# CM5: arbitrary profinite fifth-product finite observation

Every integer-valued locally constant function on P^5 factors
through a *single* finite observation q:P→J on EACH of the five
coordinates. This does not require P finite or its base totally split.

Proof: apply the already-certified four-factor theorem to the
paired-coordinate profinite Q=P×P, encoding the five original
coordinates in four Q slots with unused padding. Refine the resulting
finite Q observation via the protected two-factor rectangle theorem.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem integerLocallyConstant_quintupleProduct_finiteBoxes
    (P : Profinite.{u})
    (f : LocallyConstant (P × (P × (P × (P × P)))) ℤ) :
    ∃ (J : Type u) (hJ : Fintype J)
      (q : LocallyConstant P J)
      (d : J → J → J → J → J → ℤ),
      ∀ x y z w v : P,
        f (x,(y,(z,(w,v)))) =
          d (q x) (q y) (q z) (q w) (q v) := by
  classical
  by_cases hP : Nonempty P
  · let filler : P := Classical.choice hP
    let Q : Profinite.{u} := Profinite.of (P × P)
    let ψ : (Q × (Q × (Q × Q))) →
        P × (P × (P × (P × P))) :=
      fun t => (t.1.1,(t.1.2,(t.2.1.1,(t.2.1.2,t.2.2.1.1))))
    have hψ : Continuous ψ := by
      dsimp [ψ, Q]
      fun_prop
    let fQ : LocallyConstant (Q × (Q × (Q × Q))) ℤ :=
      f.comap ⟨ψ,hψ⟩
    obtain ⟨I, fintypeI, qQ, dQ, hQ⟩ :=
      integerLocallyConstant_quadrupleProduct_finiteBoxes Q fQ
    letI : Fintype I := fintypeI
    let inj : I → ℤ :=
      fun i => ((Fintype.equivFin I i).val : ℤ)
    have hinj : Function.Injective inj := by
      intro a b h
      apply (Fintype.equivFin I).injective
      apply Fin.ext
      change ((Fintype.equivFin I a).val : ℤ) =
        ((Fintype.equivFin I b).val : ℤ) at h
      exact_mod_cast h
    let g : LocallyConstant (P × P) ℤ :=
      LocallyConstant.map inj qQ
    obtain ⟨J, fintypeJ, q, dPair, hPair⟩ :=
      integerLocallyConstant_product_finiteRectangles P g
    letI : Fintype J := fintypeJ
    have hconst (x x' y y' : P)
        (hx : q x = q x') (hy : q y = q y') :
        qQ (x,y) = qQ (x',y') := by
      apply hinj
      have h1 := hPair x y
      have h2 := hPair x' y'
      change inj (qQ (x,y)) = dPair (q x) (q y) at h1
      change inj (qQ (x',y')) = dPair (q x') (q y') at h2
      calc
        inj (qQ (x,y)) = dPair (q x) (q y) := h1
        _ = dPair (q x') (q y') := by rw [hx,hy]
        _ = inj (qQ (x',y')) := h2.symm
    have hstable (x x' y y' z z' w w' v v' : P)
        (hx : q x = q x') (hy : q y = q y')
        (hz : q z = q z') (hw : q w = q w')
        (hv : q v = q v') :
        f (x,(y,(z,(w,v)))) =
          f (x',(y',(z',(w',v')))) := by
      have ha := hconst x x' y y' hx hy
      have hb := hconst z z' w w' hz hw
      have hc := hconst v v' filler filler hv rfl
      have h1 := hQ (x,y) (z,w) (v,filler) (filler,filler)
      have h2 := hQ (x',y') (z',w') (v',filler) (filler,filler)
      change f (x,(y,(z,(w,v)))) =
        dQ (qQ (x,y)) (qQ (z,w))
          (qQ (v,filler)) (qQ (filler,filler)) at h1
      change f (x',(y',(z',(w',v')))) =
        dQ (qQ (x',y')) (qQ (z',w'))
          (qQ (v',filler)) (qQ (filler,filler)) at h2
      calc
        f (x,(y,(z,(w,v)))) =
          dQ (qQ (x,y)) (qQ (z,w))
            (qQ (v,filler)) (qQ (filler,filler)) := h1
        _ = dQ (qQ (x',y')) (qQ (z',w'))
            (qQ (v',filler)) (qQ (filler,filler)) := by
              rw [ha,hb,hc]
        _ = f (x',(y',(z',(w',v')))) := h2.symm
    let d (i j k l m : J) : ℤ :=
      if h : ∃ t : P × (P × (P × (P × P))),
        q t.1 = i ∧ q t.2.1 = j ∧
          q t.2.2.1 = k ∧ q t.2.2.2.1 = l ∧
          q t.2.2.2.2 = m
      then f (Classical.choose h)
      else 0
    refine ⟨J, inferInstance, q, d, ?_⟩
    intro x y z w v
    have h : ∃ t : P × (P × (P × (P × P))),
        q t.1 = q x ∧ q t.2.1 = q y ∧
          q t.2.2.1 = q z ∧ q t.2.2.2.1 = q w ∧
          q t.2.2.2.2 = q v :=
      ⟨(x,(y,(z,(w,v)))),rfl,rfl,rfl,rfl,rfl⟩
    have hp := Classical.choose_spec h
    have hs := hstable x (Classical.choose h).1
      y (Classical.choose h).2.1
      z (Classical.choose h).2.2.1
      w (Classical.choose h).2.2.2.1
      v (Classical.choose h).2.2.2.2
      hp.1.symm hp.2.1.symm hp.2.2.1.symm
      hp.2.2.2.1.symm hp.2.2.2.2.symm
    change f (x,(y,(z,(w,v)))) =
      d (q x) (q y) (q z) (q w) (q v)
    dsimp [d]
    rw [dif_pos h]
    exact hs
  · haveI : IsEmpty P := not_nonempty_iff.mp hP
    refine ⟨PUnit.{u+1}, inferInstance,
      LocallyConstant.const P PUnit.unit,
      (fun _ _ _ _ _ => 0), ?_⟩
    intro x
    exact isEmptyElim x

#print axioms integerLocallyConstant_quintupleProduct_finiteBoxes
end CMDG.CondensedCM5R0
