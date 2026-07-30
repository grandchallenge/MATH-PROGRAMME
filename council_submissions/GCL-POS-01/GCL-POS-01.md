# Executive position

\begin{positionbox}
\textbf{Grand Challenge Labs takes this position:} technical communication is part of the research instrument. It is not packaging added after the research is complete.
\end{positionbox}

A research result is not ready for institutional use when only its conclusion is visible. It becomes usable when a reader can inspect the exact claim, scope, assumptions, evidence, limitations, provenance, review state, and authorized uses.

Good prose remains necessary. It does not supply those controls by itself.

This paper states an institutional position and a set of recommendations. It does not report an empirical result. It does not claim that one governance system is optimal. It does not promote GCL-TCS-00 beyond its current candidate status.[^gcltcs]

# The position

Research changes the state of knowledge. Technical communication carries that change between people, tools, repositories, and decisions.

A document therefore does more than describe research. It controls which claims can travel, what context travels with them, and what later work can rely on them.

Grand Challenge Labs will treat consequential communication as governed research infrastructure. A consequential claim will carry an explicit identity and status. Its evidence and limitations will remain attached during review, release, and public explanation.

This position rests on a simple distinction:

- Presentation can reveal authority.
- Presentation cannot create authority.

A polished artifact can still contain a false statement. A clear sentence can still hide an assumption. A reproducible experiment can still test the wrong question. A correct result can still acquire an invalid public interpretation.

GCL-TCS-00 addresses these risks through profiles, metadata, claim records, evidence records, review gates, and fail-closed promotion. ASD-STE100 supplies a strong baseline for clear technical prose.[^ste] GCL adds controls for epistemic status and institutional authority.

# Communication as an instrument

A scientific instrument converts a state of the world into a record that people can inspect. A technical artifact converts a state of inquiry into a record that people can reuse.

Both conversions can fail.

An instrument can lose calibration. A document can lose scope. An instrument can mix signal with noise. A document can mix result with interpretation. An instrument can report a value without uncertainty. A document can report a claim without limitations.

The analogy has limits. A document is not a sensor. It is a governed interface between evidence and action.

Figure 1 shows the intended state transition. Each arrow has a gate. A missing mandatory record blocks the transition.

![The governed claim pipeline binds a question to evidence, a bounded claim, review, authority, and permitted use. Missing mandatory records stop the transition.](assets/governed-claim-pipeline.pdf){#fig:pipeline width=95%}

The pipeline does not prove truth. It makes the basis of trust inspectable.

# Five institutional commitments

## Preserve technical object identity

A technical object needs one canonical identity across prose, equations, code, data, and schemas.

GCL will define canonical terms and permitted aliases. It will map notation to implementation identifiers when that mapping affects interpretation.

Stylistic variation will not justify silent changes in meaning.

## Preserve claim identity

Each consequential claim will state its type and status. The artifact will separate definitions, assumptions, observations, hypotheses, results, interpretations, recommendations, and speculation.

The claim will also state its domain, assumptions, dependencies, limitations, and falsifiers.

A summary will not strengthen the source claim. A public page will not convert a proposed claim into an established result.

## Bind evidence to the claim it can support

Evidence has scope. A benchmark result can support a statement about the tested setting. It cannot support an unrestricted statement about all models, scales, or environments.

GCL will record the method, version, location, result summary, scope, and limitations of consequential evidence.

Negative evidence will remain visible. Failed tests will not disappear because they weaken the preferred narrative.

## Treat promotion as a state transition

A document does not become authoritative because it looks complete. It becomes authoritative through an explicit decision over a fixed revision.

Promotion will require the applicable gates. Those gates cover identity, scope, structure, language, claims, evidence, verification, adversarial review, provenance, and release integrity.

Missing mandatory records will block promotion. A warning will not replace a failed gate.

## Make public exposition inherit its boundaries

Public writing can simplify language and structure. It cannot simplify away material uncertainty.

A public explanation will inherit the source claim's status, scope, assumptions, and limitations. It will distinguish analogy from mechanism. It will link to the authoritative source.

This rule protects both readers and researchers. It prevents a careful result from becoming an inflated public claim.

# What changes in practice

The position changes the treatment of artifacts, not only their wording.

| Work stage | Required behaviour |
|---|---|
| Exploration | Keep private scratch work lightweight. Do not grant it downstream authority. |
| Registration | Assign a stable identity, owner, profile, impact class, and source revision. |
| Claim formation | Record claim type, status, scope, assumptions, limitations, and falsifiers. |
| Evidence production | Record methods, versions, hashes, result scope, and negative evidence. |
| Review | State what each reviewer checked and what the review did not establish. |
| Promotion | Fix the reviewed revision and authorize specific downstream uses. |
| Publication | Admit the artifact, ledgers, reviews, assets, and manifests together. |
| Supersession | Preserve history and redirect later use to the replacement artifact. |

This structure creates a boundary between exploration and authority. GCL can move quickly inside the exploratory boundary. It must become stricter when other work begins to depend on a claim.

The impact class controls the strength of review. A routine note does not need the same process as a public benchmark claim. A claimed open-problem resolution requires the strongest process.

# Why clear language is not enough

ASD-STE100 addresses many surface failures in technical prose. It promotes controlled terms, direct sentences, stable keywords, active voice, and explicit procedures.[^ste]

These practices reduce ambiguity. They also make review easier.

They do not answer several institutional questions:

1. What kind of claim is this?
2. What evidence supports this exact scope?
3. Which revision did a reviewer examine?
4. What uncertainty remains material?
5. What downstream use did the referee authorize?
6. Did a public explanation preserve the source status?

GCL-TCS-00 adds a conformance model for these questions. It also states that conformance does not establish truth.

This distinction matters. A checklist can verify that a claim has evidence. It cannot decide that the evidence is sufficient without domain judgment.

# Counterpositions and responses

## "Skilled researchers already understand context"

Skilled readers often recover missing context. Institutions cannot rely on that recovery.

People leave projects. Repositories change. Public summaries detach from source documents. Machine systems retrieve fragments without the surrounding discussion.

The record must preserve the context that downstream use requires.

## "Governance slows discovery"

Heavy governance can slow discovery. This position does not govern all thought as if it were a public claim.

Private scratch work remains outside formal promotion until the project registers it. Review strength scales with impact. The system becomes strict when an artifact seeks authority.

The intended trade is selective friction. GCL accepts friction at points where an error can propagate.

## "Machine-readable fields create false precision"

They can. A status field can look exact while the underlying judgment remains weak.

GCL therefore separates conformance from truth. It also requires review records to state what they did not establish.

Machine-readable status supports discovery and enforcement. It does not replace technical judgment.

## "Public communication needs a stronger story"

Public communication needs a coherent story. It does not need a stronger claim.

Writers can use examples, diagrams, and analogies. They must label analogy as analogy. They must keep material limitations visible.

A compelling explanation should make the source easier to inspect. It should not detach the reader from the source.

# Limits of this position

This position has five explicit limits.

First, it does not claim that metadata prevents scientific error.

Second, it does not claim that GCL-TCS-00 is complete or optimal. The charter remains a candidate standard.

Third, it does not require strict controlled-language syntax inside equations, theorem statements, code, schemas, or exact quotations.

Fourth, it does not treat machine-assisted review as independent review.

Fifth, it does not require every temporary note to enter the governed record.

The position should change when evidence shows that its controls do not improve traceability, error detection, or responsible reuse.

# Revision conditions

GCL should revise this position when one or more conditions occur:

- Pilot projects show high recurring cost without material risk reduction.
- Researchers bypass the system and create shadow sources of authority.
- The profiles fail to represent actual artifact classes.
- Claim status does not survive release and public transformation.
- Review records become ceremonial and stop identifying unresolved risk.
- External obligations conflict with the charter's implementation.
- Independent review finds a safer or simpler control model.

These conditions are not rhetorical caveats. They are falsifiers for the present governance design.

# Adoption position

GCL should adopt the following sequence.

1. Use GCL-TCS-00 as a candidate framework in pilot projects.
2. Test it on research, mathematics, experiments, software, operations, governance, and public exposition.
3. Measure review defects, missing provenance, claim drift, author burden, and reviewer burden.
4. Record exceptions and repeated failure modes.
5. Revise the profiles and gates from pilot evidence.
6. Seek independent referee review before version 1.0 promotion.

The standard should earn authority through use and review. It should not receive authority from this position piece.

# Conclusion

At Grand Challenge Labs, communication is part of epistemic control.

A consequential claim is not yet an institutional result when its boundaries remain implicit. It becomes eligible for use when its claim, evidence, provenance, limitations, review state, and authority are inspectable.

This position does not replace scientific judgment. It makes the conditions for judgment visible.

\begin{positionbox}
\textbf{GCL position:} presentation may reveal authority, but it cannot create authority.
\end{positionbox}

\appendix

# Conformance demonstration

This artifact declares GCL-TCS-P06 as its primary profile. It declares GCL-TCS-P07 as a secondary profile.

The artifact is IC-2 because it states a public technical and governance position. It remains a candidate artifact with `review_ready` promotion status.

The package includes:

- a machine-readable conformance declaration;
- a terminology registry;
- a claim register;
- an evidence register;
- gate review records;
- an explicit empty exception register;
- a build script, validation script, manifest, and checksums.

The internal reviews cover gates G0 through G7. The same machine-assisted system drafted and checked the artifact. Those checks are not independent.

Gate G8 remains deferred pending an independent GCL referee. Gate G9 remains deferred pending authority admission and release approval.

No conformance dimension is marked `ASSURED`.

# Claim boundary

The claim register is authoritative for the claims in this piece.

The main position is a proposed recommendation. The supporting statements are proposed interpretations and recommendations. None is classified as an empirical result, theorem, or formally verified result.

The evidence register records documentary and validation support. It does not claim empirical proof that this governance model improves research outcomes.


[^gcltcs]: Grand Challenge Labs, *GCL-TCS-00: Technical Communication Charter and Conformance Model*, Candidate Standard 0.1.0, 2026-07-27. The standard remains a candidate artifact.

[^ste]: Aerospace, Security and Defence Industries Association of Europe, *ASD-STE100 Simplified Technical English: Standard for Technical Documentation*, Issue 9, January 2025.
