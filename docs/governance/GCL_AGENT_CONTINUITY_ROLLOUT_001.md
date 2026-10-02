# GCL-AGENT-CONTINUITY-ROLLOUT-001 — Mathematics-stack repository adoption plan

**Status:** PROPOSED_FOR_COUNCIL_DISPOSITION  
**Date:** 2026-09-18  
**Canonical policy:** `GCL-AGENT-CONTINUITY-001@1.0.0`  
**Canonical authority repository:** `grandchallenge/INTELLECT`  
**Effective INTELLECT protected main:** `7662e9b5eeecb065e75173176d535d57a5a42dee`  
**Reference implementation:** `grandchallenge/MATHSOLVE` protected main `ebbb049295c39281cc30a2b8e2a1d01f7fb66005`

## 1. Objective

Adopt the canonical bounded-turn continuity policy across the remaining mathematics-stack repositories in a way that preserves each repository's authority boundary.

The proposal is intentionally not a byte-for-byte replication of the MATHSOLVE implementation. It defines one universal continuity contract and three repository-local specializations:

1. MATH-PROGRAMME: thin canonical binding over the existing bounded-operation continuity machinery;
2. MATHFORGE: provenance-aware discovery/reconstruction specialization;
3. MATHCERT: certification-safe specialization that explicitly prevents authority or independence from being inherited through agent substitution.

The objective is operational continuity, not authority expansion.

## 2. Governing invariant

Repository state, not conversational memory, owns the resumable operational state of any admitted long-running operation.

A timeout, connector failure, truncated output, CI infrastructure failure, compiler diagnostic, context loss, or agent substitution is recoverable unless it exposes a genuine named governance, authentication, safety, materially changed-state, scope, or substantive evidentiary boundary.

Continuity metadata must never create mathematical proof, certification, publication, protected-branch bypass, independent review, or Human Steward authority.

## 3. Current protected-state basis

At proposal creation:

- INTELLECT: `7662e9b5eeecb065e75173176d535d57a5a42dee`;
- MATH-PROGRAMME: `d061a8e9b53a98c95bcb4c412b3107391c96ec00`;
- MATHFORGE: `3a097cf5f1ad5e12eeba83a08dccfbf7bc49b5f4`;
- MATHCERT: `2f27aed33b32b4caf6ff8622c87cfd6d40e97607`;
- MATHSOLVE reference adoption: `ebbb049295c39281cc30a2b8e2a1d01f7fb66005`.

MATH-PROGRAMME already contains a mature bounded-operation continuity mechanism in `AGENTS.md`, `governance/bounded_operation_checkpoint_registry.json`, and `ci/validate_bounded_operation_continuity.py`. The rollout must preserve that machinery rather than create a competing checkpoint system.

## 4. Council decision requested

The Council is asked to approve, reject, or amend the following architecture:

### 4.1 Universal layer

Every participating mathematics repository SHALL:

- bind `GCL-AGENT-CONTINUITY-001@1.0.0` from its root agent instruction surface;
- carry a machine-readable adoption record;
- identify its repository-local specialization, if any;
- validate the adoption in CI;
- register any new continuity workflow in `.ghos-routing/workflows.json`;
- preserve exact-head rebinding, durable checkpointing, post-mutation readback, alternate-agent recovery, and named terminal boundaries;
- state explicitly that continuity does not widen authority.

### 4.2 MATH-PROGRAMME specialization

MATH-PROGRAMME SHALL treat its existing bounded-operation mechanism as the conforming implementation of the canonical policy.

The adoption record SHALL map:

- `exact_head_preflight` -> checkpoint `freshness.verification_command`;
- `durable_checkpoint` -> bounded-operation checkpoint registry and `WORKSET_STATE.json`;
- `alternate_agent_live_rebind` -> `resume.fresh_session_safe=true` and `resume.requires_chat_history=false`;
- `deterministic_resume` -> exactly one nonterminal `next_action`;
- `named_terminal_boundary` -> recognized checkpoint boundary categories and evidence.

No second continuity registry or competing checkpoint format SHALL be introduced merely to satisfy the canonical policy.

### 4.3 MATHFORGE specialization

MATHFORGE SHALL adopt the common policy with additional source/provenance requirements.

A Forge continuity checkpoint for a long-running discovery or reconstruction operation SHOULD preserve, where material:

- source/provider identities;
- acquired byte digests and immutable source references;
- provider-manifest state;
- normalized versus reconstructed data distinctions;
- search/reconstruction parameters;
- exact generated witness identities;
- failed searches or ruled-out branches;
- next evidence-acquisition or reconstruction action;
- explicit statement that discovery evidence is not proof, certification, or promotion.

Agent substitution must not erase provenance or convert generated evidence into an independently verified claim.

### 4.4 MATHCERT specialization

MATHCERT SHALL adopt the common policy with explicit certification-independence safeguards.

Its adoption SHALL require:

- exact rebind of claim/subject, route, candidate artifact, and evidence digests after interruption;
- preservation of authorship and verification provenance;
- explicit statement that operational state may transfer across agents, but certification authority and substantive independence do not transfer automatically;
- re-evaluation of any non-authoring or independence requirement when agent substitution materially affects that requirement;
- fail-closed behavior on certification disposition;
- prohibition on inferring certification from continuity receipts, CI success, protected integration, or predecessor-agent conclusions.

A MATHCERT continuity receipt SHALL NOT serve as evidence that a certification independence condition has been satisfied.

## 5. Common machine contract

The rollout SHOULD converge on one common adoption schema rather than indefinitely duplicating validator logic.

A repository adoption record should minimally contain:

```json
{
  "policy_id": "GCL-AGENT-CONTINUITY-001",
  "version": "1.0.0",
  "repository": "grandchallenge/<REPO>",
  "required": true,
  "specialization": "<repository-local-specialization-or-null>",
  "authority_preservation": {
    "authority_changed": false
  }
}
```

A shared validator may later enforce universal fields. Repository-local validators remain responsible for specialization-specific invariants.

This shared-schema consolidation is a later implementation tranche and is not required to block initial repository adoption.

## 6. Implementation sequence

### Phase A — Programme binding

1. Bind the canonical policy from MATH-PROGRAMME `AGENTS.md`.
2. Add a machine-readable adoption record that declares the existing checkpoint machinery as the Programme specialization.
3. Add tests proving that the canonical mapping resolves to the existing checkpoint controls.
4. Do not create a duplicate continuity registry.
5. Run affected policy, routing, documentary-closure, and continuity checks.
6. Protected merge and readback under existing standing authority if the Council disposition authorizes this architecture.

### Phase B — Forge binding

1. Bind the canonical policy from MATHFORGE `AGENTS.md`.
2. Add a machine-readable adoption record.
3. Define a lightweight Forge checkpoint specialization for source/reconstruction operations.
4. Add validator coverage for provenance fields and authority-preservation clauses.
5. Register any new validation workflow with GH-OS routing.
6. Run protected repository checks and read back the admitted state.

### Phase C — Cert binding

1. Bind the canonical policy from MATHCERT `AGENTS.md`.
2. Add a machine-readable adoption record.
3. Add explicit anti-authority-inheritance and anti-independence-inheritance clauses.
4. Add adversarial tests proving that:
   - a predecessor agent's certification conclusion cannot be inherited as current certification authority;
   - a continuity receipt cannot satisfy an independence requirement;
   - a changed exact subject/evidence identity forces rebinding before certification action;
   - ordinary interruption recovery can continue without creating a new certification disposition.
5. Register any new validation workflow with GH-OS routing.
6. Run protected certification-policy and repository checks and read back admitted state.

### Phase D — Shared adoption schema

After the three repository adoptions are stable:

1. define a common adoption schema;
2. migrate MATHSOLVE and the other repositories to it without changing authority semantics;
3. retain repository-local specialization validators;
4. avoid introducing a central controller that can mutate pillar repositories or exercise their authority.

## 7. Review proportionality

This proposal changes governance/engineering controls but does not certify mathematics, weaken protected rulesets, or expand constitutional authority.

Requested Council offices:

- **Amanuensis:** continuity architecture, cross-document consistency, and authoritative integration;
- **Mechanist:** validator/workflow feasibility and repository-local implementation;
- **Cartographer:** cross-pillar dependency and rollout ordering;
- **Adversary:** failure modes, especially duplicate sources of truth and authority leakage.

The Referee office is not proposed as mandatory for this transaction unless the Council determines that a material security-sensitive or authority-expanding change has been introduced.

## 8. Executor gates

Executor work may be prepared before Council disposition but MUST remain fail-closed.

Before favorable Council disposition:

- no repository-local adoption is to be merged;
- no existing authority boundary is to be changed;
- no protected ruleset is to be weakened;
- no certification independence rule is to be relaxed.

After favorable disposition, each executor SHALL:

1. re-fetch live protected state;
2. reconcile any materially changed instructions or controls;
3. implement only its repository's approved specialization;
4. run affected checks;
5. merge only through protected controls;
6. read back the protected result;
7. record exact admitted identities in the Council docket.

## 9. Acceptance criteria

The rollout is complete only when:

- MATH-PROGRAMME, MATHFORGE, and MATHCERT each bind the canonical policy;
- each has a machine-readable adoption record;
- Programme uses its existing checkpoint machinery without a duplicate state model;
- Forge continuity preserves material source/provenance identity;
- Cert continuity cannot manufacture certification authority or independence;
- validators and routing registrations are green;
- protected merge/readback identities are recorded;
- MATHSOLVE remains conforming;
- no mathematical claim status or certification status changes as a consequence of this rollout.

## 10. Explicit non-goals

This proposal does not:

- modify the INTELLECT canonical policy;
- create a new Council quorum rule;
- require every routine PR to carry a campaign checkpoint;
- make conversational agents persistent controllers;
- transfer MATHCERT certification authority to another pillar;
- allow one agent's checkpoint to count as independent certification review;
- weaken protected branches, rulesets, required checks, or routing enforcement;
- convert CI success into proof, certification, publication, or claim promotion.

## 11. Requested disposition

Council disposition requested:

`APPROVE_BOUNDED_REPOSITORY_LOCAL_ADOPTION`

with authority for the executor dockets to implement Phases A-C under existing protected controls and repository authority boundaries.

Acceptable alternative dispositions:

- `APPROVE_WITH_CORRECTIONS`, naming exact corrections;
- `REQUIRE_BOUNDED_PILOT`, naming repository and success criteria;
- `REJECT_ROLLOUT`, naming the controlling conflict.

Until a favorable disposition is recorded, executor dockets remain `BLOCKED_PENDING_COUNCIL_DISPOSITION`.
