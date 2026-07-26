# Campaign Promotion Register

## Status

Active documentary promotion register, 2026-07-26.

This register records repository-review and merge conditions for governed campaign artifacts whose integrated files preserve their pre-merge review wording. It changes documentary lifecycle and routing only. It does not strengthen any mathematical claim.

## Promoted WP00 entries

| Artifact | Campaign | Merge evidence | Documentary disposition | Mathematical boundary |
|---|---|---|---|---|
| `YM-WP00-source-normalization-equivalence-audit` | `YM-001` | PR #86; merge commit `fa0c933e432ac4726798d70807e2ab4d0e359daa` | Repository review and merge condition discharged; promoted as the source-normalization and equivalence-control dossier | No construction of four-dimensional quantum Yang–Mills theory, mass-gap proof, confinement theorem, or area law |
| `PNP-WP00-source-definition-equivalence-audit` | `PNP-001` | PR #88; merge commit `000aada57740f20d6613a2cd6bafc07a56290355` | Repository review and merge condition discharged; promoted as the source, machine, encoding, and equivalence-control dossier | No proof of `P = NP` or `P != NP`, new polynomial-time algorithm, unrestricted lower bound, or barrier theorem |
| `RH-WP00-source-normalization-equivalence-audit` | `RH-001` | PR #89; merge commit `27873011c739516ac18134e529a708e6c71bd9e8` | Repository review and merge condition discharged; promoted as the source, function, zero, and equivalence-control dossier | No proof or disproof of RH, new zero theorem, prime-error theorem, equivalent criterion, Hilbert–Pólya operator, or certified zero range |

## Retained post-merge blockers

| Artifact | Campaign | Integration evidence | Current disposition | Remaining blockers |
|---|---|---|---|---|
| `RH-WP01` | `RH-001` | PR #90; merge commit `895ce47cbf47fc6715e365d7c31a010fcda425cc`; programme-policy run `30156255759` succeeded | Implemented, merged, and CI-passed eliminative false-proof atlas; **not formally promoted** | Legacy review retains `promotion_recommended: false` and a blocking Referee finding; independent source/concordance review and a schema-bound or superseding promotion decision remain required |
| `RH-WP02` | `RH-001` | PR #90; merge commit `895ce47cbf47fc6715e365d7c31a010fcda425cc`; programme-policy run `30156255759` succeeded | Implemented, merged, and CI-passed source-normalized theorem and barrier ledger; **not formally promoted** | Legacy review retains `promotion_recommended: false` and a blocking Referee finding; independent source-locator review and a schema-bound or superseding promotion decision remain required |

The governing record is [`campaigns/riemann_hypothesis/RH_WP01_WP02_POST_MERGE_DISPOSITION.md`](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/riemann_hypothesis/RH_WP01_WP02_POST_MERGE_DISPOSITION.md).

## Interpretation rule

The integrated WP00 files remain authoritative for their source locks, definitions, equivalence boundaries, exclusion ledgers, false-proof seeds, and next-stage gates. Their phrases such as `promotion eligible`, `repository review required`, or unchecked merge boxes record the state at artifact freeze and are not silently edited after merge.

Repository merge and successful CI establish integration and replay facts. They do not override an explicit blocking review or promote a mathematical result. A retained-blocker entry is therefore a current documentary disposition, not a contradiction.

## Governing references

- `ADR-0009`
- `ADR-0010`
- `DOMAIN_REGISTRY.yaml`
- `docs/domains/yang_mills.md`
- `docs/domains/p_vs_np.md`
- `docs/domains/riemann_hypothesis.md`

## Maintenance rule

Add an entry when a governed campaign artifact preserves a pre-merge status snapshot but later repository action changes its documentary disposition. Do not use this register for theorem promotion, certification claims, novelty, or unreviewed branch state.
