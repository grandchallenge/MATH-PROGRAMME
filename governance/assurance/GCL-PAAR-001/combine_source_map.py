"""Combine five exact-commit source-mapping shards without fetching new heads."""
import hashlib,json
from pathlib import Path
p=Path(__file__).parent
rows=[]
for a,b in ((0,3),(3,6),(6,9),(9,12),(12,14)):
 shard=json.loads((p/f'ESTATE_CONTRACT_SOURCES_{a}_{b}.json').read_text())
 rows.extend(shard['entries'])
assert len(rows)==14
assert len({x['repository'] for x in rows})==14
scope=p/'ESTATE_SCOPE_20261017.json'
r={'record_type':'GCL_PAAR_PINNED_SOURCE_MAP/1','scope_sha256':hashlib.sha256(scope.read_bytes()).hexdigest(),'entries':rows,'source_count':14,'semantic_assurance':False}
(p/'ESTATE_CONTRACT_SOURCES_20261017.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
print('COMBINED_PINNED_SOURCE_MAP',len(rows))
