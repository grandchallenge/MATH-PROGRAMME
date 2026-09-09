from __future__ import annotations
import json, math, sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
G_DIR = HERE.parent / "OZ_RT_BZ_T3_010"
sys.path.insert(0, str(G_DIR)); sys.path.insert(0, str(HERE))
import producer
import verify_t3_011_g as vg
a = vg.a

def _locks():
    out={"K":{},"G":{}}
    for name,want in producer.K_BLOBS.items():
        got=a.git_blob_sha1(producer.K_DIR/name)
        if got!=want: raise AssertionError(f"independent K source lock drift: {name}")
        out["K"][name]=got
    kc=json.loads((producer.K_DIR/"CONTRACT.json").read_text())
    if kc.get("terminals",{}).get("closure")!=producer.K_REQUIRED_TERMINAL: raise AssertionError("independent K contract drift")
    for name,want in producer.G_BLOBS.items():
        got=a.git_blob_sha1(producer.G_DIR/name)
        if got!=want: raise AssertionError(f"independent G source lock drift: {name}")
        out["G"][name]=got
    return out

def _d(sig): return {f:int(e) for f,e in sig if e}
def _pos(sig):
    d=_d(sig)
    if not d or any(e<=0 for e in d.values()): raise AssertionError("non-positive coordinate factor")
    return d
def _lcm(x,y): return abs(x*y)//math.gcd(x,y) if x and y else abs(x or y)
def _primitive(a0,b0):
    m=_lcm(a0.denominator,b0.denominator); v=[int(a0*m),int(b0*m),m]
    d=math.gcd(math.gcd(abs(v[0]),abs(v[1])),abs(v[2])); return [x//d for x in v]

def _ray(ls,rs,es):
    L,R,E=_pos(ls),_pos(rs),_pos(es); fs=sorted(set(L)|set(R)|set(E),key=repr); candidates=[]
    for i,x in enumerate(fs):
        for y in fs[i+1:]:
            det=L.get(x,0)*R.get(y,0)-L.get(y,0)*R.get(x,0)
            if not det: continue
            aa=Q(E.get(x,0)*R.get(y,0)-E.get(y,0)*R.get(x,0),det)
            bb=Q(L.get(x,0)*E.get(y,0)-L.get(y,0)*E.get(x,0),det)
            if aa>=0 and bb>=0 and all(aa*L.get(z,0)+bb*R.get(z,0)==E.get(z,0) for z in fs): candidates.append(_primitive(aa,bb))
            break
    for src,side in ((R,1),(L,0)):
        p=next(iter(src)); q=Q(E.get(p,0),src[p])
        if q>=0 and all(q*src.get(z,0)==E.get(z,0) for z in fs):
            candidates.append(_primitive(Q(0),q) if side else _primitive(q,Q(0)))
    return min(candidates) if candidates else None

def _spectator(pair):
    rem=sorted({"n","k","l"}-{producer.CHANNEL_COORDINATE[pair[0]],producer.CHANNEL_COORDINATE[pair[1]]})
    if len(rem)!=1: raise AssertionError("independent spectator ambiguity")
    return rem[0],producer.CANONICAL_SPECTATOR_CHANNEL[rem[0]]

def _first(factors):
    for pi,pair in enumerate(producer.ADMITTED_PAIRS):
        axis,sch=_spectator(pair)
        for ci,(comp,lk,rk) in enumerate(producer.COMPONENTS):
            for sid in sorted(set(factors[pair[0]])&set(factors[pair[1]])&set(factors[sch])):
                ls,_=factors[pair[0]][sid][lk]; rs,_=factors[pair[1]][sid][rk]; es,ec=factors[sch][sid]["x0"]
                if Q(ec)==0: return {"kind":"RECIPROCAL_SPECTATOR_SPECIALIZES_TO_ZERO","pair_index":pi,"pair":list(pair),"component_index":ci,"component":comp,"stratum":sid,"spectator_axis":axis,"spectator_channel_representative":sch}
                try: ray=_ray(ls,rs,es)
                except AssertionError as exc:
                    return {"kind":"RECIPROCAL_SPECTATOR_FACTOR_GEOMETRY_INVALID","pair_index":pi,"pair":list(pair),"component_index":ci,"component":comp,"stratum":sid,"spectator_axis":axis,"spectator_channel_representative":sch,"detail":str(exc)}
                if ray: return {"kind":"UNBOUNDED_RECIPROCAL_SPECTATOR_CANCELLATION_RAY","pair_index":pi,"pair":list(pair),"component_index":ci,"component":comp,"stratum":sid,"spectator_axis":axis,"spectator_channel_representative":sch,"left_factor_kind":lk,"right_factor_kind":rk,"reciprocal_spectator_factor_kind":"x0","primitive_integer_ray":ray,"homogeneous_relation":"dr*L + ds*R - dt*E = 0"}
    return None

def _check_relation(blocker,factors):
    pair=tuple(blocker["pair"]); sid=blocker["stratum"]; _,sch=_spectator(pair)
    ls,_=factors[pair[0]][sid][blocker["left_factor_kind"]]
    rs,_=factors[pair[1]][sid][blocker["right_factor_kind"]]
    es,_=factors[sch][sid]["x0"]; L,R,E=_pos(ls),_pos(rs),_pos(es)
    dr,ds,dt=blocker["primitive_integer_ray"]
    if min(dr,ds,dt)<0 or dt<=0 or dr+ds==0: raise AssertionError("invalid ray")
    for z in set(L)|set(R)|set(E):
        if dr*L.get(z,0)+ds*R.get(z,0)!=dt*E.get(z,0): raise AssertionError("ray relation fails")

def verify(result):
    if result.get("issue")!=producer.ISSUE or result.get("stage")!=producer.STAGE: raise AssertionError("L identity drift")
    producer.validate_scope()
    locks=_locks()
    if result.get("predecessor_checkpoint",{}).get("source_blobs")!=locks: raise AssertionError("L lock ledger drift")
    strata,_,_=vg.vf.vd.reconstruct_context()
    factors={ch:vg._factor_map(ch,strata) for ch in producer.CHANNEL_COORDINATE}
    blocker=_first(factors)
    if blocker is None: raise AssertionError("protected L geometry unexpectedly has no blocker")
    if result.get("characterized_blocker")!=blocker: raise AssertionError("L blocker drift")
    if blocker["kind"]=="UNBOUNDED_RECIPROCAL_SPECTATOR_CANCELLATION_RAY": _check_relation(blocker,factors)
    if result.get("terminal")!=producer.BLOCKER_TERMINAL: raise AssertionError("L must stop at blocker")
    if result.get("tested_record_count")!=0 or result.get("tested_records")!=[]: raise AssertionError("L must not truncate the unbounded class")
    if result.get("residual_sum_zero_proved") is not False or result.get("proof_effect")!="NONE" or result.get("promotion_effect")!="NONE" or result.get("t3_status")!="OPEN_WITH_CHARACTERIZED_BLOCKER": raise AssertionError("L claim firewall drift")
    return {"operation":producer.OPERATION,"status":"INDEPENDENT_T3_011_L_BLOCKER_REPLAY_COMPLETE","characterized_blocker":blocker,"tested_record_count":0,"terminal":producer.BLOCKER_TERMINAL}
