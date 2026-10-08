# RH-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [RH-001 canonical tracker #163](https://github.com/grandchallenge/MATH-PROGRAMME/issues/163), with active Solve routes [A #411](https://github.com/grandchallenge/MATHSOLVE/issues/411), [B #412](https://github.com/grandchallenge/MATHSOLVE/issues/412), and [C #414](https://github.com/grandchallenge/MATHSOLVE/issues/414).  
    **AUTHORITY:** protected Programme/Solve records only, including Programme transition receipt `governance/rh_001_authority_transition_r080.json` for the protected RH-R080 Solve admission. The route issues and this guide do not certify mathematics.  
    **EXPOSITION:** this guide explains current protected state for readers; it does not promote claims.

## 1. Status

The classical Riemann Hypothesis remains open. GCL has a qualified statement/interface baseline and an active Solve-owned spectral programme, but no protected result proves RH or supplies an all-zero Hilbert–Pólya operator.

At the protected Solve state read for this guide (`e3c15b95722048be5ff0f186d85d24b41fd57a81`), three forward routes are active in parallel. RH-R080 is now protected on Route C via MATHSOLVE PR #1014.

## 2. Plain object

The campaign studies whether arithmetic/spectral constructions can force all nontrivial zeta zeros onto the critical line. The present forward work is narrower than “prove RH directly”: it isolates exact operator and determinant conditions whose closure would be sufficient, and proves or refutes those conditions one bounded theorem at a time.

## 3. Exact obstruction

The current bottleneck is not a lack of finite numerical evidence. It is the gap between finite self-adjoint approximants and a theorem strong enough to survive the limiting process.

Two nearby operator obligations are also active: extending the proved local simple-even theorem and controlling its continuation margins. Route C separately attacks the determinant-limit bridge and does not assume global simple-evenness.

## 4. Working model

The active routes are:

- **Route A — local analytic continuation.** Improve the protected simple-even interval by richer positive even trial spaces, stronger odd coercivity, sharper parity-sensitive remainder control, or a reusable combination. Tracker: MATHSOLVE #411.
- **Route B — Herglotz continuation.** Continue the parity theorem through quantitative control of pole-localization and Herglotz margins rather than repeated endpoint retuning. Tracker: MATHSOLVE #412.
- **Route C — determinant/projective-measure closure.** Produce an admissible finite CCM family with enough compactness, non-escape, projective-state control, and limit identification to invoke the protected localized Hurwitz/Rouché bridge. Tracker: MATHSOLVE #414.

Protected Solve lineage includes direct local simple-even control through RH-R054, quantitative Herglotz continuation through RH-R055, canonical determinant normalization through RH-R056, the RH-R077 correction/reframing of the downstream Route C architecture, and RH-R080 signed-projective normality. R080 proves that pointwise positivity is not required for the abstract C4 normal-family implication: on each strict substrip, uniform control of the signed-projective ratio `kappa_delta` is sufficient. Actual CCM `kappa_delta` control remains open. Later work must respect the R077/R080 corrections rather than revive withdrawn R071/R074 claims.

## 5. Restricted claim

What is supported is a structured theorem-development programme with protected intermediate results and explicit remaining gates.

What is **not** supported: RH itself; a new global zero-free theorem; an all-zero spectral operator; full determinant convergence; novelty/priority claims; or any inference from finite numerical gaps to the infinite theorem.

## 6. Theorem-spine location

Programme baseline:

- `RH-WP00-source-normalization-equivalence-audit.md`
- `governance/governed_campaign_registry.json`
- `governance/rh_001_authority_transition_r080.json` — Programme receipt for protected Solve merge/readback `e3c15b95722048be5ff0f186d85d24b41fd57a81`

Solve forward-state authority is carried by protected work packages and handoffs under `handoffs/RH-001/` and `work_packages/RH_*.md`. The current route architecture is summarized in `handoffs/RH-001/README.md`; Route C's corrected architecture must follow the RH-R077 projective-measure closure framing together with the protected RH-R080 signed-projective extension where they supersede older determinant-convergence assumptions.

## 7. Support route

The three routes are deliberately non-identical:

- A improves the direct local operator theorem.
- B transports the theorem through scalar/spectral continuation margins.
- C attacks the terminal determinant bridge and may consume A/B spectral control, but cannot assume unproved global simple-evenness.

This separation is a robustness feature: failure of one mechanism need not collapse the others.

## 8. Debt audit and claim boundary

Current material debt includes:

- Route A: structural extension beyond the present protected local frontier.
- Route B: stronger quantitative continuation beyond the protected no-prime margin results.
- Route C: an actually admissible cofinal family, projective candidate transfer, uniform actual-family `kappa_delta` control on each strict substrip (or a stronger valid substitute), and nonzero Xi-shaped limit identification for the actual CCM family.
- Cross-route: any dependency used downstream must be protected before reliance.

LIVE issues coordinate work. Protected repository records govern promoted theorem claims. MATHCERT alone can render a later certification disposition. This guide has no mathematical, certification, publication, novelty, or priority authority.

## 9. First executable step

Use the route tracker matching the intended theorem mechanism, claim one bounded subproblem, re-fetch protected MATHSOLVE state, and work only from the current route handoff plus protected predecessors.

For the research-surface stress test itself, use Programme issue #1230. Any discovered LIVE/AUTHORITY/EXPOSITION drift is a reconciliation defect to be surfaced explicitly; it must not be repaired by silently promoting a mathematical claim.
