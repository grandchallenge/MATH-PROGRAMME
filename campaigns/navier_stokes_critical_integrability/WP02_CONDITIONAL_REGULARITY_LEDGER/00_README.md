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

It distinguishes:

- imported historical sources;
- the audited modern operational theorem interface;
- calculations reconstructed in the package;
- one-way programme implications;
- unresolved historical, reverse-correspondence, and data-class bridges.

It does not provide the missing universal estimate.

## Canonical theorem ledger

| ID | Statement | Status | Source route |
|---|---|---|---|
| `CR-000` | whole-space domain, zero forcing, full rapid-decay data class, time-first mixed-norm convention | checked | Fefferman official statement |
| `CR-001` | global Leray–Hopf weak existence and energy inequality | operationally audited | Ożański–Pooley; Leray historical concordance pending |
| `CR-002` | `\dot H^1(\mathbb R^3)\hookrightarrow L^6(\mathbb R^3)` | checked standard lemma | continuum analysis |
| `CR-003` | energy gives `u\in L^2_tL^6_x` | checked consequence | `CR-001` + `CR-002` |
| `CR-004` | LPS uniqueness/strongness at `(time,space)=(4,6)` | operationally audited | historical provenance plus explicit modern statement |
| `CR-005` | exact `H^1` differential inequality | independently checked reconstruction | strong-level calculation |
| `CR-006` | weak–strong integrated difference inequality and Grönwall estimate | independently checked reconstruction | weak energy inequality + strong equality + cross testing |
| `CR-007` | finite maximal strong time forces divergence of `I_{T_*}` | checked operational bridge | `CR-005` + local restart theory |
| `CR-008` | critical integrability implies regularity and uniqueness for campaign data | audited conditional consequence | `CR-004` + `CR-006` |
| `CR-009` | universal full-data critical integrability is sufficient for Fefferman statement (A) | checked one-way bridge | weak existence + LPS + continuation + classical smooth bootstrap |
| `CR-010` | reverse correspondence from Fefferman statement (A) | pending | finite-interval mixed-norm and every-solution identification bridge required |
| `CR-011` | compact-support lane remains restricted | checked boundary | strict data-class inclusion |

## Critical nonlinear estimate

For a smooth or sufficiently strong solution, testing by `-\Delta u` gives

```math
\frac12\frac d{dt}\|\nabla u\|_2^2
+\nu\|\Delta u\|_2^2
=-\int (u\cdot\nabla)u\cdot\Delta u\,dx.
```

The nonlinear term satisfies

```math
\left|\int (u\cdot\nabla)u\cdot\Delta u\right|
\le \|u\|_6\|\nabla u\|_3\|\Delta u\|_2
```

and

```math
\|\nabla u\|_3
\le C\|\nabla u\|_2^{1/2}\|\Delta u\|_2^{1/2}.
```

Young's inequality with exponents `4/3` and `4` yields

```math
\frac d{dt}\|\nabla u\|_2^2
+\nu\|\Delta u\|_2^2
\le C\nu^{-3}\|u\|_6^4\|\nabla u\|_2^2.
```

The exponent `4` and viscosity power `-3` have been independently verified. The calculation remains restricted to a regularity level at which testing and integrations by parts are justified.

## Weak–strong uniqueness estimate

Let `u` be strong, let `v` be Leray–Hopf with the same datum, and set `w=v-u`.

The pointwise differential equality commonly displayed for `w` is a formal smooth-pair identity. The rigorous weak–strong argument uses the weak energy inequality, the strong energy equality, admissible time regularization, and the two weak formulations to obtain

```math
\frac12\|w(t)\|_2^2
+\nu\int_0^t\|\nabla w(s)\|_2^2ds
\le
\int_0^t\left|\int (w\cdot\nabla)w\cdot u\,dx\right|ds.
```

The nonlinear term obeys

```math
\left|\int(w\cdot\nabla)w\cdot u\right|
\le \|u\|_6\|w\|_3\|\nabla w\|_2
\le C\|u\|_6\|w\|_2^{1/2}\|\nabla w\|_2^{3/2}.
```

Young and Grönwall give the integrated or distributional inequality

```math
\frac d{dt}\|w\|_2^2
+\nu\|\nabla w\|_2^2
\le C\nu^{-3}\|u\|_6^4\|w\|_2^2.
```

Thus `u\in L^4_tL^6_x` makes the Grönwall coefficient integrable and identifies every Leray–Hopf solution with the strong solution on the interval.

This clarification is authoritative for the programme package: the formal equality is never an unconditional Leray–Hopf identity.

## Maximal-time continuation

If the maximal `H^1` strong solution has finite critical integral up to `T_*`, the `H^1` estimate gives a uniform gradient bound. Together with the energy estimate, this gives a uniform `H^1` bound. The adopted local theory supplies a restart lifespan depending only on this bound and `\nu`; restarting at times approaching `T_*` contradicts maximality. Therefore

```math
T_*<\infty
\quad\Longrightarrow\quad
\int_0^{T_*}\|u(t)\|_6^4dt=\infty.
```

The exact historical theorem number and lifespan formula remain nonblocking provenance debt.

## One-way correspondence

The promoted bridge is:

```text
full-data universal critical integrability
  -> global Leray weak existence
  -> critical control on every finite interval
  -> operational LPS strongness and weak–strong uniqueness
  -> no finite maximal strong time
  -> classical smooth continuation and pressure recovery for smooth rapid-decay data
  -> inherited energy bound
  -> Fefferman statement (A).
```

The approved wording is **sufficient for statement (A)**. Bidirectional equivalence remains unpromoted until `CR-010` is discharged.

## Source states

| Source ID | Operational use | Audit state |
|---|---|---|
| `NS-CI-SRC-CLAY-FEFFERMAN` | official data and solution class | audited |
| `NS-CI-SRC-LERAY-1934` | historical weak/strong foundation | identified; exact concordance pending |
| `NS-CI-SRC-OZANSKI-POOLEY` | local strong theory, global weak existence, weak–strong uniqueness | audited at statement level |
| `NS-CI-SRC-PRODI-1959` | original uniqueness exponent law | audited with modern-formulation gap |
| `NS-CI-SRC-SERRIN-1962` | historical regularity provenance | theorem body pending |
| `NS-CI-SRC-LADYZHENSKAYA-1967` | historical smoothness/uniqueness provenance | translation pending |
| `NS-CI-SRC-OPERATIONAL-LPS-2024` | explicit whole-space Leray–Hopf `(4,6)` interface | audited |

All source IDs in the machine ledger resolve to the MATHFORGE source ledger, and audit-state distinctions are preserved.

## Claim boundary

WP02 does not claim:

- universal finiteness of `I_T`;
- global regularity as a new theorem;
- novelty of the LPS criterion or continuation estimate;
- unconditional validity of the `-\Delta u` test at Leray–Hopf regularity;
- an unconditional pointwise difference-energy equality for a weak solution;
- completed historical source extraction;
- bidirectional equivalence with the official Clay statement;
- full-data coverage from a compact-support theorem.

## Interaction with WP01

WP01 protects this ledger from invalid use:

- `FP-001` and `FP-002` block an energy-only upgrade;
- `FP-004` blocks circular Grönwall closure;
- `FP-005` and `FP-006` enforce the strong-level test boundary;
- `FP-009` enforces the full data class;
- `FP-012` enforces time/space exponent order;
- `FP-013` prevents interior-to-global theorem drift;
- `FP-014` enforces the universal weak-solution quantifier.

## Cross-document integration

Checked against:

- WP00's problem statement, source states, theorem spine, and one-way correspondence decision;
- the promoted WP01 false-proof atlas and semantic review;
- the MATHFORGE source ledger;
- MATHCERT's provenance-bearing imported-interface policy;
- the canonical tracker `MATH-PROGRAMME#55`.

No blocking conflict remains.

## Remaining nonblocking debt

- exact Leray theorem concordance;
- original Serrin theorem-body extraction;
- Ladyzhenskaya mathematical translation;
- exact local-lifespan theorem number;
- explicit source location for the final smooth-bootstrap and pressure-recovery interface;
- reverse correspondence `CR-010`;
- theorem-prover certification of the scaling and implication substrate.

These debts remain visible and do not alter the conditional theorem chain.

## Acceptance record

- [x] Human-readable theorem chain supplied.
- [x] Machine-readable theorem ledger supplied.
- [x] Source IDs reconciled with MATHFORGE.
- [x] Exact `H^1` estimate independently checked.
- [x] Weak–strong estimate independently checked with the formal/integrated distinction recorded.
- [x] Local restart logic independently checked.
- [x] One-way Clay implication isolated.
- [x] Reverse correspondence and compact-support extension remain explicit debt.
- [x] Formalist boundary reviewed.
- [x] Amanuensis WP00/WP01/WP02 consistency review complete.
- [x] Referee promotion approved.
- [x] Provider Solve CI passed in workflow run `30058471721`.
- [x] Programme policy CI passed in workflow run `30058245792`.

## Promotion decision

WP02 is the canonical source-normalized conditional-regularity ledger for `NS-CI-001`.

This promotion certifies the organization and reconstruction of classical conditional analysis only. It does not supply the open critical estimate or open mechanism generation automatically.

## Next executable step

Maintain WP02 as the authoritative theorem interface consumed by future route proposals. Any future mechanism must identify the exact inequality or imported theorem interface it changes, and must pass WP01 before receiving a separate mechanism-generation gate.