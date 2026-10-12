# Erdős Compendium — documentary production protocol

State: ACTIVE_READER_REFERENCE_V1
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
SHA-256 of its stripped manuscript text**, source-claim check, read-only
critical review, protected admission PR, successful MkDocs run, and an
independent, recorded **public HTML and mathematical rendering readback**.
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
protected reviewers must additionally check that linked evidence actually
supports an acceptance decision before authorizing ledger updates. Never
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
4. **Adversarial editorial check.** Verify that the small example is valid,
   the theorem statement matches its primary source, the language does not
   imply novelty/certification, each reported GCL outcome exists in protected
   state, and an open case remains open.
5. **Protect, publish and separately admit.** Route the authored manuscript
   through normal documentation CI. The build first generates a conspicuously
   UNACCEPTED DRAFT page, **excluded** from reviewed coverage. Read back both
   the actual GitHub and deployed mathematical rendering; only then propose
   a SHA-256-bound `EDITORIAL_ADMISSIONS.json` row through a separate protected
   PR with actual non-author approval. Its merge may promote the reviewed
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
