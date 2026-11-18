#!/usr/bin/env python3
"""Closed-world, fail-closed 1,221-problem proof-work queue inventory validator.

Queue creation never certifies mathematics. Full closure demands separate receipts.
"""
from __future__ import annotations
import collections
import hashlib
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1]
REG='governance/erdos_proof_verification/coverage/REGISTRY.json'
SRC='governance/erdos_catalogue/REGISTRY.json'
PHASES='ABCD'
PILOT={246:3202,247:3203,248:3204,249:3205,250:3206}
VALID_STATUS={'UNEXECUTED','PILOT_REUSE_PENDING_EVIDENCE','IN_PROGRESS','EVIDENCE_BLOCKED','VERIFIED_BOUNDED','NOT_APPLICABLE_REVIEWED','PROTECTED_ADMITTED','REUSED_SCOPE_VERIFIED'}

def ensure(ok,msg):
    if not ok:raise ValueError(msg)

def read(path,root=ROOT):
    p=(root/path).resolve()
    ensure(p.is_relative_to(root.resolve()) and p.is_file(),'unsafe or missing file '+str(path))
    return json.loads(p.read_text())

TRIAGE_FIVE_PATH = 'governance/erdos_proof_verification/triage/0560-0564.json'


def validate_five_source_scope(row, root=ROOT):
    n=row['problem_id']
    if n not in (560,561,562,563,564):
        return
    doc=read(TRIAGE_FIVE_PATH,root)
    ensure(doc['record_type']=='GCL-ERDOS-560-564-PHASE-A-SCOPE-TRIAGE/1'
           and doc['source_commit']=='536408716724a2402bdfa7c1d764bf83d64a8c89'
           and doc['source_file_blob_sha1']=='4e60263a80af6207aca494d2e1388e44fa372889'
           and doc['cohort_issue']==3217 and doc['phase_B_issue']==3230
           and doc['source_only_verified_count']==3 and doc['source_blocked_count']==2
           and doc['selection_policy']=='SOURCE_SCOPE_BEFORE_PROOF__NO_DUPLICATE_QUEUE__NO_AUTO_CERTIFICATION',
           '560-564 protected triage identity or claim scope drift')
    records=doc['records']
    ensure(len(records)==5 and [r['problem_id'] for r in records]==[560,561,562,563,564],
           '560-564 triage record census drift')
    r=records[n-560]
    expected_selected=n in (560,561,562)
    expected='SELECTED_WITH_MANIFEST' if expected_selected else 'PENDING'
    stage=row['stage_work_items']['A']
    ensure(r['source_audit_issue']==row['source_audit_issue']
           and r['source_issue_body_sha256']==row['source_issue_body_sha256']
           and re.fullmatch('[a-f0-9]{64}',r['source_comment_sha256']) is not None
           and isinstance(r['source_comment_id'],int) and r['source_comment_id']>0
           and r['source_issue_live_custody']=='OPEN__PROJECT_RETURNED__ISSUE_FIELD_RETURNED'
           and r['source_role_return_disposition']=='BOUNDED_TASK_DESIGNED'
           and r['triage_decision']==expected
           and row['source_issue_live_state']=='OPEN_RETURNED'
           and row['triage_decision']==expected
           and row['literature_status_current']=='SOURCE_AUDIT_RETURNED__RESEARCH_STATUS_UNCERTIFIED'
           and row['mathcert_status']=='NOT_SUBMITTED'
           and row['scope']=='OPEN_BOUNDED_LEMMA_ONLY'
           and r['critical_role_pass']['scope']=='STATEMENT_AND_QUEUE_SCOPE_ONLY__NO_PROOF'
           and r['critical_role_pass']['separate_human_identity_claim'] is False
           and r['critical_role_pass']['role']=='LOGICAL_ADVERSARY'
           and r['critical_role_pass']['actor']=='fyremael'
           and all(v is False for v in r['prohibitions'].values()),
           f'problem {n}: source critical-scope or return identity drift')
    comment=f"https://github.com/grandchallenge/MATH-PROGRAMME/issues/{row['source_audit_issue']}#issuecomment-{r['source_comment_id']}"
    ensure(stage['source_lock_receipt']==TRIAGE_FIVE_PATH
           and stage['evidence_refs']==[TRIAGE_FIVE_PATH,comment]
           and stage['work_status']==('VERIFIED_BOUNDED' if expected_selected else 'EVIDENCE_BLOCKED')
           and stage['review_status']==('ROLE_SCOPED_CRITICAL_PASS' if expected_selected else 'BLOCKER_CONFIRMED')
           and stage['blocker']==(None if expected_selected else r['critical_role_pass']['finding'])
           and row['closure_status']==(
               'ADMITTED_BOUNDED_COMPLETE'
               if n==560 and row['stage_work_items']['D']['work_status']=='PROTECTED_ADMITTED'
               else ('IN_PROGRESS' if expected_selected else 'BLOCKED_WITH_EVIDENCE'))
           and r['selected_phase_B_queue_issue']==(3230 if expected_selected else None)
           and r['scope_review']==('SOURCE_READY_FOR_BOUNDED_VERIFICATION' if expected_selected
                                    else ('SOURCE_CONFLICT_REPAIR_REQUIRED' if n==563 else 'EVIDENCE_BLOCKED')),
           f'problem {n}: invalid Phase A triage, evidence or blocker')
    # Phase A was an immutable prerequisite, not a permanent B/C/D freeze.
    # A future stage may advance only if source-selected, previous evidence
    # is reviewed, and its own stage-specific receipts exist. This preserves
    # the original no-promotion gate without deadlocking legitimate Phase B.
    admitted={'VERIFIED_BOUNDED','PROTECTED_ADMITTED','REUSED_SCOPE_VERIFIED',
              'NOT_APPLICABLE_REVIEWED'}
    for later, predecessor in (('B','A'),('C','B'),('D','C')):
        v=row['stage_work_items'][later]
        if v['work_status']=='UNEXECUTED':
            ensure(not v['evidence_refs'] and v['formal_replay_receipt'] is None
                   and v['protected_admission_ref'] is None,
                   f'problem {n}: unexecuted stage contains false completion evidence')
            continue
        prior=row['stage_work_items'][predecessor]
        ensure(expected_selected and prior['work_status'] in admitted,
               f'problem {n}: downstream phase not source-selected/reviewed')
        if later in ('C','D'):
            ensure(prior['work_status']=='PROTECTED_ADMITTED',
                   f'problem {n}: {later} requires previous protected admission')
        evidence=v['evidence_refs']
        ensure(isinstance(evidence,list) and bool(evidence)
               and all(isinstance(x,str) and x.startswith(
                   f'governance/erdos_proof_verification/evidence/{n:04}/') for x in evidence)
               and v['source_lock_receipt']==TRIAGE_FIVE_PATH,
               f'problem {n}: downstream evidence/source lock not scoped')
        # The named evidence files must exist in this exact checked-out
        # candidate, not merely be strings that resemble paths.
        ensure(all((root / ref).resolve().is_relative_to(root.resolve())
                   and (root / ref).is_file() for ref in evidence),
               f'problem {n}: downstream proof evidence file missing')
        if v['work_status'] in admitted:
            ensure(v['review_status'] not in ('NOT_REVIEWED','PENDING','')
                   and v['adversarial_review_receipt'] in evidence
                   and v['semantic_equivalence_receipt'] in evidence,
                   f'problem {n}: bounded result lacks semantic/adversarial review')
        if n==561 and later=='B' and v['work_status'] in admitted:
            prefix='governance/erdos_proof_verification/evidence/0561/'
            names=(
                'B_FACTOR_GATE_RECONSTRUCTION_001.md',
                'B_SOURCE_SCOPE_LOCK_001.json',
                'B_SEMANTIC_EQUIVALENCE_001.md',
                'B_ADVERSARIAL_REVIEW_001.md',
                'B_FINITE_FACTOR_ORACLE_001.json',
                'B_RETURN_BINDING_001.json',
            )
            expected_paths={prefix+name for name in names}
            if v['work_status']=='PROTECTED_ADMITTED':
                expected_paths.add(prefix+'B_PROTECTED_CUSTODY_BINDING_001.json')
            ensure(set(evidence)==expected_paths
                   and v['review_status']=='ROLE_SCOPED_CRITICAL_PASS'
                   and v['source_lock_receipt']==TRIAGE_FIVE_PATH
                   and v['semantic_equivalence_receipt']==prefix+'B_SEMANTIC_EQUIVALENCE_001.md'
                   and v['adversarial_review_receipt']==prefix+'B_ADVERSARIAL_REVIEW_001.md'
                   and v['formal_replay_receipt'] is None
                   and v['axiom_report_receipt'] is None
                   and v['blocker']=='PRECURSOR_CLAIMS_3_2_TO_3_8_NOT_INDEPENDENTLY_REPLAYED'
                   and row['scope']=='OPEN_BOUNDED_LEMMA_ONLY'
                   and row['closure_status']=='IN_PROGRESS'
                   and row['mathcert_status']=='NOT_SUBMITTED'
                   and row['certification_ref'] is None,
                   'problem 561 B: incomplete review or false mathematical admission')
            source=read(prefix+'B_SOURCE_SCOPE_LOCK_001.json',root)
            oracle=read(prefix+'B_FINITE_FACTOR_ORACLE_001.json',root)
            ret=read(prefix+'B_RETURN_BINDING_001.json',root)
            ensure(
                source.get('record_type')=='ERDOS_PV_0561_B_SOURCE_SCOPE_LOCK/1'
                and source.get('assignment_id')=='ERDOS-PV-0561-B'
                and source.get('catalogue_commit')=='536408716724a2402bdfa7c1d764bf83d64a8c89'
                and source.get('catalogue_git_blob_sha1')=='4e60263a80af6207aca494d2e1388e44fa372889'
                and source.get('source_issue_body_sha256')==row['source_issue_body_sha256']
                and source.get('source_audit_result_comment_id')==6918133447
                and source.get('source_status_at_lock')=='open'
                and source.get('primary_2026_version')=='arXiv:2610.25958v1'
                and source.get('primary_2026_html_bytes')==433901
                and source.get('primary_2026_html_sha256')=='abcf3930c1b8d77578286b701d9317b63e7ea3832dcf10c627ef1220a32f04f7'
                and source.get('primary_2026_proof_claim')=='THEOREM_1_2_S_EQUALS_2__PAPER_AUTHOR_CLAIM'
                and source.get('bounded_independent_target')=='COROLLARY_2_6_PARITY_SPECIALIZATION_AND_CLAIM_3_10_CONDITIONAL_FINAL_CONTRADICTION'
                and source.get('formalization_work_required') is True
                and source.get('mathcert_status')=='NOT_SUBMITTED'
                and all(source.get(flag) is False for flag in (
                    'independent_1978_primary_replay','independent_2002_primary_replay',
                    'formal_provider_file_at_admitted_snapshot',
                    'original_general_conjecture_solved',
                    'mathematical_certification','external_independent_review_attested')),
                'problem 561 B: source lock or versioned theorem scope drift')
            ensure(
                oracle.get('record_type')=='ERDOS_PV_0561_B_FINITE_FACTOR_GATE_REPLAY/1'
                and oracle.get('assignment_id')=='ERDOS-PV-0561-B'
                and oracle.get('primary_preprint_version')=='2610.25958v1'
                and oracle.get('test_count')==6
                and oracle.get('test_result')=='PASS'
                and oracle.get('test_stdout_sha256')=='526e71b645ace0c1f3ccef175f687bbddea3cd08fc8a26730f2aa4f79fb6ef1b'
                and oracle.get('independent_cut_vs_direct_coloring_graph_budget_comparisons')==1004
                and oracle.get('complete_cut_certificates_on_0_through_4')==46935
                and oracle.get('five_vertex_max_degree_2_full_census')==253
                and oracle.get('synthetic_reduced_case_cut_samples')==12160
                and oracle.get('integer_inequality_parameter_cases')==12331
                and oracle.get('status')=='FINITE_REGRESSION_PASS__CONDITIONAL_PROOF_NOT_KERNEL_CERTIFIED'
                and oracle.get('full_theorem_1_2_verified') is False
                and oracle.get('mathematical_certification') is False,
                'problem 561 B: bounded numerical evidence or proof-class drift')
            ensure(
                ret.get('record_type')=='ERDOS_PV_0561_B_CLAIM_AND_WORKER_RETURN/1'
                and ret.get('assignment_id')=='ERDOS-PV-0561-B'
                and ret.get('source_issue_body_sha256')==row['source_issue_body_sha256']
                and ret.get('claim_sha')=='9de9ed70bab495645e5d0bc501441cd2e4935512'
                and ret.get('claim_source_manifest_blob')=='7bdd13ac702be3ca6c9e409401088536ab0e99e4'
                and ret.get('claim_actor')=='fyremael'
                and ret.get('return_comment_id')==6965492109
                and ret.get('return_body_sha256')=='40773b15a10b06ee2c4d842f36c8f424b39031debd6cafd4513ec4066e302870'
                and ret.get('single_result_readback') is True
                and ret.get('full_you_theorem_1_2_verified') is False
                and ret.get('whole_erdos_561_solved') is False
                and ret.get('lean_formal_proof_present') is False
                and ret.get('mathcert_certified') is False,
                'problem 561 B: authenticated unique worker return drift')
            refs=oracle.get('source_refs',{})
            expected_refs={
                'factor_oracle','oracle_tests','mathematical_reconstruction',
                'semantic_normalization','adversarial_review','source_lock'}
            ensure(set(refs)==expected_refs and len(refs)==6,
                   'problem 561 B: missing exact proof/source reference')
            for key,ref in refs.items():
                path=ref.get('path','')
                full=(root/path).resolve()
                ensure(isinstance(path,str)
                       and full.is_relative_to(root.resolve())
                       and full.is_file()
                       and re.fullmatch('[0-9a-f]{64}',ref.get('sha256','')),
                       'problem 561 B: invalid evidence ref '+key)
                if key in ('mathematical_reconstruction','semantic_normalization',
                           'adversarial_review','source_lock'):
                    raw=full.read_bytes()
                    ensure(ref.get('bytes')==len(raw)
                           and hashlib.sha256(raw).hexdigest()==ref['sha256'],
                           'problem 561 B: immutable proof/source bytes drift '+key)
            ensure(refs['mathematical_reconstruction']['path']==prefix+'B_FACTOR_GATE_RECONSTRUCTION_001.md'
                   and refs['semantic_normalization']['path']==prefix+'B_SEMANTIC_EQUIVALENCE_001.md'
                   and refs['adversarial_review']['path']==prefix+'B_ADVERSARIAL_REVIEW_001.md'
                   and refs['source_lock']['path']==prefix+'B_SOURCE_SCOPE_LOCK_001.json',
                   'problem 561 B: protected proof path substitution')
            if v['work_status']=='PROTECTED_ADMITTED':
                merge='070f9a9d71b22132d48d7c1dc0c05671c11c0a90'
                custody_path=prefix+'B_PROTECTED_CUSTODY_BINDING_001.json'
                c=read(custody_path,root)
                c_sha=hashlib.sha256((root/custody_path).read_bytes()).hexdigest()
                pathset={
                    'ci/erdos_pv_0561_factor_gate.py',
                    'ci/test_erdos_pv_0561_factor_gate.py',
                    'ci/test_erdos_pv_full_coverage.py',
                    'ci/test_erdos_pv_queue.py',
                    'ci/validate_erdos_pv_full_coverage.py',
                    'governance/policy_shard_registry.json',
                    'governance/erdos_proof_verification/coverage/cohorts/0501-0600.json',
                    prefix+'B_FACTOR_GATE_RECONSTRUCTION_001.md',
                    prefix+'B_SEMANTIC_EQUIVALENCE_001.md',
                    prefix+'B_ADVERSARIAL_REVIEW_001.md',
                    prefix+'B_SOURCE_SCOPE_LOCK_001.json',
                    prefix+'B_FINITE_FACTOR_ORACLE_001.json',
                    prefix+'B_RETURN_BINDING_001.json',
                }
                blobs=c.get('protected_source_and_artifact_blob_ids',{})
                ensure(
                    v['protected_admission_ref']=='grandchallenge/MATH-PROGRAMME@'+merge
                    and c_sha=='3dfa7f37eeb334d14703abce8f7bf071b6e0af6d8bd883b625de045b74a8afd3'
                    and c.get('record_type')=='ERDOS_PV_B_ADMISSION_CUSTODY_BINDING/1'
                    and c.get('assignment_id')=='ERDOS-PV-0561-B'
                    and c.get('phase')=='B' and c.get('problem_id')==561
                    and c.get('source_issue_body_sha256')==row['source_issue_body_sha256']
                    and c.get('source_catalogue_commit')=='536408716724a2402bdfa7c1d764bf83d64a8c89'
                    and c.get('source_catalogue_blob')=='4e60263a80af6207aca494d2e1388e44fa372889'
                    and c.get('protected_evidence_pull_request')=='https://github.com/grandchallenge/MATH-PROGRAMME/pull/3458'
                    and c.get('protected_evidence_head')=='0a5c5624d6a865223eea2404d9286b5323e4d2f3'
                    and c.get('protected_evidence_merge_commit')==merge
                    and c.get('protected_exact_byte_readback')=='MATCHED_THIRTEEN_FILES_AGAINST_GIT_FETCHED_PROTECTED_MERGE'
                    and set(blobs)==pathset and len(blobs)==13
                    and all(re.fullmatch('[0-9a-f]{40}',blob) for blob in blobs.values())
                    and c.get('claim_ref')=='refs/heads/gcl-pv-claims/ERDOS-PV-0561-B'
                    and c.get('claim_sha')=='9de9ed70bab495645e5d0bc501441cd2e4935512'
                    and c.get('claim_actor')=='fyremael'
                    and c.get('claim_source_manifest_blob')=='7bdd13ac702be3ca6c9e409401088536ab0e99e4'
                    and c.get('unique_result_sha256')=='40773b15a10b06ee2c4d842f36c8f424b39031debd6cafd4513ec4066e302870'
                    and c.get('bounded_disposition')=='VERIFIED_CONDITIONAL_FACTOR_GATE__PRECURSOR_REDUCTIONS_UNVERIFIED'
                    and c.get('original_problem_status')=='OPEN'
                    and c.get('mathcert_status')=='NOT_SUBMITTED'
                    and c.get('formalization_work_required') is True
                    and c.get('formalization_residual')=='PRECURSOR_CLAIMS_3_2_TO_3_8_NOT_INDEPENDENTLY_REPLAYED'
                    and c.get('next_phase')=='ERDOS-PV-0561-C'
                    and c.get('release_state')=='PENDING_EXACT_PROTECTED_CUSTODY_MERGE_AND_AUTHENTICATED_READBACK'
                    and all(c.get(flag) is False for flag in (
                        'mathcert_certified','full_you_theorem_1_2_verified',
                        'whole_original_erdos_561_solved',
                        'lean_kernel_proof_present',
                        'external_independent_mathematical_review_attested',
                        'phase_C_automatically_certified',
                        'phase_D_automatically_closed',
                        'cohort_100_problems_complete')),
                    'problem 561 B: protected custody identity or claim-boundary drift')
                # Only immutable original mathematical evidence is byte-stable
                # across subsequent main revisions. Controller/tests can change.
                for path in (prefix+'B_FACTOR_GATE_RECONSTRUCTION_001.md',
                             prefix+'B_SEMANTIC_EQUIVALENCE_001.md',
                             prefix+'B_ADVERSARIAL_REVIEW_001.md',
                             prefix+'B_SOURCE_SCOPE_LOCK_001.json',
                             prefix+'B_FINITE_FACTOR_ORACLE_001.json',
                             prefix+'B_RETURN_BINDING_001.json'):
                    data=(root/path).read_bytes()
                    gitblob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
                    ensure(blobs[path]==gitblob,
                           'problem 561 B: immutable protected proof bytes drift: '+path)
        if n==561 and later=='C' and v['work_status'] in admitted:
            prefix='governance/erdos_proof_verification/evidence/0561/'
            expected={
                'C_FORMAL_APPLICABILITY_001.md':
                  '124c887260709e5618125b3d34a12a7fdc63540d9cf589a554be935814eef923',
                'C_ADVERSARIAL_REVIEW_001.md':
                  '8a838165cf14b2b8fcb5dd201f9d5e112705224602bced7ccebafed5ef3b8cad',
                'C_SOURCE_SCOPE_LOCK_001.json':
                  '625ff10a7c184661e42b988a466759b40b410100aa12e6eeee9dc9a67c2ebbc7',
                'C_LEAN_CORE_REPLAY_001.json':
                  'f86f90c8096c1ca8cd35b630f37fa4bc0f5101d01d6cbc8b50f1ddc182da0a6e',
                'C_LEAN_CORE_STDOUT_001.txt':
                  '7663b11dbbb604efd36982fad51c2436e355d37d2b64fa67dfa17bc1a0489c68',
                'C_RETURN_BINDING_001.json':
                  'e714a47ebd3b62e3fd3a66f1072ea0b30eb608ad7cd364716e0150ad8df89fc1',
            }
            cust=prefix+'C_PROTECTED_CUSTODY_BINDING_001.json'
            paths={prefix+name for name in expected}
            if v['work_status']=='PROTECTED_ADMITTED':paths.add(cust)
            ensure(set(evidence)==paths
                   and v['review_status']=='ROLE_SCOPED_CRITICAL_PASS'
                   and v['source_lock_receipt']==TRIAGE_FIVE_PATH
                   and v['semantic_equivalence_receipt']==prefix+'C_FORMAL_APPLICABILITY_001.md'
                   and v['formal_replay_receipt']==prefix+'C_LEAN_CORE_REPLAY_001.json'
                   and v['axiom_report_receipt']==prefix+'C_LEAN_CORE_STDOUT_001.txt'
                   and v['adversarial_review_receipt']==prefix+'C_ADVERSARIAL_REVIEW_001.md'
                   and v['blocker']=='FORMALIZATION_WORK_REQUIRED__GRAPH_FACTOR_AND_PRECURSOR_CLAIMS'
                   and row['scope']=='OPEN_BOUNDED_LEMMA_ONLY'
                   and row['closure_status']=='IN_PROGRESS'
                   and row['mathcert_status']=='NOT_SUBMITTED'
                   and row['certification_ref'] is None
                   and row['stage_work_items']['D']['work_status']=='UNEXECUTED',
                   'problem 561 C: false scope, review or protected admission')
            for name,digest in expected.items():
                ensure(hashlib.sha256((root/prefix/name).read_bytes()).hexdigest()==digest,
                       'problem 561 C: immutable source, receipt, type or review drift: '+name)
            lean=read(prefix+'C_LEAN_CORE_REPLAY_001.json',root)
            source=read(prefix+'C_SOURCE_SCOPE_LOCK_001.json',root)
            ret=read(prefix+'C_RETURN_BINDING_001.json',root)
            ensure(lean.get('record_type')=='ERDOS_PV_0561_C_LEAN_CORE_REPLAY/1'
                   and lean.get('source_sha256')=='f07d1acfa07ff4b61a60f31646cc77a04eb56330c748feaa4dea7b064d8b6e16'
                   and lean.get('claim_sha')=='a5496eb0bdc1199ce0330de45abc26f05d90e0cd'
                   and lean.get('import_closure')==['Init']
                   and lean.get('positive_exit_code')==0
                   and lean.get('scope')=='ELEVEN_KERNEL_CHECKED_ARITHMETIC_AUXILIARIES_ONLY'
                   and lean.get('lean_version','').startswith('Lean (version 4.33.0')
                   and len(lean.get('types_sha256',{}))==11
                   and len(lean.get('axioms',{}))==11
                   and len(lean.get('hostile',{}))==5
                   and all(set(a)<={'propext','Quot.sound','Classical.choice'}
                           for a in lean['axioms'].values())
                   and all(lean.get(k) is False for k in (
                       'full_factor_theorem_kernel_checked',
                       'star_center_structural_hypotheses_kernel_checked',
                       'full_you_theorem_1_2_kernel_checked',
                       'original_erdos_561_conjecture_solved','mathcert_certified'))
                   and hashlib.sha256((root/lean['source_path']).read_bytes()).hexdigest()
                       ==lean['source_sha256'],
                   'problem 561 C: unacceptable Lean proof or axiom report')
            ensure(source.get('assignment_id')=='ERDOS-PV-0561-C'
                   and source.get('source_issue_body_sha256')==row['source_issue_body_sha256']
                   and source.get('frozen_formal_provider',{}).get('read_status')=='HTTP_404_ABSENT_AT_PINNED_REVISION'
                   and source.get('exact_prior_phase_b',{}).get('evidence_protected_merge')
                       =='070f9a9d71b22132d48d7c1dc0c05671c11c0a90'
                   and source.get('formalization_work_required') is True
                   and source.get('mathcert_status')=='NOT_SUBMITTED'
                   and ret.get('record_type')=='ERDOS_PV_0561_C_CLAIM_AND_WORKER_RETURN/1'
                   and ret.get('claim_sha')=='a5496eb0bdc1199ce0330de45abc26f05d90e0cd'
                   and ret.get('claim_source_manifest_blob')=='a4ea49fe9927d66db70b50a465148082677006d5'
                   and ret.get('return_comment_id')==6973794423
                   and ret.get('return_body_sha256')=='48d1ddbb6cbb0929a4fc74cd741a3580bf58c9c6319643c5deb7f6b41e7c72be'
                   and ret.get('single_result_readback') is True
                   and all(ret.get(k) is False for k in (
                       'full_graph_factor_formalized','whole_erdos_561_solved','mathcert_certified')),
                   'problem 561 C: source or authenticated return mismatch')
        if n==560 and later=='C' and v['work_status'] in admitted:
            prefix='governance/erdos_proof_verification/evidence/0560/'
            required={prefix+x for x in (
                'C_SOURCE_SCOPE_LOCK_001.json',
                'C_LEAN_CORE_REPLAY_001.json',
                'C_LEAN_CORE_STDOUT_001.txt',
                'C_FORMAL_APPLICABILITY_001.md',
                'C_ADVERSARIAL_REVIEW_001.md',
                'C_RETURN_BINDING_001.json',
            )}
            custody_path=prefix+'C_PROTECTED_CUSTODY_BINDING_001.json'
            if v['work_status']=='PROTECTED_ADMITTED':
                required.add(custody_path)
            ensure(set(evidence)==required
                   and v['formal_replay_receipt']==prefix+'C_LEAN_CORE_REPLAY_001.json'
                   and v['axiom_report_receipt']==prefix+'C_LEAN_CORE_STDOUT_001.txt'
                   and v['semantic_equivalence_receipt']==prefix+'C_FORMAL_APPLICABILITY_001.md'
                   and v['adversarial_review_receipt']==prefix+'C_ADVERSARIAL_REVIEW_001.md'
                   and v['review_status']=='ROLE_SCOPED_CRITICAL_PASS'
                   and v['blocker']=='FORMALIZATION_WORK_REQUIRED__COPY_COUNT_TAIL_FIRST_MOMENT'
                   and row['mathcert_status']=='NOT_SUBMITTED',
                   'problem 560 C: bounded formalization residual or review custody false')
            source=read(prefix+'C_SOURCE_SCOPE_LOCK_001.json',root)
            replay=read(prefix+'C_LEAN_CORE_REPLAY_001.json',root)
            returned=read(prefix+'C_RETURN_BINDING_001.json',root)
            ensure(returned.get('record_type')=='ERDOS_PV_0560_C_CLAIM_AND_WORKER_RETURN/1'
                   and returned.get('assignment_id')=='ERDOS-PV-0560-C'
                   and returned.get('claim_sha')=='8b6a32fa6fc8fd037051835fa54542f81ecca50e'
                   and returned.get('return_comment_id')==6947981217
                   and returned.get('return_body_sha256')=='7ac16b9c6ebfdc9c7c549ec0708af0d83af1b1da57aee7371b88dc4eedfa659a'
                   and returned.get('single_result_readback') is True
                   and returned.get('whole_size_ramsey_proved') is False
                   and returned.get('mathcert_certified') is False,
                   'problem 560 C: worker return/source or completion boundary drift')
            if v['work_status']=='PROTECTED_ADMITTED':
                merge='2371fb3feda35d98f6da19855a0a1348ca284afa'
                cust=read(custody_path,root)
                expected_paths=required-{custody_path}
                expected_paths.update({
                    'experiments/erdos_proof_verification/0560/Erdos560Core.lean',
                    'experiments/erdos_proof_verification/0560/lean-toolchain',
                    'experiments/erdos_proof_verification/0560/lakefile.toml',
                    'ci/erdos_pv_0560_formal_replay.py',
                    'ci/test_erdos_pv_0560_formal_replay.py',
                    'governance/formal_validation_registry.json',
                    '.github/workflows/formal-validation.yml',
                    'ci/formal_contract_dependency.py',
                    'governance/erdos_proof_verification/coverage/cohorts/0501-0600.json',
                })
                blobs=cust.get('protected_source_and_artifact_blob_ids',{})
                custody_hash=hashlib.sha256((root/custody_path).read_bytes()).hexdigest()
                ensure(
                    v['protected_admission_ref']=='grandchallenge/MATH-PROGRAMME@'+merge
                    and custody_hash=='e72bff7dee6924da0edcbb794d4ea276bd114147bd830bb5eb5c002f2aa475c3'
                    and cust.get('record_type')=='ERDOS_PV_C_ADMISSION_CUSTODY_BINDING/1'
                    and cust.get('assignment_id')=='ERDOS-PV-0560-C'
                    and cust.get('problem_id')==560 and cust.get('phase')=='C'
                    and cust.get('protected_evidence_head')=='bbc5fcba7afd74919d2cd3c760a5a7aa0da99c5a'
                    and cust.get('protected_evidence_merge_commit')==merge
                    and cust.get('protected_evidence_pull_request')=='https://github.com/grandchallenge/MATH-PROGRAMME/pull/3443'
                    and cust.get('protected_exact_byte_readback')=='MATCHED_FIFTEEN_FILES_AGAINST_GIT_FETCHED_PROTECTED_MERGE'
                    and set(blobs)==expected_paths and len(blobs)==15
                    and all(re.fullmatch('[0-9a-f]{40}',digest) for digest in blobs.values())
                    and cust.get('claim_ref')=='refs/heads/gcl-pv-claims/ERDOS-PV-0560-C'
                    and cust.get('claim_sha')=='8b6a32fa6fc8fd037051835fa54542f81ecca50e'
                    and cust.get('claim_actor')=='fyremael'
                    and cust.get('unique_result_sha256')=='7ac16b9c6ebfdc9c7c549ec0708af0d83af1b1da57aee7371b88dc4eedfa659a'
                    and cust.get('next_phase')=='ERDOS-PV-0560-D'
                    and cust.get('formalization_work_required') is True
                    and cust.get('formalization_residual')=='FORMALIZATION_WORK_REQUIRED__COPY_COUNT_TAIL_FIRST_MOMENT'
                    and cust.get('lean_compiled_auxiliary_theorems')==12
                    and cust.get('lean_rejected_hostile_targets')==3
                    and cust.get('next_phase_documentary_work_executed') is False
                    and cust.get('release_state')=='PENDING_EXACT_PROTECTED_CUSTODY_MERGE_AND_AUTHENTICATED_READBACK'
                    and len(cust.get('nonclaims',{}))==7
                    and all(flag is False for flag in cust.get('nonclaims',{}).values()),
                    'problem 560 C: protected custody and exact identity drift')
                # Sealed evidence is immutable; workflow/registry entries in
                # the hash-locked provenance receipt may evolve in later PRs.
                for source_path in expected_paths & (
                        required | {'experiments/erdos_proof_verification/0560/Erdos560Core.lean'}):
                    raw=(root/source_path).read_bytes()
                    git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
                    ensure(git_blob==blobs[source_path],
                           'problem 560 C: original protected evidence bytes changed: '+source_path)
            expected_source=root/'experiments/erdos_proof_verification/0560/Erdos560Core.lean'
            actual_sha=hashlib.sha256(expected_source.read_bytes()).hexdigest()
            log_sha=hashlib.sha256((root/(prefix+'C_LEAN_CORE_STDOUT_001.txt')).read_bytes()).hexdigest()
            ensure(source.get('formal_applicability')=='YES_FOR_BOUNDED_LEMMA'
                   and source.get('formal_provider_availability')=='NONE_IN_FROZEN_PROVIDER'
                   and source.get('formalization_work_required') is True
                   and source.get('kernel_replay',{}).get('formal_source_sha256')==actual_sha
                   and source.get('kernel_replay',{}).get('full_primary_theorem_compiled') is False
                   and replay.get('record_type')=='ERDOS_PV_0560_C_LEAN_CORE_REPLAY/1'
                   and replay.get('source_sha256')==actual_sha
                   and replay.get('predecessor_main')=='123701f543f32c7bf92197f77f39405a3702f8f4'
                   and replay.get('claim_sha')=='8b6a32fa6fc8fd037051835fa54542f81ecca50e'
                   and replay.get('positive_exit_code')==0
                   and replay.get('positive_stdout_sha256')==log_sha
                   and replay.get('whole_size_ramsey_proved') is False
                   and replay.get('formalization_work_required') is True
                   and replay.get('mathlib_semantic_equivalence_kernel_checked') is False
                   and replay.get('mathcert_certified') is False
                   and set(replay.get('axioms',{}))=={
                        'completeBetween_disjoint','right_subset_neighbors',
                        'completeBetween_symm','completeBetween_mono','n_le_two_pow',
                        'integral_factor_cleared','strict_gate_base','strict_gate_step',
                        'strict_gate_all','integral_denominators_positive',
                        'gap_ge_two','t_ge_four'}
                   and all(set(ax)<={'propext','Quot.sound'}
                           for ax in replay['axioms'].values())
                   and set(replay.get('hostile',{}))=={
                        'incorrect_t_ge_2','incorrect_gap_a_eq_1',
                        'overlap_without_loopless'}
                   and all(c['exit_code']!=0 for c in replay['hostile'].values()),
                   'problem 560 C: exact kernel-source, hostile or claim boundary drift')
        if n==560 and later=='D' and v['work_status'] in admitted:
            prefix='governance/erdos_proof_verification/evidence/0560/'
            required={prefix+name for name in (
                'D_DOCUMENTARY_ADMISSION_001.md',
                'D_EDITORIAL_ADVERSARIAL_REVIEW_001.md',
                'D_DOCUMENTARY_REVIEW_001.json',
                'D_RETURN_BINDING_001.json')}
            if v['work_status']=='PROTECTED_ADMITTED':
                required.add(prefix+'D_PROTECTED_CUSTODY_BINDING_001.json')
            ensure(set(evidence)==required
                   and v['source_lock_receipt']==TRIAGE_FIVE_PATH
                   and v['semantic_equivalence_receipt']==prefix+'D_DOCUMENTARY_ADMISSION_001.md'
                   and v['adversarial_review_receipt']==prefix+'D_EDITORIAL_ADVERSARIAL_REVIEW_001.md'
                   and v['formal_replay_receipt'] is None and v['axiom_report_receipt'] is None
                   and v['review_status']=='ROLE_SCOPED_CRITICAL_PASS'
                   and v['blocker']=='FORMALIZATION_WORK_REQUIRED__COPY_COUNT_TAIL_FIRST_MOMENT'
                   and row['scope']=='OPEN_BOUNDED_LEMMA_ONLY'
                   and row['mathcert_status']=='NOT_SUBMITTED'
                   and row['certification_ref'] is None,
                   'problem 560 D: documentary evidence, scope or formal review drift')
            doc=read(prefix+'D_DOCUMENTARY_REVIEW_001.json',root)
            ret=read(prefix+'D_RETURN_BINDING_001.json',root)
            ensure(doc.get('record_type')=='ERDOS_PV_0560_D_DOCUMENTARY_EVIDENCE/1'
                   and doc.get('assignment_id')=='ERDOS-PV-0560-D'
                   and doc.get('source_issue_body_sha256')==row['source_issue_body_sha256']
                   and doc.get('held_claim_sha')=='0ac8ec3ce8d59868e1d260f8974fb62c36ab0b85'
                   and doc.get('source_catalogue_commit')=='536408716724a2402bdfa7c1d764bf83d64a8c89'
                   and doc.get('original_problem_status')=='OPEN'
                   and doc.get('scope_disposition')=='REVIEWED_VERIFIED_BOUNDED_OFF_DIAGONAL_LEMMA__ORIGINAL_PROBLEM_OPEN'
                   and doc.get('finite_graph_cases')==36168
                   and doc.get('exact_rational_parameter_checks')==987
                   and doc.get('kernel_checked_auxiliary_declarations')==12
                   and doc.get('hostile_kernel_targets_rejected')==3
                   and doc.get('formalization_residual')=='FORMALIZATION_WORK_REQUIRED__COPY_COUNT_TAIL_FIRST_MOMENT'
                   and doc.get('phase_C_protected_custody_merge')=='1f2c11fe2c3f40c9083ebf8603f0fd25e36d5f21'
                   and doc.get('mathcert_status')=='NOT_SUBMITTED'
                   and doc.get('distinct_human_reviewer') is False
                   and doc.get('per_problem_documentary_candidate') is True
                   and doc.get('phase_D_protected_admission_ref') is None
                   and doc.get('cohort_100_problems_complete') is False
                   and doc.get('global_1221_problems_complete') is False
                   and all(doc.get(key) is False for key in (
                       'full_primary_proposition_in_lean',
                       'mathlib_source_equivalence_kernel_checked',
                       'original_diagonal_conjecture_solved',
                       'external_independent_mathematical_review',
                       'mathcert_certified','external_certification_requested')),
                   'problem 560 D: original open/formal/MATHCERT boundary drift')
            ensure(ret.get('record_type')=='ERDOS_PV_0560_D_CLAIM_AND_WORKER_RETURN/1'
                   and ret.get('assignment_id')=='ERDOS-PV-0560-D'
                   and ret.get('claim_sha')=='0ac8ec3ce8d59868e1d260f8974fb62c36ab0b85'
                   and ret.get('claim_source_manifest_blob')=='878243e3026fbe00a99a0af1753e25904bf2e06d'
                   and ret.get('return_comment_id')==6963394409
                   and ret.get('return_body_sha256')=='90d6b082312f3bd26827c0801d34dddff207c89bfbe49157cdcccec11308ffbe'
                   and ret.get('unique_result_verified') is True
                   and ret.get('full_diagonal_conjecture_solved') is False
                   and ret.get('mathcert_certified') is False,
                   'problem 560 D: authenticated return/source binding drift')
            refs=doc.get('source_refs',{})
            expected={'public_document','documentary_admission','adversarial_review',
                      'index','navigation','phase_b_proof','phase_b_count_receipt',
                      'phase_c_lean_receipt','phase_c_lean_stdout','phase_c_source_scope',
                      'phase_c_adversarial','phase_b_custody','phase_c_custody'}
            ensure(set(refs)==expected,'problem 560 D: missing documentary references')
            for key,record in refs.items():
                path=record.get('path','')
                resolved=(root/path).resolve()
                ensure(isinstance(path,str) and resolved.is_relative_to(root.resolve())
                       and resolved.is_file()
                       and re.fullmatch('[a-f0-9]{64}',record.get('sha256','')),
                       'problem 560 D: unsafe or missing source path '+key)
                if key not in ('index','navigation'):
                    actual=resolved.read_bytes()
                    ensure(len(actual)==record.get('bytes')
                           and hashlib.sha256(actual).hexdigest()==record['sha256'],
                           'problem 560 D: documentary source byte drift '+key)
            ensure(refs['public_document']['path']=='docs/erdos/proof-verification-0560.md'
                   and refs['documentary_admission']['path']==prefix+'D_DOCUMENTARY_ADMISSION_001.md'
                   and refs['adversarial_review']['path']==prefix+'D_EDITORIAL_ADVERSARIAL_REVIEW_001.md'
                   and refs['index']['path']=='docs/erdos/index.md'
                   and refs['navigation']['path']=='mkdocs.yml',
                   'problem 560 D: public document identity changed')
            page=(root/'docs/erdos/proof-verification-0560.md').read_text()
            ensure('Original problem: OPEN' in page
                   and 'not necessarily induced' in page
                   and 'The full size-Ramsey counting theorem is not yet formalized.' not in page
                   and 'MATHCERT' in page and 'twelve' in page.lower()
                   and 'formalization' in page.lower()
                   and 'proof-verification-0560.md' in (root/'docs/erdos/index.md').read_text()
                   and 'erdos/proof-verification-0560.md' in (root/'mkdocs.yml').read_text(),
                   'problem 560 D: public claim or navigation not scoped')
            if v['work_status']=='PROTECTED_ADMITTED':
                evidence_merge='fc77c28fd1132efca1ff2cc5db56d8632b06c8e5'
                custody_path=prefix+'D_PROTECTED_CUSTODY_BINDING_001.json'
                custody=read(custody_path,root)
                custody_sha=hashlib.sha256((root/custody_path).read_bytes()).hexdigest()
                expected_paths={
                    'docs/erdos/index.md','docs/erdos/proof-verification-0560.md',
                    'mkdocs.yml','governance/erdos_proof_verification/coverage/cohorts/0501-0600.json',
                    prefix+'D_DOCUMENTARY_ADMISSION_001.md',
                    prefix+'D_DOCUMENTARY_REVIEW_001.json',
                    prefix+'D_EDITORIAL_ADVERSARIAL_REVIEW_001.md',
                    prefix+'D_RETURN_BINDING_001.json',
                    'ci/validate_erdos_pv_full_coverage.py',
                    'ci/test_erdos_pv_full_coverage.py',
                    'ci/test_erdos_pv_queue.py',
                }
                blobs=custody.get('protected_source_and_artifact_blob_ids',{})
                closure_expected=[
                    prefix+'D_DOCUMENTARY_ADMISSION_001.md',
                    prefix+'D_DOCUMENTARY_REVIEW_001.json',
                    prefix+'D_EDITORIAL_ADVERSARIAL_REVIEW_001.md',
                    custody_path,'docs/erdos/proof-verification-0560.md',
                ]
                ensure(v['protected_admission_ref']=='grandchallenge/MATH-PROGRAMME@'+evidence_merge
                       and row['closure_status']=='ADMITTED_BOUNDED_COMPLETE'
                       and row['closure_evidence_refs']==closure_expected
                       and custody_sha=='a5e9d582e2c88a1c69d2cb89c48428b331aa6e52f952ac758c6f590489d638a5'
                       and custody.get('record_type')=='ERDOS_PV_D_ADMISSION_CUSTODY_BINDING/1'
                       and custody.get('assignment_id')=='ERDOS-PV-0560-D'
                       and custody.get('phase')=='D' and custody.get('problem_id')==560
                       and custody.get('source_issue_body_sha256')==row['source_issue_body_sha256']
                       and custody.get('protected_evidence_pull_request')=='https://github.com/grandchallenge/MATH-PROGRAMME/pull/3451'
                       and custody.get('protected_evidence_head')=='890a52e7ff2452fc85b74d8724379ef942f6bb1b'
                       and custody.get('protected_evidence_merge_commit')==evidence_merge
                       and custody.get('protected_exact_byte_readback')=='MATCHED_ELEVEN_FILES_AGAINST_GIT_FETCHED_PROTECTED_MERGE'
                       and set(blobs)==expected_paths and len(blobs)==11
                       and all(re.fullmatch('[a-f0-9]{40}',digest) for digest in blobs.values())
                       and custody.get('claim_ref')=='refs/heads/gcl-pv-claims/ERDOS-PV-0560-D'
                       and custody.get('claim_sha')=='0ac8ec3ce8d59868e1d260f8974fb62c36ab0b85'
                       and custody.get('claim_actor')=='fyremael'
                       and custody.get('unique_result_sha256')=='90d6b082312f3bd26827c0801d34dddff207c89bfbe49157cdcccec11308ffbe'
                       and custody.get('original_problem_status')=='OPEN'
                       and custody.get('mathcert_status')=='NOT_SUBMITTED'
                       and custody.get('formalization_work_required') is True
                       and custody.get('formalization_residual')=='FORMALIZATION_WORK_REQUIRED__COPY_COUNT_TAIL_FIRST_MOMENT'
                       and custody.get('bounded_disposition')=='REVIEWED_VERIFIED_BOUNDED_OFF_DIAGONAL_LEMMA__ORIGINAL_PROBLEM_OPEN'
                       and custody.get('release_state')=='PENDING_EXACT_PROTECTED_CUSTODY_MERGE_AND_AUTHENTICATED_READBACK'
                       and all(custody.get(key) is False for key in (
                           'full_CFW_proposition_2_2_kernel_proved',
                           'source_to_Mathlib_equivalence_kernel_proved',
                           'external_independent_review_attested',
                           'original_diagonal_Knn_conjecture_solved',
                           'mathcert_certified','cohort_100_problems_complete',
                           'global_1221_problems_complete')),
                       'problem 560 D: protected documentary custody, source or closure boundary drift')
                # Verify immutable proof/publication bytes. Original tool and
                # menu files may evolve in subsequent protected changes.
                for path in (required-{custody_path})|{'docs/erdos/proof-verification-0560.md'}:
                    data=(root/path).read_bytes()
                    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
                    ensure(blobs[path]==blob,
                           'problem 560 D: original evidence file changed: '+path)
        if v['work_status']=='PROTECTED_ADMITTED':
            ensure(bool(v['protected_admission_ref']),
                   f'problem {n}: unbound protected admission')
            if n==560 and later=='B':
                locked='grandchallenge/MATH-PROGRAMME@997a3d8068c3b2a036d5811bfabfce2b92a4be15'
                cust='governance/erdos_proof_verification/evidence/0560/B_PROTECTED_CUSTODY_BINDING_001.json'
                ensure(v['protected_admission_ref']==locked and cust in evidence,
                       'problem 560: exact bounded evidence admission identity drift')
                binding=read(cust,root)
                ensure(binding.get('record_type')=='ERDOS_PV_B_ADMISSION_CUSTODY_BINDING/1'
                       and binding.get('assignment_id')=='ERDOS-PV-0560-B'
                       and binding.get('protected_evidence_merge_commit')==locked.split('@')[1]
                       and binding.get('protected_evidence_head')=='1c8797ead93d27dbb5f036c17bbcd78921b1139b'
                       and binding.get('claim_sha')=='321bcc27a63b0732b7154cc7dd0aa6d1fe3549f5'
                       and binding.get('source_issue_body_sha256')==row['source_issue_body_sha256']
                       and binding.get('unique_result_sha256')=='f5c282e50bef75522ba306f10126c5ff7763f8dd92076eb7e69b3162e60258b3'
                       and binding.get('protected_exact_byte_readback')=='MATCHED_EIGHT_FILES'
                       and all(x is False for x in binding.get('nonclaims',{}).values()),
                       'problem 560: protected bounded source evidence or claim boundary drift')
        else:
            ensure(v['protected_admission_ref'] is None,
                   f'problem {n}: protected admission claimed before merge')

def validate_row(row,source,phase_issues,root=ROOT):
    n=source['problem_id'];tag=f'problem {n}'
    ensure(row['problem_id']==n,tag+': wrong ID')
    ensure(row['source_audit_issue']==source['issue_number'],tag+': wrong source issue')
    ensure(re.fullmatch('[0-9a-f]{64}',row['source_issue_body_sha256']) is not None and row['source_issue_body_sha256']==source['issue_body_sha256'],tag+': source body hash mismatch')
    ensure(row['catalogue_status_at_lock']==source['catalogue_status'] and row['catalogue_triage_class_at_lock']==source['triage_class'],tag+': status/triage lock mismatch')
    ensure(row['formal_provider_hint_at_lock'] is source['protected_fc_present'],tag+': formal hint mismatch')
    ensure(row['topics']==source['topics'],tag+': source topics changed')
    ensure(n not in PILOT or row['existing_proof_issue']==PILOT[n],tag+': pilot dedup boundary drift')
    ensure(row['existing_proof_issue'] is None or (isinstance(row['existing_proof_issue'],int) and row['existing_proof_issue']>0),tag+': invalid prior proof issue')
    ensure(row['mathcert_status'] in ('NOT_SUBMITTED','SUBMITTED','CERTIFIED','DECLINED'),tag+': certification status invalid')
    if row['mathcert_status']!='NOT_SUBMITTED':
        ensure(bool(row['certification_ref']) and 'MATHCERT' in row['certification_ref'] and bool(row['closure_evidence_refs']),tag+': certification without MathCERT evidence')
    ensure(row['triage_decision'] in ('PENDING','SELECTED_WITH_MANIFEST','REUSED_EXISTING_VERIFICATION','DECLINED_WITH_REASON'),tag+': unknown triage decision')
    if row['triage_decision']=='DECLINED_WITH_REASON':
        ensure(row.get('triage_reason') and bool(row['closure_evidence_refs']),tag+': silent decline')
    if row['triage_decision']=='REUSED_EXISTING_VERIFICATION':
        ensure(row.get('prior_work_to_reconcile') and row['closure_evidence_refs'],tag+': unevidenced reuse')
    if row['source_issue_live_state']=='NOT_RECONCILED':
        ensure(row['triage_decision'] in ('PENDING','SELECTED_WITH_MANIFEST'),tag+': no current source readback')
    if row['catalogue_status_at_lock']=='open':
        ensure(row['scope']!='FULL_ORIGINAL_CONJECTURE_SOLVED',tag+': open conjecture promoted')
    stages=row['stage_work_items'];ensure(set(stages)==set(PHASES),tag+': missing work stages')
    for stage,rec in stages.items():
        issue=row['existing_proof_issue'] if row['existing_proof_issue'] is not None and stage!='A' else phase_issues[stage]
        ensure(rec['issue_number']==issue and rec['cohort_issue_number']==phase_issues[stage],tag+': incorrect project queue linkage at '+stage)
        ensure(rec['task_id']==f'ERDOS-PV-{n:04}-{stage}',tag+': task ID mismatch')
        ensure(rec['work_status'] in VALID_STATUS,tag+': unknown stage work status')
        ensure(rec['work_status']!='PILOT_REUSE_PENDING_EVIDENCE' or (n in PILOT and stage!='A'),tag+': ungrounded pilot reuse')
        if rec['work_status'] in ('VERIFIED_BOUNDED','PROTECTED_ADMITTED','REUSED_SCOPE_VERIFIED','NOT_APPLICABLE_REVIEWED'):
            ensure(rec['evidence_refs'] and rec['review_status'] not in ('NOT_REVIEWED','PENDING'),tag+': green work without evidence/adversarial review')
        if rec['work_status']=='PROTECTED_ADMITTED':
            ensure(bool(rec['protected_admission_ref']),tag+': admitted without protected readback')
        if rec['formal_replay_receipt'] is not None:
            ensure(stage=='C' and bool(rec['axiom_report_receipt']) and bool(rec['semantic_equivalence_receipt']),tag+': kernel replay missing axiom/type receipts')
        if rec['work_status']=='EVIDENCE_BLOCKED':
            ensure(rec['blocker'] and rec['evidence_refs'],tag+': blocker without evidence')
    if row['closure_status']=='ADMITTED_BOUNDED_COMPLETE':
        ensure(stages['D']['work_status']=='PROTECTED_ADMITTED' and bool(row['closure_evidence_refs']),tag+': false terminal closure')
        ensure(row['source_issue_live_state']!='NOT_RECONCILED' and row['triage_decision']!='PENDING',tag+': closed without source/triage')
        admitted={'VERIFIED_BOUNDED','PROTECTED_ADMITTED','REUSED_SCOPE_VERIFIED','NOT_APPLICABLE_REVIEWED'}
        ensure(all(stages[p]['work_status'] in admitted for p in PHASES),tag+': terminal stages not actually reviewed')
    else:ensure(row['closure_status'] in ('NOT_STARTED','IN_PROGRESS','BLOCKED_WITH_EVIDENCE'),tag+': invalid closure status')
    validate_five_source_scope(row,root)

def validate(root=ROOT):
    registry=read(REG,root);source_path=root/SRC;source=read(SRC,root)
    ensure(registry['record_type']=='ERDOS_PV_EXHAUSTIVE_QUEUE_REGISTRY/1','wrong registry identity')
    ensure(registry['source_registry_sha256']==hashlib.sha256(source_path.read_bytes()).hexdigest(),'source registry byte drift')
    ensure(registry['source_lock']==source['source'],'source lock drift')
    src=source['issues'];ensure(len(src)==1221 and [x['problem_id'] for x in src]==list(range(1,1222)),'source missing/duplicate problem')
    ensure(registry['population']['count']==1221 and registry['population']['unique_count']==1221 and not registry['population']['missing_ids'],'population count fiction')
    counts=dict(sorted(collections.Counter(x['catalogue_status'] for x in src).items()))
    ensure(registry['population']['historical_status_counts']==counts,'source status census drift')
    ensure(registry['population']['formal_provider_hints']==sum(x['protected_fc_present'] for x in src),'formal provider census drift')
    ensure(registry['model']['individual_problem_records']==1221 and registry['model']['new_problem_work_records']==1216 and registry['model']['per_problem_stage_slots']==4884,'scope arithmetic drift')
    ensure(registry['model']['cohort_stage_queue_issues']==52 and registry['model']['crosscutting_queue_issues']==6,'queue issue census drift')
    ensure(registry['inventory_complete'] and registry['source_registry_path']==SRC,'inventory state incompatible')
    ensure(registry['project_number']==2 and registry['queue_class']=='Mathematics','wrong queue')
    ensure(len(registry['cohorts'])==13,'missing cohort')
    ensure(registry['pilots']=={str(k):v for k,v in PILOT.items()},'pilot issue identity drift')
    issue_ids=set();project_ids=set();seen=[];pending=0;complete=0
    for i,meta in enumerate(registry['cohorts']):
        start=1+100*i;end=min(start+99,1221);expected={p:3212+13*j+i for j,p in enumerate(PHASES)}
        ensure((meta['first'],meta['last'],meta['count'])==(start,end,end-start+1),'missing/overlapping cohort range')
        ensure(meta['phase_issues']==expected,'cohort phase issue drift')
        ensure(meta['packet']==f'governance/erdos_proof_verification/coverage/cohorts/{start:04}-{end:04}.json','unsafe cohort pathname')
        packet=read(meta['packet'],root)
        ensure(packet['record_type']=='ERDOS_PV_COHORT_WORKSET/1' and packet['source_lock']==source['source'],'invalid packet source lock')
        ensure(packet['phase_issues']==expected and packet['range']=={'first':start,'last':end,'count':end-start+1},'packet range/queue mismatch')
        ensure(len(packet['items'])==end-start+1,'missing cohort items')
        ensure(packet['phase_project_items']==meta['phase_project_items'],'project refs drift')
        for phase,n in expected.items():
            ensure(n not in issue_ids,'duplicate phase issue');issue_ids.add(n)
            pid=packet['phase_project_items'][phase]
            ensure(isinstance(pid,str) and pid.startswith('PVTI_') and pid not in project_ids,'invalid or duplicate project item');project_ids.add(pid)
        for row,source_row in zip(packet['items'],src[start-1:end]):
            validate_row(row,source_row,expected,root);seen.append(row['problem_id']);pending+=(row['triage_decision']=='PENDING');complete+=(row['closure_status']=='ADMITTED_BOUNDED_COMPLETE')
    ensure(seen==list(range(1,1222)),'source population missing or permuted')
    cross=registry['crosscutting_issues'];ensure(len(cross)==6 and sorted(cross.values())==list(range(3264,3270)),'missing closure/dispatch issues')
    for label,n in cross.items():
        ensure(n not in issue_ids,'crosscut issue collision');issue_ids.add(n)
        pid=registry['crosscutting_project_items'][label]
        ensure(pid.startswith('PVTI_') and pid not in project_ids,'bad crosscut project item');project_ids.add(pid)
    ensure(len(issue_ids)==len(project_ids)==58,'queue inventory not 58 unique project tasks')
    if registry['triage_complete']:ensure(pending==0,'triage called complete with PENDING decisions')
    if registry['proof_verification_complete']:ensure(complete==1221,'proof verification called complete without 1221 admitted rows')
    if registry['documentary_closure_complete']:ensure(registry['proof_verification_complete'],'premature documentary closure')
    if registry['mathcert_certification_inferred']:raise ValueError('certification cannot follow from queue existence')
    return {'result':'PASS','individual_problems':len(seen),'distinct_phase_task_ids':len(seen)*4,'cohorts':13,'project_issues':58,'new_proof_problems':1216,'pilots_reused':5,'triage_pending':pending,'substantive_terminal_count':complete,'formal_provider_hints':registry['population']['formal_provider_hints'],'source_historical_status_counts':counts}

if __name__=='__main__':
    try:print(json.dumps(validate(),sort_keys=True))
    except Exception as exc:
        print(f'ERDOS_PV_FULL_COVERAGE_FAIL: {type(exc).__name__}: {exc}',file=sys.stderr)
        sys.exit(1)
