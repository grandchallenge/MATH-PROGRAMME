import CMDGCondensedCM4P3DerivedCM5R0UniformClosedCechAllPositive
import CMDGCondensedCM4P3DerivedCM5R0AllArityClosedCechRelation

/-!
# Degree-uniform reduction of finite-observation relation cocycles

A genuine profinite relation cochain with one finite clopen
coordinate observation gives a cocycle on a finite closed family
of images in the target. The all-positive-degree closed-cover theorem
then supplies a finite-index primitive. The remaining work is to prove
continuous reassembly on the actual relation and an unconditional
finite-observation factorization at every arity.
-/

noncomputable section
universe u v
open Set CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem uniformProfiniteFiniteObservation_stage
    (P T : Profinite.{u}) (p : P ⟶ T)
    {J : Type v} [Fintype J] (q : LocallyConstant P J)
    (n : ℕ)
    (d : (Fin (n + 2) → J) → ℤ)
    (hc : ∀ xs : Fin (n + 3) → P,
      (∀ i : Fin (n + 3),
        p.hom.hom (xs i) = p.hom.hom (xs 0)) →
      (∑ k : Fin (n + 3),
        (-1 : ℤ) ^ (k : ℕ) * d (fun j => q (xs (k.succAbove j)))) = 0) :
    ∃ (E : J → Set T) (hE : ∀ j, IsClosed (E j))
      (hImage : ∀ j, E j = p.hom.hom '' {x : P | q x = j})
      (b : uniformClosedCechLocalCochain T E n),
      (∀ σ : Fin (n + 2) → J,
        ∀ t : uniformClosedCechIntersection T E (n + 1) σ,
        (∑ k : Fin (n + 2),
          (-1 : ℤ) ^ (k : ℕ) *
            b (fun j => σ (k.succAbove j))
              ⟨t.val, uniformClosedCechIntersection_face_subset T E
                n σ k t.property⟩) = d σ) := by
  classical
  let E : J → Set T := fun j => p.hom.hom '' {x : P | q x = j}
  have hE (j : J) : IsClosed (E j) := by
    have hf : IsClosed {x : P | q x = j} :=
      (q.isLocallyConstant.isClopen_fiber j).1
    exact ((hf.isCompact).image p.hom.hom.continuous).isClosed
  let cI : uniformClosedCechLocalCochain T E (n + 1) :=
    fun σ => LocallyConstant.const _ (d σ)
  have hCI : uniformClosedCechDifferential T E (n + 1) cI = 0 := by
    funext σ
    apply DFunLike.ext
    intro t
    have ht (j : Fin (n + 3)) : t.val ∈ E (σ j) := by
      have hp : t.val ∈ ⋂ j : Fin (n + 3), E (σ j) := t.property
      exact Set.mem_iInter.mp hp j
    have hchoose (j : Fin (n + 3)) :
        ∃ x : P, q x = σ j ∧ p.hom.hom x = t.val := by
      obtain ⟨x,hx,hpx⟩ := ht j
      exact ⟨x,hx,hpx⟩
    choose xs hxs using hchoose
    have hrel : ∀ j : Fin (n + 3),
        p.hom.hom (xs j) = p.hom.hom (xs 0) := by
      intro j
      exact (hxs j).2.trans (hxs 0).2.symm
    have h := hc xs hrel
    change (LocallyConstant.evalₗ ℤ t)
      (∑ k : Fin (n + 3), (-1 : ℤ) ^ (k : ℕ) •
        uniformClosedCechFaceRestrict T E (n + 1) σ k
          (cI (σ ∘ k.succAbove))) = 0
    simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply, smul_eq_mul]
    change (∑ k : Fin (n + 3),
      (-1 : ℤ) ^ (k : ℕ) * d (σ ∘ k.succAbove)) = 0
    have htag (j : Fin (n + 3)) : q (xs j) = σ j := (hxs j).1
    have hfun (k : Fin (n + 3)) :
        (fun j : Fin (n + 2) => q (xs (k.succAbove j))) =
          σ ∘ k.succAbove := by
      funext j
      exact htag (k.succAbove j)
    simpa only [hfun] using h
  obtain ⟨b,hb⟩ :=
    uniformClosedCechAllPositive_cocycle_coboundary T n E hE cI hCI
  refine ⟨E,hE,(fun _ => rfl),b,?_⟩
  intro σ t
  have h := congrArg
    (fun c : uniformClosedCechLocalCochain T E (n + 1) =>
      c σ t)
      hb
  change (∑ k : Fin (n + 2),
      (-1 : ℤ) ^ (k : ℕ) *
        b (σ ∘ k.succAbove)
          ⟨t.val, uniformClosedCechIntersection_face_subset T E n σ k t.property⟩) = d σ
  rw [← show (cI σ) t = d σ from rfl]
  rw [← h]
  simp only [uniformClosedCechDifferential]
  change (∑ k : Fin (n + 2),
    (-1 : ℤ) ^ (k : ℕ) *
      b (σ ∘ k.succAbove) ⟨t.val, _⟩) =
    (uniformClosedCechDifferential T E n b σ) t
  change (∑ k : Fin (n + 2),
    (-1 : ℤ) ^ (k : ℕ) *
      b (σ ∘ k.succAbove) ⟨t.val, _⟩) =
    (LocallyConstant.evalₗ ℤ t)
      (∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
        uniformClosedCechFaceRestrict T E n σ k
          (b (σ ∘ k.succAbove)))
  simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply, smul_eq_mul]
  rfl

/-- Continuously reassemble a finite-index family of ambient base
functions into one locally constant function of a tuple in P.
The observation map q is shared by the tuple coordinates, with
no section of p. -/
def uniformProfiniteObservedPullback
    (P T : Profinite.{u}) (p : P ⟶ T)
    {J : Type v} [Fintype J] (q : LocallyConstant P J)
    (n : ℕ) (B : uniformClosedCechAmbientCochain T J n) :
    LocallyConstant (Fin (n + 1) → P) ℤ := by
  let obs : (Fin (n + 1) → P) → (Fin (n + 1) → J) :=
    fun xs i => q (xs i)
  let g : (Fin (n + 1) → P) → ℤ :=
    fun xs => B (obs xs) (p.hom.hom (xs 0))
  have hg : IsLocallyConstant g := by
    apply IsLocallyConstant.iff_isOpen_fiber.mpr
    intro z
    have hset : g ⁻¹' {z} =
        ⋃ σ : Fin (n + 1) → J,
          {xs | obs xs = σ} ∩
          {xs | B σ (p.hom.hom (xs 0)) = z} := by
      ext xs
      simp only [Set.mem_preimage, Set.mem_singleton_iff,
        Set.mem_iUnion, Set.mem_inter_iff, Set.mem_setOf_eq]
      constructor
      · intro hx
        exact ⟨obs xs, rfl, hx⟩
      · rintro ⟨σ,hσ,hx⟩
        simpa [g,hσ] using hx
    rw [hset]
    apply isOpen_iUnion
    intro σ
    have hobs : IsOpen {xs : Fin (n + 1) → P | obs xs = σ} := by
      have hset' : {xs : Fin (n + 1) → P | obs xs = σ} =
          ⋂ i : Fin (n + 1),
            {xs : Fin (n + 1) → P | q (xs i) = σ i} := by
        ext xs
        simp only [Set.mem_iInter, Set.mem_setOf_eq, obs]
        exact funext_iff
      rw [hset']
      apply isOpen_iInter_of_finite
      intro i
      have hcoord : Continuous
          (fun xs : Fin (n + 1) → P => xs i) := continuous_apply i
      exact (q.isLocallyConstant.isOpen_fiber (σ i)).preimage hcoord
    have hb : IsOpen {xs : Fin (n + 1) → P |
        B σ (p.hom.hom (xs 0)) = z} :=
      ((B σ).isLocallyConstant.isOpen_fiber z).preimage
        (p.hom.hom.continuous.comp (continuous_apply 0))
    exact hobs.inter hb
  exact ⟨g,hg⟩

theorem uniformProfiniteObservedPullback_apply
    (P T : Profinite.{u}) (p : P ⟶ T)
    {J : Type v} [Fintype J] (q : LocallyConstant P J)
    (n : ℕ) (B : uniformClosedCechAmbientCochain T J n)
    (xs : Fin (n + 1) → P) :
    uniformProfiniteObservedPullback P T p q n B xs =
      B (fun i => q (xs i)) (p.hom.hom (xs 0)) := rfl

/-- A cochain whose values depend on ONE finite observation has
an actual continuous primitive on all related tuples, in EVERY
positive degree, with the exact alternating Čech boundary. The
finite observation is an explicit hypothesis, to be discharged by
an arity-uniform factorization theorem. -/
theorem uniformProfiniteFiniteObserved_relationCocycle_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    {J : Type v} [Fintype J] (q : LocallyConstant P J)
    (n : ℕ)
    (d : (Fin (n + 2) → J) → ℤ)
    (hc : ∀ xs : Fin (n + 3) → P,
      (∀ i : Fin (n + 3),
        p.hom.hom (xs i) = p.hom.hom (xs 0)) →
      (∑ k : Fin (n + 3),
        (-1 : ℤ) ^ (k : ℕ) *
          d (fun j => q (xs (k.succAbove j)))) = 0) :
    ∃ g : LocallyConstant (Fin (n + 1) → P) ℤ,
      ∀ xs : Fin (n + 2) → P,
        (∀ i : Fin (n + 2),
          p.hom.hom (xs i) = p.hom.hom (xs 0)) →
        (∑ k : Fin (n + 2),
          (-1 : ℤ) ^ (k : ℕ) * g (xs ∘ k.succAbove)) =
            d (fun j => q (xs j)) := by
  classical
  obtain ⟨E, hE, hImage, b, hb⟩ :=
    uniformProfiniteFiniteObservation_stage P T p q n d hc
  obtain ⟨B,hB⟩ := uniformClosedCechRestrict_surjective T E hE n b
  let g : LocallyConstant (Fin (n + 1) → P) ℤ :=
    uniformProfiniteObservedPullback P T p q n B
  refine ⟨g, ?_⟩
  intro xs hrel
  let σ : Fin (n + 2) → J := fun j => q (xs j)
  have ht (j : Fin (n + 2)) : p.hom.hom (xs 0) ∈ E (σ j) := by
    rw [hImage (σ j)]
    exact ⟨xs j, rfl, hrel j⟩
  have hxσ : p.hom.hom (xs 0) ∈
      uniformClosedCechIntersection T E (n + 1) σ := by
    simp only [uniformClosedCechIntersection, Set.mem_iInter]
    exact ht
  have hface (k : Fin (n + 2)) :
      p.hom.hom (xs 0) ∈
        uniformClosedCechIntersection T E n (σ ∘ k.succAbove) :=
    uniformClosedCechIntersection_face_subset T E n σ k hxσ
  have hterm (k : Fin (n + 2)) :
      g (xs ∘ k.succAbove) =
        b (σ ∘ k.succAbove) ⟨p.hom.hom (xs 0), hface k⟩ := by
    have hB' := congrArg
      (fun a : uniformClosedCechLocalCochain T E n =>
        a (σ ∘ k.succAbove) ⟨p.hom.hom (xs 0), hface k⟩) hB
    have htfirst :
        p.hom.hom (xs (k.succAbove 0)) = p.hom.hom (xs 0) :=
      hrel (k.succAbove 0)
    rw [uniformProfiniteObservedPullback_apply]
    change B (σ ∘ k.succAbove) (p.hom.hom (xs (k.succAbove 0))) =
      b (σ ∘ k.succAbove) ⟨p.hom.hom (xs 0), hface k⟩
    rw [htfirst]
    exact hB'
  calc
    (∑ k : Fin (n + 2),
      (-1 : ℤ) ^ (k : ℕ) * g (xs ∘ k.succAbove)) =
        (∑ k : Fin (n + 2),
          (-1 : ℤ) ^ (k : ℕ) *
            b (σ ∘ k.succAbove)
              ⟨p.hom.hom (xs 0), hface k⟩) := by
            apply Finset.sum_congr rfl
            intro k hk
            rw [hterm k]
    _ = d σ := hb σ ⟨p.hom.hom (xs 0), hxσ⟩

#print axioms uniformProfiniteFiniteObserved_relationCocycle_potential

#print axioms uniformProfiniteObservedPullback_apply

#print axioms uniformProfiniteFiniteObservation_stage
end CMDG.CondensedCM5R0
