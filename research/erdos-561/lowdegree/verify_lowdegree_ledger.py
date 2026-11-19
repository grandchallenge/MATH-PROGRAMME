#!/usr/bin/env python3
"""Exact reduction of 75 method survivors by audited low-degree deductions
and strictly applicable literature statements. Does NOT certify the
upstream joint-three-star residual theorem used in the Ramsey reduction.
"""
import json,collections,os
from pathlib import Path
src=Path(os.environ.get('UPSTREAM_561_CERTIFICATE', Path(__file__).resolve().parent.parent/'unique-core'/'GENERAL_CORE_PARAMETER_CERTIFICATE.json'))
assert src.is_file()
j=json.loads(src.read_text())
entries=[]
for record in j['remaining_pairs']:
 a,b,d=tuple(record[0]),tuple(record[1]),record[2]
 E=sum(max(a[i]+b[k-i]-1 for i in range(3) if 0<=k-i<3) for k in range(5))-1
 prior=[]
 if len(set(a))==1 and len(set(b))==1:
  prior.append('BEFRS_1978_both_uniform')
 if all(v%2==1 for v in a+b):
  prior.append('Davoodi_2025_Theorem_2_5_all_odd')
 if (len(set(a))==1 and a[0]%2==1 and b[0]%2==1 and min(b)>=2) or \
    (len(set(b))==1 and b[0]%2==1 and a[0]%2==1 and min(a)>=2):
  prior.append('Davoodi_2025_Theorem_2_6_odd_uniform_other_min_ge_2')
 additional=[]
 if d==2:additional.append('EXHAUSTIVE_ALL_MAXDEG2_GRAPH_TYPES')
 if d==3 and E<=15:additional.append('PROVED_ALL_SUBCUBIC_NONCAP_GRAPH_MIN16_EDGES')
 entries.append({'red':a,'blue':b,'D':d,'E':E,'prior_published':prior,'new_methods':additional})

assert len(entries)==75
published=[x for x in entries if x['prior_published']]
method=[x for x in entries if x['new_methods']]
overlap=[x for x in entries if x['prior_published'] and x['new_methods']]
remaining=[x for x in entries if not x['prior_published'] and not x['new_methods']]
assert (len(published),len(method),len(overlap),len(remaining))==(12,25,1,39), (len(published),len(method),len(overlap),len(remaining))
assert len({(x['red'],x['blue']) for x in entries})==75
print('LOW_DEGREE_LEDGER_PASS',json.dumps({'initial':len(entries),'covered_by_literature':len(published),'covered_by_lowdegree_methods':len(method),'overlap':len(overlap),'newly_unaccounted':len(remaining),'unaccounted_by_D':dict(collections.Counter(x['D'] for x in remaining)),'unordered_unaccounted':len({tuple(sorted((x['red'],x['blue']))) for x in remaining})},sort_keys=True))
Path(__file__).with_name('LOWDEGREE_75_CASE_LEDGER.json').write_text(json.dumps({'counts':{'initial':75,'published':len(published),'new_methods':len(method),'overlap':len(overlap),'unaccounted':len(remaining)},'entries':entries,'remaining':remaining},indent=2)+'\n')
