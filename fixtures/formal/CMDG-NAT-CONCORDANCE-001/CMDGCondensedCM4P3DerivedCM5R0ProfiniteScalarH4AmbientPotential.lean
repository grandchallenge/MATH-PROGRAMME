import CMDGCondensedCM4P3DerivedCM5R0QuintupleFiniteBoxes
import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverH4CocycleInduction

/-!
# CM5: arbitrary profinite scalar H⁴

Every locally constant integer cochain on P^5 satisfying the exact
six-face fibrewise 4-cocycle law has a globally locally constant
four-vertex primitive. The source map p:P→T is arbitrary between
profinite spaces; no section, injectivity, finite spaces, or discrete
product-uniform-finiteness assumption.
-/
noncomputable section
universe u
open CategoryTheory Limits Set TopologicalSpace
namespace CMDG.CondensedCM5R0

theorem integerProfiniteFourCocycle_ambientQuintuple_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (P × (P × (P × (P × P)))) ℤ)
    (hc : ∀ x y z w v a : P,
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      p.hom.hom z = p.hom.hom w →
      p.hom.hom w = p.hom.hom v →
      p.hom.hom v = p.hom.hom a →
      c (y,(z,(w,(v,a)))) - c (x,(z,(w,(v,a)))) +
        c (x,(y,(w,(v,a)))) - c (x,(y,(z,(v,a)))) +
        c (x,(y,(z,(w,a)))) - c (x,(y,(z,(w,v)))) = 0) :
    ∃ b : LocallyConstant (P × (P × (P × P))) ℤ,
      ∀ x y z w v : P,
        p.hom.hom x = p.hom.hom y →
        p.hom.hom y = p.hom.hom z →
        p.hom.hom z = p.hom.hom w →
        p.hom.hom w = p.hom.hom v →
        c (x,(y,(z,(w,v)))) =
          b (y,(z,(w,v))) - b (x,(z,(w,v))) +
            b (x,(y,(w,v))) - b (x,(y,(z,v))) +
            b (x,(y,(z,w))) := by
  classical
  obtain ⟨I, fintypeI, q, d, hfact⟩ :=
    integerLocallyConstant_quintupleProduct_finiteBoxes P c
  letI : Fintype I := fintypeI
  let E : I → Set T := fun i => p.hom.hom '' {x : P | q x = i}
  have hclosed (i : I) : IsClosed (E i) := by
    have hc : IsClosed {x : P | q x = i} :=
      (q.isLocallyConstant.isClopen_fiber i).1
    have hcompact : IsCompact {x : P | q x = i} := hc.isCompact
    exact (hcompact.image p.hom.hom.continuous).isClosed
  let cI : (i j k l m : I) →
      LocallyConstant (↥((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m)) ℤ :=
    fun i j k l m => LocallyConstant.const _ (d i j k l m)
  have hcI : ∀ (i j k l m n : I) (t : T)
      (hi : t ∈ E i) (hj : t ∈ E j)
      (hk : t ∈ E k) (hl : t ∈ E l)
      (hm : t ∈ E m) (hn : t ∈ E n),
      cI j k l m n ⟨t, ⟨⟨⟨⟨hj,hk⟩,hl⟩,hm⟩,hn⟩⟩ -
      cI i k l m n ⟨t, ⟨⟨⟨⟨hi,hk⟩,hl⟩,hm⟩,hn⟩⟩ +
      cI i j l m n ⟨t, ⟨⟨⟨⟨hi,hj⟩,hl⟩,hm⟩,hn⟩⟩ -
      cI i j k m n ⟨t, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hm⟩,hn⟩⟩ +
      cI i j k l n ⟨t, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hn⟩⟩ -
      cI i j k l m ⟨t, ⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩⟩ = 0 := by
    intro i j k l m n t hi hj hk hl hm hn
    obtain ⟨xi, hxi, hpxi⟩ := hi
    obtain ⟨xj, hxj, hpxj⟩ := hj
    obtain ⟨xk, hxk, hpxk⟩ := hk
    obtain ⟨xl, hxl, hpxl⟩ := hl
    obtain ⟨xm, hxm, hpxm⟩ := hm
    obtain ⟨xn, hxn, hpxn⟩ := hn
    change q xi = i at hxi
    change q xj = j at hxj
    change q xk = k at hxk
    change q xl = l at hxl
    change q xm = m at hxm
    change q xn = n at hxn
    have hxy : p.hom.hom xi = p.hom.hom xj := hpxi.trans hpxj.symm
    have hyz : p.hom.hom xj = p.hom.hom xk := hpxj.trans hpxk.symm
    have hzw : p.hom.hom xk = p.hom.hom xl := hpxk.trans hpxl.symm
    have hwv : p.hom.hom xl = p.hom.hom xm := hpxl.trans hpxm.symm
    have hva : p.hom.hom xm = p.hom.hom xn := hpxm.trans hpxn.symm
    have h := hc xi xj xk xl xm xn hxy hyz hzw hwv hva
    rw [hfact xj xk xl xm xn, hfact xi xk xl xm xn,
      hfact xi xj xl xm xn, hfact xi xj xk xm xn,
      hfact xi xj xk xl xn, hfact xi xj xk xl xm] at h
    change d j k l m n - d i k l m n + d i j l m n -
      d i j k m n + d i j k l n - d i j k l m = 0
    simpa [hxi, hxj, hxk, hxl, hxm, hxn] using h
  obtain ⟨bI, hbI⟩ :=
    integerFiniteClosedFamily_fourCocycle_is_coboundary
      T E hclosed cI hcI
  let g : P × (P × (P × P)) → ℤ := fun xyzw =>
    bI (q xyzw.1) (q xyzw.2.1) (q xyzw.2.2.1)
      (q xyzw.2.2.2) (p.hom.hom xyzw.1)
  have hg : IsLocallyConstant g := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro n
    have hfiber : g ⁻¹' {n} =
        ⋃ i : I, ⋃ j : I, ⋃ k : I, ⋃ l : I,
          ((({t : P × (P × (P × P)) | q t.1 = i} ∩
            {t : P × (P × (P × P)) | q t.2.1 = j}) ∩
            {t : P × (P × (P × P)) | q t.2.2.1 = k}) ∩
            {t : P × (P × (P × P)) | q t.2.2.2 = l}) ∩
          {t : P × (P × (P × P)) |
            bI i j k l (p.hom.hom t.1) = n} := by
      ext t
      simp only [Set.mem_preimage, Set.mem_singleton_iff,
        Set.mem_iUnion, Set.mem_inter_iff, Set.mem_setOf_eq]
      constructor
      · intro h
        exact ⟨q t.1, q t.2.1, q t.2.2.1, q t.2.2.2,
          ⟨⟨⟨rfl,rfl⟩,rfl⟩,rfl⟩,h⟩
      · rintro ⟨i,j,k,l,⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,h⟩
        simpa only [g,hi,hj,hk,hl] using h
    rw [hfiber]
    apply isOpen_iUnion
    intro i
    apply isOpen_iUnion
    intro j
    apply isOpen_iUnion
    intro k
    apply isOpen_iUnion
    intro l
    have hq1 : IsOpen {t : P × (P × (P × P)) | q t.1 = i} :=
      (q.isLocallyConstant.isOpen_fiber i).preimage continuous_fst
    have hq2 : IsOpen {t : P × (P × (P × P)) | q t.2.1 = j} :=
      (q.isLocallyConstant.isOpen_fiber j).preimage
        (continuous_fst.comp continuous_snd)
    have hq3 : IsOpen {t : P × (P × (P × P)) | q t.2.2.1 = k} :=
      (q.isLocallyConstant.isOpen_fiber k).preimage
        (continuous_fst.comp (continuous_snd.comp continuous_snd))
    have hq4 : IsOpen {t : P × (P × (P × P)) | q t.2.2.2 = l} :=
      (q.isLocallyConstant.isOpen_fiber l).preimage
        (continuous_snd.comp (continuous_snd.comp continuous_snd))
    have hbijkl : IsOpen {t : P × (P × (P × P)) |
        bI i j k l (p.hom.hom t.1) = n} :=
      ((bI i j k l).isLocallyConstant.isOpen_fiber n).preimage
        (p.hom.hom.continuous.comp continuous_fst)
    exact (((hq1.inter hq2).inter hq3).inter hq4).inter hbijkl
  let b : LocallyConstant (P × (P × (P × P))) ℤ := ⟨g,hg⟩
  refine ⟨b, ?_⟩
  intro x y z w v hxy hyz hzw hwv
  have hxE : p.hom.hom x ∈ E (q x) := ⟨x,rfl,rfl⟩
  have hyE : p.hom.hom x ∈ E (q y) := ⟨y,rfl,hxy.symm⟩
  have hzE : p.hom.hom x ∈ E (q z) :=
    ⟨z,rfl,(hxy.trans hyz).symm⟩
  have hwE : p.hom.hom x ∈ E (q w) :=
    ⟨w,rfl,(hxy.trans hyz |>.trans hzw).symm⟩
  have hvE : p.hom.hom x ∈ E (q v) :=
    ⟨v,rfl,((hxy.trans hyz).trans hzw |>.trans hwv).symm⟩
  have h := hbI (q x) (q y) (q z) (q w) (q v)
    (p.hom.hom x) hxE hyE hzE hwE hvE
  change d (q x) (q y) (q z) (q w) (q v) =
    bI (q y) (q z) (q w) (q v) (p.hom.hom x) -
    bI (q x) (q z) (q w) (q v) (p.hom.hom x) +
    bI (q x) (q y) (q w) (q v) (p.hom.hom x) -
    bI (q x) (q y) (q z) (q v) (p.hom.hom x) +
    bI (q x) (q y) (q z) (q w) (p.hom.hom x) at h
  rw [hfact x y z w v]
  change d (q x) (q y) (q z) (q w) (q v) =
    bI (q y) (q z) (q w) (q v) (p.hom.hom y) -
    bI (q x) (q z) (q w) (q v) (p.hom.hom x) +
    bI (q x) (q y) (q w) (q v) (p.hom.hom x) -
    bI (q x) (q y) (q z) (q v) (p.hom.hom x) +
    bI (q x) (q y) (q z) (q w) (p.hom.hom x)
  rw [← hxy]
  exact h

#print axioms integerProfiniteFourCocycle_ambientQuintuple_potential
end CMDG.CondensedCM5R0
