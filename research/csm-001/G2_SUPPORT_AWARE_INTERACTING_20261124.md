# CSM-G2-WP15 — contextual quotients, hard observation support and space-time limits

**Status:** internally proved candidate sufficient theorems and exact rational reference implementation. Originality UNADJUDICATED; no independent mathematical certification or MATHCERT. WP14 PR #3707 protected merge reconciled at f04818e191d5184959029b4ca67ef3d0cfc45133. Working protected base f4ad57e25f268f7ac18a10a4056cf978b6aa9286.

## 1. Local contextual quotient, not isolated observational equivalence

Use WP14's directed conditional-independent labelled dynamics, now with rational nonnegative local tables. Each component $i$ has hidden state set $X_i$, labels $Z_i$, ordered distinct parents $\mathrm{pa}(i)$, and rows normalized jointly over label and child state. Let $\pi_i:X_i\to\bar X_i$ be a surjection. A contextual deterministic quotient is the exact local identity

$$
\sum_{y_i:\pi_i(y_i)=b}T_i^a(y_i\mid x_{\mathrm{pa}(i)})
=\bar T_i^a(b\mid\pi_{\mathrm{pa}(i)}(x_{\mathrm{pa}(i)}))
\tag{1}
$$

for every local label, parent configuration and destination class. In particular the sum on the left must be constant across any parent configurations with equal componentwise classes. The quotient retains the original observation alphabet. Hidden distinctions relevant to any outgoing factor cannot be removed. This is stronger than equivalence of isolated cylinder laws.

**Exact transport.** On a finite network, the sum of the global product labelled transfer over a fiber of the product projection equals the product of the local sums in (1), by distributivity. Hence the global labelled transfer intertwines with the deterministic encoder. Iterating proves equality of every output cylinder law for arbitrary initial microscopic distributions and their pushforwards, including correlated distributions. In particular stationarity pushes forward. The argument also holds on a countable locally finite graph: conditional independence proves equality for every finite set of next-slice output/quotient ports, hence equality of the product transition kernel by the cylinder uniqueness theorem. Iterate in time. No microscopic global matrix need be constructed. Reducible microscopic chains, conserved invisible coordinates and structural zeros are allowed.

### Coarsest stable componentwise partition

For each local factor compute, for each microscopic parent tuple, the vector of sums over the current child classes for each label. For every component, collect signatures by substituting each of its states at each of its outgoing parent positions, holding all other parent coordinates fixed at every possible microscopic context, and recording those aggregate vectors. Split its current classes by equality of signatures. Repeat simultaneously until no class splits.

The fixed point satisfies (1): two tuples with equal parent classes can be joined by single-coordinate substitutions, each leaving every aggregate vector unchanged. Conversely, any compatible partition refining the supplied initial partition refines each intermediate partition. Indeed, if it refines the current partition, its own aggregate identities imply equality of sums into the current coarser child classes for all substitutions within its classes; it therefore cannot be split by this iteration. Induction proves the result. The terminal partition is the unique coarsest compatible componentwise refinement of the initial partition. It need not be the minimal linear predictive quotient, nor the smallest arbitrary global partition.

Every nonterminal iteration increases the total number of classes by at least one, so the number of proper refinement rounds is at most $\sum_i (|X_i|-|\bar X_i^{\rm initial}|)$. Each round scans only local tables and parent positions, with exact rational sums and equality tests. A direct implementation forms signatures with size polynomial in the total explicit local table size and maximum local arity. It never traverses the product hidden state space. The initial partition may encode mandatory distinctions; e.g. insisting on a conserved color as part of the interface can prevent the reduction.

### Randomized encodings and a necessary caution

For row-stochastic local encoders $E_i$ a candidate local stochastic identity is

$$
\sum_y T_i^a(y\mid x)E_i(y,b)
=\sum_{\bar x}\left(\prod_{j\in\mathrm{pa}(i)} E_j(x_j,\bar x_j)\right)
 \bar T_i^a(b\mid\bar x).
\tag{2}
$$

Local marginal identities alone are insufficient when multiple child factors share one randomized parent: the expectation of a product is not in general the product of the expectations. For example a fair encoded bit sent to two deterministic copying observation ports yields correlated output bits, whereas two independent fair microscopic ports are uncorrelated despite matching local marginals.

A conservative sufficient side condition is that every encoder with any nondeterministic row affects at most one outgoing quotient factor; all other outgoing quotient factors must be constant in that parent coordinate, uniformly in the other inputs, labels and destination states. Deterministically encoded parents require no such restriction. Given a fixed microscopic state, the independent encoder random variables entering distinct nonconstant quotient factors are then disjoint. The expectation factorizes, proving the global stochastic intertwiner $T^z E=E\bar T^z$ where $E$ is the product encoder. Iteration and $E\mathbf1=\mathbf1$ give exact observed-word transport. This asserts word-law transport and pushforward of stationary distributions, not that independently resampling an encoder at every microscopic time realizes the quotient's entire hidden path. The implementation verifies (2) and the side condition locally. It does not synthesize stochastic encoders or claim the side condition is necessary. The unrestricted contextual deterministic refinement is the principal construction.

## 2. Rectangular labelled supports

A quotient or direct nonnegative model is accepted for support-restricted comparison if, for every constituent and label, the child support

$$
S_i(a)=\{y_i:T_i^a(y_i\mid x)>0\}
$$

is nonempty and independent of the entire parent tuple $x$. Require the wildcard $T_i^*=\sum_a T_i^a$ to have full child support. A globally unused wildcard state can be removed by a separate exact restriction, but is rejected rather than implicitly removed in this implementation.

For a fixed collection of observation clamps, the hidden variables at each site/time have individual allowed domains $S_i(a)$ or the full domain for a wildcard. These form a product set; conditional on arbitrary legal boundary values, every factor touching the free variables is positive on this product. Thus there are hard zeros on the original state space, but no hard relation among distinct free variables after clamping. Nonrectangular parent-dependent supports are not covered. Such failure is an undecided certificate result, not evidence of non-Gibbs behavior.

Recompute WP14's pair cross-ratio envelopes using all parent values and only child values in the particular label's support, including the wildcard. When a coordinate has a singleton domain, the corresponding cross-ratio is one. These are rational maxima; no division by zero is used. The label-specific scope restricts the conditional density to the allowed domain. The ratio lemma of WP14 applies to pairs of positive distributions on that domain, with the same upper bound $\widehat\tau(R)$. For a common clamp pattern, every single-site or trajectory-block conditional is positive on its free allowed product set. Its heat-bath chain is irreducible there, and all telescoping intermediate contexts within the product domains are legal.

Consequently WP14's single-site tilted inequalities and its trajectory-column response theorem apply verbatim with the restricted cross-ratio envelopes. For a finite network, conditional disagreement after $n$ common observed slices obeys

$$
e_{n,i}\le K\frac{w_i}{\min_j w_j}\rho^n
$$

with $K=1$ in the site case and $K=(1-q)^{-1}$ in the trajectory-column case. Port-clamp-uniform likelihood, log-variation and quasi-Bernoulli margins follow by WP14's observable argument. Every label has strictly positive row likelihood despite its zero entries. The reduced unlabelled chain has positive transitions, and hence unique stationarity. All microscopic stationary output laws agree with this reduced law by (1), even when microscopic stationarity is not unique. WP07 gives positive Hölder reverse conditionals and an exponentially summable temporal interaction on the finite joint alphabet. There is no assertion that the unreduced microscopic hidden chain mixes.

## 3. Two-sided space-time comparison: single-site criterion

Let $\mathcal G$ be the graph on hidden space-time variables, connecting distinct variables occurring in a common local factor scope. Its degree is bounded when local parent and child incidence is bounded. Let $A$ be the sparse interior comparison rows from Section 2, summed without temporal tilt for the purposes of the norm. If a positive spatial weight vector satisfies

$$
\max_i\frac{\sum_{(h,j)} A_i(h,j)w_j}{w_i}=q_{\rm sp}<1 ,
\tag{3}
$$

then arbitrary fixed label/wildcard configurations have uniform two-sided posterior comparison. Here rows and weights are indexed locally and the time coordinate is implicit. On a countable graph require uniform upper/lower bounds on weights and a common strict margin.

**Finite-volume proof.** Fix a finite hidden region, and compare its two conditional distributions for possibly different exterior hidden values and clamp patterns. Mark as defects all exterior variables where boundary values can differ, and every variable in a factor scope whose label changes. Unchanged factors have common supports on their child domains; changing a different variable's allowed domain does not restrict the possible parent values of such a factor. At a free site not in the defect set, the local conditional laws can be compared by the same restricted cross-ratio telescoping, since every incident factor has the same label and its child value is within the same domain in both configurations. At defect sites use the trivial disagreement bound one. Couple finite heat-bath chains by maximal single-site updates as WP14. This gives $e_v\le\sum_u A_{vu}e_u$ at all nondefect free sites. Outside the free region use the fixed exterior coupling; unmarked exterior sites agree. A boundary site with no outgoing factor in a finite strip has a smaller comparison row, which is covered by the interior bound. Both marginal chains are irreducible on their possibly different product domains. Their coupled stationary law exists by finiteness.

If a free site is at graph distance at least $r$ from the defect set, unroll its comparison inequality for $r$ steps, using the zero disagreement at any agreeing exterior site. Every branch remaining free contracts the weighted supremum by $q_{\rm sp}$ per step. Thus

$$
e_v\le \frac{\sup w}{\inf w}\,q_{\rm sp}^{\,r}.
\tag{4}
$$

In particular the local posterior is insensitive to arbitrary exterior hidden configurations sufficiently far away, and to label changes whose factor scopes are sufficiently far away. These are two-sided space-time statements, not just forward temporal filter bounds. We report the space-time margin separately from WP14's temporally tilted margin; one does not follow automatically from the other.

## 4. Symmetric trajectory-column comparison for strong internal memory

The site criterion (3) may fail for strongly persistent constituents despite weak cross-component interactions. Use the WP14 trajectory-column perturbation types $(j,\ell,u,a)$, restricted to the allowed child domains. Here a changed exterior variable of component $j$ at time $t$ affects the factors on column $i$ in an interval $[t+\ell,t+u]$, with central total variation bound $a$ computed from local pair cross ratios. The own-chain rate $\kappa_i<1$ is the bound for its self-parent/child pair factor, after arbitrary future or past messages, on the appropriate allowed domains. Outside the affected interval a maximal conditional coupling propagates at rate at most $\kappa_i$ in either time direction. This statement remains true if some allowed domains are singletons; they can only make contraction easier.

Define spatial adjacency between distinct components sharing any factor scope. Use the product metric

$$
d((r,i),(t,j))=|r-t|+d_{\rm spatial}(i,j).
$$

For a candidate $r_0$ with $\max_i\kappa_i<r_0<1$, define the symmetric response

$$
W_{\rm sym}(\kappa,r_0,\ell,u)
=\sum_{h\in\mathbb Z}
 \kappa^{\mathrm{dist}(0,[h+\ell,h+u])}r_0^{-|h|}.
\tag{5}
$$

This differs from WP14's directional temporal tilt. Put $H=\max(|\ell|,|u|)$. The sum over $-H\le h\le H$ is finite, and the omitted left and right tails are exactly

$$
\frac{\kappa^{H+1-u}+\kappa^{H+1+\ell}}
 {r_0^{H+1}(1-\kappa/r_0)}.
$$

Use $0^0=1$ for a zero-distance central term. The formula follows from geometric summation, and is exact rational. Each exterior perturbation type of column $i$ contributes $a W_{\rm sym}/r_0$ to a sparse matrix $G^{\rm sym}_{ij}(r_0)$. The extra $1/r_0$ covers one spatial edge. A sufficient symmetric certificate is

$$
G^{\rm sym}(r_0)w\le q_{\rm sym}w,\qquad q_{\rm sym}<1,\quad w>0 .
\tag{6}
$$

### Proof with changing support domains

Consider a finite spatial cylinder with a finite consecutive time interval. Both measures have specified legal hidden boundary states and label/wildcard patterns. Include both temporal ends and spatial exterior in the defect set when their values may differ, and include every scope of a factor with a changed label. For equal boundary data those boundary defects may be omitted.

In a column heat-bath comparison condition on all other trajectories. Each free column is an inhomogeneous positive nearest-neighbor chain on its individual allowed domains. Compare its two conditional distributions by changing incident factors one at a time and gluing couplings via their common intermediate distributions. For a factor with unchanged label, telescope over the changed exterior variables exactly as WP14. For a factor with changed label, replace it and its fixed exterior arguments together, using central total variation bound one. Its changed internal support, if any, is only at the child of that incoming factor. All other factors remain positive for every value of that variable as parent. Thus the intermediate measures are well defined on products of the respective allowed domains. On each unchanged exterior segment of the column the two conditional chains have identical factors; coupling maximally on the affected interval and propagating outwards bounds disagreement at time $r$ by $\kappa_i^{\mathrm{dist}(r,I)}$ where $I$ is the affected internal interval. A factor affecting only fixed variables is irrelevant. If an own temporal boundary changes and its adjacent pair factor label is unchanged, couple through that chain from the boundary, giving a bound $\kappa_i^{|r-t_{\rm end}|}$; any changed adjacent label can instead be treated as a changed factor source. Temporal ends without outgoing factors have no corresponding source. The backward coupling for the terminal end uses the same pair cross-ratio bound.

Gluing the finite sequence of column couplings gives simultaneous disagreement bounds at each internal time, with sources from changed factors and own boundaries, plus the sum of exterior perturbations weighted by their disagreement probabilities. The stationary coupling of random-scan column heat-bath chains is legitimate on the two product domains, because each finite marginal chain is irreducible. For a target variable $v=(r,i)$ let $D(v)$ be its distance to the defect set in the product metric. For exterior input $u=(t,j)$ of a perturbation type, the triangle inequality gives $D(v)-D(u)\le 1+|t-r|$. Normalize disagreements by $w_i r_0^{D(v)}/\inf w$. Therefore every exterior response sum contributes at most its row of (6) times the maximum normalized disagreement, even when the exterior site is on the fixed boundary. Zero disagreement boundary sites may be omitted.

At most $1+|\mathrm{children}(i)|$ factors contain each internal time variable. For a changed-factor interval $I$ contained in the defect set, $\kappa_i^{\mathrm{dist}(r,I)}\le\sum_{t\in I}\kappa_i^{|r-t|}$, and $D(v)\le |r-t|$ for those $t$. Hence the normalized sum of changed-factor sources is at most

$$
(1+|\mathrm{children}(i)|)\left(1+\frac{2\kappa_i}{r_0-\kappa_i}\right).
$$

The two own temporal boundary sources contribute at most two. Marking all exterior sites ensures finite defect distance in each finite cylinder; agreeing boundary sites can be omitted for a stronger estimate if each relevant component still has a defect, while a defect-free component has zero disagreement by equality of its conditional measures. Put

$$
M=\sup_i\left[(1+|\mathrm{children}(i)|)\left(1+\frac{2\kappa_i}{r_0-\kappa_i}\right)+2\right].
$$

The maximum normalized disagreement is at most $M+q_{\rm sym}$ times the same maximum in the sense $E\le M+q_{\rm sym}E$ if it exceeds the fixed boundary bound one. Since $M\ge1$, the same upper bound $M/(1-q_{\rm sym})$ also holds otherwise. Thus

$$
e_v\le \frac{\sup w}{\inf w}
       \frac{M}{1-q_{\rm sym}}r_0^{D(v)} .
\tag{7}
$$

All estimates are uniform in cylinder size, temporal length and the entire observation pattern, including hard observation domain changes. The prefactor can be large; it is part of the witness and cannot be discarded. This proof does not assert that the time-column comparison dynamics is a physical update rule. It is a finite-volume coupling argument.

The code checks (3) first with the temporal certificate's weights. For a column witness when this fails, it tries a bounded list of symmetric rates with those weights, and separately replays the resulting symmetric local inequalities. This is a sufficient search, not a claim of complete gain discovery.

## 5. Countable spatial limit and two-sided observed quasilocal specification

Assume a countable locally finite spatial graph of finite-state/finite-label constituents, bounded parent/child incidence and uniform strictly positive lower bounds on the nonzero reduced local entries, and either the site condition (3) or the symmetric column condition (6) with uniform weights, rates and finite prefactor. The local quotient identity (1), if used, is required everywhere. These assumptions are hypotheses on the infinite family, not extrapolation from a finite simulation. For a finite-type translation-invariant template on a locally finite lattice, they can be verified by the local incidences for the template and constant or periodic weights. In particular the homogeneous nearest-neighbor examples below use exactly the same row types on the infinite line as on the tested rings of length at least three.

### Hidden specification under arbitrary observation clamps

For each complete label/wildcard pattern, the allowed domains are a product of finite nonempty sets. The local Gibbs specification is obtained by multiplying the corresponding labelled/wildcard factors touching a finite region and normalizing on the free domains, with legal exterior values fixed. Normalizations are positive. Finite-set kernels are consistent by summation, and local (depend only on finitely many exterior states). Existence of an infinite-volume probability measure follows by taking weak subsequential limits of the finite-volume distributions with legal boundary states along increasing cylinders exhausting space-time; compactness is the product compactness of finite discrete state spaces. Every fixed finite-set Gibbs identity passes to the limit by locality. For uniqueness, compare two candidate measures by conditioning on a common large cylinder's exterior, couple each pair of boundary configurations using (4) or (7), then integrate these boundary couplings. For any finite set of variables, the union bound on disagreement tends to zero as its distance from the exterior grows. Thus the two measures agree on all cylinders. The same argument shows convergence without selecting subsequences, and uniform insensitivity to observation-pattern changes outside large neighborhoods of a fixed finite set. No hidden conditional phase transition is possible in this certified regime.

### Identification with the stationary observed dynamics

The unlabelled update is a Feller Markov kernel on the compact countable product hidden space: each finite-coordinate cylinder test depends only on its finitely many parents. A stationary law exists by Cesaro compactness. Its two-sided stationary path distribution is Gibbs for the wildcard specification. To verify this, condition a hidden variable on the preceding slice and on all other states of its current slice. Its initial conditional weight is its incoming transition factor. Conditioning also on the next slice changes this weight by the product of the finitely many outgoing child factors depending on this variable; all other transition factors cancel, by conditional independence. The remaining earlier/later times cancel by the Markov property. All factors involved are positive, and the single-site conditional is therefore precisely the local Gibbs kernel. In a finite set, positive one-site kernels determine the normalized product Gibbs kernel, by connecting any two configurations through single-coordinate changes and comparing their probability ratios. This proves all finite-set identities. The all-wildcard uniqueness result hence gives a unique stationary reduced hidden law. For finite label clamps, sample each label conditionally independently given the hidden transition with probability $T_i^a/Q_i$. The posterior hidden distribution is a finite reweighting of the wildcard measure by those factors, restricting the individual child domains. Thus it satisfies the clamped specification and equals its unique Gibbs measure. For arbitrary initial finite observations this uses only positive cylinder probabilities, as checked below. If the microscopic model is reducible, it still has a stationary law by the same Feller/compactness argument; all stationary microscopic observed laws are identical to the quotient's observed law by (1). The microscopic hidden laws themselves need not be unique.

### Uniform insertion nonnullness and quasilocality

Fix a target output port at site/time $v=(t,i)$. Set this port to wildcard while clamping any other finite collection of labels. Under the corresponding hidden posterior the conditional probability of target label $a$ is the expectation of

$$
f_a(x,y)=T_i^a(y\mid x)/Q_i(y\mid x)
$$

on its local parent/child scope. The wildcard $Q_i$ is positive everywhere. To obtain a lower bound, condition on all hidden variables except the target child. Its conditional hidden density is proportional to the incoming wildcard row times the product of outgoing child factors, evaluated at their legal child values. These factors are positive for every possible target child value by the support hypothesis. Let $m_j$ be the minimum nonzero entry of local factor $j$ over labels and wildcard and $c_i$ the minimum labelled row likelihood. The outgoing product lies between $\prod_{j\in\mathrm{children}(i)}m_j$ and one. Comparing the insertion numerator with the wildcard denominator gives the uniform lower bound

$$
\Pr(Z_v=a\mid \text{other finite clamps})
\ge c_i\prod_{j\in\mathrm{children}(i)}m_j>0 .
\tag{8}
$$

This also proves positivity of all finite observed cylinder assignments, by the chain rule (or from positive labelled row likelihoods along a finite temporal ordering).

For two clamp patterns, the local function $f_a$ has range in $[0,1]$. A coupling bound for its expectation difference is the sum of the hidden disagreement bounds over its finite scope, using (4) or (7). In particular the insertion probability is uniformly continuous in the exterior label configuration, with an exponential bound in the relevant space-time distance to the changed factor scopes. The same holds for log probabilities by dividing by (8). Take expanding finite exterior clamps with the target wildcard; uniqueness and uniform comparison show convergence to a limit for every exterior pattern, independent of the exhaustion. Conditional martingale convergence identifies this limit as a version of the one-site conditional of the stationary observed field. For a finite target set, use the chain rule of single-site insertion probabilities with successive target labels clamped and the rest wildcard; the same uniform limit of finite conditional distributions exists, is strictly positive and quasilocal, and gives consistent finite-set specification kernels. Consistency follows by taking uniform limits of the finite conditional probability identities and using their positive denominators. The observed law is therefore compatible with a nonnull quasilocal space-time specification, not just a temporal conditional bound. The theorem does not establish uniqueness of all observed Gibbs measures for that specification, an explicit absolutely summable interaction on arbitrary graphs, or a characterization of conditional phase transitions outside this regime.

The proof is conditional on uniform local margins on the infinite incidence graph. There is no algorithm here for arbitrary countably presented graphs, and the finite verifier does not claim to have simulated an infinite system.

## 6. Exact evidence

The test family has a binary physical state $b$ and an invisible microscopic color $c$ preserved exactly at each site. Its next binary probability is

$$
p_i(1\mid x)=\tfrac12+A(2b_i-1)+B(2b_{i-1}-1)
$$

with $B>0$. The next color equals the old color. This is a genuinely interacting transition law, not a shared observation-only channel. The color has no effect on any local port or physical transition. Observations report the new binary state exactly with probability $1/2$ and emit an erasure label otherwise. The three local labels have supports $\{0\},\{1\},\{0,1\}$ after quotienting. The original color-preserving tables have parent-dependent support. They fail the direct rectangular support test, but exact contextual refinement discovers the partition $(0,0,1,1)$ for two colors in one proper round. The reduced two-state tables still have structural zeros; the strict WP14 verifier rejects them. No positive approximation was substituted. The construction demonstrates a hidden nonmixing microscopic realization with regular interacting observations; it does not claim that the observed law lacks an alternative positive realization.

| Model | Temporal certificate / rate | Temporal gain | Two-sided space-time rate | Spatial gain | Prefactor |
| --- | --- | ---: | --- | ---: | ---: |
| Moderate ring, A=1/8, B=1/32 | site, 13/32 | 0.945015 | site, about 0.669224 | 0.669224 | 1 |
| Strong ring, A=7/16, B=1/4096 | column, 29/32 | 0.266514 | symmetric column, 29/32 | 0.511026 | 353.824 |
| Near-persistent ring, A=15/32, B=1/16384 | column, 31/32 | 0.162602 | symmetric column, 31/32 | 0.250438 | 246.815 |

Rounded decimals display exact rational bounds. The moderate and strong certificates replay at 128 constituents, with four microscopic states each and two quotient states each, using one distinct local factor envelope. No joint hidden state or joint output alphabet is constructed by the verifier. Their identical local coefficients and constant weights also certify the infinite-line templates under Section 5, with no empirical extrapolation. The moderate case has per-port forward nonnullness 11/64, log-variation constant 10/11, and two-sided insertion nonnullness 1331/262144. The strong case has insertion lower bound 16581375/549755813888; its space-time prefactor is conservative and the rate cannot be interpreted independently of it.

Eight exact tests cover the deterministic tensor intertwiner on every microscopic row of a small coupled example, cylinder equality for a correlated prior, coarsest refinement propagation through two downstream levels, stochastic shared-parent obstruction and an accepted nonshared case, all shared suffixes through length two with every initial state and partial current clamps, hard support and nonrectangular controls, exact two-sided smoothing when a remote observed domain changes, insertion lower bounds, symmetric geometric sum against partial sums, the strong-memory 128-site replay, and a nonvacuous long-strip comparison at separation 79 using a 90-slice exact small-network oracle. Joint materialization is test-only. Exact candidate 43549d3e68f0371c9508bb7fa15fae01dc4795ed passed 8/8 tests, capture 2fdb0196f3794d70aff87905b94f8137. Numerical readouts: capture 23d85ab201cc45b78e9519f5d9e07a10 for quotient and temporal margins, capture 2e8fb66953e04ae3987e4dbab095aa90 for symmetric spatial margins. All local independent attestation flags false. Final source/code/test head replay required.

## 7. Prior art and scope

Contextual partition refinement uses established strong lumpability and stochastic bisimulation principles; see Dean and Givan, Model Minimization in Markov Decision Processes (AAAI 1997), and the exact partition-refinement literature. The sparse local identity (1), the correlation guard for stochastic encoders, and transport of the specific support-aware thermodynamic witnesses are the scoped construction here. No claim of inventing bisimulation or of unrestricted stochastic quotient minimality.

Dobrushin comparison and block comparison are established tools; Rebeschini and van Handel, [Comparison Theorems for Gibbs Measures](https://arxiv.org/abs/1308.4117), explicitly develops block comparison and high-dimensional filtering. Kuelske and Opoku, [The Posterior Metric and the Goodness of Gibbsianness for Transforms of Gibbs Measures](https://arxiv.org/abs/0711.3764), develops continuity under constrained posterior comparison. The space-time Gibbs formulation of probabilistic cellular automata is classical, including Lebowitz, Maes and Speer, Statistical mechanics of probabilistic cellular automata (1990). Primary/authoritative abstract and bibliographic sources inspected; full theorem-level source concordance and originality adjudication remain open. The contribution sought is the exact local quotient-plus-support calculus, symmetric rational response witness, and uniform observed insertion and limit estimates as one compositional certificate, not a claim to invent the PCA/Gibbs correspondence or general Gibbs preservation theory.

**Disposition:** internally established exact contextual deterministic quotient and conservative stochastic interface replay; support-restricted local small gain for nonnegative reduced models with rectangular labelled supports; symmetric two-sided space-time comparison including strong memory; countable locally finite spatial limit and nonnull quasilocal observed specification under uniform margins. All conditional on explicit compatibility and local inequalities. No independent mathematical certification, general parent-dependent hard-constraint classification or arbitrary infinite-volume phase diagram.

**Next boundary:** CSM-G2_NONRECTANGULAR_SUPPORT_AND_CONDITIONAL_PHASE_OBSTRUCTION_OPEN. Seek support-aware temporal block/automaton or constrained block heat-bath compatibility for genuine parent-dependent hard supports surviving contextual quotient, and establish a precise conditional phase-transition obstruction or distinguish genuinely non-Gibbs observations from certificate failure. Keep #3136 open.
