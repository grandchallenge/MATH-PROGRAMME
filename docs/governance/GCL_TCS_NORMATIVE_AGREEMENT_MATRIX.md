# GCL-TCS-00 normative ↔ machine agreement matrix

**Operation:** `GCL-TCS-CANDIDATE-HARDENING-004`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#814`  
**Status:** derivative candidate-standard reconciliation evidence; not normative and not promotion authority  
**Protected audit baseline:** `f0aefb88fdb62a128e0c2f04559150de2d3a1128`  
**Normative assembled SHA-256:** `ea750b9b80b53c7d6ed755978fa4bdf59413fad93cec1db81eb3238372ce61c9`  
**Machine-contract revision:** `0.1.0-r1`

The normative seven-part Markdown source controls meaning. This matrix records how each bound normative obligation or strong default is represented by current machine policy, schemas, templates, validators, and tests. A matrix row cannot create, weaken, or promote an obligation.

| ID | Normative requirement | Machine representation | Validator / test | Checkability | Gap |
|---|---|---|---|---|---|
| `N-2-01` | A promoted artifact must not depend on unregistered scratch as its only authority. | `normative_source_contract.scratch_boundary` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-4.1-01` | A writing rule MUST NOT change technical meaning. | `principles.PR-01 + normative_obligations.correctness_preservation` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-4.1-02` | When clarity and precision conflict, the author MUST first attempt a structural solution. | `normative_obligations.structural_solution_before_exception` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-4.2-01` | A document MUST distinguish established results from hypotheses, interpretations, recommendations, and speculation. | `normative_obligations.claim_boundary_distinction` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-4.2-02` | Presentation quality MUST NOT raise claim status. | `normative_obligations.no_presentation_promotion` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-4.2-03` | Public explanations MUST preserve source claim status, scope, assumptions, and important limitations. | `normative_obligations.public_source_claim_preservation` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-4.3-01` | A consequential claim MUST link to evidence or accepted derivation. | `record_contracts.claim.supporting_evidence + fail_closed_conditions.missing_claim_ledger` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-4.3-02` | Evidence MUST be sufficient for declared claim type and impact class. | `normative_obligations.evidence_sufficiency` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-4.4-01` | Empirical or computational results MUST provide enough information to repeat the relevant procedure. | `profiles.GCL-TCS-P04 + normative_obligations.reproducibility_information` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-4.4-02` | If full reproduction is impossible, the artifact MUST state why and provide the strongest available substitute. | `normative_obligations.reproducibility_limitation_substitute` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-4.5-01` | When synonyms are used, the document MUST identify the canonical term. | `normative_obligations.canonical_term_identification` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-4.6-01` | An artifact MUST state material uncertainty, unresolved proof debt, missing controls, unsupported assumptions, and known failure cases. | `normative_obligations.explicit_uncertainty` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-4.6-02` | An artifact MUST NOT use silence to imply that an unresolved question is settled. | `normative_obligations.no_silence_as_resolution` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-4.7-01` | The promotion system MUST fail closed. | `normative_obligations.fail_closed_promotion + fail_closed_conditions` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-4.7-02` | Missing mandatory metadata, ledgers, reviews, hashes, or exception records MUST block the applicable gate. | `fail_closed_conditions + record_contracts` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-4.7-03` | A tool MUST NOT infer promotion state from display text. | `normative_obligations.machine_status_controls_display` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-6.1-01` | A lower layer MUST NOT silently weaken a higher-layer requirement. | `conformance_rules.lower_layer_must_not_weaken` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-6.2-01` | Authors/reviewers MUST resolve conflicts using the charter conflict order. | `conflict_order + conformance_rules.conflict_resolution_required` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-6.2-02` | If obligations cannot be reconciled, the artifact MUST NOT be promoted. | `conformance_rules.unresolved_conflict_blocks_promotion` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-6.2-03` | The owner MUST record the conflict and request an authority decision. | `conformance_rules.unresolved_conflict_record_required` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-6.3-01` | Each standard and annex MUST identify normative and informative content. | `conformance_rules.normative_informative_identification` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-6.4-01` | Artifact declarations MUST identify exact charter/profile/annex versions. | `conformance_rules.exact_version_locks_required + schemas/gcl-tcs-conformance.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-6.4-02` | A project MUST NOT use an unspecified 'latest standard' as its only version lock. | `conformance_rules.unspecified_latest_forbidden` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-6.5-01` | Each governed record MUST have an authority status. | `authority_statuses + mandatory_metadata.core` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-7.2-01` | Each mandatory conformance dimension MUST carry an assessment state. | `assessment_states + schemas/gcl-tcs-conformance.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-7.2-02` | An artifact MUST NOT report ASSURED without a linked review record. | `conformance_rules.assured_requires_linked_review` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-7.3-01` | A conformance statement MUST include profile(s), impact, target state, dimensions, active exceptions, promotion state, date and standard versions. | `record_contracts.conformance_statement + schemas/gcl-tcs-record-contracts.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-7.4-01` | An artifact MUST separately record claim status and verification evidence. | `record_contracts.claim + record_contracts.evidence` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-8-01` | The owner MUST select the highest applicable impact class. | `conformance_rules.highest_applicable_impact_class` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-8-02` | A project annex MUST NOT lower a charter-mandated impact class. | `conformance_rules.annex_cannot_lower_impact_class` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-8-03` | An artifact claiming to solve/disprove/materially settle a recognized open problem MUST be IC-3. | `conformance_rules.open_problem_minimum_impact_class` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.1-01` | Each governed artifact MUST declare one primary profile. | `profiles + mandatory_metadata.core + schemas/gcl-tcs-conformance.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-9.1-02` | The complete obligation set is the union of primary and secondary profiles; stricter requirements apply on conflict unless meaning changes. | `conformance_rules.profile_union_and_stricter_rule` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.2-PROFILE` | operational/procedural mandatory emphasis and dimensions are normative profile obligations. | `profiles.GCL-TCS-P01` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.3-PROFILE` | research mandatory emphasis and dimensions are normative profile obligations. | `prifiles.GCL-TCS-P02` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.4-PROFILE` | mathematical/formal mandatory emphasis and dimensions are normative profile obligations. | `prifiles.GCL-TCS-P03` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.5-PROFILE` | experimental/computational mandatory emphasis and dimensions are normative profile obligations. | `profiles.GCL-TCS-P04  | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.6-PROFILE` | software/API/notebook mandatory emphasis and dimensions are normative profile obligations. | `prifiles.GCL-TCS-P05` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.7-PROFILE` | public exposition mandatory emphasis and dimensions are normative profile obligations. | `profiles.GCL-TCS-P06` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.8-PROFILE` | governance/documentary mandatory emphasis and dimensions are normative profile obligations. | `profiles.GCL-TCS-P07` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.2-02` | Operational surrounding procedure MUST remain explicit. | `profiles.GCL-TCS-P01.emphasis + language_structure_contract` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-9.7-02` | P06 MUST inherit claim status from authoritative source artifacts. | `normative_obligations.public_source_claim_preservation` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-9.7-03` | P06 MUST NOT create a stronger technical claim than its sources support. | `normative_obligations.no_public_claim_inflation` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-10.1-01` | Every governed artifact MUST have a machine-readable conformance declaration. | `mandatory_metadata + schemas/gcl-tcs-conformance.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-10.1-02` | Human-readable front matter MUST NOT replace the machine declaration. | `normative_obligations.machine_declaration_not_replaceable` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-10.1-03` | Every required field MUST be present; silent omission is forbidden. | `mandatory_metadata.omission_policy + schemas/gcl-tcs-conformance.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-10.2-01` | The declaration MUST contain the complete core artifact field set. | `mandatory_metadata.core + schemas/gcl-tcs-conformance.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-10.3-01` | Each consequential claim MUST have the specified stable claim record fields. | `record_contracts.claim + schemas/gcl-tcs-record-contracts.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-10.3-02` | A project annex adding a claim status MUST define its relation to charter statuses. | `record_contracts.claim.annex_status_relation_required` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-10.4-01` | Each evidence record MUST contain the specified evidence fields. | `record_contracts.evidence + schemas/gcl-tcs-record-contracts.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-10.5-01` | Each review record MUST contain the specified review fields. | `record_contracts.review + schemas/gcl-tcs-record-contracts.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-10.6-01` | Machine-readable promotion status MUST use the charter enumeration. | `promotion_statuses + schemas/gcl-tcs-conformance.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-11.1-01` | An artifact MUST use the same term for the same technical object unless aliasing is explicit. | `language_structure_contract.term_consistency` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-10.1-02` | A new technical term MUST be defined before dependence. | `language_structure_contract.define_terms_before_use` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-10.1-03` | A term MUST NOT silently change meaning across prose/equations/code/figures/metadata. | `language_structure_contract.no_cross_surface_term_drift` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-11.3-01` | Passive constructions MUST remain technically correct. | `language_structure_contract.passive_voice_must_preserve_correctness` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-11.3-02` | A procedure MUST identify the responsible actor where responsibility is not the reader's. | `language_structure_contract.responsible_actor_required` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-11.5-01` | A procedural step MUST contain one primary action. | `language_structure_contract.one_primary_action_per_step` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-11.5-02` | Prerequisites, warnings, expected results and recovery steps MUST appear before needed. | `language_structure_contract.sequence_context_before_need` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-11.6-01` | A figure/table/equation MUST have enough context; surrounding text MUST state what it shows and why it matters. | `language_structure_contract.visual_context_required` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-11.6-02` | Applicable plots MUST identify quantity/sample/aggregation/uncertainty/filtering/exploratory-confirmatory status. | `language_structure_contract.plot_context_fields` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-11.6-03` | Material public visual content MUST have alt text or equivalent description. | `language_structure_contract.public_visual_accessibility` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-12.1-01` | An author MUST NOT treat an unrecorded deviation as an implicit exception. | `exception_model + record_contracts.exception` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-12.3-01` | Each artifact exception MUST contain the specified fields. | `record_contracts.exception + schemas/gcl-tcs-record-contracts.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-12.3-02` | An exception MUST be as narrow as possible. | `exception_contract.narrow_scope_required` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-12.4-01` | Exceptions cannot waive the enumerated non-waivable requirements. | `exception_model.non_waivable` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-12.5-01` | Approved exceptions MUST have review/expiry timing unless a profile defines permanence. | `record_contracts.exception + gcl_tcs_exception_control` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-12.5-02` | Promotion MUST fail for missing, expired or revoked required exceptions. | `gcl_tcs_exception_control + fail_closed_conditions` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-13.1-01` | Each gate decision MUST use the GCL-TCS decision enumeration. | `gate_decisions + record_contracts.gate` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-13.1-02` | NOT_APPLICABLE requires a reason and reviewer approval; DEFERRED does not satisfy a gate. | `promotion_contract.not_applicable + record_contracts.gate` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.1-03` | A gate MUST check the exact promoted revision; material change invalidates affected gates. | `promotion_contract.exact_revision_gate_binding` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.2-G0` | G0 purpose and pass conditions are normative gate requirements. | `gates.G0 + gate_contracts.G0` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.3-G1` | G1 purpose and pass conditions are normative gate requirements. | `gates.G1 + gate_contracts.G1` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.4-G2` | G2 purpose and pass conditions are normative gate requirements. | `gates.G2 + gate_contracts.G2` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.5-G3` | G3 purpose and pass conditions are normative gate requirements. | `gates.G3 + gate_contracts.G3` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.6-G4` | G4 purpose and pass conditions are normative gate requirements. | `gates.G4 + gate_contracts.G4` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.7-G5` | G5 purpose and pass conditions are normative gate requirements. | `gates.G5 + gate_contracts.G5` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.8-G6` | G6 purpose and pass conditions are normative gate requirements. | `gates.G6 + gate_contracts.G6` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.9-G7` | G7 purpose and pass conditions are normative gate requirements. | `gates.G7 + gate_contracts.G7` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.10-G8` | G8 purpose and pass conditions are normative gate requirements. | `gates.G8 + gate_contracts.G8` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.11-G9` | G9 purpose and pass conditions are normative gate requirements. | `gates.G9 + gate_contracts.G9` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.7-02` | G5 review records MUST state what was checked and not checked. | `record_contracts.review + gate_contracts.G5` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-13.10-02` | The artifact owner MUST NOT be sole referee for IC-2/IC-3. | `review_control.ic2_ic3_owner_not_sole_referee` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-14-01` | The gate applicability matrix is normative; conditional gates become mandatory when relevant. | `gate_matrix + promotion_contract.conditional_gate_activation` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-14-02` | IC-3 MUST pass G6 and G7 absent a valid NOT_APPLICABLE decision that preserves non-waivable rules. | `promotion_contract.ic3_g6_g7_required` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-15-01` | Review roles identify functions and do not confer authority without a review record. | `review_control.role_name_does_not_confer_authority` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-15-02` | IC-2/IC-3 artifacts MUST record material role overlap. | `review_control.ic2_ic3_role_overlap_recorded` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-15-04` | Automated checks MUST NOT impersonate independent human/institutional decisions. | `review_control.automation_cannot_impersonate_authority` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-15-05` | Review records MUST identify automated and judgment-based checks separately. | `review_control.automated_and_judgment_checks_separate` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-16-01` | A conforming implementation MUST block promotion on every enumerated fail-closed condition. | `fail_closed_conditions` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-16-02` | A warning is insufficient for a fail-closed condition. | `normative_obligations.fail_closed_is_blocking` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-17-01` | Each release MUST include change log, migration note, compatibility statement, previous/new identifiers, review and promotion records. | `record_contracts.release + schemas/gcl-tcs-record-contracts.schema.json` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-17-02` | A project MUST review active exceptions after a major version change. | `change_control.active_exception_review_after_major` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-17-03` | A superseded standard MUST NOT remain the default for new artifacts unless locked by approved annex. | `change_control.superseded_not_default` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-18-01` | Detailed modules MUST conform to this charter and cannot silently remove a non-waivable requirement. | `change_control.modules_conform_and_cannot_remove_nonwaivable` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-19-01` | Machine-readable templates in the package are normative for version 0.1.0. | `machine_contracts.templates` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `N-20-01` | Criterion 1 requires policy/schema agreement with normative text before v1.0. | `normative_source_contract + machine_contracts + this matrix` | `tests/test_gcl_tcs_normative_agreement.py` | `machine` | `CLOSED` |
| `S-4.5-01` | A technical object SHOULD have one canonical project name. | `strong_defaults.canonical_name` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-4.5-02` | Notation/code/schema/prose terms SHOULD map through a terminology or notation registry. | `strong_defaults.cross_surface_registry_mapping` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-6.3-01` | Examples/commentary/motivation/teaching notes SHOULD be informative. | `strong_defaults.examples_informative` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-6.3-02` | Requirements/schemas/enumerations/gate criteria SHOULD be normative. | `strong_defaults.machine_requirements_normative` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-9.4-01` | Logically atomic mathematical statements SHOULD remain intact when splitting obscures scope. | `strong_defaults.atomic_formal_statement` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-11.1-01` | A definition SHOULD state scope and distinguish nearby concepts. | `strong_defaults.definition_scope` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-11.2-01` | A sentence SHOULD make one principal assertion. | `strong_defaults.one_principal_assertion` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-11.2-02` | Independent claims/hidden conditions/multiple actions SHOULD be split. | `strong_defaults.split_independent_content` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-11.2-03` | Explanatory prose SHOULD normally use no more than 25 words per sentence, diagnostically. | `strong_defaults.sentence_length_diagnostic` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-11.3-01` | Active voice SHOULD be used when the agent is known and relevant. | `strong_defaults.active_voice_when_agent_known` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-11.4-01` | A paragraph SHOULD address one topic. | `strong_defaults.one_topic_per_paragraph` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-11.4-02` | A paragraph SHOULD identify its topic early when not clear from heading. | `strong_defaults.topic_sentence_when_needed` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-11.4-03` | A prose paragraph SHOULD normally contain no more than six sentences. | `strong_defaults.paragraph_length_diagnostic` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-11.5-01` | A complex enumeration SHOULD use a vertical list. | `strong_defaults.vertical_complex_list` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-18-01` | GCL SHOULD adopt the standards family in the stated order. | `strong_defaults.module_adoption_order` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-AppB-01` | A reviewer SHOULD reject an exception when any decision-test answer is no. | `strong_defaults.exception_decision_test` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `S-AppC-01` | A G8 referee decision SHOULD use the prescribed decision structure. | `strong_defaults.g8_decision_structure` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-11.6-01B` | Surrounding text MUST state what a figure/table/equation shows and why it matters. | `language_structure_contract.visual_context_required` | `tests/test_gcl_tcs_normative_agreement.py` | `review` | `CLOSED` |
| `N-15-03A` | For IC-3, the author MUST NOT be the sole G5 reviewer. | `review_control.ic3_separation_of_duties.author_not_sole_G5_reviewer` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-15-03B` | For IC-3, the authoring team MUST NOT supply the only G6 review. | `review_control.ic3_separation_of_duties.authoring_team_not_only_G6_review` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-15-03C` | For IC-3, the owner MUST NOT be the sole referee. | `review_control.ic3_separation_of_duties.owner_not_sole_referee` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |
| `N-15-03D` | For IC-3, the release steward MUST verify the exact promoted revision. | `review_control.ic3_separation_of_duties.release_steward_exact_revision_verification` | `tests/test_gcl_tcs_normative_agreement.py` | `hybrid` | `CLOSED` |

## Result

The matrix contains **119 source-bound reconciliation rows**. Every row points back to a protected normative source clause. All identified machine-representation gaps in this candidate correction tranche are recorded as `CLOSED`; obligations that inherently require judgment remain represented in policy/templates and are tested for presence/shape rather than falsely converted into automated truth tests.

## Candidate corrections

- Bind the machine policy to the seven protected source parts and assembled source digest.
- Represent full claim, evidence, review, exception, gate, conformance-statement, and release record contracts.
- Tighten the declaration schema to the exact candidate standard/profile versions.
- Add normative machine-readable conformance and record templates for candidate `0.1.0`.
- Add a library-only agreement validator and adversarial contract tests.
- Preserve the historical issued submission manifest and its original machine-policy/schema hashes as historical evidence.

## Authority boundary

This is a candidate-standard machine-contract correction. It does not alter the seven normative source parts, promote GCL-TCS-00 to version 1.0, issue a G8/G9 disposition, or create new constitutional, mathematical, certification, publication, or external authority.
