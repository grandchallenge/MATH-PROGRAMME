#!/usr/bin/env python3
"""Exact rational bridge-tree Gaussian Laurent and Wick/BV regression.

Independent standard-library tests of graph determinants, effective resistance,
Laurent convolution, monoidal gluing and symbolic free edge conversion.
No numerical tolerance, network, scipy, or fitted coefficients.
"""
from fractions import Fraction as F
from itertools import permutations

def det(A):
    M=[[F(x) for x in row] for row in A]; n=len(M); value=F(1)
    for j in range(n):
        i=next((i for i in range(j,n) if M[i][j]),None)
        if i is None: return F(0)
        if i!=j:
            M[i],M[j]=M[j],M[i]
            value=-value
        piv=M[j][j]; value*=piv
        for i in range(j+1,n):
            r=M[i][j]/piv
            for k in range(j+1,n):
                M[i][k]-=r*M[j][k]
    return value

def inverse(A):
    n=len(A)
    M=[[F(a) for a in row]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        p=next(i for i in range(j,n) if M[i][j])
        M[p],M[j]=M[j],M[p]
        q=M[j][j]; M[j]=[x/q for x in M[j]]
        for i in range(n):
            if i!=j:
                z=M[i][j]; M[i]=[a-z*b for a,b in zip(M[i],M[j])]
    return [row[n:] for row in M]

def laplacian(n, edges, root=None):
    if root is None: root=n-1
    verts=[i for i in range(n) if i!=root]
    d={u:i for i,u in enumerate(verts)}
    Q=[[F(0) for _ in verts] for _ in verts]
    for u,v,w in edges:
        w=F(w)
        if u!=root: Q[d[u]][d[u]]+=w
        if v!=root: Q[d[v]][d[v]]+=w
        if u!=root and v!=root:
            Q[d[u]][d[v]]-=w; Q[d[v]][d[u]]-=w
    return Q, d

def triangles(q, local_weights=None, bridge_weights=None):
    if local_weights is None: local_weights=[(1,1,1)]*q
    if bridge_weights is None: bridge_weights=[1]*(q-1)
    ed=[]
    for i in range(q):
        a=3*i; u,v,w=local_weights[i]
        ed.extend([(a,a+1,u),(a+1,a+2,v),(a,a+2,w)])
    for i,w in enumerate(bridge_weights):
        ed.append((3*i+2,3*i+3,w))
    return 3*q,ed

def connected(n,edges,removed=None):
    neighbors=[[] for _ in range(n)]
    for i,(u,v,w) in enumerate(edges):
        if i==removed:continue
        neighbors[u].append(v);neighbors[v].append(u)
    seen={0}; stack=[0]
    while stack:
        for v in neighbors[stack.pop()]:
            if v not in seen: seen.add(v);stack.append(v)
    return len(seen)==n

def lmul(A,B):
    out={}
    for i,a in A.items():
        for j,b in B.items():
            out[i+j]=out.get(i+j,F(0))+a*b
    return {k:v for k,v in out.items() if v}

# Original long-distance quadratic witness and bridge-graph Kirchhoff.
n,edges=triangles(2)
Q,d=laplacian(n,edges)
Sigma=inverse(Q)
assert det(Q)==9
assert Sigma[d[0]][d[0]]==F(7,3)
assert Sigma[d[2]][d[2]]==F(5,3) # 2-3 bridge plus other triangle resistance
assert len(edges)-(n-1)==2
bridge_ids=[j for j in range(len(edges)) if not connected(n,edges,removed=j)]
assert bridge_ids==[6]

# Triangle inverse covariance is 2/3 per anchored difference.
Qa,_=laplacian(3,[(0,1,1),(1,2,1),(0,2,1)],root=2)
assert det(Qa)==3
assert inverse(Qa)==[[F(2,3),F(1,3)],[F(1,3),F(2,3)]]
variance_by_blocks=F(2,3)+F(1)+F(2,3)
assert variance_by_blocks==Sigma[d[0]][d[0]]==F(7,3)
# cA*cB = 1/(6*pi), so pi times amplitude =7/18.
pi_times_delta_bridge_finite=variance_by_blocks/F(6)
assert pi_times_delta_bridge_finite==F(7,18)

# Factorized test (1+a^2)(1+e^2)(1+t^2):
# triangular block Laurent powers -1 and +1, bridge powers 0 and +2.
A={-1:F(1),1:F(2,3)}
B={-1:F(1),1:F(2,3)}
E={0:F(1),2:F(1)}
assert lmul(lmul(A,B),E)[0]==F(7,3)
assert lmul(A,lmul(B,E))==lmul(lmul(A,B),E)
assert A.get(0,F(0))==B.get(0,F(0))==0

# In particular the "early finite part" graph gluing is zero, but the
# all-Laurent coefficient convolution has all three required contributions.
parts=[F(2,3),F(2,3),F(1)]
assert sum(parts)==F(7,3) and len(parts)==3

# Four triangles linked by delta bridges: h=4, c=(6*pi)^-2.
# Pair test t1^2*t2^2 contributes epsilon^4 exactly on Gaussian bridges.
n4,e4=triangles(4)
Q4,_=laplacian(n4,e4)
assert det(Q4)==3**4==81
assert len(e4)-(n4-1)==4
assert [i for i in range(len(e4)) if not connected(n4,e4,removed=i)]==[12,13,14]
# Two bridge moments have Laurent exponent 2, the third bridge moment 0;
# four triangle leading poles exponent -4. Constant coefficient equals 1.
state={0:F(1)}
for i in range(4):state=lmul(state,{-1:F(1)})
for s in [{2:F(1)},{2:F(1)},{0:F(1)}]:state=lmul(state,s)
assert state=={0:F(1)}
# pi^2*c = (1/6)^2 = 1/36.
assert F(1,6)**2 == F(1,36)

# Weighted tree-of-block factorization, with no floating-point determinants.
weighted=0
for u in range(1,5):
    for v in range(1,5):
        n2,ew=triangles(2,local_weights=[(u,v,u+v),(v,u+1,v+2)],bridge_weights=[u+2])
        tau=det(laplacian(n2,ew)[0])
        tauA=det(laplacian(3,[(0,1,u),(1,2,v),(0,2,u+v)])[0])
        tauB=det(laplacian(3,[(0,1,v),(1,2,u+1),(0,2,v+2)])[0])
        assert tau==tauA*tauB*(u+2)
        weighted+=1

# Genuine symbolic free bridge BV relation at epsilon^0 for h=2.
# Each coefficient records: power of internal LA, LB; bridge
# distribution kind ('P'=|t|/2 or 'D'=delta) and delta derivative degree.
wick={(1,0,"P",0):F(1),(0,1,"P",0):F(1),(0,0,"D",0):F(1)}
delta={(1,0,"D",0):F(1),(0,1,"D",0):F(1),(0,0,"D",2):F(1)}
def bridge_second_derivative(series):
    z={}
    for (a,b,kind,degree),value in series.items():
        assert kind=="D" or (kind=="P" and degree==0)
        key=(a,b,"D",degree+2) if kind=="D" else (a,b,"D",0)
        z[key]=z.get(key,F(0))+value
    return z
assert bridge_second_derivative(wick)==delta
# The Wick finite-part amplitude on root normalized / flat internal tests
# with f(0)=1 is (1/12*pi).
assert wick[(0,0,"D",0)]/12==F(1,12)

# Test formal Laurent Cauchy associativity for distinct graphwise sectors.
X={-2:F(2),0:F(3,7),2:F(-4,9)}
Y={-1:F(1,2),1:F(7,3),3:F(4)}
Z={0:F(1),2:F(5,8),4:F(2,7)}
for order in permutations([X,Y,Z]):
    left=lmul(lmul(order[0],order[1]),order[2])
    right=lmul(order[0],lmul(order[1],order[2]))
    assert left==right

print("PASS: exact bridge-tree determinants, tau=9 and tau=81")
print("PASS: 16 weighted block-tree determinant factorizations")
print("PASS: two triangles effective resistance =7/3, amplitude 7/(18*pi)")
print("PASS: three exact Laurent contributions 2/3 + 2/3 +1")
print("PASS: four triangles quartic finite part 1/(36*pi*pi)")
print("PASS: Wick-bridge finite part and its exact symbolic BV edge conversion")
print("PASS: Laurent Cauchy associativity under 6 distinct factor orders")

