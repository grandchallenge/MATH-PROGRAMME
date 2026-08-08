import Mathlib.ModelTheory.Semantics
import Mathlib.Algebra.Category.Ring.Basic
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Topology.Category.TopCat.Basic
import Mathlib.Topology.Category.CompHaus.Basic
import Mathlib.Topology.Category.Profinite.Basic
import Mathlib.CategoryTheory.Sites.Grothendieck
import Mathlib.CategoryTheory.Sites.Sheaf
import Mathlib.Condensed.Basic
import Mathlib.Condensed.Discrete.Basic

/-!
CMDG-VERTICAL-SPINE-V0-001 interface probe.

This file checks only that the pinned formal-library surfaces named by the V0
manifest exist in the retained Lean/mathlib environment. It does not confer
semantic authority, foundational concordance, dependency minimality, global
completeness, or GRAPH_CERTIFIED.
-/

#check FirstOrder.Language
#check RingCat
#check CategoryTheory.Category
#check TopCat
#check CompHaus
#check Profinite
#check CategoryTheory.GrothendieckTopology
#check CategoryTheory.Sheaf
#check CategoryTheory.coherentTopology
#check Condensed
#check CondensedSet
#check Condensed.discrete
#check Condensed.underlying
#check Condensed.discreteUnderlyingAdj
