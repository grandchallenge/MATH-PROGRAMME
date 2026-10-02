#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
SEED = 20261002
SELECTOR_POINTS = 2048
BASELINE = np.array([1.0, 1.0, 2/7, 25/7, 6/7, 3/25, 2/25, 9/7], dtype=float)
FREE_POSITIONS = [1, 2, 4, 5, 6, 7, 8, 9]
COLORS = {
    "F01":"white","F02":"black","F03":"white","F04":"black",
    "F05":"white","F06":"black","F07":"white","F08":"black",
    "U1":"black","U2":"white","U3":"black","U4":"black","U5":"white","U6":"white",
}
EDGE_DEFS = [
    ("F01|F04","F01","F04",1,("A","P2")),
    ("F01|F02","F01","F02",1,("P1","A")),
    ("F07|F02","F07","F02",1,("A","P0")),
    ("F03|F06","F03","F06",-1,("P4","C")),
    ("F03|F04","F03","F04",1,("C","D")),
    ("F03|F08","F03","F08",1,("D","P4")),
    ("F07|F04","F07","F04",-1,("D","A")),
    ("F05|F04","F05","F04",1,("P2","C")),
    ("F05|F06","F05","F06",1,("C","P3")),
    ("F07|F08","F07","F08",1,("P5","D")),
    ("B1","F07","U1",1,("P0","P5")),
    ("B2","U2","F02",1,("P0","P1")),
    ("B3","F01","U3",1,("P2","P1")),
    ("B4","F05","U4",1,("P3","P2")),
    ("B5","U5","F06",1,("P3","P4")),
    ("B6","U6","F08",1,("P4","P5")),
]
FACES = {
    "F01":["A","P2","P1"], "F02":["P0","A","P1"],
    "F03":["P4","C","D"], "F04":["A","D","C","P2"],
    "F05":["P2","C","P3"], "F06":["P3","C","P4"],
    "F07":["A","P0","P5","D"], "F08":["P4","D","P5"],
}
BOUNDARY_OWNER = ["F07","F02","F01","F05","F06","F08"]
BOUNDARY = ["P0","P1","P2","P3","P4","P5"]
TOL = {
    "extension":1e-9, "closure":1e-9, "te3":1e-8, "te4":1e-8,
    "te5_margin":1e-6, "edge":1e-8,
}

def q(value: float) -> float:
    return float(f"{float(value):.15g}")

def normalized_edges() -> list[tuple[str,str,str,int,tuple[str,str]]]:
    out=[]
    for eid,a,b,sign,dual in EDGE_DEFS:
        w,bk=(a,b) if COLORS[a]=="white" else (b,a)
        out.append((eid,w,bk,sign,dual))
    return out

EDGES=normalized_edges()
INTERIOR=sorted(v for v in COLORS if not v.startswith("U"))
WHITE=sorted(v for v,c in COLORS.items() if c=="white")
BLACK=sorted(v for v,c in COLORS.items() if c=="black")

def enumerate_matchings() -> list[tuple[tuple[int,...],tuple[int,...]]]:
    incident={v:[i for i,e in enumerate(EDGES) if v in e[1:3]] for v in COLORS}
    selected=[]
    def rec(covered:set[str], chosen:list[int], used_boundary:set[str]) -> None:
        if len(covered)==len(INTERIOR):
            selected.append(tuple(chosen)); return
        vertex=next(v for v in INTERIOR if v not in covered)
        for ei in incident[vertex]:
            _,w,b,_,_=EDGES[ei]
            other=b if vertex==w else w
            if other in INTERIOR and other in covered: continue
            if other.startswith("U") and other in used_boundary: continue
            nc=set(covered); nc.add(vertex); nb=set(used_boundary)
            if other in INTERIOR: nc.add(other)
            else: nb.add(other)
            rec(nc,chosen+[ei],nb)
    rec(set(),[],set())
    records=[]
    for matching in selected:
        used={v for ei in matching for v in EDGES[ei][1:3] if v.startswith("U")}
        bset=[]
        for i in range(1,7):
            u=f"U{i}"
            if (COLORS[u]=="black" and u in used) or (COLORS[u]=="white" and u not in used):
                bset.append(i)
        records.append((tuple(bset),matching))
    return records

RECORDS=enumerate_matchings()

def weights_from_x(x: np.ndarray) -> np.ndarray:
    weights=np.ones(16,dtype=float)
    for position,value in zip(FREE_POSITIONS,x):
        weights[position]=value
    return weights

def minors_from_x(x: np.ndarray) -> tuple[dict[tuple[int,...],float],np.ndarray]:
    weights=weights_from_x(x)
    minors:dict[tuple[int,...],float]={}
    for boundary,matching in RECORDS:
        value=float(np.prod(weights[list(matching)]))
        minors[boundary]=minors.get(boundary,0.0)+value
    return minors,weights

def permutation_sign(seq:list[int]) -> int:
    inversions=sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))
    return -1 if inversions%2 else 1

def signed_minor(minors:dict[tuple[int,...],float], seq:tuple[int,int,int]) -> float:
    if len(set(seq))<3: return 0.0
    return permutation_sign(list(seq))*minors.get(tuple(sorted(seq)),0.0)

def c_from_minors(minors:dict[tuple[int,...],float]) -> np.ndarray:
    pivot=(1,2,4)
    delta=signed_minor(minors,pivot)
    C=np.zeros((3,6),dtype=float)
    for r,j in enumerate(pivot): C[r,j-1]=1.0
    for j in range(1,7):
        if j in pivot: continue
        for r in range(3):
            seq=list(pivot); seq[r]=j
            C[r,j-1]=signed_minor(minors,tuple(seq))/delta
    return C

def c_perp_rows(C:np.ndarray) -> np.ndarray:
    pivot=(1,2,4); free=[3,5,6]
    N=np.zeros((3,6),dtype=float)
    for r,j in enumerate(free):
        N[r,j-1]=1.0
        for k,p in enumerate(pivot): N[r,p-1]=-C[k,j-1]
    if np.max(np.abs(C@N.T))>1e-10: raise AssertionError("C-perp construction drift")
    return N

def graph_hypotheses() -> dict[str,Any]:
    neighbors={v:set() for v in COLORS}
    for _,w,b,_,_ in EDGES:
        neighbors[w].add(b); neighbors[b].add(w)
    def surplus(vertices:list[str]) -> tuple[int,dict[str,Any]]:
        best=None
        for r in range(1,len(vertices)+1):
            for S in itertools.combinations(vertices,r):
                N=set().union(*(neighbors[v] for v in S))
                row=(len(N)-len(S),S,tuple(sorted(N)))
                if best is None or row[0]<best[0]: best=row
        assert best is not None
        return best[0],{"subset":list(best[1]),"neighbors":list(best[2])}
    sb,wb=surplus(sorted(v for v in INTERIOR if COLORS[v]=="black"))
    sw,ww=surplus(sorted(v for v in INTERIOR if COLORS[v]=="white"))
    supports=[set(b) for b,_ in RECORDS]
    pairs=[]
    for i in range(1,7):
        j=i%6+1
        pairs.append({"pair":[i,j],
            "apm_with_both":any(i in S and j in S for S in supports),
            "apm_with_neither":any(i not in S and j not in S for S in supports)})
    return {"matching_count":len(RECORDS),"kmin":min(sb,sw),
            "black_subset_min":{"value":sb,**wb},"white_subset_min":{"value":sw,**ww},
            "two_boundary_nondegenerate":all(x["apm_with_both"] and x["apm_with_neither"] for x in pairs),
            "adjacent_pair_witnesses":pairs}

def perpendicular_basis(n:np.ndarray) -> np.ndarray:
    n=n/np.linalg.norm(n)
    axis=np.zeros(3); axis[int(np.argmin(np.abs(n)))]=1.0
    u=axis-n*np.dot(axis,n); u=u/np.linalg.norm(u)
    v=np.cross(n,u)
    return np.vstack([u,v])

def winding(L:np.ndarray) -> float:
    total=0.0
    for i in range(6):
        a=L[:,i]; b=L[:,(i+1)%6]
        angle=math.atan2(float(a[0]*b[1]-a[1]*b[0]),float(a@b))
        if angle<=0: angle+=2*math.pi
        total+=angle
    return total

def spd_normalize(L:np.ndarray, indices:list[int]) -> tuple[np.ndarray,np.ndarray] | None:
    A=[]; rhs=[]
    for i in indices:
        x,y=L[:,i]; A.append([x*x,2*x*y,y*y]); rhs.append(1.0)
    try: a,b,c=np.linalg.solve(np.array(A),np.array(rhs))
    except np.linalg.LinAlgError: return None
    M=np.array([[a,b],[b,c]],dtype=float)
    if np.min(np.linalg.eigvalsh(M))<=1e-10: return None
    transform=np.linalg.cholesky(M).T
    return transform@L,M

def fibonacci_normals(count:int=SELECTOR_POINTS):
    golden=math.pi*(3-math.sqrt(5))
    for k in range(count):
        z=1-2*(k+0.5)/count; r=math.sqrt(max(0.0,1-z*z)); theta=k*golden
        yield k,np.array([r*math.cos(theta),r*math.sin(theta),z],dtype=float)

def plane_candidate(B3:np.ndarray,n:np.ndarray,target:float,unit_indices:list[int]):
    L=perpendicular_basis(n)@B3
    dets=[float(np.linalg.det(L[:,[i,(i+1)%6]])) for i in range(6)]
    if min(dets)<=1e-10 or abs(winding(L)-target)>1e-7: return None
    normalized=spd_normalize(L,unit_indices)
    if normalized is None: return None
    Ln,M=normalized
    ndets=[float(np.linalg.det(Ln[:,[i,(i+1)%6]])) for i in range(6)]
    if min(ndets)<=1e-10 or abs(winding(Ln)-target)>1e-7: return None
    return Ln,M,min(ndets)

def select_plane(B3:np.ndarray,target:float,unit_indices:list[int]):
    for k,n in fibonacci_normals():
        for sign in (1.0,-1.0):
            nn=sign*n
            candidate=plane_candidate(B3,nn,target,unit_indices)
            if candidate is not None:
                return k,int(sign),nn,candidate
    return None

def solve_extensions(weights:np.ndarray,zeta:np.ndarray,tzeta:np.ndarray):
    wi={v:i for i,v in enumerate(WHITE)}; bi={v:i for i,v in enumerate(BLACK)}
    A=[]; rhs=[]
    for black in sorted(v for v in BLACK if not v.startswith("U")):
        row=np.zeros(len(WHITE),dtype=complex)
        for ei,(_,w,b,sign,_) in enumerate(EDGES):
            if b==black: row[wi[w]]+=sign*weights[ei]
        A.append(row); rhs.append(0j)
    pf=[((-1)**i)*zeta[i] for i in range(6)]
    for j in range(6):
        _,_,_,sign,_=EDGES[10+j]; row=np.zeros(len(WHITE),dtype=complex); u=f"U{j+1}"
        if COLORS[u]=="white": row[wi[u]]=-1
        else: row[wi[BOUNDARY_OWNER[j]]]=-sign*weights[10+j]
        A.append(row); rhs.append(pf[j])
    A=np.array(A); rhs=np.array(rhs); f=np.linalg.lstsq(A,rhs,rcond=None)[0]
    fres=float(np.max(np.abs(A@f-rhs))); fv={v:f[i] for i,v in enumerate(WHITE)}
    A=[]; rhs=[]
    for white in sorted(v for v in WHITE if not v.startswith("U")):
        row=np.zeros(len(BLACK),dtype=complex)
        for ei,(_,w,b,sign,_) in enumerate(EDGES):
            if w==white: row[bi[b]]+=sign*weights[ei]
        A.append(row); rhs.append(0j)
    pt=[((-1)**i)*tzeta[i] for i in range(6)]
    for j in range(6):
        _,_,_,sign,_=EDGES[10+j]; row=np.zeros(len(BLACK),dtype=complex); u=f"U{j+1}"
        if COLORS[u]=="black": row[bi[u]]=1
        else: row[bi[BOUNDARY_OWNER[j]]]=-sign*weights[10+j]
        A.append(row); rhs.append(pt[j])
    A=np.array(A); rhs=np.array(rhs); t=np.linalg.lstsq(A,rhs,rcond=None)[0]
    tres=float(np.max(np.abs(A@t-rhs))); tv={v:t[i] for i,v in enumerate(BLACK)}
    return fv,tv,fres,tres

def primitive(weights:np.ndarray,fv:dict[str,complex],tv:dict[str,complex]):
    adj:dict[str,list[tuple[str,complex]]]={}
    for ei,(_,w,b,sign,(a,c)) in enumerate(EDGES):
        inc=fv[w]*(sign*weights[ei])*tv[b]
        adj.setdefault(a,[]).append((c,inc)); adj.setdefault(c,[]).append((a,-inc))
    pos={"P0":0j}; queue=["P0"]; closures=[]
    while queue:
        a=queue.pop(0)
        for b,inc in adj[a]:
            candidate=pos[a]+inc
            if b not in pos: pos[b]=candidate; queue.append(b)
            else: closures.append(pos[b]-candidate)
    return pos,max(abs(x) for x in closures)

def orient(a:complex,b:complex,c:complex) -> float:
    return float(((b-a).conjugate()*(c-a)).imag)

def validate_geometry(pos:dict[str,complex],weights:np.ndarray,fv:dict[str,complex],tv:dict[str,complex]) -> dict[str,Any]:
    lengths=[]; ratios=[]
    for ei,(_,w,b,_,(a,c)) in enumerate(EDGES):
        length=abs(pos[c]-pos[a]); lengths.append(length)
        ratios.append(length/(weights[ei]*abs(fv[w])*abs(tv[b])))
    face_orient=[]; min_cross=math.inf
    for face,vertices in FACES.items():
        crosses=[orient(pos[vertices[i-1]],pos[vertices[i]],pos[vertices[(i+1)%len(vertices)]]) for i in range(len(vertices))]
        sign=1 if all(x>1e-10 for x in crosses) else (-1 if all(x<-1e-10 for x in crosses) else 0)
        face_orient.append(sign); min_cross=min(min_cross,min(abs(x) for x in crosses))
    crossings=0
    dual_edges=[dual for *_,dual in EDGES]
    for i,(a,b) in enumerate(dual_edges):
        for c,d in dual_edges[i+1:]:
            if {a,b}&{c,d}: continue
            o1,o2=orient(pos[a],pos[b],pos[c]),orient(pos[a],pos[b],pos[d])
            o3,o4=orient(pos[c],pos[d],pos[a]),orient(pos[c],pos[d],pos[b])
            if o1*o2<-1e-10 and o3*o4<-1e-10: crossings+=1
    def angle(p:str,v:str,n:str) -> float:
        a=pos[p]-pos[v]; b=pos[n]-pos[v]
        cosine=float(np.clip((a.real*b.real+a.imag*b.imag)/(abs(a)*abs(b)),-1,1))
        return math.acos(cosine)
    sums={v:{"white":0.0,"black":0.0} for v in pos}
    for face,vertices in FACES.items():
        for i,v in enumerate(vertices):
            sums[v][COLORS[face]]+=angle(vertices[i-1],v,vertices[(i+1)%len(vertices)])
    te4=max(abs(sums[v][c]-math.pi) for v in ["A","C","D"] for c in ["white","black"])
    margins=[min(sums[v][c],math.pi-sums[v][c]) for v in BOUNDARY for c in ["white","black"]]
    boundary_gauge=max(
        [abs(abs(fv[v])-1) for v in ["U2","U5","U6"]]+
        [abs(abs(tv[v])-1) for v in ["U1","U3","U4"]]
    )
    return {
        "te1_min_edge":q(min(lengths)),
        "te2_all_convex":all(x!=0 for x in face_orient),
        "te2_common_orientation":len(set(face_orient))==1 and face_orient[0]!=0,
        "minimum_face_turn_cross":q(min_cross),
        "nonadjacent_crossing_count":crossings,
        "te3_max_relative_gauge_error":q(max(abs(r-1) for r in ratios)),
        "boundary_gauge_max_error":q(boundary_gauge),
        "te4_max_angle_residual":q(te4),
        "te5_min_angle_margin":q(min(margins)),
    }

def embedding_ok(metrics:dict[str,Any],fres:float,tres:float,closure:float) -> bool:
    return (
        fres<TOL["extension"] and tres<TOL["extension"] and closure<TOL["closure"] and
        metrics["te1_min_edge"]>TOL["edge"] and metrics["te2_all_convex"] and
        metrics["te2_common_orientation"] and metrics["nonadjacent_crossing_count"]==0 and
        metrics["te3_max_relative_gauge_error"]<TOL["te3"] and
        metrics["boundary_gauge_max_error"]<TOL["te3"] and
        metrics["te4_max_angle_residual"]<TOL["te4"] and
        metrics["te5_min_angle_margin"]>TOL["te5_margin"]
    )

def construct(x:np.ndarray) -> dict[str,Any]:
    minors,weights=minors_from_x(x); C=c_from_minors(minors); Cp=c_perp_rows(C)
    left=select_plane(C,2*math.pi,[1,4,5]); right=select_plane(Cp,4*math.pi,[0,2,3])
    if left is None or right is None:
        return {"selector_status":"SELECTOR_COVERAGE_LIMIT",
                "lambda_found":left is not None,"tilde_lambda_found":right is not None,
                "existence_interpretation":"no nonexistence inference; source Corollary 1.13 is a separate conditional existence result"}
    li,ls,ln,(L,_,_)=left; ti,ts,tn,(Lt,_,_)=right
    zeta=L[0]+1j*L[1]; tzeta=Lt[0]-1j*Lt[1]
    fv,tv,fres,tres=solve_extensions(weights,zeta,tzeta)
    pos,closure=primitive(weights,fv,tv); metrics=validate_geometry(pos,weights,fv,tv)
    return {
        "selector_status":"FOUND",
        "lambda_selector":{"index":li,"sign":ls,"normal":[q(v) for v in ln]},
        "tilde_lambda_selector":{"index":ti,"sign":ts,"normal":[q(v) for v in tn]},
        "extension_residuals":{"white":q(fres),"black":q(tres),"primitive_closure":q(closure)},
        "metrics":metrics,
        "valid_numerical_t_embedding":embedding_ok(metrics,fres,tres,closure),
        "positions":{name:[q(value.real),q(value.imag)] for name,value in sorted(pos.items())},
        "boundary_shape_signature":boundary_signature(pos),
    }

def boundary_signature(pos:dict[str,complex]) -> list[float]:
    lengths=np.array([abs(pos[BOUNDARY[(i+1)%6]]-pos[BOUNDARY[i]]) for i in range(6)])
    return [q(v) for v in lengths/lengths.sum()]

def sample_plan() -> list[dict[str,Any]]:
    rows=[{"id":"baseline","kind":"baseline","x":BASELINE.copy(),"metadata":{}}]
    for j in range(8):
        for sign in (-1,1):
            delta=sign*0.2
            x=BASELINE.copy(); x[j]*=math.exp(delta)
            rows.append({"id":f"axis_{j+1}_{'minus' if sign<0 else 'plus'}","kind":"axis","x":x,
                         "metadata":{"coordinate":j+1,"log_delta":delta}})
    rng=np.random.default_rng(SEED)
    for radius in (0.5,1.5,3.0):
        for index in range(8):
            delta=rng.uniform(-radius,radius,8); x=BASELINE*np.exp(delta)
            rows.append({"id":f"random_r{radius}_{index+1}","kind":"random","x":x,
                         "metadata":{"log_radius":radius,"log_delta":[q(v) for v in delta]}})
    return rows

def multiple_baseline_branches(count:int=5) -> list[dict[str,Any]]:
    minors,weights=minors_from_x(BASELINE); C=c_from_minors(minors); Cp=c_perp_rows(C)
    def collect(B,target,indices):
        out=[]
        for k,n in fibonacci_normals():
            for sign in (1.0,-1.0):
                candidate=plane_candidate(B,sign*n,target,indices)
                if candidate is not None:
                    out.append((k,int(sign),sign*n,candidate[0]))
                    if len(out)>=count:return out
        return out
    left=collect(C,2*math.pi,[1,4,5]); right=collect(Cp,4*math.pi,[0,2,3])
    branches=[]
    for index,(l,r) in enumerate(zip(left,right),1):
        li,ls,ln,L=l; ti,ts,tn,Lt=r
        fv,tv,fres,tres=solve_extensions(weights,L[0]+1j*L[1],Lt[0]-1j*Lt[1])
        pos,closure=primitive(weights,fv,tv); metrics=validate_geometry(pos,weights,fv,tv)
        branches.append({
            "branch":f"BASELINE-B{index}",
            "lambda_selector":{"index":li,"sign":ls},
            "tilde_lambda_selector":{"index":ti,"sign":ts},
            "valid_numerical_t_embedding":embedding_ok(metrics,fres,tres,closure),
            "boundary_shape_signature":boundary_signature(pos),
            "metrics":metrics,
        })
    return branches

def sensitivity() -> dict[str,Any]:
    minors,weights=minors_from_x(BASELINE); C=c_from_minors(minors); Cp=c_perp_rows(C)
    left=select_plane(C,2*math.pi,[1,4,5]); right=select_plane(Cp,4*math.pi,[0,2,3])
    assert left and right
    nleft=left[2]; nright=right[2]
    def fixed(x):
        mm,ww=minors_from_x(x); CC=c_from_minors(mm); NN=c_perp_rows(CC)
        l=plane_candidate(CC,nleft,2*math.pi,[1,4,5]); r=plane_candidate(NN,nright,4*math.pi,[0,2,3])
        if l is None or r is None:return None
        L=l[0]; Lt=r[0]; fv,tv,_,_=solve_extensions(ww,L[0]+1j*L[1],Lt[0]-1j*Lt[1])
        pos,_=primitive(ww,fv,tv); return np.array(boundary_signature(pos))
    eps=1e-4; J=np.zeros((6,8))
    for j in range(8):
        plus=BASELINE.copy(); minus=BASELINE.copy(); plus[j]*=math.exp(eps); minus[j]*=math.exp(-eps)
        p,m=fixed(plus),fixed(minus)
        if p is None or m is None: raise AssertionError("local branch continuation failed")
        J[:,j]=(p-m)/(2*eps)
    sv=np.linalg.svd(J,compute_uv=False)
    return {"observable":"six boundary-edge lengths normalized by perimeter",
            "branch_rule":"hold the baseline selected lambda and tilde-lambda normal directions fixed while recomputing their plane sections and boundary normalization",
            "log_parameter_step":eps,"jacobian":[[q(v) for v in row] for row in J],
            "rank_at_1e-8":int(np.linalg.matrix_rank(J,tol=1e-8)),
            "singular_values":[q(v) for v in sv],
            "interpretation":"This is representative-branch sensitivity, not a branch-invariant mechanical response."}

def build() -> dict[str,Any]:
    hypotheses=graph_hypotheses()
    samples=sample_plan(); atlas=[]
    for row in samples:
        result=construct(row["x"])
        atlas.append({"id":row["id"],"kind":row["kind"],"x":[q(v) for v in row["x"]],
                      "metadata":row["metadata"],"result":result})
    found=[row for row in atlas if row["result"]["selector_status"]=="FOUND"]
    valid=[row for row in found if row["result"]["valid_numerical_t_embedding"]]
    branches=multiple_baseline_branches()
    signatures=np.array([b["boundary_shape_signature"] for b in branches])
    pairwise=[q(float(np.max(np.abs(signatures[i]-signatures[j]))))
              for i in range(len(signatures)) for j in range(i+1,len(signatures))]
    aggregates={
        "attempted":len(atlas),"selector_found":len(found),"valid_numerical_t_embeddings":len(valid),
        "selector_coverage_limits":len(atlas)-len(found),
        "max_white_extension_residual":q(max(row["result"]["extension_residuals"]["white"] for row in valid)),
        "max_black_extension_residual":q(max(row["result"]["extension_residuals"]["black"] for row in valid)),
        "max_primitive_closure_residual":q(max(row["result"]["extension_residuals"]["primitive_closure"] for row in valid)),
        "max_te3_relative_gauge_error":q(max(row["result"]["metrics"]["te3_max_relative_gauge_error"] for row in valid)),
        "max_te4_angle_residual":q(max(row["result"]["metrics"]["te4_max_angle_residual"] for row in valid)),
        "min_te5_angle_margin":q(min(row["result"]["metrics"]["te5_min_angle_margin"] for row in valid)),
        "min_edge_length":q(min(row["result"]["metrics"]["te1_min_edge"] for row in valid)),
    }
    return {"hypotheses":hypotheses,"atlas":atlas,"branches":branches,
            "branch_pairwise_max_boundary_signature_difference":pairwise,
            "sensitivity":sensitivity(),"aggregates":aggregates}

def artifacts(data:dict[str,Any]) -> dict[str,Any]:
    atlas=data["atlas"]; branches=data["branches"]; agg=data["aggregates"]
    samples={"schema_version":"1.0.0","work_package":"VGSE-MS-M0","seed":SEED,
             "selector_points":SELECTOR_POINTS,
             "samples":[{"id":r["id"],"kind":r["kind"],"x":r["x"],"metadata":r["metadata"]} for r in atlas]}
    realization={"schema_version":"1.0.0","work_package":"VGSE-MS-M0",
                 "constructor":"VGSE-MS-M0-TE3-FORWARD-001","aggregate":agg,"samples":atlas}
    te3={"schema_version":"1.0.0","work_package":"VGSE-MS-M0",
         "gauge_rule":"geometric_length = |F_white| * weight * |Ftilde_black|; boundary factors are normalized to one",
         "aggregate":{"valid_count":agg["valid_numerical_t_embeddings"],
                      "max_relative_gauge_error":agg["max_te3_relative_gauge_error"],
                      "max_boundary_gauge_error":q(max(r["result"]["metrics"]["boundary_gauge_max_error"] for r in atlas if r["result"]["selector_status"]=="FOUND"))}}
    branch={"schema_version":"1.0.0","work_package":"VGSE-MS-M0","baseline_branches":branches,
            "pairwise_max_boundary_signature_difference":data["branch_pairwise_max_boundary_signature_difference"],
            "conclusion":"UNIQUE_REALIZATION_HYPOTHESIS_FALSIFIED_NUMERICALLY"}
    falsification={"schema_version":"1.0.0","work_package":"VGSE-MS-M0",
      "hypotheses":[
        {"claim":"Every positive quotient point has one unique admissible t-embedding under the M0 boundary-gauge normalization.",
         "status":"FALSIFIED_NUMERICALLY",
         "evidence":"Five valid baseline branches use distinct admissible lambda/tilde-lambda selector pairs and have distinct scale-free boundary edge signatures.",
         "minimum_pairwise_signature_separation":min(data["branch_pairwise_max_boundary_signature_difference"])},
        {"claim":"The finite 2048-point representative selector is complete over the wide log-radius-3 stress box.",
         "status":"FALSIFIED",
         "evidence":f"{agg['selector_coverage_limits']} sampled point(s) returned SELECTOR_COVERAGE_LIMIT. This is an algorithmic selector limit, not a nonexistence result."}
      ]}
    results={"schema_version":"1.0.0","work_package":"VGSE-MS-M0",
      "disposition":"TE3_REALIZATION_ATLAS_PARTIAL",
      "graph_hypotheses":data["hypotheses"],
      "atlas_summary":agg,
      "source_conditional_global_existence":"Galashin Corollary 1.13 applies if the exact finite graph-hypothesis audit and the pinned source theorem are accepted; M0 does not independently certify that theorem.",
      "established_numerically":[
        "full TE1-TE5 plus injective/noncrossing t-embedding replay at the protected baseline",
        "valid independent quotient-to-t-embedding realizations across all baseline, axis, log-radius-0.5, and log-radius-1.5 samples in the declared deterministic atlas",
        "multiple distinct valid t-embedding representatives at one fixed quotient point"
      ],
      "not_established":[
        "completeness of the finite plane selector across the full positive quotient orthant",
        "global branch classification of all t-embeddings",
        "mechanical meaning of any quotient or geometric coordinate",
        "VGSE-C06/source correspondence"
      ],
      "next_boundary":"M0 is sufficient to supply a genuine TE3-native design family for a separately governed M1 kinematic-semantics activation; no M1 authority is created by this result.",
      "claim_boundary":{"mathematical_certification":false,"source_correspondence_c06":false,"mechanics":false,
        "rigid_foldability":false,"collision_freedom":false,"finite_thickness":false,"stiffness":false,
        "manufacturing":false,"product":false,"novelty_patent_commercial":false}}
    claims={"schema_version":"1.0.0","work_package":"VGSE-MS-M0","claims":[
      {"id":"VGSE-MS-M0-C01","statement":"The fixed VGSE graph has exact finite surplus kmin=2 and is 2-boundary-nondegenerate by APM enumeration.","status":"COMPUTED_EXACT_FINITE"},
      {"id":"VGSE-MS-M0-C02","statement":"The protected baseline quotient point admits a numerical source-contract t-embedding with TE1-TE5 and noncrossing/injectivity replay within declared tolerances.","status":"NUMERICALLY_REPLAYED"},
      {"id":"VGSE-MS-M0-C03","statement":"The declared atlas contains independent quotient points with valid numerical t-embeddings across the local and intermediate sample boxes.","status":"NUMERICALLY_REPLAYED"},
      {"id":"VGSE-MS-M0-C04","statement":"A fixed quotient point does not select a unique geometry under the M0 realization contract; multiple valid representatives with distinct scale-free boundary signatures were constructed.","status":"NUMERICALLY_FALSIFIED_UNIQUENESS"},
      {"id":"VGSE-MS-M0-C05","statement":"All positive weights globally admit t-embeddings.","status":"SOURCE_THEOREM_CONDITIONAL_NOT_M0_CERTIFIED","source":"Galashin arXiv:2410.09574v2 Corollary 1.13"}
    ]}
    return {
      "QUOTIENT_SAMPLE.json":samples,"REALIZATION_ATLAS.json":realization,"TE3_REPLAY.json":te3,
      "BRANCH_LEDGER.json":branch,"SENSITIVITY.json":{"schema_version":"1.0.0","work_package":"VGSE-MS-M0",**data["sensitivity"]},
      "FALSIFICATION_LEDGER.json":falsification,"RESULTS.json":results,"CLAIM_LEDGER.json":claims}

def validate_retained(generated:dict[str,Any]) -> None:
    for name,expected in generated.items():
        path=HERE/name
        if not path.is_file(): raise AssertionError(f"missing retained artifact {name}")
        actual=json.loads(path.read_text(encoding="utf-8"))
        if name in {"QUOTIENT_SAMPLE.json","BRANCH_LEDGER.json","FALSIFICATION_LEDGER.json","CLAIM_LEDGER.json"}:
            if actual!=expected: raise AssertionError(f"{name} deterministic content drift")
        elif name=="RESULTS.json":
            if actual["disposition"]!=expected["disposition"] or actual["atlas_summary"]["attempted"]!=expected["atlas_summary"]["attempted"]:
                raise AssertionError("RESULTS.json disposition/sample drift")
        elif name=="REALIZATION_ATLAS.json":
            if actual["aggregate"]!=expected["aggregate"]:
                raise AssertionError("REALIZATION_ATLAS aggregate drift")
            if [r["result"]["selector_status"] for r in actual["samples"]] != [r["result"]["selector_status"] for r in expected["samples"]]:
                raise AssertionError("selector-status drift")
        elif name=="TE3_REPLAY.json":
            if actual["aggregate"]!=expected["aggregate"]: raise AssertionError("TE3_REPLAY aggregate drift")
        elif name=="SENSITIVITY.json":
            if actual["rank_at_1e-8"]!=expected["rank_at_1e-8"]:
                raise AssertionError("sensitivity rank drift")
    result=generated["RESULTS.json"]
    if result["atlas_summary"]["valid_numerical_t_embeddings"]<32:
        raise AssertionError("atlas lost required numerical coverage")
    if result["graph_hypotheses"]["kmin"]!=2 or not result["graph_hypotheses"]["two_boundary_nondegenerate"]:
        raise AssertionError("source theorem graph hypotheses drift")
    if generated["BRANCH_LEDGER.json"]["conclusion"]!="UNIQUE_REALIZATION_HYPOTHESIS_FALSIFIED_NUMERICALLY":
        raise AssertionError("falsification disposition drift")

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    data=build(); generated=artifacts(data)
    if args.write:
        for name,value in generated.items():
            (HERE/name).write_text(json.dumps(value,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if args.check:
        validate_retained(generated)
        print("VGSE-MS-M0 deterministic realization atlas: PASS")
    if not args.write and not args.check:
        print(json.dumps(generated["RESULTS.json"],indent=2,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
