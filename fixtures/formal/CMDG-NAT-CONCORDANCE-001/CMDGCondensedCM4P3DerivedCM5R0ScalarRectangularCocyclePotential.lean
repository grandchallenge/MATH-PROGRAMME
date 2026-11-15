import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverCocycleInduction
import Mathlib.Topology.LocallyConstant.Algebra

/-!
# CM5: continuous integer potentials for rectangularly finite Čech cocycles

This is the constructive passage from the protected finite closed-cover
cocycle theorem to an arbitrary profinite quotient map p : P → T.

A scalar cocycle c on the actual equivalence relation of p is not
solved by selecting one point in each fiber; that selection need not
be continuous. Instead, when its values are determined by finitely
many clopen source cells, the images of those cells form a finite
closed cover of T. The previously proved finite closed-cover theorem
supplies global locally constant potentials, whose composition with
the original map yields a genuine locally constant primitive on P.

This theorem does not assume finite P or T, a splitting of p,
or a finite quotient of T. The remaining unconditional scalar step
is rectangular factorization of every locally constant scalar
cochain on the Čech relation, after the protected extension of
that cochain to P × P.
-/

noncomputable section

universe u v

open CategoryTheory Limits Set

namespace CMDG.CondensedCM5R0

/-- A *genuine locally constant* primitive for a cocycle on an
arbitrary profinite quotient, assuming its scalar values depend
on a single finite clopen observation q of each source endpoint.

The cocycle condition is only imposed when the three points lie
over one base point. All topological continuity is proved; no
fiberwise choice function appears in the conclusion. -/
theorem integerProfiniteCocycle_potential_of_finiteRectangles
    (P T : Profinite.{u}) (p : P ⟶ T)
    {I : Type v} [Fintype I]
    (q : LocallyConstant P I)
    (d : I → I → ℤ)
    (c : P → P → ℤ)
    (hc : ∀ x y z : P,
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      c x z = c x y + c y z)
    (hrect : ∀ x y : P, p.hom.hom x = p.hom.hom y →
      c x y = d (q x) (q y)) :
    ∃ b : LocallyConstant P ℤ,
      ∀ x y : P, p.hom.hom x = p.hom.hom y →
        c x y = b x - b y := by
  classical
  let E : I → Set T :=
    fun i => p.hom.hom '' ((q : P → I) ⁻¹' {i})
  have hEclosed (i : I) : IsClosed (E i) := by
    exact (CompHausLike.isClosedMap p) _
      (q.isLocallyConstant.isClopen_fiber i).1
  let co : (i j : I) → LocallyConstant (↥(E i ∩ E j)) ℤ :=
    fun i j => LocallyConstant.const _ (d i j)
  have hco (i j k : I) (t : T)
      (hi : t ∈ E i) (hj : t ∈ E j) (hk : t ∈ E k) :
      co i k ⟨t, ⟨hi, hk⟩⟩ =
        co i j ⟨t, ⟨hi, hj⟩⟩ +
          co j k ⟨t, ⟨hj, hk⟩⟩ := by
    change d i k = d i j + d j k
    obtain ⟨x, hqx, hpx⟩ := hi
    obtain ⟨y, hqy, hpy⟩ := hj
    obtain ⟨z, hqz, hpz⟩ := hk
    simp only [Set.mem_preimage, Set.mem_singleton_iff] at hqx hqy hqz
    have hxy : p.hom.hom x = p.hom.hom y := hpx.trans hpy.symm
    have hyz : p.hom.hom y = p.hom.hom z := hpy.trans hpz.symm
    have hxz : p.hom.hom x = p.hom.hom z := hxy.trans hyz
    have hxk := hrect x z hxz
    have hxi := hrect x y hxy
    have hyk := hrect y z hyz
    calc
      d i k = c x z := by simpa only [hqx, hqz] using hxk.symm
      _ = c x y + c y z := hc x y z hxy hyz
      _ = d i j + d j k := by rw [hxi, hyk, hqx, hqy, hqz]
  obtain ⟨a, ha⟩ :=
    integerFiniteClosedFamily_cocycle_is_coboundary T E hEclosed co hco
  have hbLC :
      IsLocallyConstant
        (fun x : P => a (q x) (p.hom.hom x)) := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro n
    have hfiber :
        (fun x : P => a (q x) (p.hom.hom x)) ⁻¹' ({n} : Set ℤ) =
          ⋃ i : I, ((q : P → I) ⁻¹' {i}) ∩
            ((fun x : P => a i (p.hom.hom x)) ⁻¹' {n}) := by
      ext x
      simp only [Set.mem_preimage, Set.mem_singleton_iff,
        Set.mem_iUnion, Set.mem_inter_iff]
      constructor
      · intro hx
        exact ⟨q x, rfl, hx⟩
      · rintro ⟨i, hi, hx⟩
        simpa only [hi] using hx
    rw [hfiber]
    apply isOpen_iUnion
    intro i
    exact (q.isLocallyConstant.isOpen_fiber i).inter
      (((a i).isLocallyConstant.isOpen_fiber n).preimage
        p.hom.hom.continuous)
  refine ⟨⟨fun x => a (q x) (p.hom.hom x), hbLC⟩, ?_⟩
  intro x y hxy
  have hxE : p.hom.hom x ∈ E (q x) :=
    ⟨x, by simp, rfl⟩
  have hyE : p.hom.hom x ∈ E (q y) :=
    ⟨y, by simp, hxy.symm⟩
  have ht := ha (q x) (q y) (p.hom.hom x) hxE hyE
  change d (q x) (q y) =
    a (q x) (p.hom.hom x) - a (q y) (p.hom.hom x) at ht
  calc
    c x y = d (q x) (q y) := hrect x y hxy
    _ = a (q x) (p.hom.hom x) -
          a (q y) (p.hom.hom x) := ht
    _ = a (q x) (p.hom.hom x) -
          a (q y) (p.hom.hom y) := by rw [hxy]

#print axioms integerProfiniteCocycle_potential_of_finiteRectangles

end CMDG.CondensedCM5R0
