# MP-EXTERNAL-EXECUTION-PLANE-001

**Status:** active on protected merge  
**Authority:** adopted `GCL-CEX-01` 0.1.0 and `MP-STREAMLINED-EXECUTION-001`  
**Scope:** scientific and computational campaign execution in the MATH-PROGRAMME estate

## Purpose

GitHub is the control, provenance, review, and evidence-admission plane. It is not the default high-fanout scientific batch scheduler.

Scientific computation may run on an external batch substrate when the governed operation, source bytes, work-unit domain, retry policy, and returned evidence remain exact and machine-verifiable.

This profile does not create a new mathematical, certification, publication, credential, production, or commercial authority.

## Control-plane duties

GitHub MAY:

1. hold protected source, campaign state, operation contracts, freezes, and manifests;
2. authorize and content-address an execution package;
3. submit or hand off that package to an external executor;
4. record immutable external execution identities;
5. verify returned receipts and complete work-unit coverage;
6. aggregate only after every required work unit is present and valid;
7. admit verified evidence through the ordinary protected review and merge path.

GitHub-hosted Actions SHOULD be used for CI, cheap deterministic preflight, packaging, receipt verification, aggregation checks, and bounded smoke execution.

## External-compute trigger

A scientific workload is `EXTERNAL_COMPUTE_REQUIRED` when any of these conditions is true:

- more than 32 independent scientific work units are required;
- a GitHub-hosted workflow would request more than 16 scientific jobs in parallel;
- the campaign would request more than 32 concurrent GitHub-hosted scientific jobs in aggregate;
- expected GitHub-hosted scientific runner consumption exceeds 240 runner-minutes;
- the workload requires a specialized accelerator, large-memory host, HPC scheduler, or batch facility not appropriate to ordinary CI.

An operation MAY retain GitHub-hosted scientific execution only through a bounded operational exception that states the capacity isolation and preserves estate CI headroom. The exception does not change scientific semantics or claim authority.

## External executor boundary

The external executor receives an immutable manifest and content-addressed inputs. It MUST NOT receive repository merge, protected-branch write, claim-promotion, certification, or release authority.

Provider selection is an operational choice. Cloud batch, Kubernetes, Slurm, hosted sessions, and other external schedulers are interchangeable only when the manifest invariants and receipt contract remain unchanged.

The executor MAY retry a failed work unit only under the frozen retry policy. A retry keeps the same work-unit identity and scientific inputs. Provider instance identity, host identity, and attempt identity remain operational evidence.

## Required manifest

Every external execution manifest binds:

- campaign and operation identity;
- exact source repository and commit;
- source payload SHA-256;
- scientific authority reference;
- complete work-unit domain and expected cardinality;
- scientific invariants that no executor may alter;
- operational parameters that may vary without changing the scientific subject;
- provider class and adapter identity;
- retry policy;
- required output artifacts and digests;
- claim boundaries.

The manifest itself is SHA-256 addressed before execution.

## Required receipt

Every work unit returns a receipt that binds:

- manifest SHA-256;
- work-unit identity;
- source commit and source payload SHA-256;
- provider execution identity;
- start and finish timestamps;
- return code and operational status;
- exact output artifact paths, sizes, and SHA-256 digests;
- `scientific_semantics_changed: false`;
- `promotion_claim: false`;
- `repository_mutation_performed: false`.

An operational failure is retained as operational evidence. It is not scientific infeasibility.

## Readmission

Returned evidence is not authoritative merely because an external provider produced it.

GitHub readmission MUST verify manifest identity, source identity, complete work-unit coverage, duplicate-free work-unit identities, output digests, receipt invariants, and campaign-specific semantic checks. Missing or invalid work units block aggregation.

Only the existing campaign authority may interpret or promote a scientific result. MATHCERT retains its separate certification authority.

## Existing executions

An execution already in flight before this profile becomes protected is grandfathered. It SHOULD NOT be cancelled solely to satisfy this profile when cancellation would discard valid exact work. Any retry or successor launch uses this profile.

## Claim boundary

This profile changes execution topology only. It does not establish a theorem, scientific result, runtime or cost superiority claim, hardware claim, novelty claim, publication authority, certification, or deployment authority.

## Documentary record

The protected admission and review record is registered at
`governance/rebuild_evidence/MP-EXTERNAL-EXECUTION-PLANE-001/closure_contract.json`.
That record distinguishes the substantively reviewed candidate, the later navigation-only
repair, and the protected merge. It records no unresolved documentary obligation and does
not widen the claim boundary above.
