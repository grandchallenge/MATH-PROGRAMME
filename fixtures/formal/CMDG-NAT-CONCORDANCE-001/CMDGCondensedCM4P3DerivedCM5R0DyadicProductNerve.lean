import CMDGCondensedCM4P3DerivedCM5R0DyadicCellCover

/-! The exact nerve image of the binary product cover at any
finite selection of axes and any common dyadic level. -/
noncomputable section
universe u
open Set CategoryTheory
namespace CMDG.CondensedCM5R0.CompactCover.Dyadic
open OrderedGrid

variable (I : Type u)

def cubeP : Profinite.{u} := Profinite.of (I → Bits)
def cubeT : CompHaus.{u} := CompHaus.of (I → Interval)
def cubeCover : profiniteToCompHaus.obj (cubeP I) ⟶ cubeT I :=
  CompHausLike.ofHom _ (⟨fun x i => value (x i),
    continuous_pi fun i => value_continuous.comp (continuous_apply i)⟩ :
    C((I → Bits),(I → Interval)))

theorem cubeCover_epi : Epi (cubeCover I) := by
  apply (CompHaus.epi_iff_surjective _).2
  intro y
  choose a ha using fun i => value_surj (y i)
  exact ⟨a,funext ha⟩

abbrev Rel (n : ℕ) :=
  compactRelationProfinite (cubeP I) (cubeT I) (cubeCover I) n

variable {I}

def observe (F : Finset I) (m n : ℕ) (z : Rel I n) :
    Fin (n+1) → Vertex (↥F) :=
  fun j i => prefixIndex m (z.val j i.val)

def observeList (F : Finset I) (m n : ℕ) (z : Rel I n) :
    List (Vertex (↥F)) := List.ofFn (observe F m n z)

theorem observe_continuous (F : Finset I) (m n : ℕ) :
    Continuous (observe F m n) := by
  apply continuous_pi
  intro j
  apply continuous_pi
  intro i
  exact (prefix_continuous m).comp
    ((continuous_apply i.val).comp ((continuous_apply j).comp continuous_subtype_val))

theorem observe_face (F : Finset I) (m n : ℕ) (k : Fin (n+2))
    (z : Rel I (n+1)) :
    observe F m n ((compactRelationFace (cubeP I) (cubeT I) (cubeCover I) n k).hom.hom z) =
      observe F m (n+1) z ∘ k.succAbove := rfl

theorem shared_cell_adjacent (m a b : ℕ) {x : ℝ}
    (ha : x ∈ cell m a) (hb : x ∈ cell m b) : a ≤ b+1 := by
  have hp : (0 : ℝ) < 2^m := by positivity
  have h := (div_le_div_iff_of_pos_right hp).mp (ha.1.trans hb.2)
  exact_mod_cast h

theorem observe_valid (F : Finset I) (m n : ℕ) (z : Rel I n) :
    valid (2^m-1) (observeList F m n z) := by
  apply (valid_ofFn _ _ _).2
  constructor
  · intro j i
    have h := prefix_lt m (z.val j i.val)
    unfold observe
    omega
  · intro j k i
    have h : value (z.val j i.val) = value (z.val k i.val) := by
      have hh := (z.property j).trans (z.property k).symm
      exact congrFun hh i.val
    exact shared_cell_adjacent m _ _ (value_mem_cell m (z.val j i.val))
      (by rw [h]; exact value_mem_cell m (z.val k i.val))

/-- Conversely every admissible ordered tuple of observed cell labels
has a genuine equal-image lift, not just a pairwise formal relation. -/
theorem observe_surj_valid (F : Finset I) (m n : ℕ)
    (x : Fin (n+1) → Vertex (↥F))
    (hx : valid (2^m-1) (List.ofFn x)) :
    ∃ z : Rel I n, observe F m n z = x := by
  classical
  obtain ⟨hb,ha⟩ := (valid_ofFn _ _ _).1 hx
  let top : ↥F → ℕ := fun i => Finset.univ.sup (fun j : Fin (n+1) => x j i)
  let t : ↥F → ℝ := fun i => (top i : ℝ)/(2:ℝ)^m
  have ht (j : Fin (n+1)) (i : ↥F) : t i ∈ cell m (x j i) := by
    have hlo : x j i ≤ top i :=
      Finset.le_sup (f:=fun k : Fin (n+1) => x k i) (Finset.mem_univ j)
    have hhi : top i ≤ x j i+1 :=
      Finset.sup_le (fun k _ => ha k j i)
    constructor
    · exact div_le_div_of_nonneg_right (by exact_mod_cast hlo) (by positivity)
    · apply div_le_div_of_nonneg_right _ (by positivity)
      exact_mod_cast hhi
  have hl (j : Fin (n+1)) (i : ↥F) : x j i < 2^m := by
    have hp : 0 < 2^m := by positivity
    have hh := hb j i
    omega
  choose a hap hav using fun j i => cell_lift m (x j i) (hl j i) (t i) (ht j i)
  let y : Fin (n+1) → I → Bits :=
    fun j i => if hi : i ∈ F then a j ⟨i,hi⟩ else fun _ => 0
  have hy : ∀ j, (cubeCover I).hom.hom (y j) = (cubeCover I).hom.hom (y 0) := by
    intro j
    funext i
    change value (y j i) = value (y 0 i)
    by_cases hi : i ∈ F
    · simp only [y,dif_pos hi]
      exact Subtype.ext ((hav j ⟨i,hi⟩).trans (hav 0 ⟨i,hi⟩).symm)
    · simp [y,hi]
  refine ⟨⟨y,hy⟩,?_⟩
  funext j i
  change prefixIndex m (y j i.val) = x j i
  simp only [y,dif_pos i.property]
  exact hap j i

#print axioms cubeCover_epi
#print axioms observe_valid
#print axioms observe_surj_valid
#print axioms observe_face
end CMDG.CondensedCM5R0.CompactCover.Dyadic
