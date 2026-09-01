import CMDGCondensedCM4P3GFreeSections

/-!
# CMDG CM4-P3-G Boolean-cube parameter object

This successor fixture packages the profinite Boolean cube indexed by the chosen Nöbeling basis.
It is the compact parameter space on which the universal `0/1` measure family will live.
-/

namespace CMDG.CondensedCM4P3G.BooleanCube

universe u

open CMDG.CondensedCM4P3G.BasisSeparation

/-- The Boolean product indexed by the chosen integral Nöbeling basis, as a profinite object. -/
noncomputable def basisBooleanCube (X : Profinite.{u}) : Profinite.{u} :=
  Profinite.of (IntegralBasisIndex X → Bool)

/-- The underlying points of the Boolean cube are definitionally Boolean basis-coordinate
vectors. -/
theorem basisBooleanCube_points (X : Profinite.{u}) :
    (basisBooleanCube X : Type u) = (IntegralBasisIndex X → Bool) := by
  rfl

#check basisBooleanCube
#print axioms basisBooleanCube

end CMDG.CondensedCM4P3G.BooleanCube
