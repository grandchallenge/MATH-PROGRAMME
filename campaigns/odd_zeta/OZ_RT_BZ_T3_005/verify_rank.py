from fractions import Fraction as Q
P=1000003; CS=(("ES",2),("ES",1),("U",2),("U",1)); ES=(Q(1),Q(1,2),Q(0))
def rk(n,k,l): return Q((n+k+1)*(n-k)**2*(n+k+l+1),(k+1)**3*(k+l+1))
def rl(n,k,l): return Q((n+l+1)*(n-l)**2*(n+k+l+1),(l+1)**3*(k+l+1))
def Rk(a,n,k,l,s,e): return rk(n,k,l)*((Q(s+k+1)+e)/Q(s+k+1) if a=='U' else 1)
def Rs(a,r,k,s,e):
 z=s+k+1 if a=='U' else s+1; return Q(s**r,(s+1)**r)*(Q(z)+e)/Q(z)
def m2(d): return [(i,j) for i in range(d,-1,-1) for j in range(d-i,-1,-1)]
def m4(d): return [(i,j,h,u) for i in range(d,-1,-1) for j in range(d-i,-1,-1) for h in range(d-i-j,-1,-1) for u in range(d-i-j-h,-1,-1)]
def row(a,r,n,k,l,s,e,d):
 b=[Q(n**i*l**j)*e**q for q in (1,0) for i,j in m2(d)]; A=[z*x for z in (1,rl(n,k,l),rl(n,k,l)*rl(n,k,l+1)) for x in b]
 D=(k+1)**3*(k+l+1)*((s+k+1) if a=='U' else 1); K=lambda kk:[Q(kk*(n+1-kk)*n**i*l**j*kk**h*s**u,D if kk==k else ((kk+0)**3*(kk+l)*(s+kk) if a=='U' else (kk+0)**3*(kk+l)))*e**q for q in (1,0) for i,j,h,u in m4(d)]
 x=K(k); D2=(k+2)**3*(k+l+2)*((s+k+2) if a=='U' else 1); y=[Q((k+1)*(n-k)*n**i*l**j*(k+1)**h*s**u,D2)*e**q for q in (1,0) for i,j,h,u in m4(d)]; Kd=[u-Rk(a,n,k,l,s,e)*v for u,v in zip(x,y)]
 D=(s+1)**r*((s+k+1) if a=='U' else 1); x=[Q((s-1)*(l+1-s)*n**i*l**j*k**h*s**u,D)*e**q for q in (1,0) for i,j,h,u in m4(d)]; sp=s+1; D2=(sp+1)**r*((sp+k+1) if a=='U' else 1); y=[Q((sp-1)*(l+1-sp)*n**i*l**j*k**h*sp**u,D2)*e**q for q in (1,0) for i,j,h,u in m4(d)]; Sd=[u-Rs(a,r,k,s,e)*v for u,v in zip(x,y)]
 return A+Kd+Sd
def q(x): return x.numerator%P*pow(x.denominator%P,-1,P)%P
def elim(rows,na,nb):
 M=[[q(x) for x in reversed(r[na:])]+[q(x) for x in reversed(r[:na])] for r in rows]; z=0
 for c in range(nb):
  p=next((i for i in range(z,len(M)) if M[i][c]),None)
  if p is None:return z,[]
  M[z],M[p]=M[p],M[z]; inv=pow(M[z][c],-1,P); M[z][c:]=[(x*inv)%P for x in M[z][c:]]
  for i in range(z+1,len(M)):
   f=M[i][c]
   if f:M[i][c:]=[(x-f*y)%P for x,y in zip(M[i][c:],M[z][c:])]
  z+=1
 return z,[r[nb:] for r in M[z:] if any(r[nb:])]
def rank(M):
 M=[r[:] for r in M]; z=0
 if not M:return 0
 for c in range(len(M[0])):
  p=next((i for i in range(z,len(M)) if M[i][c]),None)
  if p is None:continue
  M[z],M[p]=M[p],M[z]; inv=pow(M[z][c],-1,P); M[z][c:]=[(x*inv)%P for x in M[z][c:]]
  for i in range(z+1,len(M)):
   f=M[i][c]
   if f:M[i][c:]=[(x-f*y)%P for x,y in zip(M[i][c:],M[z][c:])]
  z+=1
 return z
def stage(d,N):
 na=6*len(m2(d)); nb=4*len(m4(d)); cons=[]; cr={}; eq=0
 for a,r in CS:
  rows=[row(a,r,n,k,l,s,e,d) for e in ES for n in range(4,N+1) for l in range(2,n-1) for k in range(1,n) for s in range(1,l+1)]; rb,c=elim(rows,na,nb); cr[f'{a}_R{r}']=rb; cons+=c; eq+=len(rows)
 sr=rank(cons); u=na+4*nb; return {'equations':eq,'component_certificate_ranks':cr,'shared_telescoper_rank':sr,'rank':sum(cr.values())+sr,'unknowns':u,'nullity':u-sum(cr.values())-sr}
