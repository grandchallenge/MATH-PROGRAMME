import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedH5
import CMDGCondensedCM4P3DerivedCM5R0QuintupleFiniteBoxes

/-!
# CM5: finite observation of all six coordinates of a profinite product

Every integer-valued locally constant cochain on P⁶ factors through
ONE common finite observation q:P→J in each coordinate. Pair the
coordinates into three copies of Q=P×P, use protected fourfold
finite-box theorem on Q⁴, then refine the Q-observation using the
protected two-factor finite-rectangle theorem. No finiteness or
nonempty hypothesis on P is assumed.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem integerLocallyConstant_sextupleProduct_finiteBoxes
    (P : Profinite.{u})
    (f : LocallyConstant
      (P × (P × (P × (P × (P × P))))) ℤ) :
    ∃ (J : Type u) (hJ : Fintype J)
      (q : LocallyConstant P J)
      (d : J → J → J → J → J → J → ℤ),
      ∀ x y z w v r : P,
        f (x,(y,(z,(w,(v,r))))) =
          d (q x) (q y) (q z) (q w) (q v) (q r) := by
  classical
  by_cases hP : Nonempty P
  · let filler : P := Classical.choice hP
    let Q : Profinite.{u} := Profinite.of (P × P)
    let ψ : (Q × (Q × (Q × Q))) →
        P × (P × (P × (P × (P × P)))) :=
      fun t => (t.1.1,(t.1.2,
        (t.2.1.1,(t.2.1.2,(t.2.2.1.1,t.2.2.1.2)))))
    have hψ : Continuous ψ := by
      dsimp [ψ, Q]
      fun_prop
    let fQ : LocallyConstant (Q × (Q × (Q × Q))) ℤ :=
      f.comap ⟨ψ,hψ⟩
    obtain ⟨I,fintypeI,qQ,dQ,hQ⟩ :=
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
    obtain ⟨J,fintypeJ,q,dPair,hPair⟩ :=
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
    have hstable (x x' y y' z z' w w' v v' r r' : P)
        (hx : q x = q x') (hy : q y = q y')
        (hz : q z = q z') (hw : q w = q w')
        (hv : q v = q v') (hr : q r = q r') :
        f (x,(y,(z,(w,(v,r))))) =
          f (x',(y',(z',(w',(v',r'))))) := by
      have ha := hconst x x' y y' hx hy
      have hb := hconst z z' w w' hz hw
      have hc := hconst v v' r r' hv hr
      have h1 := hQ (x,y) (z,w) (v,r) (filler,filler)
      have h2 := hQ (x',y') (z',w') (v',r') (filler,filler)
      change f (x,(y,(z,(w,(v,r))))) =
        dQ (qQ (x,y)) (qQ (z,w))
          (qQ (v,r)) (qQ (filler,filler)) at h1
      change f (x',(y',(z',(w',(v',r'))))) =
        dQ (qQ (x',y')) (qQ (z',w'))
          (qQ (v',r')) (qQ (filler,filler)) at h2
      calc
        f (x,(y,(z,(w,(v,r))))) =
          dQ (qQ (x,y)) (qQ (z,w))
            (qQ (v,r)) (qQ (filler,filler)) := h1
        _ = dQ (qQ (x',y')) (qQ (z',w'))
            (qQ (v',r')) (qQ (filler,filler)) := by rw [ha,hb,hc]
        _ = f (x',(y',(z',(w',(v',r'))))) := h2.symm
    let d (i j k l m n : J) : ℤ :=
      if h : ∃ t : P × (P × (P × (P × (P × P)))),
        q t.1 = i ∧ q t.2.1 = j ∧
          q t.2.2.1 = k ∧ q t.2.2.2.1 = l ∧
          q t.2.2.2.2.1 = m ∧ q t.2.2.2.2.2 = n
      then f (Classical.choose h)
      else 0
    refine ⟨J, inferInstance, q, d, ?_⟩
    intro x y z w v r
    have h : ∃ t : P × (P × (P × (P × (P × P)))),
        q t.1 = q x ∧ q t.2.1 = q y ∧
          q t.2.2.1 = q z ∧ q t.2.2.2.1 = q w ∧
          q t.2.2.2.2.1 = q v ∧ q t.2.2.2.2.2 = q r :=
      ⟨(x,(y,(z,(w,(v,r))))),rfl,rfl,rfl,rfl,rfl,rfl⟩
    have hp := Classical.choose_spec h
    have hs := hstable x (Classical.choose h).1
      y (Classical.choose h).2.1
      z (Classical.choose h).2.2.1
      w (Classical.choose h).2.2.2.1
      v (Classical.choose h).2.2.2.2.1
      r (Classical.choose h).2.2.2.2.2
      hp.1.symm hp.2.1.symm hp.2.2.1.symm
      hp.2.2.2.1.symm hp.2.2.2.2.1.symm
      hp.2.2.2.2.2.symm
    change f (x,(y,(z,(w,(v,r))))) =
      d (q x) (q y) (q z) (q w) (q v) (q r)
    dsimp [d]
    rw [dif_pos h]
    exact hs
  · haveI : IsEmpty P := not_nonempty_iff.mp hP
    refine ⟨PUnit.{u+1}, inferInstance,
      LocallyConstant.const P PUnit.unit,
      (fun _ _ _ _ _ _ => 0), ?_⟩
    intro x
    exact isEmptyElim x

#print axioms integerLocallyConstant_sextupleProduct_finiteBoxes
end CMDG.CondensedCM5R0
