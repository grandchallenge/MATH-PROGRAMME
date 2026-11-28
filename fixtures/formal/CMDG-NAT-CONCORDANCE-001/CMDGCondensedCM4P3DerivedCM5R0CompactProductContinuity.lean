import CMDGCondensedCM4P3DerivedCM5R0CompactCoverScalarCohomology
import CMDGCondensedCM4P3DerivedCM5R0CompactCoverFiniteCoordinates

/-! Actual scalar Čech continuity for products of profinite covers.
Finite-coordinate restriction and the pointed extension are compatible
with every face, in every degree. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.CompactCover.ProductContinuity
open CompactCover
variable {I : Type u} (P : I → Profinite.{u}) (T : I → CompHaus.{u})
  (p : ∀ i, profiniteToCompHaus.obj (P i) ⟶ T i)

def prodP : Profinite.{u} := Profinite.of (∀ i, P i)
def prodT : CompHaus.{u} := CompHaus.of (∀ i, T i)
def prodCover : profiniteToCompHaus.obj (prodP P) ⟶ prodT T :=
  CompHausLike.ofHom _ (⟨fun x i => (p i).hom.hom (x i),
    continuous_pi fun i => (p i).hom.hom.continuous.comp (continuous_apply i)⟩ :
      C((∀ i, P i),(∀ i,T i)))

theorem prodCover_epi (hp : ∀ i, Epi (p i)) : Epi (prodCover P T p) := by
  apply (CompHaus.epi_iff_surjective _).2
  intro y
  choose x hx using fun i => (CompHaus.epi_iff_surjective (p i)).1 (hp i) (y i)
  exact ⟨x,funext hx⟩

abbrev Rel (n : ℕ) := compactRelationProfinite (prodP P) (prodT T) (prodCover P T p) n
abbrev Cochain (n : ℕ) := LocallyConstant (Rel P T p n) ℤ
abbrev D (n : ℕ) := scalarD (prodP P) (prodT T) (prodCover P T p) n

def relHomeo (n : ℕ) :
    Rel P T p n ≃ₜ (∀ i, compactRelationProfinite (P i) (T i) (p i) n) :=
  productRelationHomeo (fun i => (p i).hom.hom) n

variable (F : Finset I)
abbrev subP (i : ↥F) := P i.val
abbrev subT (i : ↥F) := T i.val
abbrev subCover (i : ↥F) := p i.val

def restrictRel (n : ℕ) : C(Rel P T p n, Rel (subP P F) (subT T F) (subCover P T p F) n) :=
  ⟨fun z => ⟨fun j i => z.val j i.val,
    fun j => funext fun i => congrFun (z.property j) i.val⟩,
    Continuous.subtype_mk (continuous_pi fun j => continuous_pi fun i =>
      (continuous_apply i.val).comp ((continuous_apply j).comp continuous_subtype_val)) _⟩

def extendRel (x : ∀ i, P i) (n : ℕ) :
    C(Rel (subP P F) (subT T F) (subCover P T p F) n, Rel P T p n) := by
  classical
  refine ⟨fun z => ⟨fun j i => if h : i ∈ F then z.val j ⟨i,h⟩ else x i,?_⟩,?_⟩
  · intro j
    funext i
    change (p i).hom.hom (if h : i ∈ F then z.val j ⟨i,h⟩ else x i) =
      (p i).hom.hom (if h : i ∈ F then z.val 0 ⟨i,h⟩ else x i)
    by_cases hi : i ∈ F
    · simp only [dif_pos hi]
      exact congrFun (z.property j) ⟨i,hi⟩
    · simp only [dif_neg hi]
  · apply Continuous.subtype_mk
    apply continuous_pi
    intro j
    apply continuous_pi
    intro i
    by_cases hi : i ∈ F
    · simp only [dif_pos hi]
      exact
        (continuous_apply (⟨i,hi⟩ : ↥F)).comp ((continuous_apply j).comp
          (continuous_subtype_val : Continuous (Subtype.val : Rel (subP P F) (subT T F) (subCover P T p F) n → _)))
    · simp only [dif_neg hi]
      exact continuous_const

theorem restrict_extend (x : ∀ i, P i) (n : ℕ)
    (z : Rel (subP P F) (subT T F) (subCover P T p F) n) :
    restrictRel P T p F n (extendRel P T p F x n z) = z := by
  classical
  apply Subtype.ext
  funext j i
  change (if h : i.val ∈ F then z.val j ⟨i.val,h⟩ else x i.val) = z.val j i
  rw [dif_pos i.property]

def pull (n : ℕ) (c : Cochain (subP P F) (subT T F) (subCover P T p F) n) :
    Cochain P T p n := c.comap (restrictRel P T p F n)

def descend (x : ∀ i, P i) (n : ℕ) (c : Cochain P T p n) :
    Cochain (subP P F) (subT T F) (subCover P T p F) n :=
  c.comap (extendRel P T p F x n)

theorem pull_injective (x : ∀ i, P i) (n : ℕ) :
    Function.Injective (pull P T p F n) := by
  intro a b h
  ext z
  have hh := congrArg (fun c : Cochain P T p n => c (extendRel P T p F x n z)) h
  change a (restrictRel P T p F n (extendRel P T p F x n z)) =
    b (restrictRel P T p F n (extendRel P T p F x n z)) at hh
  rwa [restrict_extend] at hh

theorem pull_D (n : ℕ) (c : Cochain (subP P F) (subT T F) (subCover P T p F) n) :
    D P T p n (pull P T p F n c) =
      pull P T p F (n+1) (D (subP P F) (subT T F) (subCover P T p F) n c) := by
  ext z
  rw [scalarD_eq]
  change compactCategoricalRelationScalarDifferential _ _ _ n (pull P T p F n c) z =
    D (subP P F) (subT T F) (subCover P T p F) n c (restrictRel P T p F (n+1) z)
  rw [scalarD_eq,compactCategoricalRelationScalarDifferential_apply,
    compactCategoricalRelationScalarDifferential_apply]
  apply Finset.sum_congr rfl
  intro k hk
  rfl

theorem descend_D (x : ∀ i, P i) (n : ℕ) (c : Cochain P T p n) :
    D (subP P F) (subT T F) (subCover P T p F) n (descend P T p F x n c) =
      descend P T p F x (n+1) (D P T p n c) := by
  ext z
  rw [scalarD_eq]
  change compactCategoricalRelationScalarDifferential _ _ _ n (descend P T p F x n c) z =
    D P T p n c (extendRel P T p F x (n+1) z)
  rw [scalarD_eq,compactCategoricalRelationScalarDifferential_apply,
    compactCategoricalRelationScalarDifferential_apply]
  apply Finset.sum_congr rfl
  intro k hk
  rfl

theorem descend_pull (x : ∀ i, P i) (n : ℕ)
    (c : Cochain (subP P F) (subT T F) (subCover P T p F) n) :
    descend P T p F x n (pull P T p F n c) = c := by
  ext z
  change c (restrictRel P T p F n (extendRel P T p F x n z)) = c z
  rw [restrict_extend]

theorem cochain_finiteSupport (x : ∀ i, P i) (n : ℕ) (c : Cochain P T p n) :
    ∃ F : Finset I, pull P T p F n (descend P T p F x n c) = c := by
  classical
  let b := c.comap (⟨(relHomeo P T p n).symm,(relHomeo P T p n).symm.continuous⟩ : C((∀ i, compactRelationProfinite (P i) (T i) (p i) n),Rel P T p n))
  obtain ⟨G,hG⟩ := finiteCoordinateSupport b
  refine ⟨G,?_⟩
  ext z
  change c (extendRel P T p G x n (restrictRel P T p G n z)) = c z
  have h := hG (relHomeo P T p n (extendRel P T p G x n (restrictRel P T p G n z)))
    (relHomeo P T p n z) (by
      intro i hi
      apply Subtype.ext
      funext j
      change (if h : i ∈ G then z.val j i else x i) = z.val j i
      rw [dif_pos hi])
  change c ((relHomeo P T p n).symm (relHomeo P T p n _)) =
    c ((relHomeo P T p n).symm (relHomeo P T p n z)) at h
  simpa only [Homeomorph.symm_apply_apply] using h

theorem cocycle_finiteSupport (x : ∀ i, P i) (n : ℕ) (c : Cochain P T p (n+1))
    (hc : D P T p (n+1) c = 0) :
    ∃ F : Finset I, ∃ b : Cochain (subP P F) (subT T F) (subCover P T p F) (n+1),
      D (subP P F) (subT T F) (subCover P T p F) (n+1) b = 0 ∧
      pull P T p F (n+1) b = c := by
  obtain ⟨G,hG⟩ := cochain_finiteSupport P T p x (n+1) c
  refine ⟨G,descend P T p G x (n+1) c,?_,hG⟩
  rw [descend_D,hc]
  rfl

theorem coboundary_reflects (x : ∀ i, P i) (n : ℕ)
    (c : Cochain (subP P F) (subT T F) (subCover P T p F) (n+1))
    (h : ∃ b : Cochain P T p n, D P T p n b = pull P T p F (n+1) c) :
    ∃ b : Cochain (subP P F) (subT T F) (subCover P T p F) n,
      D (subP P F) (subT T F) (subCover P T p F) n b = c := by
  obtain ⟨b,hb⟩ := h
  exact ⟨descend P T p F x n b,by rw [descend_D,hb,descend_pull]⟩

#print axioms prodCover_epi
#print axioms cocycle_finiteSupport
#print axioms coboundary_reflects
end CMDG.CondensedCM5R0.CompactCover.ProductContinuity
