from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
M_DIR = HERE.parent / "OZ_RT_BZ_T3_011_M"
G_DIR = HERE.parent / "OZ_RT_BZ_T3_010"
if str(G_DIR) not in sys.path:
    sys.path.insert(0, str(G_DIR))


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load(M_DIR / "producer.py", "oz_t3_011_m_for_n")
k = m.k
j = m.j
i = j.i
h = j.h
g, f, a = m.g, m.f, m.a

OPERATION = "OZ-RT-BZ-T3-011-N"
STAGE = "T3_011_N_DOUBLE_RECIPROCAL_ACTIVE_POSITIVE_SPECTATOR_COKERNEL_AUDIT"
ISSUE = 929
M_REVIEWED_HEAD = "a381062f8d2287b7a08a79d2572ecdf8693baebb"
M_MERGE_COMMIT = "5accb4c59db6e0495476a08afed87fb62c196a20"
M_REQUIRED_TERMINAL = "SINGLE_RECIPROCAL_ACTIVE_TRIVARIATE_RESPONSE_CLASS_COKERNEL_INVISIBLE"
M_EXPECTED_RECORDS = 2564
M_BLOBS = {
    "producer.py": "19ec58bd410359f3721236bbabc612d0f649636b",
    "CONTRACT.json": "e3aaea4f714c3e243fd8a782baf59e05111380a6",
    "verifier.py": "8621c594d510b54928a798259fadcf67f7fb6b82",
}
I_REQUIRED_TERMINAL = i.CLOSURE_TERMINAL
ADMITTED_PAIRS = tuple(m.ADMITTED_PAIRS)
CHANNEL_COORDINATE = dict(m.CHANNEL_COORDINATE)
CANONICAL_SPECTATOR_CHANNEL = dict(m.CANONICAL_SPECTATOR_CHANNEL)
ORIENTATIONS = ("negative_left_negative_right",)
FROZEN_RECORD_COUNT = m.FROZEN_RECORD_COUNT
POSSIBLE_RECORD_COUNT = FROZEN_RECORD_COUNT * len(ORIENTATIONS)
COMPONENTS = (
    ("ScSd", "x1", "x1", (0, 1)),
    ("Sc", "x1", "x0", (0,)),
    ("Sd", "x0", "x1", (1,)),
    ("I", "x0", "x0", ()),
)
ESCAPE_TERMINAL = "DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_RESPONSE_ESCAPE_FOUND"
CLOSURE_TERMINAL = "DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_RESPONSE_CLASS_COKERNEL_INVISIBLE"
AMBIGUITY_TERMINAL = "DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY"
BLOCKER_TERMINAL = "DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"


class UnboundedSupportOverlap(RuntimeError):
    def __init__(self, evidence: dict):
        super().__init__("double-reciprocal-active trivariate support overlap is unbounded")
        self.evidence = evidence


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]


def validate_scope(
    reciprocal_active_axes: int = 2,
    reciprocal_spectator: bool = False,
    shifted_spectator: bool = False,
    shifted_poles: bool = False,
    arbitrary_rational_functions: bool = False,
    support_or_harmonic_enlargement: bool = False,
    candidate_bank_or_scalar_namespace_widening: bool = False,
    recurrence_widening: bool = False,
    correction_recombination: bool = False,
    candidate_linear_combinations: bool = False,
    third_finite_difference_operator: bool = False,
    arbitrary_degree_cutoff=None,
):
    if reciprocal_active_axes != 2:
        raise AssertionError("N admits exactly two reciprocal active axes")
    if reciprocal_spectator:
        raise AssertionError("N spectator exponent remains positive")
    if shifted_spectator or shifted_poles:
        raise AssertionError("N retains the unshifted spectator and coordinate-zero poles only")
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
    got = {}
    for name, want in M_BLOBS.items():
        value = a.git_blob_sha1(M_DIR / name)
        if value != want:
            raise AssertionError(f"M source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((M_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-M":
        raise AssertionError("M contract operation drift")
    if contract.get("terminals", {}).get("closure") != M_REQUIRED_TERMINAL:
        raise AssertionError("M closure terminal drift")
    return {"M": got}


def _sig_dict(sig):
    return {factor: int(exp) for factor, exp in sig if exp}


def _single_step(sig, label):
    d = _sig_dict(sig)
    if len(d) != 1:
        raise AssertionError(f"{label} is not a single affine Laurent atom")
    factor, exp = next(iter(d.items()))
    if exp == 0:
        raise AssertionError(f"{label} has zero Laurent exponent")
    return factor, exp


def _ceil_div(p: int, q: int) -> int:
    if q <= 0:
        raise AssertionError("positive divisor required")
    return -((-p) // q)


def _egcd(a: int, b: int):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return abs(old_r), old_s if old_r >= 0 else -old_s, old_t if old_r >= 0 else -old_t


def _two_nonnegative(a: int, b: int, d: int):
    """Solve a*x - b*y=d with a,b>0 and x,y>=0."""
    gg, u, v = _egcd(a, b)
    if d % gg:
        return None
    scale = d // gg
    x0 = u * scale
    y0 = -v * scale
    sx, sy = b // gg, a // gg
    n = max(_ceil_div(-x0, sx), _ceil_div(-y0, sy))
    x, y = x0 + sx * n, y0 + sy * n
    if x < 0 or y < 0 or a * x - b * y != d:
        raise AssertionError("nonnegative Diophantine reconstruction drift")
    return x, y


def _finite_same_sign(coeffs, rhs):
    sign = 1 if coeffs[0] > 0 else -1
    if any((1 if c > 0 else -1) != sign for c in coeffs):
        raise AssertionError("same-sign solver received mixed signs")
    target = sign * rhs
    aa = [abs(c) for c in coeffs]
    if target < 0:
        return []
    if len(aa) == 1:
        return [(target // aa[0],)] if target % aa[0] == 0 else []
    if len(aa) == 2:
        out = []
        for x in range(target // aa[0] + 1):
            rem = target - aa[0] * x
            if rem % aa[1] == 0:
                out.append((x, rem // aa[1]))
        return out
    if len(aa) == 3:
        out = []
        for x in range(target // aa[0] + 1):
            rem1 = target - aa[0] * x
            for y in range(rem1 // aa[1] + 1):
                rem2 = rem1 - aa[1] * y
                if rem2 % aa[2] == 0:
                    out.append((x, y, rem2 // aa[2]))
        return out
    raise AssertionError("unexpected same-sign group arity")


def _mixed_group(coeffs, rhs):
    """Return (base_solution, primitive_ray) for a mixed-sign group, or None."""
    pos = [i for i, c in enumerate(coeffs) if c > 0]
    neg = [i for i, c in enumerate(coeffs) if c < 0]
    if not pos or not neg:
        raise AssertionError("mixed-group solver received one sign")
    if len(coeffs) == 2:
        ip, im = pos[0], neg[0]
        seed = _two_nonnegative(coeffs[ip], -coeffs[im], rhs)
        if seed is None:
            return None
        base = [0, 0]
        base[ip], base[im] = seed
        gg = math.gcd(coeffs[ip], -coeffs[im])
        ray = [0, 0]
        ray[ip] = (-coeffs[im]) // gg
        ray[im] = coeffs[ip] // gg
        return tuple(base), tuple(ray)
    if len(coeffs) != 3:
        raise AssertionError("unexpected mixed-sign group arity")

    cc = list(coeffs)
    dd = rhs
    if len(pos) == 1:
        cc = [-c for c in cc]
        dd = -dd
    pos2 = [i for i, c in enumerate(cc) if c > 0]
    neg2 = [i for i, c in enumerate(cc) if c < 0]
    if len(pos2) != 2 or len(neg2) != 1:
        raise AssertionError("mixed trivariate sign normalization drift")
    ix, iy = pos2
    iz = neg2[0]
    ax, by, cz = cc[ix], cc[iy], -cc[iz]
    hh = math.gcd(ax, cz)
    gg = math.gcd(by, hh)
    if dd % gg:
        return None
    period = hh // gg
    chosen = None
    for y in range(period):
        rem = dd - by * y
        if rem % hh:
            continue
        pair = _two_nonnegative(ax, cz, rem)
        if pair is not None:
            chosen = (pair[0], y, pair[1])
            break
    if chosen is None:
        raise AssertionError("mixed trivariate congruence class was not reconstructed")
    base = [0, 0, 0]
    base[ix], base[iy], base[iz] = chosen
    rg = math.gcd(ax, cz)
    ray = [0, 0, 0]
    ray[ix] = cz // rg
    ray[iz] = ax // rg
    return tuple(base), tuple(ray)


@lru_cache(maxsize=None)
def solve_signed_tridegrees(base_sig, left_sig, right_sig, spectator_sig, target_sig, lower=(1, 1, 1)):
    """Solve target-base = r*L+s*R+t*E exactly for x>=lower.

    L/R signatures may be positive or reciprocal (negative); spectator is positive.
    Returns (status, finite_solutions, seed, primitive_ray), where status is
    `finite` or `unbounded`. There is no degree cutoff.
    """
    steps = [
        _single_step(left_sig, "left"),
        _single_step(right_sig, "right"),
        _single_step(spectator_sig, "spectator"),
    ]
    base = _sig_dict(base_sig)
    target = _sig_dict(target_sig)
    factors = set(base) | set(target) | {factor for factor, _ in steps}
    rhs = {z: target.get(z, 0) - base.get(z, 0) for z in factors}
    for i, (factor, coeff) in enumerate(steps):
        rhs[factor] -= coeff * int(lower[i])

    groups = {}
    for i, (factor, coeff) in enumerate(steps):
        groups.setdefault(factor, []).append((i, coeff))
    for factor in factors - set(groups):
        if rhs[factor] != 0:
            return "finite", (), None, None

    local = []
    unbounded = None
    for factor in sorted(groups, key=repr):
        members = groups[factor]
        indexes = [i for i, _ in members]
        coeffs = [c for _, c in members]
        d = rhs.get(factor, 0)
        signs = {1 if c > 0 else -1 for c in coeffs}
        if len(signs) == 1:
            sols = _finite_same_sign(coeffs, d)
            if not sols:
                return "finite", (), None, None
            local.append((indexes, sols))
        else:
            result = _mixed_group(coeffs, d)
            if result is None:
                return "finite", (), None, None
            base_local, ray_local = result
            local.append((indexes, [base_local]))
            ray = [0, 0, 0]
            for idx, value in zip(indexes, ray_local):
                ray[idx] = value
            unbounded = tuple(ray) if unbounded is None else unbounded

    def combine(choice):
        y = [0, 0, 0]
        for (indexes, _sols), vals in zip(local, choice):
            for idx, value in zip(indexes, vals):
                y[idx] = value
        return tuple(y[i] + int(lower[i]) for i in range(3))

    seed_choice = tuple(sols[0] for _idx, sols in local)
    seed = combine(seed_choice)
    if unbounded is not None:
        if not _solution_matches(base_sig, left_sig, right_sig, spectator_sig, target_sig, seed):
            raise AssertionError("unbounded affine seed reconstruction drift")
        if not _ray_matches(left_sig, right_sig, spectator_sig, unbounded):
            raise AssertionError("unbounded homogeneous ray reconstruction drift")
        return "unbounded", (), seed, unbounded

    out = []
    for choice in itertools.product(*(sols for _idx, sols in local)):
        degree = combine(choice)
        if not _solution_matches(base_sig, left_sig, right_sig, spectator_sig, target_sig, degree):
            raise AssertionError("finite signed tridegree reconstruction drift")
        out.append(degree)
    return "finite", tuple(sorted(set(out))), None, None


def _solution_matches(base_sig, left_sig, right_sig, spectator_sig, target_sig, degree):
    out = _sig_dict(base_sig)
    for sig, power in zip((left_sig, right_sig, spectator_sig), degree):
        for factor, exp in sig:
            out[factor] = out.get(factor, 0) + int(exp) * int(power)
            if out[factor] == 0:
                del out[factor]
    return tuple(sorted(out.items())) == tuple(target_sig)


def _ray_matches(left_sig, right_sig, spectator_sig, ray):
    out = {}
    for sig, power in zip((left_sig, right_sig, spectator_sig), ray):
        for factor, exp in sig:
            out[factor] = out.get(factor, 0) + int(exp) * int(power)
    return all(value == 0 for value in out.values()) and any(ray)


def _spectator(pair):
    remaining = {"n", "k", "l"} - {
        CHANNEL_COORDINATE[pair[0]], CHANNEL_COORDINATE[pair[1]]
    }
    if len(remaining) != 1:
        raise AssertionError("pair does not determine unique spectator")
    axis = next(iter(remaining))
    return axis, CANONICAL_SPECTATOR_CHANNEL[axis]


def _orientation_maps(pair, orientation, forward_factors, inverse_factors):
    left, right = pair
    if orientation == "negative_left_negative_right":
        return inverse_factors[left], inverse_factors[right], "both"
    raise AssertionError(f"unknown orientation: {orientation}")


def signed_moment_ledger(
    witness_index,
    base_index,
    left_maps,
    left_kind,
    right_maps,
    right_kind,
    spectator_maps,
    lower,
    context,
):
    aggregate = {}
    possible = set()
    matches = []
    support_pairs = 0
    for base_key in sorted(set(witness_index) & set(base_index), key=repr):
        cell_id, scalar, mon = base_key
        sid = g._stratum_id(cell_id)
        left_sig, left_coeff = left_maps[sid][left_kind]
        right_sig, right_coeff = right_maps[sid][right_kind]
        spectator_sig, spectator_coeff = spectator_maps[sid]["x0"]
        for target_sig, weight in witness_index[base_key]:
            for base_sig, coeff in base_index[base_key]:
                support_pairs += 1
                status, degrees, seed, ray = solve_signed_tridegrees(
                    base_sig, left_sig, right_sig, spectator_sig, target_sig, tuple(lower)
                )
                if status == "unbounded":
                    raise UnboundedSupportOverlap({
                        **context,
                        "cell_id": cell_id,
                        "stratum_id": sid,
                        "scalar": scalar,
                        "monomial": list(mon),
                        "base_signature": [list(x) for x in base_sig],
                        "target_signature": [list(x) for x in target_sig],
                        "left_step_signature": [list(x) for x in left_sig],
                        "right_step_signature": [list(x) for x in right_sig],
                        "spectator_step_signature": [list(x) for x in spectator_sig],
                        "feasible_seed_tridegree": list(seed),
                        "primitive_integer_ray": list(ray),
                        "support_feasible_recession": True,
                    })
                for r, s, t in degrees:
                    possible.add((r, s, t))
                    contribution = (
                        weight * coeff * (left_coeff ** r) * (right_coeff ** s) * (spectator_coeff ** t)
                    )
                    aggregate[(r, s, t)] = aggregate.get((r, s, t), Q(0)) + contribution
                    matches.append([
                        r, s, t, cell_id, scalar, list(mon), qjson(weight), qjson(coeff), qjson(contribution)
                    ])
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    rows = [[r, s, t, *qjson(aggregate[(r, s, t)])] for r, s, t in sorted(aggregate)]
    return {
        "possible_tridegrees": [[r, s, t] for r, s, t in sorted(possible)],
        "nonzero_tridegrees": [[r, s, t] for r, s, t in sorted(aggregate)],
        "coefficient_rows": rows,
        "coefficient_sha256": sha(rows),
        "match_count": len(matches),
        "match_sha256": sha(matches),
        "support_signature_pairs_inspected": support_pairs,
        "_aggregate": aggregate,
    }


def _pairing_rows(ledgers, degrees):
    rows = []
    for degree in sorted(degrees):
        value = (
            ledgers["ScSd"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sc"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sd"]["_aggregate"].get(degree, Q(0))
            + ledgers["I"]["_aggregate"].get(degree, Q(0))
        )
        rows.append([*degree, *qjson(value)])
    return rows


def _strip_internal(ledger):
    return {key: value for key, value in ledger.items() if not key.startswith("_")}


def _component_indexes(endpoint, uid, pair, strata, bank, poly_cache, vector_cache):
    left, right = pair
    return {
        "I": g._cached_vector_index(endpoint, uid, (), strata, bank, poly_cache, vector_cache)[1],
        "Sc": g._cached_vector_index(endpoint, uid, (left,), strata, bank, poly_cache, vector_cache)[1],
        "Sd": g._cached_vector_index(endpoint, uid, (right,), strata, bank, poly_cache, vector_cache)[1],
        "ScSd": g._cached_vector_index(endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache)[1],
    }


def _make_ledgers(pair, endpoint, uid, orientation, strata, bank, witness_index, forward_factors, inverse_factors, poly_cache, vector_cache, lower, purpose):
    left, right = pair
    axis, sch = _spectator(pair)
    left_maps, right_maps, reciprocal_axis = _orientation_maps(pair, orientation, forward_factors, inverse_factors)
    spectator_maps = forward_factors[sch]
    indexes = _component_indexes(endpoint, uid, pair, strata, bank, poly_cache, vector_cache)
    ledgers = {}
    for name, lk, rk, _marker in COMPONENTS:
        ledgers[name] = signed_moment_ledger(
            witness_index,
            indexes[name],
            left_maps,
            lk,
            right_maps,
            rk,
            spectator_maps,
            lower,
            {
                "pair": list(pair),
                "endpoint": endpoint,
                "candidate": unknown_json(uid),
                "orientation": orientation,
                "reciprocal_active_axis": reciprocal_axis,
                "spectator_axis": axis,
                "component": name,
                "purpose": purpose,
            },
        )
    return ledgers, axis, sch, reciprocal_axis, indexes


def _i_boundary_rows(pair, endpoint, uid, strata, bank, witness_index, inverse_factors, poly_cache, vector_cache):
    left, right = pair
    indexes = _component_indexes(endpoint, uid, pair, strata, bank, poly_cache, vector_cache)
    ledgers = {
        "ScSd": i.inverse_bivariate_moment_ledger(witness_index, indexes["ScSd"], inverse_factors[left], "x1", inverse_factors[right], "x1"),
        "Sc": i.inverse_bivariate_moment_ledger(witness_index, indexes["Sc"], inverse_factors[left], "x1", inverse_factors[right], "x0"),
        "Sd": i.inverse_bivariate_moment_ledger(witness_index, indexes["Sd"], inverse_factors[left], "x0", inverse_factors[right], "x1"),
        "I": i.inverse_bivariate_moment_ledger(witness_index, indexes["I"], inverse_factors[left], "x0", inverse_factors[right], "x0"),
    }
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_bidegrees"]))
    selected = {(r, s) for r, s in domain if r >= 1 and s >= 1}
    rows = []
    for r, s in sorted(selected):
        value = (
            ledgers["ScSd"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sc"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sd"]["_aggregate"].get((r, s), Q(0))
            + ledgers["I"]["_aggregate"].get((r, s), Q(0))
        )
        rows.append([r, s, *qjson(value)])
    return rows


def _n_zero_boundary_rows(pair, endpoint, uid, zero_side, strata, bank, witness_index, forward_factors, inverse_factors, poly_cache, vector_cache):
    lower = (0, 1, 1) if zero_side == "left" else (1, 0, 1)
    selector = (
        (lambda r, s, t: r == 0 and s >= 1 and t >= 1)
        if zero_side == "left"
        else (lambda r, s, t: s == 0 and r >= 1 and t >= 1)
    )
    ledgers, *_ = _make_ledgers(
        pair, endpoint, uid, "negative_left_negative_right", strata, bank,
        witness_index, forward_factors, inverse_factors, poly_cache, vector_cache,
        lower, f"{zero_side}_reciprocal_degree_zero_N_boundary"
    )
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
    return _pairing_rows(ledgers, {(r, s, t) for r, s, t in domain if selector(r, s, t)})


def _m_zero_boundary_rows(pair, endpoint, uid, zero_side, strata, bank, witness_index, forward_factors, inverse_factors, poly_cache, vector_cache):
    if zero_side == "left":
        orientation, lower = "positive_left_negative_right", (0, 1, 1)
        selector = lambda r, s, t: r == 0 and s >= 1 and t >= 1
    elif zero_side == "right":
        orientation, lower = "negative_left_positive_right", (1, 0, 1)
        selector = lambda r, s, t: s == 0 and r >= 1 and t >= 1
    else:
        raise AssertionError("unknown zero boundary")
    ledgers, *_ = m._make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
        lower, f"{zero_side}_reciprocal_degree_zero_M_boundary"
    )
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
    return m._pairing_rows(ledgers, {(r, s, t) for r, s, t in domain if selector(r, s, t)})


def _candidate_record(pair, endpoint, uid, orientation, strata, bank, witness_index, forward_factors, inverse_factors, poly_cache, vector_cache):
    primary, axis, sch, reciprocal_axis, _indexes = _make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
        (1, 1, 1), "admitted_N_class"
    )
    domain = set()
    support_pairs = 0
    for ledger in primary.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
        support_pairs += ledger["support_signature_pairs_inspected"]
    domain = {(r, s, t) for r, s, t in domain if min(r, s, t) >= 1}
    pairing_rows = _pairing_rows(primary, domain)
    nonzero = [row for row in pairing_rows if row[-2] != 0]

    i_ledgers, *_ = _make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
        (1, 1, 0), "t_zero_I_boundary"
    )
    i_domain = set()
    for ledger in i_ledgers.values():
        i_domain.update(map(tuple, ledger["possible_tridegrees"]))
    i_selected = {(r, s, 0) for r, s, t in i_domain if r >= 1 and s >= 1 and t == 0}
    i_rows_here = [[r, s, num, den] for r, s, _t, num, den in _pairing_rows(i_ledgers, i_selected)]
    i_rows_protected = _i_boundary_rows(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse_factors, poly_cache, vector_cache
    )
    i_match = i_rows_here == i_rows_protected and not any(row[-2] != 0 for row in i_rows_protected)

    left_zero_here = _n_zero_boundary_rows(
        pair, endpoint, uid, "left", strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache
    )
    left_zero_protected = _m_zero_boundary_rows(
        pair, endpoint, uid, "left", strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache
    )
    right_zero_here = _n_zero_boundary_rows(
        pair, endpoint, uid, "right", strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache
    )
    right_zero_protected = _m_zero_boundary_rows(
        pair, endpoint, uid, "right", strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache
    )
    m_match = (
        left_zero_here == left_zero_protected
        and right_zero_here == right_zero_protected
        and not any(row[-2] != 0 for row in left_zero_protected + right_zero_protected)
    )

    ambiguity = None
    if not i_match:
        ambiguity = "T_ZERO_BOUNDARY_DISAGREES_WITH_PROTECTED_T3_011_I"
    elif not m_match:
        ambiguity = "RECIPROCAL_DEGREE_ZERO_BOUNDARY_DISAGREES_WITH_PROTECTED_T3_011_M"

    return {
        "pair": list(pair),
        "endpoint": endpoint,
        "candidate": unknown_json(uid),
        "coordinate_pair": [CHANNEL_COORDINATE[pair[0]], CHANNEL_COORDINATE[pair[1]]],
        "orientation": orientation,
        "reciprocal_active_axes": reciprocal_axis,
        "spectator_axis": axis,
        "spectator_channel_representative": sch,
        "finite_overlap_tridegrees": [[r, s, t] for r, s, t in sorted(domain)],
        "finite_overlap_sha256": sha([[r, s, t] for r, s, t in sorted(domain)]),
        "component_ledgers": {name: _strip_internal(ledger) for name, ledger in primary.items()},
        "pairing_rows": pairing_rows,
        "pairing_sha256": sha(pairing_rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_tridegree": nonzero[0][:3] if nonzero else None,
        "t_zero_boundary_rows": i_rows_here,
        "protected_I_boundary_rows": i_rows_protected,
        "t_zero_semantics_exactly_match_I": i_match,
        "left_reciprocal_degree_zero_boundary_rows": left_zero_here,
        "protected_M_left_boundary_rows": left_zero_protected,
        "right_reciprocal_degree_zero_boundary_rows": right_zero_here,
        "protected_M_right_boundary_rows": right_zero_protected,
        "reciprocal_degree_zero_semantics_exactly_match_M": m_match,
        "support_signature_pairs_inspected": support_pairs,
        "semantic_ambiguity_kind": ambiguity,
        "all_double_reciprocal_active_trivariate_degrees_annihilated": ambiguity is None and not nonzero,
    }


def _base_result(locks, support_records, support_pairs):
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "predecessor_checkpoint": {
            "reviewed_head": M_REVIEWED_HEAD,
            "merge_commit": M_MERGE_COMMIT,
            "source_blobs": locks,
            "required_terminal": M_REQUIRED_TERMINAL,
            "possible_record_count": M_EXPECTED_RECORDS,
            "tested_record_count": M_EXPECTED_RECORDS,
            "semantic_functional_ambiguity": None,
            "first_cokernel_breaking_direction": None,
            "characterized_blocker": None,
        },
        "boundary_checkpoints": {
            "I": I_REQUIRED_TERMINAL,
            "M": M_REQUIRED_TERMINAL,
        },
        "double_reciprocal_active_trivariate_class": {
            "monomial_domain": "x_c^-r*x_d^-s*x_e^t",
            "degrees": "r,s,t>=1",
            "unordered_pair_order": [list(p) for p in ADMITTED_PAIRS],
            "orientation_order": list(ORIENTATIONS),
            "spectator_is_unshifted": True,
            "reciprocal_active_axes": 2,
            "reciprocal_spectator_admitted": False,
            "complete_overlap_derived_from_exact_signatures": True,
            "support_feasible_seed_required_for_recession": True,
            "arbitrary_degree_cutoff_used": False,
            "t_zero_boundary_matches_protected_I": True,
            "reciprocal_degree_zero_boundaries_match_protected_M": True,
            "third_finite_difference_operator_admitted": False,
        },
        "domain_analysis": {
            "candidate_records_inspected_for_support": support_records,
            "support_signature_pairs_inspected": support_pairs,
            "finite_solver_uses_signature_derived_bounds_only": True,
            "arbitrary_degree_cutoff_used": False,
        },
    }


def build():
    validate_scope()
    solve_signed_tridegrees.cache_clear()
    locks = assert_locks()
    m_result = m.build()
    if m_result.get("terminal") != M_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-N requires exact protected M closure terminal")
    if m_result.get("possible_record_count") != M_EXPECTED_RECORDS or m_result.get("tested_record_count") != M_EXPECTED_RECORDS:
        raise AssertionError("T3-011-N M record-count drift")
    if any(m_result.get(key) is not None for key in (
        "semantic_functional_ambiguity", "first_cokernel_breaking_direction", "characterized_blocker"
    )):
        raise AssertionError("T3-011-N requires clean protected M closure")
    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    try:
        forward_factors = {ch: g.e._coordinate_factors(ch, strata) for ch in CHANNEL_COORDINATE}
        inverse_factors = {ch: h.inverse_coordinate_factors(ch, strata) for ch in CHANNEL_COORDINATE}
    except AssertionError as exc:
        base = _base_result(locks, 0, 0)
        return {
            **base,
            "status": "DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_LAURENT_COKERNEL_AUDIT_BLOCKED",
            "characterized_blocker": {"kind": "COORDINATE_FACTOR_BLOCKER", "detail": str(exc)},
            "possible_record_count": POSSIBLE_RECORD_COUNT,
            "tested_record_count": 0,
            "tested_records": [],
            "semantic_functional_ambiguity": None,
            "first_cokernel_breaking_direction": None,
            "all_double_reciprocal_active_trivariate_responses_cokernel_invisible": False,
            "residual_sum_zero_proved": False,
            "proof_effect": "NONE",
            "promotion_effect": "NONE",
            "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
            "terminal": BLOCKER_TERMINAL,
        }

    witness_indexes = {channel: g._witness_index(bank["witness"]) for channel, bank in banks.items()}
    poly_cache, vector_cache = {}, {}
    records = []
    first_escape = None
    first_ambiguity = None
    first_blocker = None
    support_pairs = 0
    stop = False
    for pair_index, pair in enumerate(ADMITTED_PAIRS):
        for orientation_index, orientation in enumerate(ORIENTATIONS):
            for endpoint_index, endpoint in enumerate(pair):
                bank = banks[endpoint]
                witness_index = witness_indexes[endpoint]
                for candidate_index, uid in enumerate(bank["candidates"]):
                    try:
                        rec = _candidate_record(
                            pair, endpoint, uid, orientation, strata, bank, witness_index,
                            forward_factors, inverse_factors, poly_cache, vector_cache
                        )
                    except UnboundedSupportOverlap as exc:
                        first_blocker = {
                            "kind": "UNBOUNDED_DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_CANCELLATION_RAY",
                            "pair_index": pair_index,
                            "orientation_index": orientation_index,
                            "endpoint_index": endpoint_index,
                            "candidate_index": candidate_index,
                            **exc.evidence,
                        }
                        stop = True
                        break
                    rec.update({
                        "ordinal": len(records),
                        "pair_index": pair_index,
                        "orientation_index": orientation_index,
                        "endpoint_index": endpoint_index,
                        "candidate_index": candidate_index,
                    })
                    records.append(rec)
                    support_pairs += rec["support_signature_pairs_inspected"]
                    if rec["semantic_ambiguity_kind"] is not None:
                        first_ambiguity = rec
                        stop = True
                        break
                    if rec["nonzero_pairings"]:
                        r, s, t, num, den = rec["nonzero_pairings"][0]
                        first_escape = {
                            "ordinal": rec["ordinal"],
                            "pair": rec["pair"],
                            "endpoint": endpoint,
                            "candidate": rec["candidate"],
                            "orientation": orientation,
                            "spectator_axis": rec["spectator_axis"],
                            "tridegree": [r, s, t],
                            "normalized_cokernel_pairing": [num, den],
                        }
                        stop = True
                        break
                if stop:
                    break
            if stop:
                break
        if stop:
            break

    base = _base_result(locks, len(records) + (1 if first_blocker else 0), support_pairs)
    if first_blocker is not None:
        terminal = BLOCKER_TERMINAL
    elif first_ambiguity is not None:
        terminal = AMBIGUITY_TERMINAL
    elif first_escape is not None:
        terminal = ESCAPE_TERMINAL
    else:
        if len(records) != POSSIBLE_RECORD_COUNT:
            raise AssertionError(f"N exhaustive record drift: {len(records)} != {POSSIBLE_RECORD_COUNT}")
        terminal = CLOSURE_TERMINAL

    cache = solve_signed_tridegrees.cache_info()
    return {
        **base,
        "status": "DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_LAURENT_COKERNEL_AUDIT_COMPLETE" if first_blocker is None else "DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_LAURENT_COKERNEL_AUDIT_BLOCKED",
        "execution_ledger": {
            "coordinate_factor_maps": len(forward_factors),
            "inverse_coordinate_factor_maps": len(inverse_factors),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "signed_solver_cache_hits": cache.hits,
            "signed_solver_cache_misses": cache.misses,
        },
        "characterized_blocker": first_blocker,
        "possible_record_count": POSSIBLE_RECORD_COUNT,
        "tested_record_count": len(records),
        "tested_records": records,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "all_double_reciprocal_active_trivariate_responses_cokernel_invisible": terminal == CLOSURE_TERMINAL,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }
