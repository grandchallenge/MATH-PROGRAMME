"""Exact formal-jet and cochain-connection controls for R1/077."""
from fractions import Fraction as F
from math import factorial

# Formal independent even moments; "cusp" means |z|/2, not a negative delta jet.
primitive={(0,"cusp",0):F(1)}
kernel={(0,0,0):F(1)}
for j in range(1,9):
    c=F(1,factorial(2*j))
    primitive[2*j,2*j-2,2*j]=c
    kernel[2*j,2*j,2*j]=c
d2primitive={(p,0 if basis=="cusp" else basis+2,m):v
             for (p,basis,m),v in primitive.items()}
assert d2primitive==kernel
for (p,basis,m),c in kernel.items():
    assert p%2==0 and c*factorial(p)==1 and m==p

n=6
def zero():return [[F(0) for _ in range(n)] for _ in range(n)]
def eye():
    out=zero()
    for i in range(n):out[i][i]=F(1)
    return out
def add(a,b):return [[a[i][j]+b[i][j] for j in range(n)] for i in range(n)]
def sub(a,b):return [[a[i][j]-b[i][j] for j in range(n)] for i in range(n)]
def mul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(n)),F(0))
                     for j in range(n)] for i in range(n)]
def coeffs(t):
    return 1+t*t,2+3*t*t+t**4,2*t,6*t+4*t**3

def W(t,sign=1):
    a,b,_,_=coeffs(t);out=eye()
    for offset,c in ((0,sign*a),(3,sign*b)):
        out[offset][offset+1]=c
        out[offset+1][offset+2]=c
        out[offset][offset+2]=c*c/2
    return out

def Wprime(t):
    a,b,ap,bp=coeffs(t);out=zero()
    for offset,c,cp in ((0,a,ap),(3,b,bp)):
        out[offset][offset+1]=cp
        out[offset+1][offset+2]=cp
        out[offset][offset+2]=c*cp
    return out

d0=zero()
for i in range(3):d0[3+i][i]=F(1)

# Independent explicit lower-left block exp((a-b)N), rather than differentiating
# the conjugation identity that the connection check is intended to verify.
def dq_explicit(t):
    a,b,_,_=coeffs(t);g=a-b;out=zero()
    for i in range(3):out[3+i][i]=F(1)
    out[3][1]=g;out[4][2]=g;out[3][2]=g*g/2
    return out
def dqprime_explicit(t):
    a,b,ap,bp=coeffs(t);g=a-b;gp=ap-bp;out=zero()
    out[3][1]=gp;out[4][2]=gp;out[3][2]=g*gp
    return out

scales=[F(-2),F(-1),F(-1,2),F(0),F(1,3),F(1),F(2)]
for t in scales:
    wt=W(t);wi=W(t,-1)
    assert mul(wi,wt)==eye()==mul(wt,wi)
    dq=mul(mul(wi,d0),wt)
    assert dq==dq_explicit(t)
    assert mul(dq,dq)==zero()
    A=mul(wi,Wprime(t))
    assert add(dqprime_explicit(t),sub(mul(A,dq),mul(dq,A)))==zero()
    assert W(-t)==wt and dq_explicit(-t)==dq

def transport(s,t):return mul(W(t,-1),W(s))
for s in scales:
    for t in scales:
        T=transport(s,t)
        assert mul(T,dq_explicit(s))==mul(dq_explicit(t),T)
        for u in scales:
            assert mul(transport(t,u),T)==transport(s,u)

# Hostile control: the bare regulator derivative is not a cochain connection.
assert dqprime_explicit(F(1))!=zero()
print("PASS: 9 formal independent-moment delta-jet spatial-derivative identities")
print("PASS: 7 exact regulator conjugation and transported-connection controls")
print("PASS: 49 cochain transports and 343 exact scale cocycle controls")
print("PASS: bare regulator derivative fails the cochain test away from zero")
print("LIMIT: finite algebra does not prove normal-topology or bounded-input estimates")
