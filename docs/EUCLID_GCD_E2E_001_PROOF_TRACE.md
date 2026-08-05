# Euclidean GCD: an end-to-end certified proof trace

<p class="page-deck">A concrete arithmetic question carried from source-conscious intake through deterministic construction, independent checking, Lean replay, and bounded Programme closeout.</p>

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
| MATH-PROGRAMME | pending this closeout | binds the cross-pillar receipt and publishes this page |

Each completed pillar passed exact-head CI, independent non-author review by `jimsteeg`, Human Steward exact-head disposition, deliberate protected merge, and protected-main readback.

The machine-readable closeout candidate is [`governance/euclid_gcd_e2e_001_closeout.json`](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/euclid_gcd_e2e_001_closeout.json).

## Claim boundary

This Stage 1 result does **not** establish:

- correctness of every extended-Euclidean implementation;
- admission of the `(0,0)` case;
- that the modern integer Bézout identity appears verbatim in Euclid;
- mathematical novelty, priority, or first-formalization priority;
- completion or activation of the linear Diophantine extension;
- completion or activation of `EUCLID-ELEMENTS-BOOK-VII-MICRO-001`.

The linear Diophantine theorem remains blocked until this Programme closeout is independently approved, Human-Steward-authorized, protected-merged, and read back. The Book VII microcampaign additionally requires protected Stage 2 completion and an exact historical source lock.

## Reproduce the bounded checks

The authoritative executable and formal surfaces remain in their protected repositories:

- MATHSOLVE candidate and producer at merge `3a8493aa322f0e640c921b8824c4d7f88a8c057d`;
- MATHCERT checker, tests, and Lean module at merge `78b69e6a3461a83f4893d61c421b1570c08a9ba6`.

The Programme closeout validator checks the exact receipt, arithmetic trace, Bézout witness, page content, and non-inflation boundaries without contacting the network.
