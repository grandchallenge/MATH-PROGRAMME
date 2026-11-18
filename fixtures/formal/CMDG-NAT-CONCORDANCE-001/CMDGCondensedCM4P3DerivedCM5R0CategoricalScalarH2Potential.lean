import CMDGCondensedCM4P3DerivedCM5R0CategoricalTripleRelationIso
import CMDGCondensedCM4P3DerivedCM5R0DiscreteProductSections

/-!
# CMDG CM5 — scalar H² potential on the genuine categorical Čech nerve

The protected triple-point geometry and a new categorical triple-pullback
iso convert arbitrary locally constant integer 2-cocycles on the
genuine P(T)×_T P(T)×_T P(T) to the actual closed equal-image triple
relation. The proved closed-relation H² theorem supplies a primitive,
then the categorical pair-projection comparison transports it back to
P(T)×_T P(T) with exactly the alternating Čech signs.

The four-point Čech cocycle identity is a NON-VACUOUS hypothesis.
No theorem that every cochain induced from L_T → G_S satisfies it,
no condensed-module second relation extension, and no Ext² vanishing
is asserted here. Those remain distinct formal obligations.
-/

noncomputable section

universe u
open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

theorem stoneanCechCategoricalTripleToExplicit_ofRelated
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    (stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom
      (stoneanCechTripleOfRelated T x y z hxy hyz) =
        (⟨(x, (y, z)), ⟨hxy, hyz⟩⟩ :
          stoneanCechExplicitTripleProfinite T) := by
  let p := Profinite.presentation.π T
  let t := stoneanCechTripleOfRelated T x y z hxy hyz
  apply Subtype.ext
  apply Prod.ext
  · change (pullback.fst p p).hom.hom
        ((stoneanCechTripleXY T).hom.hom t) = x
    rw [stoneanCechTripleOfRelated_xy, stoneanCechPairOfRelated_fst]
  · apply Prod.ext
    · change (pullback.snd p p).hom.hom
          ((stoneanCechTripleXY T).hom.hom t) = y
      rw [stoneanCechTripleOfRelated_xy, stoneanCechPairOfRelated_snd]
    · change (stoneanCechTripleZ T).hom.hom t = z
      exact stoneanCechTripleOfRelated_z T x y z hxy hyz

/-- Source-to-categorical triple comparison sends the actual explicit
triple point to the protected categorical point constructor. -/
theorem stoneanCechExplicitTripleToAbstract_ofRelated
    (T : Profinite.{u})
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    (stoneanCechExplicitTripleToAbstract T).hom.hom
      (⟨(x, (y, z)), ⟨hxy, hyz⟩⟩ :
        stoneanCechExplicitTripleProfinite T) =
      stoneanCechTripleOfRelated T x y z hxy hyz := by
  let A := stoneanCechExplicitTripleToAbstract T
  let B := stoneanCechCategoricalTripleToExplicitProfinite T
  have hB := stoneanCechCategoricalTripleToExplicit_ofRelated
    T x y z hxy hyz
  have hcomp := congrArg A.hom.hom hB
  change A.hom.hom (B.hom.hom
      (stoneanCechTripleOfRelated T x y z hxy hyz)) =
    A.hom.hom (⟨(x, (y, z)), ⟨hxy, hyz⟩⟩ :
      stoneanCechExplicitTripleProfinite T) at hcomp
  have hAB : A.hom.hom (B.hom.hom
      (stoneanCechTripleOfRelated T x y z hxy hyz)) =
      stoneanCechTripleOfRelated T x y z hxy hyz := by
    have h := stoneanCechCategoricalTriple_roundtrip T
    have hh := congrArg
      (fun m : stoneanPresentationCechTriples T ⟶
          stoneanPresentationCechTriples T =>
        m.hom.hom (stoneanCechTripleOfRelated T x y z hxy hyz)) h
    change A.hom.hom (B.hom.hom
        (stoneanCechTripleOfRelated T x y z hxy hyz)) =
      stoneanCechTripleOfRelated T x y z hxy hyz at hh
    exact hh
  exact (hAB.symm.trans hcomp).symm


/-- Genuine categorical scalar Čech H² vanishes for cochains whose
alternating four-point cocycle identity holds on the actual
profinite Čech quadruple relation. -/
theorem integerStoneanCechCategoricalTwoCocycle_hasPairPotential
    (T : Profinite.{u})
    (c : LocallyConstant (stoneanPresentationCechTriples T) ℤ)
    (hc : ∀ (x y z w : Stonean.toProfinite.obj T.presentation)
        (hxy : (Profinite.presentation.π T).hom.hom x =
          (Profinite.presentation.π T).hom.hom y)
        (hyz : (Profinite.presentation.π T).hom.hom y =
          (Profinite.presentation.π T).hom.hom z)
        (hzw : (Profinite.presentation.π T).hom.hom z =
          (Profinite.presentation.π T).hom.hom w),
        c (stoneanCechTripleOfRelated T y z w hyz hzw) -
        c (stoneanCechTripleOfRelated T x z w (hxy.trans hyz) hzw) +
        c (stoneanCechTripleOfRelated T x y w hxy (hyz.trans hzw)) -
        c (stoneanCechTripleOfRelated T x y z hxy hyz) = 0) :
    ∃ b : LocallyConstant (stoneanPresentationCechPairs T) ℤ,
      ∀ (x y z : Stonean.toProfinite.obj T.presentation)
        (hxy : (Profinite.presentation.π T).hom.hom x =
          (Profinite.presentation.π T).hom.hom y)
        (hyz : (Profinite.presentation.π T).hom.hom y =
          (Profinite.presentation.π T).hom.hom z),
        c (stoneanCechTripleOfRelated T x y z hxy hyz) =
          b (stoneanCechPairOfRelated T y z hyz) -
          b (stoneanCechPairOfRelated T x z (hxy.trans hyz)) +
          b (stoneanCechPairOfRelated T x y hxy) := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  let C : LocallyConstant
      (↥(profiniteCechTripleRelatedSet P T p)) ℤ :=
    c.comap (stoneanCechExplicitTripleToAbstract T).hom.hom
  have hC : ∀ (x y z w : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w),
      C ⟨(y, (z, w)), ⟨hyz, hzw⟩⟩ -
      C ⟨(x, (z, w)), ⟨hxy.trans hyz, hzw⟩⟩ +
      C ⟨(x, (y, w)), ⟨hxy, hyz.trans hzw⟩⟩ -
      C ⟨(x, (y, z)), ⟨hxy, hyz⟩⟩ = 0 := by
    intro x y z w hxy hyz hzw
    change
      c ((stoneanCechExplicitTripleToAbstract T).hom.hom
          ⟨(y, (z, w)), ⟨hyz, hzw⟩⟩) -
      c ((stoneanCechExplicitTripleToAbstract T).hom.hom
          ⟨(x, (z, w)), ⟨hxy.trans hyz, hzw⟩⟩) +
      c ((stoneanCechExplicitTripleToAbstract T).hom.hom
          ⟨(x, (y, w)), ⟨hxy, hyz.trans hzw⟩⟩) -
      c ((stoneanCechExplicitTripleToAbstract T).hom.hom
          ⟨(x, (y, z)), ⟨hxy, hyz⟩⟩) = 0
    rw [stoneanCechExplicitTripleToAbstract_ofRelated,
      stoneanCechExplicitTripleToAbstract_ofRelated,
      stoneanCechExplicitTripleToAbstract_ofRelated,
      stoneanCechExplicitTripleToAbstract_ofRelated]
    exact hc x y z w hxy hyz hzw
  obtain ⟨B, hB⟩ :=
    integerProfiniteTwoCocycle_hasPotential P T p C hC
  let b : LocallyConstant (stoneanPresentationCechPairs T) ℤ :=
    B.comap (stoneanCechCategoricalPairToExplicit T)
  refine ⟨b, ?_⟩
  intro x y z hxy hyz
  have h := hB x y z hxy hyz
  change
    c (stoneanCechTripleOfRelated T x y z hxy hyz) =
      B (stoneanCechCategoricalPairToExplicit T
          (stoneanCechPairOfRelated T y z hyz)) -
      B (stoneanCechCategoricalPairToExplicit T
          (stoneanCechPairOfRelated T x z (hxy.trans hyz))) +
      B (stoneanCechCategoricalPairToExplicit T
          (stoneanCechPairOfRelated T x y hxy))
  rw [stoneanCechCategoricalPairToExplicit_ofRelated,
    stoneanCechCategoricalPairToExplicit_ofRelated,
    stoneanCechCategoricalPairToExplicit_ofRelated,
    ← stoneanCechExplicitTripleToAbstract_ofRelated]
  exact h

#print axioms stoneanCechCategoricalTripleToExplicit_ofRelated
#print axioms stoneanCechExplicitTripleToAbstract_ofRelated
#print axioms integerStoneanCechCategoricalTwoCocycle_hasPairPotential

end CMDG.CondensedCM5R0
