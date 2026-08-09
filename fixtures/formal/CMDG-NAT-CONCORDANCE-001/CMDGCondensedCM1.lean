import Mathlib.Condensed.Discrete.Basic

/-!
CMDG-CONDENSED-CM1-001 checked adjunction fixture.

This fixture binds an actual `Adjunction` object for the exact pinned Type-valued
condensed model and exposes its induced Hom-equivalence, unit, and counit.

It does not assert full concordance between the pinned no-cardinality-bound mathlib
model and every cardinal-bounded Clausen–Scholze presentation; it does not assert
that `Condensed.discrete` is fully faithful; it does not assert that every condensed
object is discrete; and it does not confer CM2, GRAPH_CERTIFIED, dependency
minimality, or global CMDG completeness.
-/

noncomputable section

open CategoryTheory

universe u

namespace CMDG.CondensedCM1

noncomputable def cm1Discrete : Type (u + 1) ⥤ CondensedSet.{u} :=
  Condensed.discrete (Type (u + 1))

noncomputable def cm1Underlying : CondensedSet.{u} ⥤ Type (u + 1) :=
  Condensed.underlying (Type (u + 1))

noncomputable def cm1Adj :
    cm1Discrete.{u} ⊣ cm1Underlying.{u} :=
  Condensed.discreteUnderlyingAdj (Type (u + 1))

noncomputable def cm1HomEquiv (X : Type (u + 1)) (Y : CondensedSet.{u}) :
    (cm1Discrete.{u}.obj X ⟶ Y) ≃
      (X ⟶ cm1Underlying.{u}.obj Y) :=
  cm1Adj.{u}.homEquiv X Y

noncomputable def cm1Unit (X : Type (u + 1)) :
    X ⟶ cm1Underlying.{u}.obj (cm1Discrete.{u}.obj X) :=
  cm1Adj.{u}.unit.app X

noncomputable def cm1Counit (Y : CondensedSet.{u}) :
    cm1Discrete.{u}.obj (cm1Underlying.{u}.obj Y) ⟶ Y :=
  cm1Adj.{u}.counit.app Y

theorem cm1Discrete_source :
    cm1Discrete.{u} = Condensed.discrete (Type (u + 1)) := rfl

theorem cm1Underlying_source :
    cm1Underlying.{u} = Condensed.underlying (Type (u + 1)) := rfl

theorem cm1Adj_source :
    cm1Adj.{u} = Condensed.discreteUnderlyingAdj (Type (u + 1)) := rfl

end CMDG.CondensedCM1
