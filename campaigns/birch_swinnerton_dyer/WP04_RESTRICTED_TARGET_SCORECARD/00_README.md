# BSD-WP04 — Restricted theorem target scorecard

## Status

- Campaign: `BSD-001`
- Work package: `BSD-WP04`
- Tracker: `MATH-PROGRAMME#66`
- State: `REVIEW_READY_SELECTED_TARGET_BSD-R2-A1`
- Selected target: `BSD-R2-A1`
- Selected-target status: `SELECTED_RESEARCH_TARGET_UNPROVED`
- Inputs: Referee-promoted WP01, WP02, and WP03
- Mechanism generation: closed
- Novelty claims: closed

WP04 selects one theorem-grade restricted target. Selection means that the statement is precise enough to organize later source reconstruction, proof obligations, and falsification. It does not assert truth, novelty, or progress on universal BSD.

## Selected statement

Let \(E/\mathbb Q\) be a semistable elliptic curve of odd conductor \(N\). Assume:

1. \(E\) has good ordinary reduction at \(2\);
2. the mod-\(2\) representation \(E[2]\) is irreducible;
3. the complete Hasse–Weil \(L\)-function satisfies \(\operatorname{ord}_{s=1}L(E,s)=1\).

Using the period, regulator, Tamagawa, torsion, and complete-\(L\) normalization fixed by WP00, prove or disprove

\[
\operatorname{ord}_2\!\left(\frac{L'(E,1)}{\Omega_E\,\operatorname{Reg}_E}\right)
=
\operatorname{ord}_2\!\left(\frac{\#\Sha(E/\mathbb Q)\prod_{\ell\mid N}c_\ell}{\#E(\mathbb Q)_{\mathrm{tors}}^2}\right).
\]

Gross–Zagier–Kolyvagin supplies rank one and finiteness of \(\Sha\) from the analytic-rank-one hypothesis. The selected obligation is only the exact \(2\)-primary valuation identity.

## Why this target was selected

The current theorem frontier is broad for odd primes:

- good-reduction rank-one \(p\)-parts are established in the semistable, irreducible setting;
- multiplicative primes \(p>3\) are also covered;
- newer good-ordinary and Eisenstein work enlarges the odd-prime terrain;
- explicit \(2\)-part results exist for special quadratic-twist families.

The prime \(2\) remains excluded from the general odd-prime Iwasawa interfaces. `BSD-R2-A1` isolates that exclusion in a finite-level statement with an explicit curve class, fixed normalization, no finite-data premise, and no hidden height-nondegeneracy assumption.

## Candidate dispositions

| Candidate | Adjusted score | Disposition |
|---|---:|---|
| `BSD-R2-A1` rank-one \(2\)-part | 36 | selected, unproved |
| `BSD-R2-A0` rank-zero \(2\)-part | 35 | retained fallback |
| `BSD-PC2-1` soft \(2\)-converse | 29 | not selected |
| `BSD-ADD-1` additive-prime \(p\)-part | 22 | formulation debt |
| `BSD-HR2-1` rank-two height bridge | 23 | rejected for hidden nondegeneracy |

The unrestricted rank-one converse and the multiplicative odd-prime \(p\)-part were retired before scoring because current primary sources place them in theorem terrain.

## Adversarial boundary

The target must survive WP01 fixtures for one-prime-to-global promotion, odd-prime-to-\(2\) local-theory transfer, Euler-factor drift, period and isogeny drift, hidden height nondegeneracy, Selmer local-condition drift, and circular use of BSD.

Passing the scorecard is not evidence that `BSD-R2-A1` is true.

## Replay

```bash
python campaigns/birch_swinnerton_dyer/WP04_RESTRICTED_TARGET_SCORECARD/replay.py
```

The replay validates the source delta, score arithmetic, exactly-one selection, composable imports, WP01 gates, proof-obligation DAG, and closed downstream gates.

## Current decision

`BSD-R2-A1` is selected provisionally pending independent Referee reconstruction. It remains unproved. `BSD-WP05`, target-specific source and interface reconstruction, is next eligible only after promotion and separate authorization. Mechanism generation remains closed.
