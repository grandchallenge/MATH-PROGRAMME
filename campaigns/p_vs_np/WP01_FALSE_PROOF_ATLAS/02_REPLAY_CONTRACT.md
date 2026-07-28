# PNP-WP01 — Replay Contract

## Accepted replay claim

The replay may state:

> The atlas has the required number of uniquely identified fixtures; every fixture has an explicit invalid inference, missing obligation, witness, decision, remediation, and resolved WP02 interface.

It may not state that the replay:

- proves `P = NP` or `P != NP`;
- proves a lower bound;
- proves that a proposed algorithm is impossible;
- exhausts all possible proof methods;
- upgrades a barrier theorem into an impossibility theorem;
- validates the mathematical truth of a source theorem.

## Decision semantics

`REJECT` means the inference as written is invalid.

`NARROW` means a nearby statement may be valid only after its conditions and scope are restored.

Neither decision refutes the terminal proposition or its negation.

## Required mutation failures

The test package must reject at least:

1. duplicate fixture identifiers;
2. missing obligations or remediation;
3. unknown WP02 interfaces;
4. a decision outside `REJECT` and `NARROW`;
5. a false terminal promotion;
6. an opened mechanism, experiment, target-selection, or novelty gate;
7. a current-frontier record without source-maturity debt.
