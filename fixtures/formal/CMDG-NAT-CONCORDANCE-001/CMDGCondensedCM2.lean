import Mathlib.Condensed.CartesianClosed

/-!
CMDG-CONDENSED-CM2-001 checked Cartesian-closedness fixture.

This fixture materializes the chosen Cartesian product structure and, for an
arbitrary object `X` of the exact pinned Type-valued condensed model, the
`Closed X` witness, selected right adjoint to `tensorLeft X`, checked
adjunction, Hom-equivalence, unit, and counit/evaluation map.

It does not identify the internal hom with a pointwise function object; it does
not assert that `Condensed.underlying` or `Condensed.discrete` preserves
exponentials; and it does not confer full cardinal-bounded Clausen–Scholze
concordance, CM3, C05/C06 discharge, GRAPH_CERTIFIED, dependency minimality,
or global CMDG completeness.
-/

noncomputable section

open CategoryTheory
open CategoryTheory.Limits
open CategoryTheory.MonoidalCategory
open CategoryTheory.CartesianMonoidalCategory

universe u

namespace CMDG.CondensedCM2

noncomputable def cm2CartesianMonoidal :
    CartesianMonoidalCategory (CondensedSet.{u}) :=
  inferInstance

noncomputable def cm2MonoidalClosed :
    MonoidalClosed (CondensedSet.{u}) :=
  inferInstance

noncomputable def cm2ProductWitness (X Y : CondensedSet.{u}) :
    IsLimit (BinaryFan.mk (fst X Y) (snd X Y)) :=
  tensorProductIsBinaryProduct X Y

noncomputable def cm2Closed (X : CondensedSet.{u}) : Closed X :=
  MonoidalClosed.closed X

noncomputable def cm2TensorLeft (X : CondensedSet.{u}) :
    CondensedSet.{u} ⥤ CondensedSet.{u} :=
  tensorLeft X

noncomputable def cm2RightAdj (X : CondensedSet.{u}) :
    CondensedSet.{u} ⥤ CondensedSet.{u} :=
  (cm2Closed X).rightAdj

noncomputable def cm2Adj (X : CondensedSet.{u}) :
    cm2TensorLeft X ⊣ cm2RightAdj X := by
  change tensorLeft X ⊣ (cm2Closed X).rightAdj
  exact (cm2Closed X).adj

noncomputable def cm2HomEquiv (X Y Z : CondensedSet.{u}) :
    (cm2TensorLeft X |>.obj Y ⟶ Z) ≃
      (Y ⟶ cm2RightAdj X |>.obj Z) :=
  (cm2Adj X).homEquiv Y Z

noncomputable def cm2Unit (X Y : CondensedSet.{u}) :
    Y ⟶ cm2RightAdj X |>.obj (cm2TensorLeft X |>.obj Y) :=
  (cm2Adj X).unit.app Y

noncomputable def cm2Counit (X Z : CondensedSet.{u}) :
    cm2TensorLeft X |>.obj (cm2RightAdj X |>.obj Z) ⟶ Z :=
  (cm2Adj X).counit.app Z

noncomputable def cm2Evaluation (X Z : CondensedSet.{u}) :
    cm2TensorLeft X |>.obj (cm2RightAdj X |>.obj Z) ⟶ Z :=
  cm2Counit X Z

theorem cm2TensorLeft_source (X : CondensedSet.{u}) :
    cm2TensorLeft X = tensorLeft X := rfl

theorem cm2Evaluation_source (X Z : CondensedSet.{u}) :
    cm2Evaluation X Z = (cm2Adj X).counit.app Z := rfl

end CMDG.CondensedCM2
