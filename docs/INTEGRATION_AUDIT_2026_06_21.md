# Integration Audit — 2026-06-21

Status: audit complete; follow-up reconciliation recommended  
Scope: MATH-PROGRAMME documentation, pedagogy, Minderlings, classification/discovery contracts, and foundation-aware doctrine

## Executive summary

The programme standards are coherent at the level of intent. The merged stack now has:

- a visible MkDocs navigation path to the Pedagogy Standard;
- the Minderlings page implemented as a reader-facing mnemonic tool;
- classification/discovery schemas and validators from the reconciled Programme work;
- foundation-aware doctrine for structured objects, axiom profiles, witness policy, and pathology governance.

The remaining issues are integration gaps, not conceptual failures. The stack needs one reconciliation pass so older pages name the newer governing standard, foundation-aware doctrine appears in navigation, and the new `foundational_profile` requirement becomes schema/validator-backed rather than merely doctrinal.

## Audited artifacts

- `mkdocs.yml`
- `docs/GRAND_CHALLENGE_PEDAGOGY_STANDARD.md`
- `docs/PEDAGOGICAL_STYLE_GUIDE.md`
- `docs/CHAIDEZ_PEDAGOGICAL_PROTOCOL.md`
- `docs/MINDERLINGS.md`
- `docs/FOUNDATION_AWARE_MATH_PROGRAMME.md`
- `CLASSIFICATION_DISCOVERY_STANDARD.md`
- `ci/validate_programme.py`
- `schemas/*.json`
- `templates/work_package_template.md`
- `CLAIM_LEDGER_STANDARD.md`
- `DOMAIN_REGISTRY.yaml`

## Checks performed

### 1. Navigation wiring

Result: partial pass.

The MkDocs navigation includes:

- `MINDERLINGS.md` under Programme;
- `GRAND_CHALLENGE_PEDAGOGY_STANDARD.md` under Doctrine;
- existing Pedagogy, Chaidez, Cross-Pillar Lanes, computational algebra, reduction/certificate, Groebner/EXPSPACE, and resource-budget doctrine.

Gap: `docs/FOUNDATION_AWARE_MATH_PROGRAMME.md` is merged but not yet visible in MkDocs navigation.

Recommendation: add `Foundation-Aware Programme: FOUNDATION_AWARE_MATH_PROGRAMME.md` under Doctrine, near Pedagogy Standard and Claim Boundary.

### 2. Pedagogy consistency

Result: needs reconciliation.

The new Pedagogy Standard defines the current programme rule as rails before research and introduces a nine-move exposition pattern:

1. status box;
2. plain object;
3. exact obstruction;
4. working model;
5. restricted claim;
6. theorem-spine location;
7. support route;
8. debt and boundary;
9. first executable step.

The older `PEDAGOGICAL_STYLE_GUIDE.md` still describes an eight-move pattern and does not yet name the new Pedagogy Standard as governing. This is not a contradiction in practice, but it creates avoidable reader drift.

Recommendation: update the Style Guide header to say it is a companion to `GRAND_CHALLENGE_PEDAGOGY_STANDARD.md`, rename the eight-move section to a legacy/compact pattern or promote it to the nine-move pattern, and add support-route, semantic-bridge, corpus-quarantine, and mnemonic-aid language.

### 3. Chaidez protocol alignment

Result: mostly pass.

The Chaidez protocol already contains the strongest campaign mechanics:

- result-status box;
- theorem spine and dependency DAG;
- proof-debt register;
- computation taxonomy;
- trust quartet;
- escalation gate;
- pillar separation.

Gap: the computation taxonomy is narrower than the new standard. It lists exploratory evidence, regression audit, exact finite verification, and continuum proof, while the new standard adds certificate replay and formal proof as distinct support-route classes.

Recommendation: add a short amendment section to `CHAIDEZ_PEDAGOGICAL_PROTOCOL.md` saying that for new Work Packages, the computation taxonomy is refined by the Pedagogy Standard's support-route classes.

### 4. Minderlings integration

Result: pass.

The Minderlings page is now correctly framed as a mnemonic reader aid and coordination device. It explicitly says the Minderlings do not certify mathematics, replace reviewers, or create theorem status.

Gap: none blocking.

Recommendation: add one cross-link from the Pedagogy Standard to Minderlings and one cross-link from the Minderlings doctrine panel back to the Pedagogy Standard in a future small PR.

### 5. Classification/discovery integration

Result: pass with one terminology caveat.

The classification/discovery layer correctly treats external classifications and provider output as evidence, not authority. The validator checks graph references, mapping references, provider source IDs, duplicate graph nodes and edges, primary MSC mapping uniqueness, and audited status for primary mappings.

Gap: the Pedagogy Standard uses the phrase `external corpus quarantine`, while the classification/discovery standard uses `discovery evidence`, `external mappings`, and `human review`. These are compatible but should be made explicitly synonymous.

Recommendation: add a sentence to the Classification/Discovery Standard: "This is the machinery behind the Pedagogy Standard's external corpus quarantine rule."

### 6. Foundation-aware integration

Result: high-value doctrine; needs productization.

The foundation-aware doctrine is strong and should become a first-class Programme standard. It requires a `foundational_profile` block for cards, Work Packages, and certificate ledgers.

Gap: there is no matching schema or validator enforcement yet. Searches for `foundational_profile` show the requirement is currently doctrinal, not machine-checked. That is acceptable for the first merge, but should not remain unresolved.

Recommendation: add:

- `schemas/foundational_profile.schema.json`;
- optional `foundational_profile` fields in candidate problem, claim ledger, and work package templates;
- validator checks that profile fields are present for new artifacts where the doctrine requires them;
- examples for the Union-Closed domain.

### 7. Status wording and promotion boundaries

Result: mostly pass; one downgrade recommended.

The stack is consistent about not allowing visuals, provider classifications, or raw computation to become proof. The Pedagogy Standard explicitly says CAS output is not certification, Lean with `sorry` is not a theorem, and visualization is not evidence unless separately replayable.

Caveat: the foundation-aware doctrine says `Status: proposed programme standard` even though the PR has merged. That wording may confuse readers.

Recommendation: change its status line to `Status: active programme doctrine` or `Status: merged programme standard`.

## Severity-ranked findings

| Severity | Finding | Impact | Fix |
| --- | --- | --- | --- |
| High | Foundation-aware doctrine is not in MkDocs navigation | Readers may miss an active standard | Add nav entry |
| High | `foundational_profile` is required by doctrine but not schema-backed | Doctrine cannot yet be enforced by CI | Add schema + validator integration |
| Medium | Pedagogy Standard uses nine moves; old Style Guide says eight moves | Reader confusion, minor standard drift | Update Style Guide header and section |
| Medium | Chaidez taxonomy lacks certificate replay / formal proof classes | Campaign docs lag support-route taxonomy | Add amendment |
| Low | Corpus quarantine and discovery evidence terms are compatible but uncrosslinked | Mild vocabulary drift | Add cross-link sentence |
| Low | Foundation status says proposed after merge | Status ambiguity | Change status line |
| Low | Minderlings page could cross-link back to Pedagogy Standard | Better reader loop | Add link |

## Recommended follow-up PR

Title:

```text
Reconcile current operating standards
```

Files:

```text
mkdocs.yml
README.md
docs/PEDAGOGICAL_STYLE_GUIDE.md
docs/CHAIDEZ_PEDAGOGICAL_PROTOCOL.md
docs/GRAND_CHALLENGE_PEDAGOGY_STANDARD.md
docs/MINDERLINGS.md
docs/FOUNDATION_AWARE_MATH_PROGRAMME.md
CLASSIFICATION_DISCOVERY_STANDARD.md
templates/work_package_template.md
schemas/foundational_profile.schema.json
```

Minimum viable scope:

1. Add Foundation-Aware doctrine to MkDocs nav.
2. Update foundation status from proposed to active.
3. Add cross-links among Pedagogy Standard, Style Guide, Chaidez Protocol, Minderlings, Classification/Discovery, and Foundation-Aware doctrine.
4. Add `schemas/foundational_profile.schema.json`.
5. Add optional `foundational_profile` to work package template.
6. Do not yet enforce the profile in every historical artifact.

## Decision

The current stack is safe to proceed. It is not yet fully integrated.

Proceed with a small reconciliation PR before adding more doctrine or opening another major domain branch.
