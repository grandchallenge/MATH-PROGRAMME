# Erdős #2 — critical review of the Phase B finite periodicity lemma

**Role-scoped, non-certifying review.** The producing and criticizing roles were performed by the same authenticated GCL operator; there is no fabricated independent person, external referee, or Lean kernel attestation. The exact source statement and published-status provenance were previously reviewed in source audit #1271, comments #6256012770 and #6472247244.

## Logical obligations

The theorem is unconditional **only** for finite families of integral congruence classes with moduli at least 2. The proof uses that every modulus divides the positive common multiple (L). For each (z=tL+r), subtracting (a_i) shows that (m_imid(z-a_i)) and (m_imid(r-a_i)) have identical truth values. An existential finite disjunction preserves this equivalence. Coverage of all integers follows precisely if every residue of one full period is covered.

There is no gap from restricting attention to nonnegative (r): the Euclidean remainder exists for **negative** (z) too. Empty index sets require (L=1) and produce no covered residue, so both sides remain false. No condition of pairwise distinctness is needed for *periodicity*, but distinctness is a **separate** restriction when this theorem is used on Erdős #2. The proof does not use Hough's deep sieve, nor derive the numerical universal bound.

## Hostile controls actually executed

1. The six-class positive control, with lcm 24, has all residues witnessed. The frozen 24-entry witness vector was checked against *independent direct divisibility*, not solely against the implementation that generated it.
2. Mutation of `23 mod 24` to `24 mod 24` misses residue 23. An implementation that only checks the moduli, or silently assumes the source-list was already a cover, must fail this test.
3. The family `0 mod 2`, `1 mod 2` covers every integer but is not a distinct-covering system. A checker that silently treats *coverage* as sufficient for admissibility to Erdős #2 must fail this test.
4. Empty and singleton-even families expose false universal coverage. Negative residue representatives and shifts by multiples of the modulus expose incorrect canonicalization.
5. A forged witness, forged `covers_all_integers` claim, false `distinct_moduli` claim and wrong period are all rejected by the separately implemented direct certificate validator.
6. Invalid or nonintegral moduli, including Boolean impostors, are rejected. A period over the computational cap raises `PERIOD_EXCEEDS_RESOURCE_CAP`, never reports that the family fails to cover.
7. The 144 choices of congruence residues for pairwise distinct moduli 2,3,4,6 were enumerated exhaustively, and each computed class table was compared with direct membership for every integer in `[-2L,2L]`. This tests both covered and uncovered cases, not just one hand-selected positive instance.

Each of the 16 unit tests passed on authenticated CHAD. The mathematical proof, rather than the finite test census, establishes the period-reduction theorem for arbitrary finite inputs.

## Source and evidence quality

Source lock: catalogue `teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89:data/problems.yaml`; source-audit issue #1271 body SHA-256 `65e4ef993de9e9c69ac5ca9f21c9d784f5553f79fafed42cf197f38a3295e54d`. Phase B claim ref `refs/heads/gcl-pv-claims/ERDOS-PV-0002-B`, SHA `3f4d92596ee282919c4c115b5cd85077a5722b40`. This exact claim is held and not released until protected admission/custody.

The deterministic fixture file has SHA-256 `f7241455b220050df1558aedc5a69fe4c384bfd3e42cf657f6ee7821f8705c84`. The test suite regenerates the fixture in CI and refuses drift. Capacity is bounded to avoid consuming a large CHAD instance or exhaustively enumerating a huge common period. No repeated GraphQL population scan or Colab/GPU job is needed for a 24-residue arithmetic fixture.

## Disposition and missing bridge

**PASS — bounded general periodicity lemma and six-class finite witness, with adversarial controls.** This does not grant acceptance to the original global minimum-modulus upper-bound theorem, any external 2026 lower-bound construction, or a claimed Lean proof.

For the Phase C formal gate, the required next obligations are exact pinned Lean/mathlib theorem semantics, kernel compilation, `#print axioms`, negative fixture and source-to-formal equivalence review. Do not mark Phase C reviewed, issue #3238 available, the 100-problem cohort complete, or MATHCERT accepted on the basis of this ordinary mathematical proof.
