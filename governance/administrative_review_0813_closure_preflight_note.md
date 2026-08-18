# MP-ADMIN-ADMINISTRATIVE-0813-CLOSURE-PREFLIGHT-001

Successor execution repair under issue #554.

The protected August 13 receipt-recovery classifier is live-valid after PR #559, but the ordinary runtime still enters its BEHIND/full-executor preamble before the exact recovery can become observable. Candidate preparation itself is left unchanged; a post-#559 scheduled run proved that preparation completes from the repaired protected head.

The correction makes one exact-target closure preflight structurally first inside the existing single Referee/executor step. After ordinary non-authoritative candidate preparation and runtime-contract validation, the step invokes the protected `pending_closures` classifier before the BEHIND/full-runtime path. Only the exact issue #475 / merged PR #476 / record `MP-ADMIN-ADMINISTRATIVE-REVIEW-2026-08-13-001` tuple may be recovered, and only by delegating unchanged to existing `finish_closure` mechanics.

If the exact target is absent, the preflight is a no-op and the ordinary runtime executes as before. If the exact target completes, the step exits before the ordinary runtime so the checkout that predates the protected receipt merge is not reused. The existing single-use `github.token` Referee credential and all Candidate/Referee/administrator identity separation remain unchanged.

It does not authorize ordinary candidate finalization through the preflight, record re-execution or re-merge, direct completion-ledger edits, PR #558 mutation or merge, duplicate receipts, generalized closure recovery, cadence/deadline reset, structural-frontier mutation, bypass/direct protected push, or mathematical/source/certification/publication/external-claim authority.

Protected admission requires fresh exact-head machine gates, independent non-author exact-head APPROVED review, explicit Human Steward exact-head disposition, expected-head protected merge, and protected-main readback.
