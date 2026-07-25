# Domain 07 · P versus NP

**Campaign ID:** `PNP-001`  
**Mathematical status:** open problem  
**Programme state:** WP00 source, model, and encoding dossier merged  
**Governance:** `ADR-0009`

## Canonical challenge

Determine whether every decision language whose YES instances admit polynomially bounded certificates verifiable in deterministic polynomial time is itself decidable in deterministic polynomial time.

The target is the exact language-theoretic proposition `P = NP` or its negation under uniform finite algorithms, complete encoded bit-length, total malformed-input handling, and deterministic polynomial-time many-one reductions.

## Programme posture

`PNP-WP00` fixes the Turing-machine model, binary encodings, resource accounting, reduction certificates, exact SAT equivalence routes, stronger sufficient statements, neighbouring complexity classes, barrier scope, and false-proof seeds.

The next documentary stages are the executable false-proof atlas and the source-normalized algorithm, lower-bound, and theorem ledger. No unrestricted algorithm or lower-bound claim is authorized by WP00.

## Canonical artifacts

- [WP00 integrated audit](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/PNP-WP00-source-definition-equivalence-audit.md)
- [Charter](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/p_vs_np/WP00_SOURCE_DEFINITION_EQUIVALENCE/00_CHARTER.md)
- [Machine and encoding lock](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/p_vs_np/WP00_SOURCE_DEFINITION_EQUIVALENCE/02_MACHINE_AND_ENCODING_LOCK.md)
- [Merge record PR #88](https://github.com/grandchallenge/MATH-PROGRAMME/pull/88)
- [Catalogue-integration decision ADR-0009](../decisions/ADR-0009_POST_MERGE_DOMAIN_COVERAGE.md)

## Claim boundary

The programme has not proved `P = NP` or `P != NP`, produced a new polynomial-time algorithm for an NP-complete language, proved an unrestricted circuit or machine lower bound, established a new barrier theorem, or made a novelty claim.
