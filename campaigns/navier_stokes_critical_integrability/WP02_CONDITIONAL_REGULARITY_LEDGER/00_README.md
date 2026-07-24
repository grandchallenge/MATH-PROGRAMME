# NS-CI-WP02 — Source-normalized conditional-regularity ledger

## Metadata

- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP02`
- Parent tracker: `MATH-PROGRAMME#55`
- MATHSOLVE tracker: `grandchallenge/MATHSOLVE#20`
- Provider PR: `grandchallenge/MATHSOLVE#21`
- Provider artifacts:
  - `grandchallenge/MATHSOLVE:work_packages/NS_CI_WP02_CONDITIONAL_REGULARITY_LEDGER.md`
  - `grandchallenge/MATHSOLVE:work_packages/ns_ci_wp02_theorem_ledger.yaml`
  - `grandchallenge/MATHSOLVE:work_packages/NS_CI_WP02_ADVERSARIAL_SEMANTIC_REVIEW.md`
- Result class: source-normalized classical conditional analysis
- Promotion state: `REFEREE_PROMOTED_CONDITIONAL_REGULARITY_LEDGER`
- Promotion date: 2026-07-23

## Purpose and claim boundary

WP02 preserves the theorem chain that consumes

```math
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt.
```

It distinguishes historical sources, an audited operational theorem interface, reconstructed calculations, one-way programme implications, and unresolved provenance or correspondence debt. It does not prove universal critical integrability, global regularity, novelty, or bidirectional equivalence.

## Ledger state

| ID | Statement | Status |
|---|---|---|
| `CR-000` | whole-space problem and time-first `(4,6)` convention | checked |
| `CR-001` | global Leray–Hopf existence and energy inequality | operationally audited |
| `CR-002` | whole-space `\dot H^1\to L^6` | checked |
| `CR-003` | energy gives `L^2_tL^6_x` | checked consequence |
| `CR-004` | operational LPS theorem at `(4,6)` | audited imported theorem |
| `CR-005` | strong-level `H^1` inequality | independently checked |
| `CR-006` | integrated weak–strong inequality | independently checked |
| `CR-007` | critical-integral continuation criterion | checked operational bridge |
| `CR-008` | conditional regularity and uniqueness | audited consequence |
| `CR-009` | universal full-data critical integrability implies Fefferman (A) | checked one-way bridge |
| `CR-010` | reverse correspondence | pending |
| `CR-011` | compact-support restricted lane | checked boundary |

## Analytic core

At strong regularity,

```math
\frac d{dt}\|\nabla u\|_2^2
+\nu\|\Delta u\|_2^2
\le C\nu^{-3}\|u\|_6^4\|\nabla u\|_2^2.
```

The coefficient follows from Hölder `(6,3,2)`, Gagliardo–Nirenberg, and Young exponents `4/3` and `4`. The `-\Delta u` test is not asserted unconditionally for Leray–Hopf solutions.

For weak–strong uniqueness, the rigorous starting point is the integrated inequality

```math
\frac12\|w(t)\|_2^2
+\nu\int_0^t\|\nabla w\|_2^2
\le \int_0^t\left|\int (w\cdot\nabla)w\cdot u\right|ds,
```

not the formal smooth-pair differential equality. This yields

```math
\frac d{dt}\|w\|_2^2
+\nu\|\nabla w\|_2^2
\le C\nu^{-3}\|u\|_6^4\|w\|_2^2
```

in integrated, distributional, or justified strong form.

A finite critical integral up to a maximal strong time gives a uniform `H^1` bound and a uniform local restart interval, so

```math
T_*<\infty\Longrightarrow\int_0^{T_*}\|u(t)\|_6^4dt=\infty.
```

## Correspondence boundary

The promoted chain is

```text
universal full-data critical integrability
  -> global weak existence
  -> conditional strongness and weak–strong uniqueness
  -> no finite maximal strong time
  -> classical smooth continuation and pressure recovery
  -> Fefferman statement (A).
```

The approved wording is **sufficient for statement (A)**. `CR-010` remains pending before any equivalence claim.

## Cross-document integration

Source IDs resolve to the MATHFORGE source ledger. WP01 fixtures protect the energy gap, circularity, test admissibility, data class, exponent order, theorem scope, and universal quantifier. The combined Agent Council artifact ledger records WP00, WP01, and WP02.

Merge the WP01 governance PR before WP02. The WP02 branch carries the combined ledger state so both promoted records survive the ordered integration.

## Nonblocking debt

Historical Leray/Serrin/Ladyzhenskaya extraction, exact local-lifespan and smooth-bootstrap source locations, reverse correspondence `CR-010`, and theorem-prover certification remain explicit and nonblocking for this ledger.

## Promotion decision

WP02 is Referee-promoted as the canonical source-normalized conditional-regularity ledger. This promotion does not open mechanism generation automatically; any mechanism requires a separate governed gate.