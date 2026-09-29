# OPENMATH-2026 — Current Campaign State

> **Canonical machine authority:** `governance/openmath_2026_campaign_state.json`
>
> This page is a human projection of that record. It is not a second source of truth.
>
> Historical records `governance/openmath_2026_external_state.json` and `governance/openmath_2026_campaign_binding.json` are **SUPERSEDED_FOR_CURRENT_STATE**. Preserve them as history; do not use them to resume current work.

## Campaign summary

- Hills: **7 / 7 source-locked and Solve-released**
- Independent-agent state: **1 CAPTURED pending adjudication; 6 LEASED_NOT_LAUNCHED**
- Certified hills: **0**
- Official competition submissions: **0**
- Official competition acceptances: **0**
- Current blocking next action: **adjudicate recovered Agent 001 result**

`LEASED` does not mean `LAUNCHED`. `RETURNED` does not mean `CAPTURED`. `CAPTURED` does not mean `ACCEPTED` or `CERTIFIED`.

## Seven-hill control board

| Hill | Problem | Source / Solve | Independent agent | Cert | Competition |
|---|---|---|---|---|---|
| H1 | Kobon triangles | Source locked; active; campaign best observed **93**; protected frontier remains **q=5 exact nested-triangle equality or q>=6**, source-conditional | **CAPTURED** — Agent 001 result recovered; adjudication **PENDING** | H1 claims admitted; independent Cert executor **PENDING** | **CERT_PENDING; NOT_SUBMITTED** |
| H2 | Busy Beaver 6 certificates | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 002 / #505 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |
| H3 | Clique-cluster Ramsey multiplicity | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 003 / #506 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |
| H4 | Collatz modular descent | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 004 / #507 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |
| H5 | Grothendieck constant witnesses | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 005 / #508 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |
| H6 | 3x3 matrix multiplication tensor | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 006 / #509 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |
| H7 | Erdős Problem 3 | Source locked, slot-bound, semantic pack protected, Solve WP01 ready | **LEASED_NOT_LAUNCHED** — Agent 007 / #510 | NOT_YET_ELIGIBLE | **NO_CANDIDATE; NOT_SUBMITTED** |

## H1 in plain terms

We have an exact rational 18-line construction scoring **93** under the protected Solve replay and the public AutoLab evaluator. That evaluator replay is an unofficial local score, not an official competition entry.

The protected upper-bound route has narrowed a possible 95-triangle witness to either:

1. the exact surviving q=5 nested-triangle equality geometry; or
2. q>=6 finite multiple points.

Agent 001 returned a claimed reduction closing the q=5 case. The original intake infrastructure rejected the return incorrectly. The exact returned bytes are now durably recovered and pass the repaired generic RESULT/1 parser, but the mathematics has **not** been adjudicated. Therefore the protected H1 frontier has **not** been advanced by the recovered claim.

## Competition state

No OPENMATH-2026 hill has a recorded official competition submission.

For H1:

`RH_BADER_RECONSTRUCTION_093 -> LOCALLY_VERIFIED -> CERT_PENDING -> NOT_SUBMITTED`

There is no protected `SUBMITTED` or `ACCEPTED` receipt.

For H2-H7 there is not yet a candidate submission object.

## Independent-agent state

- Agent 001 / H1: `CAPTURED_RECOVERED_UNADJUDICATED`
- Agent 002 / H2: `LEASED_NOT_LAUNCHED`
- Agent 003 / H3: `LEASED_NOT_LAUNCHED`
- Agent 004 / H4: `LEASED_NOT_LAUNCHED`
- Agent 005 / H5: `LEASED_NOT_LAUNCHED`
- Agent 006 / H6: `LEASED_NOT_LAUNCHED`
- Agent 007 / H7: `LEASED_NOT_LAUNCHED`

The H2-H7 classification means protected leases exist, but there is no durable launch or result evidence on the governed surfaces. It does not make claims about invisible off-platform activity.

## Exact domain authorities

- Source/provider truth: `grandchallenge/MATHFORGE` bound by the canonical state.
- Tactical/hill truth: `grandchallenge/MATHSOLVE` bound by the canonical state.
- Certification truth: `grandchallenge/MATHCERT` bound by the canonical state.
- Campaign/current-state truth: this Programme canonical record.

## Current next action

**Adjudicate the recovered Agent 001 H1 result.**

Until that bounded adjudication closes:

- the H1 frontier remains unchanged;
- Agent 001's claimed q=5 closure is not an admitted mathematical result;
- Agents 002-007 remain `LEASED_NOT_LAUNCHED`;
- no discretionary next OpenMath mathematical tranche is authorized by the campaign control plane.

After that operation, the canonical campaign state SHALL be reconciled again before further discretionary substantive work.

## CORE CLARITY rule

Operational state and declared campaign state are one protected system.

If Forge, Solve, Cert, external-agent state, or competition state changes and this canonical record has not yet been reconciled, OPENMATH-2026 is in **control-plane drift** and discretionary substantive advancement is blocked.
