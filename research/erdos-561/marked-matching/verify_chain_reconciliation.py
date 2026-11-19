#!/usr/bin/env python3
"""Cross-check every pair across the exact preceding protected-ledger stages.
This validates provenance/case bookkeeping, NOT the mathematical truth
of the still-conditional joint 3x3 residual reduction.
"""
import json,os,hashlib
from pathlib import Path
r=Path(__file__).resolve().parent
paths={
 '75':Path(os.environ.get('ERDOS561_UPSTREAM_75',r.parent/'unique-core'/'GENERAL_CORE_PARAMETER_CERTIFICATE.json')),
 '39':Path(os.environ.get('ERDOS561_UPSTREAM_39',r.parent/'lowdegree'/'LOWDEGREE_75_CASE_LEDGER.json')),
 '25':Path(os.environ.get('ERDOS561_UPSTREAM_25',r.parent/'unique16'/'SIXTEEN_TO_EIGHTEEN_PARAMETER_CERTIFICATE.json')),
 '22':Path(os.environ.get('ERDOS561_UPSTREAM_22',r.parent/'even-caps'/'EVEN_CAP_PARAMETER_CERTIFICATE.json')),
}
assert all(p.is_file() for p in paths.values()),paths
expected={'75':'c8cc2088c3f5e91096b248d57363a955d332bcb1bf2bc787a4190b88b3f09985',
 '39':'eb9fee1ee3472b2ae7490b0b104e4a896a2be41914055057aff36db59c7201f0',
 '25':'1ee51aed0080c4b10e5460835dd6a9ec209a45a511dd558d796ce1c64ed51f80',
 '22':'5f51015fc07155d41954679d080b4c049bcac9adce143b31df0be09da1295acd'}
assert all(hashlib.sha256(paths[k].read_bytes()).hexdigest()==v for k,v in expected.items()), 'SOURCE_CHAIN_DIGEST_MISMATCH'
original=json.loads(paths['75'].read_text())
lowdegree=json.loads(paths['39'].read_text())
unique16=json.loads(paths['25'].read_text())
even=json.loads(paths['22'].read_text())
last=json.loads((r/'FINAL_22_CASE_CERTIFICATE.json').read_text())

norm=lambda a,b:(tuple(a),tuple(b))
sets={
 '75':{norm(v[0],v[1]) for v in original['remaining_pairs']},
 '39':{norm(v['red'],v['blue']) for v in lowdegree['remaining']},
 '25':{norm(v['red'],v['blue']) for v in unique16['remaining_25']},
 '22':{norm(v['red'],v['blue']) for v in even['remaining_22']},
 'final_excluded':{norm(v['red'],v['blue']) for v in last['closed_pairs']},
}
assert [len(sets[z]) for z in ('75','39','25','22','final_excluded')]==[75,39,25,22,22]
assert sets['75']>=sets['39']>=sets['25']>=sets['22']
assert sets['22']==sets['final_excluded']
assert [len(sets[a]-sets[b]) for a,b in [('75','39'),('39','25'),('25','22')]]==[36,14,3]
assert (len(sets['75']-sets['39']) + len(sets['39']-sets['25']) + len(sets['25']-sets['22']) + len(sets['final_excluded']))==75
assert len({tuple(sorted(pair)) for pair in sets['75']})>=11
print('FULL_GCL_3STAR_CASE_CHAIN_PASS',{'start':75,'by_lowdegree':39,'by_motif':25,'by_even_caps':22,
 'new_matching_gate':22,'conditional_method_survivors':0,'source_sha256':{
 k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()}})
