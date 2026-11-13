# Erdős #1: bounded binary-block transfer, proof and exact scope

Work item: `ERDOS-PV-0001-B`; cohort #3212/#3225; original audited issue #1270.
Status: **bounded mathematical lemma reconstructed**, not a proof of the
complete Erdős #1 disproof, not a Lean kernel execution and not MATHCERT.

## Exact source lock and assumptions

Source: `tadamcz/erdos1@db6f9091dfaf9bac704e6b28fb3a094594869328`,
`Erdos1/Resolutions/Erdos1_219usd_38h.lean`, blob
`07d2f36647a2319e65c0c8c756527460925e9075`.
Original benchmark statement provider:
`google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020`,
`FormalConjectures/ErdosProblems/1.lean`, blob
`c8aa6e1889b02f48b18164df3dce518a80409b27`.
Source-audit review: #1270, comments #6099562233 and #6249309294.

Let $I$ be a finite index type of size $d$, let $k\geq 1$, and let
$a_i$ be positive integers with $a_i\leq W$ for all $i\in I$.
Assume *bounded integer-relation freedom*:

$$
\left(\forall i,\ |c_i|<2^k\right)
\land \sum_{i\in I} a_i c_i=0
\quad\Longrightarrow\quad
\forall i,\ c_i=0
$$

for every family of integer coefficients $c_i$.

Define the indexed binary-block weights

$$
w_{i,j}=a_i 2^j,\qquad i\in I,\quad 0\leq j<k.
$$

**Claim.** The $dk$ weights are distinct positive integers no greater
than $W2^{k-1}$, and all their subset sums are distinct.

## Independent reconstruction of the transfer argument

Suppose two subsets of indexed positions have the same weight sum.
Subtract their characteristic functions. Their difference at each
$(i,j)$ is a signed digit $\varepsilon_{i,j}\in\{-1,0,1\}$.
Consequently,

$$
0=\sum_{i\in I}\sum_{j=0}^{k-1}
    a_i\varepsilon_{i,j}2^j
 =\sum_{i\in I}a_i c_i,
\qquad
c_i:=\sum_{j=0}^{k-1}\varepsilon_{i,j}2^j.
$$

For every $i$, the triangle inequality gives

$$
|c_i|\leq\sum_{j=0}^{k-1}2^j=2^k-1<2^k.
$$

The stated integer-relation freedom therefore forces all $c_i=0$.

To recover the *individual digits* from a zero signed-binary sum,
reduce the equality for each $c_i$ modulo two: the lowest digit
$\varepsilon_{i,0}$ is even, and the only even member of
$\{-1,0,1\}$ is zero. Divide the remaining equality by two and
repeat inductively. Thus each $\varepsilon_{i,j}=0$, hence the
original subsets were identical.

Distinct singleton subsets have different sums, so the indexing map
$(i,j)\mapsto w_{i,j}$ is itself injective; there are exactly $dk$
**distinct** weights. Positivity and the upper bound follow from
$a_i>0$, $a_i\leq W$, and $j\leq k-1$.
This verifies the asserted bounded transfer theorem.

## Executable falsification fixtures

The lightweight deterministic Python check is
`python3 ci/erdos_pv_binary_blocks.py`.
Its source is accompanied by exact frozen output:
`governance/erdos_proof_verification/evidence/0001/BINARY_BLOCK_FINITE_FIXTURES_001.json`.
The fixture payload SHA256 is
`4d3945b9df088715da74cfff480165a8437e7f4a55c670fffb05a38b68312f8b`.

- Positive $(a,k)=((1,5),2)$: no bounded nonzero integer relation,
  four distinct weights $[1,2,5,10]$ and all 16 subset sums unique.
- Positive $((1,9),3)$: relation-free with $|c_i|<8$, six weights
  $[1,2,4,9,18,36]$ and all 64 subset sums unique.
- Adversarial $((1,3),2)$: the relation $(3,-1)$ violates the hypothesis.
  Weights $[1,2,3,6]$ have only 13 different subset sums; in particular
  $1+2=3$. This is not a counterexample to the conditional lemma.

## Claim boundary and next stage

The proof reconstructs the *binary-block transfer* assuming a
relation-free family exists. The deep, source-dependent construction
of families that disprove the **uniform subset-sum lower bound** is
not proved here. A finite regression is not a proof of a universal
theorem; the separate argument above provides the general transfer.

The pinned Formal Conjectures file contains a `sorry` for the
historical uniform lower-bound assertion; no GCL replay of the
author's full disproof, no formal replay of this lemma, no admissible
kernel/axiom transcript and no external independent reviewer are
claimed. The necessary next stage is formal applicability and
adversarial validation of this exact bounded lemma under Phase C.
