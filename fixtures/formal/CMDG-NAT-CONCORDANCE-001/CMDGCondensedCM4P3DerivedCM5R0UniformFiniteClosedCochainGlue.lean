import CMDGCondensedCM4P3DerivedCM5R0UniformClosedCechH0

/-!
# Degree-uniform finite closed-family cochain gluing and patching

Compatible ambient cochains can be glued over arbitrary finite closed
subsets, without clopen refinement. Actual primitives glue whenever
their values agree on the true tuple intersections. A lower-degree
coboundary corrects overlap discrepancies without changing the
higher differential, giving a degree-uniform primitive patching rule.
-/

/-!
# Degree-uniform gluing of closed-family cochains

For each cochain degree, finitely many ambient tuple cochains that agree on
the actual closed intersections admit one ambient tuple cochain agreeing
with them on all respective closed pieces. The glue is constructed for
each genuine tuple using the already proved closed-family H0 theorem.

No claim of positive Čech cohomological exactness is made here.
-/

noncomputable section
universe u v w
open Set
namespace CMDG.CondensedCM5R0

theorem uniformClosedCechFiniteCochains_glue
    (X : Profinite.{u}) {I : Type v} {J : Type w} [Finite J]
    (E : I → Set X) (F : J → Set X)
    (hE : ∀ i, IsClosed (E i)) (hF : ∀ j, IsClosed (F j))
    (n : ℕ) (B : J → uniformClosedCechAmbientCochain X I n)
    (hagree : ∀ (j k : J) (σ : Fin (n + 1) → I)
      (x : X), x ∈ F j → x ∈ F k →
      x ∈ uniformClosedCechIntersection X E n σ →
      B j σ x = B k σ x) :
    ∃ C : uniformClosedCechAmbientCochain X I n,
      ∀ (j : J) (σ : Fin (n + 1) → I)
        (x : X), x ∈ F j →
        x ∈ uniformClosedCechIntersection X E n σ →
        C σ x = B j σ x := by
  classical
  have hex (σ : Fin (n + 1) → I) :
      ∃ g : LocallyConstant X ℤ,
        ∀ (j : J) (x : X), x ∈ F j →
          x ∈ uniformClosedCechIntersection X E n σ →
          g x = B j σ x := by
    let G : J → Set X := fun j =>
      uniformClosedCechIntersection X E n σ ∩ F j
    have hG (j : J) : IsClosed (G j) :=
      (uniformClosedCechIntersection_isClosed X E hE n σ).inter (hF j)
    let f (j : J) : LocallyConstant (G j) ℤ :=
      (B j σ).comap
        (⟨Subtype.val, continuous_subtype_val⟩ : C(G j, X))
    have hf (j : J) (x : G j) : f j x = B j σ x.val := rfl
    have hg : ∀ (j k : J) (x : X) (hj : x ∈ G j) (hk : x ∈ G k),
        f j ⟨x, hj⟩ = f k ⟨x, hk⟩ := by
      intro j k x hj hk
      exact hagree j k σ x hj.2 hk.2 hj.1
    obtain ⟨g, hglue⟩ :=
      uniformFiniteClosedFamily_glue_ambient X G hG f hg
    refine ⟨g, ?_⟩
    intro j x hj hx
    exact hglue j x ⟨hx, hj⟩
  choose C hC using hex
  exact ⟨C, fun j σ x hj hx => hC σ j x hj hx⟩

/-- Degree-uniform additivity of the genuine ambient Čech differential. -/
theorem uniformClosedCechAmbientDifferential_add
    (X : Profinite.{u}) (I : Type v) (n : ℕ)
    (B D : uniformClosedCechAmbientCochain X I n) :
    uniformClosedCechAmbientDifferential X I n
      (fun σ => B σ + D σ) =
    (fun σ => uniformClosedCechAmbientDifferential X I n B σ +
      uniformClosedCechAmbientDifferential X I n D σ) := by
  funext σ
  apply DFunLike.ext
  intro x
  rw [uniformClosedCechAmbientDifferential_apply,
    LocallyConstant.add_apply,
    uniformClosedCechAmbientDifferential_apply,
    uniformClosedCechAmbientDifferential_apply]
  simp only [scalarCechDifferential, LocallyConstant.add_apply, mul_add,
    Finset.sum_add_distrib]

#print axioms uniformClosedCechAmbientDifferential_add

/-- Degree-uniform subtraction identity for the ambient Čech differential. -/
theorem uniformClosedCechAmbientDifferential_sub
    (X : Profinite.{u}) (I : Type v) (n : ℕ)
    (B D : uniformClosedCechAmbientCochain X I n) :
    uniformClosedCechAmbientDifferential X I n
      (fun σ => B σ - D σ) =
    (fun σ => uniformClosedCechAmbientDifferential X I n B σ -
      uniformClosedCechAmbientDifferential X I n D σ) := by
  funext σ
  apply DFunLike.ext
  intro x
  rw [uniformClosedCechAmbientDifferential_apply,
    LocallyConstant.sub_apply,
    uniformClosedCechAmbientDifferential_apply,
    uniformClosedCechAmbientDifferential_apply]
  simp only [scalarCechDifferential, LocallyConstant.sub_apply, mul_sub,
    Finset.sum_sub_distrib]

#print axioms uniformClosedCechAmbientDifferential_sub

/-- A compatible finite family of ambient local primitives of an
ambient cocycle glues to a single primitive on the union of its closed
domains. The theorem preserves the actual tuple-intersection validity
and does not assume the primitives are compatible automatically. -/
theorem uniformClosedCechFinitePrimitives_glue
    (X : Profinite.{u}) {I : Type v} {J : Type w} [Finite J]
    (E : I → Set X) (F : J → Set X)
    (hE : ∀ i, IsClosed (E i)) (hF : ∀ j, IsClosed (F j))
    (n : ℕ) (C : uniformClosedCechAmbientCochain X I (n + 1))
    (B : J → uniformClosedCechAmbientCochain X I n)
    (hagree : ∀ (j k : J) (σ : Fin (n + 1) → I)
      (x : X), x ∈ F j → x ∈ F k →
      x ∈ uniformClosedCechIntersection X E n σ →
      B j σ x = B k σ x)
    (hprimitive : ∀ (j : J) (σ : Fin (n + 2) → I)
      (x : X), x ∈ F j →
      x ∈ uniformClosedCechIntersection X E (n + 1) σ →
      (uniformClosedCechAmbientDifferential X I n (B j) σ) x =
        C σ x) :
    ∃ b : uniformClosedCechAmbientCochain X I n,
      ∀ (σ : Fin (n + 2) → I) (x : X),
        x ∈ (⋃ j, F j) →
        x ∈ uniformClosedCechIntersection X E (n + 1) σ →
        (uniformClosedCechAmbientDifferential X I n b σ) x =
          C σ x := by
  obtain ⟨b, hb⟩ :=
    uniformClosedCechFiniteCochains_glue X E F hE hF n B hagree
  refine ⟨b, ?_⟩
  intro σ x hxF hxE
  obtain ⟨j, hj⟩ := Set.mem_iUnion.mp hxF
  have hs : (uniformClosedCechAmbientDifferential X I n b σ) x =
      (uniformClosedCechAmbientDifferential X I n (B j) σ) x := by
    rw [uniformClosedCechAmbientDifferential_apply,
      uniformClosedCechAmbientDifferential_apply]
    unfold scalarCechDifferential
    apply Finset.sum_congr rfl
    intro k hk
    have hface :=
      uniformClosedCechIntersection_face_subset X E n σ k hxE
    change (-1 : ℤ) ^ (k : ℕ) * b (σ ∘ k.succAbove) x =
      (-1 : ℤ) ^ (k : ℕ) * B j (σ ∘ k.succAbove) x
    rw [hb j (σ ∘ k.succAbove) x hj hface]
  exact hs.trans (hprimitive j σ x hj hxE)

/-- Two local primitives can be glued after a lower-degree correction
has made their cochain values agree on the actual closed overlap.
The correction does not change either cocycle since d squared is zero.
This is the algebraic patch step in arbitrary positive degree. -/
theorem uniformClosedCechPrimitives_patch_two
    (X : Profinite.{u}) {I : Type v}
    (E : I → Set X) (hE : ∀ i, IsClosed (E i))
    (F G : Set X) (hF : IsClosed F) (hG : IsClosed G)
    (n : ℕ)
    (C : uniformClosedCechAmbientCochain X I (n + 2))
    (B_F B_G : uniformClosedCechAmbientCochain X I (n + 1))
    (A : uniformClosedCechAmbientCochain X I n)
    (hFprim : ∀ (σ : Fin (n + 3) → I) (x : X),
      x ∈ F → x ∈ uniformClosedCechIntersection X E (n + 2) σ →
      (uniformClosedCechAmbientDifferential X I (n + 1) B_F σ) x = C σ x)
    (hGprim : ∀ (σ : Fin (n + 3) → I) (x : X),
      x ∈ G → x ∈ uniformClosedCechIntersection X E (n + 2) σ →
      (uniformClosedCechAmbientDifferential X I (n + 1) B_G σ) x = C σ x)
    (hmatch : ∀ (σ : Fin (n + 2) → I) (x : X),
      x ∈ F → x ∈ G →
      x ∈ uniformClosedCechIntersection X E (n + 1) σ →
      B_F σ x = B_G σ x +
        (uniformClosedCechAmbientDifferential X I n A σ) x) :
    ∃ B : uniformClosedCechAmbientCochain X I (n + 1),
      ∀ (σ : Fin (n + 3) → I) (x : X),
        x ∈ F ∪ G →
        x ∈ uniformClosedCechIntersection X E (n + 2) σ →
        (uniformClosedCechAmbientDifferential X I (n + 1) B σ) x =
          C σ x := by
  classical
  let D : Bool → Set X := fun b => if b then G else F
  have hD (b : Bool) : IsClosed (D b) := by
    cases b
    · simpa [D] using hF
    · simpa [D] using hG
  let B : Bool → uniformClosedCechAmbientCochain X I (n + 1) :=
    fun b => if b then
      (fun σ => B_G σ + uniformClosedCechAmbientDifferential X I n A σ)
      else B_F
  have hb_agree : ∀ (j k : Bool) (σ : Fin (n + 2) → I)
      (x : X), x ∈ D j → x ∈ D k →
      x ∈ uniformClosedCechIntersection X E (n + 1) σ →
      B j σ x = B k σ x := by
    intro j k σ x hj hk hx
    cases j <;> cases k
    · rfl
    · change B_F σ x = B_G σ x +
        (uniformClosedCechAmbientDifferential X I n A σ) x
      exact hmatch σ x hj hk hx
    · change B_G σ x +
        (uniformClosedCechAmbientDifferential X I n A σ) x = B_F σ x
      exact (hmatch σ x hk hj hx).symm
    · rfl
  have hcorrected (σ : Fin (n + 3) → I) (x : X) :
      (uniformClosedCechAmbientDifferential X I (n + 1)
        (fun τ => B_G τ + uniformClosedCechAmbientDifferential X I n A τ)
        σ) x =
      (uniformClosedCechAmbientDifferential X I (n + 1) B_G σ) x := by
    rw [uniformClosedCechAmbientDifferential_add X I (n + 1) B_G
      (uniformClosedCechAmbientDifferential X I n A)]
    have hsq := uniformClosedCechAmbientDifferential_sq_zero X I n A
    have hzero := congrArg
      (fun d : uniformClosedCechAmbientCochain X I (n + 2) =>
        d σ x) hsq
    simpa only [LocallyConstant.add_apply, Pi.zero_apply,
      LocallyConstant.zero_apply, add_zero] using congrArg
      (fun z : ℤ => (uniformClosedCechAmbientDifferential X I (n + 1) B_G σ) x + z)
      hzero
  have hb_prim : ∀ (j : Bool) (σ : Fin (n + 3) → I)
      (x : X), x ∈ D j →
      x ∈ uniformClosedCechIntersection X E (n + 2) σ →
      (uniformClosedCechAmbientDifferential X I (n + 1) (B j) σ) x =
        C σ x := by
    intro j σ x hj hx
    cases j
    · exact hFprim σ x hj hx
    · exact (hcorrected σ x).trans (hGprim σ x hj hx)
  obtain ⟨b,hb⟩ :=
    uniformClosedCechFinitePrimitives_glue X E D hE hD (n + 1)
      C B hb_agree hb_prim
  refine ⟨b, ?_⟩
  intro σ x hx hxE
  apply hb σ x
  cases hx with
  | inl h => exact Set.mem_iUnion.mpr ⟨false, h⟩
  | inr h => exact Set.mem_iUnion.mpr ⟨true, h⟩
  exact hxE

#print axioms uniformClosedCechPrimitives_patch_two

#print axioms uniformClosedCechFinitePrimitives_glue

#print axioms uniformClosedCechFiniteCochains_glue
end CMDG.CondensedCM5R0
