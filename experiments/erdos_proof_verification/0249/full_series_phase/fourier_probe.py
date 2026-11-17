#!/usr/bin/env python3
"""ERDOS249 full-S experimental phase probe. Finite evidence only; never a proof of irrationality."""
import argparse, cmath, json, math, hashlib
from pathlib import Path

def totients(n):
    a=list(range(n+1))
    for p in range(2,n+1):
        if a[p]==p:
            for j in range(p,n+1,p):
                a[j]-=a[j]//p
    return a

def comparator(n):
    return 2*(n//2)

def exact_residue(coeff, N, L):
    mask=(1<<L)-1
    return sum(coeff(N+j) << (L-j) for j in range(1,L+1))&mask

def residue_sequence(coeff, X, L):
    mask=(1<<L)-1
    a=exact_residue(coeff,X,L)
    for N in range(X,2*X):
        yield a
        a=((a<<1)+coeff(N+L+1))&mask

def phase_scan(coeff, X, L, H):
    mask=(1<<L)-1
    vals=list(residue_sequence(coeff,X,L))
    # Exact consistency of rolling recurrence at all inspected boundaries, as well as terminal.
    for N in [X,X+1,X+X//2,2*X-1]:
        assert vals[N-X]==exact_residue(coeff,N,L)
    data=[]
    for h in range(1,H+1):
        re=im=0.
        for r in vals:
            angle=2*math.pi*((h*r)&mask)/(1<<L)
            re+=math.cos(angle); im+=math.sin(angle)
        re/=X; im/=X
        data.append(dict(h=h,re=round(re,9),im=round(im,9),
                         modulus=round(math.hypot(re,im),9),
                         gap_to_one=round(math.hypot(re-1,im),9)))
    return data

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--x',type=int,required=True)
    p.add_argument('--l',type=int,default=48)
    p.add_argument('--h',type=int,default=64)
    p.add_argument('--out',required=True)
    a=p.parse_args()
    assert a.x>=64 and a.h>=3 and 2*a.x+a.l+1 < 500000
    assert a.l>=32 and a.l>=4+math.ceil(math.log2(2*a.x+a.l+2))
    phi=totients(2*a.x+a.l+1)
    assert phi[1]==1 and phi[2]==1 and phi[3]==2 and phi[4]==2 and phi[5]==4
    # Explicit independent reference arithmetic for N=1..9, L small.
    for N in range(1,10):
        for L in (4,7,10):
            r=exact_residue(phi.__getitem__,N,L)
            ref=sum(phi[N+j]*(2**(L-j)) for j in range(1,L+1))%2**L
            assert r==ref
    result={'schema':'GCL-ERDOS249-FULL-S-FOURIER-FINITE/1',
            'purpose':'finite first-harmonic diagnostics, NOT a full-S solution or inference of irrationality',
            'x':a.x,'window_N':[a.x,2*a.x-1],'truncation_L':a.l,'max_h':a.h,
            'tail_bound':f'(2*X+L+2)/2^L = {2*a.x+a.l+2}/{1<<a.l}',
            'phase_error_le':2*math.pi*a.h*(2*a.x+a.l+2)/(1<<a.l),
            'strict_control':'a(n)=2*floor(n/2) has exactly rational generating value 4/3; h=3 must have modulus nearly 1',
            'actual_totient':phase_scan(phi.__getitem__,a.x,a.l,a.h),
            'rational_control_4_over_3':phase_scan(comparator,a.x,a.l,a.h),
            'math_status':'OPEN; finite phases do not establish required all-h uniform bound'}
    out=Path(a.out)
    out.write_text(json.dumps(result,indent=2)+'\n')
    raw=out.read_bytes()
    print(json.dumps({'file':str(out),'sha256':hashlib.sha256(raw).hexdigest(),
       'x':a.x,'L':a.l,'H':a.h,'tail_phase_error_bound':result['phase_error_le'],
       'totient_max_modulus':max(result['actual_totient'],key=lambda x:x['modulus']),
       'control_h3':result['rational_control_4_over_3'][2],
       'totient_h1':result['actual_totient'][0],
       'totient_h3':result['actual_totient'][2]},sort_keys=True))
if __name__=='__main__':main()
