#!/usr/bin/env python3
"""Independent finite-depth phase witness; fixed-depth limits differ from accurate-tail regime."""
from fourier_probe import totients, residue_sequence
import json,cmath,hashlib
from pathlib import Path
XVALUES=(1024,4096,16384,65536)
DEPTHS=(2,4,8,12,16,24,32,48)
rows=[]
for X in XVALUES:
    phi=totients(2*X+max(DEPTHS)+1)
    for L in DEPTHS:
        seq=list(residue_sequence(phi.__getitem__,X,L))
        mod=1<<L
        exact_zero=sum(v==0 for v in seq)
        import math
        re=sum(math.cos(2*math.pi*v/mod) for v in seq)/X
        im=sum(math.sin(2*math.pi*v/mod) for v in seq)/X
        rows.append(dict(X=X,L=L,integral_fraction=round(exact_zero/X,9),
            phase_average_re=round(re,9),phase_average_im=round(im,9),
            phase_average_modulus=round(math.hypot(re,im),9),
            upper_tail_error_bound=(2*X+L+2)/mod))
assert len(rows)==32
data=dict(schema='GCL-ERDOS249-FIXED-DEPTH-STRESS-FINITE/1',
          factual_scope='finite samples; density-one theorem requires separate proof; no S irrationality assertion',
          exact_modular_recursion='A_(N+1,L) = (2*A_(N,L)+totient(N+L+1)) mod 2^L',
          rows=rows)
out=Path(__file__).with_name('depth_stress_results.json')
out.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'focus':[{k:v for k,v in r.items() if k in ('X','L','integral_fraction','phase_average_modulus','upper_tail_error_bound')}
 for r in rows if r['X'] in (1024,65536) and r['L'] in (2,4,8,16,48)]},indent=2))
