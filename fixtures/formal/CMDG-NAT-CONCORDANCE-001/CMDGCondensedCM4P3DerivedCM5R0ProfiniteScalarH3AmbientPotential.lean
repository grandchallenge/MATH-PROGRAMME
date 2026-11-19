import CMDGCondensedCM4P3DerivedCM5R0QuadrupleFiniteBoxes
import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverH3CocycleInduction

/-!
# CMDG CM5 — scalar H³ primitive on arbitrary profinite fibre quadruples

For every profinite map p:P→T, any globally locally constant
integer fourfold cochain obeying the exact alternating five-point
Čech 3-cocycle identity ON RELATED FIVE-TUPLES admits a
globally locally constant threefold primitive with correct
four-face sign convention.

One finite clopen observation q:P→I of all four coordinates
yields a finite closed family E_i=p(q⁻¹{i}) on T. The
previously proved finite-closed-family H³ theorem supplies
a global triple-index primitive bI on T. Its composition
with the finite observations of triples and p(first coordinate)
is locally constant and satisfies the exact coboundary identity.

Neither a section of p, finiteness of P or T, nor a uniform
product-of-ℤ coefficient observation is assumed. No Ext³,
all-shift derived solidity or source-semantic independence claimed.
-/

noncomputable section
universe u
open CategoryTheory Limits Set TopologicalSpace
namespace CMDG.CondensedCM5R0

theorem integerProfiniteThreeCocycle_ambientQuadruple_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (P × (P × (P × P))) ℤ)
    (hc : ∀ x y z w v : P,
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      p.hom.hom z = p.hom.hom w →
      p.hom.hom w = p.hom.hom v →
      c (y,(z,(w,v))) - c (x,(z,(w,v))) +
        c (x,(y,(w,v))) - c (x,(y,(z,v))) +
        c (x,(y,(z,w))) = 0) :
    ∃ b : LocallyConstant (P × (P × P)) ℤ,
      ∀ x y z w : P,
        p.hom.hom x = p.hom.hom y →
        p.hom.hom y = p.hom.hom z →
        p.hom.hom z = p.hom.hom w →
        c (x,(y,(z,w))) =
          b (y,(z,w)) - b (x,(z,w)) +
            b (x,(y,w)) - b (x,(y,z)) := by
  classical
  obtain ⟨I, fintypeI, q, d, hfact⟩ :=
    integerLocallyConstant_quadrupleProduct_finiteBoxes P c
  letI : Fintype I := fintypeI
  let E : I → Set T :=
    fun i => p.hom.hom '' {x : P | q x = i}
  have hclosed (i : I) : IsClosed (E i) := by
    have hc : IsClosed {x : P | q x = i} :=
      (q.isLocallyConstant.isClopen_fiber i).1
    have hcompact : IsCompact {x : P | q x = i} :=
      hc.isCompact
    exact (hcompact.image p.hom.hom.continuous).isClosed
  let cI : (i j k l : I) →
      LocallyConstant (↥(((E i ∩ E j) ∩ E k) ∩ E l)) ℤ :=
    fun i j k l => LocallyConstant.const _ (d i j k l)
  have hcI : ∀ (i j k l m : I) (t : T)
      (hi : t ∈ E i) (hj : t ∈ E j)
      (hk : t ∈ E k) (hl : t ∈ E l) (hm : t ∈ E m),
      cI j k l m ⟨t, ⟨⟨⟨hj,hk⟩,hl⟩,hm⟩⟩ -
      cI i k l m ⟨t, ⟨⟨⟨hi,hk⟩,hl⟩,hm⟩⟩ +
      cI i j l m ⟨t, ⟨⟨⟨hi,hj⟩,hl⟩,hm⟩⟩ -
      cI i j k m ⟨t, ⟨⟨⟨hi,hj⟩,hk⟩,hm⟩⟩ +
      cI i j k l ⟨t, ⟨⟨⟨hi,hj⟩,hk⟩,hl⟩⟩ = 0 := by
    intro i j k l m t hi hj hk hl hm
    obtain ⟨xi, hxi, hpxi⟩ := hi
    obtain ⟨xj, hxj, hpxj⟩ := hj
    obtain ⟨xk, hxk, hpxk⟩ := hk
    obtain ⟨xl, hxl, hpxl⟩ := hl
    obtain ⟨xm, hxm, hpxm⟩ := hm
    change q xi = i at hxi
    change q xj = j at hxj
    change q xk = k at hxk
    change q xl = l at hxl
    change q xm = m at hxm
    have hxy : p.hom.hom xi = p.hom.hom xj :=
      hpxi.trans hpxj.symm
    have hyz : p.hom.hom xj = p.hom.hom xk :=
      hpxj.trans hpxk.symm
    have hzw : p.hom.hom xk = p.hom.hom xl :=
      hpxk.trans hpxl.symm
    have hwv : p.hom.hom xl = p.hom.hom xm :=
      hpxl.trans hpxm.symm
    have h := hc xi xj xk xl xm hxy hyz hzw hwv
    rw [hfact xj xk xl xm, hfact xi xk xl xm,
      hfact xi xj xl xm, hfact xi xj xk xm,
      hfact xi xj xk xl] at h
    change d j k l m - d i k l m + d i j l m -
      d i j k m + d i j k l = 0
    simpa [hxi, hxj, hxk, hxl, hxm] using h
  obtain ⟨bI, hbI⟩ :=
    integerFiniteClosedFamily_threeCocycle_is_coboundary
      T E hclosed cI hcI
  let g : P × (P × P) → ℤ := fun xyz =>
    bI (q xyz.1) (q xyz.2.1) (q xyz.2.2)
      (p.hom.hom xyz.1)
  have hg : IsLocallyConstant g := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro n
    have hfiber : g ⁻¹' {n} =
        ⋃ i : I, ⋃ j : I, ⋃ k : I,
          (({xyz : P × (P × P) | q xyz.1 = i} ∩
            {xyz : P × (P × P) | q xyz.2.1 = j}) ∩
            {xyz : P × (P × P) | q xyz.2.2 = k}) ∩
          {xyz : P × (P × P) |
            bI i j k (p.hom.hom xyz.1) = n} := by
      ext xyz
      simp only [Set.mem_preimage, Set.mem_singleton_iff,
        Set.mem_iUnion, Set.mem_inter_iff, Set.mem_setOf_eq]
      constructor
      · intro h
        exact ⟨q xyz.1, q xyz.2.1, q xyz.2.2,
          ⟨⟨rfl,rfl⟩,rfl⟩, h⟩
      · rintro ⟨i,j,k,⟨⟨hi,hj⟩,hk⟩,h⟩
        simpa only [g,hi,hj,hk] using h
    rw [hfiber]
    apply isOpen_iUnion
    intro i
    apply isOpen_iUnion
    intro j
    apply isOpen_iUnion
    intro k
    have hq1 : IsOpen {xyz : P × (P × P) | q xyz.1 = i} :=
      (q.isLocallyConstant.isOpen_fiber i).preimage continuous_fst
    have hq2 : IsOpen {xyz : P × (P × P) | q xyz.2.1 = j} :=
      (q.isLocallyConstant.isOpen_fiber j).preimage
        (continuous_fst.comp continuous_snd)
    have hq3 : IsOpen {xyz : P × (P × P) | q xyz.2.2 = k} :=
      (q.isLocallyConstant.isOpen_fiber k).preimage
        (continuous_snd.comp continuous_snd)
    have hbijk : IsOpen {xyz : P × (P × P) |
        bI i j k (p.hom.hom xyz.1) = n} :=
      ((bI i j k).isLocallyConstant.isOpen_fiber n).preimage
        (p.hom.hom.continuous.comp continuous_fst)
    exact ((hq1.inter hq2).inter hq3).inter hbijk
  let b : LocallyConstant (P × (P × P)) ℤ := ⟨g,hg⟩
  refine ⟨b, ?_⟩
  intro x y z w hxy hyz hzw
  have hxE : p.hom.hom x ∈ E (q x) :=
    ⟨x,rfl,rfl⟩
  have hyE : p.hom.hom x ∈ E (q y) :=
    ⟨y,rfl,hxy.symm⟩
  have hzE : p.hom.hom x ∈ E (q z) :=
    ⟨z,rfl,(hxy.trans hyz).symm⟩
  have hwE : p.hom.hom x ∈ E (q w) :=
    ⟨w,rfl,(hxy.trans hyz |>.trans hzw).symm⟩
  have h := hbI (q x) (q y) (q z) (q w)
    (p.hom.hom x) hxE hyE hzE hwE
  change d (q x) (q y) (q z) (q w) =
    bI (q y) (q z) (q w) (p.hom.hom x) -
    bI (q x) (q z) (q w) (p.hom.hom x) +
    bI (q x) (q y) (q w) (p.hom.hom x) -
    bI (q x) (q y) (q z) (p.hom.hom x) at h
  rw [hfact x y z w]
  change d (q x) (q y) (q z) (q w) =
    bI (q y) (q z) (q w) (p.hom.hom y) -
    bI (q x) (q z) (q w) (p.hom.hom x) +
    bI (q x) (q y) (q w) (p.hom.hom x) -
    bI (q x) (q y) (q z) (p.hom.hom x)
  rw [← hxy]
  exact h

#print axioms integerProfiniteThreeCocycle_ambientQuadruple_potential
end CMDG.CondensedCM5R0
