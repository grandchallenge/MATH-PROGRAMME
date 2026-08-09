#!/usr/bin/env python3
import json
from pathlib import Path
here=Path(__file__).resolve().parent
result=json.loads((here/'SEARCH_RESULT.json').read_text(encoding='utf-8'))
jet=json.loads((here/'JET_COEFFICIENT_MAP.json').read_text(encoding='utf-8'))
frontier=result['stage_a']['search']['strongest_frontier']
assert frontier['rank']==1210 and frontier['unknowns']==1210 and frontier['nullity']==0
assert result['stage_a']['search']['external_shift']=='l'
assert result['stage_a']['search']['differences']==['k','s']
assert jet['monomial_count']==198 and jet['weight']==5
assert jet['nested_atom_count_max']==1
assert jet['max_atomic_arity']==4 and jet['max_one_body_parameter_slots']==4
print('OZ-RT-BZ-T3-005 retained mirror frontier and jet map valid')
