# CSM-G2-WP14 — conditioned small gain for interacting statistical networks

**Status:** internally proved candidate theorems, exact rational implementation and finite regression evidence. Originality UNADJUDICATED; no independent mathematical certification or MATHCERT. Continues WP13, PR #3703, protected revision d7b4cf58fcd3a639d2f294473860f1108810bcf8.

## 1. Genuine interacting dynamics and conditioned observables

Let $V$ be a finite set of constituents. Component $i$ has finite hidden alphabet $X_i$, output port alphabet $Z_i$, and ordered distinct parent list $\mathrm{pa}(i)\subset V$. The supplied rational tables

$$
T_i^a(y_i\mid x_{\mathrm{pa}(i)})>0,\qquad
\sum_{a\in Z_i,y_i\in X_i}T_i^a(y_i\mid x_{\mathrm{pa}(i)})=1
$$

define the joint labelled transition

$$
T^z(y\mid x)=\prod_{i\in V}T_i^{z_i}(y_i\mid x_{\mathrm{pa}(i)}).
\tag{1}
$$

Unlike WP13, the microscopic transitions themselves depend on other constituents. This model permits directed cycles and mutual feedback across time; it assumes conditional independence of the labelled updates at each step given the previous slice. It does not cover arbitrary within-slice interacting update laws. The finite unlabelled chain is strictly positive, so has a unique stationary row without constructing that row in the verifier. A previously certified isolated factor is not interchangeable under interactions solely because its isolated observable law is equivalent: the interacting parent-conditioned kernel must be preserved.

The goal is uniform continuity of the next observed output under a common observed suffix of length $n$, including predictions conditioned on arbitrary other current output ports. This is stronger than decay of correlations with observations marginalized. Use the wildcard factor $T_i^*=\sum_a T_i^a$ for an unobserved port. All local bounds below range over both individual labels and the wildcard. This allows partially clamped future outputs without recomputing a certificate.

## 2. Local conditioned coefficients and finite factor reuse

For a positive function $f$ on a finite product, define the pair cross-ratio upper bound $R_{uv}(f)$ as the maximum of

$$
\frac{f(x_u,x_v,\xi)f(x'_u,x'_v,\xi)}
{f(x_u,x'_v,\xi)f(x'_u,x_v,\xi)}
$$

over all values of the two coordinates and common remaining context $\xi$. The maximum is at least one; swapping values includes reciprocals. For each local factor, take the maximum over labels including wildcard. All such maxima are rational and computed from the factor table, not the joint tensor state. A factor scope consists of its previous-slice parents and its next local variable. Its pair table is reusable at any occurrence of the identical labelled factor, up to the explicit port ordering.

**Ratio lemma.** Suppose two positive finite measures are proportional to the same positive base weight times $f$ and $g$. If the ratio $f/g$ has maximum-to-minimum ratio at most $R$, their normalized total variation distance is at most

$$
\tau(R)=\frac{\sqrt R-1}{\sqrt R+1}.
$$

Indeed, under the normalized second measure let $r=f/g\in[a,b]$, $m=\mathbb E r$. The total variation is $\mathbb E|r-m|/(2m)$. The convex chord bound on $|r-m|$ gives $(b-m)(m-a)/(m(b-a))$, maximized at $m=\sqrt{ab}$ (the constant case is zero). The code uses the smaller of two rational upper bounds: $(R-1)/(R+3)$ and the same square-root formula with the square root rounded upward to a rational dyadic grid. Both bound $\tau(R)$ from above, since $(\sqrt R+1)^2\ge R+3$. Denote the resulting rational bound by $\widehat\tau(R)<1$.

Condition on a fixed hidden boundary at time zero and on any observations or wildcards on times 1 through $N$. The hidden strip distribution has density proportional to the product of the local factors. The conditional law of a variable $(t,i)$ depends only on its incoming factor and all outgoing factors containing it as a parent. The latter are omitted at the terminal time $N$. To bound the change of this conditional law when another hidden variable $(t+h,j)$ changes, multiply the pair cross-ratio bounds of all incident factors containing both variables and apply $\widehat\tau$. This proves an exact rational upper bound on the corresponding single-site Dobrushin coefficient. Multiple incident factors can create same-time influences between shared parents, and conditioning on future factors creates forward dependencies in the hidden specification even though the physical transition is causal.

An alternative exact local-blanket calculation enumerates the local assignments and label configurations of the incident factors and computes the maximum total variation directly. It can sharpen the factor envelope. It enumerates only the Markov blanket, not the full network, and has an explicit context budget. The default factor method computes each distinct exact factor table once per replay and uses sparse incidence assembly. No externally supplied cache values are trusted.

## 3. Single-site anisotropic small gain

Let $B,S,F$ be nonnegative matrices of conditioned coefficient bounds for time offsets $-1,0,+1$ at interior sites, respectively. Let $B^{\rm end}$ be the terminal bound, where only the incoming factor remains. These matrices act on column vectors of disagreement bounds. A sufficient certificate is a rational $0<\rho<1$ and rational vector $w>0$ satisfying

$$
(\rho^{-1}B+S+\rho F)w<w,\qquad
\rho^{-1}B^{\rm end}w<w
\tag{2}
$$

componentwise. Denote the maximum ratio of either left-hand side to $w$ by $q<1$. In each of these row types, write the diagonal contribution as $d_i$ and the weighted off-diagonal contribution divided by $w_i$ as $e_i$. Condition (2) says $d_i+e_i<1$ or equivalently $e_i/(1-d_i)<1$. The code reports both internal and cross-component budgets, not merely an aggregate spectral assertion.

**Proof of strip comparison.** Take two fixed hidden boundary states, with identical observed/wildcard pattern on the strip. Run the coupled random-scan heat-bath chain, updating the same site in each copy with a maximal coupling of the two local conditional laws. Finite strict positivity gives irreducible marginal heat-bath chains with the desired strip measures as their unique stationary distributions. A stationary coupling exists by finiteness. Write $e_{t,i}$ for its disagreement probabilities. At stationarity, conditioning on the update site and telescoping one differing conditioning variable at a time gives the componentwise inequalities $e_{t,i}\le (B e_{t-1}+S e_t+F e_{t+1})_i$ on interior times and the terminal analogue. Include the fixed boundary disagreements $e_{0,i}\le1$. In the weighted supremum on the finite strip with weights $w_i\rho^t/\min_j w_j$, any maximum greater than one would occur at a free site and would be at most $q$ times itself, by (2), a contradiction. Consequently

$$
e_{t,i}\le \frac{w_i}{\min_j w_j}\rho^t .
\tag{3}
$$

The same conclusion holds for arbitrary initial priors: the conditioned strip laws are mixtures of the fixed-boundary laws, with possibly different boundary mixing weights. Mix a coupling for each pair of boundaries using any coupling of these weights. No assumption of a product prior is made.

Sparse positive weights can be discovered using the monotone map $w\mapsto\mathbf1+\max(Aw,A_{\rm end}w)$, where the maximum is componentwise and $A,A_{\rm end}$ are the two tilted nonnegative matrices in (2). If strict feasible weights exist for that rate, scale them to a finite supersolution of this iteration; iteration from one is monotone and bounded and converges to a fixed point with strict slack. Thus finite iteration succeeds eventually at any such fixed rate. The implementation tries uniform weights over a finite rational rate list first, then a bounded sparse iteration, and optionally an exact dense solve for a conservative common row envelope. Candidate weights are always checked by (2). Finite search exhaustion is undecided. Rational rates and weights are dense in the strict feasibility domain.

## 4. Trajectory-block theorem: strong internal memory, weak interactions

The single-site condition may fail merely because a constituent has strong temporal memory, even with very weak spatial interactions. The following block comparison avoids requiring small internal memory.

Condition on every other constituent trajectory and on all observations or wildcards in a finite strip. The conditional distribution of the entire time-column of $i$ is a positive inhomogeneous nearest-neighbor chain with unary factors and pair factors along time. Its own incoming factor is the only possible pair factor, since distinct parent variables appear at the same previous time. All other incident factors contribute unary weights to the time-column. In particular, conditional transition matrices of this chain, in either time direction, have row total variation contraction at most

$$
\kappa_i=\widehat\tau(R_{\text{own parent},\text{child}}(T_i))<1
$$

when $i$ is its own parent; set $\kappa_i=0$ when it is not. The ratio lemma proves this bound even after multiplying columns by arbitrary positive future or past messages. Arbitrarily strong positive internal dynamics are therefore permitted, at the cost of $\kappa_i$ near one.

### A localized exterior perturbation

Fix a factor occurrence and an exterior variable of spatial component $j\ne i$ in its scope. Its change affects at most two consecutive internal time variables of column $i$. Relative to the exterior time, the affected internal interval is $[\ell,u]\subset[-1,1]$. Let $a$ be $\widehat\tau$ of the product of the pair cross ratios of that exterior variable with each of the internal coordinates of the factor. Telescoping over the internal coordinates shows this product bounds the oscillation ratio of the changed factor as a function on the internal interval. By the ratio lemma the marginal law on the affected interval changes by at most $a$ in total variation. Couple the two interval marginals maximally; outside the interval, conditional distributions have the same factors, so propagate the coupling in either time direction using maximal conditional couplings. The marginal disagreement at internal time $r$ is then bounded by $a\kappa_i^{\mathrm{dist}(r,[t+\ell,t+u])}$ for an exterior perturbation at time $t$. This assertion is simultaneous in $r$: if the central interval agrees, couple its exterior identically; otherwise propagate to both sides with the stated chain contraction. Truncating an interval at a fixed boundary only improves the bound, and factors depending solely on fixed variables have zero effect.

If several exterior variables or factor occurrences change, replace them sequentially, gluing the resulting couplings through their common intermediate measures. The triangle inequality for disagreement probabilities gives the sum of the localized bounds, simultaneously at every time. Intermediate chain distributions remain positive and all their pair factors retain the same internal bound, since the factors are selected from the original contexts one by one. A change of the own initial boundary has disagreement at time $r$ at most $\kappa_i^r$, by the same forward chain coupling with common future factors.

### Temporal response and small gain

Take $\max_i\kappa_i<\rho<1$. For each exterior perturbation type $(j,\ell,u,a)$ of column $i$, define its tilted temporal response by the exact geometric sum

$$
\begin{aligned}
W(\kappa,\rho,\ell,u)
&=\sum_{h\in\mathbb Z}\kappa^{\mathrm{dist}(0,[h+\ell,h+u])}\rho^h\\
&=\sum_{h=-u}^{-\ell}\rho^h+
 \rho^{-u}\frac{\kappa}{\rho-\kappa}+
 \rho^{-\ell}\frac{\kappa\rho}{1-\kappa\rho}.
\end{aligned}
\tag{4}
$$

Use $0^0=1$ for the central terms. The formula follows by splitting the sum into the central interval and two geometric tails. No time-strip enumeration is required.

Define a sparse spatial interaction matrix $G(\rho)$ with zero diagonal by adding $a W(\kappa_i,\rho,\ell,u)$ to $G_{ij}(\rho)$ for each such local factor occurrence type. Count a parent position and a child position of the same exterior spatial component separately when they correspond to different times. This is a local factor incidence calculation. A sufficient certificate is

$$
\boxed{G(\rho)w\le q w,\quad w>0,\quad q<1,\quad\max_i\kappa_i<\rho<1.}
\tag{5}
$$

**Proof.** Couple the random-scan block heat-bath chain that updates a full constituent time-column at each step. Strict positivity again yields unique marginal stationary laws and a stationary coupled chain. Use the simultaneous column couplings just established at each update. For free times $r$, the stationary disagreements satisfy

$$
e_{r,i}\le \kappa_i^r+
 \sum_{\text{perturbation types }(j,\ell,u,a)}
 \sum_{t=0}^{N} a\kappa_i^{\mathrm{dist}(r,[t+\ell,t+u])}e_{t,j}.
$$

The formula conservatively includes types and boundary times whose factor occurrence may be absent. Divide by $w_i\rho^r/\min_j w_j$, and bound the finite time sum by the full nonnegative sum (4). The normalized boundary disagreement is at most one and the normalized internal-boundary term is at most one. Let $E$ be the maximum normalized disagreement over all sites and times. If $E>1$, at a maximizing free site we have $E\le1+qE$. Thus

$$
e_{r,i}\le \frac{w_i}{\min_j w_j}\frac{\rho^r}{1-q}.
\tag{6}
$$

As in Section 3, arbitrary priors follow by mixtures of fixed-boundary couplings. The constants are independent of strip length and, for bounded local margins and uniformly bounded weight ratio, independent of the number of constituents. The column construction is a proof tool: the verifier does not perform block Gibbs sampling, enumerate hidden trajectories, or construct their tensor state space.

### Reusing isolated constituent certificates under perturbation

For each isolated positive constituent supply its own labelled table $T_{i,0}$ depending only on its own parent or no parent. Let $\kappa_i^0<1$ be the locally verified isolated internal chain bound. Suppose the actual interacting table is verified entrywise to obey

$$
1-\epsilon_i\le \frac{T_i^a(y\mid x)}{T_{i,0}^a(y\mid x_i)}
\le1+\epsilon_i,\qquad 0\le\epsilon_i<1 .
\tag{7}
$$

The same relative bound holds for the wildcard sum. The baseline cross ratio for a pair spanning distinct spatial components is one, because the isolated factor depends on only its own component. The relative perturbation therefore bounds that pair ratio by $((1+\epsilon_i)/(1-\epsilon_i))^2$. For an internal pair it multiplies the isolated ratio by at most the same factor. Using the ratio lemma and the addition identity for $(\sqrt R-1)/(\sqrt R+1)$ gives the rational bounds

$$
\kappa_i\le \frac{\kappa_i^0+\epsilon_i}{1+\kappa_i^0\epsilon_i},
\qquad
a\le
\begin{cases}
\epsilon_f & \text{one internal coordinate in factor }f,\\
2\epsilon_f/(1+\epsilon_f^2) & \text{two internal coordinates in factor }f.
\end{cases}
\tag{8}
$$

The latter bounds follow by multiplying pair ratios for the internal coordinates. They use only the verified isolated internal rates, the network incidence, and the actual local relative perturbation bounds. Applying (4) and (5) now gives a compositional small-gain proof without calculating the actual interacting factor cross-ratio tables. Replay compares every actual entry against the baseline and recomputes the baseline rates. This is not a substitution of merely observationally equivalent isolated realizations.

In particular, let $k_0=\max_i\kappa_i^0<1$ and choose rational $k_0<k_*<\rho<1$. For a common distortion bound $\epsilon$, internal rates are at most $k_*$ if $\epsilon\le(k_*-k_0)/(1-k_0k_*)$. Every central exterior influence is at most $2\epsilon$. Let $E_w$ be the maximum over target columns of the sum of $w_j/w_i$ over all exterior variable occurrences of incident factors (counting their time positions). Then the explicit sufficient spatial budget is

$$
2\epsilon\, W(k_*,\rho,-1,1)E_w<1.
\tag{9}
$$

All intervals are contained in $[-1,1]$ and $W$ is monotone in $\kappa$ and interval inclusion. Thus for *every* strictly positive finite isolated constituent family there is a nonzero admissible interaction neighborhood on any fixed finite incidence graph, and uniformly on graph families with bounded $k_0$ and $E_w$. This is the substantive small-gain separation: strong temporal memory is allowed; it reduces the admissible spatial perturbation budget through the explicit temporal response factor.

## 5. Observable and thermodynamic margins

For either certificate let $K=1$ for (3) or $K=(1-q)^{-1}$ for (6). Define the local port likelihood and its oscillations by

$$
g_i(a\mid x)=\sum_{y_i} T_i^a(y_i\mid x_{\mathrm{pa}(i)}),\quad
c_i=\min_{a,x} g_i(a\mid x)>0,\quad
L_{ij}=\max |g_i(a\mid x)-g_i(a\mid x')|
$$

where the last maximum is over identical parent configurations except at $j$ and the same label; set $L_{ij}=0$ for nonparents. The likelihood of port $i$ after a common observed suffix of length $n$ and with any fixed subset of other current ports clamped equals the conditional expectation of $g_i$ at the final hidden parent slice. To see this, extend the strip by one time slice, insert the fixed labels for those other ports and wildcard at all remaining ports, including $i$. Given the preceding hidden slice, the current local updates factorize, so the unobserved port $i$ has likelihood $g_i$. Apply (3) or (6) to the two posterior strips with the common extra partial clamp; evaluate the resulting coupling at time $n$. At $n=0$ use the boundary disagreement bound directly. Telescoping changes of parent states in $g_i$ bounds the probability difference by $K\rho^n\sum_j L_{ij}w_j/\min w$. Both probabilities are at least $c_i$. Thus their absolute relative discrepancy and absolute log discrepancy are at most

$$
C_i\rho^n,\qquad C_i=\frac{K}{c_i}\sum_j L_{ij}\frac{w_j}{\min w}.
\tag{10}
$$

This holds even with arbitrary other current ports clamped, not only an unconditioned marginal. For the full joint symbol use the chain rule through an ordered list of ports, so

$$
c=\prod_i c_i,\qquad C=\sum_i C_i,\qquad
\mathrm{var}_n(\log g)\le C\rho^n.
\tag{11}
$$

The sum of local constants avoids an exponential factor $1/c$ in the continuity estimate. Local constants can remain dimension independent; full-vector non-nullness generally is not. Uniform finite-history conditional convergence and martingale identification give positive Hölder forward conditionals on the joint finite alphabet. WP07's reversal/interval construction then gives positive Hölder reverse conditionals and an exponentially summable two-sided temporal Gibbs interaction. No infinite-spatial-volume DLR theorem is asserted.

An explicit quasi-Bernoulli lower constant also follows. In the chain rule for $p(v\mid u)/p(v)$ compare each port after $t$ shared output slices; its ratio is at least $\max(c_i,1-C_i\rho^t)$. Choose an integer $n_0$ with $R=C\rho^{n_0}/(1-\rho)\le1/2$. The product of the tail ratios is bounded below by $1-R$, since the sum of all nonnegative relative error bounds in the tail is at most $R$. The same bound holds for a word ending sooner because all omitted head lower factors are at most one. Hence

$$
b=(1-R)\prod_{t=0}^{n_0-1}\prod_i \max(c_i,1-C_i\rho^t)>0,\qquad
p(uv)\ge b p(u)p(v).
$$

All constants are rational. To avoid enormous exact powers at near-marginal inputs the implementation bounds the tail product computation by a step and denominator-bit budget. On exhaustion it returns the compact positive lower bound $\frac12 c^{n_0}$ as a coefficient/base/exponent record, using $n_0=\lceil1/(1-\rho)\rceil \max(0,\lceil\log_2(2C/(1-\rho))\rceil)$, with the zero-constant case handled before this calculation. Bernoulli's inequality gives $\rho^{\lceil1/(1-\rho)\rceil}\le1/2$, proving sufficiency. This does not assert a materialized rational where only its compact expression is retained.

## 6. Verification complexity and evidence

The factor-envelope computation is finite in each explicitly supplied local table, involving pair cross ratios over pairs of coordinate values and local contexts. If local arities and alphabet sizes are bounded, this is bounded work per distinct factor. Assembly of the single-site or column influence coefficients uses only the scopes and their local pair incidences. In the perturbative variant use isolated internal rates and scan actual local labelled entries for (7); neither the local blanket nor global transition matrix needs enumeration. Given $\rho,w$, the sparse gain inequalities use work proportional to the number of assembled coefficients, and the port oscillations are computed from the local tables. Exact rational arithmetic is used throughout. The optional exact-blanket method can be exponential in blanket size, not network state count. Weight discovery is bounded and may use dense solves for small networks; sparse monotone iteration is sufficient in principle at a strictly feasible rate, without a universal polynomial-time bound on the required iterations. No joint output alphabet is enumerated for (10) or (11). The optional explicit scalar concatenation constant can have large bit length; its compact fallback is specified above.

The reference implementation is interacting_small_gain.py. Regression tests materialize only small joint networks as independent-in-method oracles. The production verification paths never build a joint lift. The genuine interacting binary ring has

$$
\Pr(Y_i=1\mid X)=\tfrac12+a(2X_i-1)+b(2X_{i-1}-1),
$$

with noisy output matching $Y_i$ with probability $5/8$. Here $a,b$ are local transition coefficients, not the quasi-Bernoulli constant. Each neighbor coefficient below is strictly positive.

| Model / verifier | Temporal rate | Gain upper (rounded) | Evidence |
| --- | ---: | ---: | --- |
| 128-site ring, a=1/8, b=1/32; single site | 13/32 | 0.945015 | One distinct factor table; per-port c=59/128, C=10/59 |
| 17-site heterogeneous feedback star; weighted single site | 3/4 | 0.987239 | Unit-weight gain exceeds 2; sparse weights suffice |
| Strong ring, a=7/16, b=1/4096; trajectory column | 29/32 | 0.266514 | Internal rate 57345/65537; same local bound for 2, 3, 128 sites |
| Same strong ring; isolated perturbation replay | 29/32 | 0.546504 | Isolated rate 7/8; relative distortion 1/256; internal bound 120/137 |
| Near-persistent ring, a=15/32, b=1/16384; column | 31/32 | 0.162602 | Internal rate greater than 15/16; weak nonzero interactions |

The strong and near-persistent specimens fail the tested uniform-weight single-site search but pass the trajectory-block test. The three-site moderate ring has a sharper exact-blanket certificate at rate 3/8. The strong 128-site column certificate also provides a compact all-word concatenation lower bound when materialization exceeds the configured bit budget. A conditioning-amplification control has iid unlabelled hidden dynamics but strong labelled XOR-type factors, and the conditioned certificate refuses acceptance despite zero unobserved gain. Its observed law is itself iid; this is a control on sufficient-criterion failure, not a non-Gibbs counterexample. All accepted factor tables are strictly positive; structural-zero generalization remains open.

Nine exact tests cover factor bounds against local exact enumeration, a three-state/three-label fixture and mixed arity, exact small-network full-tensor filtering under every shared suffix through length three and every initial boundary state including partial current-port clamps, nontrivial observed cross-time dependence, concatenation comparisons, 128-site size invariance, asymmetric weighted gains, hostile witness rejection and near-marginal compact bounds, conditioning amplification, exact temporal response sum, strong-memory column and perturbation replay, and iid controls. Initial regressions found a three-state test table arity error and a loop variable shadowing a test transition coefficient; these fixture errors were repaired. Code/test candidate 7a1fb40661f497101d63e81374c338db1c966d3b passed 9/9 exact tests in capture cff29fc2018249f381017356662458d8. Parameter readouts: moderate/weighted network capture 557f749d98a2472d80d1e91463c8a847; strong column capture 437473aa1f084ef2af216f9d6d4c78a6; isolated perturbation capture 00ba708084a3467880eb40f38e0e6aa2. Independent execution attestation flags are false. Final proof/code/test head replay required.

## 7. Prior art and boundary

The main mechanisms are established comparison theory. Rebeschini and van Handel, [Comparison Theorems for Gibbs Measures](https://arxiv.org/abs/1308.4117), Corollary 2.6 and Theorem 4.2, give classical and block comparison and explicitly distinguish weak spatial interactions from internal temporal correlations in high-dimensional filtering. Their [Phase Transitions in Nonlinear Filtering](https://arxiv.org/abs/1401.6450), Example 2.1 and the infinite-dimensional examples, show why unconditioned ergodicity does not in general imply conditional stability. Kuelske and Opoku, [The posterior metric and the goodness of Gibbsianness for transforms of Gibbs measures](https://arxiv.org/abs/0711.3764), develop continuity estimates under conditioned Dobrushin uniqueness for local transformations. Primary HTML material was inspected; full theorem-level equivalence and novelty adjudication are open. The ratio lemma is classical projective contraction/likelihood-ratio control; the weighted comparison proof is not claimed as a new Dobrushin theorem. The scoped contribution is an explicit exact rational, port-clamp-uniform certificate calculus for local labelled transitions, its trajectory-column response formula and verified perturbation reuse of isolated interfaces, with temporal Gibbs margins and tested sparse-network realizations. Originality UNADJUDICATED.

**Disposition:** internally established sufficient observable small-gain theorem for genuine finite interacting dynamics; single-site and trajectory-block methods, and explicit local perturbation certificate admitting arbitrarily persistent strictly positive isolated constituents for sufficiently weak interactions. All mathematically conditional and finite. No public certification, full tensor construction for acceptance, universal discovery complexity, or negative-instance decision. The remaining frontier is to replace strictly positive internal table bounds by reusable observable/hidden quotient certificates with support-aware compatibility under interactions, sharpen the temporal response and interaction budgets, and investigate infinite-spatial-volume limits and conditional phase-transition obstructions.

**Next boundary:** CSM-G2_SUPPORT_AWARE_INTERACTING_QUOTIENT_AND_SPATIAL_LIMIT_OPEN. Keep canonical issue #3136 open.