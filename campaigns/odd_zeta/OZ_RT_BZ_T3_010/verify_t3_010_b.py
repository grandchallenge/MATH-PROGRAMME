#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_010_a as a  # noqa: E402

STAGE = "T3_010_B_CORRECTION_FLUX_EXACT_COEFFICIENT_MATRIX_RANK_CONSISTENCY_GATE"
BLOCK_ORDER = ("weight1", "weight2", "weight3", "weight4")
A_HEAD = "78186e06e3291b7b85d4d78e3a44218890f07dd9"
A_BLOBS = {
    "t3_010_a.py": "d5cdcecb4d0bbdd3e6b71f1df4340928e8ad402e",
    "T3_010_A_CONTRACT.json": "28f6617bca38a96eee3bbc9517874cd6fd07bb14",
}


def sha(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def touches(mon: tuple[str, ...], block: str) -> bool:
    reps = set(a.WEIGHT_BLOCKS[block])
    return any(a.ORBIT_REP[x] in reps for x in mon)


def cp(rat: a.rc.Rat) -> a.rc.Poly:
    return {(): rat} if rat else {}


def delta_atom(name: str, shift: tuple[int, int, int]) -> a.rc.Poly:
    dn, dk, dl = shift
    if sum(int(x != 0) for x in shift) != 1:
        raise ValueError(shift)
    r = int(name.rsplit("_", 1)[1])
    if name.startswith("H_nmk_"):
        if dn: return cp(a.pcl.sum_pinv([a.rc.lin_nmink(i) for i in range(1, dn + 1)], r))
        if dk: return cp(a.rc.r_scale(a.pcl.pinv_factor(a.rc.lin_nmink(0), r), -1))
        return {}
    if name.startswith("H_nml_"):
        if dn: return cp(a.pcl.sum_pinv([a.rc.lin_nminl(i) for i in range(1, dn + 1)], r))
        if dl: return cp(a.rc.r_scale(a.pcl.pinv_factor(a.rc.lin_nminl(0), r), -1))
        return {}
    families = (
        ("H_nkl_", a.rc.lin_nkl, (True, True, True)),
        ("H_nk_", a.rc.lin_nk, (True, True, False)),
        ("H_nl_", a.rc.lin_nl, (True, False, True)),
        ("H_kl_", a.rc.lin_kl, (False, True, True)),
        ("H_k_", a.rc.lin_k, (False, True, False)),
        ("H_l_", a.rc.lin_l, (False, False, True)),
    )
    for prefix, form, axes in families:
        if not name.startswith(prefix):
            continue
        n_ok, k_ok, l_ok = axes
        if dn and n_ok:
            return cp(a.rc.sum_inv([form(i) for i in range(1, dn + 1)], r))
        if dk and k_ok:
            return cp(a.rc.inv(form(1), r))
        if dl and l_ok:
            return cp(a.rc.inv(form(1), r))
        return {}
    raise ValueError(name)


def delta_mon(mon: tuple[str, ...], shift: tuple[int, int, int]) -> a.rc.Poly:
    s = a.rc.p_const(1)
    o = a.rc.p_const(1)
    for name in mon:
        s = a.rc.p_mul(s, a.rc.p_add(a.rc.p_atom(name), delta_atom(name, shift)))
        o = a.rc.p_mul(o, a.rc.p_atom(name))
    return a.rc.p_add(s, a.rc.p_scale(o, -1))


def sp(poly: a.rc.Poly, ko: int | None, lo: int | None) -> a.rc.Poly:
    out: a.rc.Poly = {}
    for mon, rat in poly.items():
        x = a.specialize_rat(rat, ko, lo)
        if x:
            out[mon] = x
    return out


Coord = tuple[str, tuple[str, ...], a.rc.Sig]
Vector = dict[Coord, Q]


def ckey(c: Coord) -> str:
    return repr(c)


def fjson(factor: tuple[int, ...]) -> list[int]:
    return [int(x) for x in factor]


def cjson(c: Coord):
    scalar, mon, sig = c
    return [scalar, list(mon), [[fjson(f), int(e)] for f, e in sig]]


def vd(v: Vector) -> str:
    rows = []
    for coord in sorted(v, key=ckey):
        q = v[coord]
        rows.append([cjson(coord), q.numerator, q.denominator])
    return sha(rows)


def cbd(ids: list[tuple[str, tuple[str, ...]]], cols: list[Vector]) -> str:
    return sha([[s, list(m), vd(v)] for (s, m), v in zip(ids, cols)])


def target_vector(layer: a.pcl.Layer, channel: str, block: str) -> Vector:
    out: Vector = {}
    allowed = set(a.CHANNEL_SCALARS[channel])
    for mon, terms in layer.items():
        if not touches(mon, block):
            continue
        for scalar, rat in terms.items():
            if scalar not in allowed:
                continue
            for sig, q in rat.items():
                c = (scalar, mon, sig)
                out[c] = out.get(c, Q(0)) + q
                if out[c] == 0:
                    del out[c]
    return out


def response(poly: a.rc.Poly, scalar: str, block: str) -> Vector:
    out: Vector = {}
    for mon, rat in poly.items():
        if not touches(mon, block):
            continue
        for sig, q in rat.items():
            c = (scalar, mon, sig)
            out[c] = out.get(c, Q(0)) + q
            if out[c] == 0:
                del out[c]
    return out


def support(primitive: a.pcl.Layer, channel: str, block: str):
    return {
        scalar: sorted({mon for mon, terms in primitive.items() if scalar in terms and touches(mon, block)})
        for scalar in a.CHANNEL_SCALARS[channel]
    }


def rank_reverse(vectors: list[Vector]) -> int:
    """Independent exact rank path: largest-coordinate pivots, reversed vectors."""
    basis: dict[Coord, Vector] = {}
    for source in reversed(vectors):
        v = {k: Q(q) for k, q in source.items() if q}
        while v:
            p = max(v, key=ckey)
            if p in basis:
                f = v[p]
                for k, q in basis[p].items():
                    z = v.get(k, Q(0)) - f * q
                    if z:
                        v[k] = z
                    elif k in v:
                        del v[k]
                continue
            z = v[p]
            basis[p] = {k: q / z for k, q in v.items() if q}
            break
    return len(basis)


def classification(r: int, ra: int, u: int) -> str:
    if ra > r:
        return "EXACTLY_INCONSISTENT"
    return "CONSISTENT_UNIQUE" if r == u else "CONSISTENT_AFFINE"


def cell(primitive_sp: a.pcl.Layer, sup, channel: str, block: str, st: dict):
    target = target_vector(primitive_sp, channel, block)
    if not target:
        return {
            "classification": "STRUCTURAL_ZERO", "unknowns": 0, "coefficient_rank": 0,
            "augmented_rank": 0, "nullity": 0, "target_coordinate_count": 0,
            "matrix_coordinate_count": 0, "zero_response_columns": 0,
            "candidate_support_sha256": sha([]), "coefficient_matrix_sha256": sha([]),
            "target_sha256": vd({}),
        }, target, [], []
    cols: list[Vector] = []
    ids: list[tuple[str, tuple[str, ...]]] = []
    support_rows = []
    for scalar in a.CHANNEL_SCALARS[channel]:
        for mon in sup[scalar]:
            p = sp(delta_mon(mon, a.pcl.SHIFTS[channel]), st["k_offset"], st["l_offset"])
            cols.append(response(p, scalar, block))
            ids.append((scalar, mon))
            support_rows.append([scalar, list(mon)])
    r = rank_reverse(cols)
    ra = rank_reverse(cols + [target])
    coords = set(target)
    for x in cols:
        coords.update(x)
    u = len(cols)
    return {
        "classification": classification(r, ra, u), "unknowns": u,
        "coefficient_rank": r, "augmented_rank": ra, "nullity": u-r,
        "target_coordinate_count": len(target), "matrix_coordinate_count": len(coords),
        "zero_response_columns": sum(not x for x in cols),
        "candidate_support_sha256": sha(support_rows),
        "coefficient_matrix_sha256": cbd(ids, cols), "target_sha256": vd(target),
    }, target, cols, ids


def mletter(name: str) -> str:
    for x, y in (("H_nmk_", "H_nml_"), ("H_nml_", "H_nmk_"),
                 ("H_nk_", "H_nl_"), ("H_nl_", "H_nk_"),
                 ("H_k_", "H_l_"), ("H_l_", "H_k_")):
        if name.startswith(x):
            return y + name[len(x):]
    return name


def msig(sig: a.rc.Sig) -> a.rc.Sig:
    d: dict[tuple[int, ...], int] = {}
    for f, e in sig:
        if len(f) == 5 and f[0] == a.pcl.PINV_TAG:
            tag, aa, b, c, z = f
            mf = (tag, aa, c, b, z)
        else:
            aa, b, c, z = f
            mf = (aa, c, b, z)
        d[mf] = d.get(mf, 0) + e
        if d[mf] == 0:
            del d[mf]
    return tuple(sorted(d.items()))


def mirror_vec(v: Vector) -> Vector:
    inv = {v: k for k, v in a.MIRROR_SCALAR.items()}
    out: Vector = {}
    for (scalar, mon, sig), q in v.items():
        c = (inv[scalar], tuple(sorted(mletter(x) for x in mon)), msig(sig))
        out[c] = out.get(c, Q(0)) + q
        if out[c] == 0:
            del out[c]
    return out


def mirror_id(cid):
    inv = {v: k for k, v in a.MIRROR_SCALAR.items()}
    scalar, mon = cid
    return inv[scalar], tuple(sorted(mletter(x) for x in mon))


def verify(result: dict) -> dict:
    if result.get("stage") != STAGE:
        raise AssertionError("T3-010-B stage drift")
    if result.get("t3_010_a_checkpoint", {}).get("validated_head") != A_HEAD:
        raise AssertionError("T3-010-A checkpoint drift")
    for name, want in A_BLOBS.items():
        if a.git_blob_sha1(HERE / name) != want:
            raise AssertionError(f"T3-010-A blob drift in verifier: {name}")
    contract = json.loads((HERE / "T3_010_B_CONTRACT.json").read_text())
    if contract["stage"] != STAGE or contract["coefficient_envelope"]["degree"] != 0:
        raise AssertionError("T3-010-B contract drift")

    a.assert_source_locks(); a.validate_architecture()
    layer, predecessor = a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("predecessor digest drift in B verifier")
    primitive_full = a.primitive_oriented_layer(layer)
    strata = a.shell_strata()
    by_id = {x["id"]: x for x in strata}
    specialized = {
        st["id"]: a.primitive_oriented_layer(a.specialize_layer(layer, st["k_offset"], st["l_offset"]))
        for st in strata
    }
    supports = {(c, b): support(primitive_full, c, b) for c in a.CHANNEL_SCALARS for b in BLOCK_ORDER}
    expected = {x["id"]: x for x in result["matrix_cells"]}
    if len(expected) != 400:
        raise AssertionError("producer B matrix-cell cardinality drift")

    histogram: dict[str, int] = {}
    active = viable = inconsistent = 0
    mirror_checks = 0
    for st in strata:
        p = specialized[st["id"]]
        for channel in a.INDEPENDENT_CHANNELS:
            for block in BLOCK_ORDER:
                cid = f"{channel}:{block}:{st['id']}"
                got, target, cols, ids = cell(p, supports[(channel, block)], channel, block, st)
                rec = expected[cid]
                for key in (
                    "classification", "unknowns", "coefficient_rank", "augmented_rank", "nullity",
                    "target_coordinate_count", "matrix_coordinate_count", "zero_response_columns",
                    "candidate_support_sha256", "coefficient_matrix_sha256", "target_sha256",
                ):
                    if rec[key] != got[key]:
                        raise AssertionError(f"independent B reconstruction drift {cid}:{key}")
                histogram[got["classification"]] = histogram.get(got["classification"], 0) + 1
                if got["classification"] != "STRUCTURAL_ZERO":
                    active += 1
                    if got["classification"].startswith("CONSISTENT_"):
                        viable += 1
                    elif got["classification"] == "EXACTLY_INCONSISTENT":
                        inconsistent += 1
                if channel == "k1":
                    mst = by_id[st["mirror"]]
                    lp = specialized[mst["id"]]
                    lr, lt, lc, li = cell(lp, supports[("l1", block)], "l1", block, mst)
                    if mirror_vec(lt) != target:
                        raise AssertionError("B verifier target mirror drift")
                    lk = {mirror_id(i): mirror_vec(v) for i, v in zip(li, lc)}
                    kk = {i: v for i, v in zip(ids, cols)}
                    if lk != kk:
                        raise AssertionError("B verifier matrix mirror drift")
                    if (lr["coefficient_rank"], lr["augmented_rank"], lr["classification"]) != (
                        got["coefficient_rank"], got["augmented_rank"], got["classification"]
                    ):
                        raise AssertionError("B verifier mirror rank drift")
                    mirror_checks += 1

    if result["classification_histogram"] != dict(sorted(histogram.items())):
        raise AssertionError("B classification histogram drift")
    if result["active_cell_count"] != active or result["viable_cell_count"] != viable:
        raise AssertionError("B viability aggregate drift")
    if result["inconsistent_cell_count"] != inconsistent:
        raise AssertionError("B inconsistency aggregate drift")
    if result["structural_zero_cell_count"] != 400-active:
        raise AssertionError("B structural-zero aggregate drift")
    if mirror_checks != 100 or result["exact_k1_l1_matrix_mirror_checks"] != 100:
        raise AssertionError("B mirror-check count drift")
    if result["solution_coefficients_extracted"] or result["full_correction_layer_recombined"]:
        raise AssertionError("B premature extraction/recombination")
    if result["final_n_holonomic_search_run"]:
        raise AssertionError("B illegal recurrence search")
    if result["finite_sampling_used_as_sum_proof"]:
        raise AssertionError("B finite-sample proof inflation")
    if result["residual_sum_zero_proved"]:
        raise AssertionError("B theorem inflation")
    if result["proof_effect"] != "NONE" or result["promotion_effect"] != "NONE":
        raise AssertionError("B claim-boundary inflation")
    if result["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("B T3 status inflation")

    return {
        "schema_version": "1.0.0",
        "stage": STAGE,
        "status": "INDEPENDENT_T3_010_B_EXACT_MATRIX_REPLAY_COMPLETE",
        "independent_cell_count": 400,
        "active_cell_count": active,
        "viable_cell_count": viable,
        "inconsistent_cell_count": inconsistent,
        "exact_k1_l1_matrix_mirror_checks": mirror_checks,
        "rank_path": "independent exact-Q reverse sparse elimination with largest-coordinate pivots",
        "producer_matrix_imported_as_authority": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main() -> int:
    import t3_010_b as producer
    print(json.dumps(verify(producer.build()), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
