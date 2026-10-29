import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=R/"governance/oai26_compendium/MANUSCRIPT_INDEX_PINNED.json"
def build():
 b=D.read_bytes()
 assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()=="7a0b00eb9bfdeb59b157a98ee6522fc685580152"
 x=json.loads(b); fs=x["families"]
 assert len(fs)==372 and sum(len(f["manuscripts"]) for f in fs)==719
 return fs
def generate():
 fs=build(); root=R/'docs/oai26'; (root/'catalogue').mkdir(parents=True,exist_ok=True)
 lines=['# OAI-26 catalogue','','372 source-indexed mathematical families; no certification inferred.','','| ID | Headline | PDFs | Status |','| --- | --- | ---: | --- |']
 for f in fs:
  n=f['family_id']; d=root/'families'/n; d.mkdir(parents=True,exist_ok=True)
  p=['# Family '+n+': '+f['headline'].replace('$$','[formula in manuscript]'),'','**REFERENCE ONLY — not independently verified.**','','## Original manuscripts','']
  for m in f['manuscripts']:
   p.append('- ['+m['title'].replace('$$','[formula in manuscript]')+'](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/'+m['pdf_path']+')')
  p+=['','## Verification and editorial status','','Lean replay, Comparator acceptance, manuscript-semantic equivalence, criticism and MATHCERT are distinct. No family-wide assertion is made here.','','[GCL evidence programme](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2850)','','## Full explanation pending','','No reviewed six-section documentary article has been admitted.']
  (d/'index.md').write_text(('\n'.join(p)+'\n').replace(chr(36),'&#36;'))
  lines.append('| ['+n+'](../families/'+n+'/) | '+f['headline'].replace('|','/').replace('$$','[formula in manuscript]')+' | '+str(len(f['manuscripts']))+' | REFERENCE_ONLY |')
 (root/'catalogue'/'index.md').write_text(('\n'.join(lines)+'\n').replace(chr(36),'&#36;'))
 return {'families':372,'pdfs':719,'reference_only':372}
