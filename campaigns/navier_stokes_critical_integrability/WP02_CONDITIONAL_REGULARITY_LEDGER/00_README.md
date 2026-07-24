# NS-CI-WP02 — Source-normalized conditional-regularity ledger

## Metadata

- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP02`
- Parent tracker: `MATH-PROGRAMME#55`
- MATHSOLVE tracker: `grandchallenge/MATHSOLVE#20`
- Primary provider artifacts:
  - `grandchallenge/MATHSOLVE:work_packages/NS_CI_WP02_CONDITIONAL_REGULARITY_LEDGER.md`
  - `grandchallenge/MATHSOLVE:work_packages/ns_ci_wp02_theorem_ledger.yaml`
- Result class: source-normalized classical conditional analysis
- Promotion state: draft; independent source and derivation review pending

## Purpose

WP02 preserves the complete theorem chain that consumes the critical norm

```math
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt.
```

It distinguishes:

- imported historical sources;
- the audited modern operational theorem interface;
- calculations reconstructed in the package;
- one-way programme implications;
- unresolved reverse correspondence and data-class bridges.

It does not provide the missing universal estimate.

## Canonical theorem ledger

| ID | Statement | Status | Source route |
|---|---|---|---|
| `CR-000` | whole-space domain, zero forcing, full rapid-decay data class, time-first mixed-norm convention | checked | Fefferman official statement |
| `CR-001` | global Leray–Hopf weak existence and energy inequality | operationally audited | Ożański–Pooley; Leray historical concordance pending |
| `CR-002` | `\dot H^1(\mathbb R^3)\hookrightarrow L^6(\mathbb R^3)` | checked standard lemma | continuum analysis |
| `CR-003` | energy gives `u\in L^2_tL^6_x` | checked consequence | `CR-001` + `CR-002` |
| `CR-004` | LPS uniqueness/strongness at `(time,space)=(4,6)` | operationally audited | Prodi/Serrin/Ladyzhenskaya provenance plus explicit modern statement |
| `CR-005` | exact `H^1` differential inequality | checked reconstruction | strong-level calculation |
| `CR-006` | weak–strong difference inequality | checked reconstruction | difference equation + Grönwall |
| `CR-007` | finite maximal strong time forces divergence of `I_{T_*}` | checked operational bridge | `CR-005` + local restart theory |
| `CR-008` | critical integrability implies regularity and uniqueness for campaign data | audited conditional consequence | `CR-004` + `CR-006` |
| `CR-009` | universal full-data critical integrability is sufficient for Fefferman statement (A) | checked one-way bridge | weak existence + LPS + continuation + bootstrap |
| `CR-010` | reverse correspondence from Fefferman statement (A) | pending | source-normalized finite-interval mixed-norm and uniqueness bridge required |
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

Young's inequality with exponents `4/3` and `4` therefore yields

```math
\frac d{dt}\|\nabla u\|_2^2
+\nu\|\Delta u\|_2^2
\le C\nu^{-3}\|u\|_6^4\|\nabla u\|_2^2.
```

The exponent `4` is forced by this absorption step.

## Weak–strong uniqueness estimate

For `w=v-u`, where `u` is strong and `v` is Leray–Hopf with the same datum,

```math
\frac12\frac d{dt}\|w\|_2^2
+\nu\|\nabla w\|_2^2
=-\int(w\cdot\nabla)u\cdot w\,dx.
```

After incompressible integration by parts,

```math
\left|\int(w\cdot\nabla)u\cdot w\right|
\le \|u\|_6\|w\|_3\|\nabla w\|_2,
```

and Gagliardo–Nirenberg plus Young gives

```math
\frac d{dt}\|w\|_2^2
+\nu\|\nabla w\|_2^2
\le C\nu^{-3}\|u\|_6^4\|w\|_2^2.
```

Thus `u\in L^4_tL^6_x` makes the Grönwall coefficient integrable and identifies all Leray–Hopf solutions with the strong solution on the interval.

## One-way correspondence

The promoted bridge is:

```text
full-data universal critical integrability
  -> global Leray weak solution has L4_tL6_x on each finite interval
  -> operational LPS strongness and uniqueness
  -> no finite maximal strong time
  -> smooth whole-space solution with inherited energy bound
  -> Fefferman statement (A).
```

The wording is **sufficient for statement (A)**. Bidirectional equivalence remains unpromoted until `CR-010` is discharged.

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

## Claim boundary

WP02 does not claim:

- universal finiteness of `I_T`;
- global regularity as a new theorem;
- novelty of the LPS criterion or continuation estimate;
- unconditional validity of the `-\Delta u` test at Leray–Hopf regularity;
- completed historical source extraction;
- bidirectional equivalence with the official Clay statement;
- full-data coverage from a compact-support theorem.

## Interaction with WP01

WP01 protects this ledger from invalid use:

- `FP-004` blocks circular Grönwall closure;
- `FP-005` and `FP-006` enforce the strong-level test boundary;
- `FP-009` enforces the full data class;
- `FP-012` enforces time/space exponent order;
- `FP-013` prevents interior-to-global theorem drift;
- `FP-014` enforces the universal weak-solution quantifier.

## Acceptance gate

- [x] Human-readable theorem chain supplied.
- [x] Machine-readable theorem ledger supplied by MATHSOLVE.
- [x] Exact `H^1` estimate supplied.
- [x] Exact weak–strong difference estimate supplied.
- [x] One-way Clay implication isolated.
- [x] Reverse correspondence and compact-support extension remain explicit debt.
- [ ] Prospector verifies all source IDs and theorem states against the MATHFORGE ledger.
- [ ] Verifier independently checks every exponent and Young inequality.
- [ ] Formalist checks the proposed theorem-interface boundaries.
- [ ] Amanuensis checks WP00/WP01/WP02 consistency.
- [ ] Referee approves promotion.

## Next executable step

Perform an independent line-by-line verification of `CR-005` and `CR-006`, then add source-resolving checks that every source ID in the machine ledger exists in the MATHFORGE source ledger. This remains analytic and governance work; mechanism generation is not opened by WP02 alone.