from __future__ import annotations
import importlib.util, json, math, sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
K_DIR = HERE.parent / "OZ_RT_BZ_T3_011_K"
G_DIR = HERE.parent / "OZ_RT_BZ_T3_010"
sys.path.insert(0, str(G_DIR))

def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load predecessor: {path}")
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    spec.loader.exec_module(mod); return mod

k = _load(K_DIR / "producer.py", "oz_t3_011_k_for_l")
g, f, a = k.g, k.f, k.a

OPERATION = "OZ-RT-BZ-T3-011-L"
STAGE = "T3_011_L_RECIPROCAL_SPECTATOR_LAURENT_COKERNEL_AUDIT"
ISSUE = 920
K_REVIEWED_HEAD = "af1044c7f8e543e36c7b899ba17d4dd1a1bba546"
K_MERGE_COMMIT = "5a6557656fe2ac0963f3660787773e9d566a3c1b"
K_REQUIRED_TERMINAL = "TRIVARIATE_SPECTATOR_POLYNOMIAL_RESPONSE_CLASS_COKERNEL_INVISIBLE"
K_BLOBS = {
    "producer.py": "4a0d571a2157ffae385ec1979b85b5b94b5b2190",
    "CONTRACT.json": "6a75ca2ba209a1eaf0af4c5d6a04becd9fcac76a",
    "verifier.py": "9541e65858037ec616b958a426d130deaf79eae5",
}
G_BLOBS, G_REQUIRED_TERMINAL = dict(k.G_BLOBS), k.G_REQUIRED_TERMINAL
ADMITTED_PAIRS = tuple(k.ADMITTED_PAIRS)
CHANNEL_COORDINATE = dict(k.CHANNEL_COORDINATE)
CANONICAL_SPECTATOR_CHANNEL = dict(k.CANONICAL_SPECTATOR_CHANNEL)
COMPONENTS = (("ScSd","x1","x1"),("Sc","x1","x0"),("Sd","x0","x1"),("I","x0","x0"))
BLOCKER_TERMINAL = "RECIPROCAL_SPECTATOR_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"

def validate_scope(reciprocal_spectator=True, reciprocal_left=False, reciprocal_right=False,
                   multiple_reciprocal_axes=False, shifted_spectator=False, shifted_poles=False,
                   arbitrary_rational_functions=False, support_or_harmonic_enlargement=False,
                   candidate_bank_or_scalar_namespace_widening=False, recurrence_widening=False,
                   correction_recombination=False, candidate_linear_combinations=False,
                   third_finite_difference_operator=False, arbitrary_degree_cutoff=None):
    if not reciprocal_spectator: raise AssertionError("L changes exactly the spectator exponent sign")
    if reciprocal_left or reciprocal_right or multiple_reciprocal_axes: raise AssertionError("only spectator may be reciprocal")
    if shifted_spectator or shifted_poles: raise AssertionError("spectator stays unshifted; shifted poles forbidden")
    if arbitrary_rational_functions: raise AssertionError("arbitrary rational functions forbidden")
    if support_or_harmonic_enlargement or candidate_bank_or_scalar_namespace_widening: raise AssertionError("basis widening forbidden")
    if recurrence_widening or correction_recombination or candidate_linear_combinations: raise AssertionError("recombination widening forbidden")
    if third_finite_difference_operator: raise AssertionError("exactly two finite differences retained")
    if arbitrary_degree_cutoff is not None: raise AssertionError("arbitrary degree cutoffs forbidden")

def assert_locks():
    out = {"K": {}, "G": {}}
    for name, want in K_BLOBS.items():
        got = a.git_blob_sha1(K_DIR / name)
        if got != want: raise AssertionError(f"K source lock drift: {name}")
        out["K"][name] = got
    kc = json.loads((K_DIR / "CONTRACT.json").read_text())
    if kc.get("operation") != "OZ-RT-BZ-T3-011-K" or kc.get("terminals",{}).get("closure") != K_REQUIRED_TERMINAL:
        raise AssertionError("K contract drift")
    for name, want in G_BLOBS.items():
        got = a.git_blob_sha1(G_DIR / name)
        if got != want: raise AssertionError(f"G source lock drift: {name}")
        out["G"][name] = got
    gc = json.loads((G_DIR / "T3_011_G_CONTRACT.json").read_text())
    if gc.get("terminals",{}).get("closure") != G_REQUIRED_TERMINAL: raise AssertionError("G contract drift")
    return out

def _d(sig): return {factor:int(exp) for factor,exp in sig if exp}
def _positive(sig):
    out = _d(sig)
    if not out or any(e <= 0 for e in out.values()): raise AssertionError("non-positive coordinate factor")
    return out
def _lcm(x,y): return abs(x*y)//math.gcd(x,y) if x and y else abs(x or y)
def _ray(alpha,beta):
    m = _lcm(alpha.denominator,beta.denominator)
    v = [int(alpha*m),int(beta*m),m]
    d = math.gcd(math.gcd(abs(v[0]),abs(v[1])),abs(v[2]))
    return [x//d for x in v]

def cancellation_ray(left_sig, right_sig, spectator_sig):
    L,R,E = _positive(left_sig),_positive(right_sig),_positive(spectator_sig)
    fs = sorted(set(L)|set(R)|set(E), key=repr); candidates = []
    for src, side in ((L,0),(R,1)):
        p = next(iter(src)); q = Q(E.get(p,0),src[p])
        if q >= 0 and all(q*src.get(x,0)==E.get(x,0) for x in fs):
            candidates.append(_ray(q,Q(0)) if side == 0 else _ray(Q(0),q))
    for i,x in enumerate(fs):
        for y in fs[i+1:]:
            det = L.get(x,0)*R.get(y,0)-L.get(y,0)*R.get(x,0)
            if not det: continue
            alpha = Q(E.get(x,0)*R.get(y,0)-E.get(y,0)*R.get(x,0),det)
            beta = Q(L.get(x,0)*E.get(y,0)-L.get(y,0)*E.get(x,0),det)
            if alpha >= 0 and beta >= 0 and all(alpha*L.get(z,0)+beta*R.get(z,0)==E.get(z,0) for z in fs):
                candidates.append(_ray(alpha,beta))
            break
    return min(candidates) if candidates else None

def _spectator(pair):
    rem = sorted({"n","k","l"}-{CHANNEL_COORDINATE[pair[0]],CHANNEL_COORDINATE[pair[1]]})
    if len(rem) != 1: raise AssertionError("pair does not determine unique spectator")
    return rem[0], CANONICAL_SPECTATOR_CHANNEL[rem[0]]

def first_blocker(factors):
    for pi,pair in enumerate(ADMITTED_PAIRS):
        axis, sch = _spectator(pair)
        for ci,(comp,lk,rk) in enumerate(COMPONENTS):
            for sid in sorted(set(factors[pair[0]]) & set(factors[pair[1]]) & set(factors[sch])):
                ls,_ = factors[pair[0]][sid][lk]; rs,_ = factors[pair[1]][sid][rk]; es,ec = factors[sch][sid]["x0"]
                if Q(ec) == 0:
                    return {"kind":"RECIPROCAL_SPECTATOR_SPECIALIZES_TO_ZERO","pair_index":pi,"pair":list(pair),"component_index":ci,"component":comp,"stratum":sid,"spectator_axis":axis,"spectator_channel_representative":sch}
                try: ray = cancellation_ray(ls,rs,es)
                except AssertionError as exc:
                    return {"kind":"RECIPROCAL_SPECTATOR_FACTOR_GEOMETRY_INVALID","pair_index":pi,"pair":list(pair),"component_index":ci,"component":comp,"stratum":sid,"spectator_axis":axis,"spectator_channel_representative":sch,"detail":str(exc)}
                if ray:
                    return {"kind":"UNBOUNDED_RECIPROCAL_SPECTATOR_CANCELLATION_RAY","pair_index":pi,"pair":list(pair),"component_index":ci,"component":comp,"stratum":sid,"spectator_axis":axis,"spectator_channel_representative":sch,"left_factor_kind":lk,"right_factor_kind":rk,"reciprocal_spectator_factor_kind":"x0","primitive_integer_ray":ray,"homogeneous_relation":"dr*L + ds*R - dt*E = 0"}
    return None

def build():
    validate_scope(); locks = assert_locks()
    _, strata, _, _ = f.d.build_context()
    factors = {ch:g.e._coordinate_factors(ch,strata) for ch in CHANNEL_COORDINATE}
    blocker = first_blocker(factors)
    if blocker is None:
        blocker = {"kind":"FINITE_RECIPROCAL_SPECTATOR_DOMAIN_NOT_ESTABLISHED","detail":"no arbitrary cutoff may replace a proof of boundedness"}
    return {
        "schema_version":"1.0.0","issue":ISSUE,"operation":OPERATION,"stage":STAGE,
        "status":"RECIPROCAL_SPECTATOR_LAURENT_COKERNEL_AUDIT_BLOCKED",
        "predecessor_checkpoint":{"reviewed_head":K_REVIEWED_HEAD,"merge_commit":K_MERGE_COMMIT,"source_blobs":locks,"required_terminal":K_REQUIRED_TERMINAL,"possible_record_count":1282,"tested_record_count":1282,"semantic_functional_ambiguity":None,"first_cokernel_breaking_direction":None},
        "reciprocal_spectator_class":{"monomial_domain":"x_c^r*x_d^s*x_e^-t with integers r>=1,s>=1,t>=1","unordered_pair_order":[list(p) for p in ADMITTED_PAIRS],"spectator_is_unshifted":True,"reciprocal_spectator_admitted":True,"arbitrary_degree_cutoff_used":False,"third_finite_difference_operator_admitted":False},
        "characterized_blocker":blocker,"possible_record_count":1282,"tested_record_count":0,"tested_records":[],
        "semantic_functional_ambiguity":None,"first_cokernel_breaking_direction":None,
        "all_reciprocal_spectator_responses_cokernel_invisible":False,
        "residual_sum_zero_proved":False,"proof_effect":"NONE","promotion_effect":"NONE","t3_status":"OPEN_WITH_CHARACTERIZED_BLOCKER","terminal":BLOCKER_TERMINAL,
    }
