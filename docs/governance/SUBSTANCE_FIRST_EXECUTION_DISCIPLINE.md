# Substance-First Execution Discipline

**Control:** `MP-SUBSTANCE-FIRST-EXECUTION-001`  
**Authority:** Human Steward directive, 2026-09-07  
**Status:** binding operating doctrine for substantive GCL work and handoffs  
**Relationship:** complements `MP-STREAMLINED-EXECUTION-001`; does not create a new approval plane

## Purpose

Keep the primary intellectual, scientific, technical, editorial, or product artifact as the object of optimization.

Governance, validation, provenance, CI, release engineering, handoff records, and repository mechanics are subordinate control systems. They may constrain substantive work where a material boundary requires it, but they must not displace the work they exist to protect.

This control exists because process can become locally rational while globally defeating the work set: more checks, manifests, reconstruction layers, repair branches, evidence packets, or state transitions can create the appearance of progress while the primary artifact receives little or no material improvement.

## 1. Objective lock

Every substantial work set must identify one **PRIMARY DELIVERABLE** and its **MATERIAL ACCEPTANCE CRITERIA** before mutation.

Every material activity must satisfy at least one of these tests:

1. it directly improves the primary deliverable;
2. it directly verifies an acceptance criterion;
3. it is the smallest necessary control action required to preserve correctness, provenance, authority, security, or reversibility;
4. it removes a demonstrated blocker to one of the above.

If an activity satisfies none of these tests, defer or abandon it.

The execution lead must not substitute a process objective for the primary deliverable. A successful workflow, green CI suite, release archive, merge, ledger update, or evidence packet is not substantive completion unless the work set itself makes that object the primary deliverable.

## 2. Artifact hierarchy

For substantive work, the default priority order is:

`primary artifact -> substantive verification/review -> minimal required governance/provenance -> convenience/process artifacts`

Examples:

- for a monograph: mathematics, proofs, exposition, figures, scholarship, exercises, solutions, and editorial quality outrank release machinery;
- for an experiment: hypothesis, implementation, data, controls, measurements, analysis, and reproducibility outrank dashboard or campaign ceremony;
- for software: behavior, correctness, tests, interfaces, maintainability, and deployment fitness outrank process documentation;
- for governance work itself, the governing instrument is the primary artifact, so doctrine quality and operational clarity are substantive work.

The hierarchy may be changed only when an exact governing instrument makes a lower layer a material prerequisite.

## 3. Process proportionality

Use the smallest process surface sufficient to preserve the material boundary.

Do not add a validator, manifest, archive format, reconstruction path, wrapper, checkpoint, review role, synchronization step, release packet, or state record merely because it could provide additional evidence.

A new process artifact or control step requires a concrete answer to:

- what material failure can occur without it;
- why an existing control does not already cover that failure;
- why the proposed mechanism is the narrowest adequate response.

If those questions cannot be answered, do not add the mechanism.

## 4. Material-progress rule

A continuation or execution tranche counts as **material progress** only when it does one or more of the following:

- improves the primary artifact against an acceptance criterion;
- resolves a substantive defect or uncertainty;
- completes a required substantive verification or independent review;
- crosses a genuinely required terminal control transition for an otherwise complete artifact.

Creating additional intermediate state, evidence packaging, transport identities, procedural records, or repair scaffolding is not sufficient by itself.

Status reports must distinguish substantive progress from process state.

## 5. Continuation discipline

Repeated continuation is evidence about the execution strategy.

If two consecutive continuations occur without material progress on the primary deliverable, the execution lead must re-plan before continuing the same path.

The re-plan must identify:

- the primary deliverable;
- what materially changed since the previous checkpoint;
- what current activity is consuming effort;
- whether that activity is required by an exact control;
- the shortest path back to substantive progress or terminal completion.

Do not respond to repeated execution-window exhaustion by merely serializing the same procedural plan into another continuation.

## 6. Remediation-recursion rule

A defect in supporting machinery does not automatically authorize more supporting machinery.

When a validator, workflow, release mechanism, synchronization path, archive path, or governance helper fails:

1. determine whether the failure blocks a material acceptance criterion or required authority boundary;
2. if not, route around, defer, or remove the failing mechanism;
3. if yes, repair the narrowest blocking defect;
4. do not broaden the remediation into a new platform or control plane without separately demonstrated need.

If remediation creates another remediation dependency, re-evaluate the original necessity before proceeding.

## 7. Claim discipline

Always distinguish at least these states where relevant:

- **produced** — bytes or results exist;
- **verified** — specified checks support specified claims;
- **reviewed** — an appropriate reviewer has examined the specified object;
- **admitted** — required protected or canonical persistence has occurred;
- **authoritative/publication-ready** — the governing authority and substantive quality threshold have both been met.

Machine evidence must not be used as a proxy for intellectual, scientific, mathematical, editorial, or product quality when those are separate acceptance dimensions.

A green build proves only what the build and checks actually test.

## 8. Drift tripwires

The following conditions require immediate re-planning, not another procedural continuation.

### `PROCESS_DOMINANCE`

Supporting process has become the dominant source of work or complexity while the primary artifact is materially unchanged.

Response: stop expanding process; identify the minimum remaining control path; return effort to the primary artifact.

### `REPEATED_CONTINUATION`

Two consecutive continuations occur without material primary-artifact advancement.

Response: re-plan under Section 5.

### `EVIDENCE_SUBSTITUTION`

Machine checks, manifests, state records, or procedural evidence are being treated as proof of substantive quality they do not test.

Response: stop the inference; perform the missing substantive verification or state the limitation.

### `REMEDIATION_RECURSION`

A repair to supporting machinery creates a further repair dependency.

Response: reassess whether the original machinery is materially necessary; route around it if possible.

### `OBJECTIVE_DRIFT`

The current activity cannot be traced to a material acceptance criterion or exact required boundary.

Response: abandon or defer the activity.

### `ARTIFACT_INFLATION`

New supporting artifacts are accumulating faster than required substantive outputs.

Response: freeze creation of supporting artifacts until each proposed artifact passes the process-proportionality test.

## 9. Handoff inheritance

Every future GCL handoff for a substantial work set must explicitly inherit this control.

Its first executable preflight must include:

```text
PRIMARY DELIVERABLE
MATERIAL ACCEPTANCE CRITERIA
CURRENT SUBSTANTIVE STATE
SMALLEST SAFE EXECUTABLE TRANCHE
MATERIAL CLOSURE
MINIMUM REQUIRED CONTROL PATH
PROCESS ARTIFACTS PROPOSED
PROCESS NECESSITY TEST: pass / fail
DRIFT TRIPWIRES ACTIVE: none / list
AUTHORITY REQUIRED: delegated / reserved
```

A handoff must not require a future agent to reproduce historical process that is no longer materially necessary. Preserve historical records as evidence; inherit only live controls and material dependencies.

If a domain-specific handoff conflicts with this discipline by requiring unnecessary ceremony, `MP-STREAMLINED-EXECUTION-001` and this control govern routine bounded execution unless the domain instrument protects a specific material boundary and explicitly reserves the stricter procedure.

## 10. Execution-lead self-check

At each meaningful checkpoint, the execution lead must be able to answer:

> If only the change in the primary artifact since the last checkpoint were shown, would this still constitute meaningful progress toward the work set's acceptance criteria?

If the answer is no, classify the work performed as process state rather than substantive progress and evaluate the drift tripwires before proceeding.

## 11. Terminal-state bias

Prefer completing one meaningful unit to a defensible terminal state over opening many partially complete surfaces.

Do not optimize for the count of commits, branches, artifacts, checks, handoff records, or intermediate gates. Optimize for satisfied acceptance criteria with the least process that preserves the required boundaries.

Once the primary artifact and all required acceptance criteria are complete, close the minimum required governance path promptly. Do not continue producing evidence after the governing boundary is already satisfied.

## 12. Non-expansion boundary

This doctrine does not waive mathematical review, certification, security, provenance, publication authority, or any other materially reserved boundary.

It changes the default execution question from:

> What more process could be added?

To:

> What is the least process necessary to protect the substantive result?

Where an exact protected instrument requires a control, perform it. Where it does not, substance remains primary.
