# Programme Umbrella Release Audit — 2026-07-29

## Determination

CI contract coverage is complete.

The two remaining technical umbrella children are also complete:

- MATHFORGE issue #6 — bounded algebraic witness generation;
- MATHSOLVE issue #6 — bounded algebraic tactic routing.

Operational release closure is complete. MATH-PROGRAMME issues #7 and #125 are closed from exact, App-backed release-trust evidence. Therefore:

- `technical_children_complete: true`;
- `administrative_children_complete: true`;
- `operational_release_complete: true`;
- `operational_release_closure: COMPLETE`;
- `remaining_blockers: []`;
- umbrella issue #6: `CLOSE`.

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

## Completed administrative children

### Issue #7 — Pages release trust

The protected `Release trust administration` workflow verified:

- repository homepage `https://grandchallenge.github.io/MATH-PROGRAMME/`;
- exact-main policy run `30446169969` at `8b965d2e8913ed1252f37dc83de8456a335cedd9`;
- exact-main Pages run `30446339153`;
- validated-site artifact `8721515246`;
- byte-identical artifact and public index SHA-256 `9a54a3831d6fb0922b1e21a792c246051d1d8f078621fac5da5e87cdd59535c7`.

### Issue #125 — repository-ruleset enforcement

App-backed apply run `30446399649` updated and read back one active profile ruleset for MATHCERT, MATHSOLVE, MATH-PROGRAMME and INTELLECT. The evidence proves:

- repository-specific semantic checks and shared `policy / policy` checks are mandatory;
- strict required-status-check policy is active;
- pull requests and resolved review conversations are required;
- stale reviews are dismissed;
- force pushes and deletion are blocked;
- no bypass actor is present.

The run used a short-lived `gcl-release-trust` GitHub App installation token from the protected `release-trust` environment. The temporary human PAT was removed afterward, and verify-only run `30446476966` succeeded without it.

## Admitted release-trust evidence

- workflow run: `30446399649`;
- exact head: `8b965d2e8913ed1252f37dc83de8456a335cedd9`;
- evidence artifact: `8721612194`;
- artifact SHA-256: `719c28ea73b69cfcb07049988ab48f231c235160e8c2b01f48761b49623ac33e`;
- evidence-file SHA-256: `6c09d735c3b4f1ee4f5f53031658183ebc7a98a65fecc9c0eb9eca6a8ded2e74`;
- canonical evidence SHA-256: `a3cfeea6a58de0e193015b96fd5929567bae9a3ee2aca68efe52795474669a85`;
- verified: `true`.

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
