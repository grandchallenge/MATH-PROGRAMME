import CMDGCondensedCM4P3DerivedCM5R0ExtOneObstructionQuotient

/-!
# CM5: the genuine induced Čech-cochain obstruction group

The previous exact quotient theorem describes Ext¹(F_T,A) using
morphisms K_T → A. This module makes that obstruction visible on the
*actual Stonean Čech relation object* for arbitrary profinite T.

Only cochains induced by genuine kernel morphisms K_T → A are admitted
as numerator. The denominator consists of real Čech differences of
genuine condensed-module potentials F_{P(T)} → A. Their additive
quotient is proved isomorphic to the actual Yoneda Ext¹ group.

This is not a quotient of ALL arbitrary Čech 1-cochains, which need
not satisfy the kernel-induced cocycle/descent condition. No claim
about universal finite-stage factorization, inverse-limit descent,
Ext¹ vanishing, or derived solidity is asserted.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The actual additive map from kernel morphisms to their induced
Čech relation cochains, on the exact profinite fiber-product object. -/
noncomputable def kernelInducedCechAddHom
    (T : Profinite.{u}) (A : Ambient) :
    (stoneanPresentationKernel T ⟶ A) →+
      (((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechPairs T)) ⟶ A) := by
  refine AddMonoidHom.mk'
    (fun f => stoneanCechRelationToKernel T ≫ f) ?_
  intro f g
  exact Preadditive.comp_add _ _ _

/-- Genuine Čech cochains in the image of kernel functionals.
This is intentionally a subgroup, not all free-module cochains. -/
noncomputable def kernelInducedCechCochains
    (T : Profinite.{u}) (A : Ambient) :
    AddSubgroup (((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechPairs T)) ⟶ A) :=
  (kernelInducedCechAddHom T A).range

/-- Since the actual Čech relation map is epi, a genuine induced
Čech cochain uniquely determines its source kernel functional.
Thus the kernel Hom group and induced-cochain subgroup are additively
equivalent, not merely equinumerous sets. -/
noncomputable def kernelHomEquivInducedCechCochains
    (T : Profinite.{u}) (A : Ambient) :
    (stoneanPresentationKernel T ⟶ A) ≃+
      kernelInducedCechCochains T A := by
  apply AddEquiv.ofBijective (kernelInducedCechAddHom T A).rangeRestrict
  constructor
  · intro f g h
    apply stoneanCechKernelFunctional_injective T A
    exact congrArg Subtype.val h
  · intro c
    obtain ⟨f, hf⟩ := c.property
    refine ⟨f, ?_⟩
    apply Subtype.ext
    exact hf

/-- Actual coboundary homomorphism: each genuine module potential
F_{P(T)} → A produces an induced relation cochain via the true Čech
difference, not by an invented finite-set pointwise formula. -/
noncomputable def genuineCechBoundaryAddHom
    (T : Profinite.{u}) (A : Ambient) :
    (((Condensed.profiniteFree Coeff).obj
      (Stonean.toProfinite.obj T.presentation)) ⟶ A) →+
      kernelInducedCechCochains T A := by
  refine AddMonoidHom.mk'
    (fun g => ⟨stoneanCechDifference T ≫ g, ?_⟩) ?_
  · change ∃ f : stoneanPresentationKernel T ⟶ A,
        kernelInducedCechAddHom T A f =
          stoneanCechDifference T ≫ g
    refine ⟨kernel.ι (freeStoneanPresentationMap T) ≫ g, ?_⟩
    change stoneanCechRelationToKernel T ≫
      (kernel.ι (freeStoneanPresentationMap T) ≫ g) =
      stoneanCechDifference T ≫ g
    rw [← Category.assoc, stoneanCechRelationToKernel_comp_ι]
  · intro g h
    apply Subtype.ext
    exact Preadditive.comp_add _ _ _

/-- The obstruction on genuine induced Čech cochains. This is
well-defined and additive because each such cochain has a unique
kernel-functional origin. -/
noncomputable def inducedCechObstructionAddHom
    (T : Profinite.{u}) (A : Ambient) :
    kernelInducedCechCochains T A →+
      Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A 1 :=
  (stoneanKernelHomObstructionAddHom T A).comp
    (kernelHomEquivInducedCechCochains T A).symm.toAddMonoidHom

/-- Every Ext¹ class has a genuine kernel-induced Čech representative. -/
theorem inducedCechObstructionAddHom_surjective
    (T : Profinite.{u}) (A : Ambient) :
    Function.Surjective (inducedCechObstructionAddHom T A) := by
  intro e
  obtain ⟨f, hf⟩ :=
    stoneanKernelHomObstructionAddHom_surjective T A e
  refine ⟨kernelHomEquivInducedCechCochains T A f, ?_⟩
  change stoneanKernelHomObstructionAddHom T A
    ((kernelHomEquivInducedCechCochains T A).symm
      (kernelHomEquivInducedCechCochains T A f)) = e
  simpa only [AddEquiv.symm_apply_apply] using hf

/-- Every genuine boundary has zero Ext¹ obstruction. -/
theorem genuineCechBoundary_obstruction_zero
    (T : Profinite.{u}) (A : Ambient)
    (g : ((Condensed.profiniteFree Coeff).obj
      (Stonean.toProfinite.obj T.presentation)) ⟶ A) :
    inducedCechObstructionAddHom T A
      (genuineCechBoundaryAddHom T A g) = 0 := by
  let f : stoneanPresentationKernel T ⟶ A :=
    kernel.ι (freeStoneanPresentationMap T) ≫ g
  have hc : (kernelHomEquivInducedCechCochains T A) f =
      genuineCechBoundaryAddHom T A g := by
    apply Subtype.ext
    change stoneanCechRelationToKernel T ≫
      (kernel.ι (freeStoneanPresentationMap T) ≫ g) =
      stoneanCechDifference T ≫ g
    rw [← Category.assoc, stoneanCechRelationToKernel_comp_ι]
  rw [← hc]
  change stoneanKernelHomObstructionAddHom T A
    ((kernelHomEquivInducedCechCochains T A).symm
      ((kernelHomEquivInducedCechCochains T A) f)) = 0
  rw [AddEquiv.symm_apply_apply]
  apply (stoneanKernelHomObstruction_mem_ker_iff_extends T A f).2
  exact ⟨g, rfl⟩

/-- Exactness at induced Čech cochains: the kernel of the true Ext¹
obstruction is *precisely* the subgroup of genuine Čech boundaries.
No arbitrary cochain is asserted to be a boundary. -/
theorem inducedCechObstruction_ker_eq_boundary_range
    (T : Profinite.{u}) (A : Ambient) :
    (inducedCechObstructionAddHom T A).ker =
      (genuineCechBoundaryAddHom T A).range := by
  ext c
  constructor
  · intro hc
    let f : stoneanPresentationKernel T ⟶ A :=
      (kernelHomEquivInducedCechCochains T A).symm c
    have hf : f ∈ (stoneanKernelHomObstructionAddHom T A).ker := by
      change stoneanKernelHomObstructionAddHom T A f = 0
      exact hc
    obtain ⟨g, hg⟩ :=
      (stoneanKernelHomObstruction_mem_ker_iff_extends T A f).1 hf
    refine ⟨g, ?_⟩
    apply Subtype.ext
    have heq : c.val = stoneanCechRelationToKernel T ≫ f := by
      have he :=
        (kernelHomEquivInducedCechCochains T A).apply_symm_apply c
      exact congrArg Subtype.val he.symm
    change stoneanCechDifference T ≫ g = c.val
    calc
      stoneanCechDifference T ≫ g =
          (stoneanCechRelationToKernel T ≫
            kernel.ι (freeStoneanPresentationMap T)) ≫ g := by
              rw [stoneanCechRelationToKernel_comp_ι]
      _ = stoneanCechRelationToKernel T ≫
          (kernel.ι (freeStoneanPresentationMap T) ≫ g) :=
            Category.assoc _ _ _
      _ = stoneanCechRelationToKernel T ≫ f := by rw [hg]
      _ = c.val := heq.symm
  · rintro ⟨g, hg⟩
    change inducedCechObstructionAddHom T A c = 0
    rw [← hg]
    exact genuineCechBoundary_obstruction_zero T A g

/-- The concrete Čech obstruction cohomology group: genuinely
kernel-induced cochains modulo genuinely realized Čech boundaries. -/
noncomputable def inducedCechCohomology
    (T : Profinite.{u}) (A : Ambient) :=
  kernelInducedCechCochains T A ⧸
    (genuineCechBoundaryAddHom T A).range

/-- The actual CM5 degree-one Ext group is canonically additively
equivalent to the genuine induced Čech obstruction quotient.
This is a full group identification for every profinite T and
every ambient target A; it does NOT show the group is trivial. -/
noncomputable def inducedCechCohomologyEquivExtOne
    (T : Profinite.{u}) (A : Ambient) :
    inducedCechCohomology T A ≃+
      Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A 1 := by
  unfold inducedCechCohomology
  rw [← inducedCechObstruction_ker_eq_boundary_range T A]
  exact QuotientAddGroup.quotientKerEquivOfSurjective
    (inducedCechObstructionAddHom T A)
    (inducedCechObstructionAddHom_surjective T A)

#print axioms kernelInducedCechAddHom
#print axioms kernelHomEquivInducedCechCochains
#print axioms genuineCechBoundaryAddHom
#print axioms inducedCechObstructionAddHom_surjective
#print axioms genuineCechBoundary_obstruction_zero
#print axioms inducedCechObstruction_ker_eq_boundary_range
#print axioms inducedCechCohomologyEquivExtOne

end CMDG.CondensedCM5R0
