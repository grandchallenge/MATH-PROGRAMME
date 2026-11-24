# CSM-G2-WP13 — compositional certificate reuse and adaptive packing complexity

**Status:** internally proved candidate theorems and exact rational reference implementation. Originality UNADJUDICATED. No MATHCERT or independent mathematical certification. Continues WP12, PR #3699, protected merge d7a23a3092fc794d38a1de01614ee0156e4ec174. Working base 973827504ce708843f10e461b6b24fded8ec5b19.

## 1. Scope of composition

The objects here are stationary rational finite-state laws, supplied with verified local interfaces. The independent product is a tensor operation on laws. A finite-memory stochastic observation transducer is a morphism from joint input words to output words with retained internal state. The source factors are independent before observation. We do not treat feedback, interactions that modify constituent transition laws, or arbitrary Gibbsian coarse-graining as automatically admissible. WP03's biased XOR obstruction continues to forbid unconditional closure.

For fully revealed independent products, no new geometry is needed. If factor $i$ has non-nullness $c_i$ and conditional log variation at common suffix length $n$ at most $C_i\eta_i^{\lfloor n/L_i\rfloor}$, then the product likelihood is the product of the factor likelihoods, and its log variation is bounded by their sum. Choose rational $0<\theta_i<1$ with $\eta_i<\theta_i^{L_i}$ and take $\theta=\max_i\theta_i$. A product certificate is

$$
c=\prod_i c_i,\qquad
\mathrm{var}_n(\log g)\le
\left(\sum_i C_i\theta^{-(L_i-1)}\right)\theta^n .
$$

It requires only replay of the factor certificates. In particular no tensor matrix, product predictive chart, or Cartesian product of cell graphs need be materialized.

## 2. A reusable positive transfer interface

For a certified factor with rational observable chart matrices $A_a$, stationary row $x_*$ and terminal column $e_0$, a positive interface consists of strictly positive rational labelled matrices $T_a$, their positive stationary row $\pi$, and a rational matrix $V$ with first column one, such that

$$
T_aV=VA_a,\qquad \pi V=x_* .
$$

Require $\sum_aT_a$ row stochastic and $\pi$ stationary; replay these identities exactly. Then $\pi T_w\mathbf1=x_*A_we_0$ for all words. Thus the interface preserves the factor law exactly, not merely a finite set of moments. The terminal identity is $Ve_0=\mathbf1$. The interface need not be minimal.

The reference compiler replays a single-letter WP12 cover, takes the coordinate bounding box of its cells, and tries rational positive paddings until all projective maps send the box strictly into its interior with positive denominators. If successful, use its corners as the new states. For a corner $v$ and symbol $a$, express $F_a(v)$ by the positive multilinear barycentric weights on all corners: each free coordinate contributes the fractional position in its interval or its complement. Multiply each weight by $(vA_a)_0$ to obtain the row of $T_a$. This gives strictly positive rational matrices and exact intertwining. Their sum is stochastic by cylinder normalization. Solve its stationary equations and verify the stationary intertwiner. Alternatively it follows by positive stochastic convergence from any weights representing $x_*$ in the box.

This fast compiler is sufficient, not complete: its axis-aligned enclosing box may fail even when the law is regular. It has explicit padding and vertex budgets. A native positive labelled realization can be used directly. More generally WP10's strict-polytope realization theorem gives existence of a positive rational interface for every factor in the positive Hölder class. A finite factor-local constructive route follows from Section 6: use the same packing construction with reuse separation $R/4$ and contraction bound $1/2$, yielding strict inclusion into target boxes with slack at least $R/4$. Convexify these boxes; every block image of the resulting polytope lies in its relative interior, since it is a convex combination of interior images. The all-word denominator bounds hold on this polytope. The backward intermediate-polytope construction of WP10 then makes a strictly invariant one-letter rational polytope. Exact rational hull membership and positive barycentric coefficients are finite checks; dyadic interior thickening terminates by compactness and strict margins. This gives a general factor-local existence and synthesis route, potentially expensive; only the fast box compiler is implemented here. Nothing in the composition theorem depends on success of that particular compiler.

Each positive factor stores the following local margins, with the minimum or maximum over its indicated finite indices:

$$
\lambda_i=\min_{a,x}(T^i_a\mathbf1)_x,\quad
\beta_i=\min_{a,x,y} T^i_a(x,y)/\pi^i_y,\quad
\gamma_i=\max_{x,y}Q^i(x,y)/\pi^i_y,\quad
Q^i=\sum_a T^i_a .
$$

All are positive, and the last is at least one. Retain also per-letter minima/maxima of the row sums and entries relative to $\pi^i$. The baseline proof uses only the three scalar margins. The optional refinement uses the per-letter arrays. These are verified from the actual positive interface, not inferred from untrusted cached numbers.

## 3. Finite observation transducers and exact network reuse

Let $I$ be the joint input alphabet (ordered tuples of factor symbols), $Z$ the output alphabet, and $E$ a finite interface-state set. The transducer is

$$
K(z,t\mid h,a)\ge0,\qquad
\sum_{z,t}K(z,t\mid h,a)=1
$$

for $h,t\in E$, $a\in I$. At each step it reads one joint input, emits one output, and updates its state using independent conditional randomization. A window of memory $r$ is the special case with $E=I^r$, deterministic shift of the history and the specified stochastic observation probabilities. The exact lifted transfer, used only in the proof and reference tests, is

$$
S_z((h,x),(t,y))=
\sum_{a\in I}K(z,t\mid h,a)\prod_i T^i_{a_i}(x_i,y_i).
$$

We do not need to form this matrix for certification.

For serial composition of $K$ and $L$ with matching ports, retain both interface states and sum the intermediate output:

$$
(L\circ K)(w,(t,u)\mid(h,g),a)
=\sum_z K(z,t\mid h,a)L(w,u\mid g,z).
$$

This is stochastic and exactly represents a cascade, including shared intermediate randomization and overlapping windows. In particular it does not incorrectly replace a stochastic cascade by independent per-site noise on the original input window. Parallel composition of independent transducers is the tensor product of these transition kernels with ordered product ports. Identity is the memoryless deterministic identity on symbols. Finite summation and multiplication prove associativity and the identity laws up to canonical reindexing; the reference implementation's lexicographic ordering realizes these exact identities. The product construction assumes disjoint independent source factors in parallel branches; shared copies of an input must instead be represented by the same joint port in one transducer.

The reusable network representation consists of the original positive factor interfaces and the composed transducer. New serial readouts or independent parallel networks require only the new finite port operation and compatibility check. Factor margins need not be recomputed during composition; exact replay can recompute all margins from their original interfaces. No new composite observable quotient is required. The transducer state count and port alphabet can still grow with network topology, and the compatibility test need not pass after arbitrary composition.

## 4. Compatibility by universal support synchronization

Define the Boolean support relation for each output letter $z$ by

$$
R_z(h,t)=1\quad\Longleftrightarrow\quad
\exists a: K(z,t\mid h,a)>0 .
$$

Require every row of every $R_z$ to be nonempty. Then every possible input interface state can emit every output. For a nonempty subset $U$ of interface states let $R_z(U)$ be the union of reachable next states. Say that the transducer synchronizes in support at length $s$ if for every output word of length $s$ all initial singleton sets have the same nonempty image set. The image set may depend on the word and need not be a singleton or the whole state space.

**Exact finite decision for this compatibility condition.** Construct the reachable graph of unordered distinct nonempty subset pairs, starting with all pairs of distinct singletons. For each output letter advance both subsets simultaneously. If they become equal, drop the edge from the unequal graph, because equality persists under all subsequent letters. Every reachable directed cycle permits arbitrarily long words with unequal support sets; conversely, if the graph is acyclic, all paths staying unequal have bounded length. The least synchronizing length is one plus the maximum number of edges in such a path (one when there are no distinct initial pairs). Compute by topological sorting. The graph has at most

$$
\binom{2^{|E|}-1}{2}
$$

nodes and at most $|Z|$ outgoing edges per node. This bound is exponential in interface-state count, not in microscopic tensor dimension. Reachable graph construction avoids enumerating all long output words. A node budget produces undecided, not a compatibility decision. Missing row labels or a reachable unequal cycle are genuine obstructions to this particular sufficient condition, not obstructions to Gibbs regularity itself.

This is a stronger support condition than ordinary overlap of row supports. It is needed here to compare likelihood ratios on the *same* positive columns. The related avoiding-set graphs in consensus theory use different conditions on stochastic products; we do not import their complexity lower bounds as results about this condition.

## 5. Compositional contraction theorem

Suppose each constituent interface is strictly positive and the transducer passes support synchronization at length $s$. Put $\alpha$ equal to the minimum positive entry of $K$. Let $\lambda=\prod_i\lambda_i$, $\beta=\prod_i\beta_i$, $\gamma=\prod_i\gamma_i$, and $\Pi_y=\prod_i\pi^i_{y_i}$. Then every output word $w$ of length $s$ has a lifted transfer $S_w$ with common nonempty column support across all rows. Indeed its positive microscopic paths are exactly the interface paths of $R_w$, because all labelled factor entries are positive. Whenever a terminal interface state is allowed by that word, every microscopic terminal state is allowed, irrespective of the initial microscopic state.

For a supported column $(t,y)$, select one positive interface/input path of length $s$ from the initial interface state. The product of its transducer weights is at least $\alpha^s$. In the first $s-1$ microscopic steps, summing over all intermediate microscopic states gives a lower bound $\lambda^{s-1}$ on mass. The final transition contributes at least $\beta\Pi_y$. Thus each supported entry is at least $\alpha^s\lambda^{s-1}\beta\Pi_y$. For the upper bound, sum over all transducer outputs and paths: the microscopic marginal is the independent product of $Q_i^s$. The last unlabelled transition gives $Q_i^s(x_i,y_i)\le\gamma_i\pi^i_{y_i}$. Therefore each supported entry is at most $\gamma\Pi_y$.

Set

$$
\delta=\min(1/2,\alpha^s\lambda^{s-1}\beta/\gamma),
\qquad c=\alpha\lambda,\qquad \eta=1-\delta.
$$

The minimum-to-maximum ratio of any nonzero column of every complete block is at least $\delta>0$. Every original single-symbol likelihood from any joint prior is at least $c$: each interface row has at least one permitted input/next-state path for the symbol, and the microscopic row sum for that input is at least $\lambda$. All output words have full support.

For any two normalized nonnegative initial rows $x,y$, consider the ratio of their unnormalized messages after the first complete common block. On its common support the ratios lie in $[\delta,\delta^{-1}]$. For each next block and supported target column, the new ratio is a convex average of the preceding ratios. In this average the weight on each input index is at least $\delta$ times its probability under the normalized current $y$ message: the numerator weight is proportional to $y_i S_w(i,j)$ and the column minimum is at least $\delta$ times its maximum. Hence these averages all share the common component of weight $\delta$ given by the normalized $y$ message. The oscillation (maximum minus minimum) of ratios contracts by at most $1-\delta$ per complete block; the minimum cannot decrease and the maximum cannot increase. Zero coordinates of the common input support are simply omitted. This argument does not assume strict positivity of the full lifted matrices.

The ratio of the two subsequent conditional single-letter likelihoods is the ratio of two weighted averages of the current message ratios, one weighted by the final likelihood column and one by the terminal column. Both averages lie between the current minimum and maximum. Its absolute relative discrepancy and its absolute logarithm are therefore bounded by the oscillation divided by the minimum. After $q\ge1$ complete blocks, this is at most $\delta^{-2}\eta^{q-1}$. Absorb the initial remainder of a shared suffix into each preceding history. At suffix lengths below $s$, use single-letter non-nullness and the trivial relative/log bound $1/c$. In particular

$$
\mathrm{var}_n(\log g)\le
C\eta^{\lfloor n/s\rfloor},\qquad
C=\max(1/c,\delta^{-2}/\eta).
\tag{1}
$$

Uniform convergence and martingale identification give positive Hölder forward conditionals. WP07 time reversal and its interval construction give positive Hölder reverse conditionals and an exponentially summable two-sided Gibbs interaction.

There is also a direct all-word quasi-Bernoulli bound with no long tail product: $b=\delta$. If $v$ has length at least $s$, start from the posterior after $u$ and from the stationary prior. After the first complete block of $v$ their unnormalized messages are pointwise comparable by $\delta$ and $\delta^{-1}$; nonnegative continuation preserves this comparison. If $v$ is shorter, sum the comparison over all extensions to length $s$. Thus

$$
\delta p(u)p(v)\le p(uv)\le\delta^{-1}p(u)p(v).
\tag{2}
$$

These bounds concern any stationary law of the lift. Under the compatibility condition the stationary law is unique: the unlabelled lifted transfer raised to power $s$ has the same nonempty row support (the union of the output-word supports), and strictly positive entries on those columns. Its restriction to that recurrent support is positive stochastic. It follows that every initial row converges under the unlabelled chain. Stationary output laws are determined by the input cylinder law and the transducer: start with any fixed interface state and stationary microscopic input law, then take the stationary limit. Therefore replacement by equivalent factor interfaces is valid even for general finite transducers, not just fixed-window kernels.

### Optional tighter local path bound

For each joint input letter take the products of the per-factor minima/maxima of labelled row sums and labelled entries divided by stationary column mass. Use these as weights on the finite transducer transitions. For a fixed output word of length $s$, multiply the history-level lower and upper row-sum weighted matrices for its first $s-1$ letters, then the lower and upper stationary-entry weighted matrices at the final letter. The resulting entry bounds $L_w(h,t),U_w(h,t)$ satisfy

$$
L_w(h,t)\Pi_y\le S_w((h,x),(t,y))\le U_w(h,t)\Pi_y .
$$

The proof is the same path summation, now retaining each input path's individual weights instead of a common scalar minimum. Support synchronization implies for each nonzero upper column all lower entries are positive. The minimum over these columns and block words of the ratio of minimum lower entry to maximum upper entry, capped at $1/2$, can improve $\delta$. Use the larger of this refinement and the baseline. The one-letter likelihood bound is similarly improved by summing input-specific row-sum lower bounds over the transducer transitions. This optional refinement enumerates only short output words under an explicit budget; the baseline has no long-word enumeration. Both proofs require only factor margin arrays and the transducer, not the joint microscopic matrices.

The work to compute factor margins scales with the sum of their explicit labelled matrix sizes. Baseline support analysis scales with the reachable unequal-subset-pair graph and the explicitly specified transducer; it does not depend on the product of microscopic dimensions. The per-letter joint alphabet and the transducer description can themselves be exponential for a large network. The result is not a polynomial-time theorem in an arbitrary succinct network description.

## 6. Constructive adaptive packing with a priori cell bound

Let $d$ be the minimal predictive dimension, $k=d-1$ and $K_*$ the closed convex hull of the reachable actual predictive states in the WP10 probability-probe coordinates. These states have free coordinates in $[0,1]^k$. Assume a fixed primitive block length $s$, radius $R>0$ and bound $0\le q<1$ such that all block maps have positive denominators and Lipschitz constants at most $q$ on $K_*+RB_\infty$. Require also positive one-letter likelihoods on that neighborhood. For the factorized verification below we will use the slightly stronger componentwise secant bound furnished by the WP11 minor estimates.

Start a list of centers with the exact stationary state. For each center $x$ and primitive block $a$, compute the exact image center $y=F_a(x)$. Reuse an existing center within maximum distance $(1-q)R$ of $y$; if none exists, append $y$ as a new center. Every cell is a box of radius $R$ about its center. All centers are actual reachable states, because the initial state is stationary and all additions are exact word updates. For any point in the source box, its image differs from the image of the center by at most $qR$. The chosen destination center is within $(1-q)R$ of that image center, so the entire image is contained in the destination box. Each inclusion is checked exactly, without rounding or any unverifiable proximity assumption.

Every newly added center is separated from all previous ones by more than $(1-q)R$. Hence the number of centers is bounded by the packing number of the reachable set at that separation, and by the covering number of that set with maximum-norm balls of radius $(1-q)R/2$. More explicitly, partition each coordinate interval of diameter at most $D_*$ into bins of width $(1-q)R$ (the last may be a singleton). Each product bin contains at most one center. Thus

$$
N\le
\left(1+\left\lfloor\frac{D_*}{(1-q)R}\right\rfloor\right)^k .
\tag{3}
$$

In raw probability coordinates take $D_*=1$. This bound is on the number of cells, not on a pre-enumerated lattice or a vertex count. The algorithm is output sensitive: only images of accepted centers are explored. With a linear nearest-center scan, the search uses $O(N^2m^s k)$ comparisons plus $O(Nm^s d^2\log d)$ exact image-envelope arithmetic. A center word has at most $N$ primitive steps, since each new center is generated from an earlier center. Clearing denominators as in WP11 bounds its bit length by a polynomial in $Ns$, the rational generator bit length, and $d$. The worst-case cell count may still be large.

### Single-seed convexification and linear-in-cell verification

Unlike the general disconnected-cover proof of WP12, no shorter-prefix seeds are needed for this uniform block certificate. Let $P$ be the convex hull of the union of accepted boxes. Because every block image of every box lies in the union and denominators are positive, normalized convexity implies $F_a(P)\subset P$. Every state of a word of length divisible by $s$ is in $P$, starting from the stationary seed. Every word has positive mass because it is a suffix of a positive word whose length is divisible by $s$, using stationarity and cylinder consistency. Stationarity padding then gives $x_u\in P$ at every length as a convex combination of normalized padded states. Positivity of one-letter likelihoods extends by linearity to $P$.

For each block letter use WP12's two-point secant formula on each pair of boxes. The denominator minimum depends only on the source box; the componentwise numerator maxima depend only on the other box. For a fixed positive diagonal metric, the maximum weighted scalar secant bound over *all ordered pairs* is therefore exactly the maximum weighted numerator norm over boxes divided by the minimum denominator over boxes. This is the maximum of the conservative bounds, not necessarily the true Lipschitz supremum. It can be checked without constructing a pair graph. If it is strictly below one, say $\eta_*$, all pairs of points in the union contract under each common block by at most $\eta_*$. Every point of $P$ maps under a common block word into the convex hull of the images of union points, since all denominators on $P$ remain positive. Pairwise image diameter is at most the union diameter times $\eta_*^t$ after $t$ blocks; convexification cannot enlarge that norm diameter. Thus any histories with a shared suffix of length $n$ have the same WP12 log variation conclusion with $\eta_*^{\lfloor n/s\rfloor}$, even if their initial states lie in $P$ outside the union. We do not assert a stronger Lipschitz bound on $P$ relative to the original distance of two arbitrary points there.

The exact verifier uses one stationary seed, $Nm^s$ enclosure edges, and $O(Nm^s d^2\log d+Nmd)$ rational operations, after primitive matrices are given. It uses no quadratic pair graph, no corner enumeration, no shorter-prefix word list. It still enumerates primitive matrices of length $s$; the general WP12 graph method remains valuable when single-letter expansion requires a multi-step path-dependent metric.

### Quantitative margins imply an explicit discovery budget

Take the WP11 all-word hypotheses in raw predictive coordinates: quasi-Bernoulli lower bound $b>0$, uniform normalized matrix entry bound $J$, and every normalized two-by-two minor bounded by $H\theta^n$, with $0<\theta<1$. For $k\ge1$ choose

$$
R=\min(1/4,b/(2kJ)),\qquad D=4k(1+2k)H/b^2 .
$$

Throughout $K_*+RB_\infty$, the word denominator is at least $(b/2)p(w)$ by the same linear perturbation estimate as WP11. The coordinatewise minor identity and the sum norm bound $1+2k$ give a uniform componentwise secant column-sum bound $D\theta^{|w|}$, even when maxima of different coordinates occur at different points. Choose any $s\ge1$ with $D\theta^s\le1/2$. Use $q=1/2$ in (3). All greedy inclusion and factorized secant checks pass, with at most

$$
N\le(1+\lfloor2/R\rfloor)^k
$$

cells. This is an explicit finite construction for every positive Hölder rational law, conditional on WP07's margins and with arbitrary primitive block length. It improves WP11's sufficient block target $D\theta^s<\delta_{\rm grid}/4$ to a constant contraction target, because the centers are exact and reused by geometric proximity, not rounded to a grid. The bound is still conservative and need not improve the practical WP12 heuristic on all examples.

A convenient purely rational sufficient horizon calculation avoids incrementing $s$ or allocating a gigantic power when $\theta$ is very close to one. Set $t=\lceil1/(1-\theta)\rceil$ and $j=\max(0,\lceil\log_2(2D)\rceil)$ (take $j=0$ for $D=0$). Bernoulli's inequality gives $\theta^t\le1/2$, so $s=\max(1,tj)$ suffices. The binary logarithm ceiling is computed by integer bit lengths and exact comparison. Very large $m^s$ is returned as a symbolic base/exponent pair rather than a giant integer. This computes a conservative resource bound efficiently; it does not make the potentially exponential search efficient in the original input bit size.

For dimension one use one cell and one-symbol primitives. Without advance knowledge of margins one can try dyadic radii and primitive lengths with increasing cell budgets, verifying each candidate. The proof guarantees eventual acceptance for the positive Hölder rational class if all budgets are increased fairly. Negative instances need not terminate.

### Coupling the two advances

The compositional theorem supplies actual all-word $b,c,C,\eta,s$ from local input data. If an observable chart of the resulting law is desired, compute its finite invertible Hankel slice $G$ and $J=\|G^{-1}\|_\infty$ by WP11. Let $P_{\max}$ be the maximum actual predictive probe length. The bound (1) implies that the difference of probabilities of any one of these future probes after histories with a common suffix of length $n$ is at most $P_{\max}C\eta^{\lfloor n/s\rfloor}$: expand the probe probability into conditional factors and telescope, noting each factor is in $[0,1]$ and the common suffix only grows. Log discrepancy bounds absolute probability discrepancy on $(0,1]$. Apply WP12's row-minor argument to $G M_w$ and multiply by the exterior square of $G^{-1}$. For rational $\theta$ with $\eta<\theta^s$, this yields the uniform minor constant

$$
H=2P_{\max}C J^2\theta^{-(s-1)} .
$$

This produces a certified packing budget from the network's reusable margins and a finite Hankel computation of the same law, without an unknown spectral rate. In general these secondary constants are extremely conservative, and computing a minimal quotient itself can be costly. When only Gibbs regularity is needed, the compositional theorem avoids that quotient altogether.

## 7. Exact evidence

Two different balanced non-iid constituent laws from WP10/WP11 have existing WP12 certificates with three cells each. The fast compiler produces strictly positive interfaces of dimensions 2 and 4. Their exact stationary intertwiners are checked; all finite regression cylinder comparisons agree. The joint input alphabet has four symbols, and the first genuinely coupled readout has memory one. Its output-zero probabilities on previous/current joint inputs are set to zero at (0,3), one at (3,0), and otherwise to $(1+(h+2a+ha)\bmod3)/4$. Thus both output support relations contain structural zeros and the likelihood depends on the joint window. The output is non-iid. The second overlapping layer uses output-zero likelihoods $(3/4,1/4,1/2,1/4)$ on binary pairs in lexicographic order.

| Network | Interface states | Reachable unequal subset-pair nodes | Block | Non-nullness lower | Refined delta lower |
| --- | ---: | ---: | ---: | ---: | ---: |
| First coupled readout | 4 | 8 | 2 | 14897/73728 | 0.0000500181 |
| Two serial overlapping layers | 8 | 31 | 2 | 57247/294912 | 0.0000769047 |

Display decimals for delta are approximate; the actual values are exact fractions. The first refined delta is more than 20 times its baseline, the serial one more than 100 times. The contraction rates $1-\delta$ are close to one and the variation constants in (1) are large. This is a scalable sufficient certificate, not a sharp physical estimate of the actual relaxation rate. Neither certification path constructs the composite lift or quotient. Reference-only tests materialize the lifts and verify all supported block column ratios for the first network, and every entry of the serial transfer against the two successive lifts under exact reindexing. This establishes that the fused transducer preserves intermediate-state dependencies. Both biased and fair deterministic XOR fail support synchronization, as they must for this criterion: the former is non-Gibbs, the latter is Gibbs, so the condition is explicitly not necessary.

The new packing search uses stationary-weighted charts from WP12, tries dyadic radii and primitive lengths, and verifies uniform factorized secants in unit norm. It requires no supplied cells.

| Law | Observable dimension | Block | Cells | Enclosure edges | Pair graph edges built | Exact bound (rounded) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Balanced binary overlap | 2 | 2 | 23 | 92 | 0 | 0.712578 |
| Balanced three-state overlap | 3 | 2 | 5 | 20 | 0 | 0.528874 |
| Previously budget-limited non-iid parity overlap | 5 | 2 | 5 | 20 | 0 | 0.042648 |

These results use the strict uniform-block verifier, not the more general synchronized graph certificate. WP12 still gives more compact three-cell single-letter graph witnesses on these specimens. The new construction contributes a provable cell bound and eliminates the pair graph, not universally smaller covers. The first model uses more cells than WP12. It also proves completeness of the structured adaptive search under growing budgets; input-only polynomial complexity for general positive Hölder laws remains unresolved.

Code: compositional_certificate_reuse.py. Tests: tests/test_csm_compositional_certificate_reuse.py. Seven tests include exact factor intertwining, revealed product and coupled laws, optional refinement versus baseline, serial/parallel identities and associativity, exact serial transfer equality, exhaustive independent Boolean-product oracle on all 81 two-state/two-label nonempty-row automata, XOR controls, adaptive packing/hostile edge checks, conditional resource theorem and iid/Markov cases, malformed-interface and resource budgets. Preliminary exact parameter capture 0eee17a674154aa6975af2a2c144bf10 at candidate 55b4a40b631237cd5fc8fd880bba64168daa0dcc. Seven tests passed at candidate 13bd0dd9b2f4da0468a6930d3a1f2f74ff3e0b98, capture c1c12cd4bb12492298d26b1e05c488ff. The subsequent closed horizon bound and compact resource output require final strengthened replay. Independent execution attestation flags are false.

## 8. Prior art and boundary

Relevant established work includes Mark Piraino, [Projections of Gibbs States for Hölder Potentials](https://arxiv.org/abs/1709.07561) and [Single site factors of Gibbs measures](https://arxiv.org/abs/1905.03803), on preservation under suitable fiber mixing; Vincent Blondel and Alex Olshevsky, [How to decide consensus?](https://arxiv.org/abs/1202.3167v6), on combinatorial avoiding-set tests and NP-hardness for consensus; Antoine Girard, Giordano Pola and Paulo Tabuada, [Approximately bisimilar symbolic models for incrementally stable switched systems](https://arxiv.org/abs/0807.5022), and Giordano Pola, Pierdomenico Pepe and Maria Domenica Di Benedetto, [Compositional Symbolic Models for Networks of Incrementally Stable Control Systems](https://arxiv.org/abs/1404.0048v2), on finite abstractions and compositional small-gain design. The arXiv abstracts were checked. Full theorem-level source concordance is open. Positive realizations, tensor interfaces, finite-state stochastic kernels, support-product automata and separated-set packing are established mathematical tools. The present packet combines them into exact reusable thermodynamic margins and an adaptive observable packing certificate, with explicit hypotheses and measured examples; originality of the combination is UNADJUDICATED. No claim of inventing these established mechanisms, of arbitrary feedback closure, or of deciding general Gibbs regularity.

**Disposition:** a reusable calculus for independent products and serial/parallel finite transducer coupling through verified positive interfaces, exact finite support compatibility decision, explicit uniform thermodynamic margins, and margin-conditional a priori adaptive cover complexity with single-seed/factorized verification. All internally proved, not independently certified.

**Next boundary:** CSM-G2_INTERACTING_NETWORK_SMALL_GAIN_AND_SHARP_MARGIN_COMPLEXITY_OPEN. Extend beyond independent underlying factors and observation-only coupling to actual interacting transition laws; seek local small-gain inequalities and support-aware quotient compatibility that do not require a product of strictly positive interfaces. Develop sharper contraction and cover bounds from input structure and determine computational lower bounds for discovery. Preserve the distinction between support-criterion failure and genuine non-Gibbs behavior. Keep #3136 open.
