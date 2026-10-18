# Erdős Compendium — documentary production protocol

State: ACTIVE_READER_REFERENCE_V2
Coverage authority: MATH-PROGRAMME/governance/erdos_catalogue/REGISTRY.json
Explanatory manuscripts: governance/erdos_compendium/editorial/NNNN.md
Publication: MkDocs on protected main, ci/erdos_compendium_hook.py
Claim authority: NONE — source evidence and independent mathematical certification remain separately governed

## Universal coverage, truthful depth

Every one of the 1,221 registered problem IDs has a stable reference page:
subject tags and snapshot status, the original problem link, GCL issue, and
explicit source/proof caveats. This is REFERENCE_COVERAGE, **not 1,221 reviewed
explanations**. The generator prints separate counts for catalogue coverage
and developed editorial articles and must fail closed on missing or duplicate IDs.

Do not invent mathematical statements from topic labels. No external agent
runtime, independent reviewer, solved result, source-authoritative theorem,
worker return, or MathCert conclusion can be inferred from registry metadata,
a GitHub issue, source audit, or a text generator.

## Admission boundary for authored manuscripts

A protected manuscript merge is **not** editorial acceptance. The site
generator reads `EDITORIAL_ADMISSIONS.json` and refuses to promote any
new `editorial/NNNN.md` into an explanatory public page or reviewed coverage
count unless a separate, protected editorial admission provides the **exact
SHA-256 of its stripped manuscript text**, source-claim check, recorded editorial critical check, protected admission PR, successful MkDocs run, and an
evidence-backed **public HTML and mathematical rendering readback**.
Absent admission evidence leaves the manuscript on its public page marked
**UNACCEPTED DRAFT**, with source link and an explicit noncertification warning,
excluded from the separately reviewed coverage count. This deliberately
allows the actual deployed Markdown/MathJax to be examined before a distinct
acceptance transaction; hiding the text until after deployed-text verification
would be a circular, impossible prerequisite. Changed accepted manuscript
bytes invalidate its existing admission, causing the generator to fail closed
until the review record is deliberately updated.
Transport `RESULT/1` or merged source alone never satisfies these fields.
The gate validates the evidence record's shape and source-hash identity;
the accountable editorial agent must verify that linked evidence supports the proposed acceptance decision; applicable protected approvals are still enforced. Never
equate a syntactically valid link with proof of successful verification.

The original #1–#3 are narrowly grandfathered as **legacy authored
exemplars** to avoid silently withdrawing existing historical pedagogy.
They are visibly marked as not separately accepted, are excluded from the
reviewed count, and the grandfather rule must not expand to later manuscripts.
At the initial gate cutover, #4 and #7 were both authored **visible drafts**.
The protected `EDITORIAL_ADMISSIONS.json` is the current editorial authority,
not this historical prose: the generator checks the exact source hash before
promoting an article into the reviewed count. Erdős #4 remains an unaccepted
draft without its own admitted ledger row. Erdős #7 is separately admitted
**only upon protected merge of the proposal referencing the verified source
and rendered-site evidence**. New contributions, including #9 and #10, use
the same ledger.
The full site can deploy with these reference entries; acceptance requires
actual deployed HTML verification in a separate transaction. Editorial
acceptance does not grant mathematical certification.

## How to produce each genuinely complete explanatory article

1. **Bind the exact problem.** Read its current external statement and dated
   sources, and its pinned catalogue snapshot and GCL issue. Record any
   status drift. Check variants and quantifiers before paraphrasing.
2. **Check evidence.** Reconcile existing Forge/Solve/Cert protected work,
   returned RESULT/1 comments, reviewer dispositions and mathematical
   counterexamples; distinguish a local lemma from parent-conjecture closure.
3. **Author to the template.** Add precisely one
   governance/erdos_compendium/editorial/NNNN.md with all six H2 headings:
   question in plain language; small example; what is known; GCL's current
   state; what remains; sources and claim boundaries. Use exact mathematical
   typesetting. Avoid synthetic proof figures or unverified current statuses.
4. **Accountable editorial self-check.** Verify that the small example is valid,
   the theorem statement matches its primary source, the language does not
   imply novelty/certification, each reported GCL outcome exists in protected
   state, and an open case remains open.
5. **Protect, publish and separately admit.** Route the authored manuscript
   through normal documentation CI. The build first generates a conspicuously
   UNACCEPTED DRAFT page, **excluded** from reviewed coverage. Read back both
   the actual GitHub and deployed mathematical rendering; only then propose
   a SHA-256-bound `EDITORIAL_ADMISSIONS.json` row through a separate protected
   PR satisfying its applicable branch-protection checks and approvals. Its merge may promote the reviewed
   coverage count. Never equate editorial signoff with mathematical proof
   certification or require routine Human Steward approval.
6. **Correction and revision.** If the live mathematical status changes,
   edit the authored article in a new protected PR; never silently infer that
   the frozen snapshot label has become current truth.

## Production order and duplication rule

Use existing catalogue audits and critical reviews before soliciting new
research. Initial article exemplars #1, #2, #3 are source-bound, manually
authored first-pass explanations. Next useful editorial candidates are the
returned, critically reviewed pilot subjects #4, #7, #9, #10, #99, #101,
#138, #241, #470, #593, #595, #1052; these have genuine RESULT/1 comments
or protected mathematical work, but are **not** thereby source-accepted.
First reconcile the latest claims/critical dockets, then write an article.
No duplicate MATHSOLVE mathematical job is authorized by this editorial list.

The existing 1,221 registered source-audit tasks are the entry point for
the rest of the catalogue; do not create 1,221 duplicate source jobs merely
to populate documentary pages. Expand editorial coverage across subject
families according to source-review readiness and actual mathematical
content. A completed, reviewable article is a better throughput measure
than total pages or task labels.

## Evidence and closure checks

- Generator checks source-commit lock, 1,221 unique problem IDs, issue
  identities, valid topic/status metadata, article section contract and
  expected generated page count.
- MkDocs strict build checks rendering. Hook checks public HTML sentinels and
  removes temporary generated Markdown; committed source remains registry
  plus authored manuscripts.
- The page itself shows a clear distinction between snapshot status and
  current mathematical proof/source authority.
- Proof/claim authority remains in protected Forge/Solve/Cert records;
  documentary source prose is a human model of that authority, never a
  replacement for it.
- The MkDocs compendium is a documentary **reference annex** and must not
  be added as a released illustrated documentary edition without a
  separately governed release-manifest/source-record transaction.

## Batch editorial operations (2026-10-12)

Routine explanatory articles may be authored and critically checked by the same accountable editorial agent. Record the check accurately as a self-review, including theorem/source matching, examples, notation, dates, and explicit claim limits. Do not describe a self-review as external mathematical certification.

Use risk-classified bulk batches: initially 50–100 routine articles per documentation PR, progressing to 200–250 once the first bulk batch passes quality sampling and automated controls. There is no four-article hard cap. Limit batches by review risk, CI/runtime capacity, and source readiness, not a fixed human approval quota. After protected merger and live rendering readback, group eligible SHA-256-locked admission records in a separate protected PR. Preserve all required evidence fields, existing CI, branch protection, and approval rules. The existing critical-review field may link to a clearly identified self-critical review record; it must never imply a different reviewer performed the work.

Escalate substantive mathematical contradictions, unresolved source ambiguity, potential new theorems, or changes to certified mathematical authority rather than silently approving them. An ordinary article does not need its own independent specialist review. A merged draft remains unaccepted until its admission is protected-merged and public HTML verified.

## Bulk scale acceptance controls

- Every article receives automated structural checks, exact-source identity, stable source references, portable mathematical notation and correctly scoped status/claim checks where machine-checkable. Unsupported factual claims and unverified calculations must be flagged, not accepted by sampling alone.
- Before batch admission, perform a deterministic recorded random sample of at least 10% of routine entries (minimum 10) plus all flagged exceptions, checking actual mathematical content, citations, examples, accessibility and deployed rendering. Use a reproducible committed sampling seed and per-article outcomes. Sampling does not substitute for checking each article's automated invariants.
- Material mathematical errors trigger a fail-closed batch hold, source correction and expanded sampling. Unresolved source conflicts are diverted to an exception lane; certification-sensitive changes remain on their own protected route.
- Admit successful batches through existing protected repository policy. Group evidence in one batch dossier and keep each admitted article bound to its own exact manuscript SHA-256 and source references. An individual article need not have its own PR or independent reviewer.
- The current admission schema and HTML gate stay effective until a separately tested, protected schema migration supports batch dossiers; no automatic promotion of draft content by this policy amendment.
- Track source-ready, drafted, automatically checked, sampled, admitted and rendered totals separately, and report errors and batch exceptions so volume cannot mask declining quality.

## Accepted article source-to-rendered publication parity (post-audit R2)

After a newly admitted batch deploys successfully, the accountable editorial
controller dispatches the EXISTING `erdos-compendium-public-html-readback.yml`
workflow for each newly accepted or source-amended article, with
`problem_id` from the protected admission register. The `accepted-parity` job
checks out current protected main, checks the actual latest successful Pages
deployment is from that exact commit, checks exact admitted manuscript digest,
compares all six substantive editorial sections and every mathematical TeX
expression against the published HTML, and verifies real MathJax-rendered
nodes in Chromium. It uploads a bounded result with the protected source SHA,
public HTML SHA, public URL, article identity and observed rendering count.

If site deployment is stale, the accepted/draft state differs, prose or maths
differs, or browser rendering fails, the job FAILS CLOSED. Retry only after
protected source and public deployment agree. Do not promote an unverified
result or treat a browser comparison as proof of the theorem. Unaccepted drafts
remain drafts and do not require this accepted-only check. This is part of
existing batch publication work, **not** a separate reviewer or admission
authority. Its actual accepted-article job receipt belongs with that batch's
existing editorial evidence.

## Automatic acceptance/publication parity and permanent evidence (post-audit follow-through)

The existing **successful Pages deployment** triggers `accepted-parity-auto` in
`erdos-compendium-public-html-readback.yml`. No editor needs to remember a
separate dispatch for newly admitted or source-amended accepted articles.
The job compares the exact current protected admission SHA-256 hashes with
`governance/erdos_compendium/publication_parity/COVERAGE.json`, checks up to
25 still-uncovered articles per protected run (their full six editorial
sections, mathematical TeX and live MathJax), and prepares a receipt.
A receipt does **not** become covered merely because an Actions job passed,
an upload-artifact was created, or a PR was opened: its source and HTML hashes
become covered **only after the corresponding normal PR has merged into
protected `main`**, with the individual evidence JSON stored under
`governance/erdos_compendium/publication_parity/receipts/`. Another Pages
build then follows; if more than 25 changed articles remain, the next batch
is handled in the following deployment/receipt cycle. Invalid source,
mislabelled acceptance, stale deployment, broken maths or failure to create
an authorized protected evidence PR must fail visibly, never register a PASS.
The existing Clerk application is used solely as the ordinary protected-PR
transport, not to bypass the merge queue or to certify mathematics.

The first ledger establishes a **prospective baseline** of the 650 previously
accepted entries, with a real #99 canary; it does *not* certify those 650
older pages. A historical acceptance may be re-checked by an ordinary
source change or a separately governed backfill. The original 30-day Actions
artifacts remain helpful for troubleshooting but are not the durable evidence.
The protected JSON receipt includes the source revision, actual deployed
revision, per-article source and rendered HTML digests, job ID, observed
MathJax count and noncertifying scope. This is part of ordinary editorial
publication assurance, not a new admission/review body.
