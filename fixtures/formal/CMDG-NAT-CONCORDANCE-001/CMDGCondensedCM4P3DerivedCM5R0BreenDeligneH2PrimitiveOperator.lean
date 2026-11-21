import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneH2Exact


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

#print axioms h2HalfInverse_equation
#print axioms h2PrimitiveOperator
end CMDG.CondensedCM5R0.BreenDeligneRealCochains
