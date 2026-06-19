# MATHSOLVE_SPEC.md

## Purpose

MATHSOLVE is the Grand Challenge campaign pillar. It is the disciplined middle between discovery and certification. It turns candidate problems into Work Packages, theorem spines, reductions, exact screens, failed attempts, restricted targets, pedagogical companions, and MATHCERT handoffs.

MATHSOLVE is where understanding is earned.

## Motto

> MATHSOLVE does not certify success. MATHSOLVE organizes the struggle.

## Why this pillar exists

MATHFORGE can identify promising mathematical ore. MATHCERT can check claims. Neither alone captures the craft of mathematical development. The Chaidez programme demonstrated that real progress often consists of carefully stated partial results, normal forms, reductions, negative corridors, exact computations, compact residual domains, and plain-language exposition. That craft is MATHSOLVE.

## Responsibilities

MATHSOLVE owns:

1. **Work Package production** with lay and technical components.
2. **Theorem spine construction**: definitions, propositions, lemmas, corollaries, examples, counterexamples.
3. **Status audit synthesis**: what is known, what is open, what is solved under special hypotheses, what has changed recently.
4. **Reduction strategy**: identify normal forms, equivalences, restricted regimes, and finite/infinite decompositions.
5. **Method routing**: classify local proof obligations, compare viable exact methods, and select routes under declared budgets.
6. **Proof-obligation decomposition**: separate semantics, encoding, adequacy, termination, local confluence, provenance, and final certification.
7. **Failure accounting**: record approaches that fail and the obstruction they reveal.
8. **Exact computational campaigns**: rational screens, exhaustive enumeration, algebraic elimination, certificate ledgers, and reproducibility notes.
9. **Witness minimization**: convert expensive discovery output into a smaller exact artifact suitable for replay.
10. **Pedagogical companion writing**: explain the object, obstruction, reduction, achieved result, and next target.
11. **MATHCERT handoff preparation**: theorem statements, formal definitions, missing library notes, certificate schemas.
12. **Programme reference preservation**: carry stable knowledge graph,
   classification mapping, and discovery record references through every Work
   Package and certification handoff.

## Non-responsibilities

MATHSOLVE does not:

- declare uncertified computations certified;
- treat synthesis as proof;
- hide assumptions;
- erase dead ends;
- publish a theorem claim without a claim ledger;
- infer mathematical failure from resource exhaustion;
- infer confluence from one successful reduction path;
- accept a numerical root list where exact reality or multiplicity matters;
- require that every Work Package prove a theorem.

## Work Package types

A MATHSOLVE Work Package may be one of:

```text
STATUS_SPINE
LITERATURE_SYNTHESIS
NORMAL_FORM_REDUCTION
RESTRICTED_THEOREM
NEGATIVE_RESULT
EXACT_COMPUTATIONAL_SCREEN
ALGEBRAIC_GEOMETRY_CAMPAIGN
INTERVAL_CERTIFICATION_CAMPAIGN
FORMALIZATION_HANDOFF
COUNTEREXAMPLE_SEARCH
PEDAGOGICAL_COMPANION
```

A Work Package may combine types, but it must identify its primary type.

## Required Work Package sections

Every serious Work Package must include:

1. **Lay executive companion**.
2. **Formal problem statement**.
3. **Known terrain and source audit**.
4. **Claim ledger**.
5. **Theorem/proposition/lemma spine**.
6. **Proofs, computations, or failed attempt analysis**.
7. **Boundary between proof, evidence, and conjecture**.
8. **Next analytic target**.
9. **MATHCERT handoff**.
10. **Appendix for reproducibility and external audit**.

A computational campaign must additionally include:

1. representation and solution-correspondence audit;
2. computation contract and intended equivalence relation;
3. termination and adequacy statement for any reduction system;
4. structural forecast;
5. method comparison and selection rationale;
6. resource ledger;
7. failed-route ledger;
8. provenance from generated objects to source generators;
9. minimized witness;
10. independent replay status.

If canonical normal forms or a Groebner basis are claimed, the package must include a complete critical-pair disposition ledger.

## Work Package lifecycle

```text
Candidate problem
  -> WP00 intake card
  -> WP01 status spine
  -> WP02 definitions and formalization handoff
  -> WP03 restricted theorem or exact screen
  -> WP04 obstruction/counterexample/interval campaign
  -> WP05 synthesis or certified result preparation
```

Not every domain follows this sequence exactly, but deviations must be justified.

For an algebraic geometry campaign, the internal lifecycle is:

```text
AG-00 semantic and encoding audit
  -> AG-01 reduction contract, dimension, and support forecast
  -> AG-02 method comparison
  -> AG-03 bounded exact run with provenance
  -> AG-04 witness minimization
  -> AG-05 independent replay
  -> AG-06 MATHCERT handoff
```

## Proof-obligation decomposition

Every nontrivial exact symbolic campaign should separate:

```text
semantic obligation
  source claim and model class

encoding obligation
  source objects correspond to algebraic solutions

reduction obligation
  rules preserve the intended congruence

termination obligation
  reduction or completion cannot continue forever

local-confluence obligation
  required critical pairs close

construction obligation
  generated objects remain in the source ideal

certificate obligation
  the local claim follows from a compact exact artifact
```

A campaign may discharge only the obligations it actually needs. For one membership claim, an explicit coefficient identity is preferable to certification of a complete basis.

## Algebraic method routing

The computational algebraic geometry lane is defined in `docs/COMPUTATIONAL_ALGEBRAIC_GEOMETRY_LANE.md`. Its reduction and certificate contract is defined in `docs/REDUCTION_CERTIFICATE_FOUNDATIONS.md`.

MATHSOLVE must route by obligation:

- identity or ideal membership: exact reduction and a coefficient witness;
- universal implication over extension rings: ideal membership;
- universal implication over extension fields or domains: radical membership;
- structured square elimination: resultants before a full elimination basis;
- finite systems: favorable graded basis, quotient algebra, multiplication matrices, or FGLM;
- real solutions: exact isolation and lifting;
- singularity at one point: local standard bases and quotient dimensions;
- generator dependencies: syzygies and relation matrices;
- dimension and degree: Hilbert functions, Hilbert polynomials, or generic slicing;
- sparse Laurent systems: Newton polytopes, mixed volume, and sparse resultants;
- expensive target orders: basis conversion rather than direct computation where possible;
- parametric claims: branch conditions and specialized certificates.

The selected method must be justified against at least one alternative when the obligation is nontrivial.

## Certificate selection

Use the weakest sufficient certificate:

```text
membership
  f = sum(ai*gi)

radical membership
  f^N = sum(ai*gi)

basis validity
  critical-pair ledger

canonical normal forms
  basis validity + termination + adequacy

source-ideal preservation
  forward and reverse generator transformation matrices

parametric theorem
  branch conditions + specialized witness per relevant branch
```

Search output should be translated back into the original theorem vocabulary before handoff whenever practical.

## Success conditions

A MATHSOLVE package succeeds when it makes the next state of the problem clearer than the previous state. This includes:

- a new theorem;
- a verified small case;
- a useful normal form;
- a negative result eliminating a route;
- a careful synthesis of scattered literature;
- a formalization-ready definition layer;
- a reproducible computation;
- a smaller exact witness extracted from a larger search;
- a parameter branch exposing a missing hypothesis;
- an honest failure that exposes the true obstruction.

## Failure conditions

A MATHSOLVE package fails if it:

- reads like motivational prose without mathematical obligations;
- labels evidence as proof;
- lacks a claim ledger;
- lacks a next target;
- hides uncertainty;
- suppresses resource exhaustion or failed routes;
- discards generator provenance;
- promotes a generic computation across exceptional parameter values;
- does not teach the reader the problem’s structure;
- cannot be handed to MATHCERT in any meaningful form.

## Repository structure

```text
MATHSOLVE/
  README.md
  SPEC.md
  standards/
    GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md
    GRAND_CHALLENGE_PEDAGOGY_STANDARD.md
  domains/
    union_closed/
      WP01_status_spine/
      WP02_lean_handoff/
      WP03_known_bounds_synthesis/
      WP04_small_cases_and_certificates/
    erdos_straus/
    hadamard/
    alon_tarsi/
    osp_recoupling/
  lanes/
    computational_algebraic_geometry/
  templates/
    work_package_template.md
    claim_ledger_template.yaml
    cert_handoff_template.md
    algebraic_campaign_template.md
    reduction_system_card.yaml
    critical_pair_ledger.yaml
```

## MATHSMELT as internal stage

MATHSMELT is the internal refinement phase inside MATHSOLVE. It converts raw MATHFORGE leads into precise definitions, tractable subproblems, normal forms, theorem candidates, computational screens, and MATHCERT-ready claims. It is not the public pillar because MATHSOLVE is clearer and more serious.

## First obligation

The first MATHSOLVE domain, Union-Closed Sets, must not begin by promising a proof of Frankl’s conjecture. It begins by constructing a high-quality status spine, then a Lean handoff layer, then restricted finite and definitional lemmas.
