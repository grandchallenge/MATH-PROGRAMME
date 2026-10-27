# EXT-015 REACH-R2 / 071 — no finite Laurent source state supports all Gaussian cycle insertions

**Status:** bounded obstruction candidate. This is a precise no-go theorem for a finite Laurent-data gluing contract, not an impossibility theorem for renormalization, a full forest prescription or BV/QME. It explains why a fixed finite source truncation cannot replace the retained regulator-dependent state under arbitrary future cycle insertions.

**Admitted context:** [044](R2_GAUSSIAN_COMPONENTWISE_GLUING_044.md) distinguishes componentwise renormalization from one global finite part; [046](R2_BRIDGE_TREE_LAURENT_BV_046.md) retains full Laurent germs for bridge gluing; [059](R2_K4_DELTA_JET_INSERTION_OBSTRUCTION_059.md) and [061](R2_FILTERED_NORMAL_JET_INSERTION_061.md) require normal complement jets. The even-rank finite terms in corrected [065](R2_NESTED_GAUSSIAN_JET_FOREST_065.md) must also be retained. The present operator and domain are stated independently so that its failed identity is unambiguous.

## 1. A legal positive-regulator insertion module

Let

$$
\kappa_\epsilon(z)=
\frac1{\sqrt{2\pi}\epsilon}
\exp\!\left(-\frac{z^2}{2\epsilon^2}\right),
\qquad \epsilon>0.
\tag{71.1}
$$

Fix a smooth compact cutoff $\chi$ equal to one near zero. Work in the real linear span of regulated families

$$
\chi(z)\epsilon^r p(z/\epsilon)\kappa_\epsilon(z)^m,
\qquad r\in\mathbb Z,\quad m\ge1,\quad p\in\mathbb R[t].
\tag{71.2}
$$

Each family has a bounded-below distributional Laurent expansion on compact smooth tests. Gaussian Taylor moments prove this directly, with strong remainder estimates. Write $J_{\le L}$ for its coefficients of powers at most an integer $L$, and $\mathrm{FP}$ for its coefficient of $\epsilon^0$.

For $N\ge1$, adding $2N$ Gaussian edges on the same relative coordinate is the exact positive-regulator operator

$$
I_{2N}(A)_\epsilon
=\kappa_\epsilon^{\,2N} A_\epsilon.
\tag{71.3}
$$

It stays in (71.2). No product of limiting singular distributions is used. Put $F_N=\mathrm{FP}\circ I_{2N}$. This is also the finite limit after subtracting every negative Laurent coefficient of the whole inserted amplitude. It is not declared to be a proper-subgraph forest operation.

The proposed finite-state compatibility diagram asks whether there is a map $\overline F_{N,L}$ such that

$$
F_N=\overline F_{N,L}\circ J_{\le L}.
\tag{71.4}
$$

The statement is meaningful even if the proposed map is nonlinear: equal retained source states must have equal outputs.

## 2. Exact failure for every fixed cutoff

**Theorem 71.1.** For every finite integer $L$, there exists $N\ge1$ for which (71.4) is impossible. Two source families with identical retained data produce different renormalized inserted amplitudes, by an explicit nonzero scalar delta.

**Proof.** Choose $2N>L$ and consider

$$
A_\epsilon=\chi\kappa_\epsilon,
\qquad
\widetilde A_\epsilon=
\chi\kappa_\epsilon+\chi\epsilon^{2N}\kappa_\epsilon.
\tag{71.5}
$$

Their difference begins at Laurent degree $2N$, so $J_{\le L}A=J_{\le L}\widetilde A$. For $L\ge0$ both in particular retain the same ordinary source finite part $\delta_0$.

After insertion their difference is

$$
I_{2N}(\widetilde A-A)_\epsilon
=\chi(z)\epsilon^{2N}\kappa_\epsilon(z)^{2N+1}.
\tag{71.6}
$$

Pair with a compact smooth test $\phi$ and substitute $z=\epsilon t$:

$$
\begin{aligned}
\langle I_{2N}(\widetilde A-A)_\epsilon,\phi\rangle
&=(2\pi)^{-(2N+1)/2}
\int_\mathbb R
e^{-(2N+1)t^2/2}\chi(\epsilon t)\phi(\epsilon t)\,dt\\
&=\frac{(2\pi)^{-N}}{\sqrt{2N+1}}\phi(0)
+O(\epsilon^2).
\end{aligned}
\tag{71.7}
$$

The odd first Taylor moment vanishes. All higher Gaussian moments are finite, and the cutoff error outside the fixed neighborhood on which $\chi=1$ is exponentially small. Taylor bounds are uniform on bounded compact smooth test families, so this is a strong distributional estimate. Thus

$$
F_N(\widetilde A)-F_N(A)
=
\frac{(2\pi)^{-N}}{\sqrt{2N+1}}\delta_0
\ne0.
\tag{71.8}
$$

The difference (71.6) has no negative Laurent terms, so the same discrepancy persists after pole-only subtraction of the inserted amplitudes. Equal inputs to $J_{\le L}$ have different required outputs, which refutes (71.4). $\square$

The relevant missing information can occur arbitrarily far above the source finite part. Retaining any one fixed number of positive Laurent coefficients therefore cannot repair the contract for all such insertions.

### 2.1 Even a fixed insertion fails on this full polynomial module

The preceding elementary pair varies the insertion with the cutoff. On the module (71.2), the result is stronger.

**Theorem 71.2.** For every fixed $N\ge1$ and every finite $L$, (71.4) is impossible on (71.2).

**Proof.** Let $\mathrm{He}_{2K}$ be the probabilists' Hermite polynomial, characterized by

$$
e^{ut-u^2/2}=\sum_{j\ge0}\mathrm{He}_j(t)\frac{u^j}{j!}.
\tag{71.9}
$$

Choose $K\ge0$ with $2N+2K>L$, and take the source difference

$$
B_\epsilon(z)=
\chi(z)\epsilon^{2N}
\mathrm{He}_{2K}(z/\epsilon)\kappa_\epsilon(z).
\tag{71.10}
$$

Orthogonality against the standard Gaussian gives zero Taylor moments in every degree below $2K$. Its first nonzero distributional term therefore occurs at degree $2N+2K$. In particular $J_{\le L}B=0$.

After the fixed insertion, substituting $z=\epsilon t$ gives a Gaussian of variance $1/(2N+1)$. The generating function (71.9) gives its exact Hermite expectation

$$
\mathbb E\,\mathrm{He}_{2K}(T)
=
\frac{(2K)!}{2^K K!}
\left(\frac1{2N+1}-1\right)^K
\ne0,
\qquad T\sim\mathcal N\!\left(0,\frac1{2N+1}\right).
\tag{71.11}
$$

Here $K=0$ means the value one. Consequently

$$
F_N(B)=
\frac{(2\pi)^{-N}}{\sqrt{2N+1}}
\frac{(2K)!}{2^K K!}
\left(\frac1{2N+1}-1\right)^K
\delta_0\ne0.
\tag{71.12}
$$

All corrections begin at order $\epsilon^2$, with the same strong Taylor remainder argument as in (71.7). The polynomial is fixed for each chosen pair, and its Gaussian moments are finite; no bound uniform in $K$ is claimed. The inserted difference has no negative powers. Comparing zero with $B$ therefore refutes (71.4), including its pole-only finite-part version. $\square$

This stronger statement uses the unbounded polynomial degree allowed in (71.2). It does not rule out finite descriptions on a separately restricted module with a proven degree or jet bound. The fixture checks Hermite orthogonality and the changed-variance moment exactly for a range of $N,K$; those finite checks do not replace the generating-function proof.

## 3. What the obstruction says about a proposed renormalized operator

The theorem is a failure of one exact factorization identity on a specified linear module of positive-regulator amplitudes. It is not based on a graph count or an undefined product of delta jets. If a proposed cycle-insertion/renormalized BV construction uses only $J_{\le L}$ of each source, is claimed for all insertions (71.3), and agrees with the pole-only finite-part normalization on these whole amplitudes, it fails this explicit test.

There are legitimate ways to leave these hypotheses: retain a sufficiently rich regulator-dependent state with an order that grows with the insertion; carry additional source/complement data; restrict the insertion domain; or change the renormalization prescription and prove its consistency. The theorem does not prove that such alternatives fail.

In particular:

- it does not identify whole-graph finite part with the source-local forest scheme of 049/057/065;
- it does not prove a nonzero commutator or QME anomaly on an already defined global BV algebra;
- it does not replace the missing compatibility theorem for two overlapping differentiated source sectors;
- it does not negate the coherent fixed-source jet module of 061, which retains every required finite jet rather than a uniform fixed cutoff.

The [exact fixture](fixtures/check_finite_laurent_insertion_obstruction_071.py) verifies the Laurent exponents, Gaussian moment ratios, equal retained coefficients and nonzero inserted difference for a range of truncations without floating point. The proof for arbitrary finite $L$ is the choice $2N>L$ and the exact integral above, not the finite fixture.

**Disposition:** bounded no-go for the finite-state insertion contract; the larger [GB2 issue #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) remains OPEN for a coherent renormalized operator outside that contract, with its actual BV/factorization/transport identities.
