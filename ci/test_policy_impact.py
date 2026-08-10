#!/usr/bin/env python3
from __future__ import annotations
import policy_impact as impact

def main()->int:
    impact.validate_control()
    docs=impact.classify_paths(['docs/governance/example.md']); assert docs['policy_shards']==['core','docs']; assert not any(docs['formal_dirty'].values())
    cmdg=impact.classify_paths(['fixtures/cmdg/extractor_001/log_gcd.json']); assert 'cmdg' in cmdg['policy_shards']; assert cmdg['formal_dirty']['log-gcd'] is True; assert cmdg['formal_dirty']['pc-wp04'] is False
    req=impact.classify_paths(['requirements/policy.txt']); assert 'contracts' in req['policy_shards']; assert req['formal_dirty']['pc-wp04'] and req['formal_dirty']['union-closed-mathcert']
    admin=impact.classify_paths(['ci/administrative_autonomy_runtime.py']); assert admin['policy_shards']==['core','administrative']
    full=impact.classify_paths(['.github/workflows/ci.yml']); assert full['policy_shards']==list(impact.ALL_SHARDS); assert all(full['formal_dirty'].values())
    unknown=impact.classify_paths(['brand-new-policy-domain/data.bin']); assert unknown['policy_shards']==list(impact.ALL_SHARDS); assert unknown['unknown_paths']; assert all(unknown['formal_dirty'].values())
    control=impact.load_json(impact.CONTROL_PATH)
    formal=impact.classify_paths([],event_name='schedule',schedule=control['formal_replay']['sentinel']['cron']); assert formal['event_mode']=='formal_sentinel'; assert formal['policy_shards']==['core']
    sentinel=impact.classify_paths([],event_name='schedule',schedule=control['policy_dag']['full_policy_sentinel_cron']); assert sentinel['event_mode']=='full_policy_sentinel'; assert sentinel['policy_shards']==list(impact.ALL_SHARDS)
    manual=impact.classify_paths([],event_name='workflow_dispatch'); assert manual['event_mode']=='manual_full'; assert all(manual['formal_dirty'].values())
    pushed=impact.classify_paths(['ci/validate_cmdg_schema_contracts.py'],event_name='push'); assert 'docs' in pushed['policy_shards']
    print('policy impact gating rejection tests passed'); return 0
if __name__=='__main__': raise SystemExit(main())
