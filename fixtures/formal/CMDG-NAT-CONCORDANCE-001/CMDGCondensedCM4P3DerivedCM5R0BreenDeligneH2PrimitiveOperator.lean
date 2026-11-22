import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneH2Exact
import Mathlib.Tactic.Linarith


/-!
# CMDG CM5: global bounded linear degree-two real-cochain primitive

The admitted (or parent-PR) H² exactness theorem states that every
closed degree-two compact real cochain has a primitive. This module
strengthens the existence theorem to a *single explicit continuous
linear operator*:

  G = (1/2) • (hStar1.comp (1-(1/2) • doubleStar2)⁻¹).

The inverse is a genuine unit in the Banach algebra of continuous
linear endomorphisms, proved using ‖(1/2) [2]*‖ ≤ 1/2 < 1.
The exact inverse identity and the closed-cochain right-inverse
equation d₁(G f)=f are Lean-proved on the actual compact-real
Breen–Deligne candidate cochains, for arbitrary compact Hausdorff
abelian A and compact parameter S.

This is a global bounded choice of real cochain primitives, not
merely pointwise existence. It does NOT assert that the all-degree
Breen–Deligne resolution is exact, that it computes condensed
derived internal Hom, or that the circle-to-integer and canonical
solidification-unit comparisons have been established.
-/
noncomputable section
universe u v
namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains

variable (A : Type u) (S : Type v)
variable [TopologicalSpace A] [CompactSpace A]
  [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]

def h2HalfDoubling : C2 A S →L[ℝ] C2 A S :=
  (1/2 : ℝ) • doubleStar2 A S

theorem h2HalfDoubling_norm_lt_one :
    ‖h2HalfDoubling A S‖ < 1 := by
  have hle : ‖h2HalfDoubling A S‖ ≤ (1/2:ℝ) := by
    apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
    intro y
    calc
      ‖h2HalfDoubling A S y‖ =
          (1/2:ℝ) * ‖doubleStar2 A S y‖ := by
            simp [h2HalfDoubling,norm_smul]
      _ ≤ (1/2:ℝ) * ‖y‖ :=
        mul_le_mul_of_nonneg_left
          (doublingStar2_nonexpansive A S y) (by norm_num)
  exact lt_of_le_of_lt hle (by norm_num)

theorem h2HalfIsUnit : IsUnit (1 - h2HalfDoubling A S) :=
  isUnit_one_sub_of_norm_lt_one (x := h2HalfDoubling A S) (h2HalfDoubling_norm_lt_one A S)

def h2HalfInverseUnit : (C2 A S →L[ℝ] C2 A S)ˣ :=
  (h2HalfIsUnit A S).unit

def h2HalfInverse : C2 A S →L[ℝ] C2 A S :=
  (↑(h2HalfInverseUnit A S)⁻¹ : C2 A S →L[ℝ] C2 A S)

/-- Global continuous linear Neumann primitive, not merely an
existential primitive chosen independently for each cocycle. -/
def h2PrimitiveOperator : C2 A S →L[ℝ] C1 A S :=
  (1/2:ℝ) • (hStar1 A S).comp (h2HalfInverse A S)

theorem h2HalfInverse_equation (f : C2 A S) :
    h2HalfInverse A S f - h2HalfDoubling A S (h2HalfInverse A S f) = f := by
  let u := h2HalfInverseUnit A S
  have hmul : (1-h2HalfDoubling A S) * (↑u⁻¹ : C2 A S →L[ℝ] C2 A S) = 1 := by
    change (↑u : C2 A S →L[ℝ] C2 A S) * (↑u⁻¹ : C2 A S →L[ℝ] C2 A S) = 1
    exact Units.mul_inv u
  have hv := congrArg (fun k : C2 A S →L[ℝ] C2 A S => k f) hmul
  change (↑u⁻¹ : C2 A S →L[ℝ] C2 A S) f -
    h2HalfDoubling A S ((↑u⁻¹ : C2 A S →L[ℝ] C2 A S) f) = f
  simpa only [ContinuousLinearMap.mul_apply,
    ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply] using hv

/-- The global Neumann inverse selects a *single bounded linear*
primitive on the true kernel of the four-relation differential. This
improves the existential H² proof to a canonical continuous-linear
contracting right inverse on cocycles. -/
theorem h2PrimitiveOperator_right_inverse_on_cocycles
    (f : C2 A S) (hf : differential2 A S f = 0) :
    differential1 A S (h2PrimitiveOperator A S f) = f := by
  obtain ⟨g,hg⟩ := (degreeTwo_realCochain_exact A S f).mp hf
  let U : C1 A S →L[ℝ] C1 A S :=
    (1/2 : ℝ) • doubleStar1 A S
  have hU : ‖U‖ < 1 := by
    have hle : ‖U‖ ≤ (1/2 : ℝ) := by
      apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
      intro y
      calc
        ‖U y‖ = (1/2 : ℝ) * ‖doubleStar1 A S y‖ := by
          simp [U,norm_smul]
        _ ≤ (1/2 : ℝ) * ‖y‖ :=
          mul_le_mul_of_nonneg_left
            (doublingStar1_nonexpansive A S y) (by norm_num)
    exact lt_of_le_of_lt hle (by norm_num)
  have hsurj : Function.Surjective
      ((1-U) : C1 A S →L[ℝ] C1 A S) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (isUnit_one_sub_of_norm_lt_one hU)).2
  obtain ⟨y,hy⟩ := hsurj g
  have hy' : y - (1/2 : ℝ) • doubleStar1 A S y = g := by
    simpa only [ContinuousLinearMap.sub_apply,
      ContinuousLinearMap.one_apply,U,
      ContinuousLinearMap.smul_apply] using hy
  let x := h2HalfInverse A S f
  have hTinj : Function.Injective
      ((1 - h2HalfDoubling A S) : C2 A S →L[ℝ] C2 A S) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (h2HalfIsUnit A S)).1
  have hx : x = differential1 A S y := by
    apply hTinj
    have hcomm := differential1_commutes_doubling A S y
    have hd : differential1 A S
          (y-(1/2 : ℝ) • doubleStar1 A S y) =
          differential1 A S y -
            h2HalfDoubling A S (differential1 A S y) := by
      rw [map_sub,map_smul]
      simp only [h2HalfDoubling,ContinuousLinearMap.smul_apply]
      rw [hcomm]
    have heq : differential1 A S y -
          h2HalfDoubling A S (differential1 A S y) = f := by
      rw [←hd,hy',hg]
    have hxeq : x - h2HalfDoubling A S x = f :=
      h2HalfInverse_equation A S f
    simpa only [ContinuousLinearMap.sub_apply,
      ContinuousLinearMap.one_apply] using hxeq.trans heq.symm
  have hp : pentagonCochainDifferential A S x.1 = 0 := by
    rw [hx]
    exact pentagonCochainDifferential_comp_differential1_zero A S y
  have hh : hexRealDifferential A S x = 0 := by
    rw [hx]
    exact hexRealDifferential_comp_differential1_zero A S y
  have hs : symRealDifferential A S x = 0 := by
    rw [hx]
    exact symRealDifferential_comp_differential1_zero A S y
  have hd : diagonalRealDifferential A S x = 0 := by
    rw [hx]
    exact diagonalRealDifferential_comp_differential1_zero A S y
  have hhom := degreeTwo_closed_real_homotopy A S x hp hh hs hd
  change differential1 A S ((1/2 : ℝ) • hStar1 A S x) = f
  calc
    differential1 A S ((1/2 : ℝ) • hStar1 A S x) =
        (1/2 : ℝ) • differential1 A S (hStar1 A S x) := by
          rw [map_smul]
    _ = (1/2 : ℝ) • (x+x-doubleStar2 A S x) := by rw [hhom]
    _ = x - h2HalfDoubling A S x := by
      rw [smul_sub,smul_add]
      have ht : (1/2 : ℝ) • x + (1/2 : ℝ) • x = x := by
        rw [←add_smul]
        norm_num
      rw [ht]
      rfl
    _ = f := h2HalfInverse_equation A S f

#print axioms h2PrimitiveOperator_right_inverse_on_cocycles

/-- The finite degree-one Breen–Deligne homotopy consists of
three associativity pullbacks and one commutativity pullback. Its
actual Banach operator norm is therefore at most four. -/
theorem hStar1_norm_le_four (f : C2 A S) :
    ‖hStar1 A S f‖ ≤ 4 * ‖f‖ := by
  apply (ContinuousMap.norm_le _ (by positivity)).2
  intro p
  have h1 := f.1.norm_coe_le_norm ((qAssoc1 A S) p)
  have h2 := f.1.norm_coe_le_norm ((qAssoc2 A S) p)
  have h3 := f.1.norm_coe_le_norm ((qAssoc3 A S) p)
  have h4 := f.2.norm_coe_le_norm ((qComm A S) p)
  have ha : ‖f.1‖ ≤ ‖f‖ := le_max_left _ _
  have hb : ‖f.2‖ ≤ ‖f‖ := le_max_right _ _
  change ‖f.1 ((qAssoc1 A S) p) -
      f.1 ((qAssoc2 A S) p) -
      f.1 ((qAssoc3 A S) p) -
      f.2 ((qComm A S) p)‖ ≤ 4 * ‖f‖
  linarith [norm_sub_le (f.1 ((qAssoc1 A S) p))
      (f.1 ((qAssoc2 A S) p)),
    norm_sub_le
      (f.1 ((qAssoc1 A S) p) - f.1 ((qAssoc2 A S) p))
      (f.1 ((qAssoc3 A S) p)),
    norm_sub_le
      (f.1 ((qAssoc1 A S) p) - f.1 ((qAssoc2 A S) p) -
        f.1 ((qAssoc3 A S) p))
      (f.2 ((qComm A S) p))]

/-- The inverse of 1−[2]*/2 has norm at most two, without
needing an additional geometric-series norm theorem: the exact
inverse equation and the nonexpansive doubling estimate suffice. -/
theorem h2HalfInverse_norm_le_two (f : C2 A S) :
    ‖h2HalfInverse A S f‖ ≤ 2 * ‖f‖ := by
  let x := h2HalfInverse A S f
  have hx := h2HalfInverse_equation A S f
  have hdouble : ‖h2HalfDoubling A S x‖ ≤ (1/2 : ℝ) * ‖x‖ := by
    change ‖(1/2 : ℝ) • doubleStar2 A S x‖ ≤ _
    rw [norm_smul]
    simp only [Real.norm_eq_abs, abs_of_nonneg (by norm_num : (0:ℝ) ≤ 1/2)]
    exact mul_le_mul_of_nonneg_left
      (doublingStar2_nonexpansive A S x) (by norm_num)
  have hnorm : ‖x‖ ≤ ‖f‖ + ‖h2HalfDoubling A S x‖ := by
    have hh : x = f + h2HalfDoubling A S x := by
      have h := hx
      exact (sub_eq_iff_eq_add.mp h)
    calc
      ‖x‖ = ‖f + h2HalfDoubling A S x‖ := congrArg norm hh
      _ ≤ ‖f‖ + ‖h2HalfDoubling A S x‖ :=
        norm_add_le f (h2HalfDoubling A S x)
  linarith

theorem h2PrimitiveOperator_norm_le_four (f : C2 A S) :
    ‖h2PrimitiveOperator A S f‖ ≤ 4 * ‖f‖ := by
  have h1 := hStar1_norm_le_four A S (h2HalfInverse A S f)
  have h2 := h2HalfInverse_norm_le_two A S f
  change ‖(1/2 : ℝ) • hStar1 A S (h2HalfInverse A S f)‖ ≤ 4 * ‖f‖
  rw [norm_smul]
  simp only [Real.norm_eq_abs, abs_of_nonneg (by norm_num : (0:ℝ) ≤ 1/2)]
  linarith

theorem h2PrimitiveOperator_opNorm_le_four :
    ‖h2PrimitiveOperator A S‖ ≤ 4 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro f
  exact h2PrimitiveOperator_norm_le_four A S f

#print axioms hStar1_norm_le_four
#print axioms h2HalfInverse_norm_le_two
#print axioms h2PrimitiveOperator_opNorm_le_four

/-- A genuine bounded continuous-linear projection of all degree-two
cochains onto the actual four-relation degree-two cocycle space. -/
def h2CocycleProjection : C2 A S →L[ℝ] C2 A S :=
  (differential1 A S).comp (h2PrimitiveOperator A S)

theorem h2CocycleProjection_closed (f : C2 A S) :
    differential2 A S (h2CocycleProjection A S f) = 0 := by
  exact differential2_comp_differential1_zero A S
    (h2PrimitiveOperator A S f)

theorem h2CocycleProjection_eq_of_closed (f : C2 A S)
    (hf : differential2 A S f = 0) :
    h2CocycleProjection A S f = f := by
  exact h2PrimitiveOperator_right_inverse_on_cocycles A S f hf

/-- The full degree-two Banach cochain space splits by a bounded
idempotent whose range consists exactly of the cocycles. -/
theorem h2CocycleProjection_idempotent (f : C2 A S) :
    h2CocycleProjection A S (h2CocycleProjection A S f) =
      h2CocycleProjection A S f :=
  h2CocycleProjection_eq_of_closed A S _
    (h2CocycleProjection_closed A S f)

theorem h2CocycleProjection_norm_le :
    ‖h2CocycleProjection A S‖ ≤
      ‖differential1 A S‖ * 4 := by
  calc
    ‖h2CocycleProjection A S‖ ≤
        ‖differential1 A S‖ * ‖h2PrimitiveOperator A S‖ :=
        ContinuousLinearMap.opNorm_comp_le _ _
    _ ≤ ‖differential1 A S‖ * 4 :=
      mul_le_mul_of_nonneg_left
        (h2PrimitiveOperator_opNorm_le_four A S)
        (norm_nonneg (differential1 A S))

theorem circleTorus_h2CocycleProjection_idempotent
    (I : Type u) (P : Profinite.{v})
    (f : C2 (I → UnitAddCircle) P) :
    h2CocycleProjection (I → UnitAddCircle) P
      (h2CocycleProjection (I → UnitAddCircle) P f) =
      h2CocycleProjection (I → UnitAddCircle) P f :=
  h2CocycleProjection_idempotent (I → UnitAddCircle) P f

#print axioms h2CocycleProjection_idempotent
#print axioms h2CocycleProjection_eq_of_closed
#print axioms h2CocycleProjection_norm_le
#print axioms circleTorus_h2CocycleProjection_idempotent

/-- Quantitative degree-two exactness: a compact real cocycle has a
primitive whose supremum norm is uniformly bounded by four times the
cocycle norm, including arbitrary circle products. -/
theorem degreeTwo_quantitative_exact (f : C2 A S)
    (hf : differential2 A S f = 0) :
    ∃ g : C1 A S,
      differential1 A S g = f ∧ ‖g‖ ≤ 4 * ‖f‖ :=
  ⟨h2PrimitiveOperator A S f,
    h2PrimitiveOperator_right_inverse_on_cocycles A S f hf,
    h2PrimitiveOperator_norm_le_four A S f⟩

theorem circleTorus_degreeTwo_quantitative_exact
    (I : Type u) (P : Profinite.{v})
    (f : C2 (I → UnitAddCircle) P)
    (hf : differential2 (I → UnitAddCircle) P f = 0) :
    ∃ g : C1 (I → UnitAddCircle) P,
      differential1 (I → UnitAddCircle) P g = f ∧
      ‖g‖ ≤ 4 * ‖f‖ :=
  degreeTwo_quantitative_exact (I → UnitAddCircle) P f hf

#print axioms degreeTwo_quantitative_exact
#print axioms circleTorus_degreeTwo_quantitative_exact

#print axioms h2HalfInverse_equation
#print axioms h2PrimitiveOperator
end CMDG.CondensedCM5R0.BreenDeligneRealCochains
