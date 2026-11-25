# CSM-G2-WP16 — constrained block comparison and a visible conditional phase obstruction

**Status:** internally proved candidate sufficient theorems, explicit obstruction and exact rational reference implementation. Originality UNADJUDICATED; no independent mathematical certification or MATHCERT. Continues WP15, protected merge 17291203a93a43a1ae31fcb8f7b6f69922bccac0. Working protected base c8515b1cb206722d3f77a9c8c8a88ac4efea89af.

## 1. Model and safe-reset certificate

Use WP15's finite nonnegative labelled local dynamics, with normalized tables $T_i^a(y_i\mid x_{\mathrm{pa}(i)})$ and wildcard $Q_i=\sum_a T_i^a$. All entries are at most one. A label may now impose a genuine relation among parent and child coordinates or among several parents. Apply the exact contextual quotient first if desired; all subsequent certificates refer to the actual reduced tables, and WP15 transports their observed laws. Do not assume that every support becomes rectangular by quotienting.

Partition spatial sites into disjoint finite blocks, repeated at each time. A space-time block is one such block at one time. Each local factor has a finite scope of space-time blocks; in a block it may depend on only some coordinates. Denote the block state sets by $X_B$. Fix one safe configuration $s_B\in X_B$ per block. Require the following two finite checks for every factor and every label including wildcard:

* The factor is strictly positive when every coordinate in its scope is safe.
* Replacing the coordinates of any one incident block by their safe values preserves positivity whenever the original factor value is positive.

This is a block reset condition, not strict positivity, and not a claim that every possible boundary permits a legal interior. A hard exclusion factor can satisfy it even across blocks. A hard equality factor fails it across singleton blocks, but may satisfy it when both equal variables belong to one block. The proof uses the specific allowed reset, not an unjustified irreducibility assumption for single-site dynamics.

For fixed observations or wildcards and a finite region consisting of whole blocks, take legal exterior values from a globally feasible configuration. All-safe in the free region is feasible: start from the global configuration and reset the finitely many free blocks in any order, preserving every factor's positivity. The conditional Gibbs law is the normalized product of factors touching the free region. It has nonempty support. Every feasible configuration can reach the all-safe interior by block resets, and the reverse path from that safe interior to another feasible configuration is also legal. Therefore random-scan heat-bath updates of whole blocks are irreducible on the feasible finite state set. This argument remains valid for two different clamp patterns with different feasible sets.

## 2. Two ways to compute local influence bounds

### General exact blanket method

For one block and fixed outside assignments, a local factor touching the block gives a nonnegative section as a function of the block state. Some outside assignments may be incompatible, even if considered only as intermediate steps in a telescoping comparison. If the section is not identically zero, it is positive at the safe block state by the reset hypothesis. If identically zero, replace that section by its section with all its exterior arguments safe. This is an auxiliary extension only, not a modification of the physical model. It is positive at the safe state. Thus the product of extended incident sections can be normalized for *every* assignment of exterior block variables.

On a feasible exterior context, each incident section is nonzero and the extended conditional equals the actual heat-bath kernel. Compute, for each block $B$ and each distinct adjacent block $D$, the maximum total variation distance of the two extended conditionals for assignments differing only at $D$. The maximum is over all finite exterior assignments and incident label patterns including wildcards. Denote the result by $C_{BD}$. The extension makes arbitrary intermediate contexts available for telescoping, without requiring them to be physically feasible. By the triangle inequality the total variation between two actual kernels at feasible contexts is at most the sum of the coefficients for differing adjacent blocks. This also applies to pairs of different global clamp patterns when no label changes in any incident factor of the target block.

All comparisons are exact rational. Enumerate the local blanket, never the joint hidden state or observation alphabet. The work budget is the product of the number of boundary block configurations, incident label possibilities and internal block states, summed over distinct checked local types; pairwise TV evaluations add a factor bounded by the sum of neighbor block cardinalities. The implementation caches identical exact local types during replay. Budget exhaustion is undecided. It explicitly checks the terminal row type for finite time strips where outgoing factors are absent; the exact coefficients of a smaller blanket need not be bounded by the full-blanket coefficients.

### Faster block-rectangular support path

A factor support may be a product across incident block coordinates even though it is not a product across individual microscopic coordinates. For each labelled factor verify this by projection cardinalities: a finite nonempty relation $R$ always lies in the product of its block projections, so equality of cardinalities is equivalent to equality of sets. The projections may restrict arbitrary coordinates jointly inside a block. Each contains the safe projection. For a fixed clamp pattern the feasible hidden state set is now a product of block domains, each the intersection of incident support conditions, and each contains its safe state. All factors are positive on this product of restricted domains.

For each factor and distinct pair of block positions compute the maximum pair cross ratio on its product support as in WP15, using the grouped coordinates as one finite coordinate. All other positions range over their support projections. To bound the effect of one exterior block on a target block, multiply the pair cross-ratio maxima of all shared factors and apply WP14's rational upper bound on the likelihood-ratio total variation formula. This bounds the change of the target normalized conditional on its common allowed domain; the same proof applies when clamp patterns differ away from the target's incident factors. In the latter case the exterior assignments of both configurations satisfy the same unchanged incident support projections, so all intermediate single-block substitutions remain in these projections. This method does not use the zero-section extension or claim its cross-ratios bound that extension on illegal contexts. The exact blanket method covers the more general cross-block hard constraints.

### Discovering the finest spatial grouping for the fast path

For a nonempty finite relation on a factor scope, recursively test bipartitions of its coordinates for product support by the projection-cardinality criterion. Stop when no nontrivial bipartition works. The resulting indecomposable components are unique as a partition: if a relation is a product over two partitions, projection of either factorization onto each block of the other shows it is a product over their common refinement. Thus any successful split is compatible with the finest decomposition, and recursive splitting until indecomposable yields it. Merge spatial sites occurring in each indecomposable component of each label support, including wildcard, and take the transitive closure. A component spanning different times cannot be grouped by a partition that is spatial and repeated separately at every time; report cross-time support. Otherwise the merged partition is the finest spatial partition allowing block-rectangular supports, since any compatible partition must keep each indecomposable component together. This is not optimal selection among all block small-gain witnesses. In particular a crossing constraint may have an exact-blanket certificate even when no spatial block partition achieves rectangularity. Discovery has explicit split-test and block-state budgets, exponential only in local scope arity for the bipartition search, and the verified grouping still needs a safe configuration and strict gain. The default safe configuration is all zero; no general safe-state search is claimed.

## 3. Block comparison theorem

On the block graph, join distinct space-time blocks appearing in a common factor. The coefficient rows are sparse and indexed by relative time and spatial block. Let $w_B>0$ depend only on the spatial block. Suppose that, for every interior and terminal row type,

$$
\sum_D C_{BD}w_D\le q w_B,\qquad q<1.
\tag{1}
$$

The graph and coefficients are recomputed from the supplied tables. The terminal type is required if using one-sided finite strips; finite cylinders with a fixed exterior use the complete row.

Compare two finite-region Gibbs measures, possibly with distinct exterior states and clamp patterns. Mark as defects the disagreeing exterior blocks and all blocks in the scope of any changed factor. At a free nondefect block the two actual conditional kernels have TV distance at most the sum of coefficients for differing outside blocks, by Section 2. Couple random-scan block heat-bath chains by maximal coupling at the common update block. The two marginal finite chains are irreducible by safe resets. At a stationary coupling (existence by finiteness), the probability $e_B$ of a block disagreement satisfies $e_B\le\sum_D C_{BD}e_D$ at every nondefect free block. At defects use $e_B\le1$; agreeing exterior blocks have zero disagreement. Iterating the inequality for the graph distance $r$ from a free block to the nearest defect gives

$$
e_B\le (\sup w/\inf w)q^r .
\tag{2}
$$

The proof unrolls only through nondefect sites; the weighted supremum contracts by at most $q$ each step. No block-state tensor is formed for verification. In defect-free components both finite laws coincide.

Optionally check the directional temporal tilt, with rational $0<\rho<1$:

$$
\sum_{(h,D)} C_B(h,D)w_D\rho^h<w_B .
\tag{3}
$$

Require both interior and terminal rows. For a common clamp pattern in a finite time strip and two feasible initial hidden boundaries, the weighted maximum argument of WP14 gives $e_{t,B}\le (w_B/\inf w)\rho^t$. If initial priors differ, condition on the initial boundaries and mix the couplings of feasible boundary pairs with their posterior weights. Bound (2) also gives a temporal rate because each factor spans at most one time step. The verifier uses the smaller available temporal rate. It does not claim completeness of gain or weight discovery.

## 4. Positive insertion and observed continuity

For every factor $f$ let $m_f>0$ be its minimum nonzero entry over all labels including wildcard. Fix one target output port and leave that factor wildcard. Let $U$ be the union of all whole space-time blocks touching its factor scope, and $I(U)$ the finite set of factors touching $U$. Given exterior hidden variables from a feasible configuration, resetting all blocks in $U$ gives a feasible all-safe interior. Its conditional probability is at least

$$
\frac{\prod_{f\in I(U)}m_f}{\prod_{B\subset U}|X_B|}.
$$

Indeed its unnormalized weight is at least the numerator and each other weight is at most one. On the safe configuration the insertion function $f_a=T_i^a/Q_i$ of the target label is at least $m_i$; set it to zero where the wildcard is zero, which never occurs on the feasible posterior. Hence every target label has the uniform lower insertion bound

$$
c_i=m_i\frac{\prod_{f\in I(U)}m_f}{\prod_{B\subset U}|X_B|}>0 .
\tag{4}
$$

This proves the bound for two-sided finite cylinders containing the whole target scope of blocks. It does not assert non-nullness after an arbitrary fixed microscopic boundary when the target's parent block is itself fixed at an inadmissible value.

The target insertion function lies in $[0,1]$. A coupling bounds its expectation difference by the sum of disagreement probabilities of the blocks in its scope. Applying (2) and dividing by (4) gives a log and absolute relative probability discrepancy bound with prefactor

$$
C_i^{\rm sp}=(\sup w/\inf w)\,|\mathrm{scope}_{\rm blocks}(i)|/c_i
$$

times $q^r$, where all scope blocks have distance at least $r$ from the defect set. The constants are conservative. For a shared observed suffix of length $n\ge1$ and any common partial current output clamp, extend the strip to the next slice with the target wildcard. The target parent and child blocks lie at times at least $n$ and are free. Compare feasible initial boundary components by the preceding coupling. The relative/log difference is bounded by $C_i^{\rm sp}q^n$ or by $C_i\rho^n$ using (3), where $C_i=\sum_{(h,B)\in\mathrm{scope}}w_B/(\inf w\,c_i)$ in the latter case. For stationary histories of length zero use the stationary insertion bound, established below; no arbitrary boundary non-nullness claim is needed. Chain through the output ports for joint symbols. Thus on a finite spatial network the stationary output has full-symbol non-nullness at least $\prod_i c_i$ and log-variation constant $\sum_i C_i$ for the selected rate. WP07's reversal/interval theorem gives a positive Hölder temporal law and exponentially summable temporal Gibbs interaction. The implementation reports both spatial and temporal port constants and an explicit positive-wildcard gate for the stationary observable conclusion.

### Countable spatial limit

For a countable locally finite graph with uniformly bounded block sizes, factor incidence, positive nonzero entry lower bounds, weight ratio and strict gain, (2) is uniform in region size. The all-safe configuration is feasible for every clamp pattern. The feasible set is closed in the compact product of finite spaces. Take finite-volume Gibbs measures on increasing unions of blocks with safe exterior; locality and positivity of the finite normalization on feasible exterior contexts imply the Gibbs identities pass to weak subsequential limits. Existence follows. For two candidate infinite-volume measures, compare conditional finite-region laws given their exteriors by (2), then integrate. The union bound for any fixed finite collection of blocks tends to zero as its distance from the boundary grows. This gives uniqueness, convergence of every legal-boundary exhaustion, and exponential continuity in distant observation patterns. Finite-region kernels on unions of blocks suffice for uniqueness; their disintegration also gives the corresponding finite-coordinate kernels on legal boundary contexts. This proves constrained hidden-specification uniqueness without strict microscopic positivity.

For the identification with a stationary observed dynamical law, in this packet additionally require the unlabelled wildcard transitions to be strictly positive on all local rows. This is checked separately; we do not infer it from the reset property. By the WP15 stationary path argument, the Feller unlabelled dynamics admits a stationary law whose two-sided hidden path is Gibbs for the wildcard specification (positive finite local kernels permit the finite-set identities). Uniqueness of that specification gives uniqueness of the reduced stationary hidden path. Finite label clamps give a finite reweighting by $T_i^a/Q_i$, whose conditional specification is the corresponding constrained one. The positive wildcard gives positive probabilities for finite hidden assignments in finite space-time scopes; in particular all-safe assignments prove positive observed cylinders. Alternatively insertion follows by (4) in finite cylinders and passage to the limit. Therefore (4) and the continuity bounds hold uniformly for conditional insertion given arbitrary finite observation clamps, including time-future labels.

As finite exterior clamps exhaust the complement of a finite target set, the comparison bounds imply uniform convergence of insertion probabilities, then of finite-target kernels by the chain rule. Martingale convergence identifies these kernels with observed conditional probabilities, and positive denominators and uniform limits preserve consistency. The resulting observed space-time law has a non-null quasilocal specification. This is not a claim of uniqueness of all Gibbs measures of that observed specification or a summable interaction on arbitrary graphs. Without positive wildcard, only the constrained hidden comparison theorem is claimed here; dynamical identification is left open.

## 5. Explicit obstruction with full support and uniform non-nullness

Failure of a gain inequality, a safe reset or a partition budget is not a non-Gibbs verdict. We give a separate exact obstruction in the same local labelled-network language. It has an independent fair binary hidden refresh at every spatial site and time. At each time the label on edge $(i,i+1)$ depends on the two previous hidden bits $x,y$, with four labels $E,+,-,D$:

$$
H_E(x,y)=\tfrac12\mathbf1_{x=y},\qquad
H_+(x,y)=\frac{1+x+y}{16},\qquad
H_-(x,y)=\frac{3-x-y}{16},\qquad
H_D=1-H_E-H_+-H_- .
$$

The physical child bit is independently fair, i.e. $T_i^a(b\mid x,y)=H_a(x,y)/2$. The wildcard is strictly positive. There is no unobserved phase transition and time slices of the observed field are independent. The observed labels at one time nevertheless have a genuine spatial conditional phase obstruction. This is not a claim that the underlying hidden dynamics themselves are interacting in this negative control; the two positive examples below have genuine interacting transitions. A product with an independent genuinely interacting network preserves the obstruction under fully revealed output ports.

The label $E$ imposes equality of its two hidden bits. All other label likelihoods are strictly positive, between $1/16$ and $3/4$. Every finite observed assignment has positive probability (take all hidden bits zero). Moreover the observed law is uniformly non-null even under arbitrary finite exterior clamps at one time. Delete the target edge from the line. Each connected component of the clamped equality edges has one free fair phase before the non-E weights. Conditional on the other components, the likelihood ratio of its two phases is at most $12^2$: only the at most two boundary edges with non-E or wildcard factors can distinguish the phase, and each non-E ratio is at most twelve. All components are finite for finite clamps; unconditioned hidden singletons are components too. Each phase thus has conditional probability at least $c=1/(1+12^2)$. The two target endpoints lie in distinct components, so the probability both are one is at least $c^2$ by conditioning successively. Target label $E$ has conditional probability at least $c^2/2$. The other target labels have direct lower bounds at least $1/16$. Other times are independent. Consequently this obstruction is about discontinuity, not merely forbidden words or a lack of finite energy.

Set the target edge to wildcard. Clamp $n$ adjacent edges on both sides to $E$, and the next outer edge on each side to $+$ or, for the alternative cylinder, both to $-$. Each equality chain forces its hidden component to be constant. The fair prior and the constant equality factors give equal base weights to the two phases. Integrating the free outer bit in a plus factor weights the constant one phase by $5/32$ and the zero phase by $3/32$, so each target endpoint has probability $5/8$ of being one; the minus cylinder gives $3/8$. The two components are independent because the target is wildcard. For every $n\ge1$, exact target conditional distributions in order $E,+,-,D$ are

$$
\left(\frac{17}{64},\frac9{64},\frac7{64},\frac{31}{64}\right),
\qquad
\left(\frac{17}{64},\frac7{64},\frac9{64},\frac{31}{64}\right).
$$

The plus observable separates the two selections by $1/32$, independent of $n$. The exterior cylinders have strictly positive probability and approach the all-$E$ exterior pattern; if necessary add the common all-$E$ clamps on increasing windows at other times, which do not affect these probabilities. Any continuous version of the target conditional at the all-$E$ pattern would force both conditional averages to converge to the same value by continuity on shrinking cylinder neighborhoods. They do not. Thus the point is an essential discontinuity and no quasilocal specification of the observed field exists.

The all-$E$ constrained hidden field has two pure constant phases in that spatial slice. The soft pins make those phases observable without forcing the exterior observed process to lose full support. For every finite spatial block partition of the infinite line some equality edge crosses blocks; any all-safe configuration satisfying every equality has a common bit, and resetting one endpoint block in the opposite constant configuration breaks equality. Hence no such finite-block reset certificate exists for this model. The fast support decomposition on a finite periodic ring instead merges the entire ring into one block; its state count is exponential and no uniformly bounded spatial grouping exists. This is a precise obstruction to the certificate language, accompanied by the independent essential-discontinuity proof. Do not generalize failure of the language to a phase-transition theorem for other systems.

## 6. Exact evidence and complexity

Two positive examples preserve hard nonrectangular constraints after quotienting.

* Paired ring: two binary sites per pair, first child with parent pair plus previous pair's first bit, second child a fair refresh. First child's physical next-one probability is $1/2+\epsilon(2x-1)+\epsilon(2v-1)$ with $\epsilon=1/128$, where $x$ is its own bit and $v$ the preceding pair's first bit. Its observed label one has probability $1/2$ if its two own-pair parent bits agree, zero otherwise; label zero is the complement. The label and child update are independent given parents. Hence the physical transitions genuinely interact across pairs. The contextual quotient retains both binary states of every site. Singleton safe-reset fails, but the finest spatial support grouping automatically finds the pairs. Exact block-rectangular comparison gives gain about 0.063447, unchanged at 64 pairs (128 sites). No global tensor is built.
* Crossing exclusion ring: a child's next-one probability is $1/32+x_{\rm previous}/256$. Label one has probability zero if the child and either parent are occupied, $1/2$ otherwise; label zero is the complement. The hard support spans time, so no repeated spatial grouping makes it rectangular. Singleton safe reset works and exact extended-blanket comparison passes with gain about 0.788781 on both 3 and 8 sites, using 10416 local state-context-label evaluations after local-type caching. The safe insertion bound is only $1/2251799813685248$, sufficient but extremely conservative. This example is not a general exclusion-process or conserved-particle-number theorem.

| Model | Local states per block | Verification | Spatial gain (rounded) |
| --- | ---: | --- | ---: |
| 64-pair interacting equality ring | 4 | rectangular block support | 0.063447 |
| crossing exclusion ring | 2 | exact extended local blanket | 0.788782 |
| equality/soft-pin phase obstruction | unbounded grouping required on line | exact discontinuity | not a gain claim |

The template rows of the positive homogeneous examples on the infinite line equal the local row types on rings of at least three pairs/sites. Thus the countable theorem applies with uniform margins to those templates; no infinite simulation is claimed. The optional temporal tilt may yield a sharper rate than the spatial bound, but all reported rates include their prefactors. Factor support decomposition examines at most exponentially many cuts in each local arity; the exact blanket path may be exponential in local blanket size. Given a positive weight witness, checking sparse gain is linear in the coefficient count after those local calculations. The verifier has explicit state-count, context and split budgets; no arbitrary-network polynomial-time discovery theorem is claimed.

Code: constrained_block_comparison.py. Six exact tests cover all 255 nonempty binary three-coordinate support relations, local quotient retention and automatic grouping at 128 sites, exact crossing-constraint coefficients and type caching, invalid reset and impossible exterior extension controls, malformed gain/budget rejection, exact two-sided smoothing and insertion in small tensor oracles, full-support phase-gap and finite-clamp non-nullness controls. Initial code/test candidate 13f9b379bb89d80b5083187d1ff24192dfff9a7b passed 6/6 tests (capture 4c817488e5fa4d9e927f8a004c5c9ee0). Parameter capture e4a89f4cae354951aa689ce75f30aca5. Final observable-bound strengthened head needs fresh exact source/code/test replay. Independent execution attestation flags false.

## 7. Prior art and next boundary

The comparison argument belongs to classical Dobrushin and block comparison theory, including Rebeschini and van Handel, [Comparison Theorems for Gibbs Measures](https://arxiv.org/abs/1308.4117). Strong spatial mixing for hard-core measures is an established subject. Conditional phase selection and bad observed configurations are classical mechanisms in van Enter, Fernández and Sokal, [Regularity Properties and Pathologies of Position-Space Renormalization-Group Transformations](https://arxiv.org/abs/hep-lat/9210032), and related works. WP03's deterministic XOR obstruction and Kari–Taati's work on [Statistical Mechanics of Surjective Cellular Automata](https://arxiv.org/abs/1311.2319) already illustrate support-related pathologies. The exact equality/soft-pin construction here explicitly distinguishes full support and finite energy from quasilocality, but originality is UNADJUDICATED. Abstract-level source review only for the additional cited literature; full theorem-level concordance is open. No claim of inventing safe symbols, block coupling, strong spatial mixing or conditional phase obstructions.

**Disposition:** internally established safe-reset comparison for true parent-dependent hard constraints, exact auxiliary kernel extension, finite support-factorization grouping, uniform non-null observed quasilocality under explicit positive-wildcard and local margins, and a separately proved full-support finite-energy essential-discontinuity obstruction. No general classification of hard constraints, conserved sectors, or efficient discovery for arbitrary succinct networks.

**Next boundary:** CSM-G2_CONSERVATION_SECTORS_AND_CONSTRAINED_BLOCK_COUPLING_OPEN. Replace the common safe-reset hypothesis with locally certified communicating-sector or multi-block coupling conditions for constraints that cannot be repaired by resetting individual blocks. Distinguish physical conservation sectors from observation-visible persistent conditional phases; seek exact support automata and quantitative finite-size/phase-selection bounds. Keep canonical issue #3136 open.
