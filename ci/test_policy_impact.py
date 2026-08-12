#!/usr/bin/env python3
from __future__ import annotations
import copy
import policy_impact as impact

def main()->int:
    impact.validate_control()
    docs=impact.classify_paths(['docs/governance/example.md']);assert docs['policy_shards']==['core','docs'];assert not any(docs['formal_dirty'].values())
    cmdg=impact.classify_paths(['fixtures/cmdg/extractor_001/log_gcd.json']);assert 'cmdg' in cmdg['policy_shards'];assert cmdg['formal_dirty']['log-gcd'] is True;assert cmdg['formal_dirty']['pc-wp04'] is False
    req=impact.classify_paths(['requirements/policy.txt']);assert 'contracts' in req['policy_shards'];assert req['formal_dirty']['pc-wp04'] and req['formal_dirty']['union-closed-mathcert']
    admin=impact.classify_paths(['ci/administrative_autonomy_runtime.py']);assert admin['policy_shards']==['core','administrative']
    visual=impact.classify_paths(['tools/render_visual_pedagogy_batch3_svg_candidates.py']);assert visual['policy_shards']==['core','contracts','docs'];assert not visual['unknown_paths'];assert not any(visual['formal_dirty'].values())
    full=impact.classify_paths(['.github/workflows/ci.yml']);assert full['policy_shards']==list(impact.ALL_SHARDS);assert all(full['formal_dirty'].values())
    unknown=impact.classify_paths(['brand-new-policy-domain/data.bin']);assert unknown['policy_shards']==list(impact.ALL_SHARDS);assert unknown['unknown_paths'];assert all(unknown['formal_dirty'].values())
    assert impact.normalize_paths(['./docs/x.md'])==['docs/x.md']
    for unsafe in ('../escape','/absolute','a/../escape','..'):
        try:impact.normalize_paths([unsafe])
        except impact.ImpactError:pass
        else:raise AssertionError(f'unsafe changed path accepted: {unsafe}')
    control=impact.load_json(impact.CONTROL_PATH)
    formal=impact.classify_paths([],event_name='schedule',schedule=control['formal_replay']['sentinel']['cron']);assert formal['event_mode']=='formal_sentinel';assert formal['policy_shards']==['core']
    sentinel=impact.classify_paths([],event_name='schedule',schedule=control['policy_dag']['full_policy_sentinel_cron']);assert sentinel['event_mode']=='full_policy_sentinel';assert sentinel['policy_shards']==list(impact.ALL_SHARDS)
    manual=impact.classify_paths([],event_name='workflow_dispatch');assert manual['event_mode']=='manual_full';assert all(manual['formal_dirty'].values())
    pushed=impact.classify_paths(['ci/validate_cmdg_schema_contracts.py'],event_name='push');assert 'docs' in pushed['policy_shards']

    original_loader=impact.load_json
    protected_control=original_loader(impact.CONTROL_PATH);protected_formal=original_loader(impact.FORMAL_PATH);protected_registry=original_loader(impact.REGISTRY_PATH)
    mutations=[]
    m=copy.deepcopy(protected_control);m['classifier']['unknown_path_behavior']='IGNORE';mutations.append(m)
    m=copy.deepcopy(protected_control);m['formal_replay']['clean_transition']['full_replay_allowed']=True;mutations.append(m)
    m=copy.deepcopy(protected_control);m['formal_replay']['clean_transition']['max_attestation_age_hours']=168;mutations.append(m)
    m=copy.deepcopy(protected_control);m['authority_boundary']['required_checks_removed_or_renamed']=True;mutations.append(m)
    m=copy.deepcopy(protected_control);m['claim_boundaries']['mathematical_authority_created']=True;mutations.append(m)
    for mutated in mutations:
        def loader(path,mutated=mutated):
            if path==impact.CONTROL_PATH:return mutated
            if path==impact.FORMAL_PATH:return protected_formal
            if path==impact.REGISTRY_PATH:return protected_registry
            if path==impact.CONTROL_SCHEMA:return original_loader(path)
            if path==impact.REGISTRY_SCHEMA:return original_loader(path)
            return original_loader(path)
        impact.load_json=loader
        try:impact.validate_control()
        except (impact.ImpactError,impact.jsonschema.ValidationError):pass
        else:raise AssertionError('unsafe policy-impact control mutation was accepted')
        finally:impact.load_json=original_loader

    print('policy impact gating rejection tests passed');return 0
if __name__=='__main__':raise SystemExit(main())
