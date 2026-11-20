import CMDGCondensedCM4P3DerivedCM5R0UniformCechSyzygyTower
import CMDGCondensedCM4P3DerivedCM5R0UniformExtLongExactShift
import CMDGCondensedCM4P3DerivedCM5R0GSHigherExtShift

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

private abbrev P (T : Profinite.{u}) : Profinite.{u} :=
  Stonean.toProfinite.obj T.presentation
private abbrev p (T : Profinite.{u}) : P T ⟶ T :=
  Profinite.presentation.π T

/-- The actual first term is F(P(T)), canonically, hence projective.
The statement does NOT assert projectivity of higher terms. -/
theorem cechTerm_zero_projective (T : Profinite.{u}) :
    Projective (cechTerm T 0) := by
  have h : Projective
      ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) :=
    freeStoneanPresentation_source_projective T
  let i : cechTerm T 0 ≅
      ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) :=
    (Condensed.profiniteFree Coeff).mapIso
      (uniformRelationProjection0Iso (P T) T (p T))
  exact Projective.of_iso i.symm h

/-- The entire augmented exactness produces the true first syzygy
short exact sequence with projective middle C₀. -/
theorem cechAug_shortExact (T : Profinite.{u}) :
    (ShortComplex.mk (cechSyzygyι T 0) (cechAug T)
      (kernel.condition (cechAug T))).ShortExact := by
  letI : Epi (cechAug T) :=
    uniformFreeStoneanRelationAugmentation_epi T
  change (ShortComplex.mk
    (kernel.ι (cechAug T)) (cechAug T)
    (kernel.condition (cechAug T))).ShortExact
  exact ShortComplex.ShortExact.mk
    (ShortComplex.exact_kernel (cechAug T))

private abbrev GS (S : Profinite.{u}) : Ambient :=
  (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S

/-- The actual augmented Čech resolution and all-degree genuine
solid-target Hom exactness together provide a NONCIRCULAR
simultaneous induction: for every profinite free module and every
syzygy of its Stonean resolution, all positive Ext into the
genuine free-solid coefficient object vanish.

C₀ is projective; other terms need only be free on profinite
relations, and their current-degree vanishing is established
universally BEFORE the syzygy induction step uses it.
-/
theorem freeAndCechSyzygy_extPositive_genuineSolid_zero
    (q : ℕ) :
    (∀ (T S : Profinite.{u}),
      ∀ e : Abelian.Ext
        ((Condensed.profiniteFree Coeff).obj T) (GS S) (q+1),
        e = 0) ∧
    (∀ (T S : Profinite.{u}) (n : ℕ),
      ∀ e : Abelian.Ext (cechSyzygy T n) (GS S) (q+1),
        e = 0) := by
  induction q with
  | zero =>
    constructor
    · intro T S
      exact freeProfinite_extOne_genuineSolid_vanishes T S
    · intro T S n
      exact cechSyzygy_extOne_genuineSolid_zero T S n
  | succ q ih =>
    obtain ⟨hFreePrev,hZPrev⟩ := ih
    have hFreeNext : ∀ (T S : Profinite.{u}),
        ∀ e : Abelian.Ext
          ((Condensed.profiniteFree Coeff).obj T) (GS S) (q+2),
          e = 0 := by
      intro T S
      apply shortExact_extSucc_right_zero
        _ (cechAug_shortExact T) (GS S) q
      · exact hZPrev T S 0
      · letI : Projective (cechTerm T 0) :=
          cechTerm_zero_projective T
        intro e
        exact e.eq_zero_of_projective
    refine ⟨?_, ?_⟩
    · intro T S
      simpa only [Nat.succ_eq_add_one, Nat.add_assoc] using
        hFreeNext T S
    · intro T S n
      have hZ : ∀ e : Abelian.Ext (cechSyzygy T n) (GS S) (q+2),
          e = 0 := by
        apply shortExact_extSucc_right_zero
          _ (cechSyzygy_shortExact T n) (GS S) q
        · exact hZPrev T S (n+1)
        · exact hFreeNext
            (uniformRelationProfinite (P T) T (p T) (n+1)) S
      simpa only [Nat.succ_eq_add_one, Nat.add_assoc] using hZ

/-- **UNCONDITIONAL all-positive Ext-vanishing** from every genuine
free condensed module on a profinite source into every ACTUAL free
solid coefficient object. This is relative G_S acyclicity,
not a theorem that all profinite free modules are projective. -/
theorem freeProfinite_extPositive_genuineSolid_zero
    (T S : Profinite.{u}) (q : ℕ)
    (e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T) (GS S) (q+1)) :
    e = 0 :=
  (freeAndCechSyzygy_extPositive_genuineSolid_zero q).1 T S e

/-- Every term in the ACTUAL fully exact augmented Stonean Čech
resolution is Ext-acyclic against G_S in ALL positive degrees.
Therefore this is a valid G_S-acyclic resolution, although it is
not falsely described as a projective resolution. -/
theorem cechTerm_extPositive_genuineSolid_zero
    (T S : Profinite.{u}) (n q : ℕ)
    (e : Abelian.Ext (cechTerm T n) (GS S) (q+1)) :
    e = 0 :=
  freeProfinite_extPositive_genuineSolid_zero
    (uniformRelationProfinite (P T) T (p T) n) S q e

/-- **Final integrated certificate, in actual condensed modules.**
The augmented categorical Čech complex of the canonical Stonean
presentation is exact in every degree (including augmentation and
epi), AND every term is higher-Ext-acyclic into the genuine free-solid
coefficient object. This constitutes a VALID G_S-acyclic resolution.

This certificate does NOT claim higher Čech terms are projective.
-/
theorem uniformStoneanCech_validGSAcyclicResolution
    (T S : Profinite.{u}) :
    (∀ n : ℕ,
      (ShortComplex.mk
        (cechD T (n + 1)) (cechD T n)
        (uniformFreeRelationBoundary_sq_zero (P T) T (p T) n)).Exact) ∧
    (ShortComplex.mk
      (cechD T 0) (cechAug T)
      (uniformFreeRelationAugmentation_comp_boundary_zero
        (P T) T (p T))).Exact ∧
    Epi (cechAug T) ∧
    (∀ (n q : ℕ) (e : Abelian.Ext
      (cechTerm T n) (GS S) (q + 1)), e = 0) := by
  obtain ⟨hInternal,hZero,hEpi⟩ :=
    uniformStoneanFreeCechFullAugmentedExact T
  exact ⟨hInternal,hZero,hEpi,
    fun n q e => cechTerm_extPositive_genuineSolid_zero T S n q e⟩

#print axioms uniformStoneanCech_validGSAcyclicResolution

#print axioms cechTerm_zero_projective
#print axioms freeAndCechSyzygy_extPositive_genuineSolid_zero
#print axioms freeProfinite_extPositive_genuineSolid_zero
#print axioms cechTerm_extPositive_genuineSolid_zero
end CMDG.CondensedCM5R0
