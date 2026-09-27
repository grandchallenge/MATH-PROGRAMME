# GCL-ID-00 Programme Adoption Profile

**Status:** Effective on protected merge of `governance/GCL-ID-00-ADOPTION.json`  
**Standard:** GCL-ID-00 v0.1.0  
**Admitted standard:** `grandchallenge/gcl-standards@fca21c1efef6dc3a560aa18c687579605c4579e0`  
**Governing issue:** `grandchallenge/MATH-PROGRAMME#1070`

## Purpose

MATH-PROGRAMME adopts GCL-ID-00 to catch a specific category error before substantial inverse-solver work: asking an estimator to recover distinctions that the declared observations do not contain.

The operating rule is:

> Before substantial solver expenditure, state what is being recovered, what the solver actually sees, what is already known to preserve those observations, and what object is therefore justified as recoverable.

This is an identifiability preflight. It is not a demand for a general injectivity theorem.

## Applicability

Apply this profile when a work package makes, tests, or materially depends on a claim that hidden state, parameters, calibration, representation, geometry, or another latent object can be reconstructed from declared observations.

Typical in-scope work includes inverse problems, parameter reconstruction, latent-state recovery, geometric reconstruction, calibration recovery, system identification, and learned inverse maps.

Do not apply it merely because a work package contains mathematics or computation. The following are out of scope unless they acquire a material reconstruction claim:

- ordinary forward computation;
- theorem proving without a reconstruction claim;
- numerical evaluation without latent recovery;
- exploratory work that does not claim recovery of a particular representative.

No retrospective rewrite of existing work is required. Existing campaigns enter scope only at a new material inverse/reconstruction tranche or when they make a new recovery claim.

## Default: ID-PREFLIGHT-LITE

The default record is deliberately small. Record five things:

1. **Recovery target.** What exactly is being recovered?
2. **Solver observations.** What information does the solver actually receive?
3. **Known observational equivalences.** What transformations or distinct states are already known to preserve those observations?
4. **Strongest justified recoverable object.** Full representative, quotient, invariant, partial object, set-valued object, or unresolved?
5. **Symmetry-breaking information.** What added measurement, normalization, prior, intervention, or compatibility condition would be needed for anything stronger?

The machine record uses `schemas/identifiability_preflight.schema.json` and lives under `governance/identifiability_preflights/`.

`UNRESOLVED` is a valid state. The preflight does not require proof of injectivity before experimentation.

## Escalation levels

### ID-PREFLIGHT-LITE

Use by default. Its purpose is a cheap category-error check before solver effort.

### ID-ANALYSIS

Escalate when identifiability materially affects the campaign, a nontrivial ambiguity is found, or a representative-level recovery claim remains consequential. Appropriate work can include exact invariance arguments, Jacobian/null-space analysis, orbit/stabilizer analysis, quotient coordinates, constructive indistinguishable pairs, or other problem-specific methods.

### ID-CERTIFIED

Use when an identifiability or obstruction statement itself becomes a mathematical claim that the Programme intends to rely on as certified mathematics. Route that claim through MATHCERT. The Programme adoption does not create certification authority.

## Interpretation rules

- Absence of a known symmetry is not proof of injectivity.
- Structural non-identifiability is not numerical ill-conditioning.
- Numerical ill-conditioning is not structural non-identifiability.
- A learned inverse can select one representative because of training distribution, architecture, regularization, or a canonicalization rule. Such selection must not be reported as information contained in the observation unless the evidence supports that claim.
- Once a structural ambiguity is established under an unchanged information set, a stronger optimizer is not by itself a response. Recover the quotient, add justified information, disclose a normalization, change the target, or challenge the ambiguity argument.

## Solver gate

This profile does not block experimentation.

Before **substantial** effort is attributed to full representative recovery, the work package must either:

- support full identifiability under its observation contract; or
- disclose the added information or normalization that selects a representative.

Otherwise, evaluate the solver against the strongest supported quotient, invariant, set, partial target, or explicitly unresolved target.

## Prospective observational review

The adoption is deliberately empirical about its own value.

Count completed in-scope preflight records prospectively after adoption. VGSE-ENG-WP06 is the motivating historical example and does not count toward this window.

Open a bounded review after at least 8 completed in-scope packages, target 10, and require the review no later than 12. Measure:

- whether the target changed;
- whether hidden prior, training, or canonicalization information was exposed;
- whether futile solver work was stopped;
- whether conditioning was distinguished from structural non-identifiability;
- whether the preflight was paperwork-only.

The review record is `governance/GCL-ID-00-OBSERVATIONAL-REVIEW.json` and validates against `schemas/gcl_id_observational_review.schema.json`.

If the profile becomes ceremonial or paperwork-dominant, simplify it through a separately governed revision.

## Historical motivating example

VGSE-ENG-WP06 established the motivating pattern:

- source-defined TE3 t-embedding: geometry determines all eight quotient directions;
- broader algebraic realization without TE3: geometry determines three quotient directions and leaves an exact five-dimensional ambiguity.

The lesson is methodological, not VGSE-specific: determine what the observation relation identifies before treating the residual as a solver defect.

Protected motivating evidence remains:

- Programme substantive merge `9663a9bc8f71af808ea4578a02467cfd47c29d92`;
- Programme terminal checkpoint `f132000f8308c65ac89c31d90d5e22df6c5dc56c`;
- MATHCERT TE3 audit `15b68c196d020045bea42fc34236e0647b87cbb9`.

## Authority boundary

GCL-ID-00 adoption changes Programme method, not mathematical truth.

It creates no mathematical certification, scientific claim promotion, publication, production activation, credential expansion, commercial claim, protected bypass, or autonomous permission escalation. MATHCERT retains its existing certification authority.
