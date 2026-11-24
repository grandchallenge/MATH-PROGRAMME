import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.Topology.Homotopy.Contractible
import Mathlib.Analysis.Convex.Topology
import Mathlib.Topology.Instances.Real.Lemmas

/-! Compact coordinate boxes for the real product, including arbitrary index
sets. This is the analytic topological input to a direct BD/cohomology
calculation, not itself a proof of the derived comparison. -/
noncomputable section
universe u v
namespace CMDG.CondensedCM5R0.RealProductCompactExhaustion

variable {I : Type u}

/-- Radii need not be uniformly bounded across the index set. -/
def Box (b : I → ℝ) := ∀ i, Set.Icc (-(b i)) (b i)

instance (b : I → ℝ) : TopologicalSpace (Box b) := by
  unfold Box
  infer_instance

instance (b : I → ℝ) : CompactSpace (Box b) := by
  unfold Box
  infer_instance

def inclusion (b : I → ℝ) : C(Box b, I → ℝ) :=
  ⟨fun x i => (x i).val,
    continuous_pi fun i => continuous_subtype_val.comp (continuous_apply i)⟩

def zeroPoint (b : I → ℝ) (hb : ∀ i, 0 ≤ b i) : Box b :=
  fun i => ⟨0, ⟨by linarith [hb i], hb i⟩⟩

/-- Every compact probe of the genuine topological product lands in a
single compact box. Coordinatewise sup norms give a witness even for
uncountable I. -/
theorem compactProbe_factors {S : Type v} [TopologicalSpace S] [CompactSpace S]
    (f : C(S, I → ℝ)) :
    ∃ (b : I → ℝ), (∀ i, 0 ≤ b i) ∧
      ∃ g : C(S, Box b), (inclusion b).comp g = f := by
  let fi (i : I) : C(S, ℝ) := ⟨fun s => f s i,
    (continuous_apply i).comp f.continuous⟩
  let b (i : I) : ℝ := ‖fi i‖
  have h (s : S) (i : I) : f s i ∈ Set.Icc (-(b i)) (b i) := by
    apply abs_le.mp
    exact (fi i).norm_coe_le_norm s
  refine ⟨b, fun i => norm_nonneg _, ⟨fun s i => ⟨f s i, h s i⟩,
    continuous_pi fun i => (fi i).continuous.subtype_mk (fun s => h s i)⟩, ?_⟩
  ext s i
  rfl

/-- The factorization is through an injective map, so agreeing lifts into
a common enlarged box agree there. -/
theorem inclusion_injective (b : I → ℝ) : Function.Injective (inclusion b) := by
  intro x y h
  funext i
  apply Subtype.ext
  exact congrFun h i

def enlarge {b c : I → ℝ} (h : ∀ i, b i ≤ c i) : C(Box b, Box c) :=
  ⟨fun x i => ⟨(x i).val, ⟨by linarith [(x i).property.1, h i],
    le_trans (x i).property.2 (h i)⟩⟩,
    continuous_pi fun i => (continuous_subtype_val.comp
      (continuous_apply i)).subtype_mk _⟩

theorem inclusion_enlarge {b c : I → ℝ} (h : ∀ i, b i ≤ c i) :
    (inclusion c).comp (enlarge h) = inclusion b := by
  ext x i
  rfl

/-- Directedness is genuinely coordinatewise. -/
theorem common_box (b c : I → ℝ) :
    ∃ d : I → ℝ, (∀ i, 0 ≤ d i) ∧
      (∀ i, b i ≤ d i) ∧ (∀ i, c i ≤ d i) :=
  ⟨fun i => max 0 (max (b i) (c i)), fun _ => le_max_left _ _,
    fun _ => (le_max_left _ _).trans (le_max_right _ _),
    fun _ => (le_max_right _ _).trans (le_max_right _ _)⟩

/-- The straight-line contraction preserves every coordinate interval. -/
def contraction (b : I → ℝ) (hb : ∀ i, 0 ≤ b i) :
    ContinuousMap.Homotopy (ContinuousMap.const (Box b) (zeroPoint b hb))
      (ContinuousMap.id (Box b)) := by
  let k (p : unitInterval × Box b) (i : I) : ℝ := (p.1 : ℝ) * (p.2 i).val
  have hk (p : unitInterval × Box b) (i : I) :
      k p i ∈ Set.Icc (-(b i)) (b i) := by
    have ht0 := p.1.property.1
    have ht1 := p.1.property.2
    have hx := (p.2 i).property
    have hh : |(p.2 i).val| ≤ b i := abs_le.mpr hx
    apply abs_le.mp
    change |(p.1 : ℝ) * (p.2 i).val| ≤ b i
    rw [abs_mul, abs_of_nonneg ht0]
    exact (mul_le_mul_of_nonneg_right ht1 (abs_nonneg _)).trans (by simpa using hh)
  refine { toFun := fun p i => ⟨k p i, hk p i⟩
           continuous_toFun := ?_
           map_zero_left := ?_
           map_one_left := ?_ }
  · apply continuous_pi
    intro i
    apply Continuous.subtype_mk
    exact (continuous_subtype_val.comp continuous_fst).mul
      (continuous_subtype_val.comp ((continuous_apply i).comp continuous_snd))
  · intro x
    funext i
    apply Subtype.ext
    change 0 * (x i).val = 0
    simp
  · intro x
    funext i
    apply Subtype.ext
    change 1 * (x i).val = (x i).val
    simp

theorem box_contractible (b : I → ℝ) (hb : ∀ i, 0 ≤ b i) :
    ContractibleSpace (Box b) :=
  (contractible_iff_id_nullhomotopic _).2
    ⟨zeroPoint b hb, ⟨(contraction b hb).symm⟩⟩

/-- The exact universe-lifted real product used by the Stonean module
presheaf also has the compact-box factorization. -/
theorem liftedCompactProbe_factors {S : Type v} [TopologicalSpace S] [CompactSpace S]
    (f : C(S, ULift.{u+1,u} (I → ℝ))) :
    ∃ (b : I → ℝ), (∀ i, 0 ≤ b i) ∧
      ∃ g : C(S, Box b), ∀ s, f s = ⟨inclusion b (g s)⟩ := by
  let f' : C(S, I → ℝ) := ⟨fun s => (f s).down,
    continuous_uliftDown.comp f.continuous⟩
  obtain ⟨b, hb, g, hg⟩ := compactProbe_factors f'
  refine ⟨b, hb, g, fun s => ?_⟩
  apply ULift.ext
  exact (congrArg (fun h : C(S, I → ℝ) => h s) hg).symm

/-- Straight-line homotopies commute with enlarging a coordinate box. -/
theorem contraction_enlarge {b c : I → ℝ}
    (hb : ∀ i, 0 ≤ b i) (hc : ∀ i, 0 ≤ c i)
    (h : ∀ i, b i ≤ c i) (t : unitInterval) (x : Box b) :
    enlarge h (contraction b hb (t, x)) =
      contraction c hc (t, enlarge h x) := by
  funext i
  apply Subtype.ext
  rfl

/-- Contraction relative to the external probe, not contraction of the
probe itself. This is the exact topological comparison for BD terms. -/
def parametricContraction (b : I → ℝ) (hb : ∀ i, 0 ≤ b i)
    (S : Type v) [TopologicalSpace S] :
    ContinuousMap.Homotopy
      (⟨fun x : Box b × S => (zeroPoint b hb, x.2),
        continuous_const.prodMk continuous_snd⟩ : C(Box b × S, Box b × S))
      (ContinuousMap.id (Box b × S)) := by
  refine { toFun := fun p => (contraction b hb (p.1, p.2.1), p.2.2)
           continuous_toFun := ?_
           map_zero_left := ?_
           map_one_left := ?_ }
  · exact ((contraction b hb).continuous.comp
      (continuous_fst.prodMk (continuous_fst.comp continuous_snd))).prodMk
      (continuous_snd.comp continuous_snd)
  · intro x
    change (contraction b hb (0, x.1), x.2) = (zeroPoint b hb, x.2)
    have h := (contraction b hb).map_zero_left x.1
    exact congrArg (fun y : Box b => (y, x.2)) h
  · intro x
    change (contraction b hb (1, x.1), x.2) = x
    have h := (contraction b hb).map_one_left x.1
    exact congrArg (fun y : Box b => (y, x.2)) h

#print axioms liftedCompactProbe_factors
#print axioms contraction_enlarge
#print axioms parametricContraction
#print axioms compactProbe_factors
#print axioms inclusion_enlarge
#print axioms common_box
#print axioms box_contractible
end CMDG.CondensedCM5R0.RealProductCompactExhaustion
