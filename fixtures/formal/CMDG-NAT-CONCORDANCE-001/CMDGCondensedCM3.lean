import Mathlib.Condensed.AB

/-!
CMDG-CONDENSED-CM3-001 checked abelian/AB exactness fixture.

This fixture materializes the pinned abelian-category and Grothendieck-AB
class witnesses for condensed modules over an arbitrary ring, together with
the condensed-abelian-group specialization.

It does not assert that condensed modules are Grothendieck abelian, that they
have a separately certified separator/generator, or any derived-category,
Ext, cohomology, resolution, solid, liquid, global concordance,
GRAPH_CERTIFIED, minimality, or completeness claim.
-/

noncomputable section

open CategoryTheory
open CategoryTheory.Limits

universe u

namespace CMDG.CondensedCM3

noncomputable def cm3Abelian (R : Type (u + 1)) [Ring R] :
    Abelian (CondensedMod.{u} R) :=
  inferInstance

noncomputable def cm3AB5 (R : Type (u + 1)) [Ring R] :
    AB5 (CondensedMod.{u} R) :=
  inferInstance

noncomputable def cm3AB4 (R : Type (u + 1)) [Ring R] :
    AB4 (CondensedMod.{u} R) :=
  inferInstance

noncomputable def cm3AB4Star (R : Type (u + 1)) [Ring R] :
    AB4Star (CondensedMod.{u} R) :=
  inferInstance

noncomputable def cm3CondensedAbAbelian :
    Abelian (CondensedAb.{u}) :=
  inferInstance

noncomputable def cm3CondensedAbAB5 :
    AB5 (CondensedAb.{u}) :=
  inferInstance

noncomputable def cm3CondensedAbAB4 :
    AB4 (CondensedAb.{u}) :=
  inferInstance

noncomputable def cm3CondensedAbAB4Star :
    AB4Star (CondensedAb.{u}) :=
  inferInstance

end CMDG.CondensedCM3
