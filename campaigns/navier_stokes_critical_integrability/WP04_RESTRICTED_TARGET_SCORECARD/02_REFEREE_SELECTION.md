# NS-CI-WP04 — Referee target-selection decision

## Decision

Select `NS-CI-R014-A2`, the critical dissipation-wavenumber criterion, as the first theorem-grade restricted research target for campaign `NS-CI-001`.

Selected statement:

> Fix `nu>0`, a smooth divergence-free rapidly decreasing datum on `R3`, a finite `T>0`, and a Leray–Hopf solution `u` on `[0,T]`. Let `Lambda(t)` be the Cheskidov–Shvydkoy whole-space dissipation wavenumber. Prove or disprove
>
> ```math
> \Lambda\in L^2(0,T)
> \quad\Longrightarrow\quad
> \int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt<\infty.
> ```

A source-aligned sufficient intermediate target is

```math
\Lambda\in L^2(0,T)
\quad\Longrightarrow\quad
\|\omega_{\le Q(t)}\|_{B^0_{\infty,\infty}}\in L^1(0,T).
```

## Status semantics

`SELECTED_RESEARCH_TARGET_UNPROVED` means:

- the statement is precise enough to organize proof and falsification work;
- its data, solution class, quantifiers, scaling, imported definitions, and claim boundary have been reviewed;
- it is not proved, certified, or claimed novel;
- absence of an exact match in the bounded prior-art search is not a novelty determination;
- universal critical integrability and global regularity remain open.

## Referee rationale

### Mathematical leverage

A2 lies on the exact critical scaling boundary. The source proves universal `Lambda in L1_t`, regularity from `Lambda in L5/2_t`, and the low-mode envelope

```math
c\nu\Lambda^2
\lesssim
f(t)
\lesssim
C\Lambda^{5/2}\|u(t)\|_2.
```

The exponent `2` is therefore neither an arbitrary interpolation point nor a restatement of the target. It identifies a critical half-power gap inside a source-defined frequency criterion.

### Non-circularity

The hypothesis is an independently defined threshold observable. It does not assume `L4_tL6_x`, uniform `H1`, or a named LPS/Besov norm. All routes that covertly insert those quantities remain rejected by WP01.

### Adversarial value

Three elementary routes have already failed exactly:

1. the source envelope allows `Lambda^2` integrable while `Lambda^(5/2)` is not;
2. low-frequency Sobolev closure produces a product of two unrelated `L1_t` coefficients;
3. the direct estimate `f lesssim Lambda^(3/2)D^(1/2)` requires cubic rather than quadratic integrability of `Lambda`.

Thus selection does not rest on a disguised elementary proof. The remaining lanes require genuinely equation-specific information: time-frequency packing, excursion cost, weighted dissipation, or cancellation.

### Information value

A proof would supply a new critical conditional bridge if the prior-art boundary survives final publication review. A rigorous no-go for the natural mechanisms would also identify why critical dissipation-wavenumber control fails to govern the LPS coefficient. Either outcome improves the map of the full problem.

## Disposition of other candidates

### D1

`NS-CI-R014-D1` is not selected. Its compensated enstrophy inequality is an analytic interface that already contains the desired closure. D1 may re-enter a later scorecard only after an independent, scale-uniform, non-tautological shell-transfer hypothesis `H_D` is supplied.

### E1

`NS-CI-R014-E1` is retained as an auxiliary bridge theorem. It may be developed separately to normalize compact-support approximation, lower semicontinuity, and weak–strong identification. It is not the principal restricted target because its uniform approximation bound carries most of the regularity content.

### Recent claimed proofs

The 2026 arbitrary-swirl and broader global-regularity preprints remain in MATHFORGE claimed-proof issue `#20`. Their audit is independent and does not condition A2 selection. No result from those manuscripts is imported.

## Authorized next stage

The following work is now authorized for A2 only:

- exact source reconstruction;
- analytic mechanism generation within MATHSOLVE issue `#24`;
- adversarial dyadic packet and scalar fixtures;
- proof or no-go analysis for level-set packing, excursion duration, weighted dissipation, and direct high/low frequency routes;
- MATHCERT formalization of scaling, exponent, quantifier, and imported-interface fixtures.

WP03 numerical observatory remains closed. It may open only for a separately approved falsification test of a precise intermediate inequality. Numerical boundedness of `Lambda`, `f`, or `I_T` is not evidence for A2.

## Promotion and exit conditions

A2 may advance from selected target to theorem candidate only after one of the following:

1. a complete proof route survives Verifier, Adversary, Formalist, Amanuensis, and Referee review; or
2. a strict narrower lemma with independent value is proved and promoted; or
3. every admitted mechanism terminates with exact gaps, producing a Referee-approved no-go or retirement record.

## Claim boundary

This selection does not prove A2, assert novelty, establish a new regularity criterion, accept any claimed proof, or alter the open status of the Navier–Stokes problem.