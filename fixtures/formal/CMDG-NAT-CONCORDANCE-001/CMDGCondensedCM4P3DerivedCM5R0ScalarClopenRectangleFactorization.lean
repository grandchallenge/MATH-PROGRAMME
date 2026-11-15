import CMDGCondensedCM4P3DerivedCM5R0ScalarRectangularCocyclePotential
import Mathlib.Topology.ClopenBox

/-!
# CM5: automatic finite-rectangle observation of scalar product cochains

Every locally constant integer function on the topological product of
two copies of an arbitrary profinite P depends on one finite
locally constant observation q:P→I of EACH endpoint.

The proof uses the actual pinned mathlib finite clopen-box theorem,
not a postulated common finite quotient of the solid target.
For every value in the finite image, decompose its clopen fiber into
finitely many clopen boxes; record membership in the finitely many
boxes' coordinate clopens. Two pairs with matching coordinate
signatures then lie in exactly the same fibers.

Combining this geometric factorization with the protected finite
closed-family scalar H¹ theorem gives a genuine globally locally
constant primitive for every scalar locally constant cocycle on a
profinite quotient, PROVIDED the cocycle is represented by a scalar
locally constant function on P×P. A separate exact-pullback
comparison transports actual Stonean Čech cochains to this model.

No product-of-ℤ solid coefficient model or derived solidity is claimed.
-/

noncomputable section

universe u

open CategoryTheory Limits Set TopologicalSpace

namespace CMDG.CondensedCM5R0

/-- Explicit classical truth-value indicator of a clopen membership;
the decidability witness is contained in the definition rather than
required as an implicit argument of the theorem statement. -/
noncomputable def clopenIndicator
    (P : Profinite.{u}) (U : Clopens P) (x : P) : Bool :=
  @decide (x ∈ (U : Set P)) (Classical.propDecidable _)

/-- Every clopen membership indicator is locally constant. -/
theorem locallyConstant_decide_clopen
    (P : Profinite.{u}) (U : Clopens P) :
    IsLocallyConstant (clopenIndicator P U) := by
  classical
  apply IsLocallyConstant.iff_isOpen_fiber.mpr
  intro b
  cases b with
  | false =>
    have hset :
        (clopenIndicator P U) ⁻¹' {false} = (U : Set P)ᶜ := by
      ext x
      simp [clopenIndicator]
    rw [hset]
    exact U.isClopen.1.isOpen_compl
  | true =>
    have hset :
        (clopenIndicator P U) ⁻¹' {true} = (U : Set P) := by
      ext x
      simp [clopenIndicator]
    rw [hset]
    exact U.isClopen.2

/-- Arbitrary integer-valued locally constant maps on P×P factor
through two copies of ONE finite locally constant observation on P.
This uses finite clopen-box decomposition and requires only
compactness, not any finite hypothesis on P itself. -/
theorem integerLocallyConstant_product_finiteRectangles
    (P : Profinite.{u})
    (f : LocallyConstant (P × P) ℤ) :
    ∃ (I : Type u) (hI : Fintype I)
      (q : LocallyConstant P I) (d : I → I → ℤ),
      ∀ x y : P, f (x, y) = d (q x) (q y) := by
  classical
  let R := Set.range (f : P × P → ℤ)
  haveI : Finite R := f.range_finite.to_subtype
  letI : Fintype R := Fintype.ofFinite R
  let W (r : R) : Clopens (P × P) :=
    ⟨{z | f z = r.val}, f.isLocallyConstant.isClopen_fiber r.val⟩
  have hboxes (r : R) :
      ∃ Bs : Finset (Clopens P × Clopens P),
        W r = Bs.sup (fun k => k.1 ×ˢ k.2) :=
    TopologicalSpace.Clopens.exists_finset_eq_sup_prod (W r)
  choose Bs hBs using hboxes
  let all : Finset (Clopens P × Clopens P) :=
    Finset.univ.biUnion Bs
  let I : Type u := (↥all → Bool × Bool)
  let sig (x : P) : I := fun k =>
    (clopenIndicator P k.val.1 x,
      clopenIndicator P k.val.2 x)
  have hcoord (k : ↥all) :
      IsLocallyConstant
        (fun x : P =>
          (clopenIndicator P k.val.1 x,
            clopenIndicator P k.val.2 x)) :=
    (locallyConstant_decide_clopen P k.val.1).prodMk
      (locallyConstant_decide_clopen P k.val.2)
  have hsig : IsLocallyConstant sig := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro t
    have hfiber :
        sig ⁻¹' {t} =
          ⋂ k : ↥all, ((fun x : P =>
            (clopenIndicator P k.val.1 x,
              clopenIndicator P k.val.2 x)) ⁻¹' {t k}) := by
      ext x
      simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_iInter]
      exact funext_iff
    rw [hfiber]
    exact isOpen_iInter_of_finite (fun k =>
      (hcoord k).isOpen_fiber (t k))
  let q : LocallyConstant P I := ⟨sig, hsig⟩
  have hstable (x x' y y' : P)
      (hx : q x = q x') (hy : q y = q y') :
      f (x, y) = f (x', y') := by
    let r : R := ⟨f (x, y), ⟨(x, y), rfl⟩⟩
    have hw : (x, y) ∈ W r := rfl
    have hw' : (x, y) ∈
        (↑((Bs r).sup (fun k => k.1 ×ˢ k.2)) :
          Set (P × P)) := by
      rw [← hBs r]
      exact hw
    rw [TopologicalSpace.Clopens.coe_finset_sup] at hw'
    obtain ⟨k, hk, hxy⟩ := Set.mem_iUnion₂.mp hw'
    have hxk : x ∈ (k.1 : Set P) := hxy.1
    have hyk : y ∈ (k.2 : Set P) := hxy.2
    have hkall : k ∈ all :=
      Finset.mem_biUnion.mpr ⟨r, Finset.mem_univ _, hk⟩
    let kk : ↥all := ⟨k, hkall⟩
    have hxl := congrArg Prod.fst (congrFun hx kk)
    have hyr := congrArg Prod.snd (congrFun hy kk)
    change clopenIndicator P k.1 x =
      clopenIndicator P k.1 x' at hxl
    change clopenIndicator P k.2 y =
      clopenIndicator P k.2 y' at hyr
    have hxk' : x' ∈ (k.1 : Set P) := by
      by_contra hn
      simp [clopenIndicator, hxk, hn] at hxl
    have hyk' : y' ∈ (k.2 : Set P) := by
      by_contra hn
      simp [clopenIndicator, hyk, hn] at hyr
    have hw2' : (x', y') ∈
        (↑((Bs r).sup (fun k => k.1 ×ˢ k.2)) :
          Set (P × P)) := by
      rw [TopologicalSpace.Clopens.coe_finset_sup]
      apply Set.mem_iUnion₂.mpr
      exact ⟨k, hk, ⟨hxk', hyk'⟩⟩
    have hw2 : (x', y') ∈ W r := by
      rw [hBs r]
      exact hw2'
    have hf2 : f (x', y') = r.val := hw2
    exact hf2.symm
  let d (i j : I) : ℤ :=
    if h : ∃ z : P × P, q z.1 = i ∧ q z.2 = j then
      f (Classical.choose h)
    else 0
  letI : Fintype I := Fintype.ofFinite I
  refine ⟨I, inferInstance, q, d, ?_⟩
  intro x y
  have h : ∃ z : P × P,
      q z.1 = q x ∧ q z.2 = q y := ⟨(x, y), rfl, rfl⟩
  have hz := Classical.choose_spec h
  have hconst := hstable x (Classical.choose h).1
    y (Classical.choose h).2 hz.1.symm hz.2.symm
  change f (x, y) = d (q x) (q y)
  dsimp [d]
  rw [dif_pos h]
  exact hconst

/-- Every locally constant integer-valued cocycle on the product
P×P that satisfies the cocycle law on the fibers of an arbitrary
profinite map p:P→T admits an actual locally constant primitive.
No finite-rectangular assumption is left in this result. -/
theorem integerProfiniteCocycle_ambientProduct_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (P × P) ℤ)
    (hc : ∀ x y z : P,
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      c (x, z) = c (x, y) + c (y, z)) :
    ∃ b : LocallyConstant P ℤ,
      ∀ x y : P, p.hom.hom x = p.hom.hom y →
        c (x, y) = b x - b y := by
  obtain ⟨I, fintypeI, q, d, hrect⟩ :=
    integerLocallyConstant_product_finiteRectangles P c
  letI : Fintype I := fintypeI
  haveI : Finite I := Finite.of_fintype I
  exact integerProfiniteCocycle_potential_of_finiteRectangles
    P T p q d (fun x y => c (x, y)) hc
      (fun x y _ => hrect x y)

#print axioms locallyConstant_decide_clopen
#print axioms integerLocallyConstant_product_finiteRectangles
#print axioms integerProfiniteCocycle_ambientProduct_potential

end CMDG.CondensedCM5R0
