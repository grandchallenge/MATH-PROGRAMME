/-
Copyright 2026 Grand Challenge GCL.
SPDX-License-Identifier: Apache-2.0

Historical Source-Root & Canonical Target Type-Hash Verification for Erdős Problem #14 (#2702).
Reconstructed Historical Commit: 8432eac998110a563e03df65a28c117e97c8c142
  Base Commit: 7d1a8c9912747679d0093f6d1216420c33ee5ffa (google-deepmind/formal-conjectures)
  Audit Patch: tiers/tier-1/formal-conjectures-audit-fixes.patch
               (conjectures-io/conjectures-tasks@275ef4824c41d41f97ac4e9fff95ca471de9341d,
                SHA256: 853372293b16a79ea495a28909e6077d41e2c6402165c3c6233ea0747c919814)
  FormalConjectures/ErdosProblems/14.lean blob SHA1: 52016d0053f4656cca69c135f4e95ef1449d63f6
  TaskSupport.lean SHA256: 58a80a223dbd7383d92eb2a57b1ec207c0991131a1a1bf24585a4452777c257e

Credited External Solver: JenW1N (September 2026). GCL does NOT claim discovery of either proof.
-/
import Mathlib.Order.Filter.AtTopBot.Basic
import Mathlib.Analysis.Asymptotics.Defs
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Set.Card
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Prod
import Lean

open Lean Elab Meta Term

/--
Exact `allUniqueSums` definition from `FormalConjecturesForMathlib/Combinatorics/Basic.lean`
at commit `8432eac998110a563e03df65a28c117e97c8c142`: elements representable as the sum of
exactly one unordered pair from `A` (permitting `0 ∈ A` and diagonal pairs `p.1 = p.2`).
-/
def allUniqueSums {α : Type*} [Add α] (A : Set α) : Set α :=
  { n | ∃ p : α × α, p.1 ∈ A ∧ p.2 ∈ A ∧ p.1 + p.2 = n ∧
      ∀ a₁ ∈ A, ∀ a₂ ∈ A, a₁ + a₂ = n → (a₁ = p.1 ∧ a₂ = p.2) ∨ (a₁ = p.2 ∧ a₂ = p.1) }

/--
Exact `≫` asymptotic notation from `FormalConjecturesForMathlib/Analysis/Asymptotics/Basic.lean`
at commit `8432eac998110a563e03df65a28c117e97c8c142`.
-/
notation f " ≫ " g => Asymptotics.IsBigO Filter.atTop (g : ℕ → ℝ) (f : ℕ → ℝ)

/--
Exact `answer(...)` elaborator behavior under default `google.answer = .alwaysTrue`
from `FormalConjecturesUtil/Answer.lean` at commit `8432eac998110a563e03df65a28c117e97c8c142`.
-/
syntax (name := answer) "answer(" term ")" : term
@[term_elab answer]
def answerElab : TermElab := fun stx expectedType? => do
  match stx with
  | `(answer($a:term)) =>
    if expectedType? == some (Expr.sort .zero) && a == (← `(term| sorry)) then
      return .const `True []
    else
      elabTerm a expectedType?
  | _ => Elab.throwUnsupportedSyntax

namespace Erdos14

open Asymptotics Filter

noncomputable def nonUniqueSumCount (A : Set ℕ) (N : ℕ) : ℝ :=
  ((Set.Icc 1 N) \ (allUniqueSums A)).ncard

noncomputable def almostSquareRoot (ε : ℝ) (N : ℕ) : ℝ :=
  N ^ (1/2 - ε)

noncomputable def squareRoot (N : ℕ) : ℝ :=
  Real.sqrt N

/--
Exact statement type of `Erdos14.erdos_14.parts.i` from `8432eac998110a563e03df65a28c117e97c8c142`
(without `sorry`, represented as an explicit `Prop` definition to preserve zero-`sorry` hygiene,
while producing the identical elaborated `Expr` type as `theorem erdos_14.parts.i`).
-/
def parts_i_prop : Prop :=
  answer(sorry) ↔ ∀ A, ∀ ε > 0, nonUniqueSumCount A ≫ almostSquareRoot ε

/--
Exact statement type of `Erdos14.erdos_14.parts.ii` from `8432eac998110a563e03df65a28c117e97c8c142`.
-/
def parts_ii_prop : Prop :=
  answer(sorry) ↔ ∃ (A : Set ℕ), IsLittleO atTop (nonUniqueSumCount A) squareRoot

/-!
## Natural-Number, Zero, Unordered-Pair, and Diagonal Semantics
-/

/-- Unordered pair symmetry in `allUniqueSums`: `(a, b)` and `(b, a)` represent the same unordered sum. -/
theorem allUniqueSums_unordered_symm (A : Set ℕ) (n a b : ℕ)
    (ha : a ∈ A) (hb : b ∈ A) (hab : a + b = n)
    (huniq : ∀ a₁ ∈ A, ∀ a₂ ∈ A, a₁ + a₂ = n → (a₁ = a ∧ a₂ = b) ∨ (a₁ = b ∧ a₂ = a)) :
    n ∈ allUniqueSums A :=
  ⟨(a, b), ha, hb, hab, huniq⟩

/-- Diagonal summands `a + a = 2 * a` are valid single unordered representations in `allUniqueSums`. -/
theorem zero_singleton_allUniqueSums : 0 ∈ allUniqueSums ({0} : Set ℕ) := by
  refine ⟨(0, 0), rfl, rfl, rfl, ?_⟩
  intro a₁ ha₁ a₂ ha₂ _
  exact Or.inl ⟨ha₁, ha₂⟩

/-- Because `nonUniqueSumCount A N` intersects with `Set.Icc 1 N`, `0` is outside `[1, N]`. -/
theorem zero_not_mem_Icc_one (N : ℕ) : (0 : ℕ) ∉ Set.Icc 1 N := by
  simp

end Erdos14
