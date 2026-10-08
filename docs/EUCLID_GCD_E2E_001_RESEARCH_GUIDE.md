# EUCLID-GCD-E2E-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [closeout tracker #240](https://github.com/grandchallenge/MATH-PROGRAMME/issues/240).  
    **AUTHORITY:** `governance/euclid_gcd_e2e_001_closeout.json`.  
    **EXPOSITION:** this guide explains a terminal bounded result; the protected closeout governs the admitted claim.

## 1. Status

This campaign slice is terminal. The bounded certified result is `gcd(252,105)=21`, together with the exact Euclidean trace, Bézout witness, independent checker obligations, and Lean soundness theorem recorded by the protected cross-pillar closeout.

## 2. Plain object

The exercise demonstrates the full Forge → Solve → Cert → Programme path on a small theorem where the mathematical object, construction, witness, checker, formal theorem, and institutional authority can be kept distinct.

## 3. Exact result

The terminal Stage 1 Programme closeout was protected at `183ff2a0adfbe5bd0ffd5f2e638089b94b868c54` (tracker #240). The archived candidate JSON still describes its pre-merge state; this is historical provenance, not the current gate. The protected claim set covers the concrete gcd instance, the three linked Euclidean divisions, the Bézout identity `21 = -2*252 + 5*105`, and soundness of the accepted-certificate predicate for the bounded formalization.

## 4. Authority chain

The authoritative Programme record is `governance/euclid_gcd_e2e_001_closeout.json`. The human proof trace is `docs/EUCLID_GCD_E2E_001_PROOF_TRACE.md`.

## 5. What remains open

Nothing remains for Stage 1 itself. The linear-Diophantine Stage 2 successor has independently completed and is explained in [its certified proof trace](EUCLID_DIOPHANTINE_E2E_002_PROOF_TRACE.md). The historical Book VII microcampaign remains a separate source-concordance and admission operation, not a Stage 1 consequence.

## 6. Claim boundary

The result is not a novelty, priority, universal producer-correctness, or historical-verbatim-equivalence claim. This guide creates no additional certification effect.

## 7. First executable step

For audit or replay, begin from the protected closeout record and follow its exact Forge, Solve, Cert, and Programme identities. For new mathematics, open a separate successor with its own authority chain.

## Reader entry and prerequisites

**Status:** bounded certified Stage 1; independently protected Stage 2 exists. **Audience:** beginning number theory readers, engineers of proof checkers, formalization collaborators. **Time to first example:** 3 minutes. **Time to first fixture:** 5 minutes.

| Level | Concepts |
| --- | --- |
| Required | Integer divisibility and division with remainder |
| Helpful | Bézout identity, Euclid's algorithm |
| Deferred | Lean syntax, proof-carrying JSON, independent checker design |

## Core bridge and first examples by hand

**Friendly example:** \(252=2\cdot105+42\), \(105=2\cdot42+21\), \(42=2\cdot21+0\). Thus the last nonzero remainder is 21. The Bézout witness \(-2\cdot252+5\cdot105=21\) makes the maximality check explicit.

**Edge example:** inputs \((0,0)\) are excluded from this campaign's accepted certificate contract. A generic library may define \(\gcd(0,0)=0\), but that does not license applying this particular positive-divisor normalization or its terminal descent trace to \((0,0)\).

Bridge: division with remainder → gcd witness → candidate construction → independent exact replay → Lean soundness theorem.

## First computation or fixture

```python
from math import gcd
a, b = 252, 105
trace = []
while b:
    q, r = divmod(a, b)
    trace.append((a, b, q, r))
    a, b = b, r
print(trace)
print(a, gcd(252, 105), -2*252 + 5*105)
# Expected:
# [(252, 105, 2, 42), (105, 42, 2, 21), (42, 21, 2, 0)]
# 21 21 21
```

Input, quotient/remainder operation and expected output are exact. **Support route:** independent arithmetic regression, not replacement for MATHCERT's protected checker. **Limitation:** tests only the displayed inputs and no general producer correctness.

## First theorem or local proposition

**Euclidean invariance.** If \(a=qb+r\), then \(\gcd(a,b)=\gcd(b,r)\): the common divisors coincide because \(r=a-qb\) and \(a=qb+r\). Applying this three times proves the example's gcd.

## Challenge ladder

| Stage | Duty | Completion test |
| --- | --- | --- |
| Exercise | Compute first remainder by hand | 42 |
| Exploration | Try inputs \((105,252)\) | Same gcd, altered trace |
| Fixture | Execute the code | Exact rows and final three 21s |
| Lemma candidate | Prove Euclidean invariance | Both common-divisor inclusions |
| Open direction | Inspect a different coefficient pair | Explicit candidate and separate certification contract |

## Certification path and continuation graph

The protected Stage 1 theorem is not produced by this teaching fixture. Cross-pillar source/producer/verifier hashes and the accepted-certificate Lean statement are recorded in the frozen Stage 1 closeout, with **terminal completion** evidenced by protected Programme merge \(`183ff2a0…`\) and tracker #240.

`arithmetic trace → Bézout witness → independent GCD checker → accepted-certificate soundness → Stage 2 Diophantine proof trace → historical Book VII concordance [separate]`

## Trust quartet

**Proved:** protected accepted-certificate soundness and the concrete gcd instance. **Checked:** trace, witness, identity, and bounded mutations. **Open:** no Stage 1 theorem debt; historical source concordance for separate Book VII work. **External verification:** exact imported Forge/Solve/Cert receipts and historical sources for Stage 3.

## Bibliography and source audit

| Source | Use | Audit state |
| --- | --- | --- |
| [Stage 1 proof trace](EUCLID_GCD_E2E_001_PROOF_TRACE.md) | Full exact certificate narrative | Protected Programme exposition |
| `governance/euclid_gcd_e2e_001_closeout.json` | Candidate evidence identities | Frozen historical source, not present gate |
| [Terminal tracker readback](https://github.com/grandchallenge/MATH-PROGRAMME/issues/240#issuecomment-5190940620) | Stage 1 admission | Protected-merge provenance |
| [Stage 2 proof trace](EUCLID_DIOPHANTINE_E2E_002_PROOF_TRACE.md) | Independent successor | Separate protected claim |

**First executable step / completion test:** Recalculate all remainders and the Bézout witness independently, compare exact output against the published trace, and mark the \((0,0)\) case excluded.

