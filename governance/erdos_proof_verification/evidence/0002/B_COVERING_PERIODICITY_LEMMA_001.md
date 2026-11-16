# Erdős #2 — exact finite covering-system periodicity theorem

Assignment: `ERDOS-PV-0002-B`; bounded independent derivation. Source audit [#1271](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1271) has body SHA-256 `65e4ef993de9e9c69ac5ca9f21c9d784f5553f79fafed42cf197f38a3295e54d`. Protected predecessor: [PR #3369](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3369), merge `7d15d5a8ddc0b3d7117fd146e4325d62085b06a0`, with exact source/evidence admission `3869f60eec64dfffbeca1ac826f652ec267d10fd`.

**Proof scope:** one elementary but universal finite periodicity/reduction lemma and an exactly checked six-class construction. This is **not** a reproof of Hough's 2015 analytic upper bound or the Balister–Bollobás–Morris–Sahasrabudhe–Tiba 2022 improvement. The latter establish that Erdős #2's historical least-modulus-unboundedness question is false; the present lemma by itself does not imply any universal maximum.

## Theorem — finite integer congruence period reduction

Let (I) be a finite index set (possibly empty). For every (i\in I), let (a_i\in\mathbb Z) and (m_i\in\mathbb Z) with (m_i\geq2). Define

$$
S=\bigcup_{i\in I}\{a_i+m_i k:k\in\mathbb Z\},
\qquad
L=\mathrm{lcm}_{i\in I}m_i
$$

with (L=1) when (I) is empty. Then (L\geq1), and **for every integer (z)** with Euclidean remainder (r=z\bmod L\in\{0,\ldots,L-1\}),

$$
z\in S\quad\Longleftrightarrow\quad r\in S.
$$

Consequently:

1. (S+L=S): the covered set is exactly periodic with period (L) (not necessarily least period).
2. (S=\mathbb Z\) if and only if **every** residue (0\leq r<L) belongs to (S).
3. If at least one such residue is uncovered, **all** integers congruent to it modulo (L) are uncovered.
4. The theorem requires no pairwise-distinctness hypothesis. For *Erdős #2*, pairwise distinct positive moduli and one class per modulus are an additional, independent admissibility condition.

### Complete proof

By the definition of least common multiple, for each (i\in I) there exists an integer (q_i) with (L=q_i m_i). Euclidean division gives (z=tL+r) for a unique (r\in\{0,\ldots,L-1\}). Therefore

$$
z-a_i=tq_i m_i+(r-a_i).
$$

Thus (m_i\mid(z-a_i)) if and only if (m_i\mid(r-a_i)), because the difference of these two numbers is a multiple of (m_i). This equivalence holds separately for every class, so existentially quantifying over (i\in I) yields (z\in S\iff r\in S). The same divisibility relation gives (z\in S\iff z+L\in S), proving periodicity. Since every integer has one of those (L) remainders and every remainder is itself an integer, covering all integers is equivalent to covering all remainders. If a remainder (r) is missing, no integer (r+tL) can be in (S).

When (I=\varnothing), (S=\varnothing), (L=1), and both sides of the equivalence are false for every (z); the covering criterion also correctly fails at remainder (r=0). This completes the proof, including all signs and the empty-family edge case.

## Fully finite positive certificate

The six source-listed congruences are

$$
(0\bmod2),\ (0\bmod3),\ (1\bmod4),\ (3\bmod8),(7\bmod12),\ (23\bmod24).
$$

Their moduli are pairwise distinct, all greater than 1, and their least common multiple is **24**. The governed JSON fixture gives one index (zero-based, ordered as above) for each residue from 0 to 23:

`[0,2,0,1,0,2,0,4,0,1,0,3,0,2,0,1,0,2,0,3,0,1,0,5]`.

For each residue (r) the indexed congruence is satisfied; an **independent direct membership scanner** checks every index. Therefore all 24 residues are covered, and the theorem proves coverage of the entire integer line. This is a constructed finite example, not a demonstration of the deep upper bound on the least modulus of *every* distinct covering system.

## Independent adversarial and resource checks

- Change only the last class to `24 mod 24`. The independently checked uncovered-residue list becomes exactly `[23]`, so this altered system fails to cover (\mathbb Z).
- The two classes `0 mod 2` and `1 mod 2` cover all integers, but share the same modulus, so **fail** Erdős #2's distinctness requirement.
- The empty list yields (L=1) and uncovered residue `[0]`; a single class `0 mod 2` misses residue `[1]`.
- Negative representatives are handled by Euclidean remainder; `23 mod 24`, `-1 mod 24`, and `191 mod 24` denote the same class.
- The exact bounded verifier rejects nonpositive/nonintegral moduli and refuses to pronounce truth when (L) exceeds the explicit computational cap. Resource exhaustion is **not** a counterexample.
- All **144** choices of one residue for each modulus (2,3,4,6) were exhaustively checked against an independent direct congruence comparator for every integer (x\in[-2L,2L]). Per-family proof of general periodicity is from the argument above, not inferred by extrapolating those tests.

Implementation: `ci/erdos_pv_covering_periodicity.py`. Governed adversarial suite: `ci/test_erdos_pv_covering_periodicity.py`. Frozen certificate: `governance/erdos_proof_verification/evidence/0002/B_COVERING_PERIODICITY_FINITE_FIXTURES_001.json`, SHA-256 `f7241455b220050df1558aedc5a69fe4c384bfd3e42cf657f6ee7821f8705c84`. The source run is deterministic and CI-regenerated; finite fixture checks are subordinate to the explicit universally quantified proof above.

## Verification ladder and next obligation

**Established by direct reasoning:** the period-reduction theorem under (m_i\geq2), including (I=\varnothing), and the source-compatible six-class coverage through an exhaustive 24-residue certificate.

**Established by computation, narrowly:** 16 adversarial unit tests, three exact fixture families, 144 exhaustively chosen small distinct-modulus systems and direct integer comparisons. CHAD execution is authenticated as an OS action; it is *not* an independent external mathematical review or a Lean kernel proof.

**Not established:** an independent analytical proof of Hough's `m_1<=10^16` theorem or BBMST's `m_1<616000` improvement; any exact optimal least modulus; external 2026 claims about an example with minimum modulus 44; a frozen Problem-2 FormalConjectures declaration; Lean replay or axiom audit; MATHCERT certification.

Next `ERDOS-PV-0002-C`: normalize this theorem and the six-class instance to exact pinned Lean 4/mathlib statements, compile with no `sorry`/`admit`, print theorem types and axioms, replay hostile altered-family controls, and conduct independent logical/formal applicability review. The next phase is not admitted by the present ordinary mathematical proof.
