import Mathlib.Condensed.Solid
import Mathlib.Condensed.Discrete.Module
import Mathlib.Topology.Category.Profinite.Nobeling.Induction
import Mathlib.Algebra.Module.ULift

/-!
# CMDG CM4-P2 exact-interface audit fixture

This fixture replays only the formal interfaces established as available by
`CMDG-CONDENSED-CM4-P2-001`.

It deliberately proves neither the CM4-P2 measure/dual bridge nor the parent
CM4 solidity theorem.
-/

namespace CMDG.CondensedCM4P2

universe u

#check Condensed.finFree
#check Condensed.profiniteSolid
#check Condensed.profiniteSolidCounit
#check Condensed.profiniteSolidIsPointwiseRightKanExtension
#check Condensed.profiniteSolidification
#check CondensedMod.LocallyConstant.functor
#check CondensedMod.LocallyConstant.functorIsoDiscrete
#check CondensedMod.LocallyConstant.adjunction
#check LocallyConstant.freeOfProfinite

/-- The already-pinned Nöbeling prerequisite is replayable for every profinite set. -/
theorem nobelingAvailable (S : Profinite.{u}) :
    Module.Free ℤ (LocallyConstant S ℤ) := by
  infer_instance

end CMDG.CondensedCM4P2
