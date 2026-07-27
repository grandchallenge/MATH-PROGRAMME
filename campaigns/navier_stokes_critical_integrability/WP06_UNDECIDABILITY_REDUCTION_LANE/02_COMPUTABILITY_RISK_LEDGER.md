# NS-CI-WP06 Computability Risk Ledger

| Risk ID | Hazard | Likelihood | Programme impact | Control | Status |
|---|---|---:|---:|---|---|
| `NS-U-R01` | Euler universality is silently transferred to viscous Navier–Stokes | High | High | Equation-fidelity gate `U002` | Active |
| `NS-U-R02` | One-way simulation is reported as an iff reduction | High | High | Separate `U007` and `U008` proofs | Active |
| `NS-U-R03` | Infinite precision acts as an oracle | High | High | Robust-clock and perturbation audit `U005` | Active |
| `NS-U-R04` | A modified or averaged equation is described as the true equation | Medium | Critical | Exact operator identity and source-normalized equation | Active |
| `NS-U-R05` | Undecidability of an instance family is conflated with independence of the universal Clay statement | High | Critical | Metatheorem requirement `U010`; Formalist review | Active |
| `NS-U-R06` | Numerical nontermination is treated as mathematical non-halting | High | High | Finite-step fixture labels; no continuum promotion | Active |
| `NS-U-R07` | Viscous damping destroys the encoded state | High | High | Quantitative persistence proof `U006` | Open |
| `NS-U-R08` | Halting causes a benign observable event rather than singularity | Medium | High | Exact event taxonomy and implication chain | Open |
| `NS-U-R09` | Singular behaviour occurs for both halting and non-halting encodings | Medium | Critical | Non-halting safety theorem `U008` | Open |
| `NS-U-R10` | Speculative work diverts resources from WP01/WP02 | Medium | Medium | Non-blocking budget and explicit mainline priority | Controlled |
| `NS-U-R11` | Bounded software behaviour is described as a PDE simulation | High | Critical | Repository-test classification and explicit interface-only labels | Active |
| `NS-U-R12` | A test failure or numerical overflow is misread as evidence of singularity | Medium | Critical | Numerical-contract tests and non-probative review boundary | Active |

## Operating rule

No NS-CI-WP06 artifact may change a result status in the critical-integrability campaign unless it independently passes the ordinary theorem-spine, source, correspondence, and certification gates. A passing software test establishes only deterministic behaviour of the bounded fixture under its declared inputs.
