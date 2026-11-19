import CMDGCondensedCM4P3DerivedCM5R0SplitFreeCechDegreeFour
import CMDGCondensedCM4P3DerivedCM5R0QuintupleProbeComparison

/-!
# CM5: universe-correct sixfold compatible tuple comparison

A bounded next step toward represented sixth Čech Stonean probe
exactness. All equivalences transport genuine six-vertex fibre
conditions. This is not yet the sheafified global epi.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- The sixfold compatible relation commutes with universe lift.
This allows the actual CompHaus represented probes to be compared
to the split-set sixfold free-module complex. -/
def uliftCompatibleSextupleEquiv {A B : Type u} (f : A → B) :
    ULift.{u + 1} {q : A × (A × (A × (A × (A × A)))) //
      f q.1 = f q.2.1 ∧
      f q.1 = f q.2.2.1 ∧
      f q.1 = f q.2.2.2.1 ∧
      f q.1 = f q.2.2.2.2.1 ∧
      f q.1 = f q.2.2.2.2.2} ≃
      splitFreeCechSextuple (uliftFunction f) where
  toFun z :=
    ⟨(ULift.up z.down.1.1,
      (ULift.up z.down.1.2.1,
        (ULift.up z.down.1.2.2.1,
          (ULift.up z.down.1.2.2.2.1,
            (ULift.up z.down.1.2.2.2.2.1,
              ULift.up z.down.1.2.2.2.2.2))))),
      ⟨congrArg ULift.up z.down.2.1,
        congrArg ULift.up z.down.2.2.1,
        congrArg ULift.up z.down.2.2.2.1,
        congrArg ULift.up z.down.2.2.2.2.1,
        congrArg ULift.up z.down.2.2.2.2.2⟩⟩
  invFun z := ULift.up
    ⟨(z.1.1.down,
      (z.1.2.1.down,
        (z.1.2.2.1.down,
          (z.1.2.2.2.1.down,
            (z.1.2.2.2.2.1.down,
              z.1.2.2.2.2.2.down))))),
      ⟨congrArg ULift.down z.2.1,
        congrArg ULift.down z.2.2.1,
        congrArg ULift.down z.2.2.2.1,
        congrArg ULift.down z.2.2.2.2.1,
        congrArg ULift.down z.2.2.2.2.2⟩⟩
  left_inv := by
    rintro ⟨⟨⟨a, ⟨b, ⟨c, ⟨d,⟨e,g⟩⟩⟩⟩⟩, h⟩⟩
    rfl
  right_inv := by
    intro z
    apply Subtype.ext
    apply Prod.ext
    · exact ULift.up_down z.1.1
    · apply Prod.ext
      · exact ULift.up_down z.1.2.1
      · apply Prod.ext
        · exact ULift.up_down z.1.2.2.1
        · apply Prod.ext
          · exact ULift.up_down z.1.2.2.2.1
          · apply Prod.ext
            · exact ULift.up_down z.1.2.2.2.2.1
            · exact ULift.up_down z.1.2.2.2.2.2


/-- The next compatible fibre product is the sixfold equal-image
relation, with all six vertices and no assumption of finite fibres. -/
def compatibleNestedSextupleEquiv {A B R : Type u}
    (f : A → B) (g : R → B)
    (e : R ≃ {q : A × (A × (A × (A × A))) //
      f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
      f q.1 = f q.2.2.2.1 ∧ f q.1 = f q.2.2.2.2})
    (h : ∀ r, g r = f (e r).1.1) :
    {rv : R × A // g rv.1 = f rv.2} ≃
    {q : A × (A × (A × (A × (A × A)))) //
      f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
      f q.1 = f q.2.2.2.1 ∧ f q.1 = f q.2.2.2.2.1 ∧
      f q.1 = f q.2.2.2.2.2} where
  toFun z :=
    ⟨((e z.1.1).1.1,
      ((e z.1.1).1.2.1,
        ((e z.1.1).1.2.2.1,
          ((e z.1.1).1.2.2.2.1,
            ((e z.1.1).1.2.2.2.2,z.1.2))))),
      ⟨(e z.1.1).2.1,(e z.1.1).2.2.1,
        (e z.1.1).2.2.2.1,(e z.1.1).2.2.2.2,
        (h z.1.1).symm.trans z.2⟩⟩
  invFun z := by
    let q5 : {q : A × (A × (A × (A × A))) //
      f q.1 = f q.2.1 ∧ f q.1 = f q.2.2.1 ∧
      f q.1 = f q.2.2.2.1 ∧ f q.1 = f q.2.2.2.2} :=
      ⟨(z.1.1,(z.1.2.1,(z.1.2.2.1,
        (z.1.2.2.2.1,z.1.2.2.2.2.1)))),
        ⟨z.2.1,z.2.2.1,z.2.2.2.1,z.2.2.2.2.1⟩⟩
    refine ⟨(e.symm q5,z.1.2.2.2.2.2), ?_⟩
    have hr : g (e.symm q5) = f z.1.1 := by
      simpa [q5] using h (e.symm q5)
    exact hr.trans z.2.2.2.2.2
  left_inv := by
    intro z
    apply Subtype.ext
    apply Prod.ext
    · change e.symm (e z.1.1) = z.1.1
      exact e.symm_apply_apply _
    · rfl
  right_inv := by
    intro z
    apply Subtype.ext
    dsimp
    simp only [Equiv.apply_symm_apply]

#print axioms compatibleNestedSextupleEquiv
#print axioms uliftCompatibleSextupleEquiv
end CMDG.CondensedCM5R0
