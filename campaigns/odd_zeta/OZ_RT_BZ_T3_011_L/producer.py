from __future__ import annotations

import importlib.util
import json
import math
import sys
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
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


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
COMPONENTS = (
    ("ScSd", "x1", "x1", (0, 1)),
    ("Sc", "x1", "x0", (0,)),
    ("Sd", "x0", "x1", (1,)),
    ("I", "x0", "x0", ()),
)
BLOCKER_TERMINAL = "RECIPROCAL_SPECTATOR_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"


def validate_scope(
    reciprocal_spectator=True,
    reciprocal_left=False,
    reciprocal_right=False,
    multiple_reciprocal_axes=False,
    shifted_spectator=False,
    shifted_poles=False,
    arbitrary_rational_functions=False,
    support_or_harmonic_enlargement=False,
    candidate_bank_or_scalar_namespace_widening=False,
    recurrence_widening=False,
    correction_recombination=False,
    candidate_linear_combinations=False,
    third_finite_difference_operator=False,
    arbitrary_degree_cutoff=None,
):
    if not reciprocal_spectator:
        raise AssertionError("L changes exactly the spectator exponent sign")
    if reciprocal_left or reciprocal_right or multiple_reciprocal_axes:
        raise AssertionError("only spectator may be reciprocal")
    if shifted_spectator or shifted_poles:
        raise AssertionError("spectator stays unshifted; shifted poles forbidden")
    if arbitrary_rational_functions:
        raise AssertionError("arbitrary rational functions forbidden")
    if support_or_harmonic_enlargement or candidate_bank_or_scalar_namespace_widening:
        raise AssertionError("basis widening forbidden")
    if recurrence_widening or correction_recombination or candidate_linear_combinations:
        raise AssertionError("recombination widening forbidden")
    if third_finite_difference_operator:
        raise AssertionError("exactly two finite differences retained")
    if arbitrary_degree_cutoff is not None:
        raise AssertionError("arbitrary degree cutoffs forbidden")


def assert_locks():
    out = {"K": {}, "G": {}}
    for name, want in K_BLOBS.items():
        got = a.git_blob_sha1(K_DIR / name)
        if got != want:
            raise AssertionError(f"K source lock drift: {name}")
        out["K"][name] = got
    kc = json.loads((K_DIR / "CONTRACT.json").read_text())
    if (
        kc.get("operation") != "OZ-RT-BZ-T3-011-K"
        or kc.get("terminals", {}).get("closure") != K_REQUIRED_TERMINAL
    ):
        raise AssertionError("K contract drift")
    for name, want in G_BLOBS.items():
        got = a.git_blob_sha1(G_DIR / name)
        if got != want:
            raise AssertionError(f"G source lock drift: {name}")
        out["G"][name] = got
    gc = json.loads((G_DIR / "T3_011_G_CONTRACT.json").read_text())
    if gc.get("terminals", {}).get("closure") != G_REQUIRED_TERMINAL:
        raise AssertionError("G contract drift")
    return out


def _d(sig):
    return {factor: int(exp) for factor, exp in sig if exp}


def _positive(sig):
    out = _d(sig)
    if not out or any(e <= 0 for e in out.values()):
        raise AssertionError("non-positive coordinate factor")
    return out


def _single_step(sig, label):
    out = _positive(sig)
    if len(out) != 1:
        raise AssertionError(f"{label} coordinate factor is not a single affine Laurent atom")
    return next(iter(out.items()))


def _lcm(x, y):
    return abs(x * y) // math.gcd(x, y) if x and y else abs(x or y)


def _ray(alpha, beta):
    m = _lcm(alpha.denominator, beta.denominator)
    v = [int(alpha * m), int(beta * m), m]
    d = math.gcd(math.gcd(abs(v[0]), abs(v[1])), abs(v[2]))
    return [x // d for x in v]


def cancellation_ray(left_sig, right_sig, spectator_sig):
    """Return a primitive nonnegative ray dr*L + ds*R - dt*E = 0."""
    L, R, E = _positive(left_sig), _positive(right_sig), _positive(spectator_sig)
    fs = sorted(set(L) | set(R) | set(E), key=repr)
    candidates = []
    for src, side in ((L, 0), (R, 1)):
        p = next(iter(src))
        q = Q(E.get(p, 0), src[p])
        if q >= 0 and all(q * src.get(x, 0) == E.get(x, 0) for x in fs):
            candidates.append(_ray(q, Q(0)) if side == 0 else _ray(Q(0), q))
    for i, x in enumerate(fs):
        for y in fs[i + 1 :]:
            det = L.get(x, 0) * R.get(y, 0) - L.get(y, 0) * R.get(x, 0)
            if not det:
                continue
            alpha = Q(E.get(x, 0) * R.get(y, 0) - E.get(y, 0) * R.get(x, 0), det)
            beta = Q(L.get(x, 0) * E.get(y, 0) - L.get(y, 0) * E.get(x, 0), det)
            if alpha >= 0 and beta >= 0 and all(
                alpha * L.get(z, 0) + beta * R.get(z, 0) == E.get(z, 0)
                for z in fs
            ):
                candidates.append(_ray(alpha, beta))
            break
    return min(candidates) if candidates else None


def _egcd(a0, b0):
    old_r, r = a0, b0
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def _ceil_div(p, q):
    if q <= 0:
        raise AssertionError("positive divisor required")
    return -((-p) // q)


def _two_positive(a0, b0, d0):
    """Solve a*x - b*y=d with x,y>=1, or return None."""
    g0, u, v = _egcd(a0, b0)
    if d0 % g0:
        return None
    scale = d0 // g0
    x0 = u * scale
    y0 = -v * scale
    sx, sy = b0 // g0, a0 // g0
    n = max(_ceil_div(1 - x0, sx), _ceil_div(1 - y0, sy))
    x, y = x0 + sx * n, y0 + sy * n
    if x < 1 or y < 1 or a0 * x - b0 * y != d0:
        raise AssertionError("positive Diophantine reconstruction failed")
    return x, y


def feasible_seed(base_sig, target_sig, left_sig, right_sig, spectator_sig):
    """Find one positive integer solution target-base=rL+sR-tE when a ray exists."""
    lf, le = _single_step(left_sig, "left")
    rf, re = _single_step(right_sig, "right")
    ef, ee = _single_step(spectator_sig, "spectator")
    base, target = _d(base_sig), _d(target_sig)
    factors = set(base) | set(target) | {lf, rf, ef}
    diff = {z: target.get(z, 0) - base.get(z, 0) for z in factors}
    if any(diff[z] for z in factors - {lf, rf, ef}):
        return None

    if ef == lf and ef != rf:
        if diff.get(rf, 0) % re:
            return None
        s = diff.get(rf, 0) // re
        if s < 1:
            return None
        pair = _two_positive(le, ee, diff.get(lf, 0))
        return [pair[0], s, pair[1]] if pair else None

    if ef == rf and ef != lf:
        if diff.get(lf, 0) % le:
            return None
        r = diff.get(lf, 0) // le
        if r < 1:
            return None
        pair = _two_positive(re, ee, diff.get(rf, 0))
        return [r, pair[0], pair[1]] if pair else None

    if ef == lf == rf:
        d0 = diff.get(ef, 0)
        h = math.gcd(le, ee)
        g0 = math.gcd(re, h)
        if d0 % g0:
            return None
        period = h // g0
        for s in range(1, period + 1):
            rhs = d0 - re * s
            if rhs % h:
                continue
            pair = _two_positive(le, ee, rhs)
            if pair:
                return [pair[0], s, pair[1]]
        raise AssertionError("congruence class exists but no positive seed was reconstructed")

    return None


def _spectator(pair):
    rem = sorted(
        {"n", "k", "l"}
        - {CHANNEL_COORDINATE[pair[0]], CHANNEL_COORDINATE[pair[1]]}
    )
    if len(rem) != 1:
        raise AssertionError("pair does not determine unique spectator")
    return rem[0], CANONICAL_SPECTATOR_CHANNEL[rem[0]]


def _blocker_for_record(
    pair_index,
    endpoint_index,
    candidate_index,
    pair,
    endpoint,
    uid,
    strata,
    bank,
    witness_index,
    factors,
    poly_cache,
    vector_cache,
):
    left, right = pair
    axis, sch = _spectator(pair)
    component_indexes = {
        "I": g._cached_vector_index(endpoint, uid, (), strata, bank, poly_cache, vector_cache)[1],
        "Sc": g._cached_vector_index(endpoint, uid, (left,), strata, bank, poly_cache, vector_cache)[1],
        "Sd": g._cached_vector_index(endpoint, uid, (right,), strata, bank, poly_cache, vector_cache)[1],
        "ScSd": g._cached_vector_index(endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache)[1],
    }

    support_matches = 0
    for component_index, (component, lk, rk, _shift_marker) in enumerate(COMPONENTS):
        base_index = component_indexes[component]
        for base_key in sorted(set(witness_index) & set(base_index), key=repr):
            cell_id, scalar, mon = base_key
            sid = g._stratum_id(cell_id)
            ls, _lc = factors[left][sid][lk]
            rs, _rc = factors[right][sid][rk]
            es, ec = factors[sch][sid]["x0"]
            ray = cancellation_ray(ls, rs, es)
            if ray is None:
                continue
            for target_sig, _weight in sorted(witness_index[base_key], key=repr):
                for base_sig, _coeff in sorted(base_index[base_key], key=repr):
                    support_matches += 1
                    seed = feasible_seed(base_sig, target_sig, ls, rs, es)
                    if seed is None:
                        continue
                    if Q(ec) == 0:
                        kind = "RECIPROCAL_SPECTATOR_SPECIALIZES_TO_ZERO_ON_ADMITTED_SUPPORT"
                    else:
                        kind = "UNBOUNDED_RECIPROCAL_SPECTATOR_CANCELLATION_RAY"
                    return {
                        "kind": kind,
                        "pair_index": pair_index,
                        "endpoint_index": endpoint_index,
                        "candidate_index": candidate_index,
                        "pair": list(pair),
                        "endpoint": endpoint,
                        "candidate": k.unknown_json(uid),
                        "component_index": component_index,
                        "component": component,
                        "stratum": sid,
                        "spectator_axis": axis,
                        "spectator_channel_representative": sch,
                        "left_factor_kind": lk,
                        "right_factor_kind": rk,
                        "reciprocal_spectator_factor_kind": "x0",
                        "primitive_integer_ray": ray,
                        "feasible_seed_tridegree": seed,
                        "support_key": [cell_id, scalar, list(mon)],
                        "base_signature": list(base_sig),
                        "target_signature": list(target_sig),
                        "homogeneous_relation": "dr*L + ds*R - dt*E = 0",
                        "affine_relation": "target-base = r*L + s*R - t*E",
                    }, support_matches
    return None, support_matches


def first_admitted_blocker(strata, banks, factors):
    witness_indexes = {
        channel: g._witness_index(bank["witness"]) for channel, bank in banks.items()
    }
    poly_cache = {}
    vector_cache = {}
    records_inspected = 0
    support_matches = 0
    for pair_index, pair in enumerate(ADMITTED_PAIRS):
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                blocker, seen = _blocker_for_record(
                    pair_index,
                    endpoint_index,
                    candidate_index,
                    pair,
                    endpoint,
                    uid,
                    strata,
                    bank,
                    witness_indexes[endpoint],
                    factors,
                    poly_cache,
                    vector_cache,
                )
                records_inspected += 1
                support_matches += seen
                if blocker is not None:
                    return blocker, records_inspected, support_matches
    return None, records_inspected, support_matches


def build():
    validate_scope()
    locks = assert_locks()
    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    factors = {ch: g.e._coordinate_factors(ch, strata) for ch in CHANNEL_COORDINATE}
    blocker, records_inspected, support_matches = first_admitted_blocker(
        strata, banks, factors
    )
    if blocker is None:
        blocker = {
            "kind": "FINITE_RECIPROCAL_SPECTATOR_DOMAIN_NOT_ESTABLISHED",
            "detail": (
                "no admitted support match with a nonnegative recession ray was found; "
                "a finite exact reciprocal-domain solver is required before any pairing scan"
            ),
        }
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "RECIPROCAL_SPECTATOR_LAURENT_COKERNEL_AUDIT_BLOCKED",
        "predecessor_checkpoint": {
            "reviewed_head": K_REVIEWED_HEAD,
            "merge_commit": K_MERGE_COMMIT,
            "source_blobs": locks,
            "required_terminal": K_REQUIRED_TERMINAL,
            "possible_record_count": 1282,
            "tested_record_count": 1282,
            "semantic_functional_ambiguity": None,
            "first_cokernel_breaking_direction": None,
        },
        "reciprocal_spectator_class": {
            "monomial_domain": "x_c^r*x_d^s*x_e^-t with integers r>=1,s>=1,t>=1",
            "unordered_pair_order": [list(p) for p in ADMITTED_PAIRS],
            "spectator_is_unshifted": True,
            "reciprocal_spectator_admitted": True,
            "arbitrary_degree_cutoff_used": False,
            "third_finite_difference_operator_admitted": False,
        },
        "domain_analysis": {
            "candidate_records_inspected_for_support": records_inspected,
            "ray_bearing_support_signature_pairs_inspected": support_matches,
            "feasible_support_seed_required": True,
            "arbitrary_degree_cutoff_used": False,
        },
        "characterized_blocker": blocker,
        "possible_record_count": 1282,
        "tested_record_count": 0,
        "tested_records": [],
        "semantic_functional_ambiguity": None,
        "first_cokernel_breaking_direction": None,
        "all_reciprocal_spectator_responses_cokernel_invisible": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": BLOCKER_TERMINAL,
    }
