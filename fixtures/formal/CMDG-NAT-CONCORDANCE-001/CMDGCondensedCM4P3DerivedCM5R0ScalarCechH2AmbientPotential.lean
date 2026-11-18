import CMDGCondensedCM4P3DerivedCM5R0TripleClopenBoxFactorization
import Mathlib.Topology.LocallyConstant.Algebra

/-!
# CM5 — scalar Čech H² primitive on arbitrary profinite product nerves

For any profinite morphism p:P→T, a globally locally constant integer
function on P³ satisfying the alternating degree-three cocycle identity
only for points of the same p-fiber admits a globally locally constant
one-cochain on P² satisfying the sign-exact degree-two boundary identity.
The proof uses the triple finite-observation theorem and finite closed-cover
H² theorem. Crucially, E_i=p(q⁻¹(i)) are closed (not necessarily open),
and the pair potential varies locally constantly with both q-labels and
p(x). No global section of p is selected.
-/

noncomputable section
universe u
open CategoryTheory Limits Set TopologicalSpace

namespace CMDG.CondensedCM5R0

theorem integerProfiniteTwoCocycle_ambientTriple_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (P × (P × P)) ℤ)
    (hc : ∀ x y z w : P,
       p.hom.hom x = p.hom.hom y →
       p.hom.hom y = p.hom.hom z →
       p.hom.hom z = p.hom.hom w →
       c (y, (z, w)) - c (x, (z, w)) +
         c (x, (y, w)) - c (x, (y, z)) = 0) :
    ∃ b : LocallyConstant (P × P) ℤ,
      ∀ x y z : P,
        p.hom.hom x = p.hom.hom y →
        p.hom.hom y = p.hom.hom z →
        c (x, (y, z)) = b (y, z) - b (x, z) + b (x, y) := by
  classical
  obtain ⟨I, fintypeI, q, d, hfact⟩ :=
    integerLocallyConstant_tripleProduct_finiteBoxes P c
  letI : Fintype I := fintypeI
  let E : I → Set T :=
    fun i => p.hom.hom '' {x : P | q x = i}
  have hclosed (i : I) : IsClosed (E i) := by
    have hc : IsClosed {x : P | q x = i} :=
      (q.isLocallyConstant.isClopen_fiber i).1
    have hcompact : IsCompact {x : P | q x = i} :=
      hc.isCompact
    exact (hcompact.image p.hom.hom.continuous).isClosed
  let cI : (i j k : I) → LocallyConstant (↥((E i ∩ E j) ∩ E k)) ℤ :=
    fun i j k => LocallyConstant.const _ (d i j k)
  have hcI : ∀ (i j k l : I) (t : T)
      (hi : t ∈ E i) (hj : t ∈ E j)
      (hk : t ∈ E k) (hl : t ∈ E l),
        cI j k l ⟨t, ⟨⟨hj, hk⟩, hl⟩⟩ -
        cI i k l ⟨t, ⟨⟨hi, hk⟩, hl⟩⟩ +
        cI i j l ⟨t, ⟨⟨hi, hj⟩, hl⟩⟩ -
        cI i j k ⟨t, ⟨⟨hi, hj⟩, hk⟩⟩ = 0 := by
    intro i j k l t hi hj hk hl
    obtain ⟨xi, hxi, hpxi⟩ := hi
    obtain ⟨xj, hxj, hpxj⟩ := hj
    obtain ⟨xk, hxk, hpxk⟩ := hk
    obtain ⟨xl, hxl, hpxl⟩ := hl
    change q xi = i at hxi
    change q xj = j at hxj
    change q xk = k at hxk
    change q xl = l at hxl
    have hxy : p.hom.hom xi = p.hom.hom xj :=
      hpxi.trans hpxj.symm
    have hyz : p.hom.hom xj = p.hom.hom xk :=
      hpxj.trans hpxk.symm
    have hzw : p.hom.hom xk = p.hom.hom xl :=
      hpxk.trans hpxl.symm
    have h := hc xi xj xk xl hxy hyz hzw
    rw [hfact xj xk xl, hfact xi xk xl,
      hfact xi xj xl, hfact xi xj xk] at h
    change d j k l - d i k l + d i j l - d i j k = 0
    simpa [hxi, hxj, hxk, hxl] using h
  obtain ⟨bI, hbI⟩ :=
    integerFiniteClosedFamily_twoCocycle_is_coboundary
      T E hclosed cI hcI
  let g : P × P → ℤ := fun xy =>
    bI (q xy.1) (q xy.2) (p.hom.hom xy.1)
  have hg : IsLocallyConstant g := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro n
    have hfiber : g ⁻¹' {n} =
        ⋃ i : I, ⋃ j : I,
          ({xy : P × P | q xy.1 = i} ∩
           {xy : P × P | q xy.2 = j}) ∩
          {xy : P × P | bI i j (p.hom.hom xy.1) = n} := by
      ext xy
      simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_iUnion,
        Set.mem_inter_iff, Set.mem_setOf_eq]
      constructor
      · intro h
        exact ⟨q xy.1, q xy.2, ⟨rfl, rfl⟩, h⟩
      · rintro ⟨i, j, ⟨hi, hj⟩, h⟩
        simpa only [g, hi, hj] using h
    rw [hfiber]
    apply isOpen_iUnion
    intro i
    apply isOpen_iUnion
    intro j
    have hq1 : IsOpen {xy : P × P | q xy.1 = i} := by
      exact (q.isLocallyConstant.isOpen_fiber i).preimage continuous_fst
    have hq2 : IsOpen {xy : P × P | q xy.2 = j} := by
      exact (q.isLocallyConstant.isOpen_fiber j).preimage continuous_snd
    have hcij : IsOpen {xy : P × P |
        bI i j (p.hom.hom xy.1) = n} := by
      exact ((bI i j).isLocallyConstant.isOpen_fiber n).preimage
        (p.hom.hom.continuous.comp continuous_fst)
    exact (hq1.inter hq2).inter hcij
  let b : LocallyConstant (P × P) ℤ := ⟨g, hg⟩
  refine ⟨b, ?_⟩
  intro x y z hxy hyz
  have hxE : p.hom.hom x ∈ E (q x) :=
    ⟨x, rfl, rfl⟩
  have hyE : p.hom.hom x ∈ E (q y) :=
    ⟨y, rfl, hxy.symm⟩
  have hzE : p.hom.hom x ∈ E (q z) :=
    ⟨z, rfl, (hxy.trans hyz).symm⟩
  have h := hbI (q x) (q y) (q z) (p.hom.hom x)
    hxE hyE hzE
  change d (q x) (q y) (q z) =
    bI (q y) (q z) (p.hom.hom x) -
    bI (q x) (q z) (p.hom.hom x) +
    bI (q x) (q y) (p.hom.hom x) at h
  rw [hfact x y z]
  change d (q x) (q y) (q z) =
    bI (q y) (q z) (p.hom.hom y) -
    bI (q x) (q z) (p.hom.hom x) +
    bI (q x) (q y) (p.hom.hom x)
  rw [← hxy]
  exact h

#print axioms integerProfiniteTwoCocycle_ambientTriple_potential

end CMDG.CondensedCM5R0
