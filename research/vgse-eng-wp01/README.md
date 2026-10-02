# VGSE-ENG-WP01 — quotient design space and first forward-response law

**Campaign:** `VGSE-001`  
**Work package:** `VGSE-ENG-WP01`  
**Status:** work-branch engineering result; protected admission pending  
**Research question:** What reusable engineering laws are latent in the qualified VGSE structural object?

## Evidence binding

This work package is bound to:

- MATH-PROGRAMME starting branch head `research/vgse-eng-wp01@4624294cd09b81145b8fe174447ba15d392f241b`;
- MATHCERT protected head `2f27aed33b32b4caf6ff8622c87cfd6d40e97607`;
- MATHSOLVE protected head `b0854bb7770296b610b655753bc62b27365b27bb`.

The protected mathematical starting point qualifies exactly `VGSE-C00`, `VGSE-C01`, `VGSE-C04`, and `VGSE-C05`. `VGSE-C06` remains excluded. Nothing in WP01 changes that boundary.

## 1. Object and layered representation

The WP01 object is the **qualified reduced bipartite boundary-measurement graph** used by C04/C05. It has eight internal vertices, six ordered boundary vertices, sixteen edges, and thirty-one almost-perfect matchings.

This object is not asserted to be a physical crease graph, stiffness network, rigid-fold mechanism, or recovered source build specification.

The layers are kept separate.

| Layer | WP01 representation | Current authority |
| --- | --- | --- |
| Topology/combinatorics | bipartite colors, 16-edge incidence, six ordered boundary vertices, almost-perfect-matching rule | fixed structural object |
| Geometry | boundary and interior planar embedding coordinates admitted by the bounded C05 result | declared; not coupled into the first forward map |
| Metric/response | sixteen positive edge weights, reduced by internal-vertex gauge to eight canonical coordinates | analyzed in WP01 |
| Physical realization | thickness, constitutive law, hinge behaviour, friction, tolerance, contact, plasticity, fatigue, fabrication constraints | candidate variables only; not modeled |

The machine-readable representation is `model.json`.

## 2. Forward map

Let `M_I` be the set of almost-perfect matchings with boundary set `I`. For positive edge weights `w_e`, define

\[
\Delta_I(w)=\sum_{M\in M_I}\prod_{e\in M}w_e.
\]

The fixed topology supports nineteen nonzero boundary minors. `123` is absent. Use `124` as projective reference and let

\[
\theta_e=\log w_e,
\qquad
F(\theta)_I=\log\frac{\Delta_I(w)}{\Delta_{124}(w)},
\qquad I\neq124.
\]

Thus the raw design vector has dimension 16 and the response has 18 projective coordinates.

At the protected exact C04 representative, the replay recovers all nineteen target Plücker coordinates with common scale `1/7` exactly.

### Analytical sensitivity

For a fixed boundary class `I`, give each matching probability proportional to its weight monomial. Then

\[
\frac{\partial\log\Delta_I}{\partial\theta_e}
=
\Pr_I(e\in M).
\]

Therefore

\[
\frac{\partial F_I}{\partial\theta_e}
=
\Pr_I(e\in M)-\Pr_{124}(e\in M).
\]

This gives the Jacobian without finite differencing. It also gives a useful interpretation: local response sensitivity is the difference between edge-occupancy probabilities in two matching ensembles.

## 3. First structural law: raw weights contain an eight-dimensional gauge redundancy

For each internal vertex `v`, choose `g_v>0` and transform each incident edge by its internal endpoint factors:

\[
w'_{uv}=g_u g_v w_{uv},
\]

where a boundary endpoint contributes no gauge factor.

Every almost-perfect matching covers every internal vertex exactly once. Consequently every matching monomial, independent of boundary set, is multiplied by the same factor

\[
\prod_{v\in V_{\mathrm{int}}}g_v.
\]

Every `Delta_I` therefore receives one common scale, and every projective ratio `Delta_I/Delta_124` is **exactly invariant**.

**VERIFIED ENGINEERING RESULT — structural model.** The sixteen raw positive edge weights are not sixteen independent response controls. The fixed VGSE graph has eight independent internal-vertex gauge directions that leave `F` unchanged exactly.

At the protected representative:

- raw Jacobian rank: `8`;
- raw Jacobian nullity: `8`;
- gauge-generator rank: `8`;
- `max |J G|`: `1.11e-16` numerically.

Because the local kernel dimension equals the gauge dimension, no additional infinitesimal non-identifiability is observed at this point.

## 4. Canonical eight-parameter design coordinates

WP01 fixes the gauge by imposing

- `B1=B2=B3=B4=B5=B6=1`;
- `F01|F04=1`;
- `F03|F06=1`.

The remaining canonical coordinates are

1. `F01|F02`;
2. `F07|F02`;
3. `F03|F04`;
4. `F03|F08`;
5. `F07|F04`;
6. `F05|F04`;
7. `F05|F06`;
8. `F07|F08`.

The protected exact representative is already in this gauge, with values

`1, 1, 2/7, 25/7, 6/7, 3/25, 2/25, 9/7`.

The 18-by-8 canonical Jacobian is full column rank. Its singular values are

`5.9301, 2.1239, 1.9627, 1.5477, 1.3473, 1.2265, 0.9971, 0.8111`,

with condition number `7.3115`.

This means the quotient coordinates are locally identifiable from the projective response at the baseline and are not close to a rank singularity there.

### Local control strengths

Using log-weight coordinates, the aggregate column sensitivities `||dF/dlog(w_e)||_2` are:

| Canonical parameter | L2 sensitivity |
| --- | ---: |
| `F03|F04` | 3.8208 |
| `F01|F02` | 3.7027 |
| `F03|F08` | 2.7520 |
| `F05|F04` | 2.3007 |
| `F07|F02` | 1.9262 |
| `F07|F04` | 1.6265 |
| `F05|F06` | 1.4495 |
| `F07|F08` | 1.1243 |

These are local structural-response sensitivities. They are not physical stiffness sensitivities.

## 5. Independent-representation reconciliation

MATHSOLVE retained an older positive numerical weight representative. MATHCERT later produced an exact positive representative independently.

**GCL OBSERVATION.** After applying the canonical internal-vertex gauge to the older MATHSOLVE representative, every one of the sixteen canonicalized weights agrees with the MATHCERT exact representative to a maximum absolute discrepancy of `8.88e-16`.

This explains why the raw weight lists look very different while producing the same projective boundary data. The raw edge weights are representation-dependent; the quotient response is the intrinsic object for this WP01 metric layer.

This is not evidence that the weights are physical stiffnesses.

## 6. Candidate-invariant screen and falsification

Candidate invariant: **support of the projective boundary measurement**.

Admissible transformation class: arbitrary changes of all sixteen edge weights while every weight remains strictly positive and the topology is fixed.

For a fixed boundary class, `Delta_I` is a sum of positive matching monomials. Therefore `Delta_I>0` exactly when the topology admits at least one matching in that class. Under strict positivity, the nineteen-element support is topology-controlled and weight-invariant.

**VERIFIED ENGINEERING RESULT — structural model.** The fixed topology preserves the nineteen-minor support under every strictly positive weight assignment.

Deliberate falsification: relax strict positivity and set `F07|F04=0`. Minor `345` has one matching and that matching uses `F07|F04`; `Delta_345` therefore vanishes. The support invariant fails once zero weights are admitted.

The transformation class is therefore material. The result is not “support is invariant under arbitrary weight changes”; it is “support is invariant under strictly positive weight changes on this fixed topology.”

## 7. Bounded inverse-design result

Take the protected projective response as the target `y*` and ask for all sixteen raw positive edge weights `theta*` that realize it.

**VERIFIED ENGINEERING RESULT — negative inverse result.** The raw inverse problem is non-identifiable. Every internal-vertex gauge orbit supplies an eight-dimensional family of distinct raw designs with exactly the same `y*`.

WP01 constructs an explicit nontrivial gauge-transformed second solution. Its maximum projective-response discrepancy from the baseline is `2.22e-16` in floating replay.

After quotienting by gauge, the canonical Jacobian has rank eight. The evidence therefore supports local recovery of eight canonical coordinates near the protected baseline, while raw sixteen-weight recovery is impossible without an arbitrary gauge convention or extra information.

Engineering utility: optimization and inverse design should occur in the eight-dimensional quotient coordinates, not in the sixteen raw weights. This removes eight exactly flat directions before any later physical model is introduced.

## 8. Robustness test

A deterministic perturbation screen used seed `20260916` and 256 samples in the eight canonical log-weight coordinates. Each sample changed no edge by more than 5% multiplicatively.

Observed across all samples:

- supported-minor count: always `19`;
- canonical Jacobian rank: always `8`;
- minimum singular value: `0.8012` to `0.8193`;
- condition number: `7.2359` to `7.4027`.

**GCL OBSERVATION.** The local quotient identifiability and support result are stable across this declared perturbation neighborhood.

This is a robustness result for the structural boundary-response model only. It says nothing about tolerance, thickness, friction, or material error.

## 9. Recoverability and the C06 boundary

The visible historical geometry does not determine the pinned-C weight class by taking Euclidean edge lengths. Existing protected evidence rejects that bridge, even after boundary relabeling and global color/complement conventions.

Accordingly:

- source-visible geometry is not a certified build specification;
- the raw weights are not recoverable from the projective response because of gauge;
- eight canonical quotient coordinates are locally recoverable from the projective response near the protected baseline;
- no Figure-16-to-pinned-C source correspondence is created here;
- any later realization synthesized in these coordinates is a **GCL DESIGN**, not recovered source geometry.

## 10. Core-clarity disposition

1. **Object:** the qualified reduced bipartite boundary-measurement graph and its positive-weight family.
2. **Freedom:** positive edge weights may vary on fixed topology; internal-vertex gauge changes do not change projective response.
3. **Invariant:** the nineteen-minor support under strict positivity; projective response under gauge.
4. **Control:** eight canonical log-weight coordinates materially control the local projective response.
5. **Map:** `F(theta)=log(Delta_I/Delta_124)`.
6. **Inverse:** sixteen raw weights are non-identifiable; eight canonical coordinates are locally identifiable at the protected baseline.
7. **Robustness:** 256 canonical perturbations up to 5% preserved support and full rank.
8. **Utility:** reduce structural inverse design from a redundant 16-dimensional raw space to an identifiable 8-dimensional quotient space.
9. **Boundary:** no physical stiffness, rigid folding, collision, finite-thickness, manufacturing, durability, novelty, patent, product, or commercial result follows.

## 11. Reproduction

From this directory:

```bash
python -m pip install -r requirements.txt
python analyze_wp01.py
python test_wp01.py
```

`RESULTS.json` is the deterministic retained result. The test suite replays the exact baseline, gauge nullspace, canonical rank, falsification case, numerical-to-exact gauge reconciliation, inverse non-identifiability witness, and perturbation screen.

## 12. Next substantive action

The evidence supports a narrower successor rather than broad simulation or fabrication.

**Proposed next action: quotient-response continuation and singular-locus search.** Continue in the eight canonical log-weight coordinates, solve several bounded target-response perturbations, and track the smallest singular value of the canonical Jacobian. The objective is to determine where local inverse design remains well-conditioned, where it becomes non-unique or singular, and whether those boundaries correspond to useful response amplification or loss of admissibility.

Only after the metric quotient map is understood should a separate work package couple geometric realization variables or physical parameters into a response model.
