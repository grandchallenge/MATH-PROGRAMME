# EXT-015 REACH / UC-OP-005 — nonauthor critical review of heat-graph partition incidence

**Disposition: BOUNDED INTERNAL MATHEMATICAL ACCEPT of frozen UC004; zero post-freeze mathematical corrections requested.** This review accepts the finite component/block rank theorem, the all-partitions equivalences, the actual smooth-block nonsmoothing witness and its positive converse, and the stated ambient conic estimates. Its author is a distinct nonauthor logical context: the primary author and parent supplied the proof mechanism and do not serve as this critic. The contexts share a system, account and dependencies. This is not external independent certification, MATHCERT, protected admission or programme completion.

## 1. Exact reviewed material and evidence boundary

The assigned frozen source is [HEAT_GRAPH_PARTITION_INCIDENCE_UC004.md](HEAT_GRAPH_PARTITION_INCIDENCE_UC004.md), supplied commit d22c6a45a835880c90ce6a31a0e8896362fdb44b and remote ref research/reach-heat-incidence-uc004-primary-frozen-20261116. The commit/ref identity is supplied custody metadata; this critic performed no Git or GitHub operation. Direct hashing of the read local source bytes verified Git blob e3b4a794b022abbf5cd3b4b6c32c48ced94e82d8 and SHA256 96cc77ce3abe0da9df39581eff8d683175ea31de878c7078d2c3550e57b7e7b4. Git blob identities here were computed with the standard blob header and SHA1; all inspected files already had LF line endings.

The producer fixture [heat_graph_partition_incidence_uc004.py](../../../fixtures/algebraic/heat_graph_partition_incidence_uc004.py) has verified Git blob af837ab9dfaaccd81523d52f754d88efa55f2704 and SHA256 f4b6d122dfd68232c90f610fc794218b7c3ac8bcd1162e326a4cc5f033251137. Its source was inspected, but its functions and state were not imported or executed by the independent reconstruction below. The previously reported producer run covered 54,253 ungrounded graph/partition pairs, 15,698 grounded pairs and 203 host partitions; that execution is supplied evidence, not a new exhaustive critic run. The counts also agree with the simple-graph counts multiplied by the relevant Bell numbers.

The following exact source contracts were read and their blob hashes recomputed:

| Source | Verified Git blob | Critical use |
| --- | --- | --- |
| [UC001](UNIFORM_CONIC_GREEN_OPERATOR_AUDIT_UC001.md) | 437d40de4a1a5a723cb49bcf31f0190df1fda0b5 | Fixed cone, fixed negative-Sobolev stage and regulator derivative estimates |
| [UC002](AGENT_CRITICAL_REVIEW_UNIFORM_CONIC_UC002.md) | 948bfc32d186ea63c3543e7a5d2bad17bfd3c5b4 | Prior full-span and legal-partition objections; no independence imported |
| [UC003](UNIFORM_CONIC_ACCEPTANCE_UC003.md) | f78c82800d3850543591d8106d27911aa3b2bb34 | Accepted bounded scope and remaining source obligations |
| [Scalar105](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | a8ce66ff0edec33e2aff299550fca2089d671033 | Multiplication versus convolution and full scalar-stage requirements |
| [Mixed108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 | Actual partition inclusion108.7, complete coefficient stages108.6 and density typing |
| [Parameter126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 | Whole-source rows and the still-unproved full126.14 recovery |

One primary was frozen for this review. No post-freeze author correction was supplied or requested. Only this review file was authored by this critic.

## 2. Verification of each mathematical inference

**Component/block rank criterion: ACCEPT UC4.5 and UC4.6.** Strict positivity of the listed edge variances makes zero energy equivalent to equality across every edge, including each connected chain. Component constants therefore parameterize the whole heat kernel, including isolated vertices. Intersecting with the partition conormal imposes exactly the block-sum equations with coefficients equal to component/block intersection cardinalities. The parameterization is injective. Consequently the kernel dimension is the number of components minus the column rank of the intersection matrix. Positive semidefiniteness is essential in identifying the nullity of the restricted Gram matrix with the actual heat-kernel intersection; it holds here. Parallel edges and orientations leave this argument unchanged. A zero-variance listed edge would invalidate the component computation and is expressly excluded.

**All physical partitions in the ungrounded case: ACCEPT connectedness if and only if.** A connected graph has only the common constant kernel, whose nonzero elements have nonzero total coordinate sum and hence miss every partition conormal. Conversely the full-collision block gives one nonzero matrix row, so two or more components force a kernel. The component-size-weighted two-component witness in the primary satisfies the required total sum exactly. A disconnected graph can still pass selected partitions; no per-partition conclusion is replaced by connectedness.

**Grounded extension: ACCEPT UC4.10 and the all-partitions condition of at most one free component.** Setting the auxiliary covector slot to zero forces the entire ground-containing component to zero. Only ungrounded component constants remain. Removing its column therefore gives exactly the kernel equations, rather than imposing a physical partition constraint involving the ground. With one free component, its positive physical size prevents a nonzero constant from having total sum zero. With two free components the full physical collision again gives an obstruction. With no free components the full covariance is positive definite. Requiring the enlarged graph itself to be connected would be too strong. Coordinate heat is an explicitly additional convolutional operation type, not a newly admitted108 history.

**Actual legal partition input and nonsmoothing: ACCEPT UC4.8–UC4.9 within their stated ambient heat family.** Formula108.7 permits order-zero inclusion of a smooth compact block coefficient, with identity scalar locally, no insertion derivative and no vertex forgetting. Smooth block coefficients are admissible R1 coefficients; their inclusion can have the forbidden ambient conormal without pretending to be an independent-vertex R1 coefficient. Choosing the actual block-coordinate density fixes any Jacobian convention. The source is therefore genuine, and the subsequent heat convolution is an actual finite-measure convolution.

The orthogonal annihilator of the sum of the diagonal and heat ranges is the intersection of their annihilators. Rank failure makes this sum a proper linear subspace. The pushforward has positive total mass and support inside that subspace at every positive regulator. A smooth distribution with that support must vanish, contradicting its mass. The nonnegative choice prevents cancellation. A nonzero local smooth cutoff near a support point preserves a nonzero singular measure; Gaussian tails do not need to remain inside the original compact patch. This proves an actual nonsmooth output, not merely an algebraic zero-energy direction. It does not assert that this extra heat convolution is already an original108 universal source operation.

**Positive smooth-block converse: ACCEPT.** Rank passing makes the combined map from block and edge coordinates surjective. The product of a compact smooth block density and an edge Gaussian is Schwartz, also when the edge space has dimension zero. After an invertible linear splitting into kernel and image variables, integration over the kernel preserves the Schwartz estimates and permits every derivative under the integral. The density pushforward is thus Schwartz at every fixed positive regulator. Although the linear map need not be proper globally, this rapid decay supplies the needed convergent fiber integrals. This converse is explicitly restricted to smooth block inputs. It gives no smoothing theorem for an arbitrary singular tangential block coefficient.

**Conic neighborhoods, uniformity and parameter bounds: ACCEPT with the primary's hypotheses.** A nonempty conormal unit sphere is compact. Its strictly positive energy minimum persists on a sufficiently small closed neighborhood in the ambient unit sphere and hence on the corresponding punctured cone. For finitely many passing partitions the minima have a positive common lower bound. For weights in a compact positive set, comparison with the unit-weight form gives a uniform lower bound; upper bounds and bounded derivatives at each requested parameter order control the differentiated Gaussian factors. After factoring out the appropriate regulator power, the remaining polynomials in scaled frequency are absorbed by a weaker Gaussian. This recovers UC001's fixed-stage finite Sobolev estimates and all fixed regulator derivatives for fixed allowed conic symbols. It does not supply uniformity through zero edge weight, through an uncontrolled family of symbols or through unbounded parameter derivatives.

**One vertex, empty conormals and no edges: ACCEPT.** For one physical vertex the unique conormal is the zero space; an edgeless one-vertex graph is connected and the rank matrix is the one-by-one matrix with entry one. The gate is vacuous and consistent. More generally the discrete partition has zero conormal even for disconnected graphs, and its intersection matrix has full column rank. The primary correctly makes no nontrivial frequency-neighborhood smoothing assertion there. With no heat edges the measure is the point mass at zero, so the smooth-block converse only applies when the inclusion already fills the ambient space. Zero physical vertices are explicitly outside the graph assertion.

**Eleven-edge host: ACCEPT only the labelled conditional algebraic result.** The listed edges connect all six vertices; for example edges01,02,03,04,05 already form a spanning tree. Thus the all-partitions gate follows if those edges really are the directional convolutions of UC4.2. Reconstructing the actual restricted covariance verifies all 203 partitions below. Neither the original Wick multiplication-host label nor this arithmetic identifies its operator with that convolution family.

**No PHG or general-operator inference: ACCEPT the stated exclusions.** Ambient conic moderation and the smooth-block result do not specify fixed compatible105 powers, logarithms, auxiliary weights or differentiated recursive corner remainders. They do not prove continuity in completed108.6 coefficient sources, every R1 restriction and finite jet, actual proper density maps or whole-source126 row lifts. They leave the original rapid ideal unchanged. A connected ungrounded graph still annihilates common-coordinate frequencies, so global ellipticity and smoothing of arbitrary ambient distributions would be false. Universal150.L, residual W acyclicity, original R3, full126.14, higher weights and M5/R4 remain open. No inverse or contracting homotopy follows.

## 3. Independent hostile reconstruction and arithmetic evidence

The critic executed self-contained inline standard-library Python, using its own rational forward elimination, direct heat-direction dot products and restricted-growth partition labels. It neither imported the producer fixture nor reused its component, partition, covariance, rank or witness functions. This is logically distinct arithmetic reconstruction in the same local environment, not independent execution attestation.

For edges01 and23 and crossing blocks02 and13, take the two columns with signs chosen as in UC4.7. Direct dot products give

$$
K=\begin{pmatrix}2&-2\\-2&2\end{pmatrix},\qquad
z=q_1+q_2=(1,1,-1,-1).
$$

The Gram matrix has rank one despite both diagonal entries being two. The vector has zero sum on each crossing block and zero pairing with both heat directions. The component/block matrix has identical rows with entries one. Thus the test probes the whole two-dimensional conormal span, including the hostile combination, rather than checking its generators separately. For the aligned blocks01 and23 the reconstructed Gram matrix is diagonal with entries four, so the same disconnected heat graph passes that different partition.

| Independent exact control | Readback |
| --- | --- |
| Crossing blocks02 and13, heat edges01 and23 | Gram above; rank one; witness verified against both heat directions and both block sums |
| Aligned blocks01 and23, same heat | Gram diagonal entries four; rank two |
| Three physical vertices, heat directions coordinate0 and difference12, weights two-thirds and seven-fifths | Exactly one free component; all five reconstructed partition Grams have full rank |
| Three physical vertices, coordinate0 heat alone | Two free components; full-collision Gram has all four entries one and rank one |
| Two physical vertices, both coordinate directions grounded, weights three-sevenths and five-elevenths | No free component; full-collision Gram is the one-by-one matrix with entry68/77 |
| One vertex, no heat | Unique partition; empty conormal basis and zero Gram rank |
| Conditional eleven-edge host with the fixture's positive rational weights | All 203 independently enumerated partition Grams have full rank |

Final reconstruction output was status PASS, process exit code0. One preceding invocation completed its arithmetic assertions but failed while serializing rational numbers to JSON; adding a string serializer produced the successful final readback. No mathematical or producer-source change resulted.

Runtime readback was Windows win32, CPython3.12.12, executable F:\_codex\MATH\_evidence\reach-completion-20261027\.venv\Scripts\python.exe, with its prefix equal to that isolated virtual environment. The worktree had no uv.lock: this execution environment is **not pinned**. No packages were installed. Both reconstruction Python processes explicitly received UV_CACHE_DIR=C:\Users\jamie\AppData\Local\GCL\uv and PYTHONPYCACHEPREFIX=C:\Users\jamie\AppData\Local\GCL\PythonBytecodeCache. No WSL environment or system-site installation was used. The required ci/math_markdown_gate.py source preflight on this review, using the same environment and explicit caches, returned PASS and exit code0.

## 4. Final review disposition and remaining boundary

**BOUNDED ACCEPT at primary blob e3b4a794b022abbf5cd3b4b6c32c48ced94e82d8 and fixture blob af837ab9dfaaccd81523d52f754d88efa55f2704, with zero consolidated mathematical correction requests.** The accepted result classifies exactly when a specified finite graph-difference heat convolution is elliptic on a specified partition conormal; it includes a genuine nonsmoothing witness on failure and a smooth-block converse on passing. The separate coordinate-heat extension and ambient conic uniformity have their stated hypotheses.

A future scalar105 realization or mixed108 operator construction must still prove its actual factorization, every corner estimate and coefficient-stage map. A later ledger, exact-head CI, protected admission and protected readback remain separate transactions. This review grants no external certification or stronger original-source claim.
