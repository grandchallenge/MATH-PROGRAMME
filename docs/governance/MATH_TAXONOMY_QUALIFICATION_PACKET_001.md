# MATH taxonomy qualification packet 001

## Review state

`CANDIDATE__INDEPENDENT_REVIEW_AND_PROTECTED_ADMISSION_PENDING`

This combined packet implements issue #469 at one exact revision. It does not
certify the proposed mappings or activate ADR-0020. The independent reviewer must
inspect the exact PR head, record findings, and either approve each candidate
mapping set or request corrections. Promotion from `CANDIDATE`/`PROPOSED` to
`QUALIFIED`/`AUDITED` must name the reviewer, review date, and review reference.

## Portfolio mapping packet

| Domain | Proposed primary MSC2020 | Secondary MSC2020 | Discovery facet | Status |
|---|---|---|---|---|
| UC — Union-Closed Sets | `05D05` Extremal set theory | `06A12` Semilattices | arXiv `math.CO` | existing audited mapping; IDs preserved |
| NSCI — Navier–Stokes | `35Q30` Navier-Stokes equations | `76D05` Navier-Stokes equations for incompressible viscous fluids | arXiv `math.AP` | proposed |
| HC — Hodge | `14C30` Transcendental methods, Hodge theory; Hodge conjecture | `14C25` Algebraic cycles | arXiv `math.AG` | proposed |
| BSD | `11G40` L-functions of varieties over global fields; Birch-Swinnerton-Dyer conjecture | `11G05` Elliptic curves over global fields | arXiv `math.NT` | proposed |
| YM — Yang–Mills | `81T13` Yang-Mills and other gauge theories in quantum field theory | `81T08` Constructive quantum field theory | arXiv `math-ph` | proposed |
| PNP — P versus NP | `68Q15` Complexity classes | `68Q17` Computational difficulty of problems | arXiv `cs.CC` | proposed |
| RH — Riemann hypothesis | `11M26` Nonreal zeros of zeta and L-functions; Riemann and other hypotheses | `11M06` ζ(s) and L(s,χ) | arXiv `math.NT` | proposed |

All MSC labels are snapshots from the official `MSC_2020.pdf` retrieved on
2026-08-12. Mapping JSON contains the fuller normative labels and evidence. The
official PDF SHA-256 is
`532d86f87b042b1fbc30b72be174c98db8d2fb8e28b4150733956998363bcbe7`.

## Ambiguity and reviewer focus

- NSCI: adjudicate whether the PDE-centered `35Q30` should remain primary over
  the fluid-mechanics `76D05` view.
- YM: adjudicate whether constructive QFT is the best secondary subject and
  whether additional mathematical-physics facets are useful without clutter.
- PNP: confirm MSC is sufficient as the external spine while ACM CCS remains an
  optional later domain facet, not a replacement.
- All domains: confirm the single-primary choice, label fidelity, relation, role,
  evidence, and whether any omitted secondary code is materially necessary.

## Machine serialization and license findings

The normative MSC2020 reference and TIB SKOS candidate are separate source
records. The TIB tree at
`33972ddb6a72c3660a6e499ee5f881b57fa92d41` exposes multiple candidate Turtle
files, including `msc-2020-suggestion2-incomplete.ttl`, and no admitted complete
payload/digest. It therefore remains `UNQUALIFIED_CANDIDATE` with
`runtime_authority: false`.

The programme records individual reviewed codes and labels but does not vendor the
CC-BY-NC-SA classification. Complete-dataset redistribution, derived
serialization, or commercial/product reuse remains blocked pending a separately
scoped terms review.

## Qualification measures

| Measure | Candidate result |
|---|---|
| Active-domain coverage | 7/7 have one non-rejected primary proposal; UC alone is already audited |
| Waivers | 0 |
| Primary ambiguity requiring explicit review | NSCI: 1 recorded choice between two direct codes |
| Automated/provider promotion | 0; validator rejects automated `AUDITED` mappings |
| Registry discovery | all `classification/mappings/*.json` and `knowledge_graph/*.json` discovered offline |
| Upstream runtime dependency | none in ordinary validation |
| Serialization qualification | TIB SKOS remains unqualified and non-authoritative |
| License boundary | reference-only use recorded; broader reuse requires review |

## Independent review checklist

- [ ] Exact PR head recorded.
- [ ] Seven primary choices reviewed together; disagreements recorded.
- [ ] Labels checked against official MSC2020.
- [ ] Mapping roles, relations, provenance, confidence, and cross-domain ownership checked.
- [ ] TIB candidate non-authority and fallback checked.
- [ ] License/redistribution boundary checked.
- [ ] Adversarial tests checked, including missing/duplicate primary, waiver conflict,
      provider self-promotion, wrong-domain reference, and unresolved target.
- [ ] Nonclaims checked.
- [ ] Reviewer disposition recorded without the author self-approving or self-merging.

## Nonclaims

This packet does not establish that any mapping is uniquely correct, qualify a
machine serialization, redistribute MSC2020, establish mathematical truth,
certify a result, choose research priority, change campaign state, or authorize a
protected merge. Green CI is necessary execution evidence only.
