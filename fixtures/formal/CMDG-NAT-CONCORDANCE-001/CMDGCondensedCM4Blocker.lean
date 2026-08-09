import Mathlib.Condensed.Solid
import Mathlib.Topology.Category.Profinite.Nobeling.Induction
import Mathlib.Algebra.Ring.ULift

/-!
CMDG-CONDENSED-CM4-001 Stage-A blocker fixture.

This file freezes the exact universe-correct module-level CM4 proposition and
replays only the prerequisite that is already machine-available: Nöbeling
freeness for locally constant integer-valued functions on arbitrary profinite
sets.

It deliberately does not assert `CM4Target`. It contains no proof placeholder,
local postulate, general-ring strengthening, derived/complex claim, C06 claim,
or graph-certification claim.
-/

noncomputable section

universe u

namespace CMDG.CondensedCM4

/-- Universe-correct integer coefficient ring for `CondensedMod.{u}`. -/
abbrev ZLift : Type (u + 1) := ULift.{u + 1} ℤ

/-- Exact module-level theorem proposition governed by CMDG-CONDENSED-CM4-001. -/
def CM4Target : Prop :=
  ∀ S : Profinite.{u},
    CondensedMod.IsSolid ZLift
      ((Condensed.profiniteSolid ZLift).obj S)

/-- Stage-A confirms that the Nöbeling prerequisite is present at the pinned mathlib revision. -/
theorem nobelingAvailable (S : Profinite.{u}) :
    Module.Free ℤ (LocallyConstant S ℤ) := by
  infer_instance

end CMDG.CondensedCM4
