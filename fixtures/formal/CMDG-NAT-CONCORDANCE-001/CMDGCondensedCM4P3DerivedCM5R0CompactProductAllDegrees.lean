import CMDGCondensedCM4P3DerivedCM5R0CompactProductExtContinuity

/-! Unconditional compact-product continuity. Stonean presentations
provide genuine profinite covers of arbitrary compact factors. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.CompactCover.ProductContinuity
open CompactCover
variable {I : Type u} (T : I → CompHaus.{u})

abbrev presentationP (i : I) : Profinite.{u} :=
  Stonean.toProfinite.obj (T i).presentation

abbrev presentationCover (i : I) : profiniteToCompHaus.obj (presentationP T i) ⟶ T i :=
  CompHaus.presentation.π (T i)

def coordinateProjection (F : Finset I) : prodT T ⟶ prodT (subT T F) :=
  CompHausLike.ofHom _ (restrictCoordinates F)

abbrev coordinatePull (F : Finset I) (r : ℕ) :
    Abelian.Ext (compactFreeFunctor.obj (prodT (subT T F))) discreteIntegerCoeff r →+
      Abelian.Ext (compactFreeFunctor.obj (prodT T)) discreteIntegerCoeff r :=
  (Abelian.Ext.mk₀ (compactFreeFunctor.map (coordinateProjection T F))).precomp _ (zero_add r)

theorem compactProduct_ext_finiteSupport (x : ∀ i, T i) (r : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (prodT T)) discreteIntegerCoeff r) :
    ∃ F : Finset I, ∃ b, coordinatePull T F r b = e := by
  letI (i : I) : Epi (presentationCover T i) := CompHaus.presentation.epi_π _
  choose y hy using fun i =>
    (CompHaus.epi_iff_surjective (presentationCover T i)).1 inferInstance (x i)
  exact ext_finiteSupport (presentationP T) T (presentationCover T) y r e

theorem compactProduct_coordinatePull_injective (x : ∀ i, T i)
    (F : Finset I) (r : ℕ) : Function.Injective (coordinatePull T F r) :=
  projection_ext_injective (presentationP T) T (presentationCover T) F x r

def coordinateTransition {F G : Finset I} (h : F ⊆ G) :
    prodT (subT T G) ⟶ prodT (subT T F) :=
  CompHausLike.ofHom _ (⟨fun z i => z ⟨i.val,h i.property⟩,
    continuous_pi fun i => continuous_apply (⟨i.val,h i.property⟩ : ↥G)⟩ :
      C((∀ i : ↥G,T i.val),(∀ i : ↥F,T i.val)))

theorem coordinateTransition_comp {F G : Finset I} (h : F ⊆ G) :
    coordinateProjection T G ≫ coordinateTransition T h = coordinateProjection T F := by
  apply ConcreteCategory.hom_ext
  intro z
  rfl

abbrev transitionPull {F G : Finset I} (h : F ⊆ G) (r : ℕ) :
    Abelian.Ext (compactFreeFunctor.obj (prodT (subT T F))) discreteIntegerCoeff r →+
      Abelian.Ext (compactFreeFunctor.obj (prodT (subT T G))) discreteIntegerCoeff r :=
  (Abelian.Ext.mk₀ (compactFreeFunctor.map (coordinateTransition T h))).precomp _ (zero_add r)

theorem coordinatePull_natural {F G : Finset I} (h : F ⊆ G) (r : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (prodT (subT T F))) discreteIntegerCoeff r) :
    coordinatePull T G r (transitionPull T h r e) = coordinatePull T F r e := by
  change (Abelian.Ext.mk₀ (compactFreeFunctor.map (coordinateProjection T G))).comp
    ((Abelian.Ext.mk₀ (compactFreeFunctor.map (coordinateTransition T h))).comp e (zero_add r)) (zero_add r) = _
  rw [← Abelian.Ext.comp_assoc_of_second_deg_zero,Abelian.Ext.mk₀_comp_mk₀,
    ← Functor.map_comp,coordinateTransition_comp]
  rfl

theorem finiteClass_commonStage (x : ∀ i, T i) {F G : Finset I} (r : ℕ)
    (a : Abelian.Ext (compactFreeFunctor.obj (prodT (subT T F))) discreteIntegerCoeff r)
    (b : Abelian.Ext (compactFreeFunctor.obj (prodT (subT T G))) discreteIntegerCoeff r)
    (h : coordinatePull T F r a = coordinatePull T G r b) :
    ∃ H : Finset I, ∃ hF : F ⊆ H, ∃ hG : G ⊆ H,
      transitionPull T hF r a = transitionPull T hG r b := by
  classical
  refine ⟨F ∪ G,Finset.subset_union_left,Finset.subset_union_right,?_⟩
  apply compactProduct_coordinatePull_injective T x (F ∪ G) r
  rw [coordinatePull_natural,coordinatePull_natural,h]

/-- The family of finite-coordinate images covers the entire Ext group.
Inclusions into larger coordinate sets are the actual projection
pullbacks (functoriality), and each image is embedded. -/
theorem compactProduct_ext_union (x : ∀ i, T i) (r : ℕ) :
    (⋃ F : Finset I, Set.range (coordinatePull T F r)) = Set.univ := by
  apply Set.eq_univ_of_forall
  intro e
  obtain ⟨F,b,hb⟩ := compactProduct_ext_finiteSupport T x r e
  exact Set.mem_iUnion.mpr ⟨F,b,hb⟩

#print axioms compactProduct_ext_finiteSupport
#print axioms compactProduct_coordinatePull_injective
#print axioms compactProduct_ext_union
#print axioms finiteClass_commonStage
end CMDG.CondensedCM5R0.CompactCover.ProductContinuity
