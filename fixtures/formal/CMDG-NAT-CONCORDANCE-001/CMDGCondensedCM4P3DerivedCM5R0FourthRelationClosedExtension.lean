import CMDGCondensedCM4P3DerivedCM5R0ScalarCechH2ClosedRelation

/-!
# CMDG CM5 — the actual closed fourfold Čech relation

For arbitrary profinite p:P→T, the fourfold equal-image relation
{(x,y,z,w) | p(x)=p(y)=p(z)=p(w)} is a closed subspace of P⁴.
Every integer-valued locally constant cochain on that relation extends
to a globally locally constant function on P⁴. No section of p is
selected. This establishes a source-domain and extension ingredient
for the future scalar degree-three Čech acyclicity proof, but it does
not assert that the resulting cocycle is a coboundary or Ext³ vanishes.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

def profiniteCechFourthRelatedSet
    (P T : Profinite.{u}) (p : P ⟶ T) :
    Set (P × (P × (P × P))) :=
  {xyzw | p.hom.hom xyzw.1 = p.hom.hom xyzw.2.1 ∧
    p.hom.hom xyzw.2.1 = p.hom.hom xyzw.2.2.1 ∧
    p.hom.hom xyzw.2.2.1 = p.hom.hom xyzw.2.2.2}

theorem profiniteCechFourthRelatedSet_isClosed
    (P T : Profinite.{u}) (p : P ⟶ T) :
    IsClosed (profiniteCechFourthRelatedSet P T p) := by
  have hx : Continuous
      (fun q : P × (P × (P × P)) => p.hom.hom q.1) :=
    p.hom.hom.continuous.comp continuous_fst
  have hy : Continuous
      (fun q : P × (P × (P × P)) => p.hom.hom q.2.1) :=
    p.hom.hom.continuous.comp (continuous_fst.comp continuous_snd)
  have hz : Continuous
      (fun q : P × (P × (P × P)) => p.hom.hom q.2.2.1) :=
    p.hom.hom.continuous.comp
      (continuous_fst.comp (continuous_snd.comp continuous_snd))
  have hw : Continuous
      (fun q : P × (P × (P × P)) => p.hom.hom q.2.2.2) :=
    p.hom.hom.continuous.comp
      (continuous_snd.comp (continuous_snd.comp continuous_snd))
  simpa only [profiniteCechFourthRelatedSet, Set.setOf_and] using
    (isClosed_eq hx hy).inter
      ((isClosed_eq hy hz).inter (isClosed_eq hz hw))

/-- Every locally constant integer cochain on the ACTUAL closed
fourfold Čech relation extends to a locally constant ambient
fourfold-product cochain, without assuming any section of p. -/
theorem integerCechFourthRelated_locallyConstant_extends
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (↥(profiniteCechFourthRelatedSet P T p)) ℤ) :
    ∃ C : LocallyConstant (P × (P × (P × P))) ℤ,
      ∀ z : ↥(profiniteCechFourthRelatedSet P T p),
        C z.val = c z := by
  let Q : Profinite.{u} := Profinite.of (P × (P × (P × P)))
  exact locallyConstant_extend_closed_subset Q
    (profiniteCechFourthRelatedSet P T p)
    (profiniteCechFourthRelatedSet_isClosed P T p) c

#print axioms profiniteCechFourthRelatedSet_isClosed
#print axioms integerCechFourthRelated_locallyConstant_extends
end CMDG.CondensedCM5R0
