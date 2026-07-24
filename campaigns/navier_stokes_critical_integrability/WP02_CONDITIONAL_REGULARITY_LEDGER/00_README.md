# NS-CI-WP02 — Source-normalized conditional-regularity ledger

## Metadata

- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP02`
- Parent tracker: `MATH-PROGRAMME#55`
- MATHSOLVE tracker: `grandchallenge/MATHSOLVE#20`
- Provider PR: `grandchallenge/MATHSOLVE#21`
- Primary provider artifacts:
  - `grandchallenge/MATHSOLVE:work_packages/NS_CI_WP02_CONDITIONAL_REGULARITY_LEDGER.md`
  - `grandchallenge/MATHSOLVE:work_packages/ns_ci_wp02_theorem_ledger.yaml`
  - `grandchallenge/MATHSOLVE:work_packages/NS_CI_WP02_ADVERSARIAL_SEMANTIC_REVIEW.md`
- Result class: source-normalized classical conditional analysis
- Promotion state: `REFEREE_PROMOTED_CONDITIONAL_REGULARITY_LEDGER`
- Promotion date: 2026-07-23

## Purpose

WP02 preserves the theorem chain that consumes the critical norm

```math
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt.
```

It distinguishes imported historical sources, the audited modern operational theorem interface, calculations reconstructed in the package, one-way programme implications, and unresolved provenance or correspondence debt. It does not provide the missing universal estimate.

## Canonical theorem ledger

| ID | Statement | Status | Source route |
|---|---|---|---|
| `CR-000` | whole-space domain, zero forcing, full rapid-decay data class, time-first mixed-norm convention | checked | Fefferman official statement |
| `CR-001` | global Leray–Hopf weak existence and energy inequality | operationally audited | Ożański–Pooley; Leray concordance pending |
| `CR-002` | `\dot H^1(\mathbb R^3)\hookrightarrow L^6(\mathbb R^3)` | checked standard lemma | continuum analysis |
| `CR-003` | energy gives `u\in L^2_tL^6_x` | checked consequence | `CR-001` + `CR-002` |
| `CR-004` | LPS uniqueness/strongness at `(time,space)=(4,6)` | operationally audited | historical provenance plus explicit modern statement |
| `CR-005` | exact `H^1` differential inequality | independently checked reconstruction | strong-level calculation |
| `CR-006` | rigorous integrated weak–strong inequality and Grönwall estimate | independently checked reconstruction | weak energy inequality + strong equality + cross testing |
| `CR-007` | finite maximal strong time forces divergence of `I_{T_*}` | checked operational bridge | `CR-005` + local restart theory |
| `CR-008` | critical integrability implies regularity and uniqueness for campaign data | audited conditional consequence | `CR-004` + `CR-006` |
| `CR-009` | universal full-data critical integrability is sufficient for Fefferman statement (A) | checked one-way bridge | weak existence + LPS + continuation + classical smooth bootstrap |
| `CR-010` | reverse correspondence from Fefferman statement (A) | pending | finite-interval mixed-norm and every-solution identification bridge required |
| `CR-011` | compact-support lane remains restricted | checked boundary | strict data-class inclusion |

## Critical nonlinear estimate

For a smooth or sufficiently strong solution,

```math
\frac d{dt}\|\nabla u\|_2^2
+\nu\|\Delta u\|_2^2
\le C\nu^{-3}\|u\|_6^4\|\nabla u\|_2^2.
```

The exponent `4` and viscosity power `-3` follow from Hölder `(6,3,2)`, the three-dimensional Gagliardo–Nirenberg estimate, and Young exponents `4/3` and `4`. Testing by `-\Delta u` remains restricted to a regularity level where it is admissible.

## Weak–strong uniqueness semantics

For a strong solution `u`, Leray–Hopf solution `v`, and `w=v-u`, the formal smooth-pair differential equality is not the rigorous weak starting point. The authoritative route combines the weak energy inequality, strong energy equality, admissible time regularization, and cross-testing to obtain

```math
\frac12\|w(t)\|_2^2
+\nu\int_0^t\|\nabla w(s)\|_2^2ds
\le
\int_0^t\left|\int (w\cdot\nabla)w\cdot u\,dx\right|ds.
```

Hölder, Gagliardo–Nirenberg, Young, and Grönwall then give the distributional or justified differential estimate

```math
\frac d{dt}\|w\|_2^2
+\nu\|\nabla w\|_2^2
\le C\nu^{-3}\|u\|_6^4\|w\|_2^2,
```

so `u\in L^4_tL^6_x` identifies every Leray–Hopf solution with the strong solution on the interval.

## Maximal-time continuation

A finite critical integral up to a maximal time gives a uniform gradient bound through `CR-005`; the energy inequality supplies the remaining `L^2` component of a uniform `H^1` bound. The adopted local theory then restarts the solution with a lifespan bounded below uniformly, yielding

```math
T_*<\infty
\quad\Longrightarrow\quad
\int_0^{T_*}\|u(t)\|_6^4dt=\infty.
```

## One-way correspondence

```text
full-data universal critical integrability
  -> global Leray weak existence
  -> operational LPS strongness and weak–strong uniqueness
  -> no finite maximal strong time
  -> classical smooth continuation and pressure recovery
  -> inherited energy bound
  -> Fefferman statement (A).
```

The approved wording is **sufficient for statement (A)**. Bidirectional equivalence remains unpromoted until `CR-010` is discharged.

## Claim boundary

WP02 does not claim universal finiteness, global regularity as a new theorem, novelty, unconditional `-\Delta u` testing, an unconditional weak differential identity, completed historical extraction, bidirectional equivalence, or full-data coverage from compact-support data.

## Cross-document integration

The ledger has been checked against WP00, the promoted WP01 atlas, the MATHFORGE source ledger, MATHCERT's imported-interface policy, and the canonical tracker. The programme integration order is WP01 governance PR before WP02 governance PR; the combined artifact ledger on the WP02 branch preserves both promoted records.

## Remaining nonblocking debt

- exact Leray theorem concordance;
- original Serrin theorem-body extraction;
- Ladyzhenskaya mathematical translation;
- exact local-lifespan theorem number;
- exact source location for final smooth-bootstrap and pressure recovery;
- reverse correspondence `CR-010`;
- theorem-prover certification of scaling and implication structure.

## Acceptance record

- [x] Source IDs reconciled with MATHFORGE.
- [x] `CR-005`, `CR-006`, and `CR-007` independently checked.
- [x] Formal smooth-pair and rigorous integrated weak–strong statements separated.
- [x] One-way correspondence isolated; reverse bridge remains explicit.
- [x] Formalist and Amanuensis reviews complete.
- [x] Referee promotion approved.
- [x] Provider and programme CI required green on promoted heads.

## Promotion decision

WP02 is the canonical source-normalized conditional-regularity ledger for `NS-CI-001`. Promotion certifies the organization and reconstruction of classical conditional analysis only; it does not supply the open critical estimate or open mechanism generation automatically.
