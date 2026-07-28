# MATHFORGE Provider Import and Promotion Policy

## Authority

This policy is a binding extension of `MATHFORGE_SPEC.md` and `GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md`.

It governs the boundary between MATHFORGE provider work and MATH-PROGRAMME campaign authority. Where an older package or template permits provider work to remain implicit, this policy controls future promotion.

## Core rule

MATH-PROGRAMME SHALL import MATHFORGE provider evidence by immutable identity. It SHALL NOT absorb source reconstruction, status triage, prior-art reconnaissance, candidate generation, false-proof fixtures, or failed-route evidence into Programme-only artifacts while leaving MATHFORGE optional.

An import consists of:

1. the canonical provider repository;
2. a full 40-character MATHFORGE commit identity;
3. a repository-relative provider-manifest path;
4. the manifest's verified content identity;
5. its coverage mode, `native` or `retrospective`;
6. a Programme registry entry.

The canonical registry is `governance/mathforge_provider_imports.json`.

## Provider-gated stages

The following stages may not be promoted without a valid provider import or an approved scoped waiver:

- `WP00` source, formulation, normalization, or equivalence audit;
- `WP01` false-proof or route-rejection atlas;
- prior-art, current-status, and novelty-prohibition audit;
- candidate shortlist or restricted-target selection.

The gate applies when opening a new campaign, promoting an existing package, or materially revising a promoted provider-sensitive artifact.

## Native coverage

Native coverage means that the discovery work was performed and retained in MATHFORGE. The provider manifest identifies the Forge-owned artifacts, their claim boundaries, and their content identities.

Programme packages may summarize or cite native Forge findings. They may not replace the provider artifacts as the evidence source.

## Retrospective coverage

Retrospective coverage is permitted only for work completed before this policy entered force.

A retrospective manifest:

- indexes immutable Programme commits and paths;
- does not copy authoritative Programme text into MATHFORGE;
- does not imply that native Forge work occurred;
- records missing native provider work as explicit debt;
- requires future discovery, prior-art, WP01, or target-selection work to originate in MATHFORGE unless separately waived.

Retrospective coverage does not weaken claim or certification boundaries.

## Waivers

A waiver is exceptional and fail-closed. It must record:

- approving authority;
- concrete reason;
- exact scope;
- review date.

A waiver may cover only the named campaign and stage. It does not establish a general exemption for a domain or repository.

Missing, expired, unscoped, or incomplete waivers are invalid.

## Active-campaign coverage

Every `ACTIVE` campaign in `DOMAIN_REGISTRY.yaml` must appear in the provider import registry.

Pre-admission campaigns may also be registered. Their presence does not admit them as active domains or authorize successor stages.

A new active domain added without provider coverage fails Programme validation.

## Verification and CI

`ci/validate_mathforge_provider_imports.py` validates:

- the canonical provider repository and commit;
- active-domain coverage;
- exact campaign identifiers;
- manifest paths and Git blob identities;
- native versus retrospective classification;
- waiver completeness;
- duplicate and orphan import records.

The validator is registered in `ci/campaign_replay_registry.json`. The Programme policy workflow therefore fails closed when the provider contract is broken.

Adversarial tests in `tests/test_mathforge_provider_imports.py` reject omitted campaigns, new uncovered active domains, commit drift, manifest-identity drift, and incomplete waivers.

## Claim boundary

A valid MATHFORGE import establishes provider provenance and handoff readiness only. It does not:

- prove a mathematical claim;
- certify a computation;
- establish novelty;
- promote a Work Package by itself;
- transfer MATHCERT authority to MATHFORGE;
- convert retrospective coverage into native provider work.

MATH-PROGRAMME retains campaign and promotion authority. MATHCERT retains certification authority.

## Initial admission record

The initial registry pins eight provider manifests at MATHFORGE commit `2cb624cc61cd95ec0c8cfb8429d93128972289a5`:

- native: `UC-001`, `NS-CI-001`, `HC-001`;
- retrospective: `BSD-001`, `PNP-001`, `RH-001`, `YM-001`, `OZ-001`.

`OZ-001` remains a pre-admission source-lock campaign. Its provider registration does not complete source acquisition or open successor stages.
