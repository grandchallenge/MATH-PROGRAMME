# Euclidean GCD: an end-to-end certified proof trace

**Accessible research guide:** [EUCLID-GCD-E2E-001 Research Guide](EUCLID_GCD_E2E_001_RESEARCH_GUIDE.md)

<p class="page-deck">A concrete arithmetic question carried from source-conscious intake through deterministic construction, independent checking, Lean replay, and bounded Programme closeout.</p>


!!! info "Research surface authority"
    **LIVE:** [EUCLID-GCD-E2E-001 canonical closeout tracker #240](https://github.com/grandchallenge/MATH-PROGRAMME/issues/240).  
    **AUTHORITY:** `governance/euclid_gcd_e2e_001_closeout.json`.  
    **EXPOSITION:** this proof trace explains the protected result; the protected closeout governs the certified claim.

## The approachable task

Find the greatest common divisor of `252` and `105`.

The **object sought** is the positive natural number that divides both inputs and is divisible by every other common divisor. The certified answer is:

```text
gcd(252,105) = 21
```

This page is an exact Stage 1 proof trace. It is not a novelty or priority claim, and it is not a historical edition of Euclid.

## 1. The construction

Repeated Euclidean division gives:

```text
252 = 2 * 105 + 42
105 = 2 * 42 + 21
42 = 2 * 21 + 0
```

Each nonterminal remainder is nonnegative and smaller than the preceding divisor. The steps link exactly: the divisor and remainder of one line become the dividend and divisor of the next line. The final remainder is zero, so the last positive divisor is `21`.

This trace is a **construction** of candidate evidence. A construction emitted by a solver does not certify itself.

## 2. The witness

Back-substitution gives the integer Bézout witness:

```text
21 = -2 * 252 + 5 * 105
```

Thus every common divisor of `252` and `105` divides `21`. The trace also shows that `21` divides both inputs. Together these facts characterize the greatest common divisor.

The pair `(-2,5)` is a **witness**. It is not the same thing as the mathematical object `21`, the Euclidean construction, or the certificate that records them.

## 3. The certificate

MATHSOLVE produced deterministic candidate JSON. MATHCERT used an implementation that does not import or execute the Solve producer. It checked:

- the exact protected Forge and Solve artifact identities;
- input concordance and exclusion of `(0,0)`;
- every division equation;
- trace linkage, remainder bounds, strict descent, and terminal zero;
- positive normalization of `d`;
- divisibility of both inputs by `d`;
- the integer Bézout equation;
- an independent `math.gcd` replay;
- the admitted claim and authority boundaries.

Fifteen focused mutations demonstrated rejection of changed quotients, remainders, links, descent, terminal divisor, coefficients, inputs, identities, authority fields, protected effect, and successor activation.

## 4. The formal theorem

MATHCERT formalized an accepted-certificate predicate in Lean and proved:

```lean
theorem acceptedGCDCertificate_sound {a b d : Nat}
    (h : AcceptedGCDCertificate a b d) : d = Nat.gcd a b
```

It also kernel-replayed:

```lean
theorem gcd252105 : Nat.gcd 252 105 = 21
theorem bezout252105 : (-2 : Int) * 252 + 5 * 105 = 21
```

The formal module contains no `sorry` and introduces no local axioms. Declaration-level reports contain only standard mathlib foundations: `propext`, `Classical.choice`, and `Quot.sound`, with smaller subsets for several declarations.

## 5. What is certified

The bounded certified claim set is:

| Claim | Certified content |
| --- | --- |
| `EUCLID-GCD-E2E-001-C001` | For inputs `252` and `105`, the normalized gcd is `21`. |
| `EUCLID-GCD-E2E-001-C002` | The three Euclidean divisions are exact, linked, descending, and terminal. |
| `EUCLID-GCD-E2E-001-C003` | `x = -2`, `y = 5` satisfies `x*252 + y*105 = 21`. |
| `EUCLID-GCD-E2E-001-C004` | The accepted-certificate predicate entails `d = Nat.gcd a b`. |

The protected MATHCERT disposition is:

`CERTIFIED_CHECKER_SOUNDNESS_AND_CONCRETE_GCD_INSTANCE`

## 6. Exact authority chain

| Pillar | Protected merge | Role |
| --- | --- | --- |
| MATHFORGE | `3622bac82a39cdb9e82ec463919d9e6927c1ec0e` | fixed the modern statement, risks, source boundary, and downstream contract |
| MATHSOLVE | `3a8493aa322f0e640c921b8824c4d7f88a8c057d` | produced deterministic candidate evidence |
| MATHCERT | `78b69e6a3461a83f4893d61c421b1570c08a9ba6` | independently checked the candidate and proved the bounded Lean theorems |
| MATH-PROGRAMME | `183ff2a0adfbe5bd0ffd5f2e638089b94b868c54` | protected Stage 1 closeout and published proof trace |

Each completed pillar passed exact-head CI, independent non-author review by `jimsteeg`, Human Steward exact-head disposition, deliberate protected merge, and protected-main readback.

The original machine-readable closeout candidate (retained unmodified for historical provenance) is [`governance/euclid_gcd_e2e_001_closeout.json`](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/euclid_gcd_e2e_001_closeout.json).

## Claim boundary

This Stage 1 result does **not** establish:

- correctness of every extended-Euclidean implementation;
- admission of the `(0,0)` case;
- that the modern integer Bézout identity appears verbatim in Euclid;
- mathematical novelty, priority, or first-formalization priority;
- completion or activation of the linear Diophantine extension;
- completion or activation of `EUCLID-ELEMENTS-BOOK-VII-MICRO-001`.

The Stage 1 closeout was independently approved and merged into protected Programme `main` at `183ff2a0adfbe5bd0ffd5f2e638089b94b868c54`; [tracker #240](https://github.com/grandchallenge/MATH-PROGRAMME/issues/240#issuecomment-5190940620) records terminal readback. The [Stage 2 linear-Diophantine theorem and bounded examples](EUCLID_DIOPHANTINE_E2E_002_PROOF_TRACE.md) are now certified under their separate protected authority chain. The Book VII historical microcampaign remains subject to its independent source, licensing, and admission gates. Neither successor strengthens the bounded Stage 1 gcd claim.

## Reproduce the bounded checks

The authoritative executable and formal surfaces remain in their protected repositories:

- MATHSOLVE candidate and producer at merge `3a8493aa322f0e640c921b8824c4d7f88a8c057d`;
- MATHCERT checker, tests, and Lean module at merge `78b69e6a3461a83f4893d61c421b1570c08a9ba6`.

The Programme closeout validator checks the frozen Stage 1 candidate receipt, arithmetic trace, Bézout witness, and non-inflation boundaries without contacting the network. That candidate includes historical pending-gate fields; the terminal protected gate is established separately by the exact merge/readback evidence in tracker #240 and the Stage 2 protected lineage. Do not infer current pending status from frozen candidate metadata.
