# MP-MC-WP00 — MATHCERT provider pin review

## Identity

- Programme issue: `grandchallenge/MATH-PROGRAMME#123`
- MATHCERT provider merge: `3854dd1b4f6e162a7e74c3da1993f022ee691e5e`
- MATHCERT route-registry path: `governance/certification_routes.json`
- MATHCERT route-registry Git blob: `065f0531e4d763b389b207d4922d5a85b4335ee3`
- MATHSOLVE provider merge: `cdb34f47829942bd89a3f7f754b412527eaafb92`
- MATHSOLVE provider pull request: `grandchallenge/MATHSOLVE#74`

## Determination

MATH-PROGRAMME records the MATHCERT provider by exact commit and route-registry blob. It records each MATHSOLVE handoff by path and Git blob. It does not infer a Cert disposition from packet readiness.

The state boundary is:

- `pending`, `ready`, and `submitted` are routing or intake states;
- `certified`, `qualified`, `rejected`, and `proof_debt` are adjudicated states;
- only `certified` and `qualified` support positive mathematical promotion.

The Union-Closed, Navier–Stokes, and Hodge packets are ready in MATHSOLVE. Their pinned MATHCERT routes remain pending. They therefore cannot pass Judgment, Integration, or claim-promotion gates.

The BSD, P versus NP, Riemann, Yang–Mills, and Odd-zeta packets remain pending with explicit blockers.

## Hodge correction

The Hodge certification tracker is `grandchallenge/MATHCERT#23`. Pull request `#24` is an implementation artifact and is not the route issue.

## Claim boundary

This review establishes provider lineage and lifecycle semantics only. It certifies no mathematical claim. A ready packet is not a MATHCERT adjudication. A successful Programme policy workflow is not mathematical certification.
