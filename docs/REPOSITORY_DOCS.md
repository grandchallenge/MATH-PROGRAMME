# Repository Documents

The Pages site is the public front door. The full governed programme pack remains in the repository root and campaign directories. Root documents are repository-only unless a rendered page explicitly links to them.

Do not infer Pages URLs for root files. Use the canonical GitHub links below.

## Architecture and execution pillars

- [Architecture Overview](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/ARCHITECTURE_OVERVIEW.md)
- [MATHFORGE specification](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/MATHFORGE_SPEC.md)
- [MATHSOLVE specification](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/MATHSOLVE_SPEC.md)
- [MATHCERT specification](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/MATHCERT_SPEC.md)

## Standards and governance

- [Grand Challenge Work Package Standard](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md)
- [Canonical Pedagogy Standard pointer](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/GRAND_CHALLENGE_PEDAGOGY_STANDARD.md)
- [Claim Ledger Standard](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/CLAIM_LEDGER_STANDARD.md)
- [Certification Ladder](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/CERTIFICATION_LADDER.md)
- [Classification Discovery Standard](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/CLASSIFICATION_DISCOVERY_STANDARD.md)
- [Handoff Standard](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/HANDOFF_STANDARD.md)
- [Governance](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/GOVERNANCE.md)
- [Thurstonian Ethos](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/THURSTONIAN_ETHOS.md)
- [Domain Registry](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_REGISTRY.yaml)
- [ADR-0010 Documentary Authority](decisions/ADR-0010_DOCUMENTARY_LIBRARY_AUTHORITY.md)
- [ADR-0011 Full Workflow Coverage](decisions/ADR-0011_FULL_WORKFLOW_COVERAGE.md)
- [ADR-0012 Self-Authenticating Workflow Coverage](decisions/ADR-0012_SELF_AUTHENTICATING_WORKFLOW_COVERAGE.md)
- [Programme Workflow Coverage](WORKFLOW_COVERAGE.md)

## Canonical domains

- [Domain 01 · Union-Closed Sets](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md)
- [Domain 02 · Navier–Stokes Critical Integrability](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md)
- [Domain 03 · Hodge Conjecture](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md)
- [Domain 04 · Birch–Swinnerton-Dyer](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md)
- [Domain 05 · Poincaré Reconstruction](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md)
- [Domain 06 · Yang–Mills Existence and Mass Gap](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/YM-WP00-source-normalization-equivalence-audit.md)
- [Domain 07 · P versus NP](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/PNP-WP00-source-definition-equivalence-audit.md)
- [Domain 08 · Riemann Hypothesis](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/RH-WP00-source-normalization-equivalence-audit.md)

Domains 06–08 begin with integrated root WP00 dossiers rather than separate master-plan files. A later governed master plan may supersede those canonical entries only through an explicit registry and decision update.

Historical filename note: the detailed BSD plan remains recoverable under `DOMAIN_03_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md`. The mislabelled development-stage `DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md` was removed in PR #96; the canonical Poincaré entry is `DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md`. ADR-0005 and ADR-0006 govern the canonical numbering.

## Campaign directories

- [Navier–Stokes](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/navier_stokes_critical_integrability)
- [Hodge](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/hodge_conjecture)
- [Birch–Swinnerton-Dyer](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/birch_swinnerton_dyer)
- [Poincaré Reconstruction](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/poincare_reconstruction)
- [P versus NP](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/p_vs_np)
- [Riemann Hypothesis](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/riemann_hypothesis)

Yang–Mills currently uses its integrated root WP00 as the complete campaign entry.

Riemann Hypothesis post-WP00 records:

- [WP01/WP02 integration dossier](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/RH-WP01-WP02-post-WP00-integration.md)
- [WP01 false-proof atlas](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/riemann_hypothesis/WP01_FALSE_PROOF_ATLAS)
- [WP02 theorem ledger](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/riemann_hypothesis/WP02_THEOREM_LEDGER)
- [Post-merge retained-blocker disposition](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/riemann_hypothesis/RH_WP01_WP02_POST_MERGE_DISPOSITION.md)

RH-WP01 and RH-WP02 are implemented, merged, and CI-passed but remain formally unpromoted while their blocking legacy review dispositions remain in force.

## Documentary Library and release authority

- [Documentary Library](documentaries/index.md)
- [Release-artifact manifest](documentaries/ARTIFACT_MANIFEST.json)
- [Source-record policy](documentaries/sources/README.md)
- [Poincaré reference web edition](documentaries/poincare.md)
- [Reusable web-edition schema](documentaries/documentary_web.schema.json)
- [Poincaré edition record](documentaries/poincare.edition.json)

The committed `.tex` files are source records. The checksum-locked complete illustrated source bundle is the authoritative documentary source artifact, and the checksum-locked PDF is the rendered edition. Entries marked `metadata_only` have governed identities but no asserted stable public release locator.

## Union-Closed formal and exact baseline

- [WP01 Union-Closed Status Spine](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/WP01_UNION_CLOSED_STATUS_SPINE.md)
- [WP02 Union-Closed Lean Handoff](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/WP02_UNION_CLOSED_LEAN_HANDOFF.md)
- [Pinned cross-repository evidence](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/evidence/UC-WP02-MATHCERT.json)
- [External MATHCERT implementation](https://github.com/grandchallenge/MATHCERT)

The Union-Closed formal implementation is external, not a local `MathCert/` directory. The global programme policy checks out the exact MATHCERT commit in the evidence record and runs its complete certification gate.

## Workflow and publication controls

- [Global programme policy](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/.github/workflows/ci.yml)
- [Campaign replay registry](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/ci/campaign_replay_registry.json)
- [Campaign executable validator](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/ci/validate_campaign_replays.py)
- [CI policy reachability validator](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/ci/validate_policy_reachability.py)
- [Workflow inventory validator](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/ci/validate_workflow_coverage.py)
- [Workflow semantic validator](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/ci/validate_workflow_semantics.py)
- [Policy dependency declaration](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/requirements/policy.txt)
- [Documentation dependency declaration](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/requirements/docs.txt)
- [Pages deployment gate](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/.github/workflows/pages.yml)

The global policy independently discovers campaign executables, proves executable CI controls reachable from operative workflow roots, runs all governed replay and formal gates, and validates parsed workflow semantics. All jobs use fixed Ubuntu runners and checked-in exact top-level dependency pins. Pages deploys only a successful policy-validated SHA that remains the current `main` tip; a newer commit cancels or rejects stale publication. The dependency declarations are not represented as a complete transitive hash lock.

## Inventory and public entry points

- [Current File Manifest](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/FILE_MANIFEST.md)
- [Repository README](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/README.md)
- [Public Domain Catalogue](domains/index.md)
- [Campaign Promotion Register](CAMPAIGN_PROMOTION_REGISTER.md)
- [Programme Status Taxonomy](STATUS_TAXONOMY.md)

## Authority rule

The domain registry identifies canonical domain entries and public pages. The Agent Council artifact ledger identifies authoritative integrated governed artifacts. Claim ledgers, proof files, source records, governing source artifacts, and MATHCERT artifacts remain authoritative within their declared roles. Repository merge and CI can establish integration, declared-environment, reachability, and replay facts; they cannot prove the underlying open problem or override an explicit blocking review. Publication is permitted only after the successful policy-validated SHA is confirmed as the current `main` tip.
