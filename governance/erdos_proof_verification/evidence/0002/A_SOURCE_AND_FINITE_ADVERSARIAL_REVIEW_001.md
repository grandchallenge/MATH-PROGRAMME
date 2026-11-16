# Erdős #2 — Phase A source/scope and finite adversarial review

**Assignment:** `ERDOS-PV-0002-A` (queue [#3212](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3212)); source [#1271](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1271), now CLOSED, exactly two comments. Source issue body SHA-256 `65e4ef993de9e9c69ac5ca9f21c9d784f5553f79fafed42cf197f38a3295e54d`, freshly checked by authenticated GitHub API (CHAD capture `a26d43df548345ae8fef30f4d0741cdc`).

## Exact theorem scope

A distinct covering system is a **finite** collection of one congruence class `a_i (mod m_i)` per modulus, with `1 < m_1 < ... < m_k`, covering every integer. The original question asks whether the smallest modulus can exceed *every* fixed threshold. Hough's [published Theorem 1](https://annals.math.princeton.edu/2015/181-1/p06), *Annals of Mathematics* 181 (2015), pp. 361–382, bounds `m_1 <= 10^16`. Balister–Bollobás–Morris–Sahasrabudhe–Tiba, *Inventiones Mathematicae* 228 (2022), pp. 377–414, [arXiv:1811.03547v1](https://arxiv.org/abs/1811.03547v1), Theorem 8.1, forbids coverings when all distinct moduli are at least 616000, so `m_1 <= 615999`. This resolves the original unboundedness question **negatively**, not the exact maximum minimum modulus.

These primary-source identities, theorem thresholds and quantifiers were established in the previous [authenticated source audit](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1271#issuecomment-6256012770) and separate [role-scoped critic](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1271#issuecomment-6472247244). They are **reused**, not represented as a new proof replay. Distinct moduli, one residue per modulus and the finite-family hypothesis are essential; a family with modulus repeated cannot support the distinct-system theorem. The odd-covering problem #7 is different.

The immutable catalogue identity remains `teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89:data/problems.yaml`, blob `4e60263a80af6207aca494d2e1388e44fa372889`; frozen status DISPROVED. Current external [optimization constant 90a](https://teorth.github.io/optimizationproblems/constants/90a.html) reports an **unrefereed** 2026 machine-checked lower-bound example with minimum modulus 44, while the earlier GCL source audit cited 42. No independent replay, axiom audit or formal certification of the 44 result was performed here. The 2026 entry is recorded as **source drift**, not silently substituted for the protected source lock.

## Fresh exact finite adversarial check

For any fixed finite list, `L=lcm(m_i)` is a period: testing all residues `0,...,L-1` exhaustively decides coverage of **all integers** for *that particular list*. The following check was actually executed on authenticated CHAD with result `ADVERSARIAL_FINITE_CHECK PASS` (capture `a26d43df548345ae8fef30f4d0741cdc`):

```python
from math import lcm
def audit(rows):
    moduli = [m for a,m in rows]
    L = lcm(*moduli)
    distinct = len(set(moduli)) == len(moduli) and all(m>1 for m in moduli)
    uncovered = [x for x in range(L) if not any((x-a)%m == 0 for a,m in rows)]
    return distinct, L, uncovered
original = ((0,2),(0,3),(1,4),(3,8),(7,12),(23,24))
assert audit(original) == (True,24,[])
assert audit(original[:-1]+((24,24),)) == (True,24,[23])
assert audit(((0,2),(1,2))) == (False,2,[])
```

Thus Hough's six-class example really covers all integers; mutating its final class leaves residue 23 uncovered; repeating modulus 2 gives a trivial cover outside the distinct-modulus scope. These are genuinely exhaustive **small finite calculations**, not the analytic 616000 theorem.

## Role-scoped review and disposition

Source critic: prior semantic review #1271/6472247244. Fresh verifier: live source-body hash and lease readback, positive and hostile finite fixtures. Adversarial logical checks: repeated-modulus false transfer, finite vs arbitrary source-family confusion, threshold strictness, exact-optimum overclaim, external Lean-badge equivocation, and unrefereed 2026 source drift. They all preserve the bounded source conclusion. The same authenticated actor executed these steps, so no distinct-human or independent public certification is claimed.

**Disposition:** source-scope candidate ready for protected Phase A admission, reusing prior critically reviewed source work. Stage B proposed scope: independently formalize the finite periodicity/LCM reduction and the six-class example with a pinned Lean 4/mathlib build, exact types, `#print axioms`, and mutated negative tests. An external purported Lean result does not replace source-pinned replay. Stages B/C/D, the analytical published proofs, exact extremal constant, MATHCERT and other cohort items remain uncompleted.
