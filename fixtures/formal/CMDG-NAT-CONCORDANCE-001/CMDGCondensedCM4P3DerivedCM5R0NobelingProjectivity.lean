import CMDGCondensedCM4P3DerivedCM5R0ExtOneEquivalence
import Mathlib.Topology.Category.Profinite.Nobeling.Induction
import Mathlib.Algebra.Category.ModuleCat.Ext.HasExt
import Mathlib.CategoryTheory.Abelian.Projective.Dimension

/-!
# CM5 Nöbeling input: ordinary projectivity and Ext¹ vanishing

A genuine, nonfinite-profinite theorem extracted from the pinned
Nöbeling formalization: locally constant integer functions on every
profinite set form a free ℤ-module. Thus they are projective objects
of the *ordinary* category of integer modules and have zero ordinary
Ext¹ into every integer module.

**Precise boundary:** the result is for `ModuleCat ℤ`, not the
condensed-module ambient category `CondensedMod ZLift`. It does not
assert `Ext¹(F_T,ZLift)=0`, `Ext¹(G_T,ZLift)=0`, nor commute
ordinary and condensed Ext. These require further derived- and
source-semantic bridges.
-/

noncomputable section

universe u

open CategoryTheory

namespace CMDG.CondensedCM5R0

/-- The integer module of locally constant functions on a possibly
infinite profinite set. -/
abbrev LocallyConstantIntegerModule (T : Profinite.{u}) : ModuleCat.{u} ℤ :=
  ModuleCat.of ℤ (LocallyConstant T ℤ)

/-- Nöbeling makes the integer-valued locally constant functions
projective, without imposing finiteness on T. -/
theorem locallyConstantInteger_projective (T : Profinite.{u}) :
    Projective (LocallyConstantIntegerModule T) := by
  infer_instance

/-- Consequently the ordinary (not condensed) Ext¹ group from the
Nöbeling module into any ordinary ℤ-module vanishes, including for
infinite profinite T. -/
theorem locallyConstantInteger_extOne_eq_zero
    (T : Profinite.{u}) (M : ModuleCat.{u} ℤ)
    (e : Abelian.Ext (LocallyConstantIntegerModule T) M 1) :
    e = 0 := by
  letI : Projective (LocallyConstantIntegerModule T) :=
    locallyConstantInteger_projective T
  exact e.eq_zero_of_projective

/-- The stronger Nöbeling consequence: all *positive-degree*
ordinary Ext groups from the locally constant integer module vanish.
This still makes no assertion about condensed-module Ext. -/
theorem locallyConstantInteger_extPositive_eq_zero
    (T : Profinite.{u}) (M : ModuleCat.{u} ℤ)
    (n : ℕ)
    (e : Abelian.Ext (LocallyConstantIntegerModule T) M (n + 1)) :
    e = 0 := by
  letI : Projective (LocallyConstantIntegerModule T) :=
    locallyConstantInteger_projective T
  exact e.eq_zero_of_projective

#print axioms locallyConstantInteger_projective
#print axioms locallyConstantInteger_extOne_eq_zero
#print axioms locallyConstantInteger_extPositive_eq_zero

end CMDG.CondensedCM5R0
