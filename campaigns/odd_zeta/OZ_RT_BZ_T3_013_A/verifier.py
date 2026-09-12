from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
import urllib.request
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRED_DIR = HERE.parent / "OZ_RT_BZ_T3_012_B"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected verifier dependency: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


v = _load(PRED_DIR / "verifier.py", "oz_t3_012_b_verifier_for_013_a")

ISSUE = 949
OPERATION = "OZ-RT-BZ-T3-013-A"
STAGE = "T3_013_A_SOURCE_QROW_CERTIFICATE_WEIGHTED_REDUCED_RESIDUAL_RESPONSE_GATE"
SOURCE_COMMIT = "6cc0bf07137815ceeef0d9f340559f85352391e5"
QROW_URL = (
    "https://raw.githubusercontent.com/rain-1/-odd-zeta-values-moremath/"
    f"{SOURCE_COMMIT}/work/lb5/Qrow_rhosigma.m"
)
QROW_BLOB = "61f12f412726887f506e1d423b7ee183a22116e5"
QROW_BYTES = 44980
SAMPLES = ((8, 1, 2), (9, 2, 1))
BASIS = ("one", "rho", "sigma")


def _load_source() -> tuple[list[ast.AST], dict]:
    with urllib.request.urlopen(QROW_URL, timeout=30) as response:
        data = response.read()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if blob != QROW_BLOB or len(data) != QROW_BYTES:
        raise AssertionError("independent current-source Q-row identity drift")
    text = data.decode("utf-8").replace("^", "**").replace("{", "[").replace("}", "]")
    parsed = ast.parse(text, mode="eval").body
    if not isinstance(parsed, ast.List) or len(parsed.elts) != 2:
        raise AssertionError("independent current-source parser shape drift")
    return list(parsed.elts), {
        "repository": "rain-1/-odd-zeta-values-moremath",
        "commit": SOURCE_COMMIT,
        "path": "work/lb5/Qrow_rhosigma.m",
        "git_blob_sha1": blob,
        "byte_count": len(data),
    }


def _basis_values(nodes: list[ast.AST], n: int, k: int, l: int) -> dict[str, Q]:
    env = {
        "n": v.t_const(n),
        "k": v.t_var(k, 0),
        "l": v.t_var(l, 1),
    }
    rho = v._src_eval(nodes[0], env).get((0, 0), Q(0))
    sigma = v._src_eval(nodes[1], env).get((0, 0), Q(0))
    return {"one": Q(1), "rho": rho, "sigma": sigma}


def reconstruct() -> dict:
    v.c.assert_b_locks()
    v.c.b.assert_a_locks()
    v.c.b.a.assert_source_locks()
    v.c.b.a.validate_architecture()
    layer, predecessor = v.c.b.a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != v.c.b.a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 layer drift in T3-013-A verifier")
    primitive = v.c.b.a.primitive_oriented_layer(layer)
    supports = {
        (channel, block): v.c.b.candidate_support(primitive, channel, block)
        for channel in v.c.b.a.CHANNEL_SCALARS
        for block in v.c.BLOCK_ORDER
    }
    nodes, source = _load_source()
    for n, k, l in SAMPLES:
        if not (0 <= k < n and 0 <= l <= n and k + 1 <= n):
            raise AssertionError("T3-013-A witness left strict interior")
        if not v._qrow_check(nodes, n, k, l):
            raise AssertionError("independent current-source Q-row replay failed")

    base_ids: list[tuple[str, str, tuple[str, ...]]] = []
    polynomials = []
    for channel in v.c.b.a.INDEPENDENT_CHANNELS:
        for scalar, mon in v.c.union_support_ids(supports, channel):
            base_ids.append((channel, scalar, mon))
            polynomials.append(v.c.b.primitive_delta_monomial(mon, v.c.b.a.pcl.SHIFTS[channel]))
    if len(base_ids) != 506:
        raise AssertionError("independent protected support cardinality drift")

    columns: list[dict] = [{} for _ in range(len(base_ids) * len(BASIS))]
    target: dict = {}
    scalars = ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")
    for sample_index, (n, k, l) in enumerate(SAMPLES):
        multipliers = {s: v._mult(nodes, s, n, k, l) for s in scalars}
        weights = _basis_values(nodes, n, k, l)
        for mon, by_scalar in primitive.items():
            value = Q(0)
            for scalar, rat in by_scalar.items():
                if scalar in multipliers:
                    value += multipliers[scalar] * v.c.b.a.pcl.rat_eval_polefree(rat, n, k, l)
            if value:
                target[(sample_index, mon)] = value
        for base_index in reversed(range(len(base_ids))):
            _channel, scalar, _support_mon = base_ids[base_index]
            mult = multipliers[scalar]
            if not mult:
                continue
            for basis_index, basis in enumerate(reversed(BASIS)):
                actual_basis_index = BASIS.index(basis)
                weight = weights[basis]
                if not weight:
                    continue
                out = columns[base_index * len(BASIS) + actual_basis_index]
                for mon, rat in polynomials[base_index].items():
                    value = weight * mult * v.c.b.a.pcl.rat_eval_polefree(rat, n, k, l)
                    if value:
                        out[(sample_index, mon)] = value

    constant_columns = columns[0::len(BASIS)]
    predecessor_rank = v.rank_reverse(constant_columns)
    predecessor_augmented = v.rank_reverse(constant_columns + [target])
    if (predecessor_rank, predecessor_augmented) != (84, 85):
        raise AssertionError("independent embedded T3-012-B obstruction drift")

    rank = v.rank_reverse(columns)
    augmented = v.rank_reverse(columns + [target])
    return {
        "source": source,
        "coefficient_basis": list(BASIS),
        "samples": [list(x) for x in SAMPLES],
        "strict_interior_only": True,
        "qrow_point_replay": True,
        "protected_base_unknown_count": len(base_ids),
        "weighted_unknown_count": len(columns),
        "nonzero_weighted_column_count": sum(bool(x) for x in columns),
        "target_coordinate_count": len(target),
        "embedded_predecessor_coefficient_rank": predecessor_rank,
        "embedded_predecessor_augmented_rank": predecessor_augmented,
        "coefficient_rank": rank,
        "augmented_rank": augmented,
        "consistent": rank == augmented,
        "nullity": len(columns) - rank,
    }


def verify(result: dict) -> dict:
    if result.get("issue") != ISSUE or result.get("operation") != OPERATION or result.get("stage") != STAGE:
        raise AssertionError("T3-013-A result identity drift")
    if result.get("global_certificate_constructed"):
        raise AssertionError("T3-013-A gate inflated to global certificate")
    if result.get("residual_sum_zero_proved"):
        raise AssertionError("T3-013-A gate inflated to residual proof")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-013-A gate promoted claims")
    expected = result["gate"]
    got = reconstruct()
    for field in (
        "coefficient_basis", "samples", "strict_interior_only", "qrow_point_replay",
        "protected_base_unknown_count", "weighted_unknown_count", "nonzero_weighted_column_count",
        "target_coordinate_count", "embedded_predecessor_coefficient_rank",
        "embedded_predecessor_augmented_rank", "coefficient_rank", "augmented_rank",
        "consistent", "nullity",
    ):
        if got[field] != expected[field]:
            raise AssertionError(f"T3-013-A independent replay drift: {field}")
    if got["source"] != expected["source"]:
        raise AssertionError("T3-013-A independent source lock mismatch")
    return {
        "terminal": result["terminal"],
        "independent_source_weighted_replay_complete": True,
        "producer_weighted_matrix_imported_as_authority": False,
        "producer_source_evaluator_imported_as_authority": False,
        "gate": got,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
    }
