# Grand Challenge Labs Governance

## Repository Roles

| Repository | Responsibility | Promotion Output |
| --- | --- | --- |
| `MATHFORGE` | Source reconstruction, candidate generation, and reconnaissance | Candidate problem card |
| `MATHSOLVE` | Work packages, theorem spines, reductions, and failure accounting | Certification handoff |
| `MATHCERT` | Formal proof, exact replay, and claim classification | Checked claim |
| `MATH-PROGRAMME` | Shared standards, schemas, domain registry, and roadmap | Versioned programme policy |

## Source Of Truth

Shared standards and schemas are canonical in this repository. A pillar may vendor
the subset required for local CI, but a policy change begins here and is synchronized
to affected pillars in an explicit pull request.

Issues live in the repository that owns the next action. Cross-pillar work is linked
through immutable commit URLs and stable identifiers. GitHub Projects is an index,
not a second source of truth.

## Branch Policy

`main` is the public record. Changes arrive through focused pull requests after the
relevant CI checks pass. Direct pushes are reserved for repository bootstrap and
time-critical administration.

## Maintainer Policy

`@fyremael` is the initial code owner and write-capable maintainer. During the
single-maintainer phase, pull requests and relevant CI checks remain mandatory, but
an approving review is not required because GitHub does not allow an author to
approve their own pull request.

When another independent write-capable contributor is active, restore the
one-approval branch rule and require code-owner review where appropriate.

## Promotion Rule

No artifact moves downstream without a handoff packet. No public theorem claim is
promoted without a MATHCERT status.
