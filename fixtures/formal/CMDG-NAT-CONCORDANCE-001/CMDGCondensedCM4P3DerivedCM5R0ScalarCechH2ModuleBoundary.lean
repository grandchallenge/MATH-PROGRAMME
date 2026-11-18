import CMDGCondensedCM4P3DerivedCM5R0CategoricalScalarH2Potential
import CMDGCondensedCM4P3DerivedCM5R0DiscreteProductCechDifferential
import CMDGCondensedCM4P3DerivedCM5R0GSCechTripleBoundary

/-!
# CMDG CM5 — scalar categorical Čech H² primitives as true module morphisms

For arbitrary profinite T, the exact genuine alternating second
Čech boundary d₂:F_Q→F_R acts on morphisms F_R→Z_disc by the sign
convention [x,z]-[x,y]-[y,z]. We verify this through the existing
free-profinite Hom ↔ locally constant scalar function equivalence,
using the actual categorical triple and pair point constructors.

Any morphism F_Q→Z_disc whose scalar 2-cochain satisfies the exact
alternating four-point identity has a preimage along d₂. The primitive
constructed by the categorical scalar H² theorem is NEGATED because
the chain boundary sign convention is -δ for the cochain differential.
The same result holds for arbitrary indexed products of discrete
integer coefficient sheaves, coordinatewise, with no common finite
observation required.

The universal four-point identity for cochains induced by maps
L_T→G_S is a distinct obligation, not assumed to be settled here.
In particular these proofs do NOT claim unconditional Ext² vanishing
or full derived solidity.
-/

noncomputable section

universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem stoneanCechTripleBoundary_discreteInteger_scalar
    (T : Profinite.{u})
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechPairs T)) ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechTriples T)
        (stoneanCechTripleBoundary T ≫ g) =
      ((freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T) g).comap
        (stoneanCechTripleXZ T).hom.hom -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T) g).comap
        (stoneanCechTripleXY T).hom.hom) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T) g).comap
        (stoneanCechTripleYZ T).hom.hom := by
  unfold stoneanCechTripleBoundary
  rw [Preadditive.sub_comp, Preadditive.sub_comp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_sub]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_sub]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]


theorem stoneanCechCategoricalTriple_pointsExhausted
    (T : Profinite.{u})
    (t : stoneanPresentationCechTriples T) :
    t = stoneanCechTripleOfRelated T
      ((stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom t).val.1
      ((stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom t).val.2.1
      ((stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom t).val.2.2
      ((stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom t).property.1
      ((stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom t).property.2 := by
  let A := stoneanCechExplicitTripleToAbstract T
  let B := stoneanCechCategoricalTripleToExplicitProfinite T
  have h := congrArg
    (fun f : stoneanPresentationCechTriples T ⟶
        stoneanPresentationCechTriples T => f.hom.hom t)
    (stoneanCechCategoricalTriple_roundtrip T)
  change A.hom.hom (B.hom.hom t) = t at h
  have hs := stoneanCechExplicitTripleToAbstract_ofRelated T
    (B.hom.hom t).val.1 (B.hom.hom t).val.2.1
    (B.hom.hom t).val.2.2 (B.hom.hom t).property.1
    (B.hom.hom t).property.2
  change A.hom.hom (B.hom.hom t) =
    stoneanCechTripleOfRelated T
      (B.hom.hom t).val.1 (B.hom.hom t).val.2.1
      (B.hom.hom t).val.2.2
      (B.hom.hom t).property.1 (B.hom.hom t).property.2 at hs
  exact h.symm.trans hs


theorem stoneanCechTripleBoundary_discreteInteger_scalar_atRelated
    (T : Profinite.{u})
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechPairs T)) ⟶ discreteIntegerCoeff)
    (x y z : Stonean.toProfinite.obj T.presentation)
    (hxy : (Profinite.presentation.π T).hom.hom x =
      (Profinite.presentation.π T).hom.hom y)
    (hyz : (Profinite.presentation.π T).hom.hom y =
      (Profinite.presentation.π T).hom.hom z) :
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T)
      (stoneanCechTripleBoundary T ≫ g))
        (stoneanCechTripleOfRelated T x y z hxy hyz) =
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T) g)
          (stoneanCechPairOfRelated T x z (hxy.trans hyz)) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T) g)
          (stoneanCechPairOfRelated T x y hxy) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T) g)
          (stoneanCechPairOfRelated T y z hyz) := by
  have h := congrArg (fun F : LocallyConstant
      (stoneanPresentationCechTriples T) ℤ =>
        F (stoneanCechTripleOfRelated T x y z hxy hyz))
    (stoneanCechTripleBoundary_discreteInteger_scalar T g)
  change (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T)
        (stoneanCechTripleBoundary T ≫ g))
          (stoneanCechTripleOfRelated T x y z hxy hyz) =
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T) g)
          ((stoneanCechTripleXZ T).hom.hom
            (stoneanCechTripleOfRelated T x y z hxy hyz)) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T) g)
          ((stoneanCechTripleXY T).hom.hom
            (stoneanCechTripleOfRelated T x y z hxy hyz)) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechPairs T) g)
          ((stoneanCechTripleYZ T).hom.hom
            (stoneanCechTripleOfRelated T x y z hxy hyz)) at h
  rw [stoneanCechTripleOfRelated_xz,
    stoneanCechTripleOfRelated_xy,
    stoneanCechTripleOfRelated_yz] at h
  exact h


/-- Every integer-valued categorical Čech 2-cocycle on the genuine
free condensed-module triple is the signed second boundary of an
actual morphism from the genuine free Čech pair. -/
theorem stoneanCechSecondBoundary_integerCocycle_hasPotential
    (T : Profinite.{u})
    (h : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) ⟶ discreteIntegerCoeff)
    (hc : ∀ (x y z w : Stonean.toProfinite.obj T.presentation)
        (hxy : (Profinite.presentation.π T).hom.hom x =
          (Profinite.presentation.π T).hom.hom y)
        (hyz : (Profinite.presentation.π T).hom.hom y =
          (Profinite.presentation.π T).hom.hom z)
        (hzw : (Profinite.presentation.π T).hom.hom z =
          (Profinite.presentation.π T).hom.hom w),
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechTriples T) h)
          (stoneanCechTripleOfRelated T y z w hyz hzw) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechTriples T) h)
          (stoneanCechTripleOfRelated T x z w (hxy.trans hyz) hzw) +
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechTriples T) h)
          (stoneanCechTripleOfRelated T x y w hxy (hyz.trans hzw)) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechTriples T) h)
          (stoneanCechTripleOfRelated T x y z hxy hyz) = 0) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechPairs T)) ⟶ discreteIntegerCoeff,
      stoneanCechTripleBoundary T ≫ g = h := by
  let eqQ := freeProfiniteDiscreteIntegerHomScalarEquiv
    (stoneanPresentationCechTriples T)
  let eqR := freeProfiniteDiscreteIntegerHomScalarEquiv
    (stoneanPresentationCechPairs T)
  obtain ⟨b, hb⟩ :=
    integerStoneanCechCategoricalTwoCocycle_hasPairPotential
      T (eqQ h) hc
  let g := eqR.symm (-b)
  have hg : eqR g = -b := eqR.apply_symm_apply (-b)
  refine ⟨g, ?_⟩
  apply eqQ.injective
  ext t
  let q := (stoneanCechCategoricalTripleToExplicitProfinite T).hom.hom t
  let x := q.val.1
  let y := q.val.2.1
  let z := q.val.2.2
  let hxy := q.property.1
  let hyz := q.property.2
  have ht := stoneanCechCategoricalTriple_pointsExhausted T t
  change t = stoneanCechTripleOfRelated T x y z hxy hyz at ht
  rw [ht]
  have hd := stoneanCechTripleBoundary_discreteInteger_scalar_atRelated
    T g x y z hxy hyz
  rw [hg] at hd
  change eqQ (stoneanCechTripleBoundary T ≫ g)
      (stoneanCechTripleOfRelated T x y z hxy hyz) =
      -(b (stoneanCechPairOfRelated T x z (hxy.trans hyz))) -
      (-(b (stoneanCechPairOfRelated T x y hxy))) -
      (-(b (stoneanCechPairOfRelated T y z hyz))) at hd
  have hb' := hb x y z hxy hyz
  change eqQ h (stoneanCechTripleOfRelated T x y z hxy hyz) =
    b (stoneanCechPairOfRelated T y z hyz) -
    b (stoneanCechPairOfRelated T x z (hxy.trans hyz)) +
    b (stoneanCechPairOfRelated T x y hxy) at hb'
  change eqQ (stoneanCechTripleBoundary T ≫ g)
      (stoneanCechTripleOfRelated T x y z hxy hyz) =
    eqQ h (stoneanCechTripleOfRelated T x y z hxy hyz)
  omega

#print axioms stoneanCechTripleBoundary_discreteInteger_scalar
#print axioms stoneanCechCategoricalTriple_pointsExhausted


/-- The exact four-point scalar Čech cocycle condition on a genuine
module morphism out of the categorical Čech triple. -/
def integerCechTwoCocycleCondition
    (T : Profinite.{u})
    (h : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) ⟶ discreteIntegerCoeff) : Prop :=
  ∀ (x y z w : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z)
      (hzw : (Profinite.presentation.π T).hom.hom z =
        (Profinite.presentation.π T).hom.hom w),
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T) h)
        (stoneanCechTripleOfRelated T y z w hyz hzw) -
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T) h)
        (stoneanCechTripleOfRelated T x z w (hxy.trans hyz) hzw) +
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T) h)
        (stoneanCechTripleOfRelated T x y w hxy (hyz.trans hzw)) -
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T) h)
        (stoneanCechTripleOfRelated T x y z hxy hyz) = 0

/-- Coordinatewise scalar H² acyclicity extends through an arbitrary
(including infinite) categorical product of discrete integer targets,
with NO uniform finite observation of the coordinate family. -/
theorem stoneanCechSecondBoundary_integerProductCocycle_hasPotential
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (h : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hc : ∀ i : ι,
      integerCechTwoCocycleCondition T
        (h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechPairs T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
      stoneanCechTripleBoundary T ≫ g = h := by
  have hAll : ∀ i : ι,
      ∃ gi : ((Condensed.profiniteFree Coeff).obj
          (stoneanPresentationCechPairs T)) ⟶ discreteIntegerCoeff,
        stoneanCechTripleBoundary T ≫ gi =
          h ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i := by
    intro i
    exact stoneanCechSecondBoundary_integerCocycle_hasPotential
      T _ (hc i)
  choose gi hgi using hAll
  refine ⟨Pi.lift gi, ?_⟩
  apply Pi.hom_ext
  intro i
  rw [Category.assoc, Pi.lift_π]
  exact hgi i

#print axioms stoneanCechTripleBoundary_discreteInteger_scalar_atRelated
#print axioms stoneanCechSecondBoundary_integerCocycle_hasPotential
#print axioms stoneanCechSecondBoundary_integerProductCocycle_hasPotential

end CMDG.CondensedCM5R0
