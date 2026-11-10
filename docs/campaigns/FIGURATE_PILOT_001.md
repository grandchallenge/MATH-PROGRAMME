# FIGURATE: Diophantine Tuples of Figurate Numbers

**Research status (10 November 2026):** Continuing research programme, launched as a bounded pilot on 3 November 2026. Multiple **bounded** mathematical results have since been internally proved, tested and admitted through protected repository processes, including uniform Type B obstruction and construction families and exact ray-class arithmetic. This is **not** an independent MATHCERT certification, a claim of literature priority or a complete classification.

A square number can be drawn as a square array of dots; a triangular number as a triangle. Mathematicians call these *figurate numbers*. The FIGURATE pilot asks how difficult it is to assemble collections of positive integers when every pair obeys a figurate-number constraint.

This page is an accessible companion to the [exact research specification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_PILOT_001.md). The programme distinguishes **three** mathematical types (A, B and C), which must not be conflated.

## The mathematical end-game

The ultimate question is **when figurate Diophantine tuples exist, when they cannot exist, and what arithmetic principle separates those outcomes**. For each clearly specified polygonal order, offset and tuple type, the aspiration is an exact existence criterion or a theorem covering an infinite parameter family. Complete unrestricted classification is a research ambition, **not** an announced theorem or guaranteed outcome.

The active [WP09 research track](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3145) concentrates on **Type B**: distinct positive entries whose pairwise products, after adding a fixed offset, are polygonal numbers. The [mathematical results guide](FIGURATE_RESULTS_EXPLAINED.md) records both rigorous nonexistence conditions and genuine infinite construction families. Its latest research advances concern an oriented ray-class obstruction in a recurring Pell-equation anchor family.

### From modular tests to an existence theorem

1. **Local arithmetic:** prove which congruence restrictions are necessary, using binary and odd-prime-power conditions. Local compatibility alone is not a solution.
2. **Global construction:** transform the remaining integer conditions into constrained Pell equations; prove genuine positive-index solutions when possible.
3. **Ideal-class arithmetic:** for the recurring anchor $k=16m+4$ and offset $c=2$, interpret the global condition using ideals of the **actual quadratic order** and their oriented ray classes.
4. **Decisive realization test:** determine whether an ideal of the required norm *actually represents the required ray class*. Calculating the ray-class group does not establish that such an ideal exists.
5. **Uniform conclusion:** use a proved target-class realization or obstruction to obtain an infinite parameter-family theorem for positive-integer triples or their nonexistence.

**Progress through WP09-031:** the programme has complete local criteria in stated regimes, exact Type B families, ideal-norm enumeration and targeted ray membership tests, and full oriented ray-group structures for the **odd square-conductor subfamily**. These are meaningful intermediate results, not a general resolution of Step 4 or Step 5.

**Next proposed theorem target:** resolve target-class realization uniformly for a nontrivial family, beginning where the square-conductor ray groups are already understood. Seek either a proved infinite family of actual triples or a proved infinite family with a genuine global obstruction. Extend the algebra to general conductors when it advances that question, rather than computing groups without a stated existence application.

The longer programme must separately address **Type A** (figurate entries with square pairwise outputs) and **Type C** (both entry and output restrictions). The active Type B results do not automatically imply results for either.

## Results and mathematical explanation

[**Read the mathematical guide: *Figurate tuples—existence, obstruction and global arithmetic*.**](FIGURATE_RESULTS_EXPLAINED.md)

The results guide begins with elementary, uniform nonexistence theorems from congruences (including octagonal examples), then covers odd-prime-power local tests, exact integer construction families, Pell reductions and the later ideal/ray-class analysis through WP09-031. It separates each verified theorem from the stronger, still-open global existence and classification claims. Mathematical originality and independent specialist certification remain unverified; repository admission does not certify them.

## Research completion and remaining obligations

The [bounded-pilot closure reconciliation](FIGURATE_CLOSURE_RECONCILIATION.md) records the initial work-package acceptances and the distinct original-source fidelity gap. The [continuing WP09 tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3145) records later protected research and public admissions. **Completion of WP09-031 is not closure of the Type B local-to-global problem or of FIGURATE.** The original 2025 article is not yet source-audited in full, and independent mathematical certification and literature novelty remain unresolved.

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

## Original four pilot work packages

The list below describes the **initial November 3 pilot architecture**, not a count of current work packages. Later work through WP09 is tracked separately.

1. **WP01: sources and novelty.** Pin original literature, separate definitions, confirm open conjectures and record prior constructions and exclusions.
2. **WP02: computational census.** Run reproducible, independently checked surveys over polygonal orders and offsets; record costs, exact bounds and witness hashes.
3. **WP03: arithmetic obstructions.** Develop modular residue exclusions and simultaneous Pell-type reductions with precisely proved hypotheses.
4. **WP04: theorem attempt.** Seek a genuinely new parameter-uniform obstruction, a new infinite construction or a rigorous algorithmic result. Route substantive claims through the appropriate mathematical review and certification process.

The bounded pilot has produced source-linked proof dossiers and exact computations; the larger programme continues because the general existence/classification objective remains open. Internal mathematical results are not by themselves a novelty determination or external certification.

## Documentary library

The core documentary records serve distinct purposes:

- [Source-critical bibliography and novelty ledger](FIGURATE_SOURCES.md): precise distinctions between published theorems, conjectures, offset-specific restrictions and new research questions.
- [Reproducible bounded census](FIGURATE_CENSUS.md): full parameter domain, the 270-row archive, exact replay and finite-search limitations.
- [Research preprint, version 0.1](FIGURATE_PREPRINT.md): an **earlier** arXiv-style methods draft, not an automatically updated account of later WP09 results or a submitted article.
- [Current mathematical results and synthesis](FIGURATE_RESULTS_EXPLAINED.md): what is proved, how the evidence relates and which global realization theorem is still missing.
- [Bounded-pilot closure reconciliation](FIGURATE_CLOSURE_RECONCILIATION.md): accepted early deliverables versus outstanding primary-source and certification obligations.

## Evidence, governance and continuity

- [Canonical FIGURATE pilot charter, MATH-PROGRAMME #3093](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3093)
- [Continuing Type B research and protected WP09 evidence, #3145](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3145)
- [Latest full square-conductor oriented ray-group dossier, WP09-031](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_FULL_RAY_GROUP_031.md)
- [MATHSOLVE source specification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_PILOT_001.md)
- [Protected implementation and checks, PR #1175](https://github.com/grandchallenge/MATHSOLVE/pull/1175)
- [Research source](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_census.py) and [regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_census.py)

**Continuity boundary:** Initial charter and computational baselines, multiple bounded Type B mathematical dossiers and public explanations are protected-admitted. The WP09 target-class realization and wider parameter-classification questions remain active; the primary-source fidelity gap and independent MATHCERT certification remain separate. This overview reports programme direction and admitted evidence; it does not assert a universal existence theorem, a public priority determination or live-site deployment verification.
