# CSM-001 — mathematical research specification

**Programme:** Categorical Statistical Mechanics (CSM). **Authority:** Human Steward approval, 2026-11-04. **Owner:** grandchallenge/MATH-PROGRAMME. **Tracker:** [#3136](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3136). **Status:** activation SPEC; existing mathematical identities distinguished from unproved research claims.

## 1. Thesis and exclusions

Seek a compositional semantics for statistical mechanics and new theorems characterizing which physical properties are preserved by composition, marginalization, coarse-graining and infinite-volume limits. Initial scope: **finite classical equilibrium systems**, exactly specified inputs/outputs and nonnegative weights.

Out of initial scope: a claim to a complete foundation of statistical physics; general continuum QFT; general quantum or nonequilibrium mechanics; an unqualified assertion that categorical composition preserves locality or Gibbsian structure.

## 2. Finite baseline: the target category

Let $\mathsf{Mat}_{\mathbb{R}_{\geq0}}$ have finite sets as objects and matrices of nonnegative real numbers as morphisms. We fix the convention that $A:X\to Y$ is a family $A(y,x)$, with

$$
(B\circ A)(z,x)=\sum_{y\in Y}B(z,y)A(y,x).
$$

The identity morphism is the Kronecker delta. A symmetric monoidal product is given on objects by Cartesian product and on matrices by the Kronecker product. A morphism $1\to1$ is a nonnegative scalar. Matrix trace may be used to close a finite periodic transfer network.

**Critical distinction:** $\mathsf{Mat}_{\mathbb{R}_{\geq0}}$ is a category of **unnormalized** weighted kernels. The subcategory of stochastic kernels is not interchangeable with it when a partition function must be retained. Conditional probabilities, when defined, are obtained by normalization, which must be tracked.

**Target CSM-01 obligation:** Define an explicit category or typed syntax of *open weighted factor networks* and construct a well-defined symmetric monoidal semantics into $\mathsf{Mat}_{\mathbb{R}_{\geq0}}$, including boundary labeling, copy/delete factor conventions, gluing, and closed-network evaluation. Associativity of matrix multiplication alone does **not** prove all functoriality and wiring claims.

## 3. Reproducible finite models

For a nearest-neighbour periodic spin chain with bond weight $a>0$ for equal spins and $b>0$ for unequal spins, define

$$
T=\begin{pmatrix}a&b\\b&a\end{pmatrix}.
$$

The eigenvalues are $a+b$ and $a-b$, hence the known identity

$$
Z_N=\mathrm{tr}(T^N)=(a+b)^N+(a-b)^N.
$$

The initial integer-weight specimen uses $a=2$, $b=1$. It checks $N=1,\ldots,8$ against independent spin enumeration. This is not an original theorem.

For any finite set $X$, weight $w:X\to\mathbb{R}_{\geq0}$ and deterministic map $C:X\to Y$, set

$$
(C_*w)(y)=\sum_{x:C(x)=y}w(x).
$$

Finite partition-function conservation follows from regrouping a finite sum:

$$
\sum_{y\in Y}(C_*w)(y)=\sum_{x\in X}w(x).
$$

This identity is known, elementary and **not** a new preservation theorem for physical interactions. Its exact finite interpretation and failure modes for interaction classes are the next work.

## 4. Entropy and equilibrium

Given a finite configuration set with Hamiltonian $H$, inverse temperature $\beta$, and canonical Gibbs distribution $p_\beta$, the familiar Gibbs variational identity is

$$
\log Z(\beta)=\sup_p\left[S(p)-\beta\mathbb{E}_pH\right].
$$

Here $S(p)=-\sum_x p(x)\log p(x)$. The associated gap is

$$
\log Z-\left(S(p)-\beta\mathbb{E}_pH\right)=D_{\mathrm{KL}}(p\Vert p_\beta).
$$

These are **prior mathematical facts**. The new work, if any, must specify a category, morphism class, functorial/monoidal structure and genuinely additional compatibility or obstruction result, with theorem hypotheses spelled out.

## 5. Infinite-volume and coarse-graining obstruction

DLR consistency uses a family of conditional Gibbs kernels $\gamma_\Lambda$ indexed by finite regions and an invariant measure $\mu$, typically written $\mu\gamma_\Lambda=\mu$. The spaces, measurable structures, boundary conditions, regularity and compatibility hypotheses all matter. Existing categorical work already studies Gibbs specifications and phases.

Under an exact finite coarse-graining $C$, the effective weights are well-defined, but the effective Hamiltonian $H_{\mathrm{eff}}(y)=-\beta^{-1}\log\sum_{C(x)=y}e^{-\beta H(x)}$ may create long-range many-body couplings; in infinite volume the coarse-grained measure may be non-Gibbsian in physically relevant classes.

**Candidate research proposition (UNPROVED):** Identify a class of infinite specifications, an admissible family of coarse-graining kernels and a locality/continuity condition for which compatibility of pushforward and Gibbs reconstruction is necessary and sufficient; otherwise produce a precise counterexample/obstruction. The statement is **not ready for theorem promotion** until existing preservation and non-Gibbsian theorems have been reconciled.

## 6. Execution gates and evidence

- **G0:** Source-locked bibliography with exact theorem hypotheses and novelty matrix; distinguish source abstracts from complete proof audits.
- **G1:** Defined typed category and semantics, proof of its claimed composition laws, runnable exact finite examples plus independent tests. A script without a semantics theorem is insufficient.
- **G2:** A new preservation/obstruction theorem surviving source-semantic comparison and specialist mathematical review, or a documented no-novelty/failed route.
- **G3:** Justified passage to infinite-volume specifications and relevant measure-theoretic/topological hypotheses.
- **G4:** Quantum/dynamical extension only with scoped results from earlier gates.

For finite deterministic prototypes, exact arithmetic and independent simple enumeration are preferred. For later stochastic numerics, record fixed seeds, multi-seed CLI runs and W&B logging; use a single GPU initially where GPU computation is warranted. Do not impose stochastic testing or GPU infrastructure on a finite exact proof.

No certification or external publication claim follows from passing CI. Internal technical review may advance routine research to certification under applicable policy; public external-validation claims follow their own gates.

## 7. First finite work packet (next action)

**CSM-01-WP01:** Define open factor-network syntax, input/output typing and composition, create a small factor-graph nontrivial boundary example, and prove by finite index manipulation that its network evaluation agrees with the matrix semantics. Add a finite marginalization example where the effective coupling is not of the originally restricted local factor form. Preserve source boundaries and submit a protected PR.

**Acceptance:** full types and hypotheses; explicit tensors/indices; hand-checkable small instance; independent exact tests; complexity and normalisation conventions; proof-vs-experiment ledger; mathematical Markdown and relevant CI passing.

## 8. Interfaces and continuity

MODULUS: variational duality. CMDG: local-to-global/categorical completion. Condensed QFT: quantum equilibrium. Adaptive Intelligence Atlas: inference and information geometry. Cross-programme analogy conveys no theorem proof or new authority.

Long-horizon autonomous workset admission must use the protected bounded-operation continuity machinery before autonomous multi-stage execution. This initial activation is an ordinary bounded documentation-plus-specimen transaction. Track unfinished obligations at [the programme issue](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3136), rather than proliferating empty tickets.
