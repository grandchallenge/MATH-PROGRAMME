# PC-WP02 — Perelman/reconstruction theorem crosswalk

## Reading rule

This crosswalk maps mathematical functions, not identical theorem numbering. Perelman's preprints are compressed research papers; Morgan–Tian reorganizes the proof into a monograph; Kleiner–Lott follows Perelman's first two papers more closely and records corrections and omitted details. A row means that the sources participate in the same downstream interface, not that their statements are word-for-word identical.

| Interface | Perelman primary location | Morgan–Tian reconstruction | Kleiner–Lott comparison | Campaign node |
|---|---|---|---|---|
| short-time flow and basic evolution | background imported in `P-I` | early Ricci-flow chapters | preliminary chapters | `PC02-T002` |
| `W`, `mu`, entropy monotonicity | `P-I`, section 3 | entropy/functional chapters | section group on `W` monotonicity | `PC02-T003` |
| no-local-collapsing | `P-I`, sections 4 and 8 | noncollapsing chapters | no-collapsing sections | `PC02-T006` |
| reduced distance and volume | `P-I`, sections 6–7 | reduced-geometry chapters | reduced-volume sections | `PC02-T004` |
| pseudolocality | `P-I`, section 10 | pseudolocality chapter | pseudolocality sections | `PC02-T005` |
| ancient `kappa`-solutions | `P-I`, section 11; corrections in `P-II`, section 1 | ancient-solution chapters | `kappa`-solution sections with corrections | `PC02-T007` |
| canonical neighbourhoods | `P-I`, section 12; surgery-flow strengthening in `P-II` | canonical-neighbourhood chapters and strong theorem in chapter 17 | canonical-neighbourhood sections | `PC02-T008`, `PC02-T012` |
| standard cap solution | `P-II`, section 2 | chapter 12 | standard-solution sections | `PC02-T009` |
| surgery construction | `P-II`, sections 3–5 | chapters 13–15 | surgery overview/construction sections | `PC02-T010`, `PC02-T013` |
| noncollapsing through surgery | `P-II`, construction argument | chapter 16 | surgery noncollapse sections | `PC02-T011` |
| all-time surgery flow | `P-II`, section 5 strategy | Theorem 15.9 plus chapters 16–17 | existence theorem and construction sections | `PC02-T013` |
| topology of surgery | `P-II` topological conclusion | Theorem 0.3 and Corollary 15.4 | surgery topology discussion | `PC02-T014`, `PC02-T017` |
| finite extinction | `P-III` | Theorem 0.4, Theorem 18.1, chapters 18–19 | not covered as the proof of `P-III` | `PC02-T016` |
| Poincaré conclusion | consequence of `P-II` + `P-III` | Corollary 0.5 and terminal argument following Theorem 18.1 | outside its principal coverage | `PC02-T019` |

## Version and correction ledger

### C-001 — Ancient-solution corrections

`P-II` states that inaccuracies in the ancient-solution discussion of `P-I` require correction. Consequently, `PC02-T007` is not sourced to `P-I` alone. It imports the corrected formulation through `P-II`, checked against `MT` and `KL`.

### C-002 — Maximal-horn volume assertion

`P-II` identifies a lower-volume assertion associated with the maximal-horn discussion in `P-I` as unjustified and unnecessary. The campaign does not use it in the canonical-neighbourhood or surgery chain.

### C-003 — Eventual globally smooth flow assertion

A sketched assertion in `P-I` that surgery flow would become smooth after some finite time is not used. The all-time surgery interface is instead reconstructed from `P-II` and `MT`, with only local finiteness on bounded intervals asserted before extinction.

### C-004 — Kleiner–Lott coverage boundary

`KL` is an independent detailed source for `P-I` and `P-II`; it explicitly discusses incorrect or incomplete statements and their repairs. It is not the finite-extinction reconstruction used here. `P-III` and `MT` govern `PC02-T016`.

### C-005 — Category statement scope

`MT` states the topological/smooth equivalence used in dimension three, but exact foundational theorem locations remain a separate Moise/Munkres extraction obligation. The campaign therefore marks `PC02-T001` as an audited interface with historical source debt, not as a newly proved equivalence.

## Crosswalk acceptance requirements

For a theorem interface to be accepted:

1. at least one primary source is named when the result originates in Perelman;
2. at least one detailed reconstruction supplies the expanded hypothesis/conclusion chain;
3. correction notes are attached before consumers are permitted;
4. section-number similarity is not mistaken for statement identity;
5. finite extinction is not sourced to `KL`;
6. the exact source edition or arXiv version is pinned before quotation-level certification.

## Remaining extraction work

The crosswalk is complete at mathematical-function and theorem-interface level. Remaining source debt is quotation-level and constant-level:

- exact Moise/Munkres theorem statements;
- exact Hamilton short-time theorem source;
- exact Kneser–Milnor formulation used by the extinction hypothesis bridge;
- line-by-line parameter dependence in the surgery induction;
- exact comparison of all corrections noted by `KL` with the pinned Perelman versions.
