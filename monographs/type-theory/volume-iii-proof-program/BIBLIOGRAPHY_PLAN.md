# Volume III Bibliography / Historical Attribution Plan

## Purpose

Volume III relies on a mature body of proof theory, typed lambda calculus, constructive logic, program extraction, control interpretations and parametricity. Historical names are not decorative labels. Each priority/date statement must be sourced, and the text must distinguish an exact theorem from a later synthesis or slogan.

No novelty claim about the Curry–Howard correspondence is planned.

## Primary and foundational source families

The publication pass must verify exact bibliographic metadata, edition/circulation dates, and the claim each source is used to support.

### Natural deduction, sequent calculus and cut elimination

- Gerhard Gentzen — foundational papers introducing natural deduction and sequent calculi and establishing Hauptsatz/cut-elimination results.
- Dag Prawitz — natural-deduction normalization and proof-theoretic development.

Claims to source precisely:

- origin and role of natural deduction;
- origin and role of sequent calculus;
- the exact scope of Gentzen's cut-elimination theorem used in historical exposition;
- normalization of natural deductions and its relation to proof detours.

### Typed lambda calculus and propositions-as-types lineage

- Alonzo Church — simply typed lambda calculus / simple theory of types context relevant to the computational side.
- Haskell B. Curry and collaborators — combinatory logic / type assignment lineage relevant to proofs-as-terms history.
- William A. Howard — formulae-as-types correspondence; distinguish manuscript/circulation/publication history.

Historical discipline:

- do not attribute the entire correspondence to a single event;
- distinguish Curry-style type assignment, Howard's formulae-as-types formulation, and later normalization/programming-language interpretations;
- where a source circulated long before publication, record both dates if the historical claim depends on that distinction.

### Constructive logic and dependent propositions-as-types

- Per Martin-Löf — dependent type-theoretic constructive foundations relevant to `Π/Σ` logical readings.
- Standard constructive-logic sources for intuitionistic natural deduction, Kripke semantics and classical/constructive distinctions.

Claims to source precisely:

- universal/existential readings of dependent products/sums;
- constructive witness content;
- nonderivability/countermodel discussion for selected classical schemas.

### Classical logic and control

- Foundational work connecting classical proofs with continuations/control, including Timothy Griffin's typed-control interpretation and relevant CPS/double-negation literature.

Claims to source precisely:

- which classical principle is represented by which control operator or translation;
- whether a result is a typing correspondence, logical soundness theorem, operational interpretation, or broader slogan;
- normalization caveats introduced by control.

### Polymorphism and parametricity

- Jean-Yves Girard — polymorphic typed lambda calculus/System F lineage where historically relevant.
- John C. Reynolds — relational parametricity / abstraction theorem lineage.

Claims to source precisely:

- exact assumptions behind parametricity/free-theorem reasoning;
- distinction between theorem and the finite relation checks in this volume's laboratory.

### Program extraction and proof assistants

Primary/system-specific references will be selected only for claims actually made. Candidate source families include:

- foundational propositions-as-types extraction literature;
- proof-assistant kernel architecture papers/manuals;
- extraction mechanisms for systems such as Coq where discussed;
- LCF-style small-kernel trust architecture where historically relevant.

The volume will not write one generic paragraph that attributes identical trust/extraction architecture to all proof assistants.

## Modern expository reference families

At least one strong modern reference should support each of these areas:

- proof theory and natural deduction;
- typed lambda calculus;
- intuitionistic/constructive logic;
- programming-language type systems;
- dependent types and proof assistants;
- continuations/CPS and typed control;
- parametricity;
- extraction and certified programming.

Candidate families to verify during the scholarship pass include standard texts by authors such as Troelstra/van Dalen, Sørensen/Urzyczyn, Pierce, Girard/Lafont/Taylor, and modern proof-assistant/type-theory references. Final inclusion depends on the exact edition and claim supported.

## Historical claims requiring explicit verification

1. The chronology and terminology behind the phrase “Curry–Howard correspondence.”
2. Gentzen's introduction of natural deduction and sequent calculus and the scope of Hauptsatz.
3. Church's typed-lambda-calculus publication context.
4. Howard manuscript/circulation/publication chronology.
5. Prawitz's normalization contribution and exact theorem context.
6. When the explicit programming-language reading of proofs-as-programs became standard language in the literature.
7. The chronology of classical-logic/control correspondences.
8. Girard/Reynolds chronology for polymorphism and relational parametricity.
9. Historical claims about LCF/small-kernel architecture and later proof assistants.
10. System-specific claims about program extraction.

## Citation policy by claim class

| Claim class | Required source discipline |
|---|---|
| Foundational priority/date | primary source preferred; verify date/version |
| Standard theorem imported without full proof | theorem-level citation to a source stating the needed scope |
| Historical synthesis | multiple sources if no single primary source supports the synthesis |
| Modern implementation architecture | primary system documentation/paper plus version context where material |
| Pedagogical analogy | source optional unless historically attributed; analogy limit must be explicit |
| Novelty/priority claim by GCL | not planned; would require separate literature audit |

## Publication-pass outputs

Before Gate 5, replace this planning document's open source families with a verified `BIBLIOGRAPHY_AUDIT.md` containing:

- exact citation metadata;
- source role;
- primary/secondary classification;
- historical claims checked;
- theorem/import claims checked;
- unresolved attribution ambiguity;
- explicit note for any circulation/publication-date distinction.

The final manuscript bibliography must include both foundational sources and modern expository references. It must not imply independent mathematical review merely because a theorem has a citation.
