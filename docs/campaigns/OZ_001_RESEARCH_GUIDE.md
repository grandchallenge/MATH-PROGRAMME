# OZ-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [OZ-001 canonical tracker #113](https://github.com/grandchallenge/MATH-PROGRAMME/issues/113).  
    **AUTHORITY:** `campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE/00_INTAKE_AND_SOURCE_LOCK.md` and its protected successors.  
    **EXPOSITION:** this guide explains the current protected frontier; it does not promote an odd-zeta claim.

## 1. Status

OZ-001 is active. The campaign has source-normalized Apéry/Brown–Zudilin interfaces, false-proof controls, theorem ledgers, several bounded formal/replay results, and multiple characterized blockers. MATHCERT remains pending for the unresolved flagship claims.

## 2. Plain object

The campaign audits exact recurrences, companion identities, congruences, symbolic certificates, formal declarations, and finite computations for their precise relationship to odd zeta values and related periods.

## 3. Current obstruction

The flagship T3 route is neither proved nor refuted. Its surviving proof class is an exact two-dimensional rational delta certificate or a two-stage fibre telescoper/sequence-identification certificate. T1-top and DEPTH remain separately blocked; neither may be substituted for another without a verified bridge.

## 4. Working model

Finite agreement, recurrence residuals, source admission, and local symbolic checks are evidence only. Producer/verifier separation, singularity handling, boundary terms, adversarial mutations, and predecessor failed-route exclusions remain mandatory.

## 5. Theorem-spine location

Authority begins at `campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE/00_INTAKE_AND_SOURCE_LOCK.md` and continues through protected successors. LIVE state is tracker #113, which names the current flagship and broader source-replay operations.

## 6. Debt audit

Open debt includes the T3 exact certificate/counterexample, T1-top certificate recovery or replacement, DEPTH reopening requirements, Sharp-12 gating, quarantined Lean declarations, and the separate primes `2,3` completion problem.

## 7. Claim boundary

No new irrationality, infinitude, Sharp-12 theorem, companion theorem, or certification result follows from source admission, finite computation, or this guide.

## 8. First executable step

Read tracker #113 and the current protected predecessor for the flagship T3 operation. Work only in the characterized surviving certificate class or return an exact source-normalized counterexample/blocker.

## Reader entry and prerequisites

**Status:** active bounded formal/replay routes with characterized blockers. **Audience:** graduate discrete mathematics readers and certificate/replay contributors. **Time to first example:** 10 minutes. **Time to first fixture:** 10 minutes.

| Level | Concepts |
| --- | --- |
| Required | Binomial coefficients, finite sums, integer arithmetic |
| Helpful | Recurrences, hypergeometric identities |
| Deferred | Creative telescoping over \(\mathbb Q(n,k,\ell)\), boundary singularities, symbolic certificate proof |

## Core bridge and first examples by hand

For illustration—not as the campaign's unresolved Brown–Zudilin certificate—define the integer Apéry-style sum
\[
A_n=\sum_{k=0}^n\binom nk^2\binom{n+k}k^2.
\]

**Friendly example:** \(A_0=1\). For \(n=1\), terms \(k=0,1\) contribute 1 and 4, so \(A_1=5\).

**Boundary example:** agreement with a proposed recurrence at \(n=0,1,2\) can be tested exactly but proves no recurrence for all \(n\) and no new odd-zeta identity. In particular, finite checks cannot stand in for a rational two-dimensional telescoping certificate with all boundary terms discharged.

Bridge: finite binomial sum → exact values → candidate recurrence → universal rational identity plus boundary control → checked certificate.

## First computation or fixture

Python 3 (standard library):

```python
from math import comb
def apery(n):
    return sum(comb(n,k)**2 * comb(n+k,k)**2 for k in range(n+1))
print([apery(n) for n in range(3)])
# Expected: [1, 5, 73]
```

Inputs \(0,1,2\), finite integer-sum evaluator; expected output shown. **Support route:** exact finite calculation. **Limitation:** illustrative and independent of current Sharp-12/T3 certification.

## First theorem or local proposition

**Integrality lemma.** Every \(A_n\) above is a nonnegative integer, because its finite summands are products of squares of integer binomial coefficients. This elementary statement is not the outstanding T3 identity, a recurrence theorem, or an irrationality proof.

## Challenge ladder

| Stage | Duty | Completion test |
| --- | --- | --- |
| Exercise | Compute \(A_1\) by hand | 5 |
| Exploration | Compute \(A_2\) | 73 |
| Fixture | Replay script | Print \([1,5,73]\) |
| Lemma candidate | Prove integrality of all \(A_n\) | Use finite-sum argument |
| Open direction | Inspect one exact T3 source term | State missing \(\Delta_k R+\Delta_\ell S\) identity and boundaries |

## Certification path and continuation graph

Finite sums can be independently reproduced; an actual T3 proof needs producer/verifier separation, universal symbolic rational identity, singularity controls, and telescoping boundary checks. No current unresolved Sharp-12 claim is certified by this exercise.

`integer-sum fixture → recurrence candidate → boundary accounting → 2D telescoper [OPEN] → independent exact replay → Cert`

## Trust quartet

**Proved:** simple integrality lemma and protected local results within their own scope. **Checked:** three integer values. **Open:** T3 certificate, T1-top, DEPTH and Sharp-12. **External verification:** actual source-normalized identities, any symbolic producer's output and singularities.

## Bibliography and source audit

| Source | Role | Audit state |
| --- | --- | --- |
| [OZ-WP00 source lock](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/odd_zeta/OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE/00_INTAKE_AND_SOURCE_LOCK.md) | Normative object/source boundary | Protected Programme source |
| [OZ tracker #113](https://github.com/grandchallenge/MATH-PROGRAMME/issues/113) | Current flagship and sibling routes | LIVE only |
| Classical Apéry and Brown–Zudilin literature (linked from source lock) | Learning and imported claims | Scope varies; must be independently audited before promotion |

**First executable step / completion test:** Reproduce \([1,5,73]\), then retrieve the *actual* protected T3 term and write a bounded rational certificate ansatz with explicit singularity/boundary conditions. Do not identify this pedagogical sum with the open protected certificate without a bridge.

