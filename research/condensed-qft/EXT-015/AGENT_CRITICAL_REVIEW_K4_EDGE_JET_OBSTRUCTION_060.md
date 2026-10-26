# EXT-015 REACH / 060 — critical mathematical review of R2/059 derivative-jet edge insertion

**Verdict: BOUNDED ACCEPT**, source-locked to R2/059 candidate [PR #2858](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2858), head \`4776ce8c74ce78e686295741881dd4aff95d971d\`, [R2/059 proof](R2_K4_DELTA_JET_INSERTION_OBSTRUCTION_059.md), and [exact fixture](fixtures/check_k4_edge_jet_obstruction_059.py). This is a distinct logical GCL mathematical critic pass, not an external independently authenticated review or MATHCERT certification. Protected source admission remains distinct.

## 1. Review target and hostile failure modes

Previous R2/051–052 establish the full K4 forest preparation with **both** its scalar pole and a nonzero normal second-derivative pole. R2/059 asks whether a repeated Gaussian edge can be inserted into that *already renormalized* K4 source without losing the limit, and whether simply evaluating the new edge at the collapsed K4 vertex captures its proper source counterterm.

Potential false arguments excluded:

1. An $O(\epsilon)$ distribution remainder on fixed tests does **not** imply that its pairing with Gaussian tests that vary with $\epsilon$ is small; those tests are not bounded in $\mathcal D$.
2. The derivative-of-delta is **not** a scalar delta and its product with a smooth factor cannot be computed solely from the factor's value at the origin.
3. The K4 theta source is already prepared; substituting its primitive five-edge Gaussian would erase nested forest terms and alter every constant.
4. Renormalizing the *entire* new seven-edge graph is a different operation from multiplying a renormalized K4 source by the new positive-regulator edge. R2/059 proves a failure of the latter, not a no-go theorem for full seven-edge forests.

## 2. Independent differential-jet witness

Use relative coordinates to vertex 4. The K4 covariance and full source counterterm are

$$
Q^{-1}=\frac14(I+J),\qquad
C_\epsilon=A\epsilon^{-3}\delta+
B\epsilon^{-1}(Q^{-1}:\partial^2)\delta,
\tag{60.1}
$$

with the protected constants

$$
\pi^{3/2}A=\sqrt3-\frac34+\frac{5\sqrt2}{48},
\qquad
\pi^{3/2}B=-\frac{7\sqrt2}{288}.
\tag{60.2}
$$

For a Gaussian edge $f_\epsilon(y)=\kappa_\epsilon(a\cdot y)$, all six K4 incidence vectors have $a^TQ^{-1}a=1/2$. Rather than multiplying formal delta symbols, pair with a fixed compact test $\varphi$. The exact distribution pairing is

$$
\begin{aligned}
\langle f_\epsilon C_\epsilon,\varphi\rangle
={}&A\epsilon^{-3}f_\epsilon(0)\varphi(0)\\
&+B\epsilon^{-1}
(Q^{-1}:\partial^2)(f_\epsilon\varphi)(0)\\
={}&\kappa(0)(A-B/2)\epsilon^{-4}\varphi(0)
+\kappa(0)B\epsilon^{-2}(Q^{-1}:\partial^2)\varphi(0).
\end{aligned}
\tag{60.3}
$$

Here the mixed first-derivative term vanishes only because the Gaussian is even. Therefore the frozen-factor rule misses

$$
-\frac{\kappa(0)B}{2}\epsilon^{-4}\delta
=\frac7{576\pi^2}\epsilon^{-4}\delta.
\tag{60.4}
$$

The signs follow from the product rule and $\kappa''(0)=-\kappa(0)$: positive contact correction because $B$ is negative. A smooth compact test equal to one near zero detects the scalar correction; a test equal to $(a\cdot y)^2$ there detects the independent coefficient $\kappa(0)B\epsilon^{-2}=-7/(288\pi^2)\epsilon^{-2}$.

**Review decision:** ACCEPT Lemma 59.1 and the precise delta-jet Leibniz correction. In particular, changing only the source's scalar coefficient would not replace the second-derivative action on quadratic probes.

## 3. Independent combinatorial and scalar audit

The rank-one matrix determinant identity gives $\tau(K4+e)=16(1+1/2)=24$ for **each** of the six repeated edges. This makes the raw seven-edge amplitude coefficient $\pi^{-2}/(8\sqrt6)$ at degree $\epsilon^{-4}$.

Prepare K4 *before* overall subtraction and multiply by the extra edge. Counting four triangles by whether they contain the new edge endpoints gives two with coefficient $\pi^{-2}/12$ each and two with $\pi^{-2}/(8\sqrt3)$ each. The three square counterterms contribute $\pi^{-2}/8$ each. The six prepared thetas contribute $\pi^{-2}(1/(8\sqrt2)-1/(2\sqrt6)-1/8)$ each. All proper contributions are subtracted, including the negative prepared theta constants with their correct signs. Thus, after stripping $\pi^{-2}$, the exact prepared coefficient is independently

$$
P_0=\frac{\sqrt6}{48}
-\frac16-\frac{\sqrt3}{12}-\frac38
-6\left(\frac{\sqrt2}{16}-\frac{\sqrt6}{12}-\frac18\right)
=\frac5{24}-\frac{3\sqrt2}8-\frac{\sqrt3}{12}
+\frac{25\sqrt6}{48}.
\tag{60.5}
$$

The correctly inserted overall K4 delta jet instead contributes

$$
S_0=\frac{\sqrt6}{2}-\frac{3\sqrt2}{8}
+\frac{67}{576}.
\tag{60.6}
$$

Therefore $P_0-S_0=53/576+\sqrt6/48-\sqrt3/12$ exactly, with no uncancelled $\sqrt2$ term. A direct interval certificate shows this residual is strictly negative:

$$
576(P_0-S_0)=53+12\sqrt6-48\sqrt3
<53+12\cdot2.45-48\cdot1.732<0.
\tag{60.7}
$$

Both rational inequalities are rigorous because $2.45^2>6$ and $1.732^2<3$. Thus the nonzero leading divergence of $\kappa_\epsilon R_{K4,\epsilon}$ needs neither floating point nor a nontrivial algebraic-independence theorem.

The source term has an exponentially small cutoff error on any compact test equal to one near the graph's full diagonal: every Gaussian quotient has covariance proportional to $\epsilon^2$ and the delta-jet pairings at zero are exact. On such a test the scalar obstruction survives with coefficient $\pi^{-2}(P_0-S_0)\epsilon^{-4}$. This contradicts convergence to any finite distribution.

**Review decision:** ACCEPT Theorem 59.2 as a precise negative result about same-scale edge multiplication, not an all-graph renormalization no-go claim.

## 4. Exact computational controls

The [standard-library fixture](fixtures/check_k4_edge_jet_obstruction_059.py) uses exact rational coefficients in the basis $1,\sqrt2,\sqrt3,\sqrt6$, computes the complete weighted Laplacian of all six seven-edge choices, checks $\tau=24$ and effective resistance $1/2$, and verifies:

- the derivative contact term $7/(576\pi^2)$;
- the quotient classification of two triangle sources containing the repeated edge and two not containing it;
- all square and prepared-theta coefficients without doubling nested forests;
- the exact residual vector $(53/576,0,-1/12,1/48)$ times $\pi^{-2}$;
- the nonzero quadratic normal-probe jet coefficient.

Authenticated CHAD executed the exact candidate fixture successfully (run \`fed1aa5339a94d71a2a7a9ee6b547a1d\`). R2/059 mathematical Markdown gate passed after a prose-delimiter spacing repair (run \`4a0966f4a15c4a8381baedc6dcd44eca\`). These computational receipts validate algebraic data, not the distributional theorem independently of its proof.

## 5. Exact boundary and successor problem

**ACCEPT the two claimed negative statements with stated Gaussian and regulator limits.** No logical inconsistency is found between strong $R_{K4,\epsilon}\to0$ and failure of the product limit: the new Gaussian multipliers are not bounded in the fixed-test distribution topology.

The result identifies a necessary design requirement for the next source-local renormalization construction: **normal delta jets must act on the full complement jet**, with scale-dependent multiplier seminorms controlled by explicit filtration, or source counterterms must be evaluated at a separated regulator scale under a separately proved comparison. The quotient-edge value alone is mathematically inadequate. It does not supply or refute a global BV differential, Weiss descent, higher liquid Ext, or the full seven-edge BPHZ scheme. Do not close [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) based on this bounded result.

**Admission condition:** first protected-merge exact source PR #2858, then protected-merge this distinct role-scoped critical review; independently read back both from protected main.
