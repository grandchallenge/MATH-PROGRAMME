# Grand Challenge: CMDG

## CMDG — Certified Reconstruction of the Mathematical Dependency Graph

**Document class:** Programme memorial and anti-drift reference  
**Status:** Human Steward-approved motivating architecture; proposed for protected repository admission  
**Council docket:** `COUNCIL-CMDG-001`, MATH-PROGRAMME issue #288  
**Purpose:** Preserve the full I–XIX programme formulation that motivated the Council submission, so later implementation, review, and refinement can distinguish deliberate evolution from accidental conceptual drift.

## Authority and use

This memorial records the motivating architecture approved in entirety by the Human Steward before submission to Council. It is intended to serve as the stable conceptual reference for `CMDG-CHARTER-001`, subsequent schemas, validators, concordance work, vertical spines, and frontier tests.

It does not itself prove mathematics, certify a dependency edge, establish consistency of a foundational system, promote a theorem, or supersede a protected Council decision. Where a later protected Council decision deliberately changes this formulation, the later decision controls and the change should be recorded as an explicit delta rather than silently rewriting this memorial.

The existing Programme architecture remains in force: MATHFORGE discovers and reconstructs sources; MATHSOLVE develops theorem spines and work packages; MATHCERT determines what crosses a trusted proof or replay boundary. The existing certification ladder and claim-ledger contract are extended by CMDG rather than replaced.

---

# I. First principle: we are not building another mathlib

The objective is not:

> Re-formalize all mathematics from scratch.

That would be wasteful and effectively unbounded.

The objective is:

> Reconstruct, expose, type, audit and certify the mathematical dependency relationships that allow modern theorems to stand.

Existing formal libraries become evidence and implementation substrates. We reconstruct selected foundational objects ourselves where doing so is mathematically significant; elsewhere we audit and attest upstream formal dependencies.

This gives three levels of engagement:

| Mode | Meaning |
|---|---|
| **REUSED** | Trusted upstream result imported and dependency-attested |
| **RECONSTRUCTED** | Definition/theorem deliberately rebuilt within the programme |
| **CONCORDANT** | Two or more foundational presentations are formally related |

The third category is where CMDG becomes scientifically distinctive.

---

# II. The object being constructed is not literally a DAG

There is an important technical refinement to the programme slogan.

Mathematics contains equivalences, mutual characterizations and interchangeable definitions. Therefore the raw structure cannot always be an acyclic graph.

Internally, CMDG should be a **typed directed multigraph**

\[
G=(V,E,\tau_V,\tau_E).
\]

Nodes represent mathematical objects such as:

\[
\text{Definition},\;
\text{Theory},\;
\text{Structure},\;
\text{Construction},\;
\text{Theorem},\;
\text{Equivalence},\;
\text{Model}.
\]

Edges have explicit semantics:

```text
REQUIRES_DEFINITION
USES_THEOREM
CONSTRUCTS
INSTANTIATES
GENERALIZES
INTERPRETS
MODELS
EQUIVALENT_TO
TRANSPORTS_ALONG
USES_AXIOM
USES_CLASSICALITY
IMPLEMENTATION_IMPORT
SOURCE_DERIVED
```

`EQUIVALENT_TO`, for example, can create cycles.

For dependency ordering we therefore construct

\[
G/{\sim}
\]

by collapsing certified equivalence components. The resulting **dependency quotient** should be acyclic.

This matters because we must never confuse:

\[
\text{Lean import dependency}
\]

with

\[
\text{mathematical dependency}.
\]

CMDG should maintain at least four overlapping graphs:

\[
\boxed{
G_{\text{semantic}},
G_{\text{proof}},
G_{\text{implementation}},
G_{\text{provenance}}
}
\]

That separation is fundamental.

---

# III. The programme has two dimensions

A purely bottom-up strategy would take years before touching the frontier.

Instead:

## Dimension A: Vertical reconstruction

Construct a thin certified path all the way from foundations to Condensed Mathematics.

## Dimension B: Horizontal closure

After the path works, progressively widen each layer until the important mathematical dependency structure is covered.

Conceptually:

```text
                         FRONTIER
                            ▲
                            │
                  thin vertical spine
                            │
                            │
FOUNDATIONS ───────────────────────────────────►
             progressive horizontal closure
```

This means architectural mistakes are discovered early.

If our notion of mathematical dependency cannot successfully carry a theorem into modern condensed mathematics, we should find out before spending years exhaustively cataloguing elementary algebra.

---

# IV. The certified spine

Adopt ten epochs.

| Epoch | Layer | First certification target |
|---|---|---|
| F0 | Formal substrate | kernel, proof terms, universes, axiom census |
| F1 | Logic and metatheory | syntax, semantics, soundness, compactness/completeness |
| F2 | Arithmetic | \(\mathbb N,\mathbb Z,\mathbb Q\), recursion, induction |
| F3 | Set theory | formal ZF/ZFC object theory; ordinals/cardinals |
| F4 | Structural mathematics | algebra, order, modules, morphisms |
| F5 | Category theory | functors, naturality, Yoneda, limits, adjunctions |
| F6 | Spaces | topology, compactness, uniform/metric structures, profinite spaces |
| F7 | Analysis | real/complex analysis, measure, integration, functional analysis |
| F8 | Sheaf/homological layer | sites, sheaves, abelian categories, complexes, derived machinery |
| F9 | Condensed frontier | condensed sets/groups/modules; solid/liquid structures |

This is not a linear dependency chain. F4–F8 form a branching DAG.

For example:

```text
                         F0 FORMAL SUBSTRATE
                                  │
                         F1 LOGIC / METATHEORY
                                  │
                 ┌────────────────┴───────────────┐
                 │                                │
             F2 ARITHMETIC                    F3 SETS
                 │                                │
                 └──────────────┬─────────────────┘
                                │
                   F4 ALGEBRA / ORDER
                      │              │
                      │          F5 CATEGORY
                      │              │
                      │        limits / adjunctions
                      │              │
            ┌─────────┴──────┬───────┘
            │                │
        F6 TOPOLOGY       F7 ANALYSIS
            │                │
            └───────┬────────┘
                    │
           F8 SHEAVES / HOMOLOGY
                    │
                    ▼
             F9 CONDENSED
```

Category theory deliberately occurs early.

---

# V. The first foundational experiment should be \(\mathbb N\)

This should directly continue the Euclid campaign.

Proposed operation:

**`CMDG-NAT-CONCORDANCE-001`**

Construct three presentations of the natural numbers:

\[
\mathbb N_{\mathrm{DTT}}
\]

as the native inductive natural-number type;

\[
\mathbb N_{\mathrm{ZFC}}
\]

as the set-theoretic/von Neumann realization inside an explicit set-theoretic object theory;

and

\[
\mathbb N_{\mathrm{NNO}}
\]

through the universal property of a natural numbers object.

Then establish appropriate equivalences transporting:

\[
0,\quad
S,\quad
+,\quad
\times,\quad
<,\quad
\mid.
\]

The ultimate bridge theorem should recover the Euclidean mathematics already certified:

\[
\gcd(a,b)
\]

through the transported structures.

So the programme literally begins:

```text
EUCLID-GCD
     │
     ▼
What exactly is ℕ?
     │
 ┌───┼────────────┐
 │   │            │
DTT  ZFC       categorical
 │   │            │
 └───┴─────┬──────┘
           │
     concordance
           │
           ▼
    Euclidean arithmetic
```

That is a much stronger successor to Euclid than simply starting with abstract set theory.

---

# VI. F1: Logic must become an object of mathematics

The first formal-system lane should contain:

```text
terms
formulas
substitution
variable binding
proof rules
interpretations
models
satisfaction
soundness
completeness
compactness
```

Existing formal libraries already contain substantial first-order model-theoretic infrastructure. CMDG should use such infrastructure as reference and upstream substrate where appropriate, while producing its own dependency description and trust classification.

A major rule:

> Lean proving a first-order theorem is not itself the same thing as formalizing the first-order proof system being studied.

CMDG must distinguish object logic from metalogic.

---

# VII. F3: ZFC is an object theory, not an assumption about Lean

This should be made explicit in the charter.

We do **not** say:

> CMDG is founded on ZFC.

Instead:

> CMDG's proof substrate is dependent type theory; ZFC is one formally represented foundational theory within that substrate.

And we explicitly make no assertion of the consistency of ZFC.

We can encode:

\[
\mathrm{ZFC}
=
\{
\text{Extensionality},
\text{Empty},
\text{Pairing},
\text{Union},
\text{Power Set},
\text{Infinity},
\text{Separation},
\text{Replacement},
\text{Foundation},
\text{Choice}
\}.
\]

Then distinguish:

```text
ZFC theorem
ZFC + Choice dependency
ZF theorem
constructive theorem
classical type-theoretic theorem
foundation-independent structural theorem
```

This is where the claim ledger's `foundational_profile` concept becomes operationally important.

---

# VIII. Every theorem receives a foundational fingerprint

For every certified major theorem \(T\), produce something conceptually like:

```yaml
theorem: gcd_exists

formal_system:
  prover: Lean
  substrate: dependent_type_theory

axiom_footprint:
  classical_choice: false
  excluded_middle: false
  quotient_soundness: false
  propext: false

mathematical_dependencies:
  - natural_numbers
  - divisibility
  - well_founded_induction

foundational_realizations:
  native_dtt: CERTIFIED
  zfc: CERTIFIED
  categorical: CERTIFIED

implementation_dependencies:
  - Mathlib.Data.Nat.GCD.Basic

semantic_dependency_complete: true
```

This is much more informative than merely saying “Lean checked.”

---

# IX. CMDG needs an additional certification condition

The existing Level 0–5 ladder continues to govern theorem certification.

A Level-5 theorem is not automatically a graph-certified theorem.

Define:

\[
\boxed{\text{GC5: Graph Certified}}
\]

as a programme overlay rather than Level 6.

A theorem becomes `GRAPH_CERTIFIED` only when:

1. its formal theorem is Level 5;
2. its direct semantic prerequisites are identified;
3. implementation imports have been separated from semantic dependencies;
4. the proof's axiom footprint is recorded;
5. every dependency edge has provenance;
6. equivalence/concordance claims have themselves been certified;
7. the theorem replays from the recorded environment;
8. there is no unresolved `sorry`, opaque assumption or undocumented oracle on the certified path.

Thus:

\[
\text{machine checked}
\not\Rightarrow
\text{dependency certified}.
\]

That is the central innovation.

---

# X. The structural bridge: Bourbaki + Grothendieck

F4 and F5 should deliberately reconstruct the transition:

\[
\text{elements}
\rightarrow
\text{structures}
\rightarrow
\text{morphisms}
\rightarrow
\text{universal properties}.
\]

Representative structural chain:

\[
\begin{aligned}
\text{Magma}
&\to
\text{Semigroup}
\to
\text{Monoid}
\to
\text{Group},\\
\text{Ring}
&\to
\text{Module}
\to
\text{Algebra},\\
\text{Preorder}
&\to
\text{PartialOrder}
\to
\text{Lattice}.
\end{aligned}
\]

But CMDG should then establish that many apparently elementwise constructions have a more structural formulation.

For example:

\[
\text{product}
\rightsquigarrow
\text{categorical product},
\]

\[
\text{quotient}
\rightsquigarrow
\text{coequalizer},
\]

\[
\text{free group}
\rightsquigarrow
\text{adjunction}.
\]

This is the point where the programme transitions from Bourbakist organization to Grothendieck-style organization.

---

# XI. First contact with Condensed Mathematics should occur earlier than the final capstone

There should be a frontier ladder.

## CM0 — Condensed contact

Certify the definition of a condensed object as the relevant sheaf construction.

## CM1 — Discrete/underlying adjunction

A suitable first endpoint is the discrete condensed-object functor and underlying-object functor forming an adjunction.

That requires enough category theory, topology, sites, sheaves and sheafification to meaningfully exercise the stack.

## CM2 — Cartesian closed condensed sets

A second endpoint is the Cartesian-closed structure of condensed sets.

This is an excellent structural load test.

## CM3 — Condensed abelian/homological structure

Move into condensed abelian groups and modules, limits, colimits and Grothendieck/AB machinery.

## CM4 — Solid mathematics

Move into formal machinery for solid condensed modules and solidification.

## CM5 — Liquid Tensor benchmark

The mature benchmark should be a certified dependency reconstruction reaching a substantial Clausen–Scholze result of Liquid-Tensor class.

The objective is **not** “prove Liquid Tensor again.”

It is:

> Demonstrate that CMDG can account for the mathematical and foundational dependency chain terminating in such a theorem.

That is a different achievement.

---

# XII. The historical Euclid lane remains alive

Hilbert and Tarski should form a lateral branch:

```text
Euclid
  │
  ├── explicit assumptions
  │
Hilbert
  │
  ├── first-order reformulation
  │
Tarski
  │
  ▼
formal geometry
```

It connects to F1 logic and F3/F4 structural foundations.

This closes the historical question:

> What exactly had to be added to Euclid before geometry became fully formalizable?

It should remain a named CMDG subprogramme rather than disappear after the Euclidean exemplars.

---

# XIII. Repository architecture

Recommended ownership follows the existing MATH institutional split.

## MATH-PROGRAMME

Owns the canonical graph.

```text
CMDG_CHARTER.md
CMDG_ARCHITECTURE.md

graph/
  nodes/
  edges/
  spines/
  concordances/
  frontier/

schemas/
  dependency_node.schema.json
  dependency_edge.schema.json
  dependency_manifest.schema.json
  foundational_profile.schema.json
```

## MATHFORGE

Owns source reconstruction:

```text
historical sources
modern references
formal-library concordance
source theorem identity
candidate dependency assertions
```

## MATHSOLVE

Owns mathematical reconstruction:

```text
definition spines
theorem spines
foundation concordance work packages
dependency reductions
missing-node analysis
```

## MATHCERT

Owns:

```text
Lean replay
axiom extraction
declaration dependency extraction
semantic-concordance verification
certificate validation
independent clean-room replay
```

This extends the existing three-pillar doctrine directly.

---

# XIV. Every dependency node gets a standard contract

Minimum record:

```yaml
node_id: CMDG-NAT-001
canonical_name: Natural numbers

node_type: STRUCTURE

informal_definition: ...
formal_realizations:
  - system: Lean
    declaration: Nat
    role: NATIVE_DTT

foundational_profiles:
  - DTT
  - ZFC
  - NNO

semantic_dependencies:
  - CMDG-INDUCTION-001
  - CMDG-RECURSION-001

equivalent_realizations:
  - CMDG-NAT-ZFC-001
  - CMDG-NAT-NNO-001

claim_ledger_refs: [...]

axiom_footprint: [...]

certification:
  theorem_level: 5
  graph_status: GRAPH_CERTIFIED
```

A dependency edge likewise becomes a first-class certified artifact.

This is the machine-readable backbone of the Grand Challenge.

---

# XV. Automated tooling

Three tools should be built very early.

## 1. Declaration Dependency Extractor

For a Lean declaration \(T\), recursively recover the formal declaration dependency graph.

## 2. Axiom Footprint Extractor

Produce the exact analogue of `#print axioms`, recursively and machine-readably.

## 3. Semantic Graph Reconciler

Compare:

\[
G_{\text{declared mathematical}}
\]

against

\[
G_{\text{actual formal proof}}.
\]

Then report:

```text
unexpected dependency
missing dependency
implementation-only dependency
classicality introduced
foundation boundary crossed
unresolved semantic mapping
```

This may become one of the most valuable pieces of infrastructure produced by CMDG.

---

# XVI. The first vertical spine

Keep Version 0 small.

```text
Lean/DTT substrate
      │
first-order logic
      │
natural numbers
      │
groups / rings
      │
categories
      │
topological spaces
      │
compact Hausdorff / profinite spaces
      │
Grothendieck topologies
      │
sheaves
      │
condensed sets
      │
discrete-underlying adjunction
```

That is **CMDG Vertical Spine V0**.

It deliberately omits measure theory, functional analysis and homological algebra.

Why?

Because it lets us test the entire CMDG machinery against a genuine modern endpoint quickly.

Once V0 passes, construct V1:

```text
rings/modules
     │
abelian categories
     │
chain complexes
     │
homology
     │
Grothendieck abelian categories
     │
condensed abelian groups/modules
```

Then V2:

```text
ℝ / ℂ
   │
topological vector spaces
   │
measure/integration
   │
functional analysis
   │
condensed modules
   │
solid/liquid mathematics
```

Only V2 represents the full “modern mathematical weight” test.

---

# XVII. Programme success criteria

The Grand Challenge should not be declared successful merely because a large graph exists.

A first major programme release should require:

\[
\boxed{\text{CMDG-1.0}}
\]

with all of the following:

1. a versioned typed mathematical dependency graph;
2. complete machine validation of graph structure;
3. certified separation of semantic, formal-import and provenance dependencies;
4. F0–F9 represented;
5. a fully graph-certified V0 vertical spine;
6. at least one significant cross-foundational concordance, beginning with \(\mathbb N\);
7. complete axiom footprints for every certified spine theorem;
8. no undocumented assumptions on the vertical path;
9. independent replay from pinned environments;
10. successful CM1 and CM2 condensed frontier tests;
11. a V1 homological/condensed-module path;
12. a documented route to the Liquid Tensor-class capstone.

The longer-term **Grand Challenge closure condition** is stronger:

> A substantial modern condensed-mathematics theorem must be reachable through a completely certified mathematical dependency path from the formal substrate, with every material dependency represented, typed, provenance-bound and independently replayable.

That is the defining experiment.

---

# XVIII. Immediate implementation sequence

Start with exactly these operations:

```text
CMDG-CHARTER-001
Define mission, graph semantics, non-goals and closure criteria.

CMDG-SCHEMA-001
Implement node, edge, manifest and foundational-profile schemas.

CMDG-VALIDATOR-001
Fail-closed graph validator plus mutation tests.

CMDG-LEAN-DEPENDENCY-EXTRACTOR-001
Extract declaration dependencies and axiom footprints.

CMDG-NAT-CONCORDANCE-001
Native DTT ℕ ↔ set-theoretic ℕ ↔ categorical NNO.

CMDG-EUCLID-BRIDGE-001
Transport the existing Euclidean arithmetic/GCD result through that concordance.

CMDG-VERTICAL-SPINE-V0-001
Register the first foundation→condensed dependency spine.

CMDG-CONDENSED-CM1-001
Certify the condensed discrete/underlying adjunction as the first frontier endpoint.

CMDG-CONDENSED-CM2-001
Certify the Cartesian-closed condensed-set endpoint.

CMDG-VERTICAL-SPINE-V1-001
Extend through abelian/homological mathematics.
```

Resist opening dozens of foundation work packages initially. These ten operations establish whether the architecture actually works.

---

# XIX. The programme thesis

The central proposition can be stated cleanly:

> **Mathematics is not merely a collection of certified theorems. It is a dependency-bearing structure of definitions, constructions, equivalences and proofs. CMDG seeks to certify that structure itself.**

Euclid gave us one of the first durable theorem graphs.

Hilbert exposed hidden assumptions.

Set theory provided a common universe.

Bourbaki organized mathematics by structure.

Grothendieck organized structures through morphisms and universal properties.

Type theory made proofs executable.

Clausen and Scholze provide a sufficiently demanding modern endpoint.

CMDG joins those stages into one auditable computational object.

The first implementation operation should therefore be **`CMDG-CHARTER-001` in `grandchallenge/MATH-PROGRAMME`**, followed immediately by the schemas and validator. No mathematical lane should begin before those contracts exist, because otherwise the Programme would again accumulate formalized mathematics without first defining what it means to certify its dependency structure.

---

# Anti-drift interpretation rule

This memorial is intentionally broader and more explanatory than the eventual machine contracts. Later schemas and work packages may refine terminology, split nodes, add edge classes, alter file layout, or strengthen certification gates. Such refinements are compatible with this memorial when they preserve the thesis and are explicitly documented.

A material departure includes, at minimum:

- collapsing semantic dependency into proof-assistant import dependency;
- treating `machine_checked` as synonymous with `GRAPH_CERTIFIED`;
- treating ZFC as Lean's unspoken metatheory rather than an object theory;
- abandoning cross-foundational concordance as a programme objective;
- replacing the vertical-spine strategy with exhaustive bottom-up formalization before frontier contact;
- declaring success from graph size or documentation volume without a fully certified modern endpoint;
- treating Condensed Mathematics as a branding endpoint rather than a load test of the reconstructed stack.

Any such departure should be presented to Council as a deliberate architectural change.

# Related Programme records

- `ARCHITECTURE_OVERVIEW.md`
- `CERTIFICATION_LADDER.md`
- `CLAIM_LEDGER_STANDARD.md`
- `docs/EUCLID_GCD_E2E_001_PROOF_TRACE.md`
- Council docket `COUNCIL-CMDG-001`, issue #288

This document is the memorial reference for the motivating CMDG conception from Sections I through XIX.
