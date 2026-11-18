import CMDGCondensedCM4P3DerivedCM5R0FourthRelationClosedExtension

/-!
# CMDG CM5 — all finite Čech arities have closed relation spaces

For any finite degree n, and any profinite morphism p:P→T, the
(n+1)-tuple space of points sharing the same p-image is closed in
P^(n+1). This remains true for arbitrary (including infinite)
profinite P,T; only the tuple arity is finite. A locally constant
integer cochain on that exact closed tuple relation extends to a
locally constant function on the entire ambient tuple product.

This avoids one new extension proof per Čech degree and applies to
all future higher-relation constructions. It does not prove any
cohomological vanishing, contracting homotopy, or Ext³+ theorem.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

def profiniteCechArityRelatedSet
    (n : ℕ) (P T : Profinite.{u}) (p : P ⟶ T) :
    Set (Fin (n + 1) → P) :=
  {xs | ∀ i : Fin (n + 1),
    p.hom.hom (xs i) = p.hom.hom (xs 0)}

theorem profiniteCechArityRelatedSet_isClosed
    (n : ℕ) (P T : Profinite.{u}) (p : P ⟶ T) :
    IsClosed (profiniteCechArityRelatedSet n P T p) := by
  have hi (i : Fin (n+1)) :
      IsClosed {xs : Fin (n+1) → P |
        p.hom.hom (xs i) = p.hom.hom (xs 0)} := by
    exact isClosed_eq
      (p.hom.hom.continuous.comp (continuous_apply i))
      (p.hom.hom.continuous.comp (continuous_apply 0))
  have h : IsClosed (⋂ i : Fin (n+1),
      {xs : Fin (n+1) → P |
        p.hom.hom (xs i) = p.hom.hom (xs 0)}) :=
    isClosed_iInter hi
  simpa only [profiniteCechArityRelatedSet, Set.setOf_forall] using h

theorem integerCechArityRelated_locallyConstant_extends
    (n : ℕ) (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (↥(profiniteCechArityRelatedSet n P T p)) ℤ) :
    ∃ C : LocallyConstant (Fin (n + 1) → P) ℤ,
      ∀ z : ↥(profiniteCechArityRelatedSet n P T p),
        C z.val = c z := by
  let Q : Profinite.{u} := Profinite.of (Fin (n + 1) → P)
  exact locallyConstant_extend_closed_subset Q
    (profiniteCechArityRelatedSet n P T p)
    (profiniteCechArityRelatedSet_isClosed n P T p) c

#print axioms profiniteCechArityRelatedSet_isClosed
#print axioms integerCechArityRelated_locallyConstant_extends
end CMDG.CondensedCM5R0
