# Erdős research-first execution contract (candidate)

**Scope:** existing `ERDOS-PROOF-VERIFICATION-001` (#3201), its already registered per-problem verification issues, and source-audit handoffs. **Authority:** operational/documentary refinement only; subordinate to `AGENTS.md`, `MP-STREAMLINED-EXECUTION-001`, source pins, MATHCERT and the atomic-adjudication claim gate. This document does not activate a new controller, rewrite an existing issue, or authorize a Solve campaign.

## Decision

A source-audit RESULT/1 or a catalogue explanation is a useful intake artifact, **not** the completion criterion for mathematical investigation. Each selected mathematical verification issue shall identify an executable proof obligation, an attempted attack, an adversarial check, and an evidence-backed disposition. Do not manufacture a positive result to satisfy throughput metrics.

The existing queue, proof-verification registry, manifests, checkpoint, and phase A–D coverage issues are the authoritative execution surfaces. Reuse them; do not create a second catalogue, parallel status taxonomy, or redundant per-problem tickets.

## Minimum research transaction

1. **Ground the problem.** Read current issue and every comment, exact primary statement and version, prior GCL mathematical receipts, existing MATHSOLVE/MATHCERT work, and the current Project eligibility/custody. Record quantifiers and known source discrepancies. Follow the existing atomic claim/duplicate gate for catalogue adjudications.
2. **Name one bounded mathematical target.** State a falsifiable lemma, proposed reduction, counterexample search, exact formal theorem replay, or numerical bound; its assumptions, dependency chain, and why success would change the frontier. A generic instruction to "investigate" is insufficient.
3. **Attempt the target.** Carry out a proof derivation, independent reproduction of a source argument, formal kernel replay with exact toolchain, or reproducible finite search. Report the actual operations, input identities, output and limitations. If the primary source is unavailable, document the exact access obstruction and do the strongest independent check still possible; do not call it verified.
4. **Adversarial pass.** In a separately identified non-authoring logical pass, test quantifier shifts, missing assumptions, edge cases, proof circularity, misuse of external theorems, and source-to-claim fidelity. Distinct logical passes are allowed under existing staffing policy; do not claim external independence from a single operator.
5. **Disposition and next decision.** Choose one of `VERIFIED_BOUNDED_RESULT`, `VERIFIED_COUNTEREXAMPLE`, `REPRODUCED_PRIOR_RESULT`, `FALSIFIED_APPROACH`, `BLOCKED_WITH_EVIDENCE`, or `INCOMPLETE`. Provide exact claim scope, proof/check receipts, novelty check, adversarial objections and response, source pins, and the next smallest attack. A reproduced theorem is not new; an empirical pattern is not a proof.
6. **Governed closure.** Apply existing manifest/ledger and Project procedures. Close a bounded issue only when its actual acceptance criteria and documentary obligations are met, then independently read back the issue and exact Project item. A catalogue review's administrative closure never certifies the underlying conjecture. Only the existing MATHCERT route can promote certification.

## Evidence template for the existing issue/RESULT/1

- `problem_id`, `issue_url`, `project_item_id`, `governing_manifest`, `custody_or_claim_sha`
- `source_lock`: primary citation, version/commit/hash, statement and hypotheses
- `prior_art`: exact existing GCL and literature results; independently checked versus merely reported
- `target`: bounded assertion, relevance to original problem, success/falsification criteria
- `attempt`: derivation or command, environment, input hash, receipt/log and reproducibility boundary
- `adversarial_review`: distinct pass, counterchecks, unresolved objections
- `outcome`: one disposition above, novelty classification and exact nonclaims
- `next_action`: smallest mathematically meaningful remaining obligation, owner/route and dependency
- `closure`: protected admission/readback where applicable; issue/Project status and exact evidence

## Research progress scorecard

Report **separately** (a) source audits, (b) source-locked claims, (c) genuine proof/counterexample attempts, (d) independently reproduced existing results, (e) verified bounded new results, (f) falsified approaches with witnesses, (g) blocked obligations, (h) formal replays, (i) MATHCERT certifications, and (j) administrative closures. Never sum these into one "problems solved" number.

For each sampled run, record useful research outcomes per execution, time spent on mathematical checking versus queue administration, repeated-source/duplicate work avoided, and unresolved blocker age. A negative result counts only with an explicit witness or argument; a timeout or unsupported conjecture does not.

## First pilot and acceptance

Use existing proof-verification pilot #3202–#3206 and the coverage parent #3201. Select **one eligible, unclaimed** issue from live state (the historical checkpoint pointed to #3204; revalidate before pickup). Require one complete source lock, one bounded mathematical attempt, one separate adversarial pass, and a reproducible receipt. Compare its output with the most recent catalogue-only adjudication: did it actually establish/refute/reproduce a mathematical assertion, or only describe a future task?

Acceptance of this operating refinement requires (1) a protected PR with applicable Markdown/impact checks and protected-main readback, and (2) at least one **separately evidenced pilot execution** meeting the above transaction. The PR alone establishes documentation, **not** scientific workflow success. If the pilot fails, retain the failure and revise the operating contract; do not mark programme transformation complete.

## Resource and safety boundaries

Reuse existing GitHub, CHAD, Lean/Colab and checkpoint infrastructure. No new recurring schedules, autonomous controller, unapproved Solve dispatch, bulk Project inventory, or routine full-suite CI. Honor atomic claims and exact repository identifiers; fail closed on incomplete comment pagination or source/claim custody. Do not relax mathematical independence, source pins, protected admission, or MATHCERT authority.
