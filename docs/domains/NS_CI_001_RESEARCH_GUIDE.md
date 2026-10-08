# NS-CI-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [NS-CI-001 canonical tracker #55](https://github.com/grandchallenge/MATH-PROGRAMME/issues/55).  
    **AUTHORITY:** `DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md`.  
    **EXPOSITION:** this guide explains current protected state; it does not promote an analytic estimate or regularity claim.

## 1. Status

The three-dimensional Navier–Stokes critical-integrability target remains open. The protected interface and conditional-regularity structure are qualified, but the universal estimate
`u in L^4_t L^6_x`
for the full rapidly decreasing data class is unproved.

## 2. Plain object

The campaign asks whether every relevant Leray–Hopf solution satisfies
`∫_0^T ||u(t)||_6^4 dt < ∞`
for every finite `T`. This is the scale-critical Ladyzhenskaya–Prodi–Serrin pair `(4,6)`.

## Reader entry and prerequisites

**Status:** open analytic estimate, conditional regularity interface only. **Audience:** graduate PDE students, analysts, formalization collaborators. **Time to first example:** 10 minutes. **Time to first fixture:** 10 minutes.

| Level | Concepts |
| --- | --- |
| Required | Improper integrals, \(L^p\) spaces, elementary Hölder inequality |
| Helpful | Weak solutions, Sobolev embedding, Navier–Stokes scaling |
| Deferred | Leray–Hopf theory, critical regularity criteria, nonlinear commutators |

## 3. Exact obstruction

Energy-class control yields `L^2_t L^6_x`, not the required `L^4_t L^6_x`. The missing gain cannot come from finite-interval inclusion. A successful route needs a genuinely equation-specific cancellation, commutator, depletion, decorrelation, or comparable mechanism.

## 4. Working model

The prior L4 excursion-persistence route is terminated absent such a mechanism. The direct L5 critical-integral lane is the active mathematical direction. The WP06 computability/undecidability lane is non-blocking and supplies no evidence for the true viscous equation without a complete reduction.

## Core bridge and first examples by hand

Energy control yields a time \(L^2\) condition where the target asks for \(L^4\). These exponents cannot be reversed.

**Friendly example:** for \(f(t)=1\) on \((0,1)\), both \(\int_0^1|f|^2dt\) and \(\int_0^1|f|^4dt\) equal 1.

**Edge example:** \(f(t)=t^{-1/3}\) has \(\int_0^1|f|^2dt=3\), but \(\int_0^1|f|^4dt=\infty\), because the integrand is \(t^{-4/3}\). This is a **scalar counterexample to a functional-analytic inference**, not a Navier–Stokes solution or blow-up example.

Bridge: time-integrability condition → stronger exponent → failure of \(L^2\)-to-\(L^4\) implication → search for PDE-specific gain.

## First computation or fixture

Python 3 exact rational exponent check:

```python
from fractions import Fraction
alpha = Fraction(1, 3)
for q in (2, 4):
    beta = q * alpha
    print(q, beta, "finite" if beta < 1 else "divergent")
# Expected:
# 2 2/3 finite
# 4 4/3 divergent
```

Input \(\alpha=1/3\); operation checks the elementary criterion \(\int_0^1t^{-\beta}dt<\infty\iff\beta<1\). **Support route:** exact arithmetic fixture. **Limitation:** it is not PDE evidence.

## First theorem or local proposition

**Finite-interval embedding.** For finite \(T\), \(\|f\|_{L^2(0,T)}\le T^{1/4}\|f\|_{L^4(0,T)}\). Hölder applied to \(\int |f|^2\cdot1\) proves this. The reverse inference is not valid, as the edge example shows.

## 5. Theorem-spine location

Authority is `DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md`; LIVE state is tracker #55. The MATHCERT qualification is interface-only and leaves the analytic predicates and continuation bridge obligations explicit.

## 6. Debt audit

Open debt includes the direct critical-integral estimate, any required weak–strong uniqueness/correspondence interfaces for the exact target class, and source-normalized closure of imported analytic predicates used downstream.

## 7. Claim boundary

No regularity theorem, universal critical-integrability theorem, undecidability result, blow-up result, or independence result is admitted by the current protected state.

## Challenge ladder

| Stage | Duty | Completion test |
| --- | --- | --- |
| Exercise | Integrate \(t^{-2/3}\) by hand | Obtain 3 |
| Exploration | Find exponents \(\alpha\) with \(2\alpha<1\le4\alpha\) | Give interval \([1/4,1/2)\) |
| Fixture | Replay exponent checker | Exact \(2/3\) and \(4/3\) |
| Lemma candidate | Prove \(L^4\hookrightarrow L^2\) on \((0,T)\) | State dependence on \(T\) |
| Open direction | Specify an equation-specific signed gain | Name actual PDE term and admissible bound |

## Certification path and continuation graph

Finite scalar checks are independently replayable. The real PDE theorem would require a source-normalized analytic proof of the critical estimate and its continuation/correspondence bridge, followed by independent review—not a finite simulation.

`scalar exponent fixture → Hölder lemma → critical scaling → L5 PDE-specific estimate [OPEN] → continuation theorem → Cert handoff`

## Trust quartet

**Proved:** the elementary embedding. **Checked:** the scalar exponent fixture. **Open:** universal critical integrability for the true viscous equation. **External verification:** imported analytic continuation/weak–strong theorems and any proposed nonlinear estimate.

## Bibliography and source audit

| Source | Use | Audit state |
| --- | --- | --- |
| [NS-CI master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md) | Exact PDE, solution class, obligations | Protected Programme authority |
| [Campaign tracker #55](https://github.com/grandchallenge/MATH-PROGRAMME/issues/55) | LIVE routing | Mutable, not proof authority |
| Primary LPS and Leray–Hopf results (source ledger in master plan) | Imported continuation and regularity tools | Must preserve source hypotheses |

**First executable step / completion test:** Replay both scalar integrals and produce an exact restricted L5 estimate statement naming the missing PDE-specific term without asserting it has been proved.

## 8. First executable step

Continue the L5 lane only with an equation-specific estimate that survives the existing false-proof controls. Do not reopen L4 or elevate WP06 evidence without a new protected bridge theorem.
