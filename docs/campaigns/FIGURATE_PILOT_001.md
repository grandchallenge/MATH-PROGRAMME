# FIGURATE: Diophantine Tuples of Figurate Numbers

**Research status:** Active bounded pilot, launched 3 November 2026. **No new theorem or mathematical certification is claimed.**

A square number can be drawn as a square array of dots; a triangular number as a triangle. Mathematicians call these *figurate numbers*. The FIGURATE pilot asks how difficult it is to assemble collections of positive integers when every pair obeys a figurate-number constraint.

This page is an accessible companion to the [exact research specification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_PILOT_001.md). It distinguishes two different research questions that must not be confused.

## New: a guide to the unbounded obstruction results

[**Read the illustrated-by-examples mathematical explanation: *When three numbers cannot coexist*.**](FIGURATE_RESULTS_EXPLAINED.md)

The updated FIGURATE research goes beyond counting small tuples. A complete modular argument rules out **all Type B triples**, without any numerical entry bound, for polygonal orders divisible by 8 and offsets congruent to 2, 3, or 6 modulo 8. A second family occurs for polygonal orders congruent to 12 modulo 16 and offsets congruent to 2 modulo 4. The linked guide develops the result from parity and remainders, gives a worked octagonal example, and explains how the independently verified finite residue tables yield unbounded conclusions. Mathematical originality and independent specialist certification remain unverified; repository admission does not certify them.

## What is a figurate number?

The polygonal number of order $k$ at index $t$ is

$$
P_k(t)=\frac{(k-2)t^2-(k-4)t}{2}, \qquad k\geq3,\quad t\geq1.
$$

For $k=3$, the values are triangular numbers $1,3,6,10,15,\ldots$. For $k=4$, the values are squares $1,4,9,16,25,\ldots$. For $k=5$, the values are pentagonal numbers $1,5,12,22,35,\ldots$.

## Two mathematically different kinds of tuple

**Type A: figurate entries.** Every member of the tuple is figurate, and the product of any distinct pair, plus a fixed integer $n$, is a square:

$$
a_i=P_k(t_i), \qquad a_i a_j+n=x_{ij}^{2}\quad (i<j).
$$

**Type B: figurate pairwise outputs.** The tuple entries are arbitrary distinct positive integers, but the product of any pair plus a fixed integer $c$ must be a figurate number:

$$
a_i a_j+c=P_k(t_{ij})\quad (i<j).
$$

**Type C** imposes both a figurate-entry constraint and figurate pairwise outputs. The polygonal order and offsets must be explicitly declared for each experiment.

A result for one type is not automatically a result for another.

### Two examples

The classical Diophantine quadruple $\{1,3,8,120\}$ has the property that each pairwise product plus $1$ is a square: the resulting values are $4,9,121,25,361,961$. Because squares are polygonal numbers of order $4$, it is also a Type B example with $k=4,c=1$.

The triple $\{1,2,27\}$ is a Type B triangular example with $k=3,c=1$, because

$$
1\cdot2+1=3=T_2,\quad 1\cdot27+1=28=T_7,\quad 2\cdot27+1=55=T_{10}.
$$

Neither example is a newly discovered GCL result.

## Why the problem connects to Pell equations

Membership in a polygonal sequence can be transformed into a constrained square equation:

$$
\bigl(2(k-2)t-(k-4)\bigr)^2=8(k-2)P_k(t)+(k-4)^2.
$$

For Type B, substitute $P_k(t)=ab+c$. A square discriminant is a useful search filter, but is **not** on its own sufficient: the recovered polygonal index must be positive and integral, including the required sign and divisibility constraints.

Requiring every pair in a tuple to satisfy its own equation couples several quadratic equations. This makes extension of a triple to a quadruple a nontrivial arithmetic question.

## What was known before FIGURATE?

In August 2026, Sounak Bagchi and Christian Zhou-Zheng studied Type A triangular $D(n)$ tuples. They proved that **no Type A triangular $D(1)$ quadruple exists**, exhibited an infinite triple family, and conjectured that their family describes every triangular $D(1)$ triple. They also proved that Type A triangular $D(n)$ pairs do not exist for $n$ congruent to $2$ or $5$ modulo $9$. See [their paper](https://arxiv.org/abs/2608.27697).

In July 2026, Alan Filipin, Ana Jurasić and Alain Togbé studied Type B triangular $D(n)$ sets. They proved that the specified pairs $\{k,2k\}$ for $k=10$ and $k=28$ cannot be extended to a quadruple. The conclusion is **not** a blanket prohibition on Type B triangular quadruples. See [the journal article](https://doi.org/10.2478/auom-2026-0018).

The earlier and wider literature includes triangular-set extension results and other Diophantine tuples. [Andrej Dujella's bibliography](https://web.math.pmf.unizg.hr/~duje/ref.html) is a reference locator, not a substitute for checking theorem statements against original sources. The novelty audit is still open.

## What GCL has implemented

The current [MATHSOLVE exact-arithmetic census](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_census.py) enumerates compatible tuples with distinct positive entries bounded by a declared maximum, explicit polygonal order, offset and tuple size. It produces deterministic JSON with pairwise integer witnesses and performs no floating-point computation.

[Regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_census.py) compare selected small cases against independent brute-force enumeration. The baseline was admitted in [MATHSOLVE PR #1175](https://github.com/grandchallenge/MATHSOLVE/pull/1175); this is engineering admission, **not** mathematical certification.

Reproduce the baseline from a MATHSOLVE checkout:

```sh
python3 -m unittest discover -s tests -p test_figurate_census.py
python3 -m research.figurate_census --kind B --k 3 --offset 1 --limit 100 --size 3
```

The limit is the maximum **entry value**, not the maximum figurate index. Exhaustive output within declared bounds never establishes global nonexistence.

## Four work packages

1. **WP01: sources and novelty.** Pin original literature, separate definitions, confirm open conjectures and record prior constructions and exclusions.
2. **WP02: computational census.** Run reproducible, independently checked surveys over polygonal orders and offsets; record costs, exact bounds and witness hashes.
3. **WP03: arithmetic obstructions.** Develop modular residue exclusions and simultaneous Pell-type reductions with precisely proved hypotheses.
4. **WP04: theorem attempt.** Seek a genuinely new parameter-uniform obstruction, a new infinite construction or a rigorous algorithmic result. Route substantive claims through the appropriate mathematical review and certification process.

The pilot continues only if its evidence supports an original theorem, a rigorously improved algorithm, or a credible proof programme. All other findings retain their narrower computational or conjectural status.

## Documentary library

The documentary accompaniment is now organized as three separate, source-linked records:

- [Source-critical bibliography and novelty ledger](FIGURATE_SOURCES.md): precise distinctions between published theorems, conjectures, offset-specific restrictions and new research questions.
- [Reproducible bounded census](FIGURATE_CENSUS.md): full parameter domain, the 270-row archive, exact replay and finite-search limitations.
- [Research preprint, version 0.1](FIGURATE_PREPRINT.md): arXiv-style methods manuscript, elementary identities, computational table and research agenda. It is a research draft, **not** a submitted article or a proved new theorem.

## Evidence, governance and continuity

- [Canonical FIGURATE pilot charter, MATH-PROGRAMME #3093](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3093)
- [MATHSOLVE source specification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_PILOT_001.md)
- [Protected implementation and checks, PR #1175](https://github.com/grandchallenge/MATHSOLVE/pull/1175)
- [Research source](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_census.py) and [regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_census.py)

**Continuity boundary:** The charter and technical baseline are admitted. The primary-source documentary catalogue, bounded parameter survey and preliminary manuscript have source editions; full-proof semantic review, larger search frontier, theorem attempt and formal certification remain open. Publication of this explanatory page does not promote those research obligations to completion.
