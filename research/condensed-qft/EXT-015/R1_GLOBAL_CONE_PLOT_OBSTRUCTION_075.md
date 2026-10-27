# EXT-015 REACH-R1 / 075 — the ordinary global cone union is incomplete and has extra smooth plots

**Disposition:** exact negative result for the ordinary global topology requested in R1. The support/cone inductive union is neither regular nor sequentially complete. Its Bastiani-smooth curves are strictly more numerous than the locally normal plots of 069, already on real symmetric kernels of arity two. This does not refute the refined differentiable model constructed in 069.

**Sources and attribution:** the completeness and regularity input is published mathematics: Dabrowski–Brouder, [Functional properties of Hörmander's space of distributions having a specified wavefront set](https://arxiv.org/pdf/1308.1061), v2, section 3.1, Theorem 34 and Corollary 36. The REACH-specific cone specialization, real symmetric reduction and flat smooth-curve/failed-lift argument below are the application proved here. Inputs [033](R0_CRITICAL_AUDIT_D21_033.md), [035](R1_NORMAL_CONE_CONTINUOUS_CONTRACTIONS_035.md) and [069](R1_LOCALLY_NORMAL_COMPLETED_WEISS_069.md) retain their actual scopes.

## 1. The ordinary global topology is specified

Let $U$ be a nonempty open interval and $n\ge2$. Put $\Omega=U^n$ and let $\mathfrak N_n$ be the finite union of the nonzero conormals of all collision partial diagonals, including simultaneous disjoint collisions, as in D21/030. Define

$$
\Lambda_n=\dot T^*\Omega\setminus\mathfrak N_n,
\qquad
E_n=\{u\in\mathcal E'(\Omega):\mathrm{WF}(u)\subset\Lambda_n\}.
\tag{75.1}
$$

The cone $\mathfrak N_n$ is closed and invariant under changing covector sign. Therefore $\Lambda_n$ is open and invariant under sign. Define the ordinary global locally convex topology by

$$
E_n^{\mathrm{ind}}=
\varinjlim_{\substack{K\Subset\Omega\\
\Gamma\ \mathrm{closed},\ \Gamma\subset\Lambda_n}}
E_{n;K,\Gamma}^{\,N},
\tag{75.2}
$$

using exactly the fixed-support normal-topology sectors of 035/069. This is an ordinary locally convex inductive limit, not the plot definition of 069.

This is the space denoted $\mathcal E'_{\Lambda_n}$ with its inductive topology in the cited paper. To check the index comparison, restrict to unit covectors over a compact support. Any closed admissible cone there is a compact subset of the open cone, so it has a positive distance from the complement. A compact exhaustion and distance-from-the-complement exhaustion therefore dominate each such support/cone pair. Conversely each stage in that exhaustion is one of the sectors in (75.2). Thus the final locally convex topologies agree.

**Lemma 75.1.** The open cone $\Lambda_n$ is not closed.

**Proof.** Choose a point with its first two coordinates equal. The nonzero covector
$(1,-1,0,\ldots,0)$ is a forbidden pair conormal there. For every $\delta>0$, the covector $(1+\delta,-1,0,\ldots,0)$ is admissible: every partial-diagonal conormal has total coordinate sum zero, while this covector has total sum $\delta$. These admissible covectors converge to the forbidden one. $\square$

**Theorem 75.2.** The space (75.2) is not sequentially complete and its support/cone inductive limit is not regular.

**Proof.** Lemma 75.1 verifies the open, nonclosed cone hypothesis of Dabrowski–Brouder Theorem 34. Their section 3.1 identifies the inductive normal-sector topology with the strong dual topology used in that theorem. Corollary 36 proves non-regularity for the same inductive limit. All sign conventions match because the forbidden cone here is invariant under sign. $\square$

This is a refutation of the proposed complete regular ordinary union on these fibers. It is not an unproved topology-identification hypothesis left for a later worker.

## 2. The obstruction survives real symmetric polynomial kernels

The failed plot comparison will be proved in the actual even degree-zero arity-two symmetric sector, rather than in an unrelated unsymmetrized complex space.

Write $x_0=(a,a)\in U^2$ and choose distinct $\theta_j>0$ tending to zero. The directions of

$$
\xi_j=(1+\theta_j,-1)
\tag{75.3}
$$

are admissible at $x_0$ and approach the forbidden pair-normal direction. Their orbits under sign and coordinate exchange are pairwise disjoint: the coordinate ratio of $\xi_j$ is less than minus one, the ratio after exchange is between minus one and zero, and distinct $\theta_j$ give distinct ratios.

Use the countersequence construction in the proof of Theorem 34 of the cited paper, with isolated boundary-approaching rays of this form. The specific published input needed here is the following: it supplies compactly supported terms $v_j$ with wavefront the chosen single ray, and partial sums $Q_m=\sum_{j\le m}v_j/j!$ which are bounded and Mackey-Cauchy in the inductive topology. The terms have a common compact support, and their limiting distribution has wavefront in the closure of those rays. The construction permits the isolated rays to be chosen inside this open cone.

Let $\tau(x,y)=(y,x)$ and set

$$
S_m=\tfrac12(1+\tau^*)\,\mathrm{Re}Q_m.
\tag{75.4}
$$

Complex conjugation and coordinate exchange are continuous for (75.2): they act continuously on each normal sector into its sign-changed or exchanged sector. Hence $(S_m)$ is a bounded Mackey-Cauchy sequence of real symmetric admissible kernels with a common compact support.

At each chosen ray, exactly one of the four transformed single-ray terms is singular. Their distinct wavefront directions prevent cancellation in any finite partial sum. Thus, for every $j\le m$,

$$
(x_0,\xi_j)\in\mathrm{WF}(S_m).
\tag{75.5}
$$

There is no closed admissible cone containing the wavefronts of all $S_m$, or even of any tail of that sequence: closedness would also include the forbidden limiting ray. This observation is stronger than merely knowing that a bounded set might fail a seminorm bound in a fixed sector.

The same isolated-ray argument for the distributional limit shows that it contains every chosen ray and hence their forbidden limit. Therefore the real symmetric subspace itself also fails sequential completeness; this is not an artifact of complex scalars or missing permutation invariance.

## 3. An explicit global-LCS smooth curve with no refined lift

Take a scalar smooth bump $\rho$ supported in $(-1,1)$ with $\rho(0)=1$. Define

$$
t_m=2^{-m},\qquad
d_m=2^{-m-3},\qquad
a_m=2^{-m^2},
\tag{75.6}
$$

and, on the real parameter line, put

$$
c(t)=
\begin{cases}
\displaystyle\sum_{m\ge1}
a_m\rho\!\left(\frac{t-t_m}{d_m}\right)S_m,&t>0,\\
0,&t\le0.
\end{cases}
\tag{75.7}
$$

The bump intervals are pairwise disjoint. At each nonzero parameter at most one summand occurs, so no infinite summation inside an incomplete space is needed.

**Theorem 75.3.** The curve $c$ is Bastiani smooth into the real symmetric subspace of $E_2^{\mathrm{ind}}$, with every derivative at zero equal to zero. It is not a locally normal plot in the sense of 069.

**Proof of smoothness.** For any continuous seminorm $p$ on the global inductive limit, boundedness of $(S_m)$ gives a finite constant $M_p=\sup_m p(S_m)$. Away from zero the curve is a finite smooth expression. On the bump interval indexed by $m$, its derivative of order $k$ satisfies

$$
p(c^{(k)}(t))
\le
M_p\|\rho^{(k)}\|_\infty
2^{-m^2+(m+3)k}.
\tag{75.8}
$$

There $|t|$ is comparable to $2^{-m}$. Multiplying (75.8) by any fixed negative power $|t|^{-r}$ only adds $mr$ to the exponent, up to a constant independent of $m$. For fixed $k,r$, that exponent tends to minus infinity quadratically. The estimates give continuity at zero of all candidate derivatives and the difference-quotient limits needed inductively, with value zero. They hold for every continuous seminorm, hence in the actual locally convex topology. No completion of that topology is used. For a finite-dimensional parameter line these continuous iterated derivatives are precisely Bastiani smoothness.

**Proof of failed lift.** If $c$ were a locally normal plot near zero, one fixed compact support and one fixed closed admissible cone would contain every value there. At the centers,

$$
c(t_m)=a_m S_m,\qquad a_m\ne0.
\tag{75.9}
$$

Multiplying a distribution by a nonzero scalar does not change its wavefront set. Consequently that one cone would contain every tail wavefront in (75.5), and by closedness the forbidden limiting ray. This is impossible. $\square$

The forward identity from the locally normal DVS to the Bastiani plot structure of the global inductive LCS is smooth, since every sector inclusion is continuous linear. Theorem 75.3 proves that its inverse identity is not smooth. Thus the two specified differentiable structures are not identified by their underlying distributional identity.

## 4. Consequences and retained boundaries

The ordinary global support/cone union is not a complete regular replacement for the locally normal model. Its smooth plot class is different, and the curve above gives an actual failed local-sector lift. This settles the previously open ordinary-topology identification in the negative.

The formal total-weight completeness, smooth multimorphisms and completed differentiable Weiss theorem of 069 concern the expressly defined refined DVS. They remain valid in their own category. This note does not claim that every operation on the ordinary inductive LCS is discontinuous, that every alternative comparison is impossible, or that the refined model lacks a completion.

The uniform positive-regulator endpoint remains a separate R1 theorem. Excluded collision kernels, global renormalized BV/QME and original degree-two liquid surjectivity are not settled here. Keep those obligations open until their actual proofs or counterexamples are obtained.

The [exact fixture](fixtures/check_global_cone_plot_obstruction_075.py) checks cone geometry, sign/permutation orbit separation, disjoint bump intervals and the quadratic flatness exponents. It does not numerically construct the distributions, establish the published bounded-sequence theorem or prove an infinite topological statement.
