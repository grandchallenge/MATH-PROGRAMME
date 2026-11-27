import CMDGCondensedCM4P3DerivedCM5R0CompactCoverAugmentation
import CMDGCondensedCM4P3DerivedCM5R0UniformGenuineSolidExtAcyclic

/-! Acyclicity for the genuine scalar coefficient follows by an actual
retract of the protected solid coefficient product. Hence every
relation term of the compact cover is scalar Ext-acyclic, even
though the compact target itself need not be profinite. -/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.CompactCover

theorem basisIndexNonempty (S : Profinite.{u}) (x : S) :
    Nonempty (LiftedSourceBasisIndex S) := by
  by_contra h
  let b := liftedSourceBasis S
  have hrepr : b.repr (1 : LocallyConstant S Coeff) = b.repr 0 := by
    ext i
    exact (h ⟨i⟩).elim
  have hzero : (1 : LocallyConstant S Coeff) = 0 := b.repr.injective hrepr
  have hval := congrArg (fun f : LocallyConstant S Coeff => f x) hzero
  change (1 : Coeff) = 0 at hval
  exact one_ne_zero hval

abbrev GS (S : Profinite.{u}) : Ambient :=
  (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S

def scalarInclusion (S : Profinite.{u}) : discreteIntegerCoeff.{u} ⟶ GS S :=
  Pi.lift (fun _ : LiftedSourceBasisIndex S => 𝟙 discreteIntegerCoeff.{u}) ≫
    (gsFreeSolidToCoefficientProductIso S).inv

def scalarProjection (S : Profinite.{u}) (i : LiftedSourceBasisIndex S) :
    GS S ⟶ discreteIntegerCoeff.{u} :=
  (gsFreeSolidToCoefficientProductIso S).hom ≫
    Pi.π (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u}) i

theorem scalar_retract (S : Profinite.{u}) (i : LiftedSourceBasisIndex S) :
    scalarInclusion S ≫ scalarProjection S i = 𝟙 _ := by
  unfold scalarInclusion scalarProjection
  simp only [Category.assoc,Iso.inv_hom_id_assoc,Pi.lift_π]

theorem freeProfinite_extPositive_scalar_zero
    (T : Profinite.{u}) (q : ℕ)
    (e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      discreteIntegerCoeff.{u} (q+1)) : e=0 := by
  let S : Profinite.{u} := Profinite.of (PUnit : Type u)
  let i := Classical.choice (basisIndexNonempty S (show S from PUnit.unit))
  have hz := freeProfinite_extPositive_genuineSolid_zero T S q
    (e.comp (Abelian.Ext.mk₀ (scalarInclusion S)) (add_zero (q+1)))
  have hh : (e.comp (Abelian.Ext.mk₀ (scalarInclusion S)) (add_zero (q+1))).comp
        (Abelian.Ext.mk₀ (scalarProjection S i)) (add_zero (q+1)) = e := by
    rw [Abelian.Ext.comp_assoc_of_second_deg_zero,Abelian.Ext.mk₀_comp_mk₀,
      scalar_retract,Abelian.Ext.comp_mk₀_id]
  rw [← hh,hz,Abelian.Ext.zero_comp]

/-- Valid scalar-Ext-acyclic augmented resolution for the actual
free condensed module on the compact Hausdorff target. -/
theorem compactCover_scalarAcyclicResolution (P : Profinite.{u})
    (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T) [Epi p] :
    (∀ n : ℕ, (ShortComplex.mk
      (compactFreeRelationBoundary P T p (n+1))
      (compactFreeRelationBoundary P T p n)
      (compactFreeRelationBoundary_sq_zero P T p n)).Exact) ∧
    (ShortComplex.mk (compactFreeRelationBoundary P T p 0)
      (compactFreeRelationAugmentation P T p)
      (compactFreeRelationAugmentation_comp_boundary_zero P T p)).Exact ∧
    Epi (compactFreeRelationAugmentation P T p) ∧
    (∀ n q : ℕ, ∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj (compactRelationProfinite P T p n))
      discreteIntegerCoeff.{u} (q+1), e=0) := by
  exact ⟨compactFreeCechInternalExact P T p,
    compactFreeCechAugmentationExact P T p,
    compactFreeCechAugmentationEpi P T p,
    fun n q e => freeProfinite_extPositive_scalar_zero _ q e⟩

#print axioms basisIndexNonempty
#print axioms scalar_retract
#print axioms freeProfinite_extPositive_scalar_zero
#print axioms compactCover_scalarAcyclicResolution
end CMDG.CondensedCM5R0.CompactCover
