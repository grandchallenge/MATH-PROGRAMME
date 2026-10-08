# BSD-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [BSD-001 canonical tracker #66](https://github.com/grandchallenge/MATH-PROGRAMME/issues/66).  
    **AUTHORITY:** `DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`.  
    **EXPOSITION:** this guide explains current protected state; it does not promote a BSD theorem.

## 1. Status

The Birch–Swinnerton-Dyer conjecture remains open. WP00–WP04 have normalized the source and statement lattice, built false-proof and theorem ledgers, audited computational/formal substrate, and selected restricted target `BSD-R2-A1`. That target remains unproved.

## 2. Plain object

The campaign keeps three obligations separate: Mordell–Weil rank equals analytic rank; finiteness of the Tate–Shafarevich group; and the refined leading-term formula with periods, regulator, Tamagawa numbers, torsion, and normalization data explicit.

## 3. Exact obstruction

A parity theorem, family theorem, one-prime result, finite curve computation, or `p`-adic formula does not establish the universal complex conjecture. The selected restricted target must be proved under its exact one-prime and nonvacuity firewalls before it can enter certification.

## 4. Working model

Future theorem work is Solve-owned. The protected Programme stack supplies source normalization, false-proof exclusions, theorem dependencies, bounded computation, and target selection; it does not silently confer theorem status.

## 5. Theorem-spine location

Authority is `DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`; LIVE state is tracker #66. The current bounded target is `BSD-R2-A1`.

## 6. Debt audit

Open debt is the proof package for `BSD-R2-A1`: exact local/global hypotheses, source dependencies, one-prime firewall, nonvacuity boundary, and a clean MATHCERT handoff.

## 7. Claim boundary

The rank equality, refined formula, finiteness of `Sha`, and `BSD-R2-A1` remain unproved. Computation and formal interfaces do not substitute for theorem proof.

## 8. First executable step

Construct the Solve-owned `BSD-R2-A1` proof package from the protected target contract. Do not promote finite examples, statistics, or nonvacuity witnesses.

## Reader entry and prerequisites

**Status:** BSD open, restricted target \(BSD\)-\(R2\)-\(A1\) unproved. **Audience:** graduate arithmetic readers and source auditors. **Time to first example:** 10 minutes. **Time to first fixture:** 10 minutes.

| Level | Concepts |
| --- | --- |
| Required | Modular arithmetic, polynomial equations, rational numbers |
| Helpful | Elliptic curves, group law, analytic functions |
| Deferred | Heights, Selmer groups, \(\Sha\), \(L\)-functions and leading-term normalizations |

## Core bridge and first examples by hand

**Friendly example:** the curve \(y^2=x^3-x\) has rational point \((0,0)\), since both sides vanish. Its reduction modulo 5 can also be checked by finite enumeration.

**Boundary example:** finding points modulo 5 does not determine the Mordell–Weil rank over \(\mathbb Q\), the order of vanishing of a complex \(L\)-function, or finiteness of \(\Sha\). Even a complete count over **one** finite field lacks the needed global-to-analytic bridge.

Bridge: rational curve equation → local finite-field points → arithmetic data → complex analytic rank → conjectural global rank equality.

## First computation or fixture

Python 3, an exact finite point count for one displayed polynomial:

```python
p = 5
points = [(x, y) for x in range(p) for y in range(p)
          if (y*y - (x*x*x-x)) % p == 0]
print(points)
print("affine", len(points), "projective", len(points)+1)
# The extra point is the point at infinity on this nonsingular projective cubic.
```

Inputs \(p=5\), the polynomial and explicit enumeration are fixed; output is the enumerated list and its counts. The command is independently executable. **Support route:** exact finite arithmetic, not a rank proof or certificate of BSD.

## First theorem or local proposition

**Pairing lemma (odd characteristic).** For fixed \(x\in\mathbb F_p\), solutions of \(y^2=f(x)\) occur as \(y\) and \(-y\), except \(y=0\), which pairs with itself. This follows from \(y^2=(-y)^2\) and explains the parity pattern in finite point counts. It says nothing about analytic rank.

## Challenge ladder

| Stage | Duty | Completion test |
| --- | --- | --- |
| Exercise | Verify \((0,0)\) lies on the displayed curve | Substitute both coordinates |
| Exploration | Count solutions for each \(x\pmod5\) | Reconcile with script |
| Fixture | Re-run finite enumeration | Exact same list and counts |
| Lemma candidate | Prove pairing of \(\pm y\) | Handle \(y=0\) explicitly |
| Open direction | Read exact \(BSD\)-\(R2\)-\(A1\) profile | State one-prime/nonvacuity conditions without relaxing them |

## Certification path and continuation graph

Finite point enumeration is independently replayable. Any arithmetic/analytic rank claim needs theorem-grade local/global dependencies and an exact Cert interface; finite counts do not certify it.

`finite-field point fixture → local pairing lemma → exact global hypotheses → BSD-R2-A1 [OPEN] → checked theorem handoff`

## Trust quartet

**Proved:** elementary pairing under odd characteristic. **Checked:** one finite field point count. **Open:** BSD rank equality, \(\Sha\) finiteness and leading term, including \(BSD\)-\(R2\)-\(A1\). **External verification:** imported rank/\(L\)-function comparisons and local/global bridges.

## Bibliography and source audit

| Source | Role | Audit state |
| --- | --- | --- |
| [BSD master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md) | Statement and target contract | Protected Programme authority |
| [Tracker #66](https://github.com/grandchallenge/MATH-PROGRAMME/issues/66) | LIVE stage routing | No theorem authority |
| Classical Mordell–Weil and BSD literature (source ledger in master plan) | Mathematical prerequisites | Imported; not proved by the toy code |

**First executable step / completion test:** Reproduce the finite enumeration, verify its pairing property, and write the exact \(BSD\)-\(R2\)-\(A1\) hypotheses and missing proof node before considering a solver.

