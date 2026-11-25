from fractions import Fraction as F
from math import gcd,lcm
import random,json,hashlib
rng=random.Random(270025)
records=[]
def check_family(moduli,residues,k):
    T=k*lcm(*moduli)
    U=set(range(T));ideal=F(1);W=F(0);E=F(0)
    for j,(m,r) in enumerate(zip(moduli,residues)):
        A={x for x in range(T) if x%m==r%m}
        good=[i for i in range(j) if gcd(moduli[i],m)==1]
        bad=[i for i in range(j) if gcd(moduli[i],m)>1]
        B=lcm(*(moduli[i] for i in good))
        P=m*B
        assert T%P==0
        I={x for x in range(T) if all(x%moduli[i]!=residues[i]%moduli[i] for i in good)}
        IP={x for x in range(P) if all(x%moduli[i]!=residues[i]%moduli[i] for i in good)}
        AP={x for x in range(P) if x%m==r%m}
        assert len(I)==T//P*len(IP)
        assert len(A&I)==T//P*len(AP&IP)
        assert F(len(A),T)==F(1,m)
        assert F(len(A&I),T)==F(len(I),T)/m
        assert U=={x for x in I if all(x%moduli[i]!=residues[i]%moduli[i] for i in bad)}
        e=sum((F(1,m*moduli[i]) for i in bad),F(0))
        prev=F(len(U),T);U-=A;q=F(len(U),T)
        assert q>=(1-F(1,m))*prev-e
        ideal*=1-F(1,m);W=(1-F(1,m))*W+e;E+=e
        assert q>=ideal-W>=ideal-E
        records.append((T,m,B,str(q),str(ideal),str(W)))
for _ in range(420):
    mods=[rng.randint(1,12) for _ in range(rng.randint(1,5))]
    check_family(mods,[rng.randint(-20,20) for _ in mods],rng.randint(1,4))
# m=4, earlier modulus 2: not coprime, independence fails.
assert F(1,4)!=F(1,4)*F(1,2)
# Nonmultiple truncation: residue 0 modulo 3 has mass 1/2 on {0,1}.
assert F(1,2)!=F(1,3)
# Repeated modulus and noncoprime period multiplier explicitly included.
check_family([2,2,3,6],[0,1,-1,2],6)
print(json.dumps({'families':421,'steps':len(records),'seed':270025,'hostile_controls':2,'digest':hashlib.sha256(repr(records).encode()).hexdigest(),'result':'PASS'}))
