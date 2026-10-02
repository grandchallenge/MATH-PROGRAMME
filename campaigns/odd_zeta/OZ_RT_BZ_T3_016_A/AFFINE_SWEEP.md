# OZ-RT-BZ-T3-016-A affine sweep

## Status and authority

This packet defines a modular sampling lane for the admitted canonical-gauge affine section of the order-7 E1 standalone system.

Exact protected predecessor at packet creation:

`0a75d3d3194b8923e687c153dc92fc7eea65b3e3`

Pinned upstream source:

- repository: `rain-1/-odd-zeta-values-moremath`;
- commit: `6cc0bf07137815ceeef0d9f340559f85352391e5`;
- tree: `be780558454b704bdd016a3070d698c2e106e2b8`.

The sweep is evidence generation only. It does not prove T3, construct a characteristic-zero certificate, promote any claim, or alter the current campaign terminal.

## Mathematical representation

The admitted E1 system has 1,624 boundary-forced numerator coordinates and a 576-dimensional homogeneous discrete-curl kernel. The admitted canonical gauge fixes the 576 `r` coefficients indexed by

`k^a l^b`, with `2 <= a <= 25` and `0 <= b <= 23`.

The complementary coordinate system therefore has exactly 1,048 free coordinates. The global gauge-domain result proves that this gauge is valid over `Q` for every integer `n >= 1`.

The sweep solves the seven standalone E1 right-hand sides in the primitive integer telescoper representation `A(n) = (a_0(n),...,a_4(n))`. The operator matrix is independent of scalar normalization of `A`, so the source-normalized section with `a_0=1` is derived algebraically from the primitive section whenever `a_0(n)` is nonzero modulo the sampling prime. A second linear solve is neither needed nor admitted as independent evidence.

## Linear solve

For each fiber `(n,p)` the sampler:

1. rebuilds the exact boundary-forced E1 ansatz from the locked source;
2. derives the 576 canonical gauge indices and 1,048 complementary indices;
3. evaluates the five primitive `a_t(n)` polynomials modulo `p`;
4. constructs all seven standalone right-hand sides at once;
5. solves an overdetermined `1112 x 1048` canonical-complement system with `fastlin.solve`;
6. requires rank exactly 1,048 and `nbad = 0`;
7. checks the resulting section on 16 disjoint fresh rows;
8. requires zero fresh residual violations;
9. preserves the 1,048 x 7 primitive section as little-endian `int32` data;
10. records a content digest of the primitive section and, when defined, the algebraically normalized section.

The governed block size is 64 at `p = 4194301`; the sampler checks

`64 * (p - 1)^2 < 2^53`

before execution, preserving the exact-float accumulation precondition used by the locked `fastlin.py` implementation.

The Q-row cache is prewarmed before worker processes are spawned so concurrent workers read an existing cache instead of racing to create it.

## First sweep request

The infrastructure packet installs request `OZ-RT-BZ-T3-016-A-AFFINE-SWEEP-000` in the disabled state. Its fixed proposed sampling geometry is:

- prime: `4194301`;
- fibers: `n = 1..384`;
- four chunks of 96 fibers;
- four worker processes per chunk;
- reconstruction set: first 360 fibers;
- untouched same-prime holdout: final 24 fibers;
- 64 extra fit rows per fiber;
- 16 fresh verification rows per fiber.

For `M` samples, the source rational reconstruction system at symmetric degree bound `d` has `2(d+1)` unknown coefficients and requires `M > 2(d+1)`. Therefore 360 reconstruction fibers support an exact modular test through

`d = floor((360 - 3)/2) = 178`.

This is deliberately above the old pivot-gauge exclusion bound 132. The old source degree measurements do not determine the canonical-gauge section and are used only to size this first experiment.

## Artifact contract

Each completed chunk preserves:

- `sections.npz`: primitive free-coordinate sections with shape `(sample_count,1048,7)`;
- `metadata.json`: exact source identities, sample range, per-fiber rank/fresh-check data, `A(n)` residues, and section digests;
- `coordinate-map.json`: exact E1 monomial ordering, gauge indices, free indices, and standalone-block ordering;
- `request.json`: the exact request that governed the run;
- `environment.txt`: Python and package environment for the runner.

Artifacts are retained as GitHub Actions artifacts and are not committed as mathematical authority.

## Activation sequence

The infrastructure request remains `enabled: false`. After this packet reaches protected `main`, activation is a separate exact-head transition that changes the request identifier and sets `enabled: true`. The heavy sampling jobs run only on a protected-main `push` carrying an enabled request, or on an explicit `workflow_dispatch` against an enabled request.

This separates infrastructure review from expensive evidence generation and binds the first full sweep to an exact protected request state.

## Follow-on analysis

After all four chunks complete:

1. verify all artifact identities and concatenate the 384 fibers;
2. reconstruct candidate rational coordinate functions from the first 360 fibers;
3. require exact agreement on all 24 untouched same-prime holdout fibers;
4. characterize observed numerator/denominator degrees and common denominator structure;
5. reduce the affine particular section against the already admitted saturated 576-column minimal polynomial kernel basis;
6. repeat at independent primes as required for coefficient reconstruction and CRT/rational recovery;
7. perform an independent exact characteristic-zero replay before any stronger certificate terminal can be admitted.

One-prime interpolation, even with holdout success, is modular candidate evidence only.

## Claim firewall

The request and artifact metadata are required to retain:

- `evidence_effect = MODULAR_CANDIDATE_ONLY`;
- `proof_effect = NONE`;
- `promotion_effect = NONE`.

The current campaign terminal remains

`ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED`.
