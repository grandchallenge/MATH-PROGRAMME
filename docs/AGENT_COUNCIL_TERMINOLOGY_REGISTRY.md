# Agent Council Terminology Registry

## Status

Active programme register.

**Owner:** The Amanuensis.

This registry preserves canonical governance terms used across Agent Council documents, schemas, Work Packages, reviews, and integrated artifacts.

## Canonical terms

| Term | Canonical meaning | Boundary and exclusions |
|---|---|---|
| Amanuensis | The council office responsible for internal artifact continuity, decisions, terminology, review provenance, consistency, and editorial integration. | Does not certify mathematical truth or own external literature provenance. |
| Archivist | The council office responsible for literature provenance, attribution, priority, and the external historical record. | Does not own internal revision continuity. |
| Artifact ledger | The canonical register identifying each governed artifact and authoritative integrated version. | Not a claim ledger or certificate registry. |
| Decision record | A stable governance or integration choice stored under `docs/decisions/`. | Not a proof or substitute for source provenance. |
| Decision-record index | `docs/AGENT_COUNCIL_DECISION_RECORDS.md`, the canonical ADR navigation index. | Does not duplicate authoritative ADR bodies. |
| Terminology registry | The canonical record of governance terms and material term changes. | Not a general mathematical glossary. |
| Review provenance | Evidence identifying who or what reviewed an obligation and where findings are recorded. | Does not imply that a claim is proved. |
| Schema-bound Agent Council review record | A review conforming to `schemas/agent_review.schema.json` and explicitly registered for CI validation. | Legacy reviews are not schema-bound until migrated and registered. |
| Canonical claim ledger | A `ledger_contract: canonical_claim_ledger` record conforming to `schemas/claim_ledger.schema.json` and explicitly registered for programme validation. | A file name, Markdown table, or legacy claim list alone does not create canonical claim authority. |
| Claim-ledger registration | The two-way contract requiring every canonical ledger to be registered and every registered canonical ledger to exist with its contract marker. | Does not validate the truth of the claims; it validates trust-spine inclusion and shape. |
| Artifact lifecycle status | The stable machine phase in `artifact.status`. | Does not encode campaign-specific theorem strength. |
| Artifact disposition | A separate human-readable campaign qualification. | Must not silently create a lifecycle token. |
| Cross-document consistency | A recorded comparison among relevant authority surfaces. | Consistency does not establish correctness. |
| Final editorial integration | Controlled incorporation of specialist reviews and continuity records into one authoritative artifact. | Not merely copy-editing. |
| Authoritative integrated artifact | The artifact-ledger version designated as the current complete representation. | Drafts and superseded fragments are not authoritative. |
| Exposition and Continuity Kernel | The Cartographer, Steward, Composer, Grammarian, and Amanuensis preserving dependency, purpose, composition, language, and continuity. | Does not replace the full Council. |
| Amanuensis continuity state | The continuity state `pending`, `reviewed`, or `blocked`. | Not a mathematical claim status. |
| Mathematical execution pillars | MATHFORGE, MATHSOLVE, and MATHCERT as discovery, campaign, and certification sequence. | MATH-PROGRAMME is not a mathematical support stage. |
| MATH-PROGRAMME governance layer | The layer owning integration, governance, publication, documentation, and archives. | Cannot promote mathematical claims without the relevant support route. |
| Programme domain | A governed campaign with stable registry identity, entry, public page, governance refs, claim boundary, profile, and review date. | Does not imply progress or theorem completion. |
| Public domain landing page | A concise MkDocs route to a domain’s canonical entry and claim boundary. | Not a theorem ledger or source authority. |
| Documentation coverage contract | CI-enforced agreement among registry, pages, navigation, canonical entries, ADRs, historical notices, and authority pointers. | Build success alone is insufficient. |
| Governed root campaign artifact | An integrated root-level WP00 dossier with explicit identity and claim class. | Registration does not certify mathematics. |
| Campaign promotion register | The current documentary disposition record for integrated campaign artifacts. | Not a theorem ledger or certificate register. |
| Public status taxonomy | The public mapping among claim status, artifact lifecycle, and campaign disposition. | Does not replace machine schemas. |
| Subject spine | The primary external literature classification used to orient and retrieve mathematical work; currently MSC2020. | Does not define concepts, proof, truth, priority, certification, or programme state. |
| Subject mapping | A versioned reviewed assertion from a programme domain or graph node to an external subject identifier. | Similar labels do not establish concept identity or theorem equivalence. |
| Discovery facet | A non-authoritative category or provider signal used for retrieval and current awareness. | Provider assignment begins as proposed evidence and cannot self-promote. |
| Concept ontology | A vocabulary of mathematical concepts and semantic relations used as a design reference or crosswalk. | Is not the programme knowledge graph or subject spine. |
| Programme knowledge graph | The programme-owned graph of governed concepts and relationships. | External taxonomy edges do not silently become internal assertions. |
| Machine serialization | One encoded artifact representing an external vocabulary at an exact revision and digest. | A resolvable pin does not prove completeness, canonicality, or runtime authority. |
| Global programme policy gate | The repository-wide workflow running shared contracts, campaigns, repository tests, formal fixtures, and external evidence. | A green gate is execution evidence, not theorem support. |
| Governed campaign replay registry | The command authority for campaign replay and validation executables. | Does not define its own discovery boundary or infer correctness from exit status. |
| Code-owned executable discovery | Validator-owned classification of executable Python files by shebang or `__main__` guard. | Does not decide arguments or prove correctness. |
| CI policy reachability | The requirement that executable `ci/*.py` controls be reachable from operative workflow or replay roots through the local import graph. | Reachability is not semantic correctness. |
| Repository experiment reachability | The requirement that each library-only experiment module be imported by discovered repository tests, directly or through the local experiment graph. | A passing test does not establish a continuum, numerical, or mathematical claim. |
| Declared workflow environment | The runner family, governed Python minor line, and exact top-level dependency pins consumed by workflows. | Permits patch and transitive movement; not a full supply-chain lock. |
| Policy-validated site artifact | The run-scoped deterministic archive of the strict MkDocs output produced by a successful `main` policy run, with an inner digest. | Short-lived CI publication evidence, not a documentary release artifact or proof object. |
| Exact artifact publication | Pages deployment of the verified policy-produced site bytes without rebuilding them. | Does not establish deterministic equivalence across independent runs. |
| Cross-repository certification evidence | A schema-bound external repository, exact commit, paths, command, and claim boundary. | A moving branch or unchecked status is insufficient. |
| Retired path continuity | The condition that a removed path remains absent while replacement and historical references are governed. | Historical recoverability does not restore authority. |
| Historical identity crosswalk | A register mapping retired identity to current identity and enumerating permitted historical references. | Cannot rewrite historical review findings. |
| Current-tip publication | Publication requiring the validated SHA still to be current `main`. | Historical successful commits are not current publication authority. |
| Policy-gated publication | Publication only after a successful push-triggered global policy run and exact-artifact checks. | A site build, unrelated workflow, or stale commit is insufficient. |
| Non-probative reduction lane | A governed investigatory lane that may audit reductions, representations, risks, and bounded fixtures without supporting the target theorem. | Cannot change mainline result status or authorize mechanism escalation. |
| Instance-family undecidability | Undecidability of membership or behaviour across a computably represented family of inputs or initial data. | Does not imply independence of one universal mathematical sentence. |
| Formal independence contingency | The requirement that any independence claim name a formal system and supply a transfer metatheorem separate from dynamical undecidability. | Chaos, nontermination, or Turing completeness alone is insufficient. |
| Bounded interface fixture | A finite deterministic software object testing distinctions or API contracts under declared inputs. | Not a PDE simulation, reduction, non-halting oracle, singularity witness, or theorem certificate. |
| Documentary Library | The admitted public collection under `docs/documentaries/`, discovered through `ARTIFACT_MANIFEST.json`. | Pre-admission candidates are not collection members; publication is presentation, not mathematical support. |
| Documentary admission candidate | A source-locked documentary project registered in `DOCUMENTARY_CANDIDATES.json` before atomic public edition admission. | Candidate metadata do not confer manifest membership, a public page, an edition record, or release availability. |
| Documentary source lock | A governed record fixing candidate source scope, claim boundary, release identities, review, and next admission obligations. | Does not publish a browser edition or strengthen the target mathematics. |
| Pre-admission documentary source record | A repository-only pointer identifying a candidate complete source artifact before public edition admission. | Must remain outside `docs/` and is not an admitted public source record. |
| Repository-only source pointer | A source pointer retained under its governing campaign and excluded from the generated site until atomic manifest admission. | Repository visibility is not documentary publication or release availability. |
| Documentary source record | An admitted public pointer identifying a complete documentary source artifact. | Not the complete compilable source; candidate pointers do not enter this class before admission. |
| Authoritative documentary source artifact | The checksum-locked complete illustrated source bundle named by an admitted manifest or candidate source lock. | Identity does not establish public availability. |
| Rendered documentary edition | The checksum-locked PDF identified by the admitted manifest or candidate source lock. | Not the governing source. |
| Documentary web edition | A derivative browser-native presentation governed by schema and campaign authority. | Interactive features are not proof evidence. |
| Documentary edition record | A manifest-named `*.edition.json` instance defining one browser edition’s title, claim boundary, assets, sections, sources, palette, and rendering policy. | Not a source artifact or theorem ledger. |
| Documentary discovery authority | `docs/documentaries/ARTIFACT_MANIFEST.json`, the sole machine inventory of admitted collection editions. | Candidate registry membership and files appearing in directories do not imply admission. |
| Documentary candidate authority | `docs/documentaries/DOCUMENTARY_CANDIDATES.json`, the public metadata inventory of pre-admission source locks. | It cannot admit an edition or override the manifest. |
| Documentary claim status | The machine field `open` or `solved` governing status-sensitive validation. | Not reader-facing prose or artifact lifecycle status. |
| Documentary problem class | The machine class such as `millennium_open_problem`, `open_conjecture`, or `solved_classical_theorem`. | Does not itself state proof support or campaign promotion. |
| Documentary display status | Reader-facing status wording associated with a machine claim status and problem class. | Validation must not infer mathematical state from exact English wording alone. |
| Documentary file-class discovery | Bidirectional inventory checking for pages, edition records, admitted source records, candidate locks, assets, asset directories, root static files, and shared reader code. | File presence alone never creates authority. |
| Documentary edition tier | The expository class `reference`, `full`, or `orientation` recorded in the documentary manifest. | Tiers do not encode theorem strength, campaign promotion, or release availability. |
| Reference documentary tier | The canonical browser-reader substrate and most complete implementation exemplar. | Reference status does not strengthen imported mathematics or create a new proof. |
| Full documentary tier | A sustained narrative and technical treatment with greater depth than orientation while using the shared authority contract. | Full status is editorial, not mathematical promotion. |
| Orientation documentary tier | A complete but compressed first-principles map of the problem, theorem terrain, terminology, and guardrails. | May be expanded later; compression does not weaken claim boundaries or source obligations. |
| Release-class artifact availability | Whether an identified release artifact is `metadata_only` or a `published_release`. | A checksum without a locator is not publication evidence. |
| Metadata-only release identity | A governed artifact identity without a stable public release locator. | Must not be described as downloadable or published. |
| Documentary scope relation | The relation `campaign_documentary`, `parent_challenge_orientation`, or `solved_theorem_archive`. | Prevents scope conflation. |
| BSD-RANK-Q | Universal equality of Mordell–Weil and analytic rank over `Q`. | Excludes Sha finiteness and leading-term claims. |
| BSD-SHA-Q | Universal finiteness of `Sha(E/Q)`. | Not implied by rank equality. |
| BSD-LEAD-Q | Universal strong complex leading-term formula in campaign normalization. | Requires all explicit factors and quantifiers. |
| Solved-problem reconstruction campaign | A campaign reconstructing an established theorem’s sources, dependencies, audits, pedagogy, or certificates. | Not an open-problem attack or novelty claim. |
| Finite-extinction route | The Poincaré route from Ricci flow with surgery through topology bookkeeping to terminal discharge. | Finite extinction alone is insufficient. |
| Adversarial guard | A named false-proof fixture protecting a theorem interface. | Passing guards is not proof. |
| Theorem-interface reconstruction level | Exact theorem roles, hypotheses, conclusions, sources, dependencies, and boundaries. | Not independent proof or full formal verification. |
| Source correction ledger | A versioned record of source statements corrected, withdrawn, deferred, or reformulated. | Not a general errata list. |
| Topology event contract | A provenance-bearing interface for permitted topological consequences of a surgery transition. | Does not certify geometric occurrence. |
| Surgery-history certificate | A finite source-bound record validating event order, ancestry, equations, and terminal discharge. | Does not certify analytic Ricci-flow existence. |
| Imported event relation | A formal interface asserting a source-certified event’s recorded factor equation. | An assumption supplied to the evaluator. |
| Bounded evaluator certificate | A kernel-checked finite evaluator under explicit imported relations. | Does not certify imported relations or the full theorem. |
| Campaign-critical source concordance | Agreement in theorem role, hypotheses, corrections, and route relevance across governing sources. | Not sentence-level identity or independent verification. |
| Qualified solved-problem archive | A versioned dossier with explicit sources, dependencies, guards, certificates, debt, and claim boundary. | Not a new proof or full formal certificate. |
| CMDG | Certified Reconstruction of the Mathematical Dependency Graph; the ratified MATH-PROGRAMME Grand Challenge for machine-readable, provenance-bearing reconstruction and certification of mathematical dependency structure. | Not a claim to re-formalize all mathematics, prove foundation consistency, or infer semantic dependency from proof-assistant imports. |
| `GRAPH_CERTIFIED` | An orthogonal CMDG certification status asserting completeness relative to a versioned dependency manifest, declared closure policy, trust boundary, proof environment, axiom footprint, and reviewed dependency evidence. | Not synonymous with `machine_checked`; not an absolute claim that every mathematically relevant fact has been globally enumerated. |
| CMDG demonstration spine | A selected end-to-end certified route used to test the dependency architecture from foundations to a modern endpoint. | Does not assert that the route is mathematically minimal, historically canonical, or unique unless separately proved. |
| Foundational concordance | A certified relation between distinct foundational realizations of a mathematical object or structure, with explicit transport obligations and foundational profiles. | Shared names, informal analogy, or type equivalence alone do not establish concordance; required universal properties and interpretation bridges remain explicit obligations. |

## Change rule

A term is added or changed only when its decision, affected artifacts, consistency check, integrated authority, and ledger state are recorded.

ADR-0007 governs decision and review normalization; ADR-0008 and ADR-0009 govern public and campaign coverage; ADR-0010 governs admitted documentary authority, candidate authority, machine status, manifest discovery, source policy, and edition tiers; ADR-0011 and ADR-0012 govern global execution, discovery, environment, and current-tip publication; ADR-0013 governs the non-probative NS-CI-WP06 lane; ADR-0014 governs repository experiment reachability and exact-artifact publication; ADR-0017 governs CMDG programme authority, graph-certification terminology, demonstration-spine terminology, foundational concordance, and corrections `CMDG-C01` through `CMDG-C08`.
