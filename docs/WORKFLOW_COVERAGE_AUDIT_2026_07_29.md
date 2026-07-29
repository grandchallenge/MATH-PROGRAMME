# Repository-Wide Workflow Coverage Audit — 2026-07-29

## Determination

CI contract coverage is complete at main commit `08dc04f34e0bb5e83a1555b3b0b6e55784dabfd1`.

Operational release closure is not complete. Issue #7 remains open on two repository-level facts:

1. a successful `Deploy documentation site` run for the current main revision has not been independently recorded;
2. the repository About section does not contain the Pages homepage URL.

Issue #6 therefore remains open.

## Completed corrective sequence

### Symbolic resource budgets

Issue #11 was completed through PR #120, merged at `242994ce3da70f4fa71c775715a5bbb3a6675f3c`.

The global workflow now rejects unregistered expensive symbolic lanes, missing or invalid budgets, missing backend and fallback data, suppressed failure evidence, orphan registrations, and successful runs without result artifacts. Exact-head policy run `30411135117` passed.

### Reusable cross-pillar lane packages

Issue #10 was completed through PR #121, merged at `08dc04f34e0bb5e83a1555b3b0b6e55784dabfd1`.

Exact finite enumeration, interval arithmetic, SAT/SMT proof artifacts, Lean formalization handoff, and literature synthesis now each have doctrine, schemas, a bounded fixture, controlled statuses, rejection rules, and a MATHCERT route. Exact-head policy run `30411923062` passed.

## Audited CI surface

The audit found machine-enforced coverage for:

- the global policy workflow;
- recursive campaign executable discovery;
- executable CI reachability;
- repository tests and experiment reachability;
- symbolic resource budgets and failure ledgers;
- the five reusable cross-pillar lane packages;
- MATHFORGE provider imports;
- MATHSOLVE routing;
- formal Lean replays;
- pinned external MATHCERT evidence;
- strict documentation construction;
- exact-artifact Pages publication semantics;
- BSD and Poincaré fast-path workflows.

The machine-readable audit is `governance/workflow_coverage_audit.json`.

## Pages verification

The public Actions inventory confirms that `Deploy documentation site` exists and has successful historical main-branch deployments. The repository's public About block shows a description and topics but no homepage URL.

The current connector can read repository state and has administrative repository permission, but it does not expose either unfiltered push-triggered workflow history or repository-homepage mutation. No additional repository-administration plugin is available.

## Close conditions

Issue #7 may close only after both facts are recorded:

- a successful Pages deployment tied to the current main commit and a public-site revision check;
- repository homepage set to `https://grandchallenge.github.io/MATH-PROGRAMME/`.

After #7 closes, repeat this audit with `operational_release_closure: COMPLETE`, then close umbrella issue #6.

## Claim boundary

Complete CI coverage means the declared repository contracts are reachable and fail closed under tested mutations. It does not establish mathematical truth, certification, publication permanence, or absence of future workflow defects.
