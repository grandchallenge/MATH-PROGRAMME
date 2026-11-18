import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverH3CocycleInduction
import CMDGCondensedCM4P3DerivedCM5R0ScalarClopenRectangleFactorization

/-!
# CMDG CM5 — one finite clopen observation of all four coordinates

For every profinite P and locally constant integer map on genuine
P⁴, one finite locally constant observation q:P→J of each of
the FOUR coordinates suffices to reconstruct the entire map.

Group the four coordinates into two copies of Q=P×P. Apply the
protected two-variable finite clopen-rectangle factorization
to obtain a finite observation qQ of Q. Inject its finite
codomain into ℤ; factor this integer-valued observation through
a single finite locally constant q on P by reapplying the
same rectangle theorem. The injectivity of the encoding shows
qQ(x,y) depends only on (q x,q y), hence the original cochain
depends only on (q x,q y,q z,q w). No finite assumption on P.

This is the precise fourth-product finite-observation theorem
needed for the scalar H³ reduction. It is not Ext³ vanishing.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

theorem integerLocallyConstant_quadrupleProduct_finiteBoxes
    (P : Profinite.{u})
    (f : LocallyConstant (P × (P × (P × P))) ℤ) :
    ∃ (J : Type u) (hJ : Fintype J)
      (q : LocallyConstant P J) (d : J → J → J → J → ℤ),
      ∀ x y z w : P,
        f (x,(y,(z,w))) = d (q x) (q y) (q z) (q w) := by
  classical
  let Q : Profinite.{u} := Profinite.of (P × P)
  let ψ : (Q × Q) → P × (P × (P × P)) :=
    fun t => (t.1.1, (t.1.2, (t.2.1, t.2.2)))
  have hψ : Continuous ψ :=
    (continuous_fst.comp continuous_fst).prodMk
      ((continuous_snd.comp continuous_fst).prodMk
        ((continuous_fst.comp continuous_snd).prodMk
          (continuous_snd.comp continuous_snd)))
  let fQ : LocallyConstant (Q × Q) ℤ :=
    f.comap ⟨ψ,hψ⟩
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
  have hstable (x x' y y' z z' w w' : P)
      (hx : q x = q x') (hy : q y = q y')
      (hz : q z = q z') (hw : q w = q w') :
      f (x,(y,(z,w))) = f (x',(y',(z',w'))) := by
    have ha := hconst x x' y y' hx hy
    have hb := hconst z z' w w' hz hw
    have h1 := hQ (x,y) (z,w)
    have h2 := hQ (x',y') (z',w')
    change f (x,(y,(z,w))) =
      dQ (qQ (x,y)) (qQ (z,w)) at h1
    change f (x',(y',(z',w'))) =
      dQ (qQ (x',y')) (qQ (z',w')) at h2
    calc
      f (x,(y,(z,w))) = dQ (qQ (x,y)) (qQ (z,w)) := h1
      _ = dQ (qQ (x',y')) (qQ (z',w')) := by rw [ha,hb]
      _ = f (x',(y',(z',w'))) := h2.symm
  let d (i j k l : J) : ℤ :=
    if h : ∃ t : P × (P × (P × P)),
      q t.1 = i ∧ q t.2.1 = j ∧ q t.2.2.1 = k ∧ q t.2.2.2 = l
    then f (Classical.choose h)
    else 0
  refine ⟨J, inferInstance, q, d, ?_⟩
  intro x y z w
  have h : ∃ t : P × (P × (P × P)),
      q t.1 = q x ∧ q t.2.1 = q y ∧
      q t.2.2.1 = q z ∧ q t.2.2.2 = q w :=
    ⟨(x,(y,(z,w))), rfl, rfl, rfl, rfl⟩
  have hw := Classical.choose_spec h
  have hconst' := hstable x (Classical.choose h).1
    y (Classical.choose h).2.1 z (Classical.choose h).2.2.1
    w (Classical.choose h).2.2.2 hw.1.symm hw.2.1.symm
      hw.2.2.1.symm hw.2.2.2.symm
  change f (x,(y,(z,w))) = d (q x) (q y) (q z) (q w)
  dsimp [d]
  rw [dif_pos h]
  exact hconst'

#print axioms integerLocallyConstant_quadrupleProduct_finiteBoxes
end CMDG.CondensedCM5R0
