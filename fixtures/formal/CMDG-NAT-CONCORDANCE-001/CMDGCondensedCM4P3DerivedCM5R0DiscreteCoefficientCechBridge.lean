import CMDGCondensedCM4P3DerivedCM5R0StoneanScalarCechPrimitive
import CMDGCondensedCM4P3DerivedCM5R0ActualCechSections
import Mathlib.Condensed.Discrete.Module

/-!
# CM5: discrete integer coefficient sections and arbitrary product Čech primitives

This is the next bounded bridge after protected scalar Čech exactness.
The actual discrete lifted-integer condensed coefficient object is represented
on a profinite test by locally constant lifted-integer functions.  Thus an
honest morphism out of a free profinite condensed module into that discrete
coefficient object has a concrete locally constant description.

For an arbitrary index type, a family of integral scalar Čech cocycles has
a family of continuous primitives, with NO common finite quotient across
indices.  This is the correct coordinatewise semantics for a categorical
product of discrete coefficient sheaves.  It does not assert that the
protected free solid object G_S is such a product, nor that an arbitrary
G_S-valued kernel functional has scalar-coordinate cocycles.

No Ext vanishing or derived solidity is claimed here.
-/

noncomputable section

universe u v

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The actual discrete lifted-integer coefficient object in the pinned
condensed-module category, not the solid target G_S. -/
noncomputable abbrev discreteIntegerCoeff : Ambient :=
  (CondensedMod.LocallyConstant.functor Coeff).obj
    (ModuleCat.of Coeff Coeff)

/-- Sections of the genuine discrete coefficient sheaf over a profinite
test are literally locally constant lifted-integer functions, through
mathlib's pinned locally constant presheaf presentation. -/
noncomputable def discreteIntegerSectionsEquiv (X : Profinite.{u}) :
    ((Condensed.forget Coeff).obj discreteIntegerCoeff).obj.obj
      (Opposite.op (profiniteToCompHaus.obj X)) ≃
        LocallyConstant X Coeff :=
  Equiv.refl _

/-- The free-forgetful and profinite Yoneda adjunction give an exact
degree-zero bridge from actual condensed-module morphisms to
locally constant lifted-integer functions. -/
noncomputable def freeProfiniteDiscreteIntegerHomEquiv
    (X : Profinite.{u}) :
    (((Condensed.profiniteFree Coeff).obj X) ⟶
      discreteIntegerCoeff) ≃ LocallyConstant X Coeff :=
  (freeProfiniteSectionsEquiv X discreteIntegerCoeff).trans
    (discreteIntegerSectionsEquiv X)

/-- The scalar Čech H¹-zero theorem extends coordinatewise to an
arbitrary, possibly infinite, family of integer-valued locally constant
cocycles, without a finite-observation assumption uniform in the
coefficient index. -/
theorem integerProfiniteCechCocycle_family_hasPotential
    (P T : Profinite.{u}) (p : P ⟶ T)
    {ι : Type v}
    (c : ι → LocallyConstant
      (↥(profiniteCechRelatedSet P T p)) ℤ)
    (hc : ∀ (i : ι) (x y z : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z),
      c i ⟨(x, z), hxy.trans hyz⟩ =
        c i ⟨(x, y), hxy⟩ + c i ⟨(y, z), hyz⟩) :
    ∃ b : ι → LocallyConstant P ℤ,
      ∀ (i : ι) (x y : P)
        (hxy : p.hom.hom x = p.hom.hom y),
        c i ⟨(x, y), hxy⟩ = b i x - b i y := by
  classical
  have hi (i : ι) :
      ∃ b : LocallyConstant P ℤ,
        ∀ (x y : P) (hxy : p.hom.hom x = p.hom.hom y),
          c i ⟨(x, y), hxy⟩ = b x - b y :=
    integerProfiniteCechCocycle_hasPotential P T p (c i) (hc i)
  choose b hb using hi
  exact ⟨b, hb⟩

/-- Coordinatewise scalar H¹ exactness also holds on the honest
categorical Stonean Čech pair of any profinite T. -/
theorem integerStoneanCechCocycle_family_hasPotential
    (T : Profinite.{u}) {ι : Type v}
    (c : ι → LocallyConstant (stoneanPresentationCechPairs T) ℤ)
    (hc : ∀ (i : ι)
      (x y z : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z),
      c i (stoneanCechPairOfRelated T x z (hxy.trans hyz)) =
        c i (stoneanCechPairOfRelated T x y hxy) +
          c i (stoneanCechPairOfRelated T y z hyz)) :
    ∃ b : ι → LocallyConstant
          (Stonean.toProfinite.obj T.presentation) ℤ,
      ∀ (i : ι)
        (x y : Stonean.toProfinite.obj T.presentation)
        (hxy : (Profinite.presentation.π T).hom.hom x =
          (Profinite.presentation.π T).hom.hom y),
        c i (stoneanCechPairOfRelated T x y hxy) =
          b i x - b i y := by
  classical
  have hi (i : ι) :
      ∃ b : LocallyConstant
          (Stonean.toProfinite.obj T.presentation) ℤ,
        ∀ (x y : Stonean.toProfinite.obj T.presentation)
          (hxy : (Profinite.presentation.π T).hom.hom x =
            (Profinite.presentation.π T).hom.hom y),
          c i (stoneanCechPairOfRelated T x y hxy) =
            b x - b y :=
    integerStoneanCechCocycle_hasPotential T (c i) (hc i)
  choose b hb using hi
  exact ⟨b, hb⟩

#print axioms discreteIntegerSectionsEquiv
#print axioms freeProfiniteDiscreteIntegerHomEquiv
#print axioms integerProfiniteCechCocycle_family_hasPotential
#print axioms integerStoneanCechCocycle_family_hasPotential

end CMDG.CondensedCM5R0
