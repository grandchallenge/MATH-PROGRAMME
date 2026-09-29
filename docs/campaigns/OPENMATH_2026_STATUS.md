# OPENMATH-2026 — Current Campaign State

> **Canonical machine authority:** `governance/openmath_2026_campaign_state.json`
>
> This page is a human projection of that record. It is not a second source of truth.
>
> Historical records `governance/openmath_2026_external_state.json` and `governance/openmath_2026_campaign_binding.json` are **SUPERSEDED_FOR_CURRENT_STATE**. Preserve them as history; do not use them to resume current work.

## Current topology

OPENMATH-2026 has exactly seven first-class current hill lanes: **H1, H2, H3, H4, H5, H6, H7**. Historical aggregate labels such as `H2-H7` identify closed onboarding transactions only and are not current campaign topology.

## Campaign summary

- Hills: **7 / 7 source-locked and Solve-released**
- Independent-agent state: **3 ACCEPTED; 6 LEASED_NOT_LAUNCHED**
- Certified hills: **0**
- Official competition submissions: **0**
- Official competition acceptances: **0**
- Current blocking next action: **launch every exact hill lane whose agent state is `LEASED_NOT_LAUNCHED` from its registered immutable task URL**

`LEASED` does not mean `LAUNCHED`. `RETURNED` does not mean `CAPTURED`. `CAPTURED` does not mean `ACCEPTED` or `CERTIFIED`.

## Seven-hill control board

| Hill | Problem | Source / Solve | Independent agent | Cert | Competition |
|---|---|---|---|---|---|
| H1 | Kobon triangles | Source locked; active; campaign best observed **93**; protected frontier is now **q>=6**, source-conditional | **ACCEPTED** — Agent 001 q=5 reduction accepted at Solve level as `OM26-H1-RED-023` | H1 claims admitted; independent Cert executor **PENDING** | **CERT_PENDING; NOT_SUBMITTED** |
| H2 | Busy Beaver 6 certificates | Source locked; WP01 scorer accepted; WP02 accepted two finite witnesses; WP03 replay closure protected | **LEASED_NOT_LAUNCHED** — Agent 009 / #537; predecessor Agent 008 WP02 **ACCEPTED** | NOT_YET_ELIGIBLE | **NO_PROMOTED_CANDIDATE; NOT_SUBMITTED** |
| H3 | Clique-cluster Ramsey multiplicity | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 003 / #506 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |
| H4 | Collatz modular descent | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 004 / #507 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |
| H5 | Grothendieck constant witnesses | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 005 / #508 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |
| H6 | 3x3 matrix multiplication tensor | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 006 / #509 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |
| H7 | Erdős Problem 3 | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 007 / #510 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |

## H1 in plain terms

We have an exact rational 18-line construction scoring **93** under the protected Solve replay and the public AutoLab evaluator. That evaluator replay is an unofficial local score, not an official competition entry.

The recovered Agent 001 reduction has now been adjudicated and **accepted at Solve level** as the source-conditional claim `OM26-H1-RED-023`.

Its exact effect is to exclude the sole remaining q=5 equality normal form. The protected H1-12 frontier is therefore now:

`q >= 6`

subject to the same predecessor source-scoped local fan/no-consecutive-D1 and clean-line charging premises. This is not MATHCERT certification and does not establish that score 93 is globally optimal.

## Competition state

No OPENMATH-2026 hill has a recorded official competition submission.

For H1:

`RH_BADER_RECONSTRUCTION_093 -> LOCALLY_VERIFIED -> CERT_PENDING -> NOT_SUBMITTED`

There is no protected `SUBMITTED` or `ACCEPTED` receipt.

For H2, H3, H4, H5, H6, and H7 there is not yet a candidate submission object.

## Independent-agent state

- Agent 001 / H1: `ACCEPTED_SOURCE_CONDITIONAL_REDUCTION` (`OM26-H1-RED-023`)
- Agent 002 / H2 WP01: `ACCEPTED_SCORER_CONCORDANCE_WITH_SEARCH_NARROWING`
- Agent 008 / H2 WP02: `ACCEPTED_WITNESSES_WITH_EXACT_SEARCH_REPLAY_REJECTED`
- Agent 009 / H2 WP03: `LEASED_NOT_LAUNCHED`
- Agent 003 / H3: `LEASED_NOT_LAUNCHED`
- Agent 004 / H4: `LEASED_NOT_LAUNCHED`
- Agent 005 / H5: `LEASED_NOT_LAUNCHED`
- Agent 006 / H6: `LEASED_NOT_LAUNCHED`
- Agent 007 / H7: `LEASED_NOT_LAUNCHED`

For the active H2 WP03, H3 WP01, H4 WP01, H5 WP01, H6 WP01, and H7 WP01 assignments, `LEASED_NOT_LAUNCHED` means a protected lease exists but there is no durable launch or result evidence on the governed surfaces. It does not make claims about invisible off-platform activity.

## Exact domain authorities

- Source/provider truth: `grandchallenge/MATHFORGE` bound by the canonical state.
- Tactical/hill truth: `grandchallenge/MATHSOLVE` bound by the canonical state.
- Certification truth: `grandchallenge/MATHCERT` bound by the canonical state.
- Campaign/current-state truth: this Programme canonical record.

## Current next action

**Launch each exact active lease whose protected lifecycle is `LEASED_NOT_LAUNCHED` from its registered immutable task URL.**

Agent 001, H2 WP01, and H2 WP02 adjudications are closed. H2 WP02 retained two verified finite witnesses: `(89911,185,541)` and first-write-zero `(8021,41,122)`. Its stronger exact-search-validation claim was rejected as stated. The current exact active leases are H2 WP03, H3 WP01, H4 WP01, H5 WP01, H6 WP01, and H7 WP01. Each is a peer hill-lane operation.

Launches use `LINK_IN_RELAY_OUT`: the launcher verifies the lease and gives the zero-context agent one registered immutable public task URL. The agent returns one complete `GCL-RETURN-RELAY/1` payload; authenticated GCL infrastructure owns durable GitHub intake. Human copy/paste is not part of the protocol.

Until durable launch evidence is recorded:

- H2 WP03, H3 WP01, H4 WP01, H5 WP01, H6 WP01, and H7 WP01 remain `LEASED_NOT_LAUNCHED`;
- `LEASED` SHALL NOT be reported as `LAUNCHED`;
- no returned result is inferred from silence or lease state.

After the launch tranche, the canonical campaign state SHALL be reconciled again before further discretionary substantive work.

## CORE CLARITY rule

Operational state and declared campaign state are one protected system.

If Forge, Solve, Cert, external-agent state, or competition state changes and this canonical record has not yet been reconciled, OPENMATH-2026 is in **control-plane drift** and discretionary substantive advancement is blocked.
