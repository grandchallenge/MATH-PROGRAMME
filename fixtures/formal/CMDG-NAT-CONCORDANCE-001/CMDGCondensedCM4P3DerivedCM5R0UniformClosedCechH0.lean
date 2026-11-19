import CMDGCondensedCM4P3DerivedCM5R0UniformClosedCechCochains

/-!
# Degree-zero exactness and finite closed-family gluing

For any finite family of closed subsets of a profinite space, pairwise
compatible locally constant integer functions glue on their closed union
and extend to the entire profinite space. In particular the actual
all-tuples closed-intersection Čech complex has the expected degree-zero
cocycle-to-ambient-function comparison.

This does not assert higher-degree exactness or derived solidity.
-/

noncomputable section
universe u v w
open Set
namespace CMDG.CondensedCM5R0

/-- Degree-zero gluing on the closed union of a finite closed family. -/
theorem uniformFiniteClosedFamily_glue_on_union
    (X : Profinite.{u}) {I : Type v} [Finite I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : ∀ i, LocallyConstant (E i) ℤ)
    (hagree : ∀ (i j : I) (x : X) (hi : x ∈ E i) (hj : x ∈ E j),
      c i ⟨x, hi⟩ = c j ⟨x, hj⟩) :
    ∃ g : LocallyConstant (⋃ i, E i) ℤ,
      ∀ (i : I) (x : X) (hi : x ∈ E i),
      g ⟨x, mem_iUnion.mpr ⟨i, hi⟩⟩ = c i ⟨x, hi⟩ := by
  classical
  let U : Set X := ⋃ i, E i
  let D : I → Set U := fun i => {x | x.val ∈ E i}
  have hD (i : I) : IsClosed (D i) := by
    exact (hclosed i).preimage continuous_subtype_val
  have hcover : (⋃ i, D i) = Set.univ := by
    ext x
    simp only [Set.mem_iUnion, Set.mem_univ, iff_true]
    obtain ⟨i, hi⟩ := Set.mem_iUnion.mp x.property
    exact ⟨i, hi⟩
  let f (i : I) : LocallyConstant (D i) ℤ :=
    (c i).comap
      (⟨fun x => ⟨x.val.val, x.property⟩,
        Continuous.subtype_mk (continuous_subtype_val.comp continuous_subtype_val) _⟩ :
        C(D i, E i))
  have hf (i : I) (x : D i) : f i x = c i ⟨x.val.val, x.property⟩ := rfl
  have hagree' : ∀ (i j : I) (x : U)
      (hi : x ∈ D i) (hj : x ∈ D j),
      f i ⟨x, hi⟩ = f j ⟨x, hj⟩ := by
    intro i j x hi hj
    exact hagree i j x.val hi hj
  obtain ⟨g, hg⟩ :=
    locallyConstant_glue_finite_closed_cover D hD hcover f hagree'
  refine ⟨g, ?_⟩
  intro i x hi
  have h := hg i ⟨x, Set.mem_iUnion.mpr ⟨i, hi⟩⟩ hi
  exact h

#print axioms uniformFiniteClosedFamily_glue_on_union

/-- Finite closed unions themselves are closed, giving an ambient
extension of any compatible degree-zero tuple of local functions. -/
theorem uniformFiniteClosedFamily_glue_ambient
    (X : Profinite.{u}) {I : Type v} [Finite I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : ∀ i, LocallyConstant (E i) ℤ)
    (hagree : ∀ (i j : I) (x : X) (hi : x ∈ E i) (hj : x ∈ E j),
      c i ⟨x, hi⟩ = c j ⟨x, hj⟩) :
    ∃ g : LocallyConstant X ℤ,
      ∀ (i : I) (x : X) (hi : x ∈ E i),
      g x = c i ⟨x, hi⟩ := by
  have hU : IsClosed (⋃ i, E i) :=
    isClosed_iUnion_of_finite hclosed
  obtain ⟨g, hg⟩ :=
    uniformFiniteClosedFamily_glue_on_union X E hclosed c hagree
  obtain ⟨G, hG⟩ :=
    locallyConstant_extend_closed_subset X (⋃ i, E i) hU g
  refine ⟨G, ?_⟩
  intro i x hi
  rw [hG ⟨x, mem_iUnion.mpr ⟨i, hi⟩⟩]
  exact hg i x hi

#print axioms uniformFiniteClosedFamily_glue_ambient
/-- Every degree-zero cocycle of the genuine unrestricted-tuple complex
comes from one ambient locally constant integer function. -/
theorem uniformClosedCechDegreeZero_cocycle_glues
    (X : Profinite.{u}) {I : Type v} [Finite I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    (c : uniformClosedCechLocalCochain X E 0)
    (hc : uniformClosedCechDifferential X E 0 c = 0) :
    ∃ g : LocallyConstant X ℤ,
      ∀ (i : I) (x : X) (hx : x ∈ E i),
      g x = c (fun _ : Fin 1 => i)
        ⟨x, by
          simp only [uniformClosedCechIntersection, Set.mem_iInter]
          intro _
          exact hx⟩ := by
  classical
  obtain ⟨C, rfl⟩ := uniformClosedCechRestrict_surjective X E hclosed 0 c
  let f (i : I) : LocallyConstant (E i) ℤ :=
    (C (fun _ : Fin 1 => i)).comap
      (⟨Subtype.val, continuous_subtype_val⟩ : C(E i, X))
  have hagree : ∀ (i j : I) (x : X) (hi : x ∈ E i) (hj : x ∈ E j),
      f i ⟨x, hi⟩ = f j ⟨x, hj⟩ := by
    intro i j x hi hj
    let σ : Fin 2 → I := ![i, j]
    have hσ : x ∈ uniformClosedCechIntersection X E 1 σ := by
      simp only [uniformClosedCechIntersection, Set.mem_iInter]
      intro k
      fin_cases k <;> simp [σ, hi, hj]
    have hc' := hc
    rw [uniformClosedCechDifferential_restrict X E 0 C] at hc'
    have hz : (uniformClosedCechAmbientDifferential X I 0 C σ) x = 0 := by
      have h := congrArg (fun q : uniformClosedCechLocalCochain X E 1 =>
        q σ ⟨x, hσ⟩) hc'
      exact h
    simp [uniformClosedCechAmbientDifferential, Fin.sum_univ_two, σ] at hz
    have hfirst : (![i, j] ∘ Fin.succ) = (fun _ : Fin 1 => j) := by
      funext k
      fin_cases k
      rfl
    have hlast : (![i, j] ∘ (Fin.succAbove (1 : Fin 2))) =
        (fun _ : Fin 1 => i) := by
      funext k
      fin_cases k
      rfl
    rw [hfirst, hlast] at hz
    change C (fun _ : Fin 1 => i) x = C (fun _ : Fin 1 => j) x
    omega
  obtain ⟨g, hg⟩ := uniformFiniteClosedFamily_glue_ambient X E hclosed f hagree
  refine ⟨g, ?_⟩
  intro i x hx
  exact hg i x hx

#print axioms uniformClosedCechDegreeZero_cocycle_glues

/-- Coordinatewise degree-zero gluing for arbitrary coefficient
products, with no requirement of a common finite observation. -/
theorem uniformClosedCechDegreeZero_product_cocycle_glues
    (X : Profinite.{u}) {I : Type v} [Finite I]
    (E : I → Set X) (hclosed : ∀ i, IsClosed (E i))
    {ι : Type w} (c : ι → uniformClosedCechLocalCochain X E 0)
    (hc : ∀ a, uniformClosedCechDifferential X E 0 (c a) = 0) :
    ∃ g : ι → LocallyConstant X ℤ,
      ∀ (a : ι) (i : I) (x : X) (hx : x ∈ E i),
      g a x = c a (fun _ : Fin 1 => i)
        ⟨x, by
          simp only [uniformClosedCechIntersection, Set.mem_iInter]
          intro _
          exact hx⟩ := by
  classical
  have h (a : ι) : ∃ g : LocallyConstant X ℤ,
      ∀ (i : I) (x : X) (hx : x ∈ E i),
      g x = c a (fun _ : Fin 1 => i)
        ⟨x, by
          simp only [uniformClosedCechIntersection, Set.mem_iInter]
          intro _
          exact hx⟩ :=
    uniformClosedCechDegreeZero_cocycle_glues X E hclosed (c a) (hc a)
  choose g hg using h
  exact ⟨g, hg⟩

#print axioms uniformClosedCechDegreeZero_product_cocycle_glues
end CMDG.CondensedCM5R0
