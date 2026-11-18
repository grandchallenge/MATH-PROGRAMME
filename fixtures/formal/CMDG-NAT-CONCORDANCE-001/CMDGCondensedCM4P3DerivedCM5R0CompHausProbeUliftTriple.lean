import CMDGCondensedCM4P3DerivedCM5R0CompHausProbeUliftPair

/-!
# CMDG CM5 — universe-lifted compatible triples and signed Čech faces

The genuine represented condensed-set presheaf evaluates CompHaus Hom sets
after ULift. This module identifies the universe lift of compatible triples
with the *same* compatible-triple type used by the split free Čech complex
and verifies each of the three face maps before free-module transport.

This is an algebraic comparison, not yet the comparison of the actual
CompHaus representable of the profinite triple Q, and does not establish
global exactness or higher Ext vanishing.
-/

noncomputable section

universe u

open CategoryTheory

namespace CMDG.CondensedCM5R0

/-- The universe-lifted function with its codomain universe explicitly fixed. -/
def uliftFunction {A B : Type u} (f : A → B) :
    ULift.{u + 1} A → ULift.{u + 1} B :=
  fun z => ULift.up (f z.down)

/-- Universe lift commutes with genuine triple compatibility, with
the exact pair of equations used in the signed Čech d₂. -/
def uliftCompatibleTripleEquiv {A B : Type u} (f : A → B) :
    ULift.{u + 1}
      {xyz : A × (A × A) //
        f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2} ≃
      splitFreeCechTriple (uliftFunction f) where
  toFun z := ⟨(ULift.up z.down.1.1,
      (ULift.up z.down.1.2.1, ULift.up z.down.1.2.2)),
    ⟨congrArg ULift.up z.down.2.1,
      congrArg ULift.up z.down.2.2⟩⟩
  invFun z := ULift.up ⟨(z.1.1.down, (z.1.2.1.down, z.1.2.2.down)),
    ⟨congrArg ULift.down z.2.1, congrArg ULift.down z.2.2⟩⟩
  left_inv := by
    rintro ⟨⟨⟨a, ⟨b, c⟩⟩, h⟩⟩
    rfl
  right_inv := by
    intro z
    apply Subtype.ext
    apply Prod.ext
    · exact ULift.up_down z.1.1
    · apply Prod.ext
      · exact ULift.up_down z.1.2.1
      · exact ULift.up_down z.1.2.2

/-- The equivalence sends the (x,y) face to the actual split Čech XY face. -/
theorem uliftCompatibleTripleEquiv_xy {A B : Type u}
    (f : A → B)
    (z : ULift.{u + 1}
      {xyz : A × (A × A) //
        f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2}) :
    (splitFreeCechTripleXY
      (uliftFunction f))
      (uliftCompatibleTripleEquiv f z) =
      ⟨(ULift.up z.down.1.1, ULift.up z.down.1.2.1),
        congrArg ULift.up z.down.2.1⟩ := by
  rfl

/-- The equivalence sends the (x,z) face to the actual split Čech XZ face. -/
theorem uliftCompatibleTripleEquiv_xz {A B : Type u}
    (f : A → B)
    (z : ULift.{u + 1}
      {xyz : A × (A × A) //
        f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2}) :
    (splitFreeCechTripleXZ
      (uliftFunction f))
      (uliftCompatibleTripleEquiv f z) =
      ⟨(ULift.up z.down.1.1, ULift.up z.down.1.2.2),
        congrArg ULift.up z.down.2.2⟩ := by
  rfl

/-- The equivalence sends the (y,z) face to the actual split Čech YZ face. -/
theorem uliftCompatibleTripleEquiv_yz {A B : Type u}
    (f : A → B)
    (z : ULift.{u + 1}
      {xyz : A × (A × A) //
        f xyz.1 = f xyz.2.1 ∧ f xyz.1 = f xyz.2.2}) :
    (splitFreeCechTripleYZ
      (uliftFunction f))
      (uliftCompatibleTripleEquiv f z) =
      ⟨(ULift.up z.down.1.2.1, ULift.up z.down.1.2.2),
        (congrArg ULift.up z.down.2.1).symm.trans
          (congrArg ULift.up z.down.2.2)⟩ := by
  rfl

#print axioms uliftCompatibleTripleEquiv
#print axioms uliftCompatibleTripleEquiv_xy
#print axioms uliftCompatibleTripleEquiv_xz
#print axioms uliftCompatibleTripleEquiv_yz

end CMDG.CondensedCM5R0
