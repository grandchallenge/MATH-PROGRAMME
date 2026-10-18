# CMDG-CM4 — Mathlib Upstream Readiness Assessment

!!! info "Live source of truth"
    This page is an upstream-planning projection. Current port sequencing, blockers, and maintainer feedback are tracked on [MATH-PROGRAMME #1223](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1223). Protected repository receipts govern the underlying GCL theorem claim.


## Executive assessment

**Recommendation: upstream, but not as the current GCL file stack.**

The theorem is highly suitable for mathlib in substance because current mathlib master still carries the exact integer case as a hard TODO. The present GCL implementation, however, is not yet suitable as a single upstream PR because the terminal theorem depends on a substantial programme-local stack of measure, finite-Boolean, Nöbeling, coefficient, and reconciliation modules.

The right strategy is therefore:

1. external mathematical review;
2. dependency extraction and API normalization;
3. split reusable infrastructure into reviewable mathlib-sized PRs;
4. land the terminal `profiniteSolid ℤ` solidity theorem only after those dependencies are upstream or replaced by existing mathlib APIs.

## Why this is upstream-worthy

Current mathlib `Mathlib/Condensed/Solid.lean` says:

```text
TODO (hard): prove that ((profiniteSolid ℤ).obj S).IsSolid for S : Profinite.
```

The protected GCL theorem proves the corresponding universe-correct statement for every profinite `S`.

This is therefore a direct candidate to close a named, current, hard TODO in mathlib.

## Why the current code should not be submitted wholesale

The terminal theorem itself is only a few lines, but it imports GCL-local modules including:

```lean
CMDGCondensedCM4P3MFiniteQuotientBridge
CMDGCondensedCM4P3E
CMDGCondensedCM4P3G
CMDGCondensedCM4P3GFiniteBooleanMeasureHom
```

and those in turn encode programme-specific staging and intermediate abstractions.

An upstream PR should not require reviewers to understand GCL's P2/P3/P3G/P3M naming or governance decomposition. The reusable mathematics must be renamed and reorganized around mathematical concepts.

## Likely upstream decomposition

### PR A — Locally constant / Nöbeling functional infrastructure

Goal: upstream only generally reusable facts about finite-coordinate dependence and integral-basis representations of additive or linear functionals on locally constant integer-valued functions.

Acceptance criterion: no condensed-solid theorem in this PR.

### PR B — Point evaluation and measure/internal-Hom API

Goal: expose a clean Point-component API for the relevant condensed internal-Hom / measure object, including zero-reflection and naturality statements.

Acceptance criterion: definitions and lemmas are useful independently of the final solidity target.

### PR C — Finite Boolean reconstruction

Goal: upstream the weighted finite-Boolean reconstruction mechanism in a mathematically named namespace, with direct theorem statements and documentation explaining the finite quotient / limit argument.

Acceptance criterion: independent tests and no reference to CMDG stage names.

### PR D — Coefficient-object faithfulness / mapping-out criterion

Goal: isolate the theorem that the scalar product functional detects coefficient morphisms and connect it cleanly to the existing `CondensedMod.IsSolid` mapping-out characterization.

Acceptance criterion: no parent CM4 wrapper; this PR proves the reusable structural criterion.

### PR E — Close the mathlib TODO

Target:

```lean
theorem Condensed.profiniteSolid_isSolid
    (S : Profinite.{u}) :
    CondensedMod.IsSolid (ULift.{u + 1} ℤ)
      ((Condensed.profiniteSolid (ULift.{u + 1} ℤ)).obj S)
```

or the exact naming/type preferred by mathlib maintainers.

This PR should delete or update the existing TODO in `Mathlib/Condensed/Solid.lean`.

## Required refactoring before PR A

- Remove all `CMDG` namespace and operation identifiers from reusable source.
- Replace programme-specific theorem names with concept-based mathlib names.
- Reduce imports aggressively.
- Move declarations into the most natural existing Mathlib modules or narrowly scoped new modules.
- Add module documentation and references to the relevant condensed/solid literature.
- Run mathlib linters and all materially affected tests.
- Rebase against current mathlib master and eliminate downstream-only compatibility shims.
- Determine whether the `ULift` statement should be hidden behind an existing integer coefficient abbreviation or expressed directly in the style maintainers prefer.
- Confirm every new declaration's universe generality is intentional.
- Confirm the current proof does not depend on deprecated or private APIs.

## Licensing/provenance check

Mathlib contributions are Apache-2.0. The GCL repository is separately licensed. Before moving code verbatim, ensure the contributor(s) submitting the port have authority to submit the relevant code under mathlib's contribution terms. Rewriting the proof into mathlib-native form is recommended regardless.

## Upstream contributor integrity — required gate (October 2026)

Mathlib's [current contribution policy](https://leanprover-community.github.io/contribute/) explicitly prohibits LLM-authored GitHub or Zulip comments, requires disclosure of AI assistance in PR descriptions, and expects an engaged human contributor who understands and can justify each part of the submitted Lean code. A substantial LLM-generated code submission also requires the community's `LLM-generated` labeling procedure. These are **external policy requirements** and take precedence over GCL's internal automation or submission preferences.

Accordingly:

- **No autonomous AI submission of an AI-written mathlib PR, Zulip discussion, or reviewer comment.** GCL may prepare research notes, candidate ports, replay scripts and private/draft technical analyses, but must not present generated language as a human contribution.
- A qualified **human Lean subject expert** must personally inspect, understand, refactor and be prepared to defend the entire mathlib-bound code. The human writes the eventual upstream correspondence in their own words, including accurate AI-use disclosure.
- Seek maintainers' advice on placement and scope *before* a large port series; reduce the stack into genuinely reusable incremental PRs and compare with current mathlib master, not just the pinned 2026 GCL snapshot.
- Verify all authorship, provenance and license permissions before transferring source bytes. A verified formal proof does not waive software licensing or the community's human-supervision rules.
- A GCL-created PR or Issue in `grandchallenge/MATH-PROGRAMME` is an **internal preparation and reproducibility surface**, not a mathlib upstream submission.

**Current release gate:** independent specialist mathematical review [#1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222) **OPEN**; staged port [#1223](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1223) **OPEN**; no representation that mathlib maintainers have accepted this port.

**Recommended first upstream unit:** reusable lemmas about integral functionals on locally constant functions that can be stated without the terminal solid-module theorem. The exact unit must still be chosen with a human Lean expert and maintainer guidance, not inferred from a GCL work-package label.

## Community engagement

Mathlib's current contribution guidance recommends discussing substantial projects with the community, commonly through the mathlib Zulip, before investing in a large PR series.

For this result, the first outreach should be concise:

- identify the exact existing TODO;
- state that a Lean 4 proof exists downstream;
- summarize the Point-functional proof architecture;
- provide the protected proof/review packet;
- ask maintainers whether they prefer a staged PR series and where each reusable component should live.

Do **not** lead with GCL governance terminology.

## Upstream readiness score

### Mathematical relevance: HIGH

Directly closes a current hard TODO.

### Formal evidence: HIGH

Protected Lean proof, exact-head independent review, green formal validation, explicit axiom readback, no `sorryAx`.

### Code locality: LOW

Current proof is distributed across a large local stack.

### API maturity: MEDIUM-LOW

Several abstractions were developed to solve this campaign and have not yet been normalized against mathlib naming and module boundaries.

### Reviewability as one PR: LOW

A monolithic port would be too difficult to review.

### Reviewability as staged PRs: HIGH, after refactoring

The proof naturally decomposes into reusable mathematical layers.

## Go / no-go

**GO for upstream preparation.**

**NO-GO for submitting the present GCL branch directly to mathlib.**

The next technical operation should construct a clean mathlib-master port branch and produce a dependency-minimized prototype of PR A, while external mathematical review proceeds in parallel.
