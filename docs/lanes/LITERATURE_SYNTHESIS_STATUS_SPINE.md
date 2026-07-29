# Literature Synthesis to Status Spine

## Obligation

Use this lane to turn a dated, source-bounded literature search into a theorem and status ledger. Every status statement must have a source identity, locator, complete hypotheses, and cutoff date.

## MATHFORGE

MATHFORGE conducts source discovery, reconstructs terminology, records search queries and dates, distinguishes primary from secondary sources, and flags conflicts or extraction gaps.

## MATHSOLVE

MATHSOLVE builds the status spine, separates established, open, conditional, disputed, and unresolved nodes, and prevents unsupported composition or novelty claims.

## MATHCERT

MATHCERT verifies source identities and locators, checks each ledger node against the cited statement, and certifies only source correspondence and bounded status assertions.

## Allowed statuses

`search_locked`, `sources_audited`, `status_spine_ready`, `ready_for_mathcert`, `rejected`.

## Rejection policy

Reject undated searches, locator-free claims, survey prose promoted beyond theorem hypotheses, hidden terminology changes, and novelty claims while priority or equivalence conflicts remain.

## Package

The package root is `lanes/literature_status_spine`. Its toy fixture demonstrates a dated source record and one established status node without making a novelty claim.

## Claim boundary

A status spine records what the audited sources support at the stated cutoff. It does not prove an open theorem or establish novelty by itself.
