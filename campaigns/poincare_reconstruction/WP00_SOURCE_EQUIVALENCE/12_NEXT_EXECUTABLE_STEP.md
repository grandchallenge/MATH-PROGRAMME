# PC-001 — Next executable stage after WP00

## WP00 decision

The source, normalization, route-equivalence, and non-circularity audit is promoted.

The campaign now has:

- a corrected solved-result status;
- canonical topological, PL, and smooth theorem statements;
- an exact implication hierarchy separating Poincaré, elliptization, geometrization, and finite extinction;
- a topological-to-smooth category bridge with explicit source debt;
- a primary Poincaré-specific proof route;
- a theorem-spine dependency DAG;
- proof-debt and claim ledgers;
- a delimited MATHCERT handoff;
- an Agent Council review record.

WP00 promotion certifies the architecture and claim boundary. It does not independently certify the Hamilton–Perelman analytic core.

## Permitted parallel work

### PC-WP01 — false-proof and semantic-failure atlas

Build minimized fixtures for the following invalid routes.

1. **Homology-sphere substitution**  
   Replace simple connectivity by homology equivalence and incorrectly conclude `S³`. Use the Poincaré homology sphere as the canonical obstruction.

2. **Open contractible substitution**  
   Infer that every contractible open `3`-manifold is `R³`. Use the Whitehead manifold as the canonical obstruction.

3. **Boundary suppression**  
   Omit “closed” or “without boundary.” Use the `3`-ball as the smallest counterexample to the malformed statement.

4. **Smooth-flow-through-singularity**  
   Assume the original Ricci flow remains smooth for all time and converges after rescaling.

5. **Surgery-is-topology-preserving**  
   Treat cutting necks, capping, and discarding components as diffeomorphisms.

6. **Extinction-without-ledger**  
   Infer `M=S³` merely because some surgery flow becomes empty.

7. **Blow-up/original-space confusion**  
   Transfer the topology or global geometry of a pointed rescaling limit to the original manifold without a theorem.

8. **Qualitative non-collapsing**  
   Replace quantitative `kappa`-non-collapsing and scale conditions by a verbal compactness claim.

9. **Category suppression**  
   Begin with a topological manifold, write a smooth PDE immediately, and never cite triangulation/smoothing.

10. **Route-strength collapse**  
    Call Poincaré, elliptization, and geometrization equivalent.

11. **Circular prime-factor discharge**  
    Assume every simply connected prime `3`-manifold is `S³` while proving Poincaré.

12. **Formal-interface overclaim**  
    Formalize a theorem of the form “if surgery and extinction hold, then `M=S³`” and advertise it as a formal proof of the full theorem.

Each fixture must contain:

- tempting argument;
- exact hidden premise or invalid inference;
- smallest counterexample or dependency gap;
- theorem-spine nodes bypassed;
- what the failure rules out;
- what remains viable.

### PC-WP02 — source-normalized Hamilton–Perelman theorem ledger

Produce a theorem-by-theorem crosswalk among:

- Perelman `math/0211159`;
- Perelman `math/0303109`;
- Perelman `math/0307245`;
- Morgan–Tian;
- Kleiner–Lott;
- relevant Hamilton precursor results.

The ledger must cover:

1. Ricci-flow normalization and parabolic scaling.
2. Entropy, reduced length, reduced volume, and monotonicity.
3. No-local-collapsing and pseudolocality interfaces.
4. Pointed compactness and blow-up construction.
5. `kappa`-solution hypotheses and classification used by surgery.
6. Canonical-neighbourhood theorem and scale parameters.
7. Standard solution and cap model.
8. Surgery parameter hierarchy, persistence, and non-accumulation.
9. Topological effect of surgery and discarded-component classification.
10. Prime-decomposition/group-hypothesis bridge.
11. Finite-extinction functional, differential inequality, and surgery-time behavior.
12. Terminal connected-sum induction and Poincaré discharge.
13. Every correction, deferral, or exposition-level divergence among sources.

Every theorem entry must record:

- stable theorem ID;
- exact statement or faithful normalized paraphrase;
- source and location;
- hypotheses;
- normalizations and constants;
- incoming dependencies;
- downstream consumers;
- proof status: primary-source checked, reconstruction checked, independently replayed, or pending;
- known semantic hazards.

## Still prohibited

- calling WP00 a new proof;
- compressing singularity control to “Ricci flow smooths the manifold”;
- treating a detailed reconstruction as a primary source;
- treating Perelman's first preprint as unaffected by later corrections;
- importing the Poincaré theorem in the prime-factor or terminal topology steps;
- opening a numerical campaign as evidence for a solved theorem;
- claiming full formal certification from the terminal MATHCERT slice;
- proceeding to PC-WP03 before WP01/WP02 integration and Referee review.

## Outputs

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

WP01 is complete when every listed shortcut has an exact obstruction or dependency diagnosis and none of the fixtures accidentally invokes the target theorem.

WP02 is complete when a specialist can traverse the Poincaré-specific proof from initial metric to finite extinction and terminal topology while locating every theorem, hypothesis, parameter dependency, source correction, and remaining proof debt.

## Next integration gate

After WP01 and WP02 are Referee-reviewed, perform adversarial semantic review and cross-document integration. Only then may `PC-WP03` open the surgery-topology and extinction bookkeeping reconstruction.