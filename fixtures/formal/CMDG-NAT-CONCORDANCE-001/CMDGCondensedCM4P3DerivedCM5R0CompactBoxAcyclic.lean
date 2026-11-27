import CMDGCondensedCM4P3DerivedCM5R0DyadicCubeAcyclic

/-! Genuine closed boxes, including degenerate intervals, are retracts
of the compact cube. Relative scalar Ext acyclicity passes to retracts. -/
noncomputable section
universe u
open Set CategoryTheory
namespace CMDG.CondensedCM5R0.CompactCover.Dyadic

variable {I : Type u}

def affine (a b : ℝ) (h : a ≤ b) : C(Interval, Set.Icc a b) :=
  ⟨fun x => ⟨a + (b-a)*(x : ℝ), by
    constructor
    · have hh := mul_nonneg (sub_nonneg.mpr h) x.property.1
      linarith
    · have hh := mul_le_mul_of_nonneg_left x.property.2 (sub_nonneg.mpr h)
      linarith⟩,
   Continuous.subtype_mk (continuous_const.add (continuous_const.mul continuous_subtype_val)) _⟩

def affineSection (a b : ℝ) (h : a ≤ b) : C(Set.Icc a b, Interval) := by
  classical
  by_cases he : a=b
  · exact ⟨fun _ => ⟨0,by norm_num⟩,continuous_const⟩
  · have hp : 0 < b-a := sub_pos.mpr (lt_of_le_of_ne h he)
    exact ⟨fun y => ⟨((y:ℝ)-a)/(b-a),
      div_nonneg (sub_nonneg.mpr y.property.1) hp.le,
      (div_le_one₀ hp).2 (by linarith [y.property.2])⟩,
      Continuous.subtype_mk ((continuous_subtype_val.sub continuous_const).div_const _) _⟩

theorem affineSection_rightInverse (a b : ℝ) (h : a ≤ b) :
    Function.RightInverse (affineSection a b h) (affine a b h) := by
  intro x
  by_cases he : a=b
  · apply Subtype.ext
    change a + (b-a)*((affineSection a b h x : Interval) : ℝ) = x.val
    have hx : x.val=a := le_antisymm (he ▸ x.property.2) x.property.1
    have hz : b-a=0 := sub_eq_zero.mpr he.symm
    rw [hz,zero_mul,add_zero,hx]
  · have hp : b-a ≠ 0 := sub_ne_zero.mpr (Ne.symm he)
    apply Subtype.ext
    change a+(b-a)*((affineSection a b h x : Interval) : ℝ) = x.val
    simp [affineSection,he]
    field_simp
    <;> ring

def boxT (a b : I → ℝ) : CompHaus.{u} :=
  CompHaus.of (∀ i, Set.Icc (a i) (b i))

def boxProjection (a b : I → ℝ) (h : ∀ i, a i ≤ b i) :
    cubeT I ⟶ boxT a b :=
  CompHausLike.ofHom _ (⟨fun x i => affine (a i) (b i) (h i) (x i),
    continuous_pi fun i => (affine (a i) (b i) (h i)).continuous.comp
      (continuous_apply i)⟩ : C((I → Interval),(∀ i, Set.Icc (a i) (b i))))

def boxSection (a b : I → ℝ) (h : ∀ i, a i ≤ b i) :
    boxT a b ⟶ cubeT I :=
  CompHausLike.ofHom _ (⟨fun x i => affineSection (a i) (b i) (h i) (x i),
    continuous_pi fun i => (affineSection (a i) (b i) (h i)).continuous.comp
      (continuous_apply i)⟩ : C((∀ i, Set.Icc (a i) (b i)),(I → Interval)))

theorem boxSection_projection (a b : I → ℝ) (h : ∀ i, a i ≤ b i) :
    boxSection a b h ≫ boxProjection a b h = 𝟙 (boxT a b) := by
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  funext i
  exact affineSection_rightInverse (a i) (b i) (h i) (x i)

/-- Relative Ext acyclicity is inherited by actual categorical retracts. -/
theorem ext_zero_of_retract {X Y : Ambient} (s : X ⟶ Y) (r : Y ⟶ X)
    (hr : s ≫ r = 𝟙 X) (q : ℕ)
    (hy : ∀ e : Abelian.Ext Y discreteIntegerCoeff (q+1), e=0)
    (e : Abelian.Ext X discreteIntegerCoeff (q+1)) : e=0 := by
  have hz := hy ((Abelian.Ext.mk₀ r).comp e (zero_add (q+1)))
  have hc : (Abelian.Ext.mk₀ s).comp ((Abelian.Ext.mk₀ r).comp e (zero_add (q+1)))
      (zero_add (q+1)) = e := by
    rw [← Abelian.Ext.comp_assoc, Abelian.Ext.mk₀_comp_mk₀, hr, Abelian.Ext.mk₀_id_comp] <;> omega
  rw [← hc,hz]
  exact Abelian.Ext.comp_zero _ _ _ _ _

theorem box_extPositive_zero (a b : I → ℝ) (h : ∀ i, a i ≤ b i) (q : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (boxT a b)) discreteIntegerCoeff (q+1)) :
    e = 0 := by
  apply ext_zero_of_retract (compactFreeFunctor.map (boxSection a b h))
    (compactFreeFunctor.map (boxProjection a b h)) _ q (cube_extPositive_zero I q) e
  rw [← Functor.map_comp,boxSection_projection]
  exact compactFreeFunctor.map_id _

#print axioms affineSection_rightInverse
#print axioms boxSection_projection
#print axioms box_extPositive_zero
end CMDG.CondensedCM5R0.CompactCover.Dyadic
