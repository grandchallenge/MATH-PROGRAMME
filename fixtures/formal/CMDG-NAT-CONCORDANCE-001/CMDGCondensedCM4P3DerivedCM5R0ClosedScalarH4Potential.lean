import CMDGCondensedCM4P3DerivedCM5R0ProfiniteScalarH4AmbientPotential
import CMDGCondensedCM4P3DerivedCM5R0GenuineFifthCechBoundary

/-!
# CM5 Ext⁴ — genuine closed quintuple-fibre scalar H⁴ acyclicity

For arbitrary profinite p:P→T, an integer locally constant
four-cocycle on the *closed equal-image fivefold relation*
admits a locally constant fourfold-relation primitive.
No section of p, compact finite surrogate or degree-4 Ext
vanishing is assumed.

By coordinatewise classical choice, arbitrary (possibly infinite)
families have such primitives without a common finite observation.
-/

noncomputable section
universe u v
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem integerProfiniteFourCocycle_closedQuintuple_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant
      (↥(profiniteCechQuintupleRelatedSet P T p)) ℤ)
    (hc : ∀ (x y z w v r : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v)
      (hvr : p.hom.hom v = p.hom.hom r),
        c ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩ -
        c ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩ +
        c ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩ -
        c ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩ +
        c ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩ -
        c ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ = 0) :
    ∃ b : LocallyConstant
        (↥(profiniteCechQuadrupleRelatedSet P T p)) ℤ,
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
  let Q : Profinite.{u} :=
    Profinite.of (P × (P × (P × (P × P))))
  obtain ⟨C,hC⟩ := locallyConstant_extend_closed_subset Q
      (profiniteCechQuintupleRelatedSet P T p)
      (profiniteCechQuintupleRelatedSet_isClosed P T p) c
  have hc' : ∀ (x y z w v r : P),
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      p.hom.hom z = p.hom.hom w →
      p.hom.hom w = p.hom.hom v →
      p.hom.hom v = p.hom.hom r →
      C (y,(z,(w,(v,r)))) - C (x,(z,(w,(v,r)))) +
        C (x,(y,(w,(v,r)))) - C (x,(y,(z,(v,r)))) +
          C (x,(y,(z,(w,r)))) - C (x,(y,(z,(w,v)))) = 0 := by
    intro x y z w v r hxy hyz hzw hwv hvr
    rw [hC ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩,
      hC ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩,
      hC ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩,
      hC ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩,
      hC ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩,
      hC ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩]
    exact hc x y z w v r hxy hyz hzw hwv hvr
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

/-- Independent scalar primitives in every coordinate of an arbitrary
(including infinite) coefficient-index family. The finite observation
may depend on the coordinate: NO common finite quotient is assumed. -/
theorem integerProfiniteFourCocycle_closedQuintuple_family_hasPotential
    (P T : Profinite.{u}) (p : P ⟶ T) {ι : Type v}
    (c : ι → LocallyConstant
      (↥(profiniteCechQuintupleRelatedSet P T p)) ℤ)
    (hc : ∀ (i : ι) (x y z w v r : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v)
      (hvr : p.hom.hom v = p.hom.hom r),
        c i ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩ -
        c i ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩ +
        c i ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩ -
        c i ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩ +
        c i ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩ -
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
