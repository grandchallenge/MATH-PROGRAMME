import CMDGCondensedCM4P3DerivedCM5R0AcyclicResolutionTransfer

/-! Use the full ordered Cech replacement of the box cover. An
intersection of finitely many centered boxes is exactly the box
with coordinatewise minimum radius. Every compact probe lifts. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.RealProductProjection
open RealProductCondensedColimit RealProductCompactExhaustion
variable (S : Profinite.{u}) (I : Type u)

abbrev labels (n : ℕ) := Fin (n+1) → Radius I

def intersectionRadius (n : ℕ) (r : labels I n) : Radius I :=
  ⟨fun i => Finset.univ.inf' Finset.univ_nonempty (fun j => (r j).val i),
    fun i => Finset.le_inf' _ _ (fun j _ => (r j).property i)⟩

theorem intersectionRadius_le (n : ℕ) (r : labels I n) (j : Fin (n+1)) :
    intersectionRadius I n r ≤ r j := by
  intro i
  exact Finset.inf'_le (fun k => (r k).val i) (Finset.mem_univ j)

theorem le_intersectionRadius (n : ℕ) (r : labels I n) (a : Radius I)
    (h : ∀ j, a ≤ r j) : a ≤ intersectionRadius I n r := by
  intro i
  exact Finset.le_inf' Finset.univ_nonempty (fun j => (r j).val i) (fun j _ => h j i)

theorem intersection_face_le (n : ℕ) (k : Fin (n+2)) (r : labels I (n+1)) :
    intersectionRadius I (n+1) r ≤ intersectionRadius I n (k.removeNth r) :=
  le_intersectionRadius I n _ _ (fun j => intersectionRadius_le I (n+1) r (k.succAbove j))

abbrev realSections (T : CompHaus.{u}) :=
  C(T, ULift.{u+1,u} (S × (I → ℝ)))

abbrev boxLifts (T : CompHaus.{u}) :=
  Σ r : Radius I, ULift.{u+1,u} (T ⟶ radiusBox S I r)

def liftImage (T : CompHaus.{u}) (z : boxLifts S I T) : realSections S I T :=
  (radiusToReal S I z.1).comp z.2.down.hom.hom

theorem liftImage_surj (T : CompHaus.{u}) :
    Function.Surjective (liftImage S I T) := by
  intro x
  let f : C(T,I → ℝ) :=
    ⟨fun t => (x t).down.2, continuous_snd.comp (continuous_uliftDown.comp x.continuous)⟩
  obtain ⟨r,hr,g,hg⟩ := compactProbe_factors f
  let z : T ⟶ radiusBox S I ⟨r,hr⟩ :=
    CompHausLike.ofHom _ (⟨fun t => ((x t).down.1,g t),
      (continuous_fst.comp (continuous_uliftDown.comp x.continuous)).prodMk g.continuous⟩ :
      C(T,S × Box r))
  refine ⟨⟨⟨r,hr⟩,⟨z⟩⟩,?_⟩
  apply ContinuousMap.ext
  intro t
  apply ULift.ext
  apply Prod.ext
  · rfl
  · exact congrArg (fun q : C(T,I → ℝ) => q t) hg

abbrev relationSections (T : CompHaus.{u}) (n : ℕ) :=
  splitCechTuple (boxLifts S I T) (realSections S I T) (liftImage S I T) n

abbrev intersectionSections (T : CompHaus.{u}) (n : ℕ) :=
  Σ r : labels I n, ULift.{u+1,u} (T ⟶ radiusBox S I (intersectionRadius I n r))

def intersectionToRelation (T : CompHaus.{u}) (n : ℕ)
    (z : intersectionSections S I T n) : relationSections S I T n :=
  ⟨fun j => ⟨z.1 j,⟨z.2.down ≫ radiusInclusion S I
    (homOfLE (intersectionRadius_le I n z.1 j))⟩⟩, by
    intro j
    apply ContinuousMap.ext
    intro t
    rfl⟩

def relationToIntersection (T : CompHaus.{u}) (n : ℕ)
    (z : relationSections S I T n) : intersectionSections S I T n := by
  let r : labels I n := fun j => (z.val j).1
  let f := liftImage S I T (z.val 0)
  have hb (t : T) (i : I) : (f t).down.2 i ∈
      Set.Icc (-(intersectionRadius I n r).val i) ((intersectionRadius I n r).val i) := by
    apply abs_le.mp
    apply Finset.le_inf' Finset.univ_nonempty (fun j => (r j).val i)
    intro j _
    have h := congrArg (fun a : realSections S I T => (a t).down.2 i) (z.property j)
    change (( (z.val j).2.down.hom.hom t).2 i).val = (f t).down.2 i at h
    rw [← h]
    exact abs_le.mpr (((z.val j).2.down.hom.hom t).2 i).property
  refine ⟨r,⟨CompHausLike.ofHom _ (⟨fun t => ((f t).down.1,fun i => ⟨(f t).down.2 i,hb t i⟩),
    (continuous_fst.comp (continuous_uliftDown.comp f.continuous)).prodMk
      (continuous_pi fun i => Continuous.subtype_mk
        ((continuous_apply i).comp (continuous_snd.comp
          (continuous_uliftDown.comp f.continuous))) _)⟩ :
          C(T,S × Box (intersectionRadius I n r).val))⟩⟩

theorem relationToIntersection_labels (T : CompHaus.{u}) (n : ℕ)
    (z : relationSections S I T n) :
    (relationToIntersection S I T n z).1 = fun j => (z.val j).1 := rfl

theorem relationToIntersection_image (T : CompHaus.{u}) (n : ℕ)
    (z : relationSections S I T n) :
    liftImage S I T ⟨intersectionRadius I n (relationToIntersection S I T n z).1,
      (relationToIntersection S I T n z).2⟩ = liftImage S I T (z.val 0) := by
  apply ContinuousMap.ext
  intro t
  apply ULift.ext
  apply Prod.ext
  · rfl
  · rfl

theorem liftImage_inj_at_radius (T : CompHaus.{u}) (r : Radius I)
    (x y : T ⟶ radiusBox S I r)
    (h : liftImage S I T ⟨r,⟨x⟩⟩ = liftImage S I T ⟨r,⟨y⟩⟩) : x=y := by
  apply ConcreteCategory.hom_ext
  intro t
  have ht := congrArg (fun a : realSections S I T => (a t).down) h
  apply Prod.ext
  · exact congrArg (fun p : S × (I → ℝ) => p.1) ht
  · apply inclusion_injective r.val
    exact congrArg (fun p : S × (I → ℝ) => p.2) ht

theorem intersectionToRelation_left (T : CompHaus.{u}) (n : ℕ)
    (z : intersectionSections S I T n) :
    relationToIntersection S I T n (intersectionToRelation S I T n z) = z := by
  rcases z with ⟨r,⟨g⟩⟩
  apply Sigma.ext
  · rfl
  · apply heq_of_eq
    apply ULift.ext
    apply liftImage_inj_at_radius S I T (intersectionRadius I n r)
    exact (relationToIntersection_image S I T n (intersectionToRelation S I T n ⟨r,⟨g⟩⟩)).trans rfl

theorem intersectionToRelation_right (T : CompHaus.{u}) (n : ℕ)
    (z : relationSections S I T n) :
    intersectionToRelation S I T n (relationToIntersection S I T n z) = z := by
  apply Subtype.ext
  funext j
  apply Sigma.ext
  · rfl
  · apply heq_of_eq
    apply ULift.ext
    apply liftImage_inj_at_radius S I T (z.val j).1
    exact (relationToIntersection_image S I T n z).trans (z.property j).symm

#print axioms liftImage_surj
#print axioms relationToIntersection_image
#print axioms intersectionToRelation_left
#print axioms intersectionToRelation_right
end CMDG.CondensedCM5R0.RealProductProjection
