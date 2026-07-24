# NS-CI-WP00 — Problem, source, and equivalence audit

**Audit date:** 2026-07-23  
**Campaign:** `NS-CI-001`  
**Canonical tracker:** `MATH-PROGRAMME#55`

## 1. Audit determination

The WP00 audit supports the following statements:

1. The energy inequality and the whole-space Sobolev estimate yield
   `u in L2(0,T;L6(R3))`, not the target `L4(0,T;L6(R3))`.
2. The target integral is invariant under Navier–Stokes scaling.
3. The pair `(time,space)=(4,6)` is in the classical non-endpoint Ladyzhenskaya–Prodi–Serrin range.
4. For an `H1` strong solution, finite `L4_tL6_x` control prevents finite maximal-time breakdown through an explicit Gronwall estimate.
5. The same exponent closes the weak–strong uniqueness estimate.
6. Universal critical integrability for the full rapidly decreasing data class in Fefferman's official whole-space formulation is sufficient for Clay statement (A).
7. The compactly supported initial-data class used at campaign initialization is a restricted subclass and is not alone the full official positive branch.
8. Full bidirectional equivalence is not promoted until the reverse strong-class and every-Leray–Hopf correspondence is source-normalized.

The universal estimate remains open. This audit establishes no new Navier–Stokes theorem.

## 2. Corrected canonical challenge

Fix `nu>0`. Let `u0` be a smooth divergence-free vector field on `R3` satisfying Fefferman's rapid-decay condition:

```math
|\partial_x^\alpha u_0(x)|\le C_{\alpha,K}(1+|x|)^{-K}
```

for every multi-index `alpha` and every `K`. Let `u` be a Leray–Hopf solution of the unforced three-dimensional incompressible Navier–Stokes equations with datum `u0`.

Determine whether, for every finite `T>0`,

```math
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4\,dt<\infty.
```

### Restricted compact-support lane

The same question with `u0 in C_c^infinity(R3)` is retained as `NS-CI-R-COMPACT`. Compact support implies the official rapid-decay condition, but the converse is false. A result restricted to compact support cannot be advertised as resolving the whole official data class without an additional extension theorem.

## 3. Source ledger

| ID | Source | Audited use | State | Remaining limitation |
|---|---|---|---|---|
| `SRC-CLAY` | Fefferman, official Clay problem description | Whole-space data class, positive branch, bounded energy, local-time background, weak-existence background | `AUDITED` | Does not itself state the LPS criterion |
| `SRC-LERAY` | Leray 1934 | Historical weak/strong/uniqueness foundation | `PRIMARY_IDENTIFIED` | Exact original theorem-number map pending |
| `SRC-OP` | Ożański–Pooley modern reconstruction | Local strong existence, global weak existence, weak–strong uniqueness, blow-up lower bounds | `OPERATIONALLY_AUDITED` | Historical source mapping still pending |
| `SRC-PRODI` | Prodi 1959 | Uniqueness under `L^(2p/(p-3))_t L^p_x`; includes `(4,6)` | `AUDITED_WITH_FORMULATION_GAP` | Generalized solution framework is not silently equated with modern Leray–Hopf |
| `SRC-SERRIN` | Serrin 1962 | Historical interior-regularity attribution | `METADATA_AUDITED` | Original theorem body not extracted from audited public endpoint |
| `SRC-LADY` | Ladyzhenskaya 1967 | Historical uniqueness/smoothness attribution | `FULL_TEXT_LOCATED` | Mathematical translation pending |
| `SRC-LPS-MODERN` | Explicit modern theorem statement of the classical criterion | Operational R3 Leray–Hopf interface | `AUDITED` | Secondary for historical priority |
| `SRC-STATUS` | Clay official status page | Current open status | `AUDITED_2026-07-23` | Specific claimed proofs handled only when considered |

The detailed cross-pillar ledger is in `grandchallenge/MATHFORGE`, branch `campaign/ns-ci-source-audit`.

## 4. Energy-class baseline

For a Leray–Hopf solution,

```math
\sup_{0\le t\le T}\|u(t)\|_2^2
+2\nu\int_0^T\|\nabla u(t)\|_2^2dt
\le \|u_0\|_2^2.
```

The whole-space Sobolev inequality gives

```math
\|u(t)\|_6\le C_S\|\nabla u(t)\|_2,
```

hence

```math
\int_0^T\|u(t)\|_6^2dt
\le \frac{C_S^2}{2\nu}\|u_0\|_2^2.
```

No finite-measure embedding upgrades this to fourth-power time integrability. The explicit concentrating field in `00_README.md` confirms that the full abstract energy space is not contained in `L4_tL6_x`.

## 5. Operational LPS theorem at `(4,6)`

The source-normalized operational interface is:

> Let `u` and `u_tilde` be Leray–Hopf weak solutions on `R3` with the same initial datum. If
>
> ```math
> u\in L^r(0,T;L^q(\mathbb R^3)),
> \qquad \frac2r+\frac3q=1,
> \qquad 3<q\le\infty,
> ```
>
> then the two solutions agree. If the initial datum belongs to `H1`, the controlled solution is strong through the initial time.

Taking `r=4` and `q=6` gives the campaign criterion.

### Historical qualification

Prodi's original theorem has been checked directly and contains the exponent law `2p/(p-3)`, with `p=6` giving time exponent `4`. His generalized problem and solution class require a translation bridge before being called verbatim the modern Leray–Hopf theorem. Serrin and Ladyzhenskaya remain in the historical ledger with the exact audit states above.

## 6. Quantitative strong-solution estimate

For a sufficiently regular decaying solution, test the equation against `-Delta u`:

```math
\frac12\frac d{dt}\|\nabla u\|_2^2
+\nu\|\Delta u\|_2^2
=\int (u\cdot\nabla)u\cdot\Delta u.
```

Hölder and Gagliardo–Nirenberg give

```math
\left|\int (u\cdot\nabla)u\cdot\Delta u\right|
\le C\|u\|_6\|\nabla u\|_2^{1/2}\|\Delta u\|_2^{3/2}.
```

Young's inequality yields

```math
\frac d{dt}\|\nabla u\|_2^2
+\nu\|\Delta u\|_2^2
\le C\nu^{-3}\|u\|_6^4\|\nabla u\|_2^2.
```

Therefore

```math
\|\nabla u(t)\|_2^2
\le \|\nabla u_0\|_2^2
\exp\left(C\nu^{-3}\int_0^t\|u(s)\|_6^4ds\right).
```

This identifies the precise analytic role of the target integral. It is the integrable coefficient needed to prevent the `H1` strong norm from diverging.

## 7. Weak–strong uniqueness estimate

For two solutions with the same datum, let `w=v-u`, with `u` the solution in `L4_tL6_x`. The difference energy inequality has the critical nonlinear term

```math
\left|\int (w\cdot\nabla)w\cdot u\right|
\le \|u\|_6\|w\|_3\|\nabla w\|_2.
```

Using

```math
\|w\|_3\le C\|w\|_2^{1/2}\|\nabla w\|_2^{1/2}
```

and Young's inequality gives

```math
\frac d{dt}\|w\|_2^2
\le C\nu^{-3}\|u\|_6^4\|w\|_2^2.
```

Finite `I_T(u)` and `w(0)=0` imply `w=0` by Gronwall. The rigorous weak testing and time regularization are delegated to the audited weak–strong uniqueness theorem.

## 8. Continuation bridge

Let `u` be the maximal `H1` strong solution on `[0,T_star)`. If

```math
\int_0^{T_\star}\|u(t)\|_6^4dt<\infty,
```

then Section 6 bounds the `H1` norm uniformly up to `T_star`. The local `H1` theory can be restarted from times approaching `T_star`, contradicting maximality. Thus

```math
T_\star<\infty
\implies
\int_0^{T_\star}\|u(t)\|_6^4dt=\infty.
```

This is a conditional blow-up criterion, not a proof that `T_star` is infinite.

## 9. Correspondence with the Clay statement

### Audited forward implication

For every datum in Fefferman's whole-space class:

```text
global Leray weak existence
 + universal finite I_T on every finite interval
 + LPS regularity and uniqueness
 + local strong theory and bootstrapping
 -> global smooth solution with bounded energy.
```

Therefore the full-data universal critical-integrability statement is sufficient for Clay statement (A).

### Reverse direction not yet promoted

To call the formulations bidirectionally equivalent, the programme must source-normalize:

1. finite `L4_tL6_x` membership on every compact time interval from the exact smooth-solution class in Fefferman's statement;
2. weak–strong identification of every Leray–Hopf solution with that smooth solution;
3. behavior at the initial time in the selected `H1` or strong class.

The approved wording is therefore **sufficient for**, not **equivalent to**, until this final bridge is committed.

## 10. Claim decisions

| Claim | Decision |
|---|---|
| Energy implies `L2_tL6_x` | retain; local proof conditional on standard energy/Sobolev interfaces |
| Energy space does not imply `L4_tL6_x` | retain; direct obstruction proof |
| Critical scaling | retain; direct proof |
| `L4_tL6_x` implies uniqueness/strong regularity under stated hypotheses | promote to operationally audited literature-derived claim |
| Universal full-data critical integrability implies Clay (A) | promote as an audited one-way implication |
| Compact-support universal result implies full Clay (A) | reject without a data-class extension theorem |
| Full bidirectional equivalence | retain as pending correspondence debt |
| Current universal estimate is open | promote from official current status |

## 11. Remaining debt

Blocking before mechanism generation:

- integrate the corrected full data class into every campaign artifact;
- update the theorem spine and claim ledger to use one-way implication language;
- obtain Referee confirmation that no hidden data or solution-class transfer remains.

Nonblocking historical/certification debt:

- original Leray theorem-number map;
- exact Serrin theorem-body extraction;
- Ladyzhenskaya mathematical translation;
- kernel-checked mixed-norm scaling;
- optional formalization of the abstract concentration witness.

## 12. Stage decision

WP00 has completed its substantive source-and-equivalence analysis, subject to ledger and governance integration. Mechanism generation and numerical experimentation remain closed until those integration changes pass CI and the Referee gate.