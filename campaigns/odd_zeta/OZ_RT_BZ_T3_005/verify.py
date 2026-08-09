#!/usr/bin/env python3
import json
from pathlib import Path
import verify_rank
here=Path(__file__).resolve().parent
r=json.loads((here/'SEARCH_RESULT.json').read_text())
j=json.loads((here/'JET_COEFFICIENT_MAP.json').read_text())
for got,(d,nmax) in zip(r['stage_a']['search']['stages'],((0,6),(1,6),(2,6),(3,7),(4,8))):
    x=verify_rank.stage(d,nmax)
    for key in ('equations','component_certificate_ranks','shared_telescoper_rank','rank','unknowns','nullity'):
        assert got[key]==x[key],(d,key,got[key],x[key])
assert j['monomial_count']==198 and j['weight']==5 and j['nested_atom_count_max']==1
assert j['max_atomic_arity']==4 and j['max_one_body_parameter_slots']==4
print('independent OZ-RT-BZ-T3-005 mirror-rank replay and retained weight-five jet map valid')
