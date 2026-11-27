# Structural Capacity Calculus

<p class="page-deck">Why do some immense collections of logical relationships yield to a handful of operations, while others resist every known shortcut?</p>

<div class="scc-status"><strong>Research edition 01 · November 2026.</strong> Author-derived algebraic results and bounded exact regression; protected research records are not mathematical certification. No unrestricted superpolynomial lower bound or resolution of P versus NP is claimed.</div>

<figure class="scc-plate">
  <a href="../assets/scc/01-compression.svg" aria-label="Open full-size mathematical plate"><img src="../assets/scc/01-compression.svg" alt="Two exact eight by eight coefficient matrices: the all-ones matrix has 64 nonzero coefficients and costs one multiplication; the identity matrix has eight nonzero coefficients and costs eight multiplications."></a>
  <figcaption><strong>Plate I.</strong> Exact coefficient matrices over the two-element field. Dark squares denote coefficients equal to one, not simultaneous truth values of the switches.</figcaption>
</figure>

## I. The weight of a relationship

A calculation can express a great many relationships without doing a great deal of work. This is the phenomenon from which Structural Capacity Calculus (SCC) begins.

Take two rows of eight binary switches. Imagine a relation between each switch in the first row and each switch in the second. In the language of Boolean polynomials, the two arrangements in Plate I have very different computational costs.



$$
F=\left(\sum_{i=1}^8 x_i\right)\left(\sum_{j=1}^8 y_j\right),
\qquad
G=\sum_{i=1}^8x_iy_i.
$$

Here addition is XOR and multiplication is AND. We charge for multiplications and allow affine operations freely. The first expression has 64 pairings but costs one multiplication. The second has only eight pairings but requires eight multiplications, even allowing arbitrary reusable nonlinear intermediates.

Why must the second cost eight? Its polar bilinear form is nondegenerate on 16 coordinates. At each multiplication we can restrict one operand to a constant on an affine subspace, losing at most one dimension and making the gate affine there. After all gates, the output is affine on the remaining subspace. Nondegeneracy limits such a subspace to dimension eight. The cost is therefore at least eight, and eight independent products attain it.

The first coefficient matrix has rank one. The second has rank eight. For this quadratic example, algebraic independence rather than the number of terms identifies the resource.

<figure class="scc-plate">
  <a href="../assets/scc/02-factorization.svg" aria-label="Open full-size mathematical plate"><img src="../assets/scc/02-factorization.svg" alt="The sixteen distinct monomials obtained by choosing one variable from each of four pairs, beside a factorized circuit with three multiplication gates."></a>
  <figcaption><strong>Plate II.</strong> Exact expansion and circuit for the product of four binary sums. The placement of nodes is schematic; all terms and multiplication counts are literal.</figcaption>
</figure>

The same mechanism generalizes: the product of $m$ two-term sums on disjoint pairs expands into $2^m$ monomials and can be computed with $m-1$ multiplications. A lower-bound measure that counts the monomials is fooled by compositional reuse.

<div class="scc-thesis"><span>THE RESEARCH QUESTION</span><p>Can we discover a conservation law for logical structure that every classical computation must obey?</p></div>

A successful law would identify an independently measurable structural obligation and impose a bound on how much of it any single computational operation can discharge. It must distinguish genuine irreducibility from a large expression produced by a small circuit.

## II. Why this is relevant to P versus NP

For a verifier $R(x,y)$, the decision function asks whether at least one candidate witness $y$ succeeds:

$$
F(x)=\bigvee_y R(x,y).
$$

An exponential witness space is not evidence of an exponential computational obligation. Linear parity systems and 2-SAT have exponential candidate spaces and polynomial-time algorithms. General SAT may or may not admit a comparably powerful compression mechanism.

The [PNP-ABOVE programme](pnp_above/index.md) isolates the missing classical resource lower bound. SCC investigates a distinct algebraic route to that boundary: prove that the logical structure necessary for an explicit decision function cannot be reproduced by any small unrestricted circuit.

For ordinary Boolean circuits with bounded fan-in, counting AND gates while making affine operations free gives the established multiplicative-complexity model. Polynomial multiplicative complexity and polynomial circuit size are equivalent up to polynomial overhead. A superpolynomial lower bound for total encoded SAT in this model would imply NP is not contained in P/poly, a stronger conclusion than P versus NP. The transfer to the restricted native PNP-ABOVE promise still has its own obligations.

## III. A calculus of reuse

Let $\mathcal B_n$ be the algebra of Boolean functions on $n$ binary inputs over the field $\mathbb F_2$. A state $V$ is the linear space of currently available functions, including constants and input coordinates. A single charged step computes $g=uv$ with $u,v\in V$ and adjoins it:

$$
V'=V+\langle g\rangle.
$$

Define $F_r(V)$ as the span of products of at most $r$ elements of $V$. The quotient $A_r=F_r/F_{r-1}$ retains the leading symbols in grade $r$; constants have grade zero. Negative filtration indices denote zero. The successive quotients together form the graded algebra $A$.

Boolean idempotence gives an exact one-step law:

$$
F'_r=F_r+gF_{r-1}.
$$

Every positive power of the new primitive equals the primitive itself. Expanding all products proves the identity in both directions. The inclusion $F_r\subseteq F'_r\subseteq F_{r+1}$ follows immediately.

<figure class="scc-plate">
  <a href="../assets/scc/03-promotion.svg" aria-label="Open full-size mathematical plate"><img src="../assets/scc/03-promotion.svg" alt="For four variables before and after computing ab, the graded dimensions change from 1,4,6,4,1 to 1,5,7,3,0. The monomials ab, abc, abd and abcd each move down one grade."></a>
  <figcaption><strong>Plate III.</strong> Exact four-variable calculation. Each square counts one independent graded direction. The promoted monomials are shown explicitly; the histogram is not a drawing of a physical space.</figcaption>
</figure>

Let $q$ be the old grade-two symbol of $g$. The identity on Boolean functions induces the exact sequence

$$
0\to qA_{r-2}\to A_r\to A'_r\to qA_{r-1}\to0.
$$

The kernel consists of old directions promoted out of this grade; the cokernel consists of directions arriving from the next grade. Write $H_r=\dim A_r$ and $R_j=\dim(qA_j)$. Then

$$
H'_r-H_r=R_{r-1}-R_{r-2}.
$$

This is a conservation equation for the redistribution of graded logical structure. For a target of positive relative degree $d$, its degree falls precisely when its old leading symbol lies in $qA_{d-2}$. A single gate cannot reduce that degree by more than one.

There is a further exact constraint. The four products obtained by independently complementing either operand have the same old grade-two symbol, because they differ by affine combinations of available functions.

<figure class="scc-plate">
  <a href="../assets/scc/04-cell-ceiling.svg" aria-label="Open full-size mathematical plate"><img src="../assets/scc/04-cell-ceiling.svg" alt="The sixteen four-bit assignments are partitioned into four cells according to the first two bits. Each of the four cells contains four assignments; the product ab is one on the final cell."></a>
  <figcaption><strong>Plate IV.</strong> Exact partition into the four operand-value cells, for the specific gate computing ab. The general rank argument does not require equally sized cells.</figcaption>
</figure>

Multiplication by a Boolean indicator on the full function algebra has rank equal to its support size. Its induced graded map cannot have larger total rank. Hence the smallest of the four disjoint cells bounds the number of promoted directions:

$$
\sum_{j\geq0} R_j
\leq \min_{\alpha,\beta}|\{x:u(x)=\alpha,\ v(x)=\beta\}|
\leq 2^{n-2}.
$$

For the initial affine space, computing $x_1x_2$ attains the bound. Its rank in grade $j$ is the binomial coefficient $\binom{n-2}{j}$.

This is a sharp capacity law, but not the one we ultimately require: its ceiling is exponential, and relative degree is at most $n$. More sophisticated measures must recognize that millions of promoted directions may have one common source.

## IV. Relations between relationships

A primitive is not merely a new value. It is a new way to express relationships that were already implicit.

Suppose we have three switches $a,b,c$ and have already computed $y=ab$. Now compute $t=ac$. What happens to the relation between these products?

<figure class="scc-plate">
  <a href="../assets/scc/05-syzygy.svg" aria-label="Open full-size mathematical plate"><img src="../assets/scc/05-syzygy.svg" alt="The old product y equals ab; the new product t equals ac. Multiplying y by c or t by b gives the identical Boolean product abc."></a>
  <figcaption><strong>Plate V.</strong> Schematic dependency diagram of a literal identity: both paths compute abc. The cross-relation bt = cy is not an additional charged multiplication in the presentation.</figcaption>
</figure>

Both products $cy$ and $bt$ equal $abc$. In characteristic two, $bt+cy=0$. A syzygy is a relation among generators of a module or ideal; here the coefficients $b$ and $c$ relate the generators $t$ and $y$.

How can we preserve this information when we change our computational representation?

Let $A$ be the graded algebra from the preceding section. The old symbol of $g=uv$ is $q\in A_2$. In the successor, $g$ has degree one, so its old grade-two symbol vanishes. The inherited algebra is

$$
C=A/(q).
$$

The interesting dependencies are those annihilating $q$ that are not already explained by its multiples. They form a residual module:

$$
H=\frac{\mathrm{Ann}_A(q)}{(q)}.
$$

The ideal $(q)$ lies inside the annihilator because $q^2=0$. If $A=\bigwedge E/I$ is presented as an exterior algebra modulo its homogeneous relation ideal, and $Q$ represents $q$, then this module is the colon-ideal quotient

$$
H=\frac{(I:Q)}{I+(Q)}.
$$

The colon ideal collects all elements whose product with $Q$ belongs to the relation ideal $I$. This is a concrete way of describing dependencies around the primitive being introduced. It is not the full free resolution of $I$.

A homogeneous class $a\in H$ of grade $j$ has a representative $f\in F_j$ whose product with $g$ falls into $F_{j+1}$ rather than requiring grade $j+2$. Its lower symbol defines a correction map:

$$
\delta_g(a)=[gf]_{j+1}\pmod{(q)}.
$$

The map is well defined, linear over $C$, and square-zero: applying it a second time produces no higher symbol because $g^2=g$. This gives a cohomology of the residual dependencies. In the three-switch example, the symbol of $b$ maps to the nonzero symbol of $cy$.

The complete successor presentation now takes the form

$$
A'\cong C[t]/(t^2,\ ta+\delta_g(a):a\in H).
$$

<figure class="scc-plate">
  <a href="../assets/scc/06-quotient.svg" aria-label="Open full-size mathematical plate"><img src="../assets/scc/06-quotient.svg" alt="Three mathematical construction steps: inherit the quotient C=A/(q), introduce a square-zero symbol t, and impose the cross-relations ta=delta(a) for every residual relation a."></a>
  <figcaption><strong>Plate VI.</strong> Schematic construction of the exact presentation. These are mathematical operations describing one computational gate, not three charged gates.</figcaption>
</figure>

To see completeness, write any candidate element as $c+tb$ with $c,b\in C$. If it maps to zero, the cokernel of the old-symbol inclusion forces $qb=0$. Hence $b\in H$. The cross-relation reduces the expression to $c+\delta_g(b)$ in the embedded algebra $C$, where it must vanish. These relations therefore account for the whole kernel.

The correction map matters: discarding it would incorrectly replace $bt=cy$ by $bt=0$ in our example. A count of relations cannot capture that distinction.

## V. The spectator obstruction

Even a relation between relationships can appear to have enormous complexity for the wrong reason.

In our three-variable example, the correction differential has rank one. Append four independent unused input bits. Their sixteen square-free monomials tensor with this one direction. No extra computational gate is needed.

<figure class="scc-plate">
  <a href="../assets/scc/07-spectators.svg" aria-label="Open full-size mathematical plate"><img src="../assets/scc/07-spectators.svg" alt="One correction b to cy is tensored with the sixteen distinct square-free monomials in four unused input variables p,q,r,s. The construction still uses exactly two gates."></a>
  <figcaption><strong>Plate VII.</strong> Literal list of the sixteen monomials; the fan of lines schematically indicates tensoring the original correction with each monomial. The lines are not distinct computation paths.</figcaption>
</figure>

For $n\geq3$ inputs, the same two-gate construction has correction rank

$$
\mathrm{rank}(\delta_g)=2^{n-3}.
$$

| Input bits | Correction rank | Charged gates in the construction |
| ---: | ---: | ---: |
| 3 | 1 | 2 |
| 10 | 128 | 2 |
| 20 | 131,072 | 2 |
| 40 | 137,438,953,472 | 2 |

The general identity follows from the tensor-product filtration of the original three-variable state and the affine spectator state. The new correction is the original map tensored with the identity on the spectator exterior algebra.

This exact counterfamily rules out raw correction rank as a polynomial-capacity resource. It reveals the need for spectator invariance: a measure of intrinsic difficulty should not mistake irrelevant input variables for additional computational obligations.

## VI. Complementary regions and persistent relations

The correction differential also has a cohomology

$$
L=H^\bullet(H,\delta_g).
$$

A cycle class can be represented by a function whose product with $g$ falls into its own filtration level. Multiplication by $g$ then induces a projection $P_g$ on this cohomology. Idempotence gives $P_g^2=P_g$. The complementary indicator $1+g$ gives the complementary projection:

$$
L=\mathrm{im}(P_g)\oplus\mathrm{im}(1+P_g).
$$

<figure class="scc-plate">
  <a href="../assets/scc/08-projections.svg" aria-label="Open full-size mathematical plate"><img src="../assets/scc/08-projections.svg" alt="The three-bit assignments partition into the two assignments where ac equals one and the six where ac equals zero. The two cohomology projections admit representatives supported on these complementary sets; their dimensions are not asserted."></a>
  <figcaption><strong>Plate VIII.</strong> Exact assignment partition with schematic arrows to the two projected cohomology components. Input counts are not cohomology dimensions. The projection result has an author proof but has not yet been included in the finite replay.</figcaption>
</figure>

A single projection is elementary. The interaction of projections across successive gates may reveal constraints invisible to a one-step analysis. But these gate-local cohomologies are not yet a common space carrying all such projections; compositional transport must be constructed, not assumed.

## VII. The law we still seek

Imagine measuring the amount of structure that remains to be resolved for a particular target $F$. Denote this nonnegative quantity by $\mathcal E_F(V)$. A viable candidate should vanish when $F\in V$ and have an independently justified bound on its decrease under every legal gate:

$$
\mathcal E_F(V)-\mathcal E_F(V')\leq p(n).
$$

Here $p$ is a fixed polynomial. Telescoping along any computation gives

$$
T\geq \frac{\mathcal E_F(V_0)}{p(n)}.
$$

The mathematical challenge is to find a target-sensitive potential with superpolynomial initial demand for an explicit SAT decision family, without defining the potential in terms of the minimum circuit size itself.

Our current results delimit the search. Degree is too small; graded promotion rank has an exponential one-gate capacity; correction rank can be amplified by spectators. The next investigation must account for syzygies modulo shared factors and their transport across consecutive gates.

<div class="scc-thesis"><span>THE FRONTIER</span><p>Which logical dependencies cannot be cheaply reorganized away?</p></div>

## Research ledger

| Result | Support | Boundary |
| --- | --- | --- |
| Relative-degree promotion and exact graded sequence | Author proof; finite replay | General unrestricted model, not a superpolynomial lower bound |
| Sharp four-cell ceiling | Author proof; finite replay | Allows exponentially many promotions |
| Colon quotient and square-zero correction | Author proof; finite replay | Exact one-step presentation |
| Spectator amplification | Author proof; small exact fixtures | Rejects raw correction rank |
| Complementary cohomology projections | Author proof | Separate replay and formalization outstanding |
| Target-relative universal capacity law | Open | Required for the intended lower-bound argument |

The first [exact regression](https://github.com/grandchallenge/MATHSOLVE/blob/e8096b79099f410aed7d2096c9e5367208b21823/research/SCC-001/replay.js) passed 720 transitions, 3,168 grade checks, 71,640 target checks and 720 capacity checks. The successor [syzygy replay](https://github.com/grandchallenge/MATHSOLVE/blob/ba8f4e6b587ab1ca4f01f0b63037d77ef09476f9/research/SCC-001/syzygy_replay.js) passed 722 transitions, 3,899 grade checks, 6,332 cross-relations, 70,836 module-linearity checks and 6,332 square-zero checks.

These are bounded exact truth-table regressions, not formal proofs of the universal propositions. The proofs are recorded separately. Specialist adjudication, Lean formalization, novelty audit and the unrestricted classical lower bound remain open.

### Read the mathematics, or contribute

Start with Plates I and II; reconstruct the four-variable histogram in Plate III by listing the sixteen square-free monomials. Then verify the identity in Plate V and test what changes if the extra variables in Plate VII cease to be independent. A contributor can replay the exact finite fixtures with Node.js, without installing third-party packages.

The first executable research step is to construct a target-relative relation module with transport across two successive gates, then test an amortized inequality against arbitrary affine operands and the spectator counterfamily. A successful test must yield a proved bound covering every reachable state, or a precise counterexample to that bound. No empirical trend is a substitute.

!!! info "Research surface authority"
    **LIVE:** [SCC-001 tracker](https://github.com/grandchallenge/MATHSOLVE/issues/1309).

    **SOURCE:** [Graded promotion and capacity](https://github.com/grandchallenge/MATHSOLVE/blob/e8096b79099f410aed7d2096c9e5367208b21823/research/SCC-001/RESULT.md); [colon quotients and syzygy transport](https://github.com/grandchallenge/MATHSOLVE/blob/ba8f4e6b587ab1ca4f01f0b63037d77ef09476f9/research/SCC-001/SYZYGY_TRANSPORT.md). These are protected exploratory records, not MATHCERT certification.

    **VISUALS:** [Plate construction source](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/tools/render_scc_plates.py). Select a plate to open its full-size SVG. Every plate states its literal and schematic semantics in the adjacent caption and alternative text. The SVGs are deterministic illustrations, not evidence of a theorem.

    **CONTEXT:** [P versus NP from Above](pnp_above/index.md) and [A Mathematical Atlas of Computational Difficulty](https://github.com/grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS).
