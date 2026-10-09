# Delegated material admission — bounded agent-reviewed profiles

**Control:** `GCL-DELEGATED-MATERIAL-ADMISSION-001`  
**Programme tracking:** [issue #1247](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1247)  
**Governing staffing:** effective `GI-STEWARD-0003` and `MP-STREAMLINED-EXECUTION-001`.

## What is implemented

A profile-based, fail-closed mechanical reviewer replaces the earlier one-off six-line
image deletion exception. Only a protected controller running source from `main`
may classify a pull request and submit an App review. The candidate cannot
change its own profile registry or reviewer program and then obtain automatic
admission: every eligible candidate must modify **exactly one already existing
top-level `docs/*.md` file**, and must be internal to MATH-PROGRAMME.

The initial profiles are deliberately narrow:

| Profile | Exact permitted byte operation |
| --- | --- |
| `DOC-FINAL-NEWLINE-001` | Append one missing terminal LF |
| `DOC-TRAILING-SPACE-001` | Remove up to 12 *single* trailing spaces on non-control narrative lines, never Markdown's double-space hard line break |
| `DOC-REDUNDANT-BLANKS-001` | Collapse runs of three or more blank lines without changing any content-bearing line (maximum 12 removed lines) |

The classifier rejects fenced code, display mathematics, embedded HTML, front matter,
CRLF and tabs, excessive size, source-path traversal, mixed edits, renames, and files
outside the exact admitted scope. Existing mathematical claims are not independently
judged, and no PR claiming scientific certification is made true by formatting.

## Evidence and authority

The protected reviewer reads the old and new file *bytes* from pinned GitHub
commit identities and verifies the head blob SHA against the changed-file record.
It computes content hashes and emits a structured exact-head GitHub review.
The Verifier and Adversary entries are explicit **role-scoped logical audit
passes in a single protected system**, never falsely claimed to be external,
separate runtime sessions, or independent mathematical reviews.

GitHub's one-approval rule, required exact-head validation statuses, current
reviewer identity, and the native GH-OS merge queue remain mandatory.
The App review is an *operational permission* for precisely this bounded
routine classification, not a general mathematical, security, constitutional,
promotion, or certification authority.

A missing/unrecognized profile, missing status, failed semantic exclusion, stale
head, mutated base, insufficient metadata or missing review evidence fails closed.
A failed attempt must not result in `APPROVED`; the target PR can still follow
its appropriate specialist review and protected merge.

## Rollout boundary and successor

The initial registry represents a limited **positive proof of agency**:
the protected controller can perform future bounded housekeeping under three
reviewed content transformations, without a repeated human approval.
It does **not** authorize unbounded documentation rewrites, Lean theorem changes,
governance-record edits, required-check modifications or release promotion.

The successor under #1247 is a separately governed
`GCL-AGENT-ADMISSION-SPECIALIST-001` control: independent material-class
checks that enforce required specialist evidence on the precise merge candidate,
even where someone provides a GitHub approval. Such a check must be shown to
work on both `pull_request_target` and `merge_group` before adding it to a
protected ruleset. Do not mutate a ruleset or the separate GH-OS routing controller
under the cover of routine admission.

## Operating measurement

Record protected runs, ineligible/fail-closed dispositions, approved exact heads,
merged queue heads, failed checks, and human interventions. Guard against a
reversion to per-commit Steward review; also guard against false negative
classifications being misinterpreted as specialist approval.

**Terminal acceptance:** protected merge of classifier/profile code and test
registry, successful CI including hostile tests, then a live future positive PR
through the App and native queue, and a live negative out-of-scope PR. Only
then may the broader routine profile tranche be reported as operational.
