# HC-001 — Next executable stage after WP00

## Current decision

The mathematical content of the source, normalization, and equivalence audit is complete in draft. Promotion remains blocked by Council integration and repository validation.

No mechanism, computational observatory, restricted target, or novelty claim is authorized by this draft.

## Promotion prerequisites

1. Amanuensis confirms cross-document consistency across Programme, Forge, Solve, and Cert artifacts.
2. Referee reconstructs:
   - the canonical statement;
   - the cycle-map/generator equivalence;
   - the codimension `n-1` boundary without algebraic inverse-Lefschetz circularity;
   - the dimension-at-most-three consequence;
   - every formulation separation.
3. Repository checks pass for all four draft PRs.
4. The proof-debt register is updated with resulting evidence.

## Permitted parallel work after promotion

### HC-WP01 — false-proof atlas

Build minimized fixtures for:

- rational/integral coefficient drift;
- arbitrary complex `(p,p)` versus rational Hodge;
- higher-codimension extrapolation from Lefschetz `(1,1)`;
- algebraic inverse-Lefschetz or Kunneth projectors assumed;
- Hodge-locus algebraicity promoted to class algebraicity;
- deformation transport without a relative-cycle theorem;
- numerical period recognition promoted to exact algebraicity;
- Tate reduction without specialization/comparison/lifting;
- topological Chern character promoted to algebraic cycle generation;
- Abel-Jacobi treated as complete;
- projective replaced by compact Kahler;
- absolute or motivated promoted to algebraic;
- very-general results promoted to every fiber;
- effectivity added to the target.

Completion test: every fixture states the tempting proof, exact failure, smallest missing theorem or counterexample, what is ruled out, and what survives.

### HC-WP02 — known-case and construction ledger

For each admitted family, record:

- exact variety class, dimension, and codimension;
- coefficient ring;
- source and theorem locator;
- whether all classes or selected classes are treated;
- the actual cycle-construction mechanism;
- use of monodromy, deformation, invariant theory, correspondences, or arithmetic specialization;
- conditional dependencies;
- exact equality certificate in cohomology;
- prior-art and novelty boundary.

Completion test: a specialist can reconstruct why each admitted case produces algebraic cycles rather than relying on a theorem-name catalogue.

## Still prohibited

- selecting `HC-R021` before WP01/WP02 and prior-art integration;
- broad period computations intended as evidence for universal Hodge;
- treating symbolic intersection output as exhaustive generation;
- importing standard conjectures, variational Hodge, or Tate as invisible assumptions;
- claiming novelty from absence in a bounded search;
- using `formalized` for a theorem proved only in an abstract surrogate interface;
- changing `Q`, projectivity, or universal quantifiers without renaming the claim.

## Inputs

- `00_README.md`
- `02_NOTATION_REGISTRY.yaml`
- `03_STATEMENT_LATTICE.yaml`
- `04_PROBLEM_AND_STATUS_AUDIT.md`
- `05_KNOWN_CASE_LEDGER.csv`
- `06_DEPENDENCY_DAG.json`
- `07_IMPLICATION_LEDGER.yaml`
- `08_FALSE_PROOF_SEEDS.yaml`
- `09_PROOF_DEBT.json`
- `10_CLAIM_LEDGER.yaml`
- `11_CERT_HANDOFF.md`
- MATHFORGE source and fixture ledgers
- MATHSOLVE statement lattice and obligation DAG
- MATHCERT schema and certification boundary

## Outputs after promotion

```text
campaigns/hodge_conjecture/WP01_FALSE_PROOF_ATLAS/
  00_README.md
  01_FIXTURE_LEDGER.yaml
  fixtures/
  09_PROOF_DEBT.json
  10_CLAIM_LEDGER.yaml
  12_NEXT_EXECUTABLE_STEP.md

campaigns/hodge_conjecture/WP02_KNOWN_CASE_CONSTRUCTION_LEDGER/
  00_README.md
  04_SOURCE_NORMALIZED_CASES.md
  05_CONSTRUCTION_MECHANISM_LEDGER.yaml
  06_DEPENDENCY_DAG.json
  09_PROOF_DEBT.json
  10_CLAIM_LEDGER.yaml
  11_CERT_HANDOFF.md
```

## Bounded next action

- Input: four draft branches and this WP00 package.
- Operation: open draft PRs, run checks, perform Amanuensis and Referee reviews, and repair any conflict.
- Output: promoted `HC-WP00` or an explicit blocked disposition.
- Completion test: `promotion.ready_for_next_stage=true`, no blocking debt, and passing relevant checks.
- Spine node advanced: `HC-T004`; next nodes opened: `HC-O009..HC-O019` and `HC-K008`.