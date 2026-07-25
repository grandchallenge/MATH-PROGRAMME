# PC-WP03 adversarial surgery histories

## Purpose

These fixtures test the finite topology certificate, not the Hamilton–Perelman analytic theorems.

Run:

```bash
python campaigns/poincare_reconstruction/WP03_SURGERY_TOPOLOGY/05_ADVERSARIAL_HISTORIES/validate_histories.py
```

The validator uses only the Python standard library.

## Fixture set

`fixtures.json` contains two base histories and fourteen deterministic cases. The validator deep-copies a base, applies the listed mutations, and checks the expected error-code set.

### Positive cases

| Case | Coverage |
|---|---|
| `valid_separating_history` | separating cut, two caps, two children, terminal spherical factors, simply connected discharge |
| `valid_nonseparating_history` | nonseparating cut, one child, explicit `S^2 x S^1` factor, general extinction-class profile |

### Malformed cases

| Case | Required rejection |
|---|---|
| `invalid_missing_source_binding` | unresolved source provenance |
| `invalid_event_order` | noncontiguous indices or nonmonotone event time |
| `invalid_nonseparating_missing_bundle` | lost `S^2`-bundle factor |
| `invalid_separating_child_count` | separating cut with other than two children |
| `invalid_duplicate_ancestry_parent` | new child assigned more than one parent |
| `invalid_reconstruction_partition_loss` | post-component omitted from backward equation |
| `invalid_unpermitted_discard` | discarded topology outside source list |
| `invalid_twisted_bundle_orientable` | nonorientable factor in orientable profile |
| `invalid_discrete_only_finiteness` | finite history inferred from discreteness rather than local finiteness |
| `invalid_extinction_nonempty_terminal` | nonempty terminal active set |
| `invalid_simple_connectivity_factor` | nontrivial factor retained under simply connected profile |
| `invalid_rp3_normalization` | `RP^3#RP^3` not expanded to two spherical factors |

## Error-code contract

| Code | Meaning |
|---|---|
| `PC03-E000` | missing required structure |
| `PC03-E001` | duplicate or colliding identifier |
| `PC03-E002` | missing or unresolved source binding |
| `PC03-E003` | invalid event index/time order |
| `PC03-E004` | active-set discontinuity |
| `PC03-E005` | unresolved component or factor |
| `PC03-E006` | malformed cut/cap cardinality |
| `PC03-E007` | malformed nonseparating bundle equation |
| `PC03-E008` | invalid ancestry |
| `PC03-E009` | reconstruction partition or conservation failure |
| `PC03-E010` | impermissible or untracked discard |
| `PC03-E011` | orientation-profile violation |
| `PC03-E012` | invalid finite-history derivation |
| `PC03-E013` | invalid extinction terminal state |
| `PC03-E014` | simply connected terminal-discharge failure |
| `PC03-E015` | invalid `RP^3#RP^3` normalization |
| `PC03-E016` | event-type contract violation |
| `PC03-E017` | lifecycle endpoint mismatch |

Passing the fixtures certifies only the finite combinatorial bookkeeping contract.
