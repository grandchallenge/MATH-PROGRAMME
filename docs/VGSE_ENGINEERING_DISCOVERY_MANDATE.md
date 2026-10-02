# VGSE-001 Engineering Discovery Mandate

**Campaign:** `VGSE-001`  
**Programme tracker:** `grandchallenge/MATH-PROGRAMME#984`  
**Status:** active research mandate  
**Directive date:** 2026-09-15  
**Primary question:** **What reusable engineering laws are latent in the origami structure?**

## 1. Core clarity

VGSE-001 is no longer primarily a reconstruction exercise.

The reconstruction and certification work established a trustworthy starting point. The programme must now use that starting point to discover engineering principles that are inherent in, or exposed by, the origami structure.

The working hypothesis is:

> **Origami structures may encode mechanical function in layers: topology defines the admissible mechanism; geometry selects a realization; metric parameters tune response; material and thickness determine physical performance.**

This is a research hypothesis, not a certified result.

If the hierarchy survives analysis, the practical opportunity is substantial. A mechanism need not be designed part by part. GCL can instead work from a desired global behaviour, identify the structural constraints that make that behaviour possible, and solve for a realizable geometry.

The programme therefore asks a different question from source reconstruction:

> **What is invariant, what is tunable, what controls the tuning, what survives perturbation, what can be synthesized, and what useful mechanism follows?**

## 2. Protected starting point

The engineering programme inherits the protected mathematical boundary. It does not enlarge it.

MATHCERT restricted R4 publication merge:

`2f27aed33b32b4caf6ff8622c87cfd6d40e97607`

The R4 certificate qualifies exactly:

- `VGSE-C00`;
- `VGSE-C01`;
- `VGSE-C04`;
- `VGSE-C05`.

`VGSE-C06` remains excluded and fail-closed on the original route. The published source package does not establish the required Figure-16-to-pinned-`C` correspondence.

This has an important engineering interpretation. The visible source figure must not be treated as a certified build specification or as the unique physical realization of the qualified structure.

The C06 gap constrains **source attribution**. It does not prohibit GCL from designing new realizations of the qualified mathematics, provided those realizations are clearly identified as GCL constructions rather than recovered source geometry.

## 3. The layered engineering model

Agents should keep four layers separate until evidence supports a coupling claim.

### Layer 1 — topology and combinatorics

This layer contains the discrete structure: adjacency, incidence, connectivity, fold or face relationships, admissible constraint structure, and other information unchanged by continuous geometric deformation within the same structural class.

The central question is:

**Which useful behaviours are forced or protected by this structure?**

Candidate outputs include mobility classes, compatible motion families, conserved relationships, forbidden states, singularities, and topology-protected response features.

### Layer 2 — geometric realization

This layer selects one embedding or shape from the admissible structural family.

The central question is:

**What changes when the same structural object is realized with different geometry?**

Candidate variables include vertex positions, face shapes, edge lengths, angles, crease placement, and embedding choices.

### Layer 3 — metric and response tuning

This layer contains numerical parameters that tune the response of an admissible realization.

The central question is:

**Which parameters control the behaviour, and how strongly?**

Relevant quantities can include weights, effective stiffness parameters, mechanical advantage, displacement ratios, deployment ratios, response gains, stability margins, and boundary response. A mathematical weight is not automatically a physical stiffness; any such interpretation must be established rather than assumed.

### Layer 4 — material and fabrication

This layer contains the physical realization: thickness, constitutive law, hinge behaviour, friction, tolerances, plasticity, fatigue, contact, and fabrication constraints.

The central question is:

**Which structural and geometric discoveries survive contact with physical implementation?**

No current VGSE certificate establishes these physical properties.

## 4. Core research questions

The campaign should preferentially attack questions that expose reusable engineering structure.

1. Which kinematic or response properties are invariant under admissible changes of geometric realization?
2. Which properties vary continuously with geometry while topology is fixed?
3. What is the smallest parameter set that materially controls the response?
4. Where are the singular, locked, highly amplified, or multistable regimes?
5. Which useful behaviours are robust to perturbation and which require fine tuning?
6. Can a desired boundary response be specified first and an internal structure synthesized to realize it?
7. Does one topology define a useful family of mechanisms rather than one privileged drawing?
8. Can the structure yield reusable mechanical primitives such as compliant joints, transmissions, springs, latches, deployable cells, mechanical logic elements, or motion converters?
9. Can global coordinated behaviour emerge from local geometric constraints without centralized control?
10. Which apparent source-specific features disappear when the structure is expressed in invariant coordinates?

## 5. GCL core-clarity probe

For every proposed engineering discovery, ask these questions in order:

1. **Object —** What exact structural or physical object are we studying?
2. **Freedom —** Which variables may change without leaving the object class?
3. **Invariant —** What survives those changes?
4. **Control —** Which variables materially alter the response?
5. **Map —** What forward map connects design parameters to behaviour?
6. **Inverse —** Can we solve backward from desired behaviour to a design?
7. **Robustness —** Does the result survive perturbation, tolerance, thickness, and model error?
8. **Utility —** What engineering function becomes possible because of the result?
9. **Boundary —** What has not been established?

A result that cannot answer these questions may still be mathematically interesting, but it has not yet become an engineering discovery for this campaign.

## 6. First engineering tranche

The first substantive tranche should produce a canonical parameterized representation of the qualified VGSE structure.

It should separate at least:

- discrete/topological variables;
- geometric realization variables;
- metric or weight variables;
- candidate physical/material variables.

From that representation, the tranche should:

1. define a parameterized forward map from admissible realization to one or more measurable boundary or mechanism responses;
2. compute or derive sensitivities of those responses to the available parameters;
3. identify candidate invariants and deliberately try to break them;
4. identify degeneracies, non-identifiability, and singular regimes;
5. solve at least one bounded inverse problem from target response to admissible realization, or establish why the chosen inverse problem is ill-conditioned or impossible;
6. distinguish a recovered source property from a newly designed GCL realization at every step.

The preferred first result is not a more elaborate reproduction of Figure 16. It is a map of the design space.

## 7. First-phase material acceptance criteria

The first phase is materially successful when it produces all of the following:

1. a canonical layered model that a new agent can execute or reason from;
2. at least one verified invariant, or a well-evidenced falsification of a plausible invariant;
3. a sensitivity map that identifies the parameters that materially control response;
4. a clear account of which information is recoverable from visible geometry and which is not;
5. one bounded inverse-design result, constructive or negative;
6. a robustness result for at least one discovered behaviour;
7. an engineering claim ledger that separates observation, hypothesis, verified result, source attribution, and open question;
8. a concrete next experiment, derivation, or design synthesis that follows from the evidence.

Green CI, new manifests, additional governance records, or a larger evidence archive do not satisfy these criteria by themselves.

## 8. Agent contribution directive

Independent agents joining VGSE-001 should begin here and at `grandchallenge/MATH-PROGRAMME#984`.

Then read the exact protected mathematical starting point and the current MATHSOLVE VGSE artifacts before making a substantive claim.

Agents should follow these rules:

- optimize for engineering discovery, not process accumulation;
- do not re-prove the four qualified claims unless a new engineering result materially depends on doing so;
- preserve the C06 source-correspondence boundary;
- do not equate a source drawing with a physical design unless the correspondence is actually established;
- label GCL-created realizations as new designs;
- preserve negative results, failed invariants, singular cases, and non-identifiability;
- prefer parameter sweeps, exact derivations, sensitivity analyses, counterexamples, and inverse-design tests that distinguish layers of the model;
- report what changed physically or structurally, not only what code or workflow ran;
- keep hypotheses visibly separate from verified engineering results;
- route exact mathematical claims to MATHCERT only when certification is actually material to the engineering conclusion.

Every substantive contribution should make at least one of these clearer:

**what is invariant; what is tunable; what controls the tuning; what survives perturbation; what can be synthesized; what useful mechanism follows.**

## 9. Evidence and claim discipline

The following labels should be used explicitly in research notes and work packages where applicable:

- **SOURCE FACT** — directly supported by the pinned source record;
- **QUALIFIED MATHEMATICAL RESULT** — supported by the applicable MATHCERT disposition;
- **GCL OBSERVATION** — reproduced computational or experimental observation within stated conditions;
- **WORKING HYPOTHESIS** — plausible explanatory or predictive statement not yet established;
- **VERIFIED ENGINEERING RESULT** — survives the declared analytical, numerical, or experimental test within its stated model and range;
- **GCL DESIGN** — a realization synthesized by GCL rather than recovered from the source;
- **OPEN QUESTION** — unresolved and not to be implied by surrounding results.

Do not convert one label into another by exposition alone.

## 10. Practical research posture

The campaign should not wait for C06 to close before doing engineering work that does not depend on source identity.

Two tracks can proceed independently:

- **source correspondence:** continue only when genuinely new admissible evidence can establish the historical geometry-to-weight bridge;
- **engineering discovery:** explore the realization family permitted by the qualified structure and search for reusable mechanical laws.

If a new GCL realization satisfies the relevant mathematical constraints, it is valuable even when it does not reproduce the historical figure. The correct claim is then that GCL designed a new realization of a qualified structural object, not that GCL recovered the source design.

## 11. Boundaries

This mandate does not establish:

- rigid foldability;
- collision freedom;
- finite-thickness feasibility;
- manufacturability;
- durability or fatigue performance;
- product performance;
- novelty or priority;
- patentability;
- commercial value.

Those are legitimate later engineering questions. They require their own models, evidence, and authority.

## 12. Continuation rule

VGSE-001 is a long-horizon research campaign. Current execution state must be recoverable without conversational history.

The resumable checkpoint is registered through:

`governance/bounded_operation_checkpoints/VGSE-ENGINEERING-DISCOVERY-001.json`

A fresh agent must re-read the live tracker, this mandate, the checkpoint, and the protected evidence identities before mutation. The checkpoint records the next executable action. This mandate records why the action matters.
