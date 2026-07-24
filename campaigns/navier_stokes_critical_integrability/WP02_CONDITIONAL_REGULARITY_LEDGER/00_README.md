# NS-CI-WP02 — Referee-promoted conditional-regularity ledger

## Status

- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP02`
- Parent: `MATH-PROGRAMME#55`
- Provider: `grandchallenge/MATHSOLVE#21`
- State: `REFEREE_PROMOTED_CONDITIONAL_REGULARITY_LEDGER`

WP02 source-normalizes and reconstructs classical conditional analysis. It does not prove universal critical integrability, global regularity, novelty, or bidirectional equivalence.

## Ledger

`CR-000` through `CR-011` record the whole-space problem, Leray–Hopf energy interface, Sobolev consequence, operational `(4,6)` LPS theorem, strong `H^1` estimate, rigorous integrated weak–strong estimate, continuation criterion, one-way Clay implication, pending reverse bridge, and compact-support restriction.

## Analytic core

At strong regularity,

```math
\frac d{dt}\|\nabla u\|_2^2
+\nu\|\Delta u\|_2^2
\le C\nu^{-3}\|u\|_6^4\|\nabla u\|_2^2.
```

The exponent and viscosity power are independently checked. The `-\Delta u` test is not asserted unconditionally for a Leray–Hopf solution.

For a strong solution `u`, Leray–Hopf solution `v`, and `w=v-u`, the rigorous route begins from

```math
\frac12\|w(t)\|_2^2
+\nu\int_0^t\|\nabla w\|_2^2
\le \int_0^t\left|\int (w\cdot\nabla)w\cdot u\right|ds,
```

obtained from the weak energy inequality, strong energy equality, time regularization, and cross-testing. It yields

```math
\frac d{dt}\|w\|_2^2
+\nu\|\nabla w\|_2^2
\le C\nu^{-3}\|u\|_6^4\|w\|_2^2
```

in integrated, distributional, or justified strong form. The smooth-pair differential equality is formal only.

A finite critical integral up to a maximal strong time gives a uniform `H^1` bound and restart interval, hence

```math
T_*<\infty\Longrightarrow\int_0^{T_*}\|u(t)\|_6^4dt=\infty.
```

## Correspondence

The promoted statement is one-way:

```text
universal full-data critical integrability
  -> global weak existence
  -> conditional strongness and weak–strong uniqueness
  -> no finite maximal strong time
  -> classical smooth continuation and pressure recovery
  -> Fefferman statement (A).
```

The wording is **sufficient for statement (A)**. Reverse correspondence `CR-010` remains pending.

## Integration and promotion

All source IDs resolve to MATHFORGE. WP01 protects the relevant energy, circularity, admissibility, data-class, notation, scope, and quantifier boundaries. Historical theorem extraction, exact lifespan/bootstrap source locations, CR-010, and formal certification remain visible nonblocking debt.

Verifier, Adversary, Formalist, Amanuensis, and Referee reviews are complete. Merge WP01 governance before WP02; this branch carries the combined WP00/WP01/WP02 artifact ledger.
