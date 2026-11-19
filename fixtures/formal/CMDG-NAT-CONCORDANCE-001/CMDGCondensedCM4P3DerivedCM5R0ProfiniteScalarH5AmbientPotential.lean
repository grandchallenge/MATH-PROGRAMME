import CMDGCondensedCM4P3DerivedCM5R0SextupleFiniteBoxes
import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedH5Restriction

/-! CM5: true arbitrary-profinite scalar H5 on ambient sixfold products.
The single finite observation supplies a finite family of closed
image fibres in the arbitrary profinite base. The proven finite-family
H5 theorem constructs the primitive; no section of p is assumed. -/

noncomputable section
universe u
open CategoryTheory Limits Set TopologicalSpace
namespace CMDG.CondensedCM5R0

theorem integerProfiniteFiveCocycle_ambientSextuple_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (P × (P × (P × (P × (P × P))))) ℤ)
    (hc : ∀ x y z w v r s : P,
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      p.hom.hom z = p.hom.hom w →
      p.hom.hom w = p.hom.hom v →
      p.hom.hom v = p.hom.hom r →
      p.hom.hom r = p.hom.hom s →
      c (y,(z,(w,(v,(r,s))))) - c (x,(z,(w,(v,(r,s))))) + c (x,(y,(w,(v,(r,s))))) - c (x,(y,(z,(v,(r,s))))) + c (x,(y,(z,(w,(r,s))))) - c (x,(y,(z,(w,(v,s))))) + c (x,(y,(z,(w,(v,r))))) = 0) :
    ∃ b : LocallyConstant (P × (P × (P × (P × P)))) ℤ,
      ∀ x y z w v r : P,
        p.hom.hom x = p.hom.hom y →
        p.hom.hom y = p.hom.hom z →
        p.hom.hom z = p.hom.hom w →
        p.hom.hom w = p.hom.hom v →
        p.hom.hom v = p.hom.hom r →
        c (x,(y,(z,(w,(v,r))))) =
          b (y,(z,(w,(v,r)))) - b (x,(z,(w,(v,r)))) + b (x,(y,(w,(v,r)))) - b (x,(y,(z,(v,r)))) + b (x,(y,(z,(w,r)))) - b (x,(y,(z,(w,v)))) := by
  classical
  obtain ⟨I,fintypeI,q,d,hfact⟩ :=
    integerLocallyConstant_sextupleProduct_finiteBoxes P c
  letI : Fintype I := fintypeI
  let E : I → Set T := fun i => p.hom.hom '' {x : P | q x = i}
  have hclosed (i : I) : IsClosed (E i) := by
    have hc : IsClosed {x : P | q x = i} :=
      (q.isLocallyConstant.isClopen_fiber i).1
    have hcompact : IsCompact {x : P | q x = i} := hc.isCompact
    exact (hcompact.image p.hom.hom.continuous).isClosed
  let cI : (i j k l m n : I) →
      LocallyConstant
        (↥((((((E i ∩ E j) ∩ E k) ∩ E l) ∩ E m) ∩ E n))) ℤ :=
    fun i j k l m n => LocallyConstant.const _ (d i j k l m n)
  have hcI : ∀ (i j k l m n o : I) (t : T)
      (hi : t ∈ E i) (hj : t ∈ E j)
      (hk : t ∈ E k) (hl : t ∈ E l)
      (hm : t ∈ E m) (hn : t ∈ E n)
      (ho : t ∈ E o),
      cI j k l m n o ⟨t,⟨⟨⟨⟨⟨hj,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩ - cI i k l m n o ⟨t,⟨⟨⟨⟨⟨hi,hk⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩ + cI i j l m n o ⟨t,⟨⟨⟨⟨⟨hi,hj⟩,hl⟩,hm⟩,hn⟩,ho⟩⟩ - cI i j k m n o ⟨t,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hm⟩,hn⟩,ho⟩⟩ + cI i j k l n o ⟨t,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hn⟩,ho⟩⟩ - cI i j k l m o ⟨t,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,ho⟩⟩ + cI i j k l m n ⟨t,⟨⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,hn⟩⟩ = 0 := by
    intro i j k l m n o t hi hj hk hl hm hn ho
    obtain ⟨xi, hxi, hpxi⟩ := hi
    obtain ⟨xj, hxj, hpxj⟩ := hj
    obtain ⟨xk, hxk, hpxk⟩ := hk
    obtain ⟨xl, hxl, hpxl⟩ := hl
    obtain ⟨xm, hxm, hpxm⟩ := hm
    obtain ⟨xn, hxn, hpxn⟩ := hn
    obtain ⟨xo, hxo, hpxo⟩ := ho
    change q xi = i at hxi
    change q xj = j at hxj
    change q xk = k at hxk
    change q xl = l at hxl
    change q xm = m at hxm
    change q xn = n at hxn
    change q xo = o at hxo
    have hxy : p.hom.hom xi = p.hom.hom xj :=
      hpxi.trans hpxj.symm
    have hyz : p.hom.hom xj = p.hom.hom xk :=
      hpxj.trans hpxk.symm
    have hzw : p.hom.hom xk = p.hom.hom xl :=
      hpxk.trans hpxl.symm
    have hwv : p.hom.hom xl = p.hom.hom xm :=
      hpxl.trans hpxm.symm
    have hvr : p.hom.hom xm = p.hom.hom xn :=
      hpxm.trans hpxn.symm
    have hrs : p.hom.hom xn = p.hom.hom xo :=
      hpxn.trans hpxo.symm
    have h := hc xi xj xk xl xm xn xo hxy hyz hzw hwv hvr hrs
    rw [hfact xj xk xl xm xn xo, hfact xi xk xl xm xn xo, hfact xi xj xl xm xn xo, hfact xi xj xk xm xn xo, hfact xi xj xk xl xn xo, hfact xi xj xk xl xm xo, hfact xi xj xk xl xm xn] at h
    change d j k l m n o - d i k l m n o + d i j l m n o - d i j k m n o + d i j k l n o - d i j k l m o + d i j k l m n = 0
    simpa [hxi,hxj,hxk,hxl,hxm,hxn,hxo] using h
  obtain ⟨bI,hbI⟩ :=
    integerFiniteClosedFamily_fiveCocycle_is_coboundary
      T E hclosed cI hcI
  let g : P × (P × (P × (P × P))) → ℤ := fun t =>
    bI (q t.1) (q t.2.1) (q t.2.2.1)
      (q t.2.2.2.1) (q t.2.2.2.2)
      (p.hom.hom t.1)
  have hg : IsLocallyConstant g := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro N
    have hfiber : g ⁻¹' {N} =
      ⋃ i : I, ⋃ j : I, ⋃ k : I, ⋃ l : I, ⋃ m : I,
        (((({t : P × (P × (P × (P × P))) | q t.1 = i} ∩
          {t : P × (P × (P × (P × P))) | q t.2.1 = j}) ∩
          {t : P × (P × (P × (P × P))) | q t.2.2.1 = k}) ∩
          {t : P × (P × (P × (P × P))) | q t.2.2.2.1 = l}) ∩
          {t : P × (P × (P × (P × P))) | q t.2.2.2.2 = m}) ∩
        {t : P × (P × (P × (P × P))) |
          bI i j k l m (p.hom.hom t.1) = N} := by
      ext t
      simp only [Set.mem_preimage, Set.mem_singleton_iff,
        Set.mem_iUnion, Set.mem_inter_iff, Set.mem_setOf_eq]
      constructor
      · intro h
        exact ⟨q t.1, q t.2.1, q t.2.2.1,
          q t.2.2.2.1, q t.2.2.2.2,
          ⟨⟨⟨⟨rfl,rfl⟩,rfl⟩,rfl⟩,rfl⟩,h⟩
      · rintro ⟨i,j,k,l,m,⟨⟨⟨⟨hi,hj⟩,hk⟩,hl⟩,hm⟩,h⟩
        simpa only [g,hi,hj,hk,hl,hm] using h
    rw [hfiber]
    apply isOpen_iUnion
    intro i
    apply isOpen_iUnion
    intro j
    apply isOpen_iUnion
    intro k
    apply isOpen_iUnion
    intro l
    apply isOpen_iUnion
    intro m
    have hq1 : IsOpen {t : P × (P × (P × (P × P))) |
      q t.1 = i} :=
      (q.isLocallyConstant.isOpen_fiber i).preimage continuous_fst
    have hq2 : IsOpen {t : P × (P × (P × (P × P))) |
      q t.2.1 = j} :=
      (q.isLocallyConstant.isOpen_fiber j).preimage
        (continuous_fst.comp continuous_snd)
    have hq3 : IsOpen {t : P × (P × (P × (P × P))) |
      q t.2.2.1 = k} :=
      (q.isLocallyConstant.isOpen_fiber k).preimage
        (continuous_fst.comp (continuous_snd.comp continuous_snd))
    have hq4 : IsOpen {t : P × (P × (P × (P × P))) |
      q t.2.2.2.1 = l} :=
      (q.isLocallyConstant.isOpen_fiber l).preimage
        (continuous_fst.comp
          (continuous_snd.comp (continuous_snd.comp continuous_snd)))
    have hq5 : IsOpen {t : P × (P × (P × (P × P))) |
      q t.2.2.2.2 = m} :=
      (q.isLocallyConstant.isOpen_fiber m).preimage
        (continuous_snd.comp
          (continuous_snd.comp (continuous_snd.comp continuous_snd)))
    have hbijklm : IsOpen {t : P × (P × (P × (P × P))) |
      bI i j k l m (p.hom.hom t.1) = N} :=
      ((bI i j k l m).isLocallyConstant.isOpen_fiber N).preimage
        (p.hom.hom.continuous.comp continuous_fst)
    exact ((((hq1.inter hq2).inter hq3).inter hq4).inter hq5).inter hbijklm
  let b : LocallyConstant (P × (P × (P × (P × P)))) ℤ := ⟨g,hg⟩
  refine ⟨b, ?_⟩
  intro x y z w v r hxy hyz hzw hwv hvr
  have hxE : p.hom.hom x ∈ E (q x) := ⟨x,rfl,rfl⟩
  have hyE : p.hom.hom x ∈ E (q y) := ⟨y,rfl,hxy.symm⟩
  have hzE : p.hom.hom x ∈ E (q z) :=
    ⟨z,rfl,(hxy.trans hyz).symm⟩
  have hwE : p.hom.hom x ∈ E (q w) :=
    ⟨w,rfl,((hxy.trans hyz).trans hzw).symm⟩
  have hvE : p.hom.hom x ∈ E (q v) :=
    ⟨v,rfl,(((hxy.trans hyz).trans hzw).trans hwv).symm⟩
  have hrE : p.hom.hom x ∈ E (q r) :=
    ⟨r,rfl,((((hxy.trans hyz).trans hzw).trans hwv).trans hvr).symm⟩
  have h := hbI (q x) (q y) (q z) (q w) (q v) (q r)
    (p.hom.hom x) hxE hyE hzE hwE hvE hrE
  change d (q x) (q y) (q z) (q w) (q v) (q r) =
    bI (q y) (q z) (q w) (q v) (q r) (p.hom.hom x) -
    bI (q x) (q z) (q w) (q v) (q r) (p.hom.hom x) +
    bI (q x) (q y) (q w) (q v) (q r) (p.hom.hom x) -
    bI (q x) (q y) (q z) (q v) (q r) (p.hom.hom x) +
    bI (q x) (q y) (q z) (q w) (q r) (p.hom.hom x) -
    bI (q x) (q y) (q z) (q w) (q v) (p.hom.hom x) at h
  rw [hfact x y z w v r]
  change d (q x) (q y) (q z) (q w) (q v) (q r) =
    bI (q y) (q z) (q w) (q v) (q r) (p.hom.hom y) -
    bI (q x) (q z) (q w) (q v) (q r) (p.hom.hom x) +
    bI (q x) (q y) (q w) (q v) (q r) (p.hom.hom x) -
    bI (q x) (q y) (q z) (q v) (q r) (p.hom.hom x) +
    bI (q x) (q y) (q z) (q w) (q r) (p.hom.hom x) -
    bI (q x) (q y) (q z) (q w) (q v) (p.hom.hom x)
  rw [← hxy]
  exact h

#print axioms integerProfiniteFiveCocycle_ambientSextuple_potential
end CMDG.CondensedCM5R0
