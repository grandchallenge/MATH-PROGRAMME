#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import target

HERE=Path(__file__).resolve().parent
RESULT=HERE/'SEARCH_RESULT.json'
P=1000003
STAGES=[(order,ad,ad+2,base+ad) for order,base in ((2,7),(3,8),(4,9)) for ad in range(7)]

def poly_moments(length,offset,max_order):
    coeff=[Q(1)]+[Q(0)]*max_order
    for i in range(1,length+1):
        inv=Q(1,offset+i)
        for r in range(max_order,0,-1): coeff[r]+=coeff[r-1]*inv
    return [Q(1)]+[Q(factorial(r))*coeff[r] for r in range(1,max_order+1)]

def cumulants(mom):
    out=[Q(0)]*len(mom)
    for n in range(1,len(mom)):
        v=mom[n]
        for j in range(1,n): v-=Q(comb(n-1,j-1))*out[j]*mom[n-j]
        out[n]=v
    return out

def h(m,r): return Q((-1)**(r-1),factorial(r-1))*cumulants(poly_moments(m,0,r))[r]
def a(n,x,r): return Q((-1)**(r-1),factorial(r-1))*cumulants(poly_moments(n,x,r))[r]
def b(n,x,r):
    kl=cumulants(poly_moments(n-x,0,r))[r]; kr=cumulants(poly_moments(x,0,r))[r]
    return Q((-1)**(r-1),factorial(r-1))*(kl-kr)
def c(n,k,l,r): return Q((-1)**(r-1),factorial(r-1))*cumulants(poly_moments(n,k+l,r))[r]
def es(x,r,m): return sum((h(t,m)/Q(t**r) for t in range(1,x+1)),Q(0))
def u(x,y,r,m): return sum((h(t+y,m)/Q(t**r) for t in range(1,x+1)),Q(0))
def L(n,k,l,x): return -a(n,x,1)-c(n,k,l,1)-2*b(n,x,1)
def r11(k,l): return ((h(k+l,1)-h(k,1)-h(l,1))*(h(k,2)+h(l,2))-h(k,3)-h(l,3)+u(k,l,1,2)+u(l,k,1,2))
def r12(k,l): return (-2*(h(k,1)+h(l,1)-h(k+l,1))*h(l,3)+h(k,2)*h(k+l,2)-h(l,2)**2/2+h(k+l,2)*h(l,2)-Q(5,2)*h(l,4)+2*es(l,1,3)-u(k,l,2,2))
def r22(k,l): return (-2*(h(k,2)+h(l,2))*(h(k,3)+h(l,3))+2*h(k+l,3)*(h(k,2)+h(l,2))+2*h(k+l,2)*(h(k,3)+h(l,3))-2*h(k,5)-2*h(l,5)-6*es(k,1,4)-6*es(l,1,4)-2*es(k,2,3)-2*es(l,2,3)+6*u(k,l,1,4)+6*u(l,k,1,4)+2*u(k,l,2,3)+2*u(l,k,2,3))
def W1(n,k,l):
    lk=L(n,k,l,k); ll=L(n,k,l,l)
    return r22(k,l)+lk*r12(k,l)+ll*r12(l,k)+(lk*ll-c(n,k,l,2))*r11(k,l)
def w5(n,k,l):
    alpha=a(n,k,1)-a(n,l,1); beta=b(n,k,1)-b(n,l,1); psi=alpha/2+beta
    cc=(a(n,k,2)+a(n,l,2))/4-alpha*psi/2
    return h(n+k,5)+(alpha-beta)*h(n+k,4)/2+cc*h(n+k,3)
def w5sym(n,k,l): return (w5(n,k,l)+w5(n,l,k))/2

def verify_lift():
    for nv in range(1,7):
        for kv in range(nv+1):
            for lv in range(nv+1):
                for r in range(1,6):
                    if h(nv+kv,r)!=target.H(nv+kv,r): return ['H product lift mismatch']
                    if a(nv,kv,r)!=target.A(nv,kv,r): return ['A product lift mismatch']
                    if b(nv,kv,r)!=target.B(nv,kv,r): return ['B product lift mismatch']
                    if c(nv,kv,lv,r)!=target.C(nv,kv,lv,r): return ['C product lift mismatch']
                if es(kv,1,3)!=target.ES(kv,1,3): return ['ES auxiliary lift mismatch']
                if u(kv,lv,1,2)!=target.U(kv,lv,1,2): return ['U auxiliary lift mismatch']
                if W1(nv,kv,lv)!=target.W1(nv,kv,lv): return ['W1 reconstruction mismatch']
                if w5sym(nv,kv,lv)!=target.w5sym(nv,kv,lv): return ['w5sym reconstruction mismatch']
    return []

def rk(n,k,l): return Q((n+k+1)*(n-k)**2*(n+k+l+1),(k+1)**3*(k+l+1))
def rl(n,k,l): return Q((n+l+1)*(n-l)**2*(n+k+l+1),(l+1)**3*(k+l+1))
def den(n,k,l): return (l+1)**3*(k+l+1)
def mons2(d): return list(reversed([(i,j) for i in range(d+1) for j in range(d+1-i)]))
def mons3(d): return list(reversed([(i,j,h0) for i in range(d+1) for j in range(d+1-i) for h0 in range(d+1-i-j)]))
def matrix(order,ad,qd,nmax):
    ma=mons2(ad); mq=mons3(qd); rows=[]
    for nv in range(order+2,nmax+1):
        for kv in range(nv-order+1):
            for lv in range(nv):
                ratios=[Q(1)]; ratio=Q(1)
                for j in range(order): ratio*=rk(nv,kv+j,lv); ratios.append(ratio)
                row=[]
                for rat in ratios: row.extend(rat*Q(nv**i*kv**j) for i,j in ma)
                rr=rl(nv,kv,lv); dl=Q(den(nv,kv,lv)); dp=Q(den(nv,kv,lv+1))
                for i,j,h0 in mq: row.append(Q(nv**i*kv**j)*(Q(lv**h0,dl)-rr*Q((lv+1)**h0,dp)))
                rows.append(row)
    return rows

def rank_mod(rows):
    m=[]
    for row in rows:
        rr=[]
        for x in row:
            d=x.denominator%P
            if d==0: raise AssertionError('rank-prime denominator collision')
            rr.append((x.numerator%P)*pow(d,-1,P)%P)
        m.append(rr)
    nr=len(m); nc=len(m[0]); r=0
    for col in range(nc):
        pivot=next((i for i in range(r,nr) if m[i][col]),None)
        if pivot is None: continue
        m[r],m[pivot]=m[pivot],m[r]; inv=pow(m[r][col],P-2,P)
        for j in range(col,nc): m[r][j]=m[r][j]*inv%P
        for i in range(nr):
            if i==r: continue
            f=m[i][col]
            if f:
                for j in range(col,nc): m[i][j]=(m[i][j]-f*m[r][j])%P
        r+=1
        if r==nc: break
    return r

def verify(result=None):
    result=json.loads(RESULT.read_text()) if result is None else result; out=verify_lift()
    if out: return out
    if result.get('fixture')!='PARAMETER_LIFT_HIGHER_ORDER_001': out.append('fixture drift')
    if result.get('search_class')!='UNDEFORMED_HYPERGEOMETRIC_PARENT_ORDERS_2_TO_4_K_SHIFT_WITH_L_CERTIFICATE': out.append('search-class drift')
    got=result.get('stages',[])
    if len(got)!=len(STAGES): return out+['stage count drift']
    for rec,(order,ad,qd,nmax) in zip(got,STAGES):
        rows=matrix(order,ad,qd,nmax); rank=rank_mod(rows); unknowns=len(rows[0])
        if rec.get('order')!=order or rec.get('rank')!=rank or rec.get('unknowns')!=unknowns or rec.get('equations')!=len(rows): out.append(f'independent rank replay drift at r={order},a={ad},q={qd}')
        if rank!=unknowns: out.append(f'bounded class not excluded at r={order},a={ad},q={qd}')
    if result.get('terminal')!='NO_ORDER2_TO_ORDER4_CERTIFICATE_IN_BOUNDED_UNDEFORMED_PARENT_CLASSES': out.append('terminal drift')
    if result.get('next_distinct_route')!='PARAMETER_DEPENDENT_ORDER2_WITH_AUXILIARY_T_DIMENSION': out.append('next-route drift')
    if result.get('proof_effect')!='NONE' or result.get('promotion_effect')!='NONE': out.append('effect inflation')
    return out

def main():
    e=verify()
    if e: print('\n'.join(e)); return 1
    print('OZ-RT-BZ-T3-003 parameter lift and independent order-2-to-4 negative frontier verified'); return 0
if __name__=='__main__': raise SystemExit(main())
