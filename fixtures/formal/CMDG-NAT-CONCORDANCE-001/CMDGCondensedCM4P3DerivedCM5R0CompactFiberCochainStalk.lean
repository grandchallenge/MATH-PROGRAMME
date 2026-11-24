import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverGluing
import Mathlib.CategoryTheory.Limits.Types.Filtered
import Mathlib.CategoryTheory.Category.Preorder
import Mathlib.Topology.Separation.Regular

/-! Closed-neighborhood continuity of genuine locally constant cochains
over a compact Hausdorff base. For a profinite source Q and continuous
q:Q→T, the direct limit of sections on preimages of closed neighborhoods
of t is exactly the sections on the actual fiber. This is the local
cochain comparison in the stalk proof of condensed cohomology comparison.
No higher cohomology comparison is presumed. -/

noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits Opposite Set Filter Topology
namespace CMDG.CondensedCM5R0.CompactFiberCochainStalk

variable (Q : Profinite.{u}) (T : CompHaus.{u}) (q : C(Q,T)) (t : T)

/-- A locally constant function on the fiber extends to the entire
profinite source. -/
theorem fiberSection_extends (f : LocallyConstant (q ⁻¹' {t}) ℤ) :
    ∃ g : LocallyConstant Q ℤ, ∀ x : (q ⁻¹' {t}), g x.val = f x :=
  locallyConstant_extend_closed_subset Q _ (isClosed_singleton.preimage q.continuous) f

/-- Equality on the true fiber persists on the inverse image of some
closed neighborhood. Compactness of the source and Hausdorffness of
the target are essential: the disagreement set has closed image. -/
theorem fiberEquality_closedNeighborhood
    (f g : LocallyConstant Q ℤ)
    (h : ∀ x : Q, q x = t → f x = g x) :
    ∃ V : Set T, V ∈ 𝓝 t ∧ IsClosed V ∧
      ∀ x : Q, q x ∈ V → f x = g x := by
  let A : Set Q := {x | f x ≠ g x}
  have hA : IsClosed A := by
    have h0 := (f - g).isLocallyConstant.isOpen_fiber (0 : ℤ)
    convert h0.isClosed_compl using 1
    ext x
    change (¬ f x = g x) ↔ ¬ (f x - g x = 0)
    rw [sub_eq_zero]
  have hC : IsClosed (q '' A) := q.continuous.isClosedMap A hA
  have ht : t ∈ (q '' A)ᶜ := by
    rintro ⟨x, hx, hxt⟩
    exact hx (h x hxt)
  obtain ⟨V, hV, hVc, hsub⟩ :=
    exists_mem_nhds_isClosed_subset (hC.isOpen_compl.mem_nhds ht)
  refine ⟨V, hV, hVc, fun x hx => ?_⟩
  by_contra hne
  exact (hsub hx) ⟨x, hne, rfl⟩

/-- Closed neighborhoods ordered by reverse inclusion. -/
abbrev ClosedNhdIndex :=
  ({V : Set T // IsClosed V ∧ V ∈ 𝓝 t})ᵒᵖ

def wholeNhd : ClosedNhdIndex T t := op ⟨Set.univ, isClosed_univ, univ_mem⟩

instance closedNhdFiltered : IsFiltered (ClosedNhdIndex T t) where
  nonempty := ⟨wholeNhd T t⟩
  cocone_objs i j := by
    let k : ClosedNhdIndex T t := op ⟨i.unop.val ∩ j.unop.val,
      i.unop.property.1.inter j.unop.property.1,
      inter_mem i.unop.property.2 j.unop.property.2⟩
    exact ⟨k, (homOfLE (show k.unop ≤ i.unop from inter_subset_left)).op,
      (homOfLE (show k.unop ≤ j.unop from inter_subset_right)).op, trivial⟩
  cocone_maps i j f g := ⟨j, 𝟙 _, by subsingleton⟩

def restrictSections {V W : Set T} (h : W ⊆ V) :
    LocallyConstant (q ⁻¹' V) ℤ → LocallyConstant (q ⁻¹' W) ℤ :=
  fun f => f.comap
    (⟨fun x => ⟨x.val, h x.property⟩,
      continuous_subtype_val.subtype_mk _⟩ : C((q ⁻¹' W), (q ⁻¹' V)))

def neighborhoodCochains : ClosedNhdIndex T t ⥤ Type u where
  obj i := LocallyConstant (q ⁻¹' i.unop.val) ℤ
  map f := ↾restrictSections Q T q (leOfHom f.unop)
  map_id i := by
    ext f x
    rfl
  map_comp f g := by
    ext h x
    rfl

def fiberCocone : Cocone (neighborhoodCochains Q T q t) where
  pt := LocallyConstant (q ⁻¹' {t}) ℤ
  ι :=
    { app i := ↾restrictSections Q T q
        (singleton_subset_iff.mpr (mem_of_mem_nhds i.unop.property.2))
      naturality := by
        intro i j f
        ext h x
        rfl }

/-- Actual colimit of locally constant sections on closed neighborhoods,
with the genuine restriction maps to the fiber. This applies degreewise
to each profinite term of any actual compact-source Čech resolution. -/
def fiberCoconeIsColimit : IsColimit (fiberCocone Q T q t) := by
  apply Types.FilteredColimit.isColimitOf
  · intro f
    change LocallyConstant (q ⁻¹' {t}) ℤ at f
    obtain ⟨g,hg⟩ := fiberSection_extends Q T q t f
    let i := wholeNhd T t
    let gi : LocallyConstant (q ⁻¹' i.unop.val) ℤ :=
      g.comap ⟨Subtype.val, continuous_subtype_val⟩
    refine ⟨i, gi, ?_⟩
    change f = restrictSections Q T q (V := i.unop.val) (W := {t}) (singleton_subset_iff.mpr (mem_of_mem_nhds i.unop.property.2)) gi
    apply DFunLike.ext
    intro x
    exact (hg x).symm
  · intro i j fi fj h
    change LocallyConstant (q ⁻¹' i.unop.val) ℤ at fi
    change LocallyConstant (q ⁻¹' j.unop.val) ℤ at fj
    obtain ⟨g,hg⟩ := locallyConstant_extend_closed_subset Q _
      (i.unop.property.1.preimage q.continuous) fi
    obtain ⟨g',hg'⟩ := locallyConstant_extend_closed_subset Q _
      (j.unop.property.1.preimage q.continuous) fj
    have hfg : ∀ x : Q, q x = t → g x = g' x := by
      intro x hx
      have hi : q x ∈ i.unop.val := by
        rw [hx]
        exact mem_of_mem_nhds i.unop.property.2
      have hj : q x ∈ j.unop.val := by
        rw [hx]
        exact mem_of_mem_nhds j.unop.property.2
      have hfiber : x ∈ q ⁻¹' {t} := hx
      have hh := congrArg (fun z : LocallyConstant (q ⁻¹' {t}) ℤ => z ⟨x,hfiber⟩) h
      change fi ⟨x,hi⟩ = fj ⟨x,hj⟩ at hh
      exact (hg ⟨x,hi⟩).trans (hh.trans (hg' ⟨x,hj⟩).symm)
    obtain ⟨V,hV,hVc,hagree⟩ := fiberEquality_closedNeighborhood Q T q t g g' hfg
    let k : ClosedNhdIndex T t := op ⟨(i.unop.val ∩ j.unop.val) ∩ V,
      (i.unop.property.1.inter j.unop.property.1).inter hVc,
      inter_mem (inter_mem i.unop.property.2 j.unop.property.2) hV⟩
    have hki : k.unop.val ⊆ i.unop.val := fun x hx => hx.1.1
    have hkj : k.unop.val ⊆ j.unop.val := fun x hx => hx.1.2
    refine ⟨k, (homOfLE (show k.unop ≤ i.unop from hki)).op,
      (homOfLE (show k.unop ≤ j.unop from hkj)).op, ?_⟩
    change restrictSections Q T q hki fi = restrictSections Q T q hkj fj
    apply DFunLike.ext
    intro x
    change fi ⟨x.val,hki x.property⟩ = fj ⟨x.val,hkj x.property⟩
    exact (hg ⟨x.val,hki x.property⟩).symm.trans
      ((hagree x.val x.property.2).trans (hg' ⟨x.val,hkj x.property⟩))

#print axioms fiberSection_extends
#print axioms fiberEquality_closedNeighborhood
#print axioms fiberCoconeIsColimit
end CMDG.CondensedCM5R0.CompactFiberCochainStalk
