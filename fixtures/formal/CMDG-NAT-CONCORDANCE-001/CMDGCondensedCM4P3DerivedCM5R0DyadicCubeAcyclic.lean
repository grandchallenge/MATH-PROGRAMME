import CMDGCondensedCM4P3DerivedCM5R0DyadicCochainDescent

/-! The actual compact cube (arbitrary index set) is scalar Ext-acyclic.
No finite-grid surrogate assumption: every cochain descends through an
actual surjective observation and the primitive pulls back continuously. -/
noncomputable section
universe u
open Set CategoryTheory
namespace CMDG.CondensedCM5R0.CompactCover.Dyadic
open OrderedGrid

theorem cube_scalarExact (I : Type u) :
    scalarExact (cubeP I) (cubeT I) (cubeCover I) := by
  intro n c hc
  obtain ⟨F,m,hfactor⟩ := observation_factors (n+1) c
  let C := descend F m (n+1) c
  have hC : pull F m (n+1) C = c := by
    ext z
    exact descend_observe F m (n+1) c hfactor z
  have hclosed : ∀ xs, valid (2^m-1) xs → xs.length = n+3 → D C xs = 0 := by
    intro xs hx hl
    obtain ⟨z,hz⟩ := observation_list_surj F m (n+2) xs hx hl
    rw [← hz, ← differential_pull, hC, hc]
    rfl
  obtain ⟨B,hB⟩ := grid_exact (2^m-1) n C hclosed
  refine ⟨pull F m n B,?_⟩
  ext z
  rw [differential_pull, hB _ (observe_valid F m (n+1) z)
    (by simp [observeList])]
  exact descend_observe F m (n+1) c hfactor z

/-- The genuine free condensed module on any product of unit intervals
has no positive Ext into the discrete integer coefficient object. -/
theorem cube_extPositive_zero (I : Type u) (q : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (cubeT I)) discreteIntegerCoeff (q+1)) :
    e = 0 := by
  letI := cubeCover_epi I
  exact compactFree_extPositive_zero_of_scalarExact
    (cubeP I) (cubeT I) (cubeCover I) (cube_scalarExact I) q e

#print axioms cube_scalarExact
#print axioms cube_extPositive_zero
end CMDG.CondensedCM5R0.CompactCover.Dyadic
