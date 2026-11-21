import CMDGCondensedCM5R0BreenDeligneH2Inverse


/-!
# CM5: UNCONDITIONAL degree-two exactness of ACTUAL compact real cochains

Build the continuous-linear four-component degree-three differential
from the actual pentagon, hexagon, symmetry, and diagonal compact
cochain operators. Prove d₂∘d₁=0 and its converse:

  d₂ f=0 ↔ ∃g, d₁ g=f

for every compact Hausdorff abelian A and compact S, particularly
A=(ℝ/ℤ)^I for arbitrary index set I and profinite parameter S.

The converse uses the UNIVERSALLY proved 29-term degree-two
doubling homotopy, the four genuine commutation identities,
nonexpansive doubling, and a Banach Neumann inverse. It does not
assume exactness of the putative BD chain nor use a derived-Hom axiom.

**Important scope:** This proves H²=0 for the constructed four-relation
compact real Banach cochain complex, *not yet* the global all-degree
Breen–Deligne free resolution, the derived condensed real/circle
RHom comparison, circle-to-integers RHom, or the canonical
solidification-unit equality. No full CMDG CM5 or MATHCERT claim.
-/
noncomputable section
universe u v

namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains

variable (A : Type u) (S : Type v)
variable [TopologicalSpace A] [CompactSpace A]
    [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]

theorem degreeTwo_realCochain_closed_exact (f : C2 A S)
    (hp : pentagonCochainDifferential A S f.1 = 0)
    (hh : hexRealDifferential A S f = 0)
    (hs : symRealDifferential A S f = 0)
    (hd : diagonalRealDifferential A S f = 0) :
    ∃ g : C1 A S, differential1 A S g = f := by
  let T : C2 A S →L[ℝ] C2 A S :=
    (1/2 : ℝ) • doubleStar2 A S
  have hT : ‖T‖ < 1 := by
    have hle : ‖T‖ ≤ (1/2 : ℝ) := by
      apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
      intro y
      calc
        ‖T y‖ = (1/2 : ℝ) * ‖doubleStar2 A S y‖ := by
          simp [T,norm_smul]
        _ ≤ (1/2 : ℝ) * ‖y‖ :=
          mul_le_mul_of_nonneg_left
            (doublingStar2_nonexpansive A S y) (by norm_num)
    exact lt_of_le_of_lt hle (by norm_num)
  have hsurj : Function.Surjective
      ((1-T) : C2 A S →L[ℝ] C2 A S) :=
    (ContinuousLinearMap.isUnit_iff_bijective.mp
      (isUnit_one_sub_of_norm_lt_one hT)).2
  obtain ⟨x,hx⟩ := hsurj f
  have hx' : x - (1/2 : ℝ) • doubleStar2 A S x = f := by
    simpa only [ContinuousLinearMap.sub_apply,
      ContinuousLinearMap.one_apply, T,
      ContinuousLinearMap.smul_apply] using hx

  let DP : C2 A S →L[ℝ] C3p A S :=
    (pentagonCochainDifferential A S).comp
      (ContinuousLinearMap.fst ℝ (C2a A S) (C1 A S))
  have hpx : pentagonCochainDifferential A S x.1 = 0 := by
    have heq : DP x = 0 :=
      inverse_half_preserves_kernel (doubleStar2 A S) DP
        (doubleStar3 A S)
        (doubleStar3_nonexpansive A S)
        (by
          intro y
          exact pentagonReal_commutes_doubling A S y)
        f x hp hx'
    exact heq

  have hhx : hexRealDifferential A S x = 0 := by
    apply inverse_half_preserves_kernel (doubleStar2 A S)
      (hexRealDifferential A S) (doubleStar2Assoc A S)
      ?_ ?_ f x hh hx'
    · intro y
      change ‖y.comp (pDouble2a A S)‖ ≤ ‖y‖
      apply (ContinuousMap.norm_le _ (norm_nonneg y)).2
      intro p
      exact y.norm_coe_le_norm ((pDouble2a A S) p)
    · intro y
      simpa [doubleStar2Assoc] using hexagonReal_commutes_doubling A S y

  have hsx : symRealDifferential A S x = 0 := by
    apply inverse_half_preserves_kernel (doubleStar2 A S)
      (symRealDifferential A S) (doubleStar1 A S)
      (doublingStar1_nonexpansive A S) ?_ f x hs hx'
    intro y
    simpa [doubleStar1] using symmetryReal_commutes_doubling A S y

  have hdx : diagonalRealDifferential A S x = 0 := by
    apply inverse_half_preserves_kernel (doubleStar2 A S)
      (diagonalRealDifferential A S) (doubleStar0 A S)
      ?_ ?_ f x hd hx'
    · intro y
      change ‖y.comp (pDouble0 A S)‖ ≤ ‖y‖
      apply (ContinuousMap.norm_le _ (norm_nonneg y)).2
      intro p
      exact y.norm_coe_le_norm ((pDouble0 A S) p)
    · intro y
      simpa [doubleStar0] using diagonalReal_commutes_doubling A S y

  refine ⟨(1/2 : ℝ) • (hStar1 A S x), ?_⟩
  have hclosed := degreeTwo_closed_real_homotopy A S x hpx hhx hsx hdx
  calc
    differential1 A S ((1/2 : ℝ) • hStar1 A S x) =
        (1/2 : ℝ) • differential1 A S (hStar1 A S x) := by
          rw [map_smul]
    _ = (1/2 : ℝ) • (x + x - doubleStar2 A S x) := by rw [hclosed]
    _ = x - (1/2 : ℝ) • doubleStar2 A S x := by
      rw [smul_sub, smul_add]
      have ht : (1/2 : ℝ) • x + (1/2 : ℝ) • x = x := by
        rw [← add_smul]
        norm_num
      rw [ht]
    _ = f := hx'

theorem circleTorus_degreeTwo_realCochain_closed_exact
    (I : Type u) (P : Profinite.{v}) (f : C2 (I → UnitAddCircle) P)
    (hp : pentagonCochainDifferential (I → UnitAddCircle) P f.1 = 0)
    (hh : hexRealDifferential (I → UnitAddCircle) P f = 0)
    (hs : symRealDifferential (I → UnitAddCircle) P f = 0)
    (hd : diagonalRealDifferential (I → UnitAddCircle) P f = 0) :
    ∃ g : C1 (I → UnitAddCircle) P,
      differential1 (I → UnitAddCircle) P g = f :=
  degreeTwo_realCochain_closed_exact (I → UnitAddCircle) P f hp hh hs hd

/-- The actual finite-type four-relation degree-three real-cochain target.
Every component is the compact-continuous function Banach space of the
corresponding genuine condensed source polynomial family. -/
abbrev C3candidate :=
  C3p A S × (C2a A S × (C1 A S × C0 A S))

/-- One continuous-linear degree-two coboundary assembled from the
pentagon, hexagon, symmetric-involution and strict-diagonal operators. -/
def differential2 : C2 A S →L[ℝ] C3candidate A S :=
  ((pentagonCochainDifferential A S).comp
    (ContinuousLinearMap.fst ℝ (C2a A S) (C1 A S))).prod
   ((hexRealDifferential A S).prod
     ((symRealDifferential A S).prod
       (diagonalRealDifferential A S)))

theorem differential2_comp_differential1_zero (f : C1 A S) :
    differential2 A S (differential1 A S f) = 0 := by
  apply Prod.ext
  · exact pentagonCochainDifferential_comp_differential1_zero A S f
  · apply Prod.ext
    · exact hexRealDifferential_comp_differential1_zero A S f
    · apply Prod.ext
      · exact symRealDifferential_comp_differential1_zero A S f
      · exact diagonalRealDifferential_comp_differential1_zero A S f

/-- Exactness at the genuine degree-two compact real-cochain space.
Unlike a mere candidate-chain identity, the reverse inclusion uses
the proved finite homotopy and the Banach Neumann inverse. -/
theorem degreeTwo_realCochain_exact (f : C2 A S) :
    differential2 A S f = 0 ↔
      ∃ g : C1 A S, differential1 A S g = f := by
  constructor
  · intro hf
    have hp : pentagonCochainDifferential A S f.1 = 0 :=
      congrArg Prod.fst hf
    have hh : hexRealDifferential A S f = 0 :=
      congrArg (fun x : C3candidate A S => x.2.1) hf
    have hs : symRealDifferential A S f = 0 :=
      congrArg (fun x : C3candidate A S => x.2.2.1) hf
    have hd : diagonalRealDifferential A S f = 0 :=
      congrArg (fun x : C3candidate A S => x.2.2.2) hf
    exact degreeTwo_realCochain_closed_exact A S f hp hh hs hd
  · rintro ⟨g,hg⟩
    rw [← hg]
    exact differential2_comp_differential1_zero A S g

theorem circleTorus_degreeTwo_realCochain_exact
    (I : Type u) (P : Profinite.{v}) (f : C2 (I → UnitAddCircle) P) :
    differential2 (I → UnitAddCircle) P f = 0 ↔
      ∃ g : C1 (I → UnitAddCircle) P,
        differential1 (I → UnitAddCircle) P g = f :=
  degreeTwo_realCochain_exact (I → UnitAddCircle) P f

#print axioms differential2_comp_differential1_zero
#print axioms degreeTwo_realCochain_exact
#print axioms circleTorus_degreeTwo_realCochain_exact

#print axioms degreeTwo_realCochain_closed_exact
#print axioms circleTorus_degreeTwo_realCochain_closed_exact
end CMDG.CondensedCM5R0.BreenDeligneRealCochains
