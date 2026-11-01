# Evidence, reproducibility, and open obligations

<p class="page-deck">An auditable register of source mathematics, GCL finite checks, conditional deductions, editorial admission, and work still required.</p>

## How to interpret the evidence grades

| Grade | Meaning |
| --- | --- |
| **EXT** | Established mathematical theorem imported with attribution |
| **CAL** | Finite calculation or elementary argument, with a written proof or executable check |
| **SRC** | Source transcription, theorem-interface audit, or parameter ledger |
| **COND** | A conditional deduction from a published theorem under explicitly stated hypotheses |
| **OPEN** | No proof or complete implementation currently admitted |

A document merge or public MkDocs page certifies neither mathematical truth nor independence. The independent specialist certification route remains separate.

## Source-to-claim matrix

| Item | Primary evidence | Grade | Maximum warranted claim |
| --- | --- | --- | --- |
| MIP* = RE | [Ji et al., v4](https://arxiv.org/abs/2001.04383) | EXT | Published complexity theorem; not P ≠ NP |
| Quantum low individual degree soundness | [Ji et al., arXiv:2009.12982](https://arxiv.org/abs/2009.12982) | EXT | Corrected source underpinning |
| Gap-preserving compression | [Theorem 12.1](https://arxiv.org/pdf/2001.04383v4) | EXT | Conditional normal-form theorem for quantum strategy resources |
| Magic-square classical value $8/9$ | [MATHSOLVE #1137](https://github.com/grandchallenge/MATHSOLVE/pull/1137) | CAL | Finite two-prover game bound |
| Source compression parameter ledger | [Protected ledger](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_COMPRESSION_PARAMETER_LEDGER.md) | SRC | Exact symbolic resource and error bookkeeping |
| Nine-level identity input verifier | [Protected note](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_NINE_LEVEL_INPUT_AND_TRANSFER.md) | CAL | Finite verifier semantics; not full compressor |
| 512-pair exhaustive test | [Finite emulator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_NINE_LEVEL_INPUT_EMULATOR.py) | CAL | Reproducible finite local behavior |
| Double-exponential entanglement bound for compressed family | [Source theorem and WP00 note](https://github.com/grandchallenge/MATHSOLVE/pull/1147) | COND | Requires encoded input satisfying the source theorem |
| Indexed language is cofinite and in P | [WP00 note](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/PNP-ABOVE/WP00_NINE_LEVEL_INPUT_AND_TRANSFER.md) | COND | Existence argument for a *selected unary language*, not arbitrary game-value computation |
| General SAT-to-classical strategy-cost transfer | [Research issue #1136](https://github.com/grandchallenge/MATHSOLVE/issues/1136) | OPEN | No such implication proved |
| P = NP or P ≠ NP | [Parent PNP-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162) | OPEN | Neither proposition proved |

## Exact finite test

The protected Python emulator uses the standard library, represents the nine binary coordinates as tuples, and exhaustively checks all 512 vectors for both players and all nine marginal transitions.

It checks that each factor is the required coordinate basis vector, that each marginal is the prefix projection, that a level's linear increment reconstructs the next marginal, and that the diagonal pair distribution has 512 distinct support points. It also tests the specified empty-answer decider and representative invalid queries.

**It does not:** run the quantum compression construction, prove Theorem 12.1, produce a strategy at enormous Schmidt rank, or certify the source's Gödel-coded Turing machines.

## Research genealogy

The bounded work began with [PNP-ABOVE-WP00](https://github.com/grandchallenge/MATHSOLVE/issues/1136) and continued through [finite magic-square calibration #1137](https://github.com/grandchallenge/MATHSOLVE/pull/1137), [source interface #1140](https://github.com/grandchallenge/MATHSOLVE/pull/1140), [resource semantics #1142](https://github.com/grandchallenge/MATHSOLVE/pull/1142), [parameter ledger #1146](https://github.com/grandchallenge/MATHSOLVE/pull/1146), and [nine-level input #1147](https://github.com/grandchallenge/MATHSOLVE/pull/1147). The last two reports have protected-main readback.

The source theorem version is **arXiv:2001.04383v4, 16 October 2026**, particularly Definitions 4.14 and 5.12, Theorems 8.3, 10.30, 11.4 and 12.1, Figure 15, and Table 2. A versioned URL is not a byte-level archive hash; do not claim a hash for the external PDF unless one is actually retained.

## Falsification gates

A proposed transfer fails if it confuses Schmidt rank with classical time; relies on an expensive prover as though it were an ordinary SAT algorithm; replaces explicit input length with a succinct index without a reduction; relies on unprovided numerical constants; or implicitly assumes the SAT-to-strategy construction it must prove.

A claimed full compressed-game execution fails its evidence gate until there are exact source-faithful encoded machines, runtime and representation bounds, correct promises, effective constants, a functioning implementation of all three stages, and independent output checks.

Finite experiments may suggest lemmas but do not justify asymptotic lower bounds.

## Open obligations and stopping conditions

1. **Source machine representation:** Compile the nine-level input into the source's actual Turing-machine encoding, including malformed-input behavior and step bounds.
2. **Numerical constructivity:** Obtain explicit sufficient values of $\lambda$ and $C_0$, or document why they cannot currently be extracted.
3. **Classical invariant:** Define a nontrivial restricted model and one falsifiable quantitative lower-bound target.
4. **Uniform transfer:** Supply the direction and complexity of a SAT-to-realization reduction, or demonstrate the exact obstruction.
5. **Barrier audit:** Check relativization, natural-proofs, and algebrization assumptions before novelty promotion.
6. **Editorial continuity:** Update [the preprint record](preprint.md) if the claims or source identities change. The parent programme's original formal-conjecture definition-level concordance issue remains outstanding.

A negative result with a precise counterexample and exact scope is a legitimate terminal for a bounded investigation. Neither documentation nor a closed work package implies the Millennium problem has been solved.

For an accessible explanation of these cautions, see the [reader's primer](primer.md). For formulas and proof interfaces, see the [technical spine](technical.md).
