import CMDGCondensedCM4P3DerivedCM5R0CechRelationEpi
import CMDGCondensedCM4P3DerivedCM5R0KernelHomExtension
import Mathlib.GroupTheory.QuotientGroup.Basic

/-!
# CM5: actual Ext¹ as a quotient of Stonean-kernel functionals

For every (possibly infinite) profinite T and *every* actual
condensed ZLift-module target A, this file identifies the degree-one
Ext obstruction as the additive group of genuine morphisms K_T → A
modulo those that extend across K_T → F_{P(T)}.

This strengthens the previous all-or-nothing Ext¹-vanishing criterion:
there is an explicit, surjective additive obstruction homomorphism
Hom(K_T,A) →+ Ext¹(F_T,A), its kernel consists *exactly* of the
extendable genuine kernel morphisms, and consequently the quotient by
that kernel is additively isomorphic to the actual Ext¹ group.

The existing Stonean Čech relation-to-kernel epi also makes the
associated genuine relation-functional assignment injective. Hence
the quotient only involves the relation functionals arising from
actual K_T morphisms, not arbitrary free-set cocycles.

No assertion that this quotient is zero, no finite-stage factorization
of arbitrary solid sections, and no derived solidity is made.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The concrete additive connecting homomorphism from actual kernel
morphisms to the genuine Ext¹ group of F_T, with no finite T hypothesis. -/
noncomputable def stoneanKernelHomObstructionAddHom
    (T : Profinite.{u}) (A : Ambient) :
    (stoneanPresentationKernel T ⟶ A) →+
      Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A 1 := by
  refine AddMonoidHom.mk'
    (fun f => stoneanKernelExtOneObstruction T A (Abelian.Ext.mk₀ f)) ?_
  intro f g
  simp only [stoneanKernelExtOneObstruction, Abelian.Ext.mk₀_add,
    Abelian.Ext.comp_add]

/-- The obstruction map is surjective: each actual Ext¹ class is
represented by a morphism from the canonical Stonean kernel. -/
theorem stoneanKernelHomObstructionAddHom_surjective
    (T : Profinite.{u}) (A : Ambient) :
    Function.Surjective (stoneanKernelHomObstructionAddHom T A) := by
  intro e
  obtain ⟨x, hx⟩ := stoneanKernelExtOneObstruction_surjective T A e
  refine ⟨Abelian.Ext.addEquiv₀ x, ?_⟩
  change stoneanKernelExtOneObstruction T A
    (Abelian.Ext.mk₀ (Abelian.Ext.addEquiv₀ x)) = e
  simpa only [Abelian.Ext.mk₀_addEquiv₀_apply] using hx

/-- Pointwise form of the exact additive obstruction kernel:
a genuine kernel functional has zero obstruction **exactly when**
it extends to the free module on the Stonean presentation. -/
theorem stoneanKernelHomObstruction_mem_ker_iff_extends
    (T : Profinite.{u}) (A : Ambient)
    (f : stoneanPresentationKernel T ⟶ A) :
    f ∈ (stoneanKernelHomObstructionAddHom T A).ker ↔
      ∃ g : ((Condensed.profiniteFree Coeff).obj
           (Stonean.toProfinite.obj T.presentation)) ⟶ A,
        kernel.ι (freeStoneanPresentationMap T) ≫ g = f := by
  change stoneanKernelExtOneObstruction T A (Abelian.Ext.mk₀ f) = 0 ↔ _
  constructor
  · intro h
    obtain ⟨y, hy⟩ := Abelian.Ext.contravariant_sequence_exact₁
      (stoneanPresentationShortExact T) A (Abelian.Ext.mk₀ f)
      (by decide : 1 + 0 = 1) h
    refine ⟨Abelian.Ext.addEquiv₀ y, ?_⟩
    apply (Abelian.Ext.mk₀_bijective _ _).1
    calc
      Abelian.Ext.mk₀
          (kernel.ι (freeStoneanPresentationMap T) ≫
            Abelian.Ext.addEquiv₀ y) =
        (Abelian.Ext.mk₀ (kernel.ι (freeStoneanPresentationMap T))).comp
          (Abelian.Ext.mk₀ (Abelian.Ext.addEquiv₀ y)) (zero_add 0) :=
        (Abelian.Ext.mk₀_comp_mk₀ _ _).symm
      _ = (Abelian.Ext.mk₀
          (kernel.ι (freeStoneanPresentationMap T))).comp y (zero_add 0) := by
        rw [Abelian.Ext.mk₀_addEquiv₀_apply]
      _ = Abelian.Ext.mk₀ f := hy
  · rintro ⟨g, hg⟩
    have hy : (Abelian.Ext.mk₀
        (kernel.ι (freeStoneanPresentationMap T))).comp
          (Abelian.Ext.mk₀ g) (zero_add 0) = Abelian.Ext.mk₀ f := by
      simpa only [Abelian.Ext.mk₀_comp_mk₀] using
        congrArg Abelian.Ext.mk₀ hg
    unfold stoneanKernelExtOneObstruction
    rw [← hy]
    exact (stoneanPresentationShortExact T).extClass_comp_assoc
      (Abelian.Ext.mk₀ g)

/-- Explicit canonical additive equivalence: Ext¹(F_T,A) is Hom(K_T,A)
modulo the subgroup of extendable functionals. The denominator is
defined as the genuine kernel of the proven additive connecting map,
and its members are characterized in the preceding theorem. -/
noncomputable def freeProfiniteExtOneEquivKernelHomQuotient
    (T : Profinite.{u}) (A : Ambient) :
    ((stoneanPresentationKernel T ⟶ A) ⧸
      (stoneanKernelHomObstructionAddHom T A).ker) ≃+
        Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A 1 :=
  QuotientAddGroup.quotientKerEquivOfSurjective
    (stoneanKernelHomObstructionAddHom T A)
    (stoneanKernelHomObstructionAddHom_surjective T A)

/-- The additive quotient sends a kernel functional's class to
its actual connecting Ext¹ obstruction. -/
theorem freeProfiniteExtOneEquivKernelHomQuotient_mk
    (T : Profinite.{u}) (A : Ambient)
    (f : stoneanPresentationKernel T ⟶ A) :
    freeProfiniteExtOneEquivKernelHomQuotient T A
        (f : (stoneanPresentationKernel T ⟶ A) ⧸
          (stoneanKernelHomObstructionAddHom T A).ker) =
      stoneanKernelHomObstructionAddHom T A f := by
  rfl

/-- The true Čech-relation functional remembers the entire underlying
kernel functional because the proven relation-to-kernel map is epi.
In particular, we never quotient all arbitrary cochains without
imposing the kernel-induced relation condition. -/
theorem stoneanCechKernelFunctional_injective
    (T : Profinite.{u}) (A : Ambient) :
    Function.Injective
      (fun f : stoneanPresentationKernel T ⟶ A =>
        stoneanCechRelationToKernel T ≫ f) := by
  intro f g h
  letI : Epi (stoneanCechRelationToKernel T) :=
    stoneanCechRelationToKernel_epi T
  exact (cancel_epi (stoneanCechRelationToKernel T)).1 h

#print axioms stoneanKernelHomObstructionAddHom
#print axioms stoneanKernelHomObstructionAddHom_surjective
#print axioms stoneanKernelHomObstruction_mem_ker_iff_extends
#print axioms freeProfiniteExtOneEquivKernelHomQuotient
#print axioms freeProfiniteExtOneEquivKernelHomQuotient_mk
#print axioms stoneanCechKernelFunctional_injective

end CMDG.CondensedCM5R0
