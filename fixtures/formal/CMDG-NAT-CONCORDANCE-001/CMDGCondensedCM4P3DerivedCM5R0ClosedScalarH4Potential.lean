import CMDGCondensedCM4P3DerivedCM5R0ProfiniteScalarH4AmbientPotential
import CMDGCondensedCM4P3DerivedCM5R0GenuineFifthCechBoundary

/-!
# CM5: closed genuine fivefold Čech scalar H⁴ and families

Every locally constant integral 4-cocycle on the true closed fivefold
equal-fibre relation admits a fourfold relation primitive; works for
arbitrary infinite coordinate-index families without common finite
observation. No categorical Ext⁴ conclusion is asserted here.
-/

noncomputable section
universe u v
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem integerProfiniteFourCocycle_closedQuintuple_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (↥(profiniteCechQuintupleRelatedSet P T p)) ℤ)
    (hc : ∀ (x y z w v a : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v)
      (hva : p.hom.hom v = p.hom.hom a),
      c ⟨(y,(z,(w,(v,a)))),⟨hyz,hzw,hwv,hva⟩⟩ -
      c ⟨(x,(z,(w,(v,a)))),⟨hxy.trans hyz,hzw,hwv,hva⟩⟩ +
      c ⟨(x,(y,(w,(v,a)))),⟨hxy,hyz.trans hzw,hwv,hva⟩⟩ -
      c ⟨(x,(y,(z,(v,a)))),⟨hxy,hyz,hzw.trans hwv,hva⟩⟩ +
      c ⟨(x,(y,(z,(w,a)))),⟨hxy,hyz,hzw,hwv.trans hva⟩⟩ -
      c ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ = 0) :
    ∃ b : LocallyConstant (↥(profiniteCechQuadrupleRelatedSet P T p)) ℤ,
      ∀ (x y z w v : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w)
        (hwv : p.hom.hom w = p.hom.hom v),
      c ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ =
        b ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩ -
        b ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩ +
        b ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩ -
        b ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩ +
        b ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ := by
  let Q : Profinite.{u} := Profinite.of (P × (P × (P × (P × P))))
  obtain ⟨C,hC⟩ :=
    locallyConstant_extend_closed_subset Q
      (profiniteCechQuintupleRelatedSet P T p)
      (profiniteCechQuintupleRelatedSet_isClosed P T p) c
  have hc' : ∀ x y z w v a : P,
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      p.hom.hom z = p.hom.hom w →
      p.hom.hom w = p.hom.hom v →
      p.hom.hom v = p.hom.hom a →
      C (y,(z,(w,(v,a)))) - C (x,(z,(w,(v,a)))) +
        C (x,(y,(w,(v,a)))) - C (x,(y,(z,(v,a)))) +
        C (x,(y,(z,(w,a)))) - C (x,(y,(z,(w,v)))) = 0 := by
    intro x y z w v a hxy hyz hzw hwv hva
    rw [hC ⟨(y,(z,(w,(v,a)))),⟨hyz,hzw,hwv,hva⟩⟩,
      hC ⟨(x,(z,(w,(v,a)))),⟨hxy.trans hyz,hzw,hwv,hva⟩⟩,
      hC ⟨(x,(y,(w,(v,a)))),⟨hxy,hyz.trans hzw,hwv,hva⟩⟩,
      hC ⟨(x,(y,(z,(v,a)))),⟨hxy,hyz,hzw.trans hwv,hva⟩⟩,
      hC ⟨(x,(y,(z,(w,a)))),⟨hxy,hyz,hzw,hwv.trans hva⟩⟩,
      hC ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩]
    exact hc x y z w v a hxy hyz hzw hwv hva
  obtain ⟨B,hB⟩ :=
    integerProfiniteFourCocycle_ambientQuintuple_potential
      P T p C hc'
  let b : LocallyConstant
      (↥(profiniteCechQuadrupleRelatedSet P T p)) ℤ :=
    B.comap ⟨fun z => z.val, continuous_subtype_val⟩
  refine ⟨b, ?_⟩
  intro x y z w v hxy hyz hzw hwv
  change c ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ =
    B (y,(z,(w,v))) - B (x,(z,(w,v))) +
    B (x,(y,(w,v))) - B (x,(y,(z,v))) +
    B (x,(y,(z,w)))
  rw [← hC ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩]
  exact hB x y z w v hxy hyz hzw hwv

/-- Coordinatewise primitive for arbitrary, including infinite, families
of locally constant integer H4 cocycles on the genuine closed
fivefold relation. No common finite observation required. -/
theorem integerProfiniteFourCocycle_closedQuintuple_family_hasPotential
    (P T : Profinite.{u}) (p : P ⟶ T) {ι : Type v}
    (c : ι → LocallyConstant
      (↥(profiniteCechQuintupleRelatedSet P T p)) ℤ)
    (hc : ∀ (i : ι) (x y z w v a : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v)
      (hva : p.hom.hom v = p.hom.hom a),
      c i ⟨(y,(z,(w,(v,a)))),⟨hyz,hzw,hwv,hva⟩⟩ -
      c i ⟨(x,(z,(w,(v,a)))),⟨hxy.trans hyz,hzw,hwv,hva⟩⟩ +
      c i ⟨(x,(y,(w,(v,a)))),⟨hxy,hyz.trans hzw,hwv,hva⟩⟩ -
      c i ⟨(x,(y,(z,(v,a)))),⟨hxy,hyz,hzw.trans hwv,hva⟩⟩ +
      c i ⟨(x,(y,(z,(w,a)))),⟨hxy,hyz,hzw,hwv.trans hva⟩⟩ -
      c i ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ = 0) :
    ∃ b : ι → LocallyConstant
      (↥(profiniteCechQuadrupleRelatedSet P T p)) ℤ,
      ∀ (i : ι) (x y z w v : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w)
        (hwv : p.hom.hom w = p.hom.hom v),
      c i ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ =
        b i ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩ -
        b i ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩ +
        b i ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩ -
        b i ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩ +
        b i ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ := by
  classical
  have h (i : ι) : ∃ b : LocallyConstant
      (↥(profiniteCechQuadrupleRelatedSet P T p)) ℤ,
      ∀ (x y z w v : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w)
        (hwv : p.hom.hom w = p.hom.hom v),
      c i ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ =
        b ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩ -
        b ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩ +
        b ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩ -
        b ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩ +
        b ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ :=
    integerProfiniteFourCocycle_closedQuintuple_potential
      P T p (c i) (hc i)
  choose b hb using h
  exact ⟨b,hb⟩

#print axioms integerProfiniteFourCocycle_closedQuintuple_family_hasPotential
#print axioms integerProfiniteFourCocycle_closedQuintuple_potential
end CMDG.CondensedCM5R0
