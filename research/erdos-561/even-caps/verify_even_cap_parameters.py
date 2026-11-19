#!/usr/bin/env python3
"""Apply unconditional even-cap edge decomposition to exact previous
low-degree 25-case Ramsey method-survivor list. Only natural-number
arithmetic and explicit list comparison; no unpromoted theorem upgraded.
"""
import json,os
from pathlib import Path
from collections import Counter
p=Path(os.environ.get('UPSTREAM_561_UNIQUE16_CERTIFICATE',Path(__file__).resolve().parent.parent/'unique16'/'SIXTEEN_TO_EIGHTEEN_PARAMETER_CERTIFICATE.json'))
assert p.is_file(),p
data=json.loads(p.read_text())
old=data['remaining_25']
assert len(old)==25
closed=[];remaining=[]
for pair in old:
    a=tuple(pair['red']);b=tuple(pair['blue']);D=pair['D']
    alpha,beta=a[0]-1,b[0]-1
    assert D==alpha+beta and D==4
    if alpha%2==0 and beta%2==0:
        closed.append([a,b,alpha,beta])
    else:
        remaining.append(pair)
expected={((3,2,1),(3,3,3)),((3,3,2),(3,3,2)),((3,3,3),(3,2,1))}
assert {(tuple(x[0]),tuple(x[1])) for x in closed}==expected
assert len(remaining)==22
unique={tuple(sorted((tuple(x['red']),tuple(x['blue'])))) for x in remaining}
assert len(unique)==11
assert all(set((x['red'][0]-1,x['blue'][0]-1))=={1,3} for x in remaining)
out={'previous_method_survivors':25,'universally_even_cap_exclusions':3,'remaining_ordered':22,
     'remaining_unordered':11,'excluded_pairs':closed,'remaining_22':remaining,
     'remaining_cap_profiles':{'1+3':22}}
Path(__file__).with_name('EVEN_CAP_PARAMETER_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
print('UNIVERSAL_EVEN_CAP_3X3_FILTER_PASS',{'previous':25,'excluded':len(closed),
 'remaining_ordered':len(remaining),'remaining_unordered':len(unique)})
