import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverH2CocycleInduction
import CMDGCondensedCM4P3DerivedCM5R0ScalarClopenRectangleFactorization

/-!
# CM5 — finite clopen observation for any scalar triple-product cochain

On P×P×P for arbitrary profinite P, a locally constant integer-valued
function is determined by one finite clopen observation q:P→I on each
of the three coordinates. We first decompose each clopen fiber into
outer rectangles on P×(P×P), then inner rectangles on P×P. The joint
finite signature detects all box memberships. No assumption about a
uniform finite quotient of a potentially infinite product coefficient
target is made.
-/

noncomputable section

universe u

open CategoryTheory Limits Set TopologicalSpace

namespace CMDG.CondensedCM5R0

theorem integerLocallyConstant_tripleProduct_finiteBoxes
    (P : Profinite.{u})
    (f : LocallyConstant (P × (P × P)) ℤ) :
    ∃ (I : Type u) (hI : Fintype I)
      (q : LocallyConstant P I) (d : I → I → I → ℤ),
      ∀ x y z : P, f (x, (y, z)) = d (q x) (q y) (q z) := by
  classical
  let R := Set.range (f : P × (P × P) → ℤ)
  haveI : Finite R := f.range_finite.to_subtype
  letI : Fintype R := Fintype.ofFinite R
  let W (r : R) : Clopens (P × (P × P)) :=
    ⟨{z | f z = r.val}, f.isLocallyConstant.isClopen_fiber r.val⟩
  have houter (r : R) :
      ∃ Bs : Finset (Clopens P × Clopens (P × P)),
        W r = Bs.sup (fun k => k.1 ×ˢ k.2) :=
    TopologicalSpace.Clopens.exists_finset_eq_sup_prod (W r)
  choose Bs hBs using houter
  have hinner (k : Clopens (P × P)) :
      ∃ Cs : Finset (Clopens P × Clopens P),
        k = Cs.sup (fun m => m.1 ×ˢ m.2) :=
    TopologicalSpace.Clopens.exists_finset_eq_sup_prod k
  choose Cs hCs using hinner
  let outer : Finset (Clopens P × Clopens (P × P)) :=
    Finset.univ.biUnion Bs
  let inner : Finset (Clopens P × Clopens P) :=
    outer.biUnion (fun k => Cs k.2)
  let A : Finset (Clopens P) := outer.image Prod.fst
  let B : Finset (Clopens P) := inner.image Prod.fst
  let C : Finset (Clopens P) := inner.image Prod.snd
  let I : Type u :=
    (↥A → Bool) × ((↥B → Bool) × (↥C → Bool))
  let sig (x : P) : I :=
    (fun j : ↥A => clopenIndicator P j.val x,
      ((fun j : ↥B => clopenIndicator P j.val x),
       (fun j : ↥C => clopenIndicator P j.val x)))
  have hcoord (D : Finset (Clopens P)) :
      IsLocallyConstant
        (fun x : P => fun j : ↥D => clopenIndicator P j.val x) := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro t
    have hfiber :
        (fun x : P => fun j : ↥D => clopenIndicator P j.val x) ⁻¹' {t} =
          ⋂ j : ↥D, ((fun x : P => clopenIndicator P j.val x) ⁻¹' {t j}) := by
      ext x
      simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_iInter]
      exact funext_iff
    rw [hfiber]
    exact isOpen_iInter_of_finite
      (fun j => (locallyConstant_decide_clopen P j.val).isOpen_fiber (t j))
  have hsig : IsLocallyConstant sig :=
    (hcoord A).prodMk ((hcoord B).prodMk (hcoord C))
  let q : LocallyConstant P I := ⟨sig, hsig⟩
  have hstable (x x' y y' z z' : P)
      (hx : q x = q x') (hy : q y = q y') (hz : q z = q z') :
      f (x, (y, z)) = f (x', (y', z')) := by
    let r : R := ⟨f (x, (y, z)), ⟨(x, (y, z)), rfl⟩⟩
    have hw : (x, (y, z)) ∈ W r := rfl
    have hw' : (x, (y, z)) ∈
        (↑((Bs r).sup (fun k => k.1 ×ˢ k.2)) :
          Set (P × (P × P))) := by
      rw [← hBs r]
      exact hw
    rw [TopologicalSpace.Clopens.coe_finset_sup] at hw'
    obtain ⟨k, hk, hxyz⟩ := Set.mem_iUnion₂.mp hw'
    have hxk : x ∈ (k.1 : Set P) := hxyz.1
    have hyzk : (y, z) ∈ (k.2 : Set (P × P)) := hxyz.2
    have hin' : (y, z) ∈
        (↑((Cs k.2).sup (fun m => m.1 ×ˢ m.2)) : Set (P × P)) := by
      rw [← hCs k.2]
      exact hyzk
    rw [TopologicalSpace.Clopens.coe_finset_sup] at hin'
    obtain ⟨m, hm, hyz⟩ := Set.mem_iUnion₂.mp hin'
    have hym : y ∈ (m.1 : Set P) := hyz.1
    have hzm : z ∈ (m.2 : Set P) := hyz.2
    have hkOuter : k ∈ outer :=
      Finset.mem_biUnion.mpr ⟨r, Finset.mem_univ _, hk⟩
    have hmInner : m ∈ inner :=
      Finset.mem_biUnion.mpr ⟨k, hkOuter, hm⟩
    have hkA : k.1 ∈ A :=
      Finset.mem_image.mpr ⟨k, hkOuter, rfl⟩
    have hmB : m.1 ∈ B :=
      Finset.mem_image.mpr ⟨m, hmInner, rfl⟩
    have hmC : m.2 ∈ C :=
      Finset.mem_image.mpr ⟨m, hmInner, rfl⟩
    let kk : ↥A := ⟨k.1, hkA⟩
    let mmB : ↥B := ⟨m.1, hmB⟩
    let mmC : ↥C := ⟨m.2, hmC⟩
    have hxl := congrFun (congrArg Prod.fst hx) kk
    have hyl := congrFun (congrArg (fun t : I => t.2.1) hy) mmB
    have hzl := congrFun (congrArg (fun t : I => t.2.2) hz) mmC
    change clopenIndicator P k.1 x =
      clopenIndicator P k.1 x' at hxl
    change clopenIndicator P m.1 y =
      clopenIndicator P m.1 y' at hyl
    change clopenIndicator P m.2 z =
      clopenIndicator P m.2 z' at hzl
    have hxk' : x' ∈ (k.1 : Set P) := by
      by_contra hn
      simp [clopenIndicator, hxk, hn] at hxl
    have hym' : y' ∈ (m.1 : Set P) := by
      by_contra hn
      simp [clopenIndicator, hym, hn] at hyl
    have hzm' : z' ∈ (m.2 : Set P) := by
      by_contra hn
      simp [clopenIndicator, hzm, hn] at hzl
    have hin2' : (y', z') ∈
        (↑((Cs k.2).sup (fun mm => mm.1 ×ˢ mm.2)) : Set (P × P)) := by
      rw [TopologicalSpace.Clopens.coe_finset_sup]
      apply Set.mem_iUnion₂.mpr
      exact ⟨m, hm, ⟨hym', hzm'⟩⟩
    have hin2 : (y', z') ∈ (k.2 : Set (P × P)) := by
      rw [hCs k.2]
      exact hin2'
    have hout2' : (x', (y', z')) ∈
        (↑((Bs r).sup (fun kk => kk.1 ×ˢ kk.2)) :
          Set (P × (P × P))) := by
      rw [TopologicalSpace.Clopens.coe_finset_sup]
      apply Set.mem_iUnion₂.mpr
      exact ⟨k, hk, ⟨hxk', hin2⟩⟩
    have hw2 : (x', (y', z')) ∈ W r := by
      rw [hBs r]
      exact hout2'
    have hf2 : f (x', (y', z')) = r.val := hw2
    exact hf2.symm
  let d (i j k : I) : ℤ :=
    if h : ∃ w : P × (P × P),
      q w.1 = i ∧ q w.2.1 = j ∧ q w.2.2 = k then
      f (Classical.choose h)
    else 0
  letI : Fintype I := Fintype.ofFinite I
  refine ⟨I, inferInstance, q, d, ?_⟩
  intro x y z
  have h : ∃ w : P × (P × P),
      q w.1 = q x ∧ q w.2.1 = q y ∧ q w.2.2 = q z :=
    ⟨(x, (y, z)), rfl, rfl, rfl⟩
  have hchosen := Classical.choose_spec h
  have hconst := hstable x (Classical.choose h).1
    y (Classical.choose h).2.1 z (Classical.choose h).2.2
    hchosen.1.symm hchosen.2.1.symm hchosen.2.2.symm
  change f (x, (y, z)) = d (q x) (q y) (q z)
  dsimp [d]
  rw [dif_pos h]
  exact hconst

#print axioms integerLocallyConstant_tripleProduct_finiteBoxes

end CMDG.CondensedCM5R0
