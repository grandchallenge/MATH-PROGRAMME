# BSD-WP02 — Composition and trust rules

A theorem record may enter a proof graph only when `composition_state` is compatible with the intended conclusion.

1. `COMPOSABLE` and `COMPOSABLE_STANDARD` records may be used only within their stated domain.
2. `COMPOSABLE_RESTRICTED*` records retain every curve, prime, reduction, residual, rank, Selmer, and normalization hypothesis.
3. `FAMILY_ONLY`, `FINITE_DATABASE_ONLY`, and `INDIVIDUAL_ONLY` records cannot discharge `ALL_ELLIPTIC_CURVES_OVER_Q`.
4. `NONCOMPOSABLE_UNTIL_INSTANTIATED` records are source pointers, not theorem interfaces. A downstream artifact must extract the exact theorem and create a new record.
5. A `p`-adic theorem cannot discharge a complex order statement without a named converse or comparison record.
6. A one-prime valuation identity cannot discharge exact equality of the complete leading coefficient.
7. The low-rank interface `BSD-T-060` is operationally composable for its stated conclusion. It does not provide a higher-rank mechanism or the full leading coefficient.
8. Any change of complete or imprimitive Euler factors, period, differential, isogeny representative, Selmer local conditions, or exceptional-zero convention requires a conversion record.
9. A source abstract may establish scope for the ledger but cannot support a proof step whose internal hypotheses are not represented.
10. The theorem label `Gross–Zagier`, `Kolyvagin`, `Kato`, or `main conjecture` is never itself a valid proof interface.

The ledger is intentionally incomplete as a survey of all BSD literature. It is complete for the WP00 theorem-spine interfaces admitted at this stage.

## Hypothesis matrix

| ID | Domain | Direction | Rank range | Prime/reduction profile | Composition state |
|---|---|---|---|---|---|
| `BSD-T-010` | all `E/Q` | structural | all | none | standard |
| `BSD-T-020` | all `E/Q` | arithmetic to automorphic | all | all reduction types | composable |
| `BSD-T-040` | all `E/Q` | cohomological | all | any `p` | standard |
| `BSD-T-050` | all `E/Q` | algebraic consequence | all | any `p` | composable |
| `BSD-T-060` | all `E/Q` | analytic to arithmetic | `0,1` | final statement prime-free | operational interface |
| `BSD-T-070` | all `E/Q` | parity | parity only | every `p` | parity only |
| `BSD-T-080` | semistable `E/Q` | arithmetic to analytic | rank one | stated multiplicative-reduction alternatives | restricted |
| `BSD-T-085` | CM `E/Q` | Selmer to analytic | rank zero | source prime profile | restricted |
| `BSD-T-090` | semistable `E/Q` | analytic to `p`-part | analytic rank one | good `p`, irreducibility and exceptional `p=3` condition | restricted `p`-part |
| `BSD-T-095` | restricted CM `E/F` | complete formula | analytic rank zero | source class | restricted complete theorem |
| `BSD-T-100` | specified curve | certification | `0,1` | curve-dependent | individual only |
| `BSD-T-110` | height-ordered family | distributional | rank zero slice | family profile | family only |
| `BSD-T-120` | naive-height family | distributional | rank one slice | family profile | family only |
| `BSD-T-130` | finite conductor range | computational certificate | `0,1` | finite database | finite database only |
| `BSD-T-140` | modular forms | Euler-system interface | source-specific | source-specific | noncomposable until instantiated |
| `BSD-T-150` | non-CM family terrain | zeta-element interface | `0,1` applications | branch-specific | noncomposable until instantiated |
