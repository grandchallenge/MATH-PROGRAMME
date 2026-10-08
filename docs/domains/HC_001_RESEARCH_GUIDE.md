# HC-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [HC-001 canonical tracker #65](https://github.com/grandchallenge/MATH-PROGRAMME/issues/65).  
    **AUTHORITY:** `DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md`.  
    **EXPOSITION:** this guide explains current protected state; it does not promote a new algebraicity theorem.

## 1. Status

The rational Hodge conjecture remains open. The campaign has a source-normalized problem boundary, known-case ledger, statement lattice, false-proof controls, and a protected theorem/dependency spine. No restricted post-WP00 theorem target has yet been promoted.

## 2. Plain object

For every smooth projective complex variety `X` and codimension `p`, the target is surjectivity of the rational cycle-class map onto rational Hodge classes of type `(p,p)`.

## 3. Exact obstruction

The easy direction—algebraic cycle classes have Hodge type `(p,p)`—is not the conjecture. The open direction is to construct algebraic cycles representing arbitrary rational Hodge classes while preserving projectivity, rational coefficients, codimension, cohomology theory, and universal quantifiers.

## 4. Working model

The campaign explicitly rejects substitution by the integral Hodge conjecture, unrestricted compact-Kähler analogues, Hodge-locus algebraicity, motivated/absolute Hodge classes, numerical period recognition, or Tate-style specialization without a proved bridge.

## 5. Theorem-spine location

Authority is `DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md`. LIVE coordination is tracker #65. The protected baseline includes the known cases `p=0,1,n-1,n` and the dimension-at-most-three consequence; those are boundary conditions, not evidence for the unrestricted conjecture.

## 6. Debt audit

The first new unrestricted case is fourfolds in codimension two. Before opening mechanism work, the campaign still needs one exact restricted target with variety class, dimension, codimension, coefficient ring, cycle equivalence, implication direction, and certification boundary fixed.

## 7. Claim boundary

No new Hodge case, algebraicity algorithm, numerical certification, novelty, or priority claim is admitted.

## 8. First executable step

Select one exact post-WP00 restricted theorem obligation and register its full formulation boundary before any Solve-owned proof or computation begins.

## Reader entry and prerequisites

**Status:** rational Hodge conjecture open; protected formulation and known-case boundary only. **Audience:** graduate geometry students and research collaborators. **Time to first example:** 10 minutes. **Time to first fixture:** 10 minutes.

| Level | Concepts |
| --- | --- |
| Required | Cohomology degree, complex projective space, codimension |
| Helpful | Divisors, algebraic cycles, Hodge decomposition |
| Deferred | Intersection theory, motives, period comparison, deformation theory |

## Core bridge and first examples by hand

A codimension-\(p\) algebraic subvariety determines a cohomology class of degree \(2p\) and Hodge type \((p,p)\). The conjecture asks for the converse **with rational coefficients** on all smooth projective complex varieties.

**Friendly example:** on \(X=\mathbb P^1_\mathbb C\), the class of any point generates \(H^2(X,\mathbb Q)\). This is an established divisor case of Lefschetz \((1,1)\).

**Boundary example:** on a smooth projective fourfold, codimension 2 involves rational classes in \(H^4\cap H^{2,2}\). Knowing the divisor case \(p=1\) does **not** supply algebraic cycles for every \(p=2\) class. This is an unproved extension, not a counterexample.

Bridge: point/divisor cycle → cycle class → rational Hodge type → proved low-codimension boundary → missing universal converse.

## First computation or fixture

This Python 3 finite **indexing** fixture identifies first potentially nontrivial internal codimensions; it computes no Hodge groups:

```python
def internal_codimensions(n):
    known = {0, 1, n-1, n}
    return [p for p in range(n+1) if p not in known]
for dimension in (1, 2, 3, 4):
    print(dimension, internal_codimensions(dimension))
# Expected:
# 1 []
# 2 []
# 3 []
# 4 [2]
```

**Support route:** regression of the known-case indexing statement. **Limitation:** this is not proof of any new Hodge case.

## First theorem or local proposition

**Point case on \(\mathbb P^1\).** The class of one closed point generates \(H^2(\mathbb P^1,\mathbb Q)\), so the rational cycle-class map in codimension one is surjective. This is a classical imported result, not a new GCL theorem; its complete geometric proof and foundations belong to the sources in the protected master plan.

## Challenge ladder

| Stage | Duty | Completion test |
| --- | --- | --- |
| Exercise | Compute codimension of a point in \(\mathbb P^1\) | One |
| Exploration | Enumerate \(p=0,1,n-1,n\) for \(n\le4\) | Identify \((4,2)\) as the first residual |
| Fixture | Run indexing code | Match four displayed lines |
| Lemma candidate | State exact point cycle-class surjectivity | Specify \(X,p,\mathbb Q\) |
| Open direction | Register one restricted fourfold family | Preserve projectivity, rational coefficients and known-case limits |

## Certification path and continuation graph

The indexing fixture is replayable; the divisor theorem is imported from a classical source. A new restricted class would require a theorem statement, geometric hypotheses, provenance, and a Solve→Cert interface.

`point class → divisor cycle map → known-case catalog → specified fourfold codimension-2 target → proof/source audit → Cert handoff`

## Trust quartet

**Proved:** classical cases within their established scope. **Checked:** only the indexing toy fixture. **Open:** unrestricted rational Hodge surjectivity. **External verification:** imported Hodge-theoretic and algebraic-cycle theorems and any new restricted result.

## Bibliography and source audit

| Source | Role | Audit state |
| --- | --- | --- |
| [HC master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md) | Locked statement and known-case boundary | Protected authority |
| [Tracker #65](https://github.com/grandchallenge/MATH-PROGRAMME/issues/65) | Route selection | Mutable LIVE |
| Lefschetz \((1,1)\) and hard Lefschetz (sources in master plan) | Imported established cases | Not newly certified by guide |

**First executable step / completion test:** Run the indexing fixture and write a proposed restricted case with exact dimension/codimension/coefficient profile and a source-backed proof obligation; do not claim it is solved.

