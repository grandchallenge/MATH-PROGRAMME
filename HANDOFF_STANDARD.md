# Cross-Pillar Handoff Standard

## Identifier Chain

Use stable identifiers that preserve the domain and source:

```text
MF-UC-0001
MS-UC-WP02-C003
MC-UC-WP02-C003
```

## Required Packet

Every handoff issue must include:

1. Upstream issue or release URL.
2. Immutable upstream commit SHA.
3. Domain and stable identifier.
4. Claim ledger path.
5. Support modality.
6. Promotion condition.
7. Named owner and next review date.
8. Knowledge graph references.
9. Versioned classification mapping references.
10. Discovery record references used for source reconstruction.

## Snapshot Policy

Create a GitHub release when a handoff is sufficiently stable for downstream work.
Downstream repositories consume a release tag or commit SHA, never an unpinned
branch reference.

External classifications travel with the handoff as mappings. They never replace
the stable domain, Work Package, or claim identifiers in the identifier chain.
