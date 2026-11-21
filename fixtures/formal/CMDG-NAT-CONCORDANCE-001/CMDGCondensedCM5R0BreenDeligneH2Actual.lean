import CMDGCondensedCM5R0BreenDeligneH2Universal
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealPentagon
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealHexagon


/-!
# CM5: actual compact real degree-two closed-cochain homotopy

Import the universal 29-term degree-two polynomial identities and
the protected actual compact-continuous real-cochain operations.
Verify on genuine C(A^r×S,ℝ) Banach spaces the pointwise identity

  d₁ h₁(f) = 2f − [2]*f

whenever the four actual pentagon, hexagon, symmetry-involution, and
strict-diagonal differentials vanish. All four identification lemmas
are compiled against real compact-cochain operators and real
continuous maps; none is an abstract substitute for those cochains.
This does not assert completeness of the all-degree resolution or
identification with condensed derived internal Hom.
-/
noncomputable section
universe u v

namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains
open CMDG.CondensedCM5R0.BreenDeligneH2Universal

variable (A : Type u) (S : Type v)
variable [TopologicalSpace A] [CompactSpace A]
    [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]

private def fA (f : C2 A S) (s : S) : A → A → A → ℝ :=
  fun a b c => f.1 ((a,(b,c)),s)
private def fC (f : C2 A S) (s : S) : A → A → ℝ :=
  fun a b => f.2 ((a,b),s)

theorem eval_pent_zero (f : C2 A S)
    (hp : pentagonCochainDifferential A S f.1 = 0) (s : S) :
    ∀ a b c d : A, P (fA A S f s) a b c d = 0 := by
  intro a b c d
  have h := congrArg
    (fun z : C3p A S => z ((a,(b,(c,d))),s)) hp
  simpa [P,fA,pentagonCochainDifferential,
    pface0,pface1,pface2,pface3,pface4] using h

theorem eval_hex_zero (f : C2 A S)
    (hh : hexRealDifferential A S f = 0) (s : S) :
    ∀ a b c : A, H (fA A S f s) (fC A S f s) a b c = 0 := by
  intro a b c
  have h := congrArg
    (fun z : C2a A S => z ((a,(b,c)),s)) hh
  simp [hexRealDifferential,hexAssocStar,hexCommStar,
    pHexSwap,pHexRotate,pHexPair0,pHexPair1,pHexPair2] at h
  change _ = 0
  simp only [H,fA,fC,sub_eq_add_neg]
  convert h using 1 <;> abel

theorem eval_sym_zero (f : C2 A S)
    (hs : symRealDifferential A S f = 0) (s : S) :
    ∀ a b : A, BreenDeligneH2Universal.S (fC A S f s) a b = 0 := by
  intro a b
  have h := congrArg
    (fun z : C1 A S => z ((a,b),s)) hs
  simpa [BreenDeligneH2Universal.S,fC,symRealDifferential,pSwap] using h

theorem eval_diag_zero (f : C2 A S)
    (hd : diagonalRealDifferential A S f = 0) (s : S) :
    ∀ a : A, D (fC A S f s) a = 0 := by
  intro a
  have h := congrArg
    (fun z : C0 A S => z (a,s)) hd
  simpa [D,fC,diagonalRealDifferential,pDiag] using h

theorem eval_hStar1 (f : C2 A S) (s : S) (a b : A) :
    hStar1 A S f ((a,b),s) =
      h1 (fA A S f s) (fC A S f s) a b := by
  simp [hStar1,h1,fA,fC,qAssoc1,qAssoc2,qAssoc3,qComm]

theorem degreeTwo_closed_real_homotopy (f : C2 A S)
    (hp : pentagonCochainDifferential A S f.1 = 0)
    (hh : hexRealDifferential A S f = 0)
    (hs : symRealDifferential A S f = 0)
    (hd : diagonalRealDifferential A S f = 0) :
    differential1 A S (hStar1 A S f) =
      f + f - doubleStar2 A S f := by
  have heval_assoc (s : S) (a b c : A) :=
    h2Assoc_closed_identity (fA A S f s) (fC A S f s)
      (eval_pent_zero A S f hp s) (eval_hex_zero A S f hh s)
      (eval_sym_zero A S f hs s) (eval_diag_zero A S f hd s)
      a b c
  have heval_comm (s : S) (a b : A) :=
    h2Comm_closed_identity (fA A S f s) (fC A S f s)
      (eval_pent_zero A S f hp s) (eval_hex_zero A S f hh s)
      (eval_sym_zero A S f hs s) (eval_diag_zero A S f hd s)
      a b
  apply Prod.ext
  · ext p
    rcases p with ⟨⟨a, ⟨b,c⟩⟩,s⟩
    change (differential1 A S (hStar1 A S f)).1 ((a,(b,c)),s) =
      (f+f-doubleStar2 A S f).1 ((a,(b,c)),s)
    calc
      (differential1 A S (hStar1 A S f)).1 ((a,(b,c)),s) =
          h1 (fA A S f s) (fC A S f s) b c -
          h1 (fA A S f s) (fC A S f s) (a+b) c +
          h1 (fA A S f s) (fC A S f s) a (b+c) -
          h1 (fA A S f s) (fC A S f s) a b := by
            simp [differential1,pBC,pAB_C,pA_BC,pAB,
              eval_hStar1]
      _ = (fA A S f s) a b c + (fA A S f s) a b c -
            (fA A S f s) (a+a) (b+b) (c+c) :=
          heval_assoc s a b c
      _ = (f+f-doubleStar2 A S f).1 ((a,(b,c)),s) := by
          simp [fA,doubleStar2,pDouble2a]
  · ext p
    rcases p with ⟨⟨a,b⟩,s⟩
    change (differential1 A S (hStar1 A S f)).2 ((a,b),s) =
      (f+f-doubleStar2 A S f).2 ((a,b),s)
    calc
      (differential1 A S (hStar1 A S f)).2 ((a,b),s) =
          h1 (fA A S f s) (fC A S f s) a b -
          h1 (fA A S f s) (fC A S f s) b a := by
            simp [differential1,pSwap,eval_hStar1]
      _ = (fC A S f s) a b + (fC A S f s) a b -
            (fC A S f s) (a+a) (b+b) :=
          heval_comm s a b
      _ = (f+f-doubleStar2 A S f).2 ((a,b),s) := by
          simp [fC,doubleStar2,doubleStar1,pDouble1]

#print axioms degreeTwo_closed_real_homotopy

#print axioms eval_pent_zero
#print axioms eval_hex_zero
#print axioms eval_sym_zero
#print axioms eval_diag_zero
#print axioms eval_hStar1
end CMDG.CondensedCM5R0.BreenDeligneRealCochains
