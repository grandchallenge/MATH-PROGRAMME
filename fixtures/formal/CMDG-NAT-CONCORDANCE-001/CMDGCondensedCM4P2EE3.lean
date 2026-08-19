import CMDGCondensedCM4P2EE2

/-!
# CMDG CM4-P2-E E3 — canonical right-Kan uniqueness

E1 supplies the canonical finite comparison and E2 has already transported that comparison into
its right-extension counit. This final mathematical layer aligns the certified E2 right extension
with the pinned pointwise right-Kan-extension certificate for `Condensed.profiniteSolid`, converts
the latter to the ordinary right-Kan property, and applies the pinned uniqueness API.

No broader P2, CM4, C04/C06, or CMDG closure is asserted here.
-/

namespace CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness

universe u

open CategoryTheory

/-- The pinned `profiniteSolid` right-extension object over the same finite source used by E2. -/
noncomputable def profiniteSolidRightExtension :
    Functor.RightExtension FintypeCat.toProfinite (Condensed.finFree R) :=
  Functor.RightExtension.mk
    (Condensed.profiniteSolid R)
    (Condensed.profiniteSolidCounit R)

/-- The pinned mathlib pointwise certificate, expressed through the local E3 right-extension
object so that its source and counit can be read off syntactically. -/
noncomputable def profiniteSolidRightExtensionIsPointwise :
    profiniteSolidRightExtension.IsPointwiseRightKanExtension := by
  simpa [profiniteSolidRightExtension] using
    (Condensed.profiniteSolidIsPointwiseRightKanExtension R)

/-- Ordinary right-Kan-extension form of the pinned `profiniteSolid` certificate. -/
theorem profiniteSolidIsRightKanExtension :
    (Condensed.profiniteSolid R).IsRightKanExtension
      (Condensed.profiniteSolidCounit R) := by
  exact profiniteSolidRightExtensionIsPointwise.isRightKanExtension

/-- E3 in the source-isomorphism form exposed by the pinned uniqueness API.

The E1 transport is the counit of the certified E2 extension:
`finiteComparisonNatIso.hom : FintypeCat.toProfinite ⋙ measureFunctor ⟶ Condensed.finFree R`.
Thus both certified extensions are now over the same finite source, and the source isomorphism
required by `rightKanExtensionUniqueOfIso` is the identity of `Condensed.finFree R`. -/
noncomputable def measureProfiniteSolidNatIsoOfIso :
    CMDG.CondensedCM4P2D.measureFunctor ≅ Condensed.profiniteSolid R := by
  letI :
      CMDG.CondensedCM4P2D.measureFunctor.IsRightKanExtension
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom :=
    CMDG.CondensedCM4P2E.RightKanReconstruction.measureFunctorIsRightKanExtension
  letI :
      (Condensed.profiniteSolid R).IsRightKanExtension
        (Condensed.profiniteSolidCounit R) :=
    profiniteSolidIsRightKanExtension
  exact
    Functor.rightKanExtensionUniqueOfIso
      CMDG.CondensedCM4P2D.measureFunctor
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom
      (Iso.refl (Condensed.finFree R))
      (Condensed.profiniteSolid R)
      (Condensed.profiniteSolidCounit R)

/-- Terminal P2-E mathematical target: the protected measure/dual representation is canonically
naturally isomorphic to pinned `Condensed.profiniteSolid R` by right-Kan uniqueness. -/
noncomputable def measureProfiniteSolidNatIso :
    CMDG.CondensedCM4P2D.measureFunctor ≅ Condensed.profiniteSolid R := by
  letI :
      CMDG.CondensedCM4P2D.measureFunctor.IsRightKanExtension
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom :=
    CMDG.CondensedCM4P2E.RightKanReconstruction.measureFunctorIsRightKanExtension
  letI :
      (Condensed.profiniteSolid R).IsRightKanExtension
        (Condensed.profiniteSolidCounit R) :=
    profiniteSolidIsRightKanExtension
  exact
    Functor.rightKanExtensionUnique
      CMDG.CondensedCM4P2D.measureFunctor
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom
      (Condensed.profiniteSolid R)
      (Condensed.profiniteSolidCounit R)

#check profiniteSolidRightExtension
#check profiniteSolidRightExtensionIsPointwise
#check profiniteSolidIsRightKanExtension
#check measureProfiniteSolidNatIsoOfIso
#check measureProfiniteSolidNatIso

#print axioms profiniteSolidRightExtension
#print axioms profiniteSolidRightExtensionIsPointwise
#print axioms profiniteSolidIsRightKanExtension
#print axioms measureProfiniteSolidNatIsoOfIso
#print axioms measureProfiniteSolidNatIso

end CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness
