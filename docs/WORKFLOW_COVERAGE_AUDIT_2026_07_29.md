# Programme Umbrella Release Audit — 2026-07-29

## Determination

CI contract coverage is complete.

The two remaining technical umbrella children are also complete:

- MATHFORGE issue #6 — bounded algebraic witness generation;
- MATHSOLVE issue #6 — bounded algebraic tactic routing.

Operational release closure is not complete. MATH-PROGRAMME issues #7 and #125 remain open. Therefore:

- `technical_children_complete: true`;
- `administrative_children_complete: false`;
- `operational_release_complete: false`;
- umbrella issue #6: `KEEP_OPEN`.

## Completed technical children

### MATHFORGE bounded witness contract

MATHFORGE issue #6 was completed through PR #25.

- exact tested head: `95be2b36d1cfb6f64c3f4e64c0b5c71d2ef2def6`;
- successful Forge run: `30426791431`;
- merge commit: `5d6461b6812dd9a99d73ddf98904c33465bffca0`;
- witness schema blob: `517d96566f35a0563c2b4059338aac0738a0a1b7`;
- witness registry blob: `022ebb5dbffa6685aef1dcb9bea8b1d338c5e7ec`;
- governed demonstration witness blob: `a1e3a0eb61702430516f5961bbc4e44332f677ce`.

The Forge lane now requires local scope, exact backend identity, bounded variables, degree, runtime, basis size and intermediate terms, an expected witness, a fallback route, observed execution, a failure ledger and content-addressed registry admission.

### MATHSOLVE bounded tactic contract

MATHSOLVE issue #6 was completed through PR #77.

- exact tested head: `107312712da7fce228c7100c7d15a1ee45bae03a`;
- successful Solve run after the Forge re-pin: `30427137579`;
- merge commit: `1f763c3a554814f40806a424e8b2c83f3ec8d24e`;
- tactic schema blob: `845117b233ddb5676d59f0e2e6a43f8e17abb497`;
- tactic registry blob: `5ee8b1aa596172f3c7d96126e93809bc80e1dcda`.

The Solve lane now requires one local algebraic obligation, explicit rejection of global open-problem encoding, bounded resources, a fallback route, an expected witness, exact witness lineage, correct MATHCERT intake and adjudication states, and failure evidence for rejected or proof-debt routes.

## Remaining administrative children

### Issue #7 — Pages release trust

Two facts remain unresolved:

1. the repository homepage must be set to `https://grandchallenge.github.io/MATH-PROGRAMME/`;
2. a successful Pages deployment for current `main` must be recorded, together with evidence that the public site serves that revision.

The repository-side publication workflow is governed. The remaining debt concerns live repository metadata and deployment evidence.

### Issue #125 — protected-branch enforcement

The audit has exact-head success evidence for MATHCERT, MATHSOLVE, MATH-PROGRAMME and INTELLECT. It does not have authoritative ruleset or branch-protection evidence proving that:

- the required workflow is mandatory;
- branches must be up to date;
- review requirements are active;
- bypass actors are absent or explicitly governed.

The connected GitHub surface does not expose those administration records.

## Closure invariant

MATH-PROGRAMME issue #6 may close only when all of the following are true:

- all four child issues are complete;
- `remaining_blockers` is empty;
- `administrative_children_complete` is `true`;
- `operational_release_complete` is `true`;
- `umbrella_issue_disposition` is `CLOSE`.

The machine-readable authority is `governance/workflow_coverage_audit.json`. The schema and validator reject any attempt to close the umbrella while one child or blocker remains.

## Claim boundary

This audit governs repository workflows, provider contracts, release metadata and branch administration. It certifies no mathematical claim and does not convert a witness, tactic record, green workflow or public web page into a theorem.
