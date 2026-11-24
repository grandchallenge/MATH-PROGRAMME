"""Exact finite verification of FFKPY Lemma 2.1 and its weighted refinement."""
from itertools import combinations, product
from fractions import Fraction as F
from math import gcd,lcm,prod
import hashlib,json

def check():
    families=[ms for k in range(1,4) for ms in combinations(range(2,8),k)]
    families += [(2,3,4,6),(3,4,6,8),(4,6,9),(6,10,15),(5,6,7)]
    count=0; digest=hashlib.sha256(); tight=0
    for ms in families:
        L=lcm(*ms); ps=[F(1,m) for m in ms]; a=prod(1-p for p in ps)
        beta=sum((ps[i]*ps[j] for j in range(len(ms)) for i in range(j) if gcd(ms[i],ms[j])>1),F(0))
        weighted=sum((ps[i]*ps[j]*prod(1-p for p in ps[j+1:]) for j in range(len(ms)) for i in range(j) if gcd(ms[i],ms[j])>1),F(0))
        total=F(0)
        for rs in product(*(range(m) for m in ms)):
            d=F(sum(all(x%m!=r for m,r in zip(ms,rs)) for x in range(L)),L)
            assert d>=a-weighted>=a-beta,(ms,rs,d,a,beta,weighted)
            if d==a-weighted:tight+=1
            total+=d;count+=1;digest.update(f'{ms}|{rs}|{d}\n'.encode())
        assert total/prod(ms)==a
    # Distinct but dependent classes: deleting the correction fails.
    ms=(2,4); rs=(0,1); d=F(1,4); assert d<F(3,8) and d==F(3,8)-F(1,8)
    # Pairwise-independent binary events need not be jointly independent.
    pts=list(product(range(2),repeat=2)); es=[{p for p in pts if p[0]==0},{p for p in pts if p[1]==0},{p for p in pts if p[0]!=p[1]}]
    assert all(len(e)==2 for e in es) and all(len(a&b)==1 for a,b in combinations(es,2)) and len(set.intersection(*es))==0
    return {'record_type':'ERDOS_PV_0027_A_FINITE_REPLAY/1','families':len(families),'residue_assignments':count,'weighted_equality_cases':tight,'canonical_sha256':digest.hexdigest(),'hostile_no_correction':'2,4 residues 0,1; 1/4 < 3/8','hostile_pairwise_independence':'pairwise independent events with empty triple intersection','full_theorem_B_replayed':False,'kernel_replayed':False,'mathematical_certification':False}
if __name__=='__main__': print(json.dumps(check(),indent=2))
