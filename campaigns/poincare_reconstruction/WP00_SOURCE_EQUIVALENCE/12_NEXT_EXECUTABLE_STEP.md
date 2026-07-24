# PC-001 — Next executable stage after WP00

## WP00 decision

The source, normalization, route-equivalence, and non-circularity audit is promoted. This certifies the campaign architecture and claim boundary, not the Hamilton–Perelman analytic core.

## PC-WP01 — false-proof and semantic-failure atlas

Build minimized fixtures for:

1. **Homology-sphere substitution** — replace simple connectivity by homology equivalence; use the Poincaré homology sphere as obstruction.
2. **Open contractible substitution** — infer every contractible open `3`-manifold is `R³`; use the Whitehead manifold.
3. **Boundary suppression** — omit `closed`; use the `3`-ball.
4. **Smooth flow through singularity** — assume the original Ricci flow remains smooth for all time.
5. **Surgery is topology-preserving** — treat cuts, caps, and discarded components as diffeomorphisms.
6. **Extinction without ledger** — infer `M=S³` merely because a surgical flow becomes empty.
7. **Blow-up/original-space confusion** — transfer global topology from a pointed rescaling limit.
8. **Qualitative non-collapsing** — replace quantitative `kappa`-non-collapsing by verbal compactness.
9. **Category suppression** — apply a smooth PDE directly to an unbridged topological manifold.
10. **Route-strength collapse** — call Poincaré, elliptization, and geometrization equivalent.
11. **Circular prime-factor discharge** — assume every simply connected prime is `S³`.
12. **Formal-interface overclaim** — advertise a conditional terminal formalization as a full formal proof.

Every fixture must record:

- tempting argument;
- exact hidden premise or invalid inference;
- smallest counterexample or dependency gap;
- theorem-spine nodes bypassed;
- what the failure rules out;
- what remains viable.

## PC-WP02 — source-normalized Hamilton–Perelman theorem ledger

Build a theorem-by-theorem crosswalk among:

- Perelman `math/0211159`;
- Perelman `math/0303109`;
- Perelman `math/0307245`;
- Morgan–Tian;
- Kleiner–Lott;
- relevant Hamilton precursor results;
- Moise/Munkres and Kneser–Milnor topology interfaces.

The ledger must cover:

1. Ricci-flow normalization and parabolic scaling.
2. Entropy, reduced length, reduced volume, and monotonicity.
3. No-local-collapsing and pseudolocality.
4. Pointed compactness and blow-up construction.
5. `kappa`-solution hypotheses and classification used by surgery.
6. Canonical neighbourhoods and scale parameters.
7. Standard solutions and cap models.
8. Surgery parameter hierarchy, persistence, and non-accumulation.
9. Topological effects and discarded-component classification.
10. Prime-decomposition/group-hypothesis bridge.
11. Finite-extinction functional and differential inequality.
12. Surgery-time behavior of the extinction quantity.
13. Terminal connected-sum induction and Poincaré discharge.
14. Corrections or divergences among sources.

Every theorem entry must record:

- stable ID;
- exact statement or faithful normalized paraphrase;
- source and location;
- hypotheses;
- normalizations and constants;
- incoming dependencies;
- downstream consumers;
- verification state;
- semantic hazards.

## Still prohibited

- calling WP00 a new proof;
- compressing singularity control to “Ricci flow smooths the manifold”;
- treating a reconstruction as a primary source;
- ignoring corrections between Perelman's papers;
- importing Poincaré in the prime-factor or terminal steps;
- opening numerical evidence work;
- claiming full formal certification from the terminal MATHCERT slice;
- opening PC-WP03 before WP01/WP02 integration and Referee review.

## Expected artifacts

### WP01

```text
campaigns/poincare_reconstruction/WP01_FALSE_PROOF_ATLAS/
  00_README.md
  01_FIXTURE_LEDGER.yaml
  fixtures/
  09_PROOF_DEBT.json
  10_CLAIM_LEDGER.yaml
  12_NEXT_EXECUTABLE_STEP.md
```

### WP02

```text
campaigns/poincare_reconstruction/WP02_HAMILTON_PERELMAN_LEDGER/
  00_README.md
  02_SOURCE_REGISTRY.yaml
  03_SOURCE_CROSSWALK.md
  04_NORMALIZED_THEOREM_LEDGER.md
  05_PARAMETER_AND_NORMALIZATION_LEDGER.yaml
  06_DEPENDENCY_DAG.json
  07_CORRECTION_AND_DIVERGENCE_LOG.md
  09_PROOF_DEBT.json
  10_CLAIM_LEDGER.yaml
  11_CERT_HANDOFF.md
```

## Completion tests

WP01 closes when every listed shortcut has an exact obstruction or dependency diagnosis and no fixture invokes the target theorem.

WP02 closes when a specialist can traverse the Poincaré-specific proof from initial metric to extinction and terminal topology while locating every theorem, hypothesis, parameter dependency, correction, and remaining debt.

## Next integration gate

After WP01 and WP02 receive adversarial and Referee review, perform cross-document integration. Only then may `PC-WP03` open the surgery-topology and extinction-bookkeeping reconstruction.