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
- exact-main policy run `30450487344` at `813f53ea28e1d941cc16c8f3da517c0dcfdc08a5`;
- exact-main Pages run `30450675046`;
- validated-site artifact `8723277027`;
- byte-identical artifact and public index SHA-256 `9a54a3831d6fb0922b1e21a792c246051d1d8f078621fac5da5e87cdd59535c7`.

### Issue #125 — repository-ruleset enforcement

App-backed apply run `30450610588` updated and read back one active profile ruleset for MATHCERT, MATHSOLVE, MATH-PROGRAMME and INTELLECT. The evidence proves:

- repository-specific semantic checks plus shared `policy / policy` and
  `security / action-policy` checks are mandatory;
- strict required-status-check policy is active;
- pull requests and resolved review conversations are required;
- stale reviews are dismissed;
- force pushes and deletion are blocked;
- no bypass actor is present.

The run used a short-lived `gcl-release-trust` GitHub App installation token from the protected `release-trust` environment. The temporary human PAT was removed afterward, and verify-only run `30446476966` succeeded without it.

## Admitted release-trust evidence

- workflow run: `30450610588`;
- exact head: `813f53ea28e1d941cc16c8f3da517c0dcfdc08a5`;
- evidence artifact: `8723362498`;
- artifact SHA-256: `b6f153fda1ce0d80742828aa6ede7a51c0070e908babdc924df1fe6aef65a3da`;
- evidence-file SHA-256: `95f06401dfdd0cc5535c0d812e3818fd621db01dae5509b67f68ae9ff8d2e536`;
- canonical evidence SHA-256: `acd7e9c3ea10e9c03ea5dc81a0b84918d7241fea886426d2304e168b10c936f8`;
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
