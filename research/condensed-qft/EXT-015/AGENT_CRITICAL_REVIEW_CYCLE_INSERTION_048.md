# EXT-015 REACH-R2 / 048 — source-locked adversarial audit of Gaussian cycle insertion

**Review role:** GCL mathematical critic, logically separated from authoring; one authenticated programme identity. This is neither an external referee nor a MATHCERT certificate. **Reviewed exact research head:** \`8aa669b3812f67db5ea9b28560b09f901a00a9f1\` in [PR #2833](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2833), source [R2/047](R2_GAUSSIAN_CYCLE_INSERTION_047.md), including [fixture 047](fixtures/check_gaussian_cycle_insertion_047.py). Original audited basis: protected R2/042–046. **Claim boundary:** graphwise positive-weight Gaussian collision finite parts; not the full overlapping-subgraph forest or globally closed BV theory.

## 1. Adversarial verification of the state update

Start with a connected graph with $n$ vertices, reduced incidence matrix $B$ and positive edge weights. Its reduced precision matrix $Q=B^{\mathsf T}WB$ is strictly positive. A proposed edge between two already connected vertices has reduced incidence vector $v\ne0$; adding the edge multiplies the regulated graph amplitude by

$$
\frac{\sqrt w}{\sqrt{2\pi}\epsilon}
\exp\left(-\frac{w(v^{\mathsf T}y)^2}{2\epsilon^2}\right).
$$

The new quadratic exponent has precision $Q+wvv^{\mathsf T}$. The matrix determinant lemma yields exactly

$$
\frac{\det(Q+wvv^{\mathsf T})}{\det Q}
=1+w\,v^{\mathsf T}Q^{-1}v,
$$

while the Sherman–Morrison identity yields exactly the inverse covariance stated in R2/047. Accounting for the one extra Gaussian normalization and the added cycle rank gives the update

$$
\frac{c^+}{c}
=\frac{\sqrt{w}}{\sqrt{2\pi}\sqrt{1+wR}}.
$$

These are identities **at every positive regulator** and do not rely on an undefined distributional product after regulator removal. The whole-graph Laurent counterterms follow from the distributional Taylor expansion of the *new* normalized Gaussian. The theorem is correctly described as a graphwise insertion, not a multiplication operator on renormalized distributions.

**Hostile normalization:** The factor $1/\sqrt{1+wR}$ cannot be dropped. For a unit triangle, the old weighted tree sum is three; with one parallel new unit edge, it becomes five, rather than six. The insertion coefficient must reflect $3\to5$.

**Disposition:** ACCEPT Theorem 47.1 and its whole-graph counterterm consequence within the fixed Gaussian regulator.

## 2. Multiedge insertion order and genuine limitation

For a finite set of new edges, the final precision is the sum of their positive rank-one updates. Its determinant, covariance and Gaussian normalization depend only on the **set with multiplicity** of inserted edges, not on their order. In the sequential normalization formula the matrix-determinant ratios telescope, producing the exact final coefficient in (47.7). Adding parallel edges remains legitimate in the multigraph model.

The exact fixture verifies the determinant lemma, inverse update, Kirchhoff identity, rational normalization and six permutations of three new edges on **20 weighted connected graph seeds**, with no floating-point tolerance. This is useful regression evidence; the analytical proof follows from the determinant identity, not from enumeration.

**Hostile omission:** Order independence of **whole-graph** Gaussian renormalization is weaker than consistency of separately renormalized **proper subgraph** counterterms. In particular, a proper two-cycle or triangle may have a finite-part prescription that does not commute with its inclusion in a larger overlapping supergraph. An arbitrary Bogoliubov/Zimmermann forest theorem does not follow.

**Disposition:** ACCEPT Corollary 47.2 only at whole-graph state level.

## 3. Wick insertion and parity review

The smoothed one-dimensional cusp propagator is $P_{\epsilon,w}(z)=\epsilon p_w(z/\epsilon)$ with

$$
p_w(t)=\frac12\mathbb E|t+N(0,w^{-1})|.
$$

For a connected delta graph of cycle rank $h$, its normalized Gaussian relative density forces the new Wick-edge product to have overall factor $\epsilon^{1-h}$. Taylor-expanding the test at the full collision locus gives powers $\epsilon^{k+1-h}$, with $k$ the multi-index degree. The Wick factor is even and all centered Gaussian odd moments vanish. Therefore the coefficient at $\epsilon^0$ occurs only when $k=h-1$ is even; it is absent when $h$ is even.

When $h=1$, the finite part is $c\,E[p_w(v^{\mathsf T}Z)]\delta$. The sum of independent centered normal variables has variance $R+w^{-1}$, so its mean absolute value gives exactly

$$
c\sqrt{\frac{R+w^{-1}}{2\pi}}\,\delta.
$$

For the unit triangle, $R=2/3$, giving $\sqrt5/(6\pi)\,\delta$. For the fourth **delta** edge rather than Wick edge, the updated graph has $Q^+=\left(\begin{smallmatrix}3&-2\\-2&3\end{smallmatrix}\right)$, determinant five, inverse diagonal $3/5$, cycle rank two and nonzero quadratic-derivative finite part. These two nonzero amplitude normalizations are independently checked by the exact rational fixture after symbolic removal of powers of $\pi$.

**Edge derivative trap:** $P_{\epsilon,w}''(t)=\kappa_{\epsilon,w}(t)$ is true as an ordinary smooth function at every positive regulator. But $t=v^{\mathsf T}y$ is not an independent coordinate from the original connected Gaussian graph. Applying a *total coordinate derivative to the final graph distribution* also differentiates its old factors, introducing extra terms. The correct statement is a **factor-local edge-labelled** conversion before taking the coefficientwise finite part. R2/047 explicitly makes this distinction. It proves no global BV second-order operator by itself.

**Disposition:** ACCEPT Theorem 47.3 as a graphwise coefficient and factor-local identity with the stated parity limits; do not promote it into the full BV commutator or QME.

## 4. Negative theorem for finite-part-only gluing

The finite part of a unit triangle is zero: its cycle rank is odd and its Laurent series has powers $\epsilon^{-1},\epsilon^{1},\epsilon^{3},\ldots$, with no constant coefficient. Adding a parallel delta edge raises the cycle rank to two; the new normalized Gaussian has a **nonzero second-derivative** constant term. Pairing it with a test quadratic in one relative coordinate gives $3/(10\pi\sqrt5)$, strictly nonzero. A linear insertion map on **finite-part distributions alone** cannot map the source zero to that target.

This is a legitimate counterexample to the proposed naive linear architecture. It does not exclude a graph-indexed nonlinear reconstruction, an extended Laurent-state linear construction, or a BPHZ forest recursion. The finite state $(Q,c,h)$ is a sufficient graph-specific record and has been shown to update coherently by the theorem.

**Disposition:** ACCEPT Theorem 47.5 with its explicitly **linear, finite-part-only** quantifiers.

## 5. Reviewer boundaries and next proof object

- The connected Gaussian graph theorem is an exact **free distributional model**; it does not require an interacting action, a quantum master equation, or a choice of curved background.
- Its counterterms act on the full vertex collision diagonal and can depend on the entire graph precision matrix. **Supergraph-independent local counterterm assignments for overlapping proper subgraphs remain unproved.**
- Its rank-one state update is order independent but need not be compatible with the insertion of independently renormalized source components; R2/046 already demonstrated that premature constant-term projection destroys bridge gluing.
- Free factor-local Wick-to-delta conversion does not by itself prove the global second-order BV Leibniz defect and nilpotence on a completed domain.
- Strong distributional Laurent asymptotics do not imply Costello–Gwilliam B.6 smooth Weiss descent or the liquid syzygy higher-Ext comparison.

**Next decisive mathematics:** start with a connected delta graph carrying two inserted edges that create overlapping proper cyclic subgraphs. Define local counterterms first for each subgraph *independently of the supergraph*, then test the two possible subtraction orders and the factor-local Wick/delta relation. The first exact failure gives an anomaly/consistency obstruction; a positive proof advances toward a true forest recursion.

**Verdict:** ACCEPT the bounded mathematical content of R2/047 as a **source-locked GCL research candidate** with its stated limitations. Critical review is separate in logic but **not** separately authenticated external evaluation; protected PR review and readback remain required for durable admission. Research tracker [#2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) stays OPEN.
