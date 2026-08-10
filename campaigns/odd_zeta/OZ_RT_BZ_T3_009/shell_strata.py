#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction as Q

import one_body_coefficient_layer as cl
import residual_canonical as rc

Layer = dict[tuple[str, ...], dict[str, rc.Rat]]
Factor = tuple[int, int, int, int]

SCALAR_SWAP = {
    "TN1":"TN1", "TN2":"TN2", "TN3":"TN3",
    "SK":"SL", "SL":"SK", "AK":"AL", "AL":"AK",
    "LKK":"LLL", "LLL":"LKK", "LKL":"LLK", "LLK":"LKL",
}

ATOM_WEIGHT = {
    "A_k_1":1,"A_l_1":1,"B_k_1":1,"B_l_1":1,"C_1":1,"H_k_1":1,"H_l_1":1,"H_kl_1":1,
    "A_k_2":2,"A_l_2":2,"C_2":2,"H_k_2":2,"H_l_2":2,"H_kl_2":2,
    "H_k_3":3,"H_l_3":3,"H_nk_3":3,"H_nl_3":3,
    "H_k_4":4,"H_l_4":4,"H_nk_4":4,"H_nl_4":4,
}
WEIGHT_ORBIT_BLOCK_SIZES = {"weight1":5,"weight2":4,"weight3":2,"weight4":2}


def atom_swap(name: str) -> str:
    pairs = {
        "A_k_1":"A_l_1","A_l_1":"A_k_1","A_k_2":"A_l_2","A_l_2":"A_k_2",
        "B_k_1":"B_l_1","B_l_1":"B_k_1",
        "H_k_1":"H_l_1","H_l_1":"H_k_1","H_k_2":"H_l_2","H_l_2":"H_k_2",
        "H_k_3":"H_l_3","H_l_3":"H_k_3","H_k_4":"H_l_4","H_l_4":"H_k_4",
        "H_nk_3":"H_nl_3","H_nl_3":"H_nk_3","H_nk_4":"H_nl_4","H_nl_4":"H_nk_4",
    }
    return pairs.get(name,name)


def canonical_sig(exponents: dict[Factor,int]):
    return tuple(sorted((f,e) for f,e in exponents.items() if e))


def substitute_factor(f: Factor, k_offset: int|None, l_offset: int|None) -> Factor:
    a,b,c,d=f
    if k_offset is not None:
        a,d,b = a+b,d+b*k_offset,0
    if l_offset is not None:
        a,d,c = a+c,d+c*l_offset,0
    return (a,b,c,d)


def protected_axis(factor) -> tuple[str,Factor] | None:
    if len(factor)!=5 or factor[0]!=cl.PINV_TAG:
        return None
    f=tuple(factor[1:])
    if f[0:3]==(1,-1,0): return "k",f
    if f[0:3]==(1,0,-1): return "l",f
    raise AssertionError(f"unexpected protected factor {factor}")


def transform_rat(rat: rc.Rat, k_offset: int|None, l_offset: int|None) -> rc.Rat:
    out: defaultdict[tuple,Q]=defaultdict(Q)
    for sig,coeff0 in rat.items():
        coeff=coeff0
        exps: dict[Factor,int]={}
        killed=False
        for factor,exponent in sig:
            protected=protected_axis(factor)
            if protected is not None:
                axis,f=protected
                off=k_offset if axis=="k" else l_offset
                if off is not None:
                    if exponent>=0:
                        raise AssertionError("protected positive reciprocal acquired nonnegative exponent")
                    z=f[3]-off
                    if z<=0:
                        killed=True
                        break
                    coeff*=Q(z)**exponent
                    continue
                # On a core coordinate n-axis+s is strictly positive, so pinv is ordinary reciprocal.
                tf=substitute_factor(f,k_offset,l_offset)
            else:
                if len(factor)!=4:
                    raise AssertionError(f"unexpected ordinary factor {factor}")
                tf=substitute_factor(tuple(factor),k_offset,l_offset)
            if tf[:3]==(0,0,0):
                z=tf[3]
                if z==0 and exponent<0:
                    raise AssertionError(f"ordinary pole survived stratum substitution: {factor}")
                coeff*=Q(z)**exponent
            else:
                exps[tf]=exps.get(tf,0)+exponent
                if exps[tf]==0: del exps[tf]
        if not killed and coeff:
            out[canonical_sig(exps)]+=coeff
    return {sig:c for sig,c in out.items() if c}


def transform_layer(layer:Layer,k_offset:int|None,l_offset:int|None)->Layer:
    out:Layer={}
    for mon,terms in layer.items():
        t={}
        for scalar,rat in terms.items():
            rr=transform_rat(rat,k_offset,l_offset)
            if rr: t[scalar]=rr
        if t: out[mon]=t
    return out


def swap_rat(rat:rc.Rat)->rc.Rat:
    out={}
    for sig,c in rat.items():
        exps={}
        for (a,b,cc,d),e in sig:
            f=(a,cc,b,d)
            exps[f]=exps.get(f,0)+e
        out[canonical_sig(exps)]=c
    return out


def swap_layer(layer:Layer)->Layer:
    out:Layer={}
    for mon,terms in layer.items():
        smon=tuple(sorted(atom_swap(a) for a in mon))
        target=out.setdefault(smon,{})
        for scalar,rat in terms.items():
            ss=SCALAR_SWAP[scalar]
            if ss in target:
                target[ss]=rc.r_add(target[ss],swap_rat(rat))
            else:
                target[ss]=swap_rat(rat)
    return {m:{s:r for s,r in t.items() if r} for m,t in out.items() if any(t.values())}


def layer_rows(layer:Layer):
    rows=[]
    for mon in sorted(layer):
        terms=[]
        for scalar in cl.SCALAR_ORDER:
            rat=layer[mon].get(scalar)
            if rat: terms.append([scalar,rc.rat_json(rat)])
        rows.append([list(mon),terms])
    return rows


def digest(layer:Layer)->str:
    return hashlib.sha256(json.dumps(layer_rows(layer),separators=(",",":"),sort_keys=False).encode()).hexdigest()


def profile(layer:Layer)->dict:
    factors=set(); scalar_terms=0
    hist:defaultdict[int,int]=defaultdict(int)
    for mon,terms in layer.items():
        scalar_terms+=len(terms)
        hist[sum(ATOM_WEIGHT[a] for a in mon)]+=1
        for rat in terms.values():
            for sig in rat:
                for factor,_ in sig:
                    if len(factor)!=4: raise AssertionError("protected factor survived rational stratum")
                    factors.add(factor)
    atoms=sorted({a for mon in layer for a in mon})
    return {
        "monomials":len(layer),"scalar_terms":scalar_terms,"atoms":len(atoms),
        "max_atomic_arity":max((len(m) for m in layer),default=0),
        "ordinary_factor_count":len(factors),"protected_factor_count":0,
        "harmonic_weight_histogram":{str(k):hist[k] for k in sorted(hist)},
        "sha256":digest(layer),
    }


def eval_rat(rat:rc.Rat,n:int,k:int,l:int)->Q:
    return rc.r_eval(rat,n,k,l)


def verify_pointwise(original:Layer,strata:dict)->dict:
    checks=0
    # Core.
    core=strata["core"]
    for n in range(1,5):
        for k in range(n):
            for l in range(n):
                for mon,terms in original.items():
                    for scalar,rat in terms.items():
                        if cl.rat_eval_polefree(rat,n,k,l)!=eval_rat(core[mon][scalar],n,k,l):
                            raise AssertionError(f"core coefficient drift {(n,k,l,mon,scalar)}")
                        checks+=1
    # One-sided strips.
    for d in range(4):
        ks=strata[f"k{d}"]; ls=strata[f"l{d}"]
        for n in range(1,5):
            for q in range(n):
                k=n+d; l=q
                for mon,terms in original.items():
                    for scalar,rat in terms.items():
                        want=cl.rat_eval_polefree(rat,n,k,l)
                        got=eval_rat(ks.get(mon,{}).get(scalar,{}),n,k,l)
                        if want!=got: raise AssertionError(f"k-shell coefficient drift {(d,n,q,mon,scalar)}")
                        checks+=1
                k=q; l=n+d
                for mon,terms in original.items():
                    for scalar,rat in terms.items():
                        want=cl.rat_eval_polefree(rat,n,k,l)
                        got=eval_rat(ls.get(mon,{}).get(scalar,{}),n,k,l)
                        if want!=got: raise AssertionError(f"l-shell coefficient drift {(d,n,q,mon,scalar)}")
                        checks+=1
    # Intersections.
    for d in range(4):
        for e in range(4):
            ss=strata[f"x{d}{e}"]
            for n in range(5):
                k=n+d; l=n+e
                for mon,terms in original.items():
                    for scalar,rat in terms.items():
                        want=cl.rat_eval_polefree(rat,n,k,l)
                        got=eval_rat(ss.get(mon,{}).get(scalar,{}),n,k,l)
                        if want!=got: raise AssertionError(f"intersection coefficient drift {(d,e,n,mon,scalar)}")
                        checks+=1
    return {"exact_coefficient_checks":checks,"finite_sampling_used_as_global_proof":False}


def build()->dict:
    original,_=cl.build_layer()
    strata={"core":transform_layer(original,None,None)}
    for d in range(4):
        strata[f"k{d}"]=transform_layer(original,d,None)
        strata[f"l{d}"]=transform_layer(original,None,d)
    for d in range(4):
        for e in range(4):
            strata[f"x{d}{e}"]=transform_layer(original,d,e)

    if swap_layer(strata["core"])!=strata["core"]:
        raise AssertionError("core k-l symmetry drift")
    for d in range(4):
        if swap_layer(strata[f"k{d}"])!=strata[f"l{d}"]:
            raise AssertionError(f"one-sided shell mirror drift {d}")
    for d in range(4):
        for e in range(4):
            if swap_layer(strata[f"x{d}{e}"])!=strata[f"x{e}{d}"]:
                raise AssertionError(f"intersection mirror drift {(d,e)}")

    replay=verify_pointwise(original,strata)
    representatives=["core"]+[f"k{d}" for d in range(4)]+[f"x{d}{e}" for d in range(4) for e in range(d,4)]
    if len(representatives)!=15: raise AssertionError("symmetry-reduced stratum count drift")
    profiles={name:profile(strata[name]) for name in representatives}
    return {
        "schema_version":"1.0.0",
        "operation":"OZ-RT-BZ-T3-009",
        "execution_boundary":"SYMMETRY_REDUCED_CHANNEL_HARMONIC_BLOCK_WITH_SHELL_STRATA_001",
        "stage":"EXACT_POLE_FREE_INTERIOR_SHELL_STRATIFICATION",
        "source_coefficient_layer_sha256":"90d067ae59790fab8648d006635c14950359b66eb8b57361e61d5b47b2b3af40",
        "common_box":"0<=k,l<=n+3",
        "partition":{
            "core":"0<=k,l<=n-1",
            "k_shells":[f"k=n+{d}, 0<=l<=n-1" for d in range(4)],
            "l_shells":[f"l=n+{d}, 0<=k<=n-1" for d in range(4)],
            "intersections":[f"k=n+{d}, l=n+{e}" for d in range(4) for e in range(4)],
            "disjoint_and_complete":True,
        },
        "symmetry":{
            "full_strata":25,
            "reduced_representatives":15,
            "representatives":representatives,
            "core_invariant":True,
            "k_shell_l_shell_mirror":True,
            "intersection_swap_mirror":True,
        },
        "rationalization":"Every protected positive reciprocal is either replaced by its ordinary reciprocal on a core coordinate or evaluated to an exact positive rational/zero on a fixed shell offset. No protected factor remains in any stratum.",
        "weight_orbit_block_sizes":WEIGHT_ORBIT_BLOCK_SIZES,
        "profiles":profiles,
        "implementation_replay":replay,
        "next_stage":"BOUNDED_CHANNEL_BLOCK_CORRECTION_FLUX_VIABILITY_001",
        "anti_oversplitting":"Correction systems may be split by channel/block/stratum, but all pieces must be recombined before any final n-recurrence search.",
        "residual_sum_zero_proved":False,"proof_effect":"NONE","promotion_effect":"NONE",
        "t3_status":"OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main()->int:
    print(json.dumps(build(),sort_keys=True,separators=(",",":")))
    return 0

if __name__=="__main__": raise SystemExit(main())
