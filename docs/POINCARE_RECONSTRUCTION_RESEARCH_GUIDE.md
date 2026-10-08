# PC-WP01 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [false-proof atlas tracker #72](https://github.com/grandchallenge/MATH-PROGRAMME/issues/72).  
    **AUTHORITY:** `campaigns/poincare_reconstruction/WP01_FALSE_PROOF_ATLAS/10_CLAIM_LEDGER.yaml` and `reviews/poincare/PC-WP01.agent_review.yaml`.  
    **EXPOSITION:** this guide explains a terminal reconstruction/archive surface and does not reopen or recertify the Poincaré theorem.

## 1. Status

The Poincaré conjecture is a solved classical theorem. PC-WP01 is a terminal negative-knowledge and reconstruction artifact: it records recurrent invalid proof moves and the corrected Hamilton–Perelman dependency route.

## 2. Plain object

The archive distinguishes the analytic Ricci-flow theorems imported from the literature from the finite surgery-history representations and expression-level evaluators implemented in the repository.

## 3. Exact contribution

The protected claim ledger records false-proof diagnoses, topology-history fixtures, source-preserving reconstruction interfaces, and bounded formal/evaluator results. It does not formalize Ricci flow or independently reprove Perelman’s analytic work.

## 4. Trust boundary

A valid finite schema does not prove that a geometric event occurred. The Lean layer is conditional on imported event equations and does not formalize manifolds, connected sums, surgery existence, or finite extinction.

## 5. Authority chain

Use:
- `campaigns/poincare_reconstruction/WP01_FALSE_PROOF_ATLAS/10_CLAIM_LEDGER.yaml`
- `reviews/poincare/PC-WP01.agent_review.yaml`
- `docs/POINCARE_RECONSTRUCTION_ARCHIVE.md`

## 6. Remaining debt

Only archival/source-concordance debt remains at this surface: sentence-level proof correspondence, exact parameter translation, and independent analytic verification where explicitly retained. No open-problem theorem target is implied.

## 7. Claim boundary

No new Poincaré proof, machine-checked proof of the theorem, novelty, or priority claim is admitted.

## 8. First executable step

For audit, read the protected claim ledger and review record before consulting the archive narrative. Any new reconstruction work must preserve the imported-analytic-theorem boundary.

## Reader entry and prerequisites

**Status:** terminal reconstruction/negative-knowledge archive of a solved classical theorem. **Audience:** undergraduate topology readers and proof-audit collaborators. **Time to first example:** 10 minutes. **Time to first fixture:** 10 minutes.

| Level | Concepts |
| --- | --- |
| Required | Fundamental group intuition, spheres, closed manifolds |
| Helpful | Homology and covering spaces |
| Deferred | Ricci flow, canonical neighborhoods, surgery and finite extinction |

## Core bridge and first examples by hand

**Friendly example:** \(S^3\) is closed and simply connected. It is the conclusion of the classical Poincaré theorem, not a new GCL theorem.

**Failure example:** replacing the hypothesis "simply connected" with "has the same integer homology as \(S^3\)" is invalid. The classical Poincaré *homology sphere* has the homology of \(S^3\) but nontrivial fundamental group (the binary icosahedral group). The two conditions must not be silently exchanged.

Bridge: manifold invariants → false homology-to-homotopy inference → true classical theorem hypotheses → imported Ricci flow / surgery → finite history reconstruction.

## First computation or fixture

This intentionally limited Python 3 fixture checks only the *logical distinction* between two records; booleans are source-labelled and are **not** a computational proof of homology or fundamental group:

```python
objects = {
    "3-sphere": dict(homology_sphere=True, simply_connected=True),
    "Poincare-homology-sphere": dict(homology_sphere=True, simply_connected=False)
}
print([(name, obj["homology_sphere"], obj["simply_connected"])
       for name, obj in objects.items()])
# Expected: one true/true row and one true/false row
```

**Support route:** a finite logical regression fixture, not validation of the imported topological facts.

## First theorem or local proposition

**Elementary logical proposition.** From \(P(x)\) alone one cannot infer \(Q(x)\) when an admitted instance satisfies \(P\land\neg Q\). Here the classical homology sphere is an imported counterexample to the false implication. The protected atlas records its source; the guide does not reproduce the Ricci-flow theorem.

## Challenge ladder

| Stage | Duty | Completion test |
| --- | --- | --- |
| Exercise | Distinguish \(\pi_1\) from \(H_1\) | Name their different definitions |
| Exploration | Inspect the imported homology sphere example | Identify false implication |
| Fixture | Execute logical record check | Two contrasting rows |
| Lemma candidate | Formalize the counterexample pattern | State premises and failed conclusion |
| Open direction | Trace one finite-history imported-event edge | Identify imported analytic premise rather than asserting it |

## Certification path and continuation graph

The toy record is replayable; the protected finite backward-evaluator results have separate assumptions. The analytic Hamilton–Perelman theorems remain external/imported and are not checked by the toy fixture.

`logical counterexample → false-proof fixture → source-normalized analytic dependency → finite history replay → conditional Lean evaluator`

## Trust quartet

**Proved:** elementary logical nonimplication and bounded formal evaluator within protected hypotheses. **Checked:** the logical fixture and registered finite histories. **Open:** no classical Poincaré problem; source-concordance/independent analytic audit debt remains. **External verification:** Hamilton–Perelman and full analytic-to-finite-event premises.

## Bibliography and source audit

| Source | Role | Audit state |
| --- | --- | --- |
| [Protected false-proof claim ledger](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/poincare_reconstruction/WP01_FALSE_PROOF_ATLAS/10_CLAIM_LEDGER.yaml) | Negative-result authority | Protected |
| [Agent review](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/reviews/poincare/PC-WP01.agent_review.yaml) | Scope gate | Protected |
| Perelman I–III; Morgan–Tian; Kleiner–Lott | Classical imported geometric proofs | Governing external literature; analytic proof not formalized here |

**First executable step / completion test:** Run the logical fixture, then identify one actual false-proof ledger fixture and its smallest imported theorem dependency without upgrading the Lean expression checker to full Ricci-flow formalization.

