# CMDG-CM4 — Accessible Research Guide

<p class="page-deck">An entry path for readers who want to understand, review, or help upstream the CM4 solidity result without first reconstructing the entire CMDG campaign.</p>

!!! info "Live work is issue-led"
    External review is tracked on [#1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222).  
    Mathlib upstreaming is tracked on [#1223](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1223).  
    This guide teaches the route; it does not replace those trackers.

For an introductory path that does not assume condensed mathematics, first read [*Condensed Mathematics for the Perplexed*](CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED.md). The present guide starts from that framework and proceeds to the CM4 proof obligations.

## Status and intended reader

| Field | Value |
| --- | --- |
| Status | Certified/protected module-level theorem; external review and upstream port active |
| Audience | Graduate reader, condensed-math specialist, Lean/mathlib contributor, agentic assistant |
| Support route | Formal proof |
| First runnable artifact | `CMDGCondensedCM4P3GPointFunctional.lean` |
| Current live trackers | #1222, #1223 |

## Plain object

For a profinite space (S), mathlib defines `Condensed.profiniteSolid R`, intended to produce the solid analogue of the free condensed (R)-module on (S).

The theorem asks, for integer coefficients: is the resulting object actually solid?

## Prerequisites

| Level | Concepts |
| --- | --- |
| Required | Categories and functors; modules; profinite spaces; locally constant functions; basic Lean theorem reading |
| Helpful | Condensed sets/modules; Kan extensions; Yoneda; internal Homs; Nöbeling freeness |
| Deferred | Derived categories, Ext, source-level liquid/solid machinery beyond the selected module-level route |

The selected proof is useful pedagogically because the hardest derived machinery can be deferred rather than assumed.

## Core bridge

```text
locally constant functions
  → integral basis / finite-coordinate dependence
  → scalar functional at Point
  → finite Boolean reconstruction
  → functional detects morphisms
  → mapping-out injectivity
  → solidity
```

The bridge does not assume the terminal theorem. Its purpose is precisely to replace the historical derived obstruction with a concrete detector.

## First examples by hand

### Example 1 — finite profinite space

If (S) is finite, locally constant integer-valued functions on (S) are simply functions (S \to \mathbb Z). The coordinate functions form an obvious finite basis.

A linear functional is therefore determined by finitely many integer weights.

This is the finite model for the later coefficient-functional argument.

### Example 2 — infinite profinite space

For a general profinite (S), a locally constant integer-valued function still factors through some finite quotient of (S).

The point is not that (S) is finite. The point is that each locally constant observable only sees finite information.

Nöbeling-type freeness and the finite-quotient structure let the proof organize those finite observations globally.

## First fixture

Read the terminal theorem backwards.

1. Open `CMDGCondensedCM4Blocker.lean` and identify `cm4Target_via_pointFunctional`.
2. Follow it to `profiniteSolid_isSolid_via_pointFunctional`.
3. Follow that to `coefficientObject_isSolid_via_pointFunctional`.
4. Then inspect the faithfulness chain ending in `coefficient_eq_zero_of_solidification_kernel`.

Completion test: you can explain, without referring to P3/P4/P5/P6 names, why a morphism killed by solidification is forced to be zero.

## First local proposition

A useful first proposition to understand is:

> If the integral Point functional attached to a Point-measure section is zero, then the Point-measure section itself is zero.

Formal witness:

`measurePointIntegralFunctional_zero_reflects`.

This is the local prototype of the whole proof: a simpler observable detects the original structured object.

## Challenge ladder

| Stage | Task |
| --- | --- |
| Exercise | Prove that a linear functional on (mathbb Z^n) is determined by its values on the standard basis. |
| Exercise | Explain why a locally constant map from a profinite space to a discrete finite set factors through a finite quotient. |
| Fixture | Trace `measurePointFunctional_zero_reflects` and list every nontrivial dependency. |
| Restricted claim | Re-express `kernelProductFunctional_eq_zero_of_solidification_kernel` in ordinary mathematical prose. |
| Review task | Audit whether `weightedFiniteBooleanMeasureLimitLift_measurePoint_allTrue` uses exactly the hypotheses stated. |
| Upstream task | Identify which Point-functional lemmas belong in general mathlib APIs rather than a solid-specific file. |

## Certification path

```text
human statement
  → exact Lean target
  → local lemmas
  → clean replay
  → axiom readback
  → independent exact-head review
  → protected merge
  → external specialist review
  → mathlib-native port
```

The first seven stages are complete for the GCL result. The last two are the current live work.

## Continuation graph

```text
CM4 protected result
   ├── external mathematical review (#1222)
   │      └── sound / clarification / gap disposition
   │
   └── mathlib port (#1223)
          ├── reusable functional infrastructure
          ├── Point/internal-Hom API
          ├── finite Boolean reconstruction
          ├── coefficient faithfulness
          └── terminal profiniteSolid ℤ theorem
```

## Claim boundary

The guide supports understanding of the exact module-level integer theorem only.

It does not promote:

- the source-derived/complex theorem;
- general solid modules over arbitrary rings;
- Liquid Tensor;
- CM5;
- global dependency-graph certification.

## Independent proof and replay materials

- [Mathematical note](CMDG_CM4_MATHEMATICAL_NOTE.md): a complete reader-facing argument map separating the finite heuristic from the general profinite theorem.
- [Reproducibility protocol](CMDG_CM4_REPRODUCIBILITY.md): one exact immutable historical checkout, Lean/mathlib identity checks, two formal lanes, and adversarial failure tests.

## Where to go next

- Start with the [CM4 result page](CMDG_CM4.md).
- For specialist review, use the [External Mathematical Review Packet](CMDG-CM4-EXTERNAL-MATHEMATICAL-REVIEW.md) and report on [#1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222).
- For upstream work, use the [Mathlib Upstream Readiness Assessment](CMDG-CM4-MATHLIB-UPSTREAM-ASSESSMENT.md) and coordinate on [#1223](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1223).
