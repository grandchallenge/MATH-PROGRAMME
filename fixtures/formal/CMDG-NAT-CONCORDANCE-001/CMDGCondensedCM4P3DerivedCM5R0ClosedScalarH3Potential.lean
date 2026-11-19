import CMDGCondensedCM4P3DerivedCM5R0ProfiniteScalarH3AmbientPotential
import CMDGCondensedCM4P3DerivedCM5R0ClosedQuadrupleScalarExtension

/-!
# CMDG CM5 — closed-relation scalar H³ and arbitrary coefficient families

For any profinite p:P→T, a locally constant integer three-cocycle
on the genuine closed fourfold equal-image relation admits a locally
constant triple cochain primitive with all alternating face signs.
The proof extends across the closed fourfold domain, applies finite
closed-family H³ via finite observation, and restricts to the true
triple relation. No section of p is assumed.

The second theorem works for arbitrary (possibly infinite) indexed
families of cocycles, without requiring a common finite observation.
This is the coordinatewise semantics needed for products of discrete
coefficient sheaves. Neither theorem identifies the genuine free-solid
G_S with such a product or establishes Ext³ vanishing.
-/

noncomputable section
universe u v
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem integerProfiniteThreeCocycle_closedQuadruple_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (↥(profiniteCechQuadrupleRelatedSet P T p)) ℤ)
    (hc : ∀ (x y z w v : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v),
      c ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩ -
      c ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩ +
      c ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩ -
      c ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩ +
      c ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ = 0) :
    ∃ b : LocallyConstant (↥(profiniteCechTripleRelatedSet P T p)) ℤ,
      ∀ (x y z w : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w),
      c ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ =
        b ⟨(y,(z,w)),⟨hyz,hzw⟩⟩ -
        b ⟨(x,(z,w)),⟨hxy.trans hyz,hzw⟩⟩ +
        b ⟨(x,(y,w)),⟨hxy,hyz.trans hzw⟩⟩ -
        b ⟨(x,(y,z)),⟨hxy,hyz⟩⟩ := by
  obtain ⟨C,hC⟩ :=
    integerLocallyConstant_extendCechQuadruple P T p c
  have hc' : ∀ x y z w v : P,
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      p.hom.hom z = p.hom.hom w →
      p.hom.hom w = p.hom.hom v →
      C (y,(z,(w,v))) - C (x,(z,(w,v))) +
        C (x,(y,(w,v))) - C (x,(y,(z,v))) +
        C (x,(y,(z,w))) = 0 := by
    intro x y z w v hxy hyz hzw hwv
    rw [hC ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩,
      hC ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩,
      hC ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩,
      hC ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩,
      hC ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩]
    exact hc x y z w v hxy hyz hzw hwv
  obtain ⟨B,hB⟩ :=
    integerProfiniteThreeCocycle_ambientQuadruple_potential
      P T p C hc'
  let b : LocallyConstant (↥(profiniteCechTripleRelatedSet P T p)) ℤ :=
    B.comap ⟨fun z => z.val, continuous_subtype_val⟩
  refine ⟨b, ?_⟩
  intro x y z w hxy hyz hzw
  change c ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ =
    B (y,(z,w)) - B (x,(z,w)) +
      B (x,(y,w)) - B (x,(y,z))
  rw [← hC ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩]
  exact hB x y z w hxy hyz hzw


/-- Arbitrary, including infinite, families of genuine closed-quadruple
Čech 3-cocycles have coordinatewise locally constant triple primitives.
There is no common finite observation across the coefficient index. -/
theorem integerProfiniteThreeCocycle_closedQuadruple_family_hasPotential
    (P T : Profinite.{u}) (p : P ⟶ T) {ι : Type v}
    (c : ι → LocallyConstant
      (↥(profiniteCechQuadrupleRelatedSet P T p)) ℤ)
    (hc : ∀ (i : ι) (x y z w v : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v),
      c i ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩ -
      c i ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩ +
      c i ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩ -
      c i ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩ +
      c i ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ = 0) :
    ∃ b : ι → LocallyConstant
      (↥(profiniteCechTripleRelatedSet P T p)) ℤ,
      ∀ (i : ι) (x y z w : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w),
      c i ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ =
        b i ⟨(y,(z,w)),⟨hyz,hzw⟩⟩ -
        b i ⟨(x,(z,w)),⟨hxy.trans hyz,hzw⟩⟩ +
        b i ⟨(x,(y,w)),⟨hxy,hyz.trans hzw⟩⟩ -
        b i ⟨(x,(y,z)),⟨hxy,hyz⟩⟩ := by
  classical
  have h (i : ι) : ∃ b : LocallyConstant
      (↥(profiniteCechTripleRelatedSet P T p)) ℤ,
      ∀ (x y z w : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w),
      c i ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ =
        b ⟨(y,(z,w)),⟨hyz,hzw⟩⟩ -
        b ⟨(x,(z,w)),⟨hxy.trans hyz,hzw⟩⟩ +
        b ⟨(x,(y,w)),⟨hxy,hyz.trans hzw⟩⟩ -
        b ⟨(x,(y,z)),⟨hxy,hyz⟩⟩ :=
    integerProfiniteThreeCocycle_closedQuadruple_potential
      P T p (c i) (hc i)
  choose b hb using h
  exact ⟨b, hb⟩

#print axioms integerProfiniteThreeCocycle_closedQuadruple_family_hasPotential
#print axioms integerProfiniteThreeCocycle_closedQuadruple_potential
end CMDG.CondensedCM5R0
