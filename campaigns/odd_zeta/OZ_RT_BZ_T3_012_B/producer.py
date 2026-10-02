from __future__ import annotations

import ast
import hashlib
import json
import sys
import urllib.request
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
T3_010 = HERE.parent / "OZ_RT_BZ_T3_010"
if str(T3_010) not in sys.path:
    sys.path.insert(0, str(T3_010))

import t3_010_c as c  # noqa: E402

ISSUE = 927
STAGE = "T3_012_B_COUPLED_RECOMBINATION_VIABILITY_PROBE"
PROTECTED_BASE = "68826ff58629b59a09a97bbfcff9f560ac518d18"
C_BLOBS = {
    "t3_010_c.py": "c6359f01c12011a22194bfe7ff960aa3e30452d3",
    "T3_010_C_CONTRACT.json": "4f547f29d8bcb734f5e76816c5838d2b095a51b9",
}
EXPECTED_C_RANKS = {
    "n1": (116, 67, 68),
    "n2": (116, 67, 68),
    "n3": (116, 67, 68),
    "k1": (158, 110, 111),
}
QROW_URL = (
    "https://raw.githubusercontent.com/rain-1/-odd-zeta-values-moremath/"
    "968477ed7e406df6542f8da6fbe1cd6ca7273c47/work/lb5/Qrow_rhosigma.m"
)
QROW_BLOB = "61f12f412726887f506e1d423b7ee183a22116e5"
FUNCTIONAL_SAMPLES = ((8, 1, 2), (9, 2, 1))


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=repr).encode("utf-8")
    ).hexdigest()


def assert_source_locks() -> dict[str, str]:
    got: dict[str, str] = {}
    for name, want in C_BLOBS.items():
        value = c.b.a.git_blob_sha1(T3_010 / name)
        if value != want:
            raise AssertionError(f"T3-010-C source lock drift: {name}: {value} != {want}")
        got[name] = value
    c.assert_b_locks()
    c.b.assert_a_locks()
    c.b.a.assert_source_locks()
    c.b.a.validate_architecture()
    return got


def add_scaled(dst: dict, src: dict, factor: Q = Q(1)) -> None:
    if not factor:
        return
    for key, value in src.items():
        z = dst.get(key, Q(0)) + factor * value
        if z:
            dst[key] = z
        elif key in dst:
            del dst[key]


def exact_rank(vectors: list[dict], reverse: bool = False) -> int:
    basis: dict[object, dict] = {}
    keyfn = repr
    for source in vectors:
        v = {k: Q(x) for k, x in source.items() if x}
        while v:
            pivot = (max if reverse else min)(v, key=keyfn)
            if pivot in basis:
                factor = v[pivot]
                add_scaled(v, basis[pivot], -factor)
                continue
            scale = v[pivot]
            v = {k: x / scale for k, x in v.items() if x}
            basis[pivot] = v
            break
    return len(basis)


def _split_cell(cell_id: str) -> tuple[str, str, str]:
    parts = cell_id.split(":", 2)
    if len(parts) != 3:
        raise AssertionError(f"unexpected T3-010-C cell id {cell_id!r}")
    return parts[0], parts[1], parts[2]


def project_vector(vec: dict, mode: str) -> dict:
    out: dict = {}
    for (cell_id, coord), value in vec.items():
        channel, block, stratum = _split_cell(cell_id)
        scalar, mon, sig = coord
        if mode == "erase_partition_only":
            key = (scalar, mon, sig)
        elif mode == "erase_scalar_labels":
            key = (mon, sig)
        elif mode == "erase_rational_coefficient_labels":
            key = (mon,)
        elif mode == "retain_shell_erase_rational_labels":
            key = (stratum, mon)
        else:
            raise ValueError(mode)
        out[key] = out.get(key, Q(0)) + value
        if out[key] == 0:
            del out[key]
    return out


def reconstruct_c_systems():
    layer, predecessor = c.b.a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != c.b.a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 coefficient-layer digest drift in T3-012-B")
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
    systems = {}
    for channel in c.b.a.INDEPENDENT_CHANNELS:
        rec, ids, cols, target = c.build_channel_system(
            channel, primitive_full, strata, specialized, supports
        )
        expected = EXPECTED_C_RANKS[channel]
        got = (rec["unknown_count"], rec["coefficient_rank"], rec["augmented_rank"])
        if got != expected or rec["classification"] != "EXACTLY_INCONSISTENT":
            raise AssertionError(f"protected T3-010-C rank drift in {channel}: {got} != {expected}")
        systems[channel] = (rec, ids, cols, target)
    return systems, primitive_full, supports


def analyze_projection(systems: dict, mode: str) -> dict:
    columns: list[dict] = []
    column_ids: list[tuple] = []
    target: dict = {}
    for channel in c.b.a.INDEPENDENT_CHANNELS:
        _rec, ids, cols, local_target = systems[channel]
        add_scaled(target, project_vector(local_target, mode))
        for uid, col in zip(ids, cols):
            columns.append(project_vector(col, mode))
            column_ids.append((channel, uid[0], uid[1]))
    rank = exact_rank(columns)
    reverse_rank = exact_rank(columns, reverse=True)
    augmented = exact_rank(columns + [target])
    reverse_augmented = exact_rank(columns + [target], reverse=True)
    if rank != reverse_rank or augmented != reverse_augmented:
        raise AssertionError(f"projection rank ordering drift in {mode}")
    return {
        "mode": mode,
        "unknown_count": len(columns),
        "nonzero_column_count": sum(bool(x) for x in columns),
        "target_coordinate_count": len(target),
        "coefficient_rank": rank,
        "augmented_rank": augmented,
        "consistent": rank == augmented,
        "nullity": len(columns) - rank,
        "column_identity_sha256": sha([[ch, scalar, list(mon)] for ch, scalar, mon in column_ids]),
        "target_sha256": sha(sorted((repr(k), v.numerator, v.denominator) for k, v in target.items())),
    }


@dataclass(frozen=True)
class Jet:
    value: Q
    dk: Q = Q(0)
    dl: Q = Q(0)
    dkl: Q = Q(0)

    @staticmethod
    def const(x: int | Q) -> "Jet":
        return Jet(Q(x))

    @staticmethod
    def kvar(x: int | Q) -> "Jet":
        return Jet(Q(x), Q(1), Q(0), Q(0))

    @staticmethod
    def lvar(x: int | Q) -> "Jet":
        return Jet(Q(x), Q(0), Q(1), Q(0))

    def __add__(self, other) -> "Jet":
        other = as_jet(other)
        return Jet(self.value + other.value, self.dk + other.dk, self.dl + other.dl, self.dkl + other.dkl)

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(-self.value, -self.dk, -self.dl, -self.dkl)

    def __sub__(self, other) -> "Jet":
        return self + (-as_jet(other))

    def __rsub__(self, other) -> "Jet":
        return as_jet(other) - self

    def __mul__(self, other) -> "Jet":
        other = as_jet(other)
        return Jet(
            self.value * other.value,
            self.dk * other.value + self.value * other.dk,
            self.dl * other.value + self.value * other.dl,
            self.dkl * other.value + self.dk * other.dl + self.dl * other.dk + self.value * other.dkl,
        )

    __rmul__ = __mul__

    def inverse(self) -> "Jet":
        if not self.value:
            raise ZeroDivisionError("source-functional jet denominator vanished")
        v = self.value
        return Jet(
            Q(1) / v,
            -self.dk / (v * v),
            -self.dl / (v * v),
            2 * self.dk * self.dl / (v * v * v) - self.dkl / (v * v),
        )

    def __truediv__(self, other) -> "Jet":
        return self * as_jet(other).inverse()

    def __rtruediv__(self, other) -> "Jet":
        return as_jet(other) * self.inverse()

    def __pow__(self, exponent: int) -> "Jet":
        if not isinstance(exponent, int):
            raise TypeError("only integer powers are admitted in pinned Q-row source")
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        out = Jet.const(1)
        base = self
        e = exponent
        while e:
            if e & 1:
                out = out * base
            base = base * base
            e >>= 1
        return out


def as_jet(x) -> Jet:
    return x if isinstance(x, Jet) else Jet.const(x)


def _eval_source_ast(node: ast.AST, env: dict[str, Jet]):
    if isinstance(node, ast.List):
        return [_eval_source_ast(x, env) for x in node.elts]
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return Jet.const(node.value)
    if isinstance(node, ast.Name) and node.id in env:
        return env[node.id]
    if isinstance(node, ast.UnaryOp):
        value = _eval_source_ast(node.operand, env)
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Pow):
            if not isinstance(node.right, ast.Constant) or not isinstance(node.right.value, int):
                raise AssertionError("noninteger source exponent")
            return _eval_source_ast(node.left, env) ** node.right.value
        left = _eval_source_ast(node.left, env)
        right = _eval_source_ast(node.right, env)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
    raise AssertionError(f"unsupported pinned Q-row syntax: {ast.dump(node)}")


def load_qrow_ast() -> tuple[list[ast.AST], dict]:
    with urllib.request.urlopen(QROW_URL, timeout=30) as response:
        data = response.read()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if blob != QROW_BLOB or len(data) != 44980:
        raise AssertionError(f"pinned Q-row source identity drift: {blob}/{len(data)}")
    text = data.decode("utf-8").replace("^", "**").replace("{", "[").replace("}", "]")
    parsed = ast.parse(text, mode="eval").body
    if not isinstance(parsed, ast.List) or len(parsed.elts) != 2:
        raise AssertionError("pinned Q-row source is not the expected rho/sigma pair")
    return list(parsed.elts), {"url": QROW_URL, "git_blob_sha1": blob, "byte_count": len(data)}


def rho_sym_jet(nodes: list[ast.AST], n: int, k: int, l: int) -> Jet:
    rho, sigma = nodes
    direct = _eval_source_ast(rho, {"n": Jet.const(n), "k": Jet.kvar(k), "l": Jet.lvar(l)})
    swapped = _eval_source_ast(sigma, {"n": Jet.const(n), "k": Jet.lvar(l), "l": Jet.kvar(k)})
    return (direct + swapped) / 2


def _a0(n: int) -> int:
    return 41218*n**3 + 198849*n**2 + 320790*n + 173057


def _b8(n: int) -> int:
    return (
        3874492*n**8 + 59373972*n**7 + 394148190*n**6 + 1481084196*n**5
        + 3447878810*n**4 + 5095855458*n**3 + 4673546679*n**2
        + 2433871008*n + 551502039
    )


def _b9(n: int) -> int:
    return (
        48802112*n**9 + 967468896*n**8 + 8488000862*n**7 + 43246197636*n**6
        + 140983768422*n**5 + 304912330849*n**4 + 437406946975*n**3
        + 401272692378*n**2 + 213593890911*n + 50257929339
    )


def recurrence_coeff(j: int, n: int) -> Q:
    if j == 0:
        return Q((n + 1)**5 * (n + 2) * _a0(n + 1))
    if j == 1:
        return Q(-2 * (n + 2) * _b8(n))
    if j == 2:
        return Q(-2 * _b9(n))
    if j == 3:
        return Q(2 * (n + 3)**5 * (2*n + 5) * _a0(n))
    raise ValueError(j)


def n_shift_ratio(n: int, k: int, l: int, j: int) -> Q:
    out = Q(1)
    for i in range(1, j + 1):
        out *= Q(
            (n+k+i) * (n+l+i) * (n+k+l+i) * (n+i),
            (n-k+i)**2 * (n-l+i)**2,
        )
    return out


def k_shift_ratio(n: int, k: int, l: int) -> Q:
    return Q((n-k)**2 * (n+k+1) * (n+k+l+1), (k+1)**3 * (k+l+1))


def l_shift_ratio(n: int, k: int, l: int) -> Q:
    return Q((n-l)**2 * (n+l+1) * (n+k+l+1), (l+1)**3 * (k+l+1))


def qrow_point_check(nodes: list[ast.AST], n: int, k: int, l: int) -> bool:
    lhs = recurrence_coeff(0, n)
    for j in (1, 2, 3):
        lhs += recurrence_coeff(j, n) * n_shift_ratio(n, k, l, j)
    rho0 = rho_sym_jet(nodes, n, k, l).value
    rhok = rho_sym_jet(nodes, n, k + 1, l).value
    sigma0 = rho_sym_jet(nodes, n, l, k).value
    sigmal = rho_sym_jet(nodes, n, l + 1, k).value
    rhs = rhok * k_shift_ratio(n, k, l) - rho0 + sigmal * l_shift_ratio(n, k, l) - sigma0
    return lhs == rhs


def scalar_multiplier(nodes: list[ast.AST], scalar: str, n: int, k: int, l: int) -> Q:
    if scalar.startswith("TN"):
        j = int(scalar[-1])
        return recurrence_coeff(j, n) * n_shift_ratio(n, k, l, j)
    if scalar not in {"SK", "AK", "LKK", "LLK"}:
        raise AssertionError(f"unexpected independent scalar {scalar}")
    qk = k_shift_ratio(n, k, l)
    rho = rho_sym_jet(nodes, n, k + 1, l)
    aux = c.b.a.pcl.protected_auxiliary_polynomials()
    lk = c.b.a.pcl.eval_poly_polefree(aux["Lk"], n, k + 1, l)
    ll = c.b.a.pcl.eval_poly_polefree(aux["Ll"], n, k + 1, l)
    doubled = Q(2)
    if scalar == "SK":
        return doubled * (-qk * rho.value)
    if scalar == "LKK":
        return doubled * qk * rho.dk
    if scalar == "LLK":
        return doubled * qk * rho.dl
    return doubled * (-qk * (rho.dkl - rho.dk * ll - rho.dl * lk))


def _eval_rat(rat, n: int, k: int, l: int) -> Q:
    return c.b.a.pcl.rat_eval_polefree(rat, n, k, l)


def source_functional_probe(primitive_full, supports: dict) -> dict:
    nodes, source = load_qrow_ast()
    for point in FUNCTIONAL_SAMPLES:
        n, k, l = point
        if not (0 <= k < n and 0 <= l <= n and k + 1 <= n):
            raise AssertionError(f"functional witness not strictly interior: {point}")
        if not qrow_point_check(nodes, n, k, l):
            raise AssertionError(f"source-functional Q-row point replay failed: {point}")

    ids: list[tuple[str, str, tuple[str, ...]]] = []
    response_polys: list[object] = []
    for channel in c.b.a.INDEPENDENT_CHANNELS:
        for scalar, mon in c.union_support_ids(supports, channel):
            ids.append((channel, scalar, mon))
            response_polys.append(c.b.primitive_delta_monomial(mon, c.b.a.pcl.SHIFTS[channel]))

    columns: list[dict] = [{} for _ in ids]
    target: dict = {}
    for sample_index, (n, k, l) in enumerate(FUNCTIONAL_SAMPLES):
        multipliers = {
            scalar: scalar_multiplier(nodes, scalar, n, k, l)
            for scalar in ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")
        }
        for mon, by_scalar in primitive_full.items():
            total = Q(0)
            for scalar, rat in by_scalar.items():
                if scalar in multipliers:
                    total += multipliers[scalar] * _eval_rat(rat, n, k, l)
            if total:
                target[(sample_index, mon)] = total
        for index, ((_channel, scalar, _support_mon), poly) in enumerate(zip(ids, response_polys)):
            mult = multipliers[scalar]
            if not mult:
                continue
            out = columns[index]
            for mon, rat in poly.items():
                value = mult * _eval_rat(rat, n, k, l)
                if value:
                    out[(sample_index, mon)] = value

    rank = exact_rank(columns)
    reverse_rank = exact_rank(columns, reverse=True)
    augmented = exact_rank(columns + [target])
    reverse_augmented = exact_rank(columns + [target], reverse=True)
    if rank != reverse_rank or augmented != reverse_augmented:
        raise AssertionError("source-functional exact rank ordering drift")
    return {
        "source": source,
        "samples": [list(x) for x in FUNCTIONAL_SAMPLES],
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
        "unknown_identity_sha256": sha([[ch, s, list(mon)] for ch, s, mon in ids]),
        "target_sha256": sha(sorted((repr(k), v.numerator, v.denominator) for k, v in target.items())),
        "interpretation": "Exact finite interior necessary subsystem. Inconsistency refutes a global support-locked degree-zero coupled correction; consistency is viability only and cannot prove an identity.",
    }


def build() -> dict:
    locks = assert_source_locks()
    systems, primitive_full, supports = reconstruct_c_systems()
    modes = [
        "erase_partition_only",
        "erase_scalar_labels",
        "retain_shell_erase_rational_labels",
        "erase_rational_coefficient_labels",
    ]
    probes = [analyze_projection(systems, mode) for mode in modes]
    functional = source_functional_probe(primitive_full, supports)
    return {
        "schema_version": "1.1.0",
        "issue": ISSUE,
        "stage": STAGE,
        "protected_base": PROTECTED_BASE,
        "source_locks": locks,
        "protected_c_channel_ranks": {
            channel: {
                "unknown_count": EXPECTED_C_RANKS[channel][0],
                "coefficient_rank": EXPECTED_C_RANKS[channel][1],
                "augmented_rank": EXPECTED_C_RANKS[channel][2],
            }
            for channel in c.b.a.INDEPENDENT_CHANNELS
        },
        "probe_semantics": {
            "status": "DISCOVERY_ONLY",
            "purpose": "Measure how far the protected C inconsistency survives increasingly permissive linear projections before the exact source-functional calculation.",
            "not_a_functional_recombination_certificate": True,
            "finite_sampling_used": False,
            "exact_Q_linear_algebra": True,
        },
        "probes": probes,
        "producer_source_functional_interior_probe": functional,
        "actual_source_locked_recombination_map_reconstructed": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": "COUPLED_RECOMBINATION_PROJECTION_VIABILITY_PROBE_COMPLETE__EXACT_FUNCTIONAL_MAP_PENDING",
    }
