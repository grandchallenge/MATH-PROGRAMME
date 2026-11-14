import CMDGCondensedCM4P3DerivedCM5R0ActualCechSections
import Mathlib.Topology.Category.LightProfinite.Injective
import Mathlib.Topology.Category.Profinite.CofilteredLimit
import Mathlib.Topology.LocallyConstant.Basic
import Mathlib.CategoryTheory.Limits.Shapes.Pullback.Mono

/-!
# CM5: scalar discrete-coefficient Čech extension and finite factorization

The end goal is the *unconditional* arbitrary-profinite Ext¹(F_T,G_S)
vanishing needed for derived solidity, not another formal reformulation
of the missing Čech potential.

This source establishes a new concrete topological ingredient of the
discrete-integer route. For any injective map between profinite spaces,
every locally constant function with values in an inhabited (possibly
infinite) discrete set extends to the larger profinite space. The
finite-image factorization on compact sources reduces the general case
to the already-proved finite-discrete lifting theorem. In particular,
this applies to scalar integer coefficients on closed Čech relations.

Separately, a scalar locally constant function on the *actual* Stonean
Čech pair extends to the ambient source product, and hence factors
through a finite discrete quotient of that product (not just the pair).
This is the finite-dependence step for individual integer coordinates,
not a false uniform finite-quotient claim for arbitrary product-valued
solid sections.

Unproved future obligations: assemble scalar cocycle potentials along
the full relation, identify the true discrete condensed coefficient
sections with these locally constant functions, and construct the
protected G_S product model. We do not assert Ext¹ vanishing or derived
solidity here.
-/

noncomputable section

universe u v

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- A finite discrete-valued locally constant function extends along
every injective profinite map. This is the topological finite lifting
step, not an assumption that the injection is split. -/
theorem finiteLocallyConstant_extension_of_injective
    (X Y : Profinite.{u}) (j : X ⟶ Y)
    (hj : Function.Injective j.hom.hom)
    {A : Type v} [Finite A] [Nonempty A]
    (f : LocallyConstant X A) :
    ∃ g : LocallyConstant Y A,
      ∀ x : X, g (j.hom.hom x) = f x := by
  classical
  letI : TopologicalSpace A := ⊥
  haveI : DiscreteTopology A := ⟨rfl⟩
  haveI : T2Space A := inferInstance
  let p : A → PUnit.{u + 1} := fun _ => PUnit.unit
  let q : Y → PUnit.{u + 1} := fun _ => PUnit.unit
  have hp : Function.Surjective p := by
    intro _
    exact ⟨Classical.choice ‹Nonempty A›, rfl⟩
  have hf : Continuous (f : X → A) :=
    (IsLocallyConstant.iff_continuous _).mp f.isLocallyConstant
  have hcomm : q ∘ j.hom.hom = p ∘ (f : X → A) := rfl
  obtain ⟨g, hg, _, hgj⟩ :=
    Profinite.exists_lift_of_finite_of_injective_of_surjective
      j.hom.hom j.hom.hom.continuous hj
      p hp (f : X → A) hf q continuous_const hcomm
  refine ⟨⟨g, (IsLocallyConstant.iff_continuous _).mpr hg⟩, ?_⟩
  intro x
  exact congrFun hgj x

/-- **No finiteness assumption on the coefficient type.**
Compactness forces each individual locally constant map to have
finite image; the finite-injective lifting theorem extends that
finite image and hence the original function. This is the extension
property required for discrete integer-valued Čech cochains on
closed embedded relation spaces. -/
theorem locallyConstant_extension_of_injective
    (X Y : Profinite.{u}) (j : X ⟶ Y)
    (hj : Function.Injective j.hom.hom)
    {A : Type v} [Inhabited A]
    (f : LocallyConstant X A) :
    ∃ g : LocallyConstant Y A,
      ∀ x : X, g (j.hom.hom x) = f x := by
  classical
  by_cases hX : Nonempty X
  · let R : Type v := Set.range (f : X → A)
    haveI : Finite R := f.range_finite.to_subtype
    haveI : Nonempty R := by
      obtain ⟨x⟩ := hX
      exact ⟨⟨f x, ⟨x, rfl⟩⟩⟩
    let fR : LocallyConstant X R :=
      ⟨fun x => ⟨f x, ⟨x, rfl⟩⟩, by
        apply IsLocallyConstant.iff_isOpen_fiber.mpr
        intro z
        have hz : (fun x : X => (⟨f x, ⟨x, rfl⟩⟩ : R)) ⁻¹' {z} =
            (f : X → A) ⁻¹' {z.val} := by
          ext x
          simp only [Set.mem_preimage, Set.mem_singleton_iff]
          exact Subtype.ext_iff
        rw [hz]
        exact IsLocallyConstant.iff_isOpen_fiber.mp f.isLocallyConstant z.val⟩
    obtain ⟨gR, hgR⟩ :=
      finiteLocallyConstant_extension_of_injective X Y j hj fR
    refine ⟨gR.map Subtype.val, ?_⟩
    intro x
    exact congrArg Subtype.val (hgR x)
  · refine ⟨LocallyConstant.const Y (default : A), ?_⟩
    intro x
    exact (hX ⟨x⟩).elim

/-- Every scalar integer-valued Čech cochain on the genuine Stonean
fiber-product pair has finite-stage dependence. Its finite quotient
is of the pair object; the theorem does not promote it to a
compatible quotient of P(T), T, or an infinite product of coefficients. -/
theorem integerCechCochain_factors_finiteQuotient
    (T : Profinite.{u})
    (c : LocallyConstant (stoneanPresentationCechPairs T) ℤ) :
    ∃ (j : DiscreteQuotient (stoneanPresentationCechPairs T))
      (cQ : LocallyConstant
        ((stoneanPresentationCechPairs T).diagram.obj j) ℤ),
      c = cQ.comap
        ((stoneanPresentationCechPairs T).asLimitCone.π.app j).hom.hom := by
  exact Profinite.exists_locallyConstant
    (stoneanPresentationCechPairs T).asLimitCone
    (stoneanPresentationCechPairs T).asLimit c

/-- The ordinary profinite product of the source of the canonical
Stonean presentation with itself. -/
noncomputable abbrev stoneanPresentationPairProduct (T : Profinite.{u}) :
    Profinite.{u} :=
  (Stonean.toProfinite.obj T.presentation) ⨯
    (Stonean.toProfinite.obj T.presentation)

/-- The real Stonean Čech pair R=P×_T P embeds into the ordinary
product P×P. Its mono property is categorical and does not require
the surjection P→T to split. -/
noncomputable def stoneanCechPairEmbedding (T : Profinite.{u}) :
    stoneanPresentationCechPairs T ⟶
      stoneanPresentationPairProduct T :=
  prod.lift
    (pullback.fst (Profinite.presentation.π T) (Profinite.presentation.π T))
    (pullback.snd (Profinite.presentation.π T) (Profinite.presentation.π T))

/-- The actual Čech relation embeds injectively into the source
product, so discrete scalar cochains can be extended from the
relation to a neighbourhood-free function on the entire product. -/
theorem stoneanCechPairEmbedding_injective (T : Profinite.{u}) :
    Function.Injective (stoneanCechPairEmbedding T).hom.hom := by
  unfold stoneanCechPairEmbedding
  exact (CompHausLike.mono_iff_injective _).mp inferInstance

/-- Every scalar integer-valued locally constant cochain on
the *actual* Stonean Čech relation admits a locally constant
extension to the ambient product P(T) × P(T). This is a genuine
topological extension result and not yet a Čech coboundary. -/
theorem integerCechCochain_extend_to_product
    (T : Profinite.{u})
    (c : LocallyConstant (stoneanPresentationCechPairs T) ℤ) :
    ∃ b : LocallyConstant (stoneanPresentationPairProduct T) ℤ,
      ∀ x : stoneanPresentationCechPairs T,
        b ((stoneanCechPairEmbedding T).hom.hom x) = c x := by
  exact locallyConstant_extension_of_injective
    (stoneanPresentationCechPairs T)
    (stoneanPresentationPairProduct T)
    (stoneanCechPairEmbedding T)
    (stoneanCechPairEmbedding_injective T) c

/-- An integer-valued Čech cochain can be represented on a
finite quotient of the ambient product P(T)×P(T), not merely
on a finite quotient of R itself. This is an unconditional
finite-observation theorem for each scalar cochain. The quotient
is NOT asserted to respect the maps to T or support an
automatically coherent primitive. -/
theorem integerCechCochain_ambientFiniteObservation
    (T : Profinite.{u})
    (c : LocallyConstant (stoneanPresentationCechPairs T) ℤ) :
    ∃ (j : DiscreteQuotient (stoneanPresentationPairProduct T))
      (cQ : LocallyConstant
        ((stoneanPresentationPairProduct T).diagram.obj j) ℤ),
      ∀ x : stoneanPresentationCechPairs T,
        cQ (((stoneanPresentationPairProduct T).asLimitCone.π.app j).hom.hom
            ((stoneanCechPairEmbedding T).hom.hom x)) = c x := by
  obtain ⟨b, hb⟩ := integerCechCochain_extend_to_product T c
  let Q : Profinite.{u} := stoneanPresentationPairProduct T
  obtain ⟨j, cQ, hc⟩ :=
    Profinite.exists_locallyConstant Q.asLimitCone Q.asLimit b
  refine ⟨j, cQ, ?_⟩
  intro x
  calc
    cQ ((Q.asLimitCone.π.app j).hom.hom
        ((stoneanCechPairEmbedding T).hom.hom x)) =
      b ((stoneanCechPairEmbedding T).hom.hom x) := by
        exact (LocallyConstant.congr_fun hc
          ((stoneanCechPairEmbedding T).hom.hom x)).symm
    _ = c x := hb x

#print axioms stoneanCechPairEmbedding_injective
#print axioms integerCechCochain_extend_to_product
#print axioms integerCechCochain_ambientFiniteObservation

#print axioms finiteLocallyConstant_extension_of_injective
#print axioms locallyConstant_extension_of_injective
#print axioms integerCechCochain_factors_finiteQuotient

end CMDG.CondensedCM5R0
