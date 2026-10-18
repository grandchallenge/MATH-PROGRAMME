# Erdős Problem #41 — Historical Mathlib & Formal Conjectures Theorem-Type Bridge (`#2703`)

## 1. Scope and Provenance Lock

This artifact completes the imported Mathlib (`Finset`, `Multiset`, `Nat`) and Formal Conjectures theorem-type bridge for historical Erdős Problem #41 (`ERDOS-041-HISTORICAL-MATHLIB-BRIDGE-001`, issue `#2703`, parent review `#2536`, catalogue `#1310`, programme `#2503`).

| Artifact / Pin | Identifier |
|---|---|
| Lean Toolchain | `leanprover/lean4:v4.33.0` (commit `d8b18978322de05a8f3dba51ef03cf5461676c17`) |
| Mathlib Commit | `db584cd6d46c92f209a44c0f1c829460d327499d` |
| Refreshed Formal Conjectures Commit | `79eac378a26b46d30974cdb33962e0752591b79d` (`FormalConjectures/ErdosProblems/41.lean` blob SHA1 `2a1bd1f521325e36aaaf50a3a3feffc9c426aaf6`) |
| Frozen Formal Conjectures Commit | `85f863718beeec7b58a3a1926ee92e3472bc2020` (`FormalConjectures/ErdosProblems/41.lean` blob SHA1 `5e9eeb26586d087f4b2ab3d82734ea5ed87ddf50`) |
| Primary 1980 Survey PDF SHA256 | `e2280c6cbba6bfecedb5c5134ce827c59695dccd7f3377d42658cbc30b8db3cf` (Erdős, *Annals of Discrete Mathematics* 6 (1980), pp. 98–99) |
| Compiled Lean Bridge Module | `governance/source_erdos_critical_005/Erdos41HistoricalMathlibBridge.lean` (`66f82861886a78102e49e02a2092dcc48729317acfdd0977a2cd42504bd0ec49`) |
| Lean Compiler Stdout SHA256 | `a84f43a364ad9ef0408ee4ffd5430ccc9bc25042a91cf845d742e22d4e0c6b9e` (`exit_code = 0`, `sorry_count = 0`) |

**Claim Boundary**: This is strictly a `SOURCE_SEMANTIC` formal specification and predicate comparison. It does **not** prove, disprove, or claim `MATHCERT` for the open asymptotic density conjecture in Erdős Problem #41, does **not** mutate original frozen source locks, and does **not** directly clear `gcl-review:revise` on `#2536`.

---

## 2. Imported Mathlib Predicate Comparison

In `Erdos41HistoricalMathlibBridge.lean`, we import `Mathlib.Data.Finset.Basic`, `Mathlib.Data.Finset.Card`, `Mathlib.Data.Finset.Max`, `Mathlib.Data.Multiset.Basic`, `Mathlib.Data.Set.Finite.Basic`, `Mathlib.Algebra.Order.BigOperators.Group.Finset`, and `Mathlib.Order.Interval.Finset.Nat`, and formalize all three candidate $B_3$ predicates on $A \subseteq \mathbb{N}$:

1. **Historical 1980 Survey Predicate (`HistoricalB3 A := HistoricalBrCondition A 3`)**:

   $$
   \forall I, J : \mathrm{Finset}\;\mathbb{N},\; \uparrow I \subseteq A \to \uparrow J \subseteq A \to I.\mathrm{Nonempty} \to J.\mathrm{Nonempty} \to I.\mathrm{card} \le 3 \to J.\mathrm{card} \le 3 \to \left(\sum_{i \in I} i = \sum_{j \in J} j\right) \to I = J
   $$

   Matches Erdős (1980, pp. 98–99): sums of $r$ or fewer distinct terms from $A$ (Sidon $0/1$ coefficients, $1 \le |I| \le 3$) are all distinct.

2. **Modern Refreshed Provider Predicate (`ModernB3 A := NtupleCondition A 3`)**:

   $$
   \forall I, J : \mathrm{Multiset}\;\mathbb{N},\; (\forall i \in I, i \in A) \to (\forall j \in J, j \in A) \to I.\mathrm{card} = 3 \to J.\mathrm{card} = 3 \to I.\mathrm{sum} = J.\mathrm{sum} \to I = J
   $$

   Matches upstream `google-deepmind/formal-conjectures` commit `79eac378a26b46d30974cdb33962e0752591b79d`: sums of 3-element multisets (permitting repeated summands, up to permutation) are all distinct.

3. **Frozen Fixed-Triple Finset Predicate (`WeakFixed3 A := FrozenFinsetNtupleCondition A 3`)**:

   $$
   \forall I, J : \mathrm{Finset}\;\mathbb{N},\; \uparrow I \subseteq A \land \uparrow J \subseteq A \land I.\mathrm{card} = 3 \land J.\mathrm{card} = 3 \land \left(\sum_{i \in I} i = \sum_{j \in J} j\right) \to I = J
   $$

   Matches frozen provider commit `85f863718beeec7b58a3a1926ee92e3472bc2020`: sums of fixed 3-element distinct subsets are all distinct.

---

## 3. Kernel-Verified Theorems and Printed Axioms

Every theorem in `Erdos41HistoricalMathlibBridge.lean` compiles under `leanprover/lean4:v4.33.0` with **zero `sorry`** and depends only on standard Lean axioms `[propext, Classical.choice, Quot.sound]`:

- **One-way implications into `WeakFixed3`**:
  - `historical_implies_fixed : ∀ (A : Set ℕ), HistoricalB3 A → WeakFixed3 A`
  - `modern_implies_fixed : ∀ (A : Set ℕ), ModernB3 A → WeakFixed3 A`
- **Strictness of `WeakFixed3` (finite witness `finiteWeakWitness = {1, 2, 3}`)**:
  - `not_weakFixed3_implies_historicalB3 : ¬ (∀ A : Set ℕ, WeakFixed3 A → HistoricalB3 A)` (falsified by $\{1, 2\}$ vs. $\{3\}$)
  - `not_weakFixed3_implies_modernB3 : ¬ (∀ A : Set ℕ, WeakFixed3 A → ModernB3 A)` (falsified by $\{1, 1, 3\}$ vs. $\{1, 2, 2\}$)
- **Infinite Separating Model 1 (`infSuperincreasing = {1, 2, 4} ∪ {10^k : k ≥ 1}`)**:
  - `infSuperincreasing_infinite : infSuperincreasing.Infinite`
  - `infSuperincreasing_historicalB3 : HistoricalB3 infSuperincreasing` (proved via full superincreasing subset-sum uniqueness `infSuperincreasing_finset_sum_inj`)
  - `infSuperincreasing_not_modernB3 : ¬ ModernB3 infSuperincreasing` (falsified by $1 + 1 + 4 = 2 + 2 + 2 = 6$)
  - `exists_infinite_historicalB3_not_modernB3 : ∃ A : Set ℕ, A.Infinite ∧ HistoricalB3 A ∧ WeakFixed3 A ∧ ¬ ModernB3 A`
- **Infinite Separating Model 2 (`infModernWitness = {1, 4, 5} ∪ {100^k : k ≥ 1}`)**:
  - `infModernWitness_infinite : infModernWitness.Infinite`
  - `infModernWitness_modernB3 : ModernB3 infModernWitness` (proved via base-100 highest-summand dominance `multiset_sum_lt_tail` and base uniqueness for $n \le 3$ on $\{1, 4, 5\}$)
  - `infModernWitness_not_historicalB3 : ¬ HistoricalB3 infModernWitness` (falsified by cross-cardinality $1 + 4 = 5$)
  - `exists_infinite_modernB3_not_historicalB3 : ∃ A : Set ℕ, A.Infinite ∧ ModernB3 A ∧ WeakFixed3 A ∧ ¬ HistoricalB3 A`
- **Boundary Conventions (`Nat`/0, empty set, permutation, diagonal multiplicity, cross-cardinality)**:
  - `empty_historicalB3`, `empty_modernB3`, `empty_weakFixed3`
  - `zero_and_nonzero_not_historicalB3 : 0 ∈ A → a ∈ A → a ≠ 0 → ¬ HistoricalB3 A`
  - `multiset_perm_trivial_coincidence : xs.Perm ys → (xs : Multiset ℕ) = (ys : Multiset ℕ)`
  - `diagonal_finset_dedup_vs_multiset_card : ({a, a, a} : Finset ℕ).card = 1 ∧ (a ::ₘ a ::ₘ a ::ₘ 0 : Multiset ℕ).card = 3`
  - `cross_cardinality_pair_eq_singleton_not_historicalB3`
- **Exported Statement-Level Non-Equivalence**:
  - `frozen_statement_implies_historical_and_modern`
  - `historical_statement_not_implies_modern_statement : ¬ (∀ Q : Set ℕ → Prop, Erdos41HistoricalStatement Q → Erdos41ModernStatement Q)`
  - `modern_statement_not_implies_historical_statement : ¬ (∀ Q : Set ℕ → Prop, Erdos41ModernStatement Q → Erdos41HistoricalStatement Q)`

---

## 4. Historically Named Theorem Specification

Alongside the upstream refreshed theorem `erdos_41` (which uses `NtupleCondition A 3`, i.e., `ModernB3 A`), the exact historically faithful 1980 variant specification is:

```lean
@[category research open, AMS 11]
theorem erdos_41.variants.historical_b3 (A : Set ℕ)
    (h_b3 : HistoricalBrCondition A 3) (h_infinite : A.Infinite) :
    Filter.atTop.liminf (fun N => (A ∩ Icc 1 N).ncard / (N : ℝ)^(1/3 : ℝ)) = 0
```

Because `HistoricalB3` and `ModernB3` are logically incomparable on infinite subsets of $\mathbb{N}$, `erdos_41` and `erdos_41.variants.historical_b3` represent distinct mathematical hypotheses and must be tracked with explicit convention tags rather than conflated.
