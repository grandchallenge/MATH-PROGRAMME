# Volume II Editorial Pass Status — COMPREHENSION RC1

## Purpose

This record reconciles the editorial state of **Volume II — COMPREHENSION: How Computational Worlds Are Built** with the exact comprehensive RC1 that is already durably admitted.

It also records a repository-layout fact that had become easy to misread: the top-level `volume-ii-comprehension/` source files were admitted earlier as the Stage-B1 teaching kernel and remain as historical provenance. They are **not** the exact comprehensive RC1 review target.

The exact comprehensive RC1 is the checksummed rebuildable source package under `releases/RC1/`.

## Exact comprehensive RC1 identity

- source archive SHA-256: `1e1f4ae917e50514dc0a74fa706d30ad0d1c3dbf9ac2f45d7c8ad2445f3fd95a`
- protected source-admission commit: `3615be3114ea3aceec14e02231e3a1647faa44b4`
- protected release tree: `8fae441820506bb6902e36c048cc475dc56242d5`
- protected readback: `PASS`
- Gate 8 review docket: issue `#853`
- review matrix: `reviews/RC1/THEOREM_REVIEW_MATRIX.json`

## Internal composition evidence

The protected RC1 release record fixes the following composition evidence:

- 96-page main monograph;
- 59-page complete solutions companion;
- 43-page plate folio with 42 canonical plates;
- 168 exercises and 168 keyed solutions or rubrics;
- 14 executable laboratories, 14/14 passing;
- camera-ready internal RC1 build and PDF preflight;
- release checksum identities.

The protected workset state additionally records completion of the formal theorem/claim audit, bibliography and historical-attribution audit, notation/index audit, and the 42-plate visual programme.

These are internal composition/editorial facts. They do not constitute independent mathematical review.

## Stage-B1 mirror and supersession rule

The following top-level artifacts originated in the Stage-B1 tranche and may contain historical Stage-B language:

- `main.tex` and its companion source files;
- `README.md`;
- `CLAIMS_LEDGER.md`;
- `THEOREM_AUDIT.md`;
- `ILLUSTRATION_REGISTER.md`;
- `BIBLIOGRAPHY_AUDIT.md`;
- `EXERCISE_AUDIT.json`;
- `PUBLICATION_AUDIT_RC1.md`.

They remain useful provenance for the first two-chapter teaching kernel, but they must not be used to identify the current comprehensive RC1 or its Gate 8 target. Where those files state `PLANNED`, `Stage B`, five plates, or 24 exercises, that language describes the historical Stage-B1 snapshot.

For current release state, use this order:

1. `WORKSET_STATE.json`;
2. `releases/RC1/RELEASE_RECORD.json`;
3. `releases/RC1/SOURCE_TRANSPORT_MANIFEST.json`;
4. `reviews/RC1/GATE8_REVIEW_PACKET.md`;
5. `reviews/RC1/THEOREM_REVIEW_MATRIX.json`.

Do not silently rewrite the historical Stage-B source into an approximation of RC1. The exact RC1 bytes are already fixed by the release archive and its SHA-256 identity.

## Editorial pass disposition

The current work set identifies no material defect in the exact admitted RC1 itself. The defect is editorial continuity: stale Stage-B1 top-level surfaces were not visibly separated from the later comprehensive release.

This reconciliation therefore changes repository legibility only. It does not change an admitted theorem statement, manuscript byte, claim scope, release hash, review packet, or review target.

## Current institutional state

| Axis | State |
|---|---|
| Composition | `RC_COMPOSITION_COMPLETE` |
| Durable admission | `RC_DURABLY_ADMITTED` |
| Independent mathematical review | `PENDING_EXTERNAL_MATHEMATICAL_REVIEW` |
| Publication authority | `NOT_GRANTED` |

## Remaining boundary

A genuinely independent mathematical reader must review the exact admitted RC1 through issue `#853`. The reviewer must independently check all fifteen mandatory formal results, the explicit non-results, and the claim boundaries fixed by the protected Gate 8 packet.

A self-audit, editorial reconciliation, executable regression suite, CI result, or this status record cannot satisfy Gate 8. A qualifying Gate 8 record may support `RC_REVIEW_QUALIFIED`; Gate 9 publication authority remains separate.
