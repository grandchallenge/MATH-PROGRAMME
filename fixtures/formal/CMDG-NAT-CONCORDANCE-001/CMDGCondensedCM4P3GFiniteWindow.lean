import CMDGCondensedCM4P3G

/-!
# CMDG CM4-P3-G finite-coordinate window

This successor fixture isolates the compactness/local-constancy input needed by the remaining
coefficient mapping-out argument. A locally constant map on a Boolean product has, at the
all-false point, a single finite coordinate window controlling its value.
-/

namespace CMDG.CondensedCM4P3G.FiniteWindow

open scoped Topology

/-- Local constancy at the zero Boolean vector gives a uniform finite coordinate window:
any vector vanishing on that window has the same value as zero. -/
theorem locallyConstant_boolPi_zero_finiteWindow
    {ι β : Type*} [DecidableEq ι]
    (f : LocallyConstant (ι → Bool) β) :
    ∃ I : Finset ι, ∀ x : ι → Bool,
      (∀ i ∈ I, x i = false) →
      f x = f (fun _ => false) := by
  have hs :
      {x : ι → Bool | f x = f (fun _ => false)} ∈ 𝓝 (fun _ => false) :=
    f.isLocallyConstant.eventually_eq (fun _ => false)
  simp only [nhds_pi, Filter.mem_pi'] at hs
  rcases hs with ⟨I, t, htx, hts⟩
  refine ⟨I, ?_⟩
  intro x hx
  apply hts
  intro i hi
  have hxi : x i = false := hx i (Finset.mem_coe.1 hi)
  simpa [hxi] using mem_of_mem_nhds (htx i)

#print locallyConstant_boolPi_zero_finiteWindow
#print axioms locallyConstant_boolPi_zero_finiteWindow

end CMDG.CondensedCM4P3G.FiniteWindow
