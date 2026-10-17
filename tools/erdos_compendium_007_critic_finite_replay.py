#!/usr/bin/env python3
"""Non-authoring finite countercheck of six EC007 sampled numerical claims.
Uses fresh direct enumeration algorithms; not primary-source, proof, or critic approval.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations, product
from math import gcd, isqrt
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = (2,3,5,7,11)

def prime(n):
    return n>=2 and all(n%k for k in range(2,isqrt(n)+1))

def problem_1062():
    n=15; best=-1; count_max=0; first=None
    for mask in range(1<<n):
        values=[i+1 for i in range(n) if mask>>i&1]
        if any(len([b for b in values if a!=b and b%a==0])>1 for a in values):continue
        if len(values)>best:
            best=len(values);first=values;count_max=1
        elif len(values)==best:count_max+=1
    assert best==10 and count_max>0
    return {"n":n,"all_subsets":2**n,"largest_fork_free_subset":best,"maximizers":count_max,"witness":first}

def problem_1065():
    first=[];second=[]
    for p in range(2,101):
        if not prime(p):continue
        t=p-1;one=False;two=False
        for k in range(8):
            a=2**k
            if t%a:continue
            u=t//a
            if prime(u):one=True
            while u%3==0 and u>0:
                u//=3
                if prime(u):two=True
            if prime(u):two=True
        if one:first.append(p)
        if two:second.append(p)
    extra=sorted(set(second)-set(first))
    assert set([3,7,11,13,29,41]) <= set(first) and 19 in extra and set(first)<set(second)
    return {"checked_p_max":100,"first_family":first,"second_family":second,"second_only":extra}

def problem_1173():
    count=0;max_free=0;witness=None
    for mask in range(256):
        V={i for i in range(8) if mask>>i&1}
        if any((i+1)%8 in V for i in V):continue
        count+=1
        if len(V)>max_free:max_free=len(V);witness=sorted(V)
    assert max_free==4 and witness
    return {"graph":"directed eight-cycle","all_subsets":256,"free_subsets":count,"maximum_free_cardinality":max_free,"witness":witness}

def problem_1186():
    out={}
    for n in [8,10,12]:
        triples=[(a,a+d,a+2*d) for d in range(1,(n-1)//2+1) for a in range(n-2*d)]
        minimum=10**9;best=0
        for bits in range(1<<n):
            num=sum(1 for a,b,c in triples if ((bits>>a)&1)==((bits>>b)&1)==((bits>>c)&1))
            if num<minimum:minimum=num;best=1
            elif num==minimum:best+=1
        assert minimum=={8:0,10:1,12:2}[n]
        out[str(n)]={"binary_colorings":1<<n,"positive_step_three_APs":len(triples),"minimum_monochromatic_count":minimum,"minimizers":best}
    return out

def problem_1188():
    mods=(2,3,4,6,8,12);period=24
    options=[[-1]+list(range(p)) for p in mods]
    covered=0;minimal=0; witness=None
    for choice in product(*options):
        chosen=[(p,r) for p,r in zip(mods,choice) if r!=-1]
        if not chosen:continue
        freq=[sum(n%p==r for p,r in chosen) for n in range(period)]
        if not all(freq):continue
        covered+=1
        if all(any(n%p==r and freq[n]==1 for n in range(period)) for p,r in chosen):
            minimal+=1
            if witness is None:witness=chosen
    assert 49140==__import__("math").prod(p+1 for p in mods)
    assert covered==216 and minimal==24
    return {"period":period,"moduli":mods,"possible_assignments":49140,"covering_assignments":covered,"deletion_minimal_assignments":minimal,"example":witness}

def problem_1200():
    values=tuple(range(1,12));options=[[-1]+list(range(p)) for p in P]
    total=0;minimal_mass=None;minimum_witness=None
    for classes in product(*options):
        selected=[(p,r) for p,r in zip(P,classes) if r!=-1]
        # Enforce at least one covering class for EACH positive n<x.
        if not all(any(n%p==r for p,r in selected) for n in values):continue
        total+=1
        mass=sum((Fraction(1,p) for p,r in selected),Fraction())
        if minimal_mass is None or mass<minimal_mass:
            minimal_mass=mass;minimum_witness=selected
    assert __import__("math").prod(p+1 for p in P)==6912
    assert total==14 and minimal_mass==Fraction(2927,2310)
    return {"x":12,"primes_lt_x":P,"possible_assignments":6912,"full_interval_coverings":total,"minimum_reciprocal_mass":str(minimal_mass),"witness":minimum_witness}

def main():
    results={
        "1062":problem_1062(),"1065":problem_1065(),
        "1173":problem_1173(),"1186":problem_1186(),
        "1188":problem_1188(),"1200":problem_1200()
    }
    content=Path(__file__).read_bytes()
    output={
        "record_type":"EC007_SEPARATE_BOUNDED_FINITE_REPLAY/1",
        "cohort_id":"EC-BULK-007",
        "scope":"INDEPENDENT_CODE_PATH_WITHIN_COORDINATOR_RUN__NOT_NONAUTHOR_SPECIALIST_APPROVAL",
        "source_sha256":hashlib.sha256(content).hexdigest(),
        "source":"tools/erdos_compendium_007_critic_finite_replay.py",
        "results":results,
        "review_status":"SIX_SAMPLED_FINITE_EXAMPLES_REPRODUCED; 20_CRITIC_APPROVALS_STILL_PENDING",
        "claim_limit":"Finite exact enumerations do not imply infinite asymptotic, theorem correctness, current catalogue status, primary-paper fidelity, or independent reviewer authentication.",
    }
    p=ROOT/"governance/erdos_compendium/batches/EC-BULK-007_CRITIC_FINITE_REPLAY_20261017.json"
    p.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"checked":[*results],"results":results},sort_keys=True))
if __name__=="__main__":main()
