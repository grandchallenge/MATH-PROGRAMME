from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
import urllib.request
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRED_DIR = HERE.parent / "OZ_RT_BZ_T3_012_B"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pred = _load(PRED_DIR / "producer.py", "oz_t3_012_b_for_013_a")

ISSUE = 949
OPERATION = "OZ-RT-BZ-T3-013-A"
STAGE = "T3_013_A_SOURCE_QROW_CERTIFICATE_WEIGHTED_REDUCED_RESIDUAL_RESPONSE_GATE"
CLASS = "SOURCE_QROW_CERTIFICATE_WEIGHTED_REDUCED_RESIDUAL_RESPONSE_001"
PROTECTED_BASE = "6d760881430b3b587825a3db225f1e6599d1948e"
SOURCE_COMMIT = "6cc0bf07137815ceeef0d9f340559f85352391e5"
QROW_URL = (
    "https://raw.githubusercontent.com/rain-1/-odd-zeta-values-moremath/"
    f"{SOURCE_COMMIT}/work/lb5/Qrow_rhosigma.m"
)
QROW_BLOB = "61f12f412726887f506e1d423b7ee183a22116e5"
QROW_BYTES = 44980
SAMPLES = tuple(pred.FUNCTIONAL_SAMPLES)
COEFFICIENT_BASIS = ("one", "rho", "sigma")
PREDECESSOR_BLOBS = {
    "CONTRACT.json": "9d4dbdd03bd8c21ab2333757dbf85cd0dd5368a5",
    "producer.py": "5682d61997499eccefddc15c6967dc907c091af4",
    "verifier.py": "89d22466513957050e0d3440c801052a6531323d",
}
PREDECESSOR_TERMINAL = "SUPPORT_LOCKED_DEGREE0_COUPLED_CORRECTION_RECOMBINATION_INCOMPATIBLE"
ESCAPE_TERMINAL = "QROW_CERTIFICATE_WEIGHTED_PREDECESSOR_OBSTRUCTION_ESCAPED__GLOBAL_CERTIFICATE_REQUIRED"
NEGATIVE_TERMINAL = "QROW_CERTIFICATE_WEIGHTED_STRICT_INTERIOR_SUBSYSTEM_INCONSISTENT"


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=repr).encode("utf-8")
    ).hexdigest()


def assert_predecessor_locks() -> dict[str, str]:
    got: dict[str, str] = {}
    for name, want in PREDECESSOR_BLOBS.items():
        value = pred.c.b.a.git_blob_sha1(PRED_DIR / name)
        if value != want:
            raise AssertionError(f"T3-012-B lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((PRED_DIR / "CONTRACT.json").read_text())
    if contract.get("issue") != 927 or contract.get("terminal") != PREDECESSOR_TERMINAL:
        raise AssertionError("T3-012-B predecessor identity drift")
    pred.assert_source_locks()
    return got


def load_current_qrow_ast() -> tuple[list[ast.AST], dict]:
    with urllib.request.urlopen(QROW_URL, timeout=30) as response:
        data = response.read()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if blob != QROW_BLOB or len(data) != QROW_BYTES:
        raise AssertionError(f"current admitted Q-row source identity drift: {blob}/{len(data)}")
    text = data.decode("utf-8").replace("^", "**").replace("{", "[").replace("}", "]")
    parsed = ast.parse(text, mode="eval").body
    if not isinstance(parsed, ast.List) or len(parsed.elts) != 2:
        raise AssertionError("current admitted Q-row source is not the expected rho/sigma pair")
    return list(parsed.elts), {
        "repository": "rain-1/-odd-zeta-values-moremath",
        "commit": SOURCE_COMMIT,
        "path": "work/lb5/Qrow_rhosigma.m",
        "git_blob_sha1": blob,
        "byte_count": len(data),
    }


def _contains_source_nonmonomial_denominator(nodes: list[ast.AST]) -> bool:
    for root in nodes:
        for node in ast.walk(root):
            if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)):
                continue
            names = {x.id for x in ast.walk(node.right) if isinstance(x, ast.Name)}
            has_add_sub = any(
                isinstance(x, ast.BinOp) and isinstance(x.op, (ast.Add, ast.Sub))
                for x in ast.walk(node.right)
            )
            if names.intersection({"k", "l"}) and has_add_sub:
                return True
    return False


def source_basis_values(nodes: list[ast.AST], n: int, k: int, l: int) -> dict[str, Q]:
    env = {"n": pred.Jet.const(n), "k": pred.Jet.const(k), "l": pred.Jet.const(l)}
    rho = pred._eval_source_ast(nodes[0], env).value
    sigma = pred._eval_source_ast(nodes[1], env).value
    return {"one": Q(1), "rho": Q(rho), "sigma": Q(sigma)}


def _shift_point(n: int, k: int, l: int, shift: tuple[int, int, int]) -> tuple[int, int, int]:
    dn, dk, dl = shift
    return n + dn, k + dk, l + dl


@lru_cache(maxsize=None)
def _shifted_monomial_poly(mon: tuple[str, ...], shift: tuple[int, int, int]):
    shifted = pred.c.b.a.rc.p_const(1)
    for name in mon:
        shifted = pred.c.b.a.rc.p_mul(shifted, pred.c.b.primitive_shift_atom(name, shift))
    return shifted


def weighted_delta_coefficients(
    nodes: list[ast.AST],
    basis_cache: dict[tuple[int, int, int], dict[str, Q]],
    mon: tuple[str, ...],
    shift: tuple[int, int, int],
    basis: str,
    n: int,
    k: int,
    l: int,
) -> dict[tuple[str, ...], Q]:
    """Evaluate Delta(q*M)=q_shift*M_shift-q*M in the protected atom basis."""
    point = (n, k, l)
    shifted_point = _shift_point(n, k, l, shift)
    if point not in basis_cache:
        basis_cache[point] = source_basis_values(nodes, *point)
    if shifted_point not in basis_cache:
        basis_cache[shifted_point] = source_basis_values(nodes, *shifted_point)
    q0 = basis_cache[point][basis]
    q1 = basis_cache[shifted_point][basis]
    out: dict[tuple[str, ...], Q] = {}
    for shifted_mon, rat in _shifted_monomial_poly(mon, shift).items():
        value = q1 * pred._eval_rat(rat, n, k, l)
        if value:
            out[shifted_mon] = out.get(shifted_mon, Q(0)) + value
    out[mon] = out.get(mon, Q(0)) - q0
    if not out[mon]:
        del out[mon]
    return out


def _base_ids(primitive_full, supports: dict):
    ids: list[tuple[str, str, tuple[str, ...]]] = []
    for channel in pred.c.b.a.INDEPENDENT_CHANNELS:
        for scalar, mon in pred.c.union_support_ids(supports, channel):
            ids.append((channel, scalar, mon))
    if len(ids) != 506:
        raise AssertionError(f"protected support cardinality drift: {len(ids)} != 506")
    return ids


def weighted_source_functional_gate(primitive_full, supports: dict) -> dict:
    nodes, source = load_current_qrow_ast()
    if not _contains_source_nonmonomial_denominator(nodes):
        raise AssertionError("pinned source no longer exhibits nonmonomial rational denominator geometry")
    for point in SAMPLES:
        n, k, l = point
        if not (0 <= k < n and 0 <= l <= n and k + 1 <= n):
            raise AssertionError(f"functional witness not strictly interior: {point}")
        if not pred.qrow_point_check(nodes, n, k, l):
            raise AssertionError(f"current-source Q-row point replay failed: {point}")

    base_ids = _base_ids(primitive_full, supports)
    weighted_ids = [(*row, basis) for row in base_ids for basis in COEFFICIENT_BASIS]
    columns: list[dict] = [{} for _ in weighted_ids]
    target: dict = {}
    basis_cache: dict[tuple[int, int, int], dict[str, Q]] = {}
    scalars = ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")

    for sample_index, (n, k, l) in enumerate(SAMPLES):
        multipliers = {s: pred.scalar_multiplier(nodes, s, n, k, l) for s in scalars}
        for mon, by_scalar in primitive_full.items():
            total = Q(0)
            for scalar, rat in by_scalar.items():
                if scalar in multipliers:
                    total += multipliers[scalar] * pred._eval_rat(rat, n, k, l)
            if total:
                target[(sample_index, mon)] = total

        for base_index, (channel, scalar, support_mon) in enumerate(base_ids):
            mult = multipliers[scalar]
            if not mult:
                continue
            shift = pred.c.b.a.pcl.SHIFTS[channel]
            for basis_index, basis in enumerate(COEFFICIENT_BASIS):
                out = columns[base_index * len(COEFFICIENT_BASIS) + basis_index]
                response = weighted_delta_coefficients(
                    nodes, basis_cache, support_mon, shift, basis, n, k, l
                )
                for mon, coeff in response.items():
                    value = mult * coeff
                    if value:
                        out[(sample_index, mon)] = value

    constant_columns = columns[0::len(COEFFICIENT_BASIS)]
    predecessor_rank = pred.exact_rank(constant_columns)
    predecessor_rank_reverse = pred.exact_rank(constant_columns, reverse=True)
    predecessor_augmented = pred.exact_rank(constant_columns + [target])
    predecessor_augmented_reverse = pred.exact_rank(constant_columns + [target], reverse=True)
    if predecessor_rank != predecessor_rank_reverse or predecessor_augmented != predecessor_augmented_reverse:
        raise AssertionError("embedded T3-012-B rank ordering drift")
    if (predecessor_rank, predecessor_augmented) != (84, 85):
        raise AssertionError(
            f"embedded T3-012-B obstruction drift: {predecessor_rank}/{predecessor_augmented} != 84/85"
        )

    rank = pred.exact_rank(columns)
    reverse_rank = pred.exact_rank(columns, reverse=True)
    augmented = pred.exact_rank(columns + [target])
    reverse_augmented = pred.exact_rank(columns + [target], reverse=True)
    if rank != reverse_rank or augmented != reverse_augmented:
        raise AssertionError("source-weighted exact rank ordering drift")

    consistent = rank == augmented
    return {
        "source": source,
        "coefficient_basis": list(COEFFICIENT_BASIS),
        "coefficient_shift_semantics": "Delta(q*M)=q_shift*M_shift-q*M",
        "source_point_cache_count": len(basis_cache),
        "samples": [list(x) for x in SAMPLES],
        "sample_set_inherited_exactly_from_t3_012_b": True,
        "strict_interior_only": True,
        "shell_regularization_enters_gate": False,
        "qrow_point_replay": True,
        "source_nonmonomial_rational_denominator_detected": True,
        "protected_base_unknown_count": len(base_ids),
        "weighted_unknown_count": len(columns),
        "nonzero_weighted_column_count": sum(bool(x) for x in columns),
        "target_coordinate_count": len(target),
        "embedded_predecessor_coefficient_rank": predecessor_rank,
        "embedded_predecessor_augmented_rank": predecessor_augmented,
        "coefficient_rank": rank,
        "augmented_rank": augmented,
        "consistent": consistent,
        "nullity": len(columns) - rank,
        "unknown_identity_sha256": sha(
            [[ch, scalar, list(mon), basis] for ch, scalar, mon, basis in weighted_ids]
        ),
        "target_sha256": sha(
            sorted((repr(key), value.numerator, value.denominator) for key, value in target.items())
        ),
        "terminal": ESCAPE_TERMINAL if consistent else NEGATIVE_TERMINAL,
        "interpretation": (
            "Exact strict-interior obstruction-escape gate using the true discrete product rule for "
            "source-dependent coefficients. Consistency means only that the protected T3-012-B "
            "necessary-subsystem obstruction is escaped; it is not a global certificate or identity proof."
        ),
    }


def build() -> dict:
    locks = assert_predecessor_locks()
    _systems, primitive_full, supports = pred.reconstruct_c_systems()
    gate = weighted_source_functional_gate(primitive_full, supports)
    return {
        "schema_version": "1.1.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "hypothesis_class": CLASS,
        "protected_base": PROTECTED_BASE,
        "predecessor": {
            "operation": "OZ-RT-BZ-T3-012-B",
            "terminal": PREDECESSOR_TERMINAL,
            "source_locks": locks,
        },
        "non_reducibility": {
            "t3_011_r": {
                "reason": "uses exact nonmonomial rational source-certificate coefficient functions; T3-011-R admits only frozen coordinate-zero Laurent monomial responses and explicitly forbids shifted poles/arbitrary rational functions",
                "mechanical_source_nonmonomial_denominator_check": True,
            },
            "t3_008": {
                "reason": "acts on the protected reduced recurrence-residual correction system, not the original 198-raw-jet two-flux target; coefficient functions are fixed source rho/sigma rather than a free polynomial envelope",
            },
            "t3_012_b": {
                "reason": "changes the coefficient law from constants to the fixed source basis span_Q{1,rho,sigma} while preserving support/harmonics/scalars",
            },
        },
        "gate": gate,
        "terminal": gate["terminal"],
        "global_certificate_constructed": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
