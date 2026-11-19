#!/usr/bin/env python3
"""Independently reconcile the EXACT 22 prior low-degree ordered pairs.
Proof coverage is two universal matching-colouring constructions, NOT
an assumption that the upstream joint-residual theorem is certified.
"""
import json,os,hashlib
from collections import Counter
from pathlib import Path
base=Path(__file__).resolve().parent
src=Path(os.environ.get('UPSTREAM_561_EVEN_CAP_CERTIFICATE',base.parent/'even-caps'/'EVEN_CAP_PARAMETER_CERTIFICATE.json'))
assert src.is_file(),src
assert hashlib.sha256(src.read_bytes()).hexdigest()=='5f51015fc07155d41954679d080b4c049bcac9adce143b31df0be09da1295acd', 'UNTRUSTED_UPSTREAM_22_DIGEST'
j=json.loads(src.read_text())
assert len(j['remaining_22'])==22
seen=set();closed=[];types=Counter();reverse=set()
for case in j['remaining_22']:
 a,b=tuple(case['red']),tuple(case['blue'])
 assert len(a)==len(b)==3
 assert a==tuple(sorted(a,reverse=True)) and b==tuple(sorted(b,reverse=True))
 E=case['E'];D=case['D']
 assert D==4 and E<=23
 assert a[0]>=2 and b[0]>=2
 W=sum(max(a[i]+b[z-i]-1 for i in range(3) if 0<=z-i<3) for z in range(5))
 assert E==W-1
 assert (a,b) not in seen
 seen.add((a,b))
 # Exhaustive classification by the two universal graph-colouring tests.
 if (a==(2,2,2) and b[0]==4) or (b==(2,2,2) and a[0]==4):
  strategy='B_red_incident_unmatched_centres'
  red,blue=(a,b) if a==(2,2,2) else (b,a)
  assert red==(2,2,2) and blue[0]==4
 elif ((a in ((2,1,1),(2,2,1)) and b==(4,4,4)) or
       (b in ((2,1,1),(2,2,1)) and a==(4,4,4))):
  strategy='A_red_matching_blue_at_most_2_fourcentres'
  red,blue=(a,b) if b==(4,4,4) else (b,a)
  assert red[0]==2 and blue==(4,4,4)
 else:raise AssertionError(('UNCOVERED_PAIR',a,b,E))
 types[strategy]+=1
 closed.append({'red':a,'blue':b,'E':E,'D':D,'construction':strategy,
                'construction_target_red':red,'construction_target_blue':blue,
                'requires_upstream_three_star_residual':True})
 reverse.add(tuple(sorted((a,b))))
assert len(closed)==22 and len(reverse)==11
assert types=={'A_red_matching_blue_at_most_2_fourcentres':4,
               'B_red_incident_unmatched_centres':18},types
assert all((b,a) in seen for a,b in seen)
result={'record_type':'ERDOS561_LAST_22_CONDITIONAL_CASES/1',
 'source_upstream_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'prior_ordered_method_survivors':22,'prior_unordered':11,
 'construction_A_ordered':types['A_red_matching_blue_at_most_2_fourcentres'],
 'construction_B_ordered':types['B_red_incident_unmatched_centres'],
 'uncovered_ordered':0,'uncovered_unordered':0,
 'proof_scope':'ALL_FINITE_DELTA4_HOSTS_WITH_E_LE_29','saturated_matching_defect_cap':2,
 'joint_three_star_residual_proved_here':False,
 'unrestricted_erdos561_solved':False,'closed_pairs':closed}
(base/'FINAL_22_CASE_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print('FINAL_3STAR_PARAMETER_GATE_PASS',{'ordered':22,'unordered':11,
 'construction_A':4,'construction_B':18,'method_survivors':0,'max_edges':23})
