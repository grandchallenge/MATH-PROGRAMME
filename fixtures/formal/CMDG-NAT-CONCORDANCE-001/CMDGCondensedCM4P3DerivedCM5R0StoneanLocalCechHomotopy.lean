import CMDGCondensedCM4P3DerivedCM5R0GSCechTripleBoundary
import Mathlib.AlgebraicTopology.ExtraDegeneracy

/-!
# CMDG CM5 — all-degree Stonean-local Čech contraction

Let T be any profinite space, p : P(T) → T its actual canonical Stonean
presentation, U an arbitrary Stonean space, and q : U → T.

The base-change p_U : U ×_T P(T) → U has a *global* continuous section:
U is projective in Profinite, so q lifts to P(T). This is stronger
than choosing set-theoretic sections and requires NO global section of p.

By the actual Mathlib augmented-Čech nerve extra-degeneracy theorem, the
entire Čech nerve of this base-changed cover has a contracting extra
degeneracy. The free condensed-module functor preserves the extra
degeneracy, and the alternating-face complex becomes chain-homotopy
equivalent to its degree-zero augmentation.

This is a genuine ALL-DEGREE LOCAL contraction for EVERY Stonean probe of
an arbitrary profinite T. It does NOT identify the original unbased
Čech complex with the base-changed one, does not show global exactness of
the triple-to-L_T map, and does not prove Ext² vanishing or derived solidity.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The actual base-changed Stonean presentation of T over any Stonean
test object U → T admits a categorical splitting in Profinite. -/
noncomputable def stoneanLocalPresentationSplitEpi
    (T : Profinite.{u}) (U : Stonean.{u})
    (q : Stonean.toProfinite.obj U ⟶ T) :
    SplitEpi (pullback.fst q (Profinite.presentation.π T)) := by
  let p := Profinite.presentation.π T
  let t : Stonean.toProfinite.obj U ⟶
      Stonean.toProfinite.obj T.presentation :=
    Profinite.lift q p
  have ht : t ≫ p = q := Profinite.lift_lifts q p
  refine
    { section_ := pullback.lift (𝟙 _) t ?_
      id := ?_ }
  · simpa only [Category.id_comp] using ht.symm
  · exact pullback.lift_fst _ _ _

/-- The local base-changed presentation is epimorphic, with an
explicit section obtained from the genuine Stonean lifting property. -/
theorem stoneanLocalPresentation_epi
    (T : Profinite.{u}) (U : Stonean.{u})
    (q : Stonean.toProfinite.obj U ⟶ T) :
    Epi (pullback.fst q (Profinite.presentation.π T)) :=
  (stoneanLocalPresentationSplitEpi T U q).epi

/-- The augmented Čech nerve for the genuinely base-changed presentation.
Its simplicial objects are the finite iterated fiber products over U. -/
noncomputable def stoneanLocalPresentationCechNerve
    (T : Profinite.{u}) (U : Stonean.{u})
    (q : Stonean.toProfinite.obj U ⟶ T) :=
  (Arrow.mk (pullback.fst q
    (Profinite.presentation.π T))).augmentedCechNerve

/-- The genuine augmented Čech nerve has extra degeneracies IN ALL
simplicial degrees, without postulating any cocycle acyclicity. -/
noncomputable def stoneanLocalPresentationExtraDegeneracy
    (T : Profinite.{u}) (U : Stonean.{u})
    (q : Stonean.toProfinite.obj U ⟶ T) :=
  Arrow.AugmentedCechNerve.extraDegeneracy
    (Arrow.mk (pullback.fst q (Profinite.presentation.π T)))
    (stoneanLocalPresentationSplitEpi T U q)

/-- Transport the actual local Čech extra degeneracies to
CondensedMod Coeff by the genuine free-profinite condensed-module functor. -/
noncomputable def stoneanLocalFreeExtraDegeneracy
    (T : Profinite.{u}) (U : Stonean.{u})
    (q : Stonean.toProfinite.obj U ⟶ T) :=
  (stoneanLocalPresentationExtraDegeneracy T U q).map
    (Condensed.profiniteFree Coeff)

/-- All-degree local acyclicity, in the strong chain-homotopy sense:
the alternating free-module Čech complex of the BASE-CHANGED
Stonean presentation is equivalent to the augmentation in degree 0.

The statement is obtained from the actual pinned Mathlib contraction
theorem, not an assumed Ext-vanishing or an arbitrary-profinite
(global) Čech acyclicity claim. -/
noncomputable def stoneanLocalFreeCechHomotopyEquiv
    (T : Profinite.{u}) (U : Stonean.{u})
    (q : Stonean.toProfinite.obj U ⟶ T) :=
  (stoneanLocalFreeExtraDegeneracy T U q).homotopyEquiv

#check stoneanLocalPresentationSplitEpi
#check stoneanLocalPresentation_epi
#check stoneanLocalPresentationCechNerve
#check stoneanLocalPresentationExtraDegeneracy
#check stoneanLocalFreeExtraDegeneracy
#check stoneanLocalFreeCechHomotopyEquiv

#print axioms stoneanLocalPresentationSplitEpi
#print axioms stoneanLocalPresentation_epi
#print axioms stoneanLocalPresentationExtraDegeneracy
#print axioms stoneanLocalFreeExtraDegeneracy
#print axioms stoneanLocalFreeCechHomotopyEquiv

end CMDG.CondensedCM5R0
