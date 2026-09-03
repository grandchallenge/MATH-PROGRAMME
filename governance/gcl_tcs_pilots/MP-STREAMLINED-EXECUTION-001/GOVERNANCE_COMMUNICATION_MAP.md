# MP-STREAMLINED-EXECUTION-001 — GCL-TCS governance communication map

**Pilot artifact:** `MP-STREAMLINED-EXECUTION-001-TCS-PILOT-001`  
**Subject directive:** `MP-STREAMLINED-EXECUTION-001`  
**Source:** `docs/governance/STREAMLINED_EXECUTION_AMENDMENT.md`  
**Source blob:** `9c0e0895aa84ddf8402774070bfd7d0438a19a9f`  
**Primary profile:** `GCL-TCS-P07`  
**Secondary profile:** `GCL-TCS-P01`  
**Impact class:** `IC-2`  
**Pilot authority:** candidate / in review

## Purpose

This supplement maps the already-binding streamlined-execution directive into the GCL-TCS governance and operational communication model. It does not amend, restate with greater authority, or supersede the source directive. When this supplement and the source differ, the protected source directive controls.

The directive's central distinction is between routine execution ceremony and material authority boundaries. It removes repeat approvals that do not protect a material mathematical, certification, security, provenance, or authority boundary while preserving specialist review where such a boundary is actually present.

## Source authority lock

The subject directive records:

- control ID `MP-STREAMLINED-EXECUTION-001`;
- Human Steward directive date 2026-09-01;
- binding status on protected merge;
- explicit non-expansion of the control plane.

This pilot evaluates how clearly that instrument communicates its operating rules, evidence model, failure conditions, and reserved boundaries. It does not change the directive's authority status.

## Routine bounded execution model

For work already inside delegated scope, the source defines the operating sequence as:

1. classify the material evidence closure;
2. run the checks affected by that closure;
3. exercise the already-delegated disposition;
4. merge through the protected repository path;
5. read back the protected result.

A fresh Human Steward approval or generic independent-review ceremony is not added merely because a new commit exists. This rule applies only while the work remains inside already-authorized scope.

## Material evidence closure

The source binds evidence to the material object that can affect the conclusion, rather than to an arbitrary whole-repository head number. The closure includes changed governed bytes, directly consumed protected artifacts, relevant validators and schemas, workflows and toolchain pins, policy bytes, and the declared claim/authority scope.

Prior evidence becomes stale when a change affects that closure, creates a material conflict, or changes the relevant authority or claim boundary. Unrelated protected-main movement does not by itself invalidate evidence.

This distinction is essential for concurrent protected development: numerical SHA freshness is not a substitute for material dependency analysis.

## Concurrent-development rule

A candidate based on an older protected head can remain valid when:

- GitHub reports no material merge conflict;
- required checks for the candidate's material closure pass;
- no relevant protected dependency in that closure changed;
- the candidate does not widen its governed scope or authority.

The directive therefore prohibits synchronization commits whose only purpose is to make a base numerically current. A synchronization or rerun is required when material closure actually changes, not merely when `main` moves.

## CI proportionality

The directive requires impact-routed CI. Cheap classification and structural checks may run broadly, while expensive replay belongs only to affected material closures, explicit dispatch, or deliberate sentinel assurance.

For an unaffected expensive lane, a required status may be satisfied by a protected content-identity decision such as `UNCHANGED_ATTESTATION_REUSED`. This reuse must not weaken substantive independence: producer and independent-verifier state may not be collapsed merely to save runtime.

Unknown computational impact fails closed into the smallest defensible conservative affected set. Material-input routing is not a permanent exemption; deliberate sentinels must still exercise complete replay paths often enough to test the dependency maps themselves.

The source includes an Odd Zeta timing precedent. This pilot preserves that timing statement as a source assertion and does not independently remeasure or generalize it.

## Reserved boundaries

Streamlining does not erase materially necessary review. The source specifically preserves specialist or reserved treatment for matters such as:

- substantive mathematical certification;
- source-semantic adjudication;
- constitutional authority expansion;
- security-sensitive protection weakening;
- external claim promotion;
- any other transition whose governing instrument expressly reserves authority.

Where separation of duties is material, the reviewer must be an appropriately skilled non-author. Delegation cannot manufacture substantive mathematical independence when the same actor produced and certifies the same mathematical claim.

## Failure and ambiguity semantics

The directive is unsafe if the word "routine" is used as a blanket bypass. A transition is outside routine delegation when its material closure widens authority, changes a reserved source, weakens a security/provenance boundary, or otherwise crosses a governing reservation.

When dependency impact is ambiguous, the process must fail closed into the smallest defensible affected set. When a relevant dependency changes after validation, the affected evidence must be refreshed. When only unrelated repository material changes, refresh is unnecessary.

## Supersession model

The directive supersedes earlier routine-process requirements that demand fresh approvals, rebases, synchronization, or expensive unaffected CI solely because a new commit exists. Historical records remain historically accurate and do not need retroactive rewriting.

Supersession is narrow: earlier controls that protect a material reserved boundary remain effective unless the authoritative source expressly changes them.

## Pilot observations from current institutionalization

Two current transactions illustrate the intended distinction without creating new authority:

- PR #794 remained routine through Stage-A candidate merge, but a self-review change to its GCL-TCS gate mapping changed the candidate material closure. Earlier CI was treated as stale and the corrected exact head was rerun before merge.
- The same PR left G8 deferred after routine protected merge because independent Referee review is a material IC-2 promotion boundary under GCL-TCS. Delegated routine merge authority therefore did not become authority to self-approve G8.

The exact-head policy run for PR #794 also reused protected formal attestations for mathematically unchanged lanes while executing the affected governance/contracts checks. This is an observed instance of proportional routing, not a general productivity proof.

## What this pilot does not establish

This pilot does not establish that every historical or future transition was classified correctly. It does not measure organization-wide productivity, false-positive review burden, or false-negative governance risk. It does not independently revalidate the Odd Zeta timing figures. It does not authorize a source amendment, a new controller, weaker protection, mathematical or certification promotion, canonical Claim Ledger promotion, publication, novelty or priority claims, or external commercial claims.

G0-G7 in this candidate package are internal machine-assisted checks. They do not establish independent `CHECKED` or `ASSURED` status. G8 and G9 remain separate promotion/admission boundaries.