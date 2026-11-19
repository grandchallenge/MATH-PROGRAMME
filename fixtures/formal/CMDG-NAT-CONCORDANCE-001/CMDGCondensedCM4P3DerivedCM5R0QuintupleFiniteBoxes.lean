import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverH4CocycleInduction
import CMDGCondensedCM4P3DerivedCM5R0TripleClopenBoxFactorization

/-!
# CM5: one finite clopen observation of all five profinite coordinates

Embed a fivefold locally constant cochain in a sixfold cochain
by duplicating the fifth coordinate. Group six coordinates as two
triples. Apply the finite-rectangle factorization to P³×P³.
Encode the finite observation of P³ injectively into integers, then
use the protected triple finite-box factorization. Obtain a single
locally constant finite observation q:P→J of all five vertices.
No finite assumption on P.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem integerLocallyConstant_quintupleProduct_finiteBoxes
    (P : Profinite.{u})
    (f : LocallyConstant (P × (P × (P × (P × P)))) ℤ) :
    ∃ (J : Type u) (hJ : Fintype J)
      (q : LocallyConstant P J) (d : J → J → J → J → J → ℤ),
      ∀ x y z w v : P,
        f (x,(y,(z,(w,v)))) =
          d (q x) (q y) (q z) (q w) (q v) := by
  classical
  let Q : Profinite.{u} := Profinite.of (P × (P × P))
  let ψ : (Q × Q) → P × (P × (P × (P × P))) :=
    fun t => (t.1.1,(t.1.2.1,(t.1.2.2,
      (t.2.1,t.2.2.1))))
  have hψ : Continuous ψ := by
    change Continuous (fun t : (P × (P × P)) × (P × (P × P)) =>
      (t.1.1,(t.1.2.1,(t.1.2.2,(t.2.1,t.2.2.1)))))
    fun_prop
  let fQ : LocallyConstant (Q × Q) ℤ := f.comap ⟨ψ,hψ⟩
  obtain ⟨I, fintypeI, qQ, dQ, hQ⟩ :=
    integerLocallyConstant_product_finiteRectangles Q fQ
  letI : Fintype I := fintypeI
  let inj : I → ℤ := fun i => ((Fintype.equivFin I i).val : ℤ)
  have hinj : Function.Injective inj := by
    intro a b h
    apply (Fintype.equivFin I).injective
    apply Fin.ext
    change ((Fintype.equivFin I a).val : ℤ) =
      ((Fintype.equivFin I b).val : ℤ) at h
    exact_mod_cast h
  let g : LocallyConstant (P × (P × P)) ℤ :=
    LocallyConstant.map inj qQ
  obtain ⟨J, fintypeJ, q, dTrip, hTrip⟩ :=
    integerLocallyConstant_tripleProduct_finiteBoxes P g
  letI : Fintype J := fintypeJ
  have hconst (x x' y y' z z' : P)
      (hx : q x = q x') (hy : q y = q y')
      (hz : q z = q z') :
      qQ (x,(y,z)) = qQ (x',(y',z')) := by
    apply hinj
    have h1 := hTrip x y z
    have h2 := hTrip x' y' z'
    change inj (qQ (x,(y,z))) = dTrip (q x) (q y) (q z) at h1
    change inj (qQ (x',(y',z'))) = dTrip (q x') (q y') (q z') at h2
    calc
      inj (qQ (x,(y,z))) = dTrip (q x) (q y) (q z) := h1
      _ = dTrip (q x') (q y') (q z') := by rw [hx,hy,hz]
      _ = inj (qQ (x',(y',z'))) := h2.symm
  have hstable (x x' y y' z z' w w' v v' : P)
      (hx : q x = q x') (hy : q y = q y')
      (hz : q z = q z') (hw : q w = q w')
      (hv : q v = q v') :
      f (x,(y,(z,(w,v)))) = f (x',(y',(z',(w',v')))) := by
    have ha := hconst x x' y y' z z' hx hy hz
    have hb := hconst w w' v v' v v' hw hv hv
    have h1 := hQ (x,(y,z)) (w,(v,v))
    have h2 := hQ (x',(y',z')) (w',(v',v'))
    change f (x,(y,(z,(w,v)))) =
      dQ (qQ (x,(y,z))) (qQ (w,(v,v))) at h1
    change f (x',(y',(z',(w',v')))) =
      dQ (qQ (x',(y',z'))) (qQ (w',(v',v'))) at h2
    calc
      f (x,(y,(z,(w,v)))) =
        dQ (qQ (x,(y,z))) (qQ (w,(v,v))) := h1
      _ = dQ (qQ (x',(y',z'))) (qQ (w',(v',v'))) := by rw [ha,hb]
      _ = f (x',(y',(z',(w',v')))) := h2.symm
  let d (i j k l m : J) : ℤ :=
    if h : ∃ t : P × (P × (P × (P × P))),
      q t.1 = i ∧ q t.2.1 = j ∧ q t.2.2.1 = k ∧
        q t.2.2.2.1 = l ∧ q t.2.2.2.2 = m
    then f (Classical.choose h)
    else 0
  refine ⟨J, inferInstance, q, d, ?_⟩
  intro x y z w v
  have h : ∃ t : P × (P × (P × (P × P))),
      q t.1 = q x ∧ q t.2.1 = q y ∧
        q t.2.2.1 = q z ∧ q t.2.2.2.1 = q w ∧
        q t.2.2.2.2 = q v :=
    ⟨(x,(y,(z,(w,v)))),rfl,rfl,rfl,rfl,rfl⟩
  have hw := Classical.choose_spec h
  have hconst' := hstable x (Classical.choose h).1
    y (Classical.choose h).2.1 z (Classical.choose h).2.2.1
    w (Classical.choose h).2.2.2.1
    v (Classical.choose h).2.2.2.2
    hw.1.symm hw.2.1.symm hw.2.2.1.symm
      hw.2.2.2.1.symm hw.2.2.2.2.symm
  change f (x,(y,(z,(w,v)))) =
    d (q x) (q y) (q z) (q w) (q v)
  dsimp [d]
  rw [dif_pos h]
  exact hconst'

#print axioms integerLocallyConstant_quintupleProduct_finiteBoxes
end CMDG.CondensedCM5R0
