# Problem and status audit

## Canonical statement

Every finite nontrivial union-closed family `F` has an element `x` satisfying

```text
2 * frequency_F(x) >= |F|.
```

Status: `OPEN`.

## Source-lock refresh date

2026-07-27.

## Admitted source terrain

| Source | Audit state | Admitted use |
|---|---|---|
| Reimer (2003) | primary statement checked | average set-size theorem |
| Bruhn--Schaudt (2015) | survey orientation checked | history and equivalent formulations |
| Gilmer (2022) | primary theorem/abstract checked | first dimension-free constant |
| Sawin (2022) | primary preprint checked | golden-ratio improvement and barrier |
| Yu and Cambie (2022) | primary preprints checked | computable dependent-coupling improvement |
| Alweiss--Huang--Sellke (2024) | published primary source checked | explicit golden-ratio bound |
| Liu (2023) | primary preprint checked | conditional coupling; numerical-hypothesis boundary retained |
| Das--Wu (2024) | primary preprint checked | frequency-profile results |
| Lu--Raz (2024) | primary preprint checked | Reimer-condition counterexamples |
| Bouchard (2025) | primary preprint checked | lattice minimal-counterexample conditions |
| Hachimori--Kashiwabara (2025) | primary preprint checked | ideal-family result with Lean 4 claim |
| van der Hout--Roos (2026) | published abstract checked | experimental results and explicit open status |
| Colbert (2025/2026) | published abstract checked | generalized/infinite chain-condition context |
| DeFranco (2026) | primary preprint checked | Boolean-polynomial fixed-parameter equivalence |
| 2026 complete-proof claims | not independently audited | `NEEDS_AUDIT`; no status change |

## Programme terrain

Imported with stable boundaries:

- `UC-WP02` formal definitions and local lemmas;
- exact independent replay for universes `n <= 4`;
- lattice spine through `UC-WP05-L016`;
- hybrid package claim `UC-WP05-C015`.

## Non-equivalences and scope controls

The following do not by themselves prove the canonical statement:

- intersection-closed, lattice, graph, Horn, or ideal-family results without a complete correspondence;
- average set size;
- a positive constant below one half;
- bounded universe or family-size verification;
- necessary conditions for a minimum counterexample;
- generalized or infinite analogues;
- experimental stronger conjectures;
- posted proof claims without independent audit.

## Current disposition

The monograph is source-locked. The public documentary collection remains unchanged until UC-DOC-WP01 supplies the web edition and edition record.
