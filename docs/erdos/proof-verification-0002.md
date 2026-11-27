---
hide:
  - navigation
---

# Erdős problem 2: when repeating patterns cover every integer

*Verification record, 27 November 2026; Grand Challenge Labs.*

**Literature status: disproved.** Hough (2015) established a universal upper bound on the smallest modulus of a finite distinct covering system; Balister, Bollobás, Morris, Sahasrabudhe and Tiba (2022) improved the bound. GCL has reconstructed and kernel-checked the finite periodicity reduction, not the analytic universal bounds. No MATHCERT certification is claimed.

[Original problem](https://www.erdosproblems.com/2) · [Compendium article](https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0002/) · [Verification programme](../ERDOS_PROOF_VERIFICATION.md)

## The question

Imagine several clocks that ring on an integer time line. Each clock has a different integer period greater than one and one chosen phase. Can they be arranged so that at least one clock rings at every integer time, even when all periods are arbitrarily large?

A clock of period $m$ and phase $a$ covers precisely those integers $z$ for which $m$ divides $z-a$. A distinct covering system is a finite family of these classes with pairwise distinct moduli. The question was whether the smallest modulus of such a cover can be arbitrarily large.

Hough proved that the smallest modulus cannot exceed $10^{16}$. The 2022 result excludes any distinct cover in which every modulus is at least 616000. Thus every such cover has a modulus at most 615999. Neither bound identifies the exact largest possible minimum modulus. These are published conclusions from the protected source audit, not new GCL proofs.

## Why a finite check can prove an infinite statement

For a fixed finite family of classes, let $L$ be the least common multiple of its moduli (1 for an empty family). Every modulus divides $L$. Write an arbitrary integer as

$$
z=tL+r,\qquad 0\le r<L.
$$

For each class with modulus $m$, the difference between $z-a$ and $r-a$ is a multiple of $m$. Thus membership in that class is identical for $z$ and $r$. The same holds for membership in the union of all classes. Coverage of the entire integer line is therefore equivalent to coverage of every residue from 0 through $L-1$.

This is an exact reduction, not a sampling heuristic. Conversely, a missing residue certifies an infinite arithmetic progression of uncovered integers. The period need not be the least period. Distinctness is a separate condition, not a consequence of periodicity.

For example, consider these six classes, whose moduli are pairwise distinct:

| Modulus | Residue | Newly covered residues in 0–23, in this order |
| --- | --- | --- |
| 2 | 0 | 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22 |
| 3 | 0 | 3, 9, 15, 21 |
| 4 | 1 | 1, 5, 13, 17 |
| 8 | 3 | 11, 19 |
| 12 | 7 | 7 |
| 24 | 23 | 23 |

The common period is 24; the table exhausts it. Altering only the final residue to 24 leaves 23 uncovered, and therefore misses every integer congruent to 23 modulo 24. Two classes of modulus 2 with opposite residues cover all integers but are not a distinct covering system.

## The limit of this method

A finite periodicity test decides whether a **given** family covers the integers. The original question quantifies over **all** finite distinct families. There is no finite list of all possible moduli or phases supplied by the reduction. A universal bound needs further mathematics controlling how congruence classes interact; simply adding their nominal densities or checking more examples does not establish it.

## What has been verified

| Evidence | Scope |
| --- | --- |
| [Source audit](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1271#issuecomment-6256012770) and [source critic](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1271#issuecomment-6472247244) | Published theorem identities and quantifiers, reused |
| [Phase B ordinary proof](https://github.com/grandchallenge/MATH-PROGRAMME/blob/16cde008f56fb9ef3b30564e0a353f5586452a62/governance/erdos_proof_verification/evidence/0002/B_COVERING_PERIODICITY_LEMMA_001.md) | General finite periodicity, exhaustive certificate, hostile controls |
| [Phase C protected replay](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3777) | 17 audited Lean 4.33.0 Std-only declarations; no sorryAx; only propext and Quot.sound where needed; false target rejected |
| [Protected custody binding](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3792) | Exact candidate and protected evidence identity |

The registered `erdos-pv-0002-periodicity` lane performs the kernel replay, including the deliberately false altered-family target. From a suitably provisioned pinned Lean environment, run `python3 ci/erdos_pv_0002_formal_replay.py --execute`. Without Lean, the same script without `--execute` verifies frozen source and log identities only. Run `python3 ci/test_erdos_pv_covering_periodicity.py` for the finite computational controls. All evidence is retained in the [protected directory](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/governance/erdos_proof_verification/evidence/0002).

## Sources and remaining work

- Bob Hough, *Solution of the minimum modulus problem for covering systems*, Annals of Mathematics 181 (2015), 361–382, Theorem 1. [Primary paper](https://annals.math.princeton.edu/2015/181-1/p06).
- Paul Balister, Béla Bollobás, Robert Morris, Julian Sahasrabudhe and Marius Tiba, *The Erdős covering problem*, Inventiones Mathematicae 228 (2022), 377–414. [Published paper](https://doi.org/10.1007/s00222-021-01087-5), [locked preprint v1](https://arxiv.org/abs/1811.03547v1), Theorem 8.1 in the locked preprint.

The source audit records an unrefereed 2026 claim of minimum modulus 44, as a source-drift observation only; no independent GCL replay of that claim is asserted. The remaining GCL proof obligation is reconstruction and formal verification of the analytic Hough and BBMST bounds. The exact extremal constant is a separate question. GCL author and critic roles were separately scoped under one accountable operator; there is no external independent mathematical certification.
