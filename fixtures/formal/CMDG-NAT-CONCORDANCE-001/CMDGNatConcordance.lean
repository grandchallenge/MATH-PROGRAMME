import Mathlib.SetTheory.ZFC.Ordinal

namespace CMDG.NatConcordance

open ZFSet

/-- The retained set-theoretic natural number representation: the finite von Neumann ordinal
corresponding to a Lean natural, realized as a `ZFSet`. -/
noncomputable def zNat (n : Nat) : ZFSet :=
  (n : Ordinal).toZFSet

@[simp] theorem zNat_zero : zNat 0 = ∅ := by
  simp [zNat]

@[simp] theorem zNat_succ (n : Nat) :
    zNat (Nat.succ n) = insert (zNat n) (zNat n) := by
  simp [zNat, Nat.succ_eq_add_one]

@[simp] theorem zNat_rank (n : Nat) :
    (zNat n).rank = (n : Ordinal) := by
  simp [zNat]

theorem zNat_injective : Function.Injective zNat := by
  intro m n h
  have hrank := congrArg ZFSet.rank h
  simpa [zNat] using hrank

@[simp] theorem zNat_mem_iff {m n : Nat} :
    zNat m ∈ zNat n ↔ m < n := by
  simp [zNat]

@[simp] theorem zNat_subset_iff {m n : Nat} :
    zNat m ⊆ zNat n ↔ m ≤ n := by
  simp [zNat]

/-- Arithmetic on the retained finite-ordinal image, induced through ordinal rank.
This is an implementation-level operation on `ZFSet`; no claim is made that it is the
Programme's full syntactic-ZFC arithmetic definition outside the finite-ordinal image. -/
noncomputable def zAdd (x y : ZFSet) : ZFSet :=
  (x.rank + y.rank).toZFSet

noncomputable def zMul (x y : ZFSet) : ZFSet :=
  (x.rank * y.rank).toZFSet

def zLe (x y : ZFSet) : Prop :=
  x ⊆ y

def zDvd (x y : ZFSet) : Prop :=
  ∃ k : Nat, zMul x (zNat k) = y

@[simp] theorem zAdd_zNat (m n : Nat) :
    zAdd (zNat m) (zNat n) = zNat (m + n) := by
  simp [zAdd, zNat]

@[simp] theorem zMul_zNat (m n : Nat) :
    zMul (zNat m) (zNat n) = zNat (m * n) := by
  simp [zMul, zNat]

@[simp] theorem zLe_zNat {m n : Nat} :
    zLe (zNat m) (zNat n) ↔ m ≤ n := by
  simp [zLe]

@[simp] theorem zDvd_zNat {m n : Nat} :
    zDvd (zNat m) (zNat n) ↔ m ∣ n := by
  constructor
  · rintro ⟨k, hk⟩
    have hencoded : zNat (m * k) = zNat n := by
      simpa using hk
    exact ⟨k, (zNat_injective hencoded).symm⟩
  · rintro ⟨k, rfl⟩
    exact ⟨k, by simp⟩

/-- A concrete Type-category NNO contract. `Unit` is the chosen terminal object;
composition in `Type` is ordinary function composition. -/
structure TypeNNO where
  carrier : Type
  zero : Unit → carrier
  succ : carrier → carrier
  universal :
    ∀ {X : Type} (x0 : Unit → X) (s : X → X),
      ∃! h : carrier → X,
        h ∘ zero = x0 ∧ h ∘ succ = s ∘ h

def natZero : Unit → Nat :=
  fun _ => 0

def natFold {X : Type} (x0 : Unit → X) (s : X → X) : Nat → X
  | 0 => x0 ()
  | n + 1 => s (natFold x0 s n)

theorem natFold_zero {X : Type} (x0 : Unit → X) (s : X → X) :
    natFold x0 s ∘ natZero = x0 := by
  funext u
  cases u
  rfl

theorem natFold_succ {X : Type} (x0 : Unit → X) (s : X → X) :
    natFold x0 s ∘ Nat.succ = s ∘ natFold x0 s := by
  funext n
  rfl

theorem natFold_unique {X : Type} (x0 : Unit → X) (s : X → X)
    (h : Nat → X)
    (hzero : h ∘ natZero = x0)
    (hsucc : h ∘ Nat.succ = s ∘ h) :
    h = natFold x0 s := by
  funext n
  induction n with
  | zero =>
      have hz := congrFun hzero ()
      simpa [natZero, Function.comp_def, natFold] using hz
  | succ n ih =>
      have hs := congrFun hsucc n
      calc
        h (Nat.succ n) = s (h n) := by
          simpa [Function.comp_def] using hs
        _ = s (natFold x0 s n) := congrArg s ih
        _ = natFold x0 s (Nat.succ n) := rfl

def natTypeNNO : TypeNNO where
  carrier := Nat
  zero := natZero
  succ := Nat.succ
  universal := by
    intro X x0 s
    refine ⟨natFold x0 s, ⟨natFold_zero x0 s, natFold_succ x0 s⟩, ?_⟩
    intro h hh
    exact natFold_unique x0 s h hh.1 hh.2

abbrev NNOCarrier := Nat

def nnoZero : NNOCarrier := 0
def nnoSucc : NNOCarrier → NNOCarrier := Nat.succ
def nnoAdd : NNOCarrier → NNOCarrier → NNOCarrier := Nat.add
def nnoMul : NNOCarrier → NNOCarrier → NNOCarrier := Nat.mul
def nnoLe (m n : NNOCarrier) : Prop := m ≤ n
def nnoDvd (m n : NNOCarrier) : Prop := m ∣ n

theorem nat_type_nno_universal {X : Type} (x0 : Unit → X) (s : X → X) :
    ∃! h : NNOCarrier → X,
      h ∘ natZero = x0 ∧ h ∘ nnoSucc = s ∘ h := by
  refine ⟨natFold x0 s, ⟨natFold_zero x0 s, natFold_succ x0 s⟩, ?_⟩
  intro h hh
  exact natFold_unique x0 s h hh.1 hh.2

def dttToNNO (n : Nat) : NNOCarrier := n

@[simp] theorem dttToNNO_zero :
    dttToNNO 0 = nnoZero := rfl

@[simp] theorem dttToNNO_succ (n : Nat) :
    dttToNNO (Nat.succ n) = nnoSucc (dttToNNO n) := rfl

@[simp] theorem dttToNNO_add (m n : Nat) :
    dttToNNO (m + n) = nnoAdd (dttToNNO m) (dttToNNO n) := rfl

@[simp] theorem dttToNNO_mul (m n : Nat) :
    dttToNNO (m * n) = nnoMul (dttToNNO m) (dttToNNO n) := rfl

@[simp] theorem dttToNNO_le {m n : Nat} :
    nnoLe (dttToNNO m) (dttToNNO n) ↔ m ≤ n := Iff.rfl

@[simp] theorem dttToNNO_dvd {m n : Nat} :
    nnoDvd (dttToNNO m) (dttToNNO n) ↔ m ∣ n := Iff.rfl

noncomputable def nnoToZfc (n : NNOCarrier) : ZFSet :=
  zNat n

@[simp] theorem nnoToZfc_zero :
    nnoToZfc nnoZero = ∅ := by
  simp [nnoToZfc, nnoZero]

@[simp] theorem nnoToZfc_succ (n : NNOCarrier) :
    nnoToZfc (nnoSucc n) = insert (nnoToZfc n) (nnoToZfc n) := by
  simp [nnoToZfc, nnoSucc]

@[simp] theorem nnoToZfc_add (m n : NNOCarrier) :
    zAdd (nnoToZfc m) (nnoToZfc n) = nnoToZfc (nnoAdd m n) := by
  simp [nnoToZfc, nnoAdd]

@[simp] theorem nnoToZfc_mul (m n : NNOCarrier) :
    zMul (nnoToZfc m) (nnoToZfc n) = nnoToZfc (nnoMul m n) := by
  simp [nnoToZfc, nnoMul]

@[simp] theorem nnoToZfc_le {m n : NNOCarrier} :
    zLe (nnoToZfc m) (nnoToZfc n) ↔ nnoLe m n := by
  simp [nnoToZfc, nnoLe]

@[simp] theorem nnoToZfc_dvd {m n : NNOCarrier} :
    zDvd (nnoToZfc m) (nnoToZfc n) ↔ nnoDvd m n := by
  simp [nnoToZfc, nnoDvd]

/-- One checked theorem touching the complete admitted operation surface. This theorem is used as
the declaration-level dependency/axiom extraction root; it does not confer governance authority. -/
theorem bounded_concordance
    (m n : Nat) {X : Type} (x0 : Unit → X) (s : X → X) :
    (∃! h : NNOCarrier → X,
      h ∘ natZero = x0 ∧ h ∘ nnoSucc = s ∘ h) ∧
    zNat 0 = ∅ ∧
    zNat (Nat.succ m) = insert (zNat m) (zNat m) ∧
    zAdd (zNat m) (zNat n) = zNat (m + n) ∧
    zMul (zNat m) (zNat n) = zNat (m * n) ∧
    (zLe (zNat m) (zNat n) ↔ m ≤ n) ∧
    (zDvd (zNat m) (zNat n) ↔ m ∣ n) ∧
    dttToNNO 0 = nnoZero ∧
    dttToNNO (Nat.succ m) = nnoSucc (dttToNNO m) ∧
    dttToNNO (m + n) = nnoAdd (dttToNNO m) (dttToNNO n) ∧
    dttToNNO (m * n) = nnoMul (dttToNNO m) (dttToNNO n) ∧
    (nnoLe (dttToNNO m) (dttToNNO n) ↔ m ≤ n) ∧
    (nnoDvd (dttToNNO m) (dttToNNO n) ↔ m ∣ n) ∧
    nnoToZfc nnoZero = ∅ ∧
    nnoToZfc (nnoSucc m) = insert (nnoToZfc m) (nnoToZfc m) ∧
    zAdd (nnoToZfc m) (nnoToZfc n) = nnoToZfc (nnoAdd m n) ∧
    zMul (nnoToZfc m) (nnoToZfc n) = nnoToZfc (nnoMul m n) ∧
    (zLe (nnoToZfc m) (nnoToZfc n) ↔ nnoLe m n) ∧
    (zDvd (nnoToZfc m) (nnoToZfc n) ↔ nnoDvd m n) := by
  refine ⟨nat_type_nno_universal x0 s, ?_⟩
  simp

end CMDG.NatConcordance
