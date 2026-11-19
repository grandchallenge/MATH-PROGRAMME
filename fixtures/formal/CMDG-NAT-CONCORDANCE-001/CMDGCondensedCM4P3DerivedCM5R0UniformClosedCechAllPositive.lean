import CMDGCondensedCM4P3DerivedCM5R0UniformFiniteClosedCochainGlue
import CMDGCondensedCM4P3DerivedCM5R0UniformCechCone
import CMDGCondensedCM4P3DerivedCM5R0UniformClosedCechH1

/-!
# Actual all-positive-degree Čech exactness, finite closed families

This is an all-degree Lean theorem for genuine finite closed-intersection
cochains, conditional only on the imported, typechecked Lean lemmas.
Formal mathematical certification and categorical Ext transport are
separate obligations.
-/

noncomputable section
universe u v
open Set
namespace CMDG.CondensedCM5R0

/-- Any ambient cocycle is a coboundary on the part of the genuine
closed-intersection complex lying inside a selected closed E i. -/
theorem uniformClosedCechAmbientCocycle_vertex_primitive
    (X : Profinite.{u}) {I : Type v}
    (E : I → Set X) (n : ℕ)
    (C : uniformClosedCechAmbientCochain X I (n + 2))
    (hc : ∀ (σ : Fin (n + 4) → I) (x : X),
      x ∈ uniformClosedCechIntersection X E (n + 3) σ →
      (uniformClosedCechAmbientDifferential X I (n + 2) C σ) x = 0)
    (i : I) :
    ∀ (σ : Fin (n + 3) → I) (x : X),
      x ∈ E i →
      x ∈ uniformClosedCechIntersection X E (n + 2) σ →
      (uniformClosedCechAmbientDifferential X I (n + 1)
        (uniformClosedCechAmbientCone X I i (n + 1) C) σ) x =
          C σ x := by
  intro σ x hi hx
  have hxcons :
      x ∈ uniformClosedCechIntersection X E (n + 3)
        (Fin.cons i σ) := by
    simp only [uniformClosedCechIntersection, Set.mem_iInter] at hx ⊢
    intro j
    refine Fin.cases ?_ ?_ j
    · simpa only [Fin.cons_zero] using hi
    · intro k
      simpa only [Fin.cons_succ] using hx k
  have hz := hc (Fin.cons i σ) x hxcons
  have hcone := uniformClosedCechAmbientCone_identity
    X I i (n + 1) C σ x
  change
    (uniformClosedCechAmbientDifferential X I (n + 1)
      (uniformClosedCechAmbientCone X I i (n + 1) C) σ) x +
    (uniformClosedCechAmbientDifferential X I (n + 2) C
      (Fin.cons i σ)) x = C σ x at hcone
  rw [hz, add_zero] at hcone
  exact hcone

/-- Degree-raising induction for genuine closed-intersection Čech
exactness: all degree-(n+1) local cocycles being boundaries for every
closed family implies all degree-(n+2) ambient cocycles admit an ambient
primitive on every actual intersection. -/
theorem uniformClosedCechAmbientPositive_inductive_step
    (X : Profinite.{u}) {I : Type v} [Fintype I]
    (n : ℕ)
    (lower : ∀ (D : I → Set X) (hD : ∀ i, IsClosed (D i))
      (c : uniformClosedCechLocalCochain X D (n + 1)),
      uniformClosedCechDifferential X D (n + 1) c = 0 →
      ∃ b : uniformClosedCechLocalCochain X D n,
        uniformClosedCechDifferential X D n b = c)
    (E : I → Set X) (hE : ∀ i, IsClosed (E i))
    (C : uniformClosedCechAmbientCochain X I (n + 2))
    (hc : ∀ (σ : Fin (n + 4) → I) (x : X),
      x ∈ uniformClosedCechIntersection X E (n + 3) σ →
      (uniformClosedCechAmbientDifferential X I (n + 2) C σ) x = 0) :
    ∃ B : uniformClosedCechAmbientCochain X I (n + 1),
      ∀ (σ : Fin (n + 3) → I) (x : X),
        x ∈ uniformClosedCechIntersection X E (n + 2) σ →
        (uniformClosedCechAmbientDifferential X I (n + 1) B σ) x =
          C σ x := by
  classical
  let U (s : Finset I) : Set X :=
    ⋃ j : I, if j ∈ s then E j else ∅
  have hU (s : Finset I) : IsClosed (U s) := by
    apply isClosed_iUnion_of_finite
    intro j
    by_cases hj : j ∈ s
    · simpa [hj] using hE j
    · simp [hj]
  have hUmem (s : Finset I) (x : X) :
      x ∈ U s ↔ ∃ j : I, j ∈ s ∧ x ∈ E j := by
    simp only [U, Set.mem_iUnion]
    constructor
    · rintro ⟨j,hj⟩
      by_cases hjs : j ∈ s
      · exact ⟨j, hjs, by simpa [hjs] using hj⟩
      · simp [hjs] at hj
    · rintro ⟨j,hjs,hj⟩
      exact ⟨j, by simpa [hjs] using hj⟩
  have aux : ∀ s : Finset I,
      ∃ B : uniformClosedCechAmbientCochain X I (n + 1),
        ∀ (σ : Fin (n + 3) → I) (x : X),
          x ∈ U s →
          x ∈ uniformClosedCechIntersection X E (n + 2) σ →
          (uniformClosedCechAmbientDifferential X I (n + 1) B σ) x =
            C σ x := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      refine ⟨fun _ => LocallyConstant.const X 0, ?_⟩
      intro σ x hx
      simp [U] at hx
    | @insert i s hnot ih =>
      obtain ⟨B_F,hFprim⟩ := ih
      let F : Set X := U s
      let B_G : uniformClosedCechAmbientCochain X I (n + 1) :=
        uniformClosedCechAmbientCone X I i (n + 1) C
      have hGprim : ∀ (σ : Fin (n + 3) → I) (x : X),
          x ∈ E i →
          x ∈ uniformClosedCechIntersection X E (n + 2) σ →
          (uniformClosedCechAmbientDifferential X I (n + 1) B_G σ) x =
            C σ x :=
        uniformClosedCechAmbientCocycle_vertex_primitive X E n C hc i
      let D : I → Set X := fun j => (E j ∩ F) ∩ E i
      have hD (j : I) : IsClosed (D j) :=
        ((hE j).inter (hU s)).inter (hE i)
      let W : uniformClosedCechAmbientCochain X I (n + 1) :=
        fun τ => B_F τ - B_G τ
      have hw : uniformClosedCechDifferential X D (n + 1)
          (uniformClosedCechRestrict X D (n + 1) W) = 0 := by
        rw [uniformClosedCechDifferential_restrict]
        funext σ
        apply DFunLike.ext
        intro x
        have hx0 : x.val ∈ D (σ 0) := by
          have hp : x.val ∈ ⋂ j : Fin (n + 3), D (σ j) := x.property
          exact Set.mem_iInter.mp hp 0
        have hxF : x.val ∈ F := hx0.1.2
        have hxi : x.val ∈ E i := hx0.2
        have hxE : x.val ∈ uniformClosedCechIntersection X E (n + 2) σ := by
          simp only [uniformClosedCechIntersection, Set.mem_iInter]
          intro k
          have hp : x.val ∈ ⋂ j : Fin (n + 3), D (σ j) := x.property
          exact (Set.mem_iInter.mp hp k).1.1
        change (uniformClosedCechAmbientDifferential X I (n + 1) W σ) x.val = 0
        rw [uniformClosedCechAmbientDifferential_sub X I (n + 1) B_F B_G]
        change (uniformClosedCechAmbientDifferential X I (n + 1) B_F σ) x.val -
          (uniformClosedCechAmbientDifferential X I (n + 1) B_G σ) x.val = 0
        rw [hFprim σ x.val hxF hxE, hGprim σ x.val hxi hxE]
        exact sub_self _
      obtain ⟨a,ha⟩ := lower D hD
        (uniformClosedCechRestrict X D (n + 1) W) hw
      obtain ⟨A,hA⟩ :=
        uniformClosedCechRestrict_surjective X D hD n a
      rw [← hA, uniformClosedCechDifferential_restrict] at ha
      have hmatch : ∀ (σ : Fin (n + 2) → I) (x : X),
          x ∈ F → x ∈ E i →
          x ∈ uniformClosedCechIntersection X E (n + 1) σ →
          B_F σ x = B_G σ x +
            (uniformClosedCechAmbientDifferential X I n A σ) x := by
        intro σ x hxF hxi hxE
        have hxD : x ∈ uniformClosedCechIntersection X D (n + 1) σ := by
          simp only [uniformClosedCechIntersection, Set.mem_iInter] at hxE ⊢
          intro k
          exact ⟨⟨hxE k, hxF⟩, hxi⟩
        have heq := congrArg
          (fun q : uniformClosedCechLocalCochain X D (n + 1) =>
            q σ ⟨x,hxD⟩) ha
        change (uniformClosedCechAmbientDifferential X I n A σ) x =
          B_F σ x - B_G σ x at heq
        omega
      obtain ⟨B_new,hnew⟩ :=
        uniformClosedCechPrimitives_patch_two X E hE
          F (E i) (hU s) (hE i) n C
          B_F B_G A hFprim hGprim hmatch
      refine ⟨B_new, ?_⟩
      intro σ x hx hxE
      have hi : x ∈ F ∪ E i := by
        obtain ⟨j,hjs,hjE⟩ := (hUmem (insert i s) x).mp hx
        rcases Finset.mem_insert.mp hjs with rfl | hjs'
        · exact Or.inr hjE
        · exact Or.inl ((hUmem s x).mpr ⟨j, hjs', hjE⟩)
      exact hnew σ x hi hxE
  obtain ⟨B,hB⟩ := aux Finset.univ
  refine ⟨B, ?_⟩
  intro σ x hx
  have hx0 : x ∈ E (σ 0) :=
    Set.mem_iInter.mp hx (0 : Fin (n + 3))
  apply hB σ x
  · exact (hUmem Finset.univ x).mpr ⟨σ 0, Finset.mem_univ _, hx0⟩
  · exact hx

/-- **All-positive-degree exactness of the genuine unrestricted-tuple
finite-closed Čech complex with integer-valued locally constant
coefficients.** For every finite closed family and every q>0, each
degree-q cocycle is an actual degree-(q-1) coboundary.

The proof inducts on degree, using the existing constructive H1 base,
an all-degree vertex cone and a finite-closed-family gluing induction
with relative overlap corrections. This does not by itself assert
all-degree condensed categorical Ext vanishing or derived solidity. -/
theorem uniformClosedCechAllPositive_cocycle_coboundary
    (X : Profinite.{u}) {I : Type v} [Fintype I] :
    ∀ n : ℕ, ∀ (E : I → Set X) (hE : ∀ i, IsClosed (E i))
      (c : uniformClosedCechLocalCochain X E (n + 1)),
      uniformClosedCechDifferential X E (n + 1) c = 0 →
      ∃ b : uniformClosedCechLocalCochain X E n,
        uniformClosedCechDifferential X E n b = c := by
  intro n
  induction n with
  | zero =>
    intro E hE c hc
    exact uniformClosedCechDegreeOne_cocycle_coboundary X E hE c hc
  | succ n ih =>
    intro E hE c hc
    obtain ⟨C,hC⟩ :=
      uniformClosedCechRestrict_surjective X E hE (n + 2) c
    have hCoc :
        ∀ (σ : Fin (n + 4) → I) (x : X),
          x ∈ uniformClosedCechIntersection X E (n + 3) σ →
          (uniformClosedCechAmbientDifferential X I (n + 2) C σ) x = 0 := by
      intro σ x hx
      have hc' := hc
      rw [← hC, uniformClosedCechDifferential_restrict X E (n + 2) C] at hc'
      have h := congrArg
        (fun q : uniformClosedCechLocalCochain X E (n + 3) =>
          q σ ⟨x,hx⟩) hc'
      exact h
    obtain ⟨B,hB⟩ :=
      uniformClosedCechAmbientPositive_inductive_step X n ih
        E hE C hCoc
    refine ⟨uniformClosedCechRestrict X E (n + 1) B, ?_⟩
    rw [uniformClosedCechDifferential_restrict]
    rw [← hC]
    funext σ
    apply DFunLike.ext
    intro x
    exact hB σ x.val x.property

#print axioms uniformClosedCechAllPositive_cocycle_coboundary

#print axioms uniformClosedCechAmbientPositive_inductive_step

#print axioms uniformClosedCechAmbientCocycle_vertex_primitive
end CMDG.CondensedCM5R0
