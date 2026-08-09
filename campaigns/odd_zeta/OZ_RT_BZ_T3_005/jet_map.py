from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as Q
import t3_005_parent as parent

Poly = dict[tuple[str, ...], Q]
def const(c=0): c=Q(c); return {():c} if c else {}
def atom(name): return {(name,):Q(1)}
def add(*ps):
    out=defaultdict(Q)
    for p in ps:
        for m,c in p.items(): out[tuple(sorted(m))]+=c
    return {m:c for m,c in out.items() if c}
def scale(p,c): c=Q(c); return {m:c*v for m,v in p.items() if c*v}
def mul(a,b):
    out=defaultdict(Q)
    for m1,c1 in a.items():
        for m2,c2 in b.items(): out[tuple(sorted(m1+m2))]+=c1*c2
    return {m:c for m,c in out.items() if c}
def sub(a,b): return add(a,scale(b,-1))
def swap_name(name):
    for src,dst in (("H_k_","H_l_"),("H_l_","H_k_"),("H_nk_","H_nl_"),("H_nl_","H_nk_"),("A_k_","A_l_"),("A_l_","A_k_"),("B_k_","B_l_"),("B_l_","B_k_"),("U_k_l_","U_l_k_"),("U_l_k_","U_k_l_"),("ES_k_","ES_l_"),("ES_l_","ES_k_")):
        if name.startswith(src): return dst+name[len(src):]
    return name
def swap(p):
    out=defaultdict(Q)
    for m,c in p.items(): out[tuple(sorted(swap_name(x) for x in m))]+=c
    return {m:c for m,c in out.items() if c}
def Hk(r): return atom(f"H_k_{r}")
def Hl(r): return atom(f"H_l_{r}")
def Hkl(r): return atom(f"H_kl_{r}")
def Hnk(r): return atom(f"H_nk_{r}")
def Ak(r): return atom(f"A_k_{r}")
def Al(r): return atom(f"A_l_{r}")
def Bk(r): return atom(f"B_k_{r}")
def Bl(r): return atom(f"B_l_{r}")
def C(r): return atom(f"C_{r}")
def Ukl(r,m): return atom(f"U_k_l_{r}_{m}")
def Ulk(r,m): return atom(f"U_l_k_{r}_{m}")
def ESk(r,m): return atom(f"ES_k_{r}_{m}")
def ESl(r,m): return atom(f"ES_l_{r}_{m}")

def target_polynomial():
    Lk=scale(add(Ak(1),C(1),scale(Bk(1),2)),-1); Ll=scale(add(Al(1),C(1),scale(Bl(1),2)),-1)
    r11=add(mul(sub(Hkl(1),add(Hk(1),Hl(1))),add(Hk(2),Hl(2))),scale(add(Hk(3),Hl(3)),-1),Ukl(1,2),Ulk(1,2))
    r12=add(scale(mul(sub(add(Hk(1),Hl(1)),Hkl(1)),Hl(3)),-2),mul(Hk(2),Hkl(2)),scale(mul(Hl(2),Hl(2)),Q(-1,2)),mul(Hkl(2),Hl(2)),scale(Hl(4),Q(-5,2)),scale(ESl(1,3),2),scale(Ukl(2,2),-1))
    r22=add(scale(mul(add(Hk(2),Hl(2)),add(Hk(3),Hl(3))),-2),scale(mul(Hkl(3),add(Hk(2),Hl(2))),2),scale(mul(Hkl(2),add(Hk(3),Hl(3))),2),scale(add(Hk(5),Hl(5)),-2),scale(add(ESk(1,4),ESl(1,4)),-6),scale(add(ESk(2,3),ESl(2,3)),-2),scale(add(Ukl(1,4),Ulk(1,4)),6),scale(add(Ukl(2,3),Ulk(2,3)),2))
    W1=add(r22,mul(Lk,r12),mul(Ll,swap(r12)),mul(sub(mul(Lk,Ll),C(2)),r11))
    alpha=sub(Ak(1),Al(1)); beta=sub(Bk(1),Bl(1)); psi=add(scale(alpha,Q(1,2)),beta)
    cc=add(scale(add(Ak(2),Al(2)),Q(1,4)),scale(mul(alpha,psi),Q(-1,2)))
    w5=add(Hnk(5),scale(mul(sub(alpha,beta),Hnk(4)),Q(1,2)),mul(cc,Hnk(3)))
    return add(W1,add(w5,swap(w5)))

def is_nested(name): return name.startswith(("U_k_l_","U_l_k_","ES_k_","ES_l_"))
def atom_weight(name):
    p=name.split("_"); return int(p[-2])+int(p[-1]) if is_nested(name) else int(p[-1])
def atom_derivative_order(name): return int(name.split("_")[-1])
def fs(x): return str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def multiplier(mon):
    z=1
    for name in mon: z*=parent.raw_derivative_multiplier(atom_derivative_order(name))
    return z

def coefficient_map():
    monomials=[]
    for i,(mon,coeff) in enumerate(sorted(target_polynomial().items()),1):
        nested=[x for x in mon if is_nested(x)]
        if len(nested)>1 or sum(atom_weight(x) for x in mon)!=5: raise AssertionError("T3 weight-five map structure drift")
        mult=multiplier(mon)
        monomials.append({"id":f"M{i:03d}","coefficient":fs(coeff),"atoms":list(mon),"weight":5,"nested_atom":nested[0] if nested else None,"one_body_atoms":[x for x in mon if not is_nested(x)],"raw_derivative_orders":[atom_derivative_order(x) for x in mon],"raw_derivative_multiplier":mult,"operator_coefficient":fs(coeff/Q(mult))})
    profile=defaultdict(int)
    for x in monomials: profile[f"nested_{int(x['nested_atom'] is not None)}_onebody_{len(x['one_body_atoms'])}"]+=1
    return {"schema_version":"1.0.0","target":"W1(k,l)+2*w5_sym(n,k,l)","weight":5,"extraction":"linear raw mixed derivatives of power-sum isolators; no logarithmic cumulant operation is applied to a telescoping relation","one_body_isolator":"P_r(L,o;z)=prod_{i=1}^L(1-(-z/(o+i))^r)","raw_derivative_rule":"d^r/dz^r P_r(L,o;z)|_0=(-1)^(r+1)*r!*(H_(o+L)^(r)-H_o^(r))","monomial_count":len(monomials),"all_monomials_weight_five":True,"max_atomic_arity":max(len(x['atoms']) for x in monomials),"max_one_body_parameter_slots":max(len(x['one_body_atoms']) for x in monomials),"nested_atom_count_max":max(int(x['nested_atom'] is not None) for x in monomials),"profile":dict(sorted(profile.items())),"monomials":monomials}

def evaluate_map(n,k,l,mapping=None):
    mapping=coefficient_map() if mapping is None else mapping; out=Q(0)
    for item in mapping['monomials']:
        v=Q(1)
        for name in item['atoms']: v*=parent.direct_atom_value(name,n,k,l)
        out+=Q(item['coefficient'])*v
    return out

def direct_target(n,k,l):
    H=parent.H
    def A(x,r): return H(n+x,r)-H(x,r)
    def B(x,r): return H(n-x,r)-H(x,r)
    def Cc(r): return H(n+k+l,r)-H(k+l,r)
    def U(a,b,r,m): return sum((H(t+b,m)/Q(t**r) for t in range(1,a+1)),Q(0))
    def ES(x,r,m): return sum((H(t,m)/Q(t**r) for t in range(1,x+1)),Q(0))
    def L(x): return -A(x,1)-Cc(1)-2*B(x,1)
    def r11(a,b): return (H(a+b,1)-H(a,1)-H(b,1))*(H(a,2)+H(b,2))-H(a,3)-H(b,3)+U(a,b,1,2)+U(b,a,1,2)
    def r12(a,b): return -2*(H(a,1)+H(b,1)-H(a+b,1))*H(b,3)+H(a,2)*H(a+b,2)-H(b,2)**2/Q(2)+H(a+b,2)*H(b,2)-Q(5,2)*H(b,4)+2*ES(b,1,3)-U(a,b,2,2)
    def r22(a,b): return -2*(H(a,2)+H(b,2))*(H(a,3)+H(b,3))+2*H(a+b,3)*(H(a,2)+H(b,2))+2*H(a+b,2)*(H(a,3)+H(b,3))-2*H(a,5)-2*H(b,5)-6*ES(a,1,4)-6*ES(b,1,4)-2*ES(a,2,3)-2*ES(b,2,3)+6*U(a,b,1,4)+6*U(b,a,1,4)+2*U(a,b,2,3)+2*U(b,a,2,3)
    W1=r22(k,l)+L(k)*r12(k,l)+L(l)*r12(l,k)+(L(k)*L(l)-Cc(2))*r11(k,l)
    def w5(a,b):
        alpha=A(a,1)-A(b,1); beta=B(a,1)-B(b,1); psi=alpha/Q(2)+beta
        cc=(A(a,2)+A(b,2))/Q(4)-alpha*psi/Q(2)
        return H(n+a,5)+(alpha-beta)*H(n+a,4)/Q(2)+cc*H(n+a,3)
    return W1+w5(k,l)+w5(l,k)

def verify_map_exact_samples(mapping=None):
    mapping=coefficient_map() if mapping is None else mapping; checks=0
    for n in range(2,7):
        for k in range(n+1):
            for l in range(n+1):
                if evaluate_map(n,k,l,mapping)!=direct_target(n,k,l): raise AssertionError("weight-five jet coefficient map drift")
                checks+=1
    return checks

def verify_raw_jet_atoms():
    mapping=coefficient_map(); names=sorted({x for item in mapping['monomials'] for x in item['atoms']}); checks=0
    for n in range(2,6):
        for k in range(n+1):
            for l in range(n+1):
                for name in names:
                    if is_nested(name):
                        _,_,_,m=parent.nested_atom_parts(name); lhs=parent.nested_raw_derivative_sum(name,n,k,l); rhs=Q(parent.T(n,k,l)*parent.raw_derivative_multiplier(m))*parent.nested_atom_value(name,n,k,l)
                    else:
                        order=atom_derivative_order(name); lhs=parent.one_body_raw_derivative_at_zero(name,n,k,l); rhs=Q(parent.raw_derivative_multiplier(order))*parent.one_body_atom_value(name,n,k,l)
                    if lhs!=rhs: raise AssertionError(f"raw jet extraction drift: {name}")
                    checks+=1
    return checks
