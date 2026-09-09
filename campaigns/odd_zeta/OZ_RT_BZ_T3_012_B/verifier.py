from __future__ import annotations

import ast
import hashlib
import sys
import urllib.request
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
T3_010 = HERE.parent / "OZ_RT_BZ_T3_010"
if str(T3_010) not in sys.path:
    sys.path.insert(0, str(T3_010))

import t3_010_c as c  # noqa: E402

MODES = (
    "erase_partition_only",
    "erase_scalar_labels",
    "retain_shell_erase_rational_labels",
    "erase_rational_coefficient_labels",
)
QROW_URL = (
    "https://raw.githubusercontent.com/rain-1/-odd-zeta-values-moremath/"
    "968477ed7e406df6542f8da6fbe1cd6ca7273c47/work/lb5/Qrow_rhosigma.m"
)
QROW_BLOB = "61f12f412726887f506e1d423b7ee183a22116e5"
SAMPLES = ((8, 1, 2), (9, 2, 1))


def add(dst: dict, key: object, value: Q) -> None:
    z = dst.get(key, Q(0)) + value
    if z:
        dst[key] = z
    elif key in dst:
        del dst[key]


def projected_key(mode: str, stratum: str, coord) -> tuple:
    scalar, mon, sig = coord
    if mode == "erase_partition_only":
        return scalar, mon, sig
    if mode == "erase_scalar_labels":
        return mon, sig
    if mode == "retain_shell_erase_rational_labels":
        return stratum, mon
    if mode == "erase_rational_coefficient_labels":
        return (mon,)
    raise ValueError(mode)


def rank_reverse(vectors: list[dict]) -> int:
    basis: dict[object, dict] = {}
    for source in reversed(vectors):
        v = {k: Q(x) for k, x in source.items() if x}
        while v:
            pivot = max(v, key=repr)
            if pivot in basis:
                factor = v[pivot]
                for key, coeff in basis[pivot].items():
                    add(v, key, -factor * coeff)
                continue
            scale = v[pivot]
            basis[pivot] = {k: x / scale for k, x in v.items() if x}
            break
    return len(basis)


def reconstruct_projection(mode: str) -> dict:
    c.assert_b_locks()
    c.b.assert_a_locks()
    c.b.a.assert_source_locks()
    c.b.a.validate_architecture()
    layer, predecessor = c.b.a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != c.b.a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 layer drift in T3-012-B verifier")
    primitive_full = c.b.a.primitive_oriented_layer(layer)
    strata = c.b.a.shell_strata()
    specialized = {
        st["id"]: c.b.a.primitive_oriented_layer(
            c.b.a.specialize_layer(layer, st["k_offset"], st["l_offset"])
        )
        for st in strata
    }
    supports = {
        (channel, block): c.b.candidate_support(primitive_full, channel, block)
        for channel in c.b.a.CHANNEL_SCALARS
        for block in c.BLOCK_ORDER
    }

    target: dict = {}
    columns: list[dict] = []
    channel_offsets: dict[str, int] = {}
    channel_ids: dict[str, list] = {}
    for channel in c.b.a.INDEPENDENT_CHANNELS:
        ids = c.union_support_ids(supports, channel)
        channel_offsets[channel] = len(columns)
        channel_ids[channel] = ids
        columns.extend({} for _ in ids)

    for st in reversed(strata):
        primitive = specialized[st["id"]]
        for channel in reversed(c.b.a.INDEPENDENT_CHANNELS):
            ids = channel_ids[channel]
            pos = {uid: channel_offsets[channel] + i for i, uid in enumerate(ids)}
            for block in reversed(c.BLOCK_ORDER):
                rec, local_target, local_cols, local_ids = c.b.analyze_cell(
                    primitive, supports[(channel, block)], channel, block, st
                )
                if rec["classification"] == "STRUCTURAL_ZERO":
                    continue
                for coord, value in local_target.items():
                    add(target, projected_key(mode, st["id"], coord), value)
                for uid, local_col in zip(local_ids, local_cols):
                    out = columns[pos[uid]]
                    for coord, value in local_col.items():
                        add(out, projected_key(mode, st["id"], coord), value)

    rank = rank_reverse(columns)
    augmented = rank_reverse(columns + [target])
    return {
        "mode": mode,
        "unknown_count": len(columns),
        "nonzero_column_count": sum(bool(x) for x in columns),
        "target_coordinate_count": len(target),
        "coefficient_rank": rank,
        "augmented_rank": augmented,
        "consistent": rank == augmented,
    }


# Independent source evaluator.  A Taylor object is a truncated bivariate
# polynomial in formal eps_k, eps_l; unlike the producer's derivative-tuple Jet,
# multiplication/inversion are implemented by coefficient convolution.
Taylor = dict[tuple[int, int], Q]


def t_const(x: int | Q) -> Taylor:
    return {(0, 0): Q(x)} if x else {}


def t_var(value: int | Q, axis: int) -> Taylor:
    out = {(0, 0): Q(value)}
    out[(1, 0) if axis == 0 else (0, 1)] = Q(1)
    return out


def t_add(a: Taylor, b: Taylor, scale: Q = Q(1)) -> Taylor:
    out = dict(a)
    for key, value in b.items():
        add(out, key, scale * value)
    return out


def t_mul(a: Taylor, b: Taylor) -> Taylor:
    out: Taylor = {}
    for (i, j), x in a.items():
        for (r, s), y in b.items():
            if i + r <= 1 and j + s <= 1:
                add(out, (i + r, j + s), x * y)
    return out


def t_inv(a: Taylor) -> Taylor:
    a00 = a.get((0, 0), Q(0))
    if not a00:
        raise ZeroDivisionError("independent Q-row Taylor denominator vanished")
    # Solve a*b=1 coefficient by coefficient in the truncated ring.
    b00 = Q(1) / a00
    b10 = -a.get((1, 0), Q(0)) * b00 / a00
    b01 = -a.get((0, 1), Q(0)) * b00 / a00
    mixed_known = (
        a.get((1, 0), Q(0)) * b01
        + a.get((0, 1), Q(0)) * b10
        + a.get((1, 1), Q(0)) * b00
    )
    b11 = -mixed_known / a00
    return {k: v for k, v in {
        (0, 0): b00, (1, 0): b10, (0, 1): b01, (1, 1): b11
    }.items() if v}


def t_pow(a: Taylor, exponent: int) -> Taylor:
    if exponent < 0:
        return t_pow(t_inv(a), -exponent)
    out = t_const(1)
    base = a
    e = exponent
    while e:
        if e & 1:
            out = t_mul(out, base)
        base = t_mul(base, base)
        e >>= 1
    return out


def _src_eval(node: ast.AST, env: dict[str, Taylor]):
    if isinstance(node, ast.List):
        return [_src_eval(x, env) for x in node.elts]
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return t_const(node.value)
    if isinstance(node, ast.Name) and node.id in env:
        return env[node.id]
    if isinstance(node, ast.UnaryOp):
        value = _src_eval(node.operand, env)
        if isinstance(node.op, ast.USub):
            return t_add({}, value, Q(-1))
        if isinstance(node.op, ast.UAdd):
            return value
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Pow):
            if not isinstance(node.right, ast.Constant) or not isinstance(node.right.value, int):
                raise AssertionError("independent parser saw noninteger exponent")
            return t_pow(_src_eval(node.left, env), node.right.value)
        left = _src_eval(node.left, env)
        right = _src_eval(node.right, env)
        if isinstance(node.op, ast.Add):
            return t_add(left, right)
        if isinstance(node.op, ast.Sub):
            return t_add(left, right, Q(-1))
        if isinstance(node.op, ast.Mult):
            return t_mul(left, right)
        if isinstance(node.op, ast.Div):
            return t_mul(left, t_inv(right))
    raise AssertionError(f"unsupported independent Q-row syntax: {ast.dump(node)}")


def _load_source() -> tuple[list[ast.AST], dict]:
    with urllib.request.urlopen(QROW_URL, timeout=30) as response:
        data = response.read()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if blob != QROW_BLOB or len(data) != 44980:
        raise AssertionError("independent Q-row source identity drift")
    text = data.decode("utf-8").translate(str.maketrans({"^": "^", "{": "[", "}": "]"}))
    text = text.replace("^", "**")
    parsed = ast.parse(text, mode="eval").body
    if not isinstance(parsed, ast.List) or len(parsed.elts) != 2:
        raise AssertionError("independent Q-row parser shape drift")
    return list(parsed.elts), {"git_blob_sha1": blob, "byte_count": len(data)}


def _rho_sym(nodes: list[ast.AST], n: int, k: int, l: int) -> Taylor:
    rho, sigma = nodes
    direct = _src_eval(rho, {"n": t_const(n), "k": t_var(k, 0), "l": t_var(l, 1)})
    swapped = _src_eval(sigma, {"n": t_const(n), "k": t_var(l, 1), "l": t_var(k, 0)})
    return {key: value / 2 for key, value in t_add(direct, swapped).items()}


def _a0(n: int) -> int:
    return 41218*n**3 + 198849*n**2 + 320790*n + 173057


def _b8(n: int) -> int:
    return (3874492*n**8 + 59373972*n**7 + 394148190*n**6 + 1481084196*n**5
            + 3447878810*n**4 + 5095855458*n**3 + 4673546679*n**2
            + 2433871008*n + 551502039)


def _b9(n: int) -> int:
    return (48802112*n**9 + 967468896*n**8 + 8488000862*n**7 + 43246197636*n**6
            + 140983768422*n**5 + 304912330849*n**4 + 437406946975*n**3
            + 401272692378*n**2 + 213593890911*n + 50257929339)


def _cj(j: int, n: int) -> Q:
    if j == 0:
        return Q((n + 1)**5 * (n + 2) * _a0(n + 1))
    if j == 1:
        return Q(-2 * (n + 2) * _b8(n))
    if j == 2:
        return Q(-2 * _b9(n))
    if j == 3:
        return Q(2 * (n + 3)**5 * (2*n + 5) * _a0(n))
    raise ValueError(j)


def _nr(n: int, k: int, l: int, j: int) -> Q:
    out = Q(1)
    for i in range(1, j + 1):
        out *= Q((n+k+i)*(n+l+i)*(n+k+l+i)*(n+i), (n-k+i)**2*(n-l+i)**2)
    return out


def _kr(n: int, k: int, l: int) -> Q:
    return Q((n-k)**2*(n+k+1)*(n+k+l+1), (k+1)**3*(k+l+1))


def _lr(n: int, k: int, l: int) -> Q:
    return Q((n-l)**2*(n+l+1)*(n+k+l+1), (l+1)**3*(k+l+1))


def _qrow_check(nodes: list[ast.AST], n: int, k: int, l: int) -> bool:
    lhs = _cj(0, n) + sum((_cj(j, n) * _nr(n, k, l, j) for j in (1, 2, 3)), Q(0))
    r0 = _rho_sym(nodes, n, k, l).get((0, 0), Q(0))
    rk = _rho_sym(nodes, n, k + 1, l).get((0, 0), Q(0))
    s0 = _rho_sym(nodes, n, l, k).get((0, 0), Q(0))
    sl = _rho_sym(nodes, n, l + 1, k).get((0, 0), Q(0))
    return lhs == rk * _kr(n, k, l) - r0 + sl * _lr(n, k, l) - s0


def _mult(nodes: list[ast.AST], scalar: str, n: int, k: int, l: int) -> Q:
    if scalar.startswith("TN"):
        j = int(scalar[-1])
        return _cj(j, n) * _nr(n, k, l, j)
    rho = _rho_sym(nodes, n, k + 1, l)
    qk = _kr(n, k, l)
    aux = c.b.a.pcl.protected_auxiliary_polynomials()
    lk = c.b.a.pcl.eval_poly_polefree(aux["Lk"], n, k + 1, l)
    ll = c.b.a.pcl.eval_poly_polefree(aux["Ll"], n, k + 1, l)
    v = rho.get((0, 0), Q(0))
    dk = rho.get((1, 0), Q(0))
    dl = rho.get((0, 1), Q(0))
    dkl = rho.get((1, 1), Q(0))
    if scalar == "SK":
        return -2 * qk * v
    if scalar == "LKK":
        return 2 * qk * dk
    if scalar == "LLK":
        return 2 * qk * dl
    if scalar == "AK":
        return -2 * qk * (dkl - dk * ll - dl * lk)
    raise AssertionError(f"independent source-functional scalar drift: {scalar}")


def reconstruct_source_functional() -> dict:
    c.assert_b_locks()
    c.b.assert_a_locks()
    c.b.a.assert_source_locks()
    c.b.a.validate_architecture()
    layer, predecessor = c.b.a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != c.b.a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 layer drift in source-functional verifier")
    primitive = c.b.a.primitive_oriented_layer(layer)
    supports = {
        (channel, block): c.b.candidate_support(primitive, channel, block)
        for channel in c.b.a.CHANNEL_SCALARS for block in c.BLOCK_ORDER
    }
    nodes, source = _load_source()
    for n, k, l in SAMPLES:
        if not (0 <= k < n and 0 <= l <= n and k + 1 <= n):
            raise AssertionError("source-functional witness left strict interior")
        if not _qrow_check(nodes, n, k, l):
            raise AssertionError("independent source-functional Q-row replay failed")

    ids: list[tuple[str, str, tuple[str, ...]]] = []
    polynomials = []
    for channel in c.b.a.INDEPENDENT_CHANNELS:
        for scalar, mon in c.union_support_ids(supports, channel):
            ids.append((channel, scalar, mon))
            polynomials.append(c.b.primitive_delta_monomial(mon, c.b.a.pcl.SHIFTS[channel]))
    columns: list[dict] = [{} for _ in ids]
    target: dict = {}
    scalars = ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")
    for sample_index, (n, k, l) in enumerate(SAMPLES):
        multipliers = {s: _mult(nodes, s, n, k, l) for s in scalars}
        for mon, by_scalar in primitive.items():
            value = Q(0)
            for scalar, rat in by_scalar.items():
                if scalar in multipliers:
                    value += multipliers[scalar] * c.b.a.pcl.rat_eval_polefree(rat, n, k, l)
            if value:
                target[(sample_index, mon)] = value
        for index in reversed(range(len(ids))):
            _channel, scalar, _support_mon = ids[index]
            mult = multipliers[scalar]
            if not mult:
                continue
            out = columns[index]
            for mon, rat in polynomials[index].items():
                value = mult * c.b.a.pcl.rat_eval_polefree(rat, n, k, l)
                if value:
                    out[(sample_index, mon)] = value

    rank = rank_reverse(columns)
    augmented = rank_reverse(columns + [target])
    return {
        "source": source,
        "samples": [list(x) for x in SAMPLES],
        "strict_interior_only": True,
        "shell_regularization_enters_witness": False,
        "qrow_point_replay": True,
        "one_orientation_spatial_multiplier": 2,
        "unknown_count": len(columns),
        "nonzero_column_count": sum(bool(x) for x in columns),
        "target_coordinate_count": len(target),
        "coefficient_rank": rank,
        "augmented_rank": augmented,
        "consistent": rank == augmented,
        "nullity": len(columns) - rank,
    }


def verify(result: dict) -> dict:
    if result.get("issue") != 927 or result.get("stage") != "T3_012_B_COUPLED_RECOMBINATION_VIABILITY_PROBE":
        raise AssertionError("T3-012-B result identity drift")
    if result.get("actual_source_locked_recombination_map_reconstructed"):
        raise AssertionError("probe inflated to exact functional map")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-012-B probe promoted")
    expected = {row["mode"]: row for row in result["probes"]}
    replay = []
    for mode in MODES:
        got = reconstruct_projection(mode)
        row = expected[mode]
        for field in (
            "unknown_count", "nonzero_column_count", "target_coordinate_count",
            "coefficient_rank", "augmented_rank", "consistent",
        ):
            if got[field] != row[field]:
                raise AssertionError(f"T3-012-B independent replay drift {mode}:{field}")
        replay.append(got)

    source_replay = reconstruct_source_functional()
    source_expected = result["producer_source_functional_interior_probe"]
    for field in (
        "samples", "strict_interior_only", "shell_regularization_enters_witness",
        "qrow_point_replay", "one_orientation_spatial_multiplier", "unknown_count",
        "nonzero_column_count", "target_coordinate_count", "coefficient_rank",
        "augmented_rank", "consistent", "nullity",
    ):
        if source_replay[field] != source_expected[field]:
            raise AssertionError(f"T3-012-B source-functional independent replay drift: {field}")
    if source_replay["source"]["git_blob_sha1"] != source_expected["source"]["git_blob_sha1"]:
        raise AssertionError("T3-012-B source-functional source lock mismatch")

    return {
        "terminal": result["terminal"],
        "independent_projection_replay_complete": True,
        "independent_source_functional_replay_complete": True,
        "producer_projected_matrices_imported_as_authority": False,
        "producer_source_jets_imported_as_authority": False,
        "probes": replay,
        "source_functional_interior": source_replay,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
    }
