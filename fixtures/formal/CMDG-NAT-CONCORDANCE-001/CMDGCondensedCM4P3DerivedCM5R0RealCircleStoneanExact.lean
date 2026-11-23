import Mathlib.Topology.Category.Stonean.Basic
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.Tactic.FunProp
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.Algebra.Homology.ShortComplex.ShortExact


/-!
# CMDG CM5: all-index Stonean exactness of real–circle products

For arbitrary Stonean compact Hausdorff X (universe u) and any
index type I (universe v), construct the actual continuous-map
short exact sequence

  0 → C(X,I→ℤ) → C(X,I→ℝ) → C(X,I→UnitAddCircle) → 0.

Surjectivity uses genuine topological Stonean projectivity (Gleason)
applied to the compact interval [0,1] covering the circle. Because
Gleason projectivity is stated at one universe, lift the interval
and circle through actual ULift to handle arbitrary universe u
without restricting Stonean test object size; do NOT postulate lifts.

Choose lifts of the coordinate circle-valued maps and prove the
assembled product map X→(I→ℝ) is continuous for arbitrary I.
Prove the integer inclusion is injective and exactly identifies
the kernel of real-to-circle reduction via AddCircle.coe_eq_zero_iff
and Int.isClosedEmbedding_coe_real, including inverse continuity.

The result is proved not just as a pointwise existential sequence
but as an actual ShortComplex of ModuleCat ℤ objects with
ShortComplex.ShortExact, and standard Lean axiom footprint only.
This is the precise degree-zero Stonean test-object exactness
input for the derived circle/integer analysis.

NO CLAIM that this alone constructs the three genuine CondensedAb
representables and their short-exact categorical sequence, proves
any derived Hom calculation, an all-degree Breen–Deligne resolution,
or canonical solidification-unit compatibility.
-/
noncomputable section
universe u v
namespace CMDG.CondensedCM5R0.RealCircleStonean

variable (X : Type u) [TopologicalSpace X] [CompactSpace X]
  [T2Space X] [ExtremallyDisconnected X]

theorem circle_map_has_continuous_real_lift (f : C(X, UnitAddCircle)) :
    ∃ g : C(X, ℝ), ∀ x : X, ((g x : ℝ) : UnitAddCircle) = f x := by
  let q : Set.Icc (0 : ℝ) 1 → UnitAddCircle := fun t => ((t : ℝ) : UnitAddCircle)
  have hq : Continuous q :=
    (AddCircle.continuous_mk' (1 : ℝ)).comp continuous_subtype_val
  have hsurj : Function.Surjective q := by
    intro y
    have hm : y ∈ ((↑) : ℝ → UnitAddCircle) '' Set.Icc (0 : ℝ) (0 + 1) := by
      rw [AddCircle.coe_image_Icc_eq]
      trivial
    obtain ⟨t, ht, heq⟩ := hm
    exact ⟨⟨t, by simpa using ht⟩, heq⟩
  let q' : ULift.{u} (Set.Icc (0 : ℝ) 1) → ULift.{u} UnitAddCircle :=
    fun t => ⟨q t.down⟩
  have hq' : Continuous q' :=
    continuous_uliftUp.comp (hq.comp continuous_uliftDown)
  have hsurj' : Function.Surjective q' := by
    rintro ⟨y⟩
    obtain ⟨t, ht⟩ := hsurj y
    exact ⟨⟨t⟩, congrArg ULift.up ht⟩
  let f' : X → ULift.{u} UnitAddCircle := fun x => ⟨f x⟩
  have hf' : Continuous f' := continuous_uliftUp.comp f.continuous
  obtain ⟨g, hg, hgf⟩ :=
    (CompactT2.ExtremallyDisconnected.projective (A := X))
      hf' hq' hsurj'
  refine ⟨⟨fun x => ((g x).down : ℝ),
    (continuous_subtype_val.comp continuous_uliftDown).comp hg⟩, ?_⟩
  intro x
  have hx := congrFun hgf x
  exact congrArg ULift.down hx

theorem torus_map_has_continuous_real_lift
    (I : Type v) (f : C(X, I → UnitAddCircle)) :
    ∃ g : C(X, I → ℝ),
      ∀ x : X, ∀ i : I, ((g x i : ℝ) : UnitAddCircle) = f x i := by
  have hgi (i : I) :
      ∃ g : C(X,ℝ), ∀ x : X, ((g x : ℝ) : UnitAddCircle) = f x i := by
    let fi : C(X,UnitAddCircle) :=
      ⟨fun x => f x i, (continuous_apply i).comp f.continuous⟩
    exact circle_map_has_continuous_real_lift X fi
  choose g hg using hgi
  let G : C(X,I → ℝ) :=
    ⟨fun x i => g i x, continuous_pi (fun i => (g i).continuous)⟩
  exact ⟨G, fun x i => hg i x⟩

theorem torusLift_surjective_realToCircle
    (I : Type v) :
    Function.Surjective (fun g : C(X, I → ℝ) =>
      (⟨fun x i => ((g x i : ℝ) : UnitAddCircle), by
        apply continuous_pi
        intro i
        exact (AddCircle.continuous_mk' (1 : ℝ)).comp
          ((continuous_apply i).comp g.continuous)⟩ :
        C(X, I → UnitAddCircle))) := by
  intro f
  obtain ⟨g,hg⟩ := torus_map_has_continuous_real_lift X I f
  refine ⟨g, ?_⟩
  ext x i
  exact hg x i

def realToCircle (I : Type v) :
    C(X, I → ℝ) →+ C(X, I → UnitAddCircle) where
  toFun g :=
    ⟨fun x i => ((g x i : ℝ) : UnitAddCircle), by
      apply continuous_pi
      intro i
      exact (AddCircle.continuous_mk' (1 : ℝ)).comp
        ((continuous_apply i).comp g.continuous)⟩
  map_zero' := by
    ext x i
    rfl
  map_add' g h := by
    ext x i
    rfl

theorem realToCircle_surjective (I : Type v) :
    Function.Surjective (realToCircle X I) := by
  exact torusLift_surjective_realToCircle X I

def intToReal (I : Type v) :
    C(X, I → ℤ) →+ C(X, I → ℝ) where
  toFun f :=
    ⟨fun x i => (f x i : ℝ), by
      apply continuous_pi
      intro i
      exact (continuous_of_discreteTopology).comp
        ((continuous_apply i).comp f.continuous)⟩
  map_zero' := by
    ext x i
    simp
  map_add' f g := by
    ext x i
    simp

theorem intToReal_injective (I : Type v) :
    Function.Injective (intToReal X I) := by
  intro f g h
  ext x i
  have hh := congrArg (fun k : C(X,I → ℝ) => k x i) h
  change ((f x i : ℤ) : ℝ) = ((g x i : ℤ) : ℝ) at hh
  exact_mod_cast hh

theorem realToCircle_comp_intToReal (I : Type v) :
    (realToCircle X I).comp (intToReal X I) = 0 := by
  apply AddMonoidHom.ext
  intro f
  ext x i
  change (((f x i : ℤ) : ℝ) : UnitAddCircle) = 0
  rw [AddCircle.coe_eq_zero_iff]
  exact ⟨f x i, by simp [zsmul_eq_mul]⟩

theorem realToCircle_kernel_lifts_integer (I : Type v)
    (g : C(X,I → ℝ)) (hg : realToCircle X I g = 0) :
    ∃ z : C(X,I → ℤ), intToReal X I z = g := by
  have hm (x : X) (i : I) : ∃ n : ℤ, (n : ℝ) = g x i := by
    have h := congrArg (fun k : C(X,I → UnitAddCircle) => k x i) hg
    change ((g x i : ℝ) : UnitAddCircle) = 0 at h
    obtain ⟨n, hn⟩ := (AddCircle.coe_eq_zero_iff (p := (1 : ℝ))).mp h
    refine ⟨n, ?_⟩
    simpa [zsmul_eq_mul] using hn
  choose z hz using hm
  have hzi (i : I) : Continuous (fun x : X => z x i) := by
    apply (Int.isClosedEmbedding_coe_real.isEmbedding.continuous_iff).2
    have h : Continuous (fun x : X => g x i) :=
      (continuous_apply i).comp g.continuous
    convert h using 1
    funext x
    exact hz x i
  let Z : C(X, I → ℤ) :=
    ⟨fun x i => z x i, continuous_pi hzi⟩
  refine ⟨Z, ?_⟩
  ext x i
  exact hz x i

theorem realCircle_stonean_exact (I : Type v) :
    Function.Injective (intToReal X I) ∧
    (∀ g : C(X,I → ℝ),
      realToCircle X I g = 0 ↔
      ∃ z : C(X,I → ℤ), intToReal X I z = g) ∧
    Function.Surjective (realToCircle X I) := by
  refine ⟨intToReal_injective X I, ?_, realToCircle_surjective X I⟩
  intro g
  constructor
  · exact realToCircle_kernel_lifts_integer X I g
  · rintro ⟨z,rfl⟩
    have hc := congrArg (fun k : C(X,I → ℤ) →+ C(X,I → UnitAddCircle) => k z)
      (realToCircle_comp_intToReal X I)
    simpa only [AddMonoidHom.comp_apply, AddMonoidHom.zero_apply] using hc

noncomputable def realCircleStoneanModuleSequence (I : Type v) :
    CategoryTheory.ShortComplex (ModuleCat ℤ) :=
  CategoryTheory.ShortComplex.moduleCatMk
    (intToReal X I).toIntLinearMap
    (realToCircle X I).toIntLinearMap
    (by
      apply LinearMap.ext
      intro z
      have h := congrArg
        (fun F : C(X,I → ℤ) →+ C(X,I → UnitAddCircle) => F z)
        (realToCircle_comp_intToReal X I)
      change (realToCircle X I) ((intToReal X I) z) = 0
      exact h)

theorem realCircleStoneanModuleSequence_shortExact (I : Type v) :
    (realCircleStoneanModuleSequence X I).ShortExact := by
  apply CategoryTheory.ShortComplex.ShortExact.mk'
  · apply (CategoryTheory.ShortComplex.moduleCat_exact_iff _).2
    intro g hg
    obtain ⟨z,hz⟩ :=
      realToCircle_kernel_lifts_integer X I g hg
    exact ⟨z,hz⟩
  · exact (ModuleCat.mono_iff_injective _).2 (intToReal_injective X I)
  · exact (ModuleCat.epi_iff_surjective _).2
      (realToCircle_surjective X I)

#print axioms realCircleStoneanModuleSequence_shortExact

#print axioms realCircle_stonean_exact

#print axioms realToCircle_surjective

#print axioms torus_map_has_continuous_real_lift
#print axioms circle_map_has_continuous_real_lift
end CMDG.CondensedCM5R0.RealCircleStonean
