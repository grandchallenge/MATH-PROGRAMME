#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREDECESSOR = HERE.parent / "OZ_RT_BZ_T3_009"
if str(PREDECESSOR) not in sys.path:
    sys.path.insert(0, str(PREDECESSOR))

import one_body_coefficient_layer as pcl  # noqa: E402
import residual_canonical as rc  # noqa: E402

EXPECTED_LAYER = "90d067ae59790fab8648d006635c14950359b66eb8b57361e61d5b47b2b3af40"
EXPECTED_BLOBS = {
    "ONE_BODY_COEFFICIENT_LAYER.json": "6ed4ee15cc23a6ab1bdb40b064f1c1f8733663f7",
    "ONE_BODY_STRUCTURE_RESULT.json": "9b94915d18016d3d903d04217eadb7b10e69c7dd",
    "LETTER_SPLIT_RESULT.json": "8d9628bdc5f7c0915bc53db9e851192977c8c25b",
    "HOLONOMIC_ROUTE.json": "9e65e71a1fc268e40e2a71c411c6b364a49a94c7",
    "one_body_coefficient_layer.py": "0e09a5af6a58895750a210a58a56facfb5e094b6",
}
BLOCKS = {
    "weight1": ("H_k_1", "H_kl_1", "H_nk_1", "H_nmk_1", "H_nkl_1"),
    "weight2": ("H_k_2", "H_kl_2", "H_nk_2", "H_nkl_2"),
    "weight3": ("H_k_3", "H_nk_3"),
    "weight4": ("H_k_4", "H_nk_4"),
}
CHANNELS = {
    "n1": ("TN1",),
    "n2": ("TN2",),
    "n3": ("TN3",),
    "k1": ("SK", "AK", "LKK", "LLK"),
}
ATOM = {
    "A_k_1": (("H_nk_1", 1), ("H_k_1", -1)),
    "A_l_1": (("H_nk_1", 1), ("H_k_1", -1)),
    "A_k_2": (("H_nk_2", 1), ("H_k_2", -1)),
    "A_l_2": (("H_nk_2", 1), ("H_k_2", -1)),
    "B_k_1": (("H_nmk_1", 1), ("H_k_1", -1)),
    "B_l_1": (("H_nmk_1", 1), ("H_k_1", -1)),
    "C_1": (("H_nkl_1", 1), ("H_kl_1", -1)),
    "C_2": (("H_nkl_2", 1), ("H_kl_2", -1)),
    "H_k_1": (("H_k_1", 1),), "H_l_1": (("H_k_1", 1),),
    "H_k_2": (("H_k_2", 1),), "H_l_2": (("H_k_2", 1),),
    "H_k_3": (("H_k_3", 1),), "H_l_3": (("H_k_3", 1),),
    "H_k_4": (("H_k_4", 1),), "H_l_4": (("H_k_4", 1),),
    "H_kl_1": (("H_kl_1", 1),), "H_kl_2": (("H_kl_2", 1),),
    "H_nk_3": (("H_nk_3", 1),), "H_nl_3": (("H_nk_3", 1),),
    "H_nk_4": (("H_nk_4", 1),), "H_nl_4": (("H_nk_4", 1),),
}
CLASSES = (("interior", None), ("edge0", 0), ("shell1", 1), ("shell2", 2), ("shell3", 3))


def blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def specialize(rat: rc.Rat, ko: int | None, lo: int | None) -> rc.Rat:
    ans: rc.Rat = {}
    for sig, coeff in rat.items():
        c = coeff
        parts = []
        dead = False
        for factor, exp in sig:
            if len(factor) == 5 and factor[0] == pcl.PINV_TAG:
                _, a, b, cv, d = factor
                ordinary = (a, b, cv, d)
                if ordinary[:3] == (1, -1, 0):
                    off = ko
                elif ordinary[:3] == (1, 0, -1):
                    off = lo
                else:
                    raise AssertionError("unknown protected factor")
                if off is None:
                    parts.append((ordinary, exp))
                else:
                    value = d - off
                    if value <= 0:
                        dead = True
                        break
                    c *= Q(value) ** exp
            else:
                parts.append((factor, exp))
        if not dead and c:
            key = tuple(sorted(parts))
            ans[key] = ans.get(key, Q(0)) + c
            if not ans[key]:
                del ans[key]
    return ans


def expand(mon: tuple[str, ...]) -> dict[tuple[str, ...], int]:
    out = {(): 1}
    for atom in mon:
        nxt = {}
        for old, oc in out.items():
            for rep, ac in ATOM[atom]:
                nm = tuple(sorted(old + (rep,)))
                nxt[nm] = nxt.get(nm, 0) + oc * ac
                if nxt[nm] == 0:
                    del nxt[nm]
        out = nxt
    return out


def primitive(layer: pcl.Layer, ko: int | None, lo: int | None) -> pcl.Layer:
    out: pcl.Layer = {}
    for mon, terms in layer.items():
        ex = expand(mon)
        for pm, mult in ex.items():
            target = out.setdefault(pm, {})
            for scalar, rat in terms.items():
                sr = specialize(rat, ko, lo)
                if not sr:
                    continue
                merged = rc.r_add(target.get(scalar, {}), rc.r_scale(sr, Q(mult)))
                if merged:
                    target[scalar] = merged
                elif scalar in target:
                    del target[scalar]
            if not target:
                del out[pm]
    return out


def rank_q(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    a = [[Q(x) for x in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [x / q for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def expected_rank(pl: pcl.Layer, channel: str, block: str) -> tuple[int, int]:
    reps = set(BLOCKS[block])
    scalars = CHANNELS[channel]
    rows = []
    for mon in sorted(pl):
        if not reps.intersection(mon):
            continue
        row = [1 if pl[mon].get(s) else 0 for s in scalars]
        if any(row):
            rows.append(row)
    return len(rows), rank_q(rows)


def verify(result: dict) -> dict:
    for name, want in EXPECTED_BLOBS.items():
        if blob(PREDECESSOR / name) != want:
            raise AssertionError(f"source blob drift {name}")
    summary = json.loads((PREDECESSOR / "ONE_BODY_COEFFICIENT_LAYER.json").read_text())
    if summary["final_layer"]["sha256"] != EXPECTED_LAYER:
        raise AssertionError("layer digest drift")
    if result["residual_sum_zero_proved"] is not False or result["proof_effect"] != "NONE" or result["promotion_effect"] != "NONE":
        raise AssertionError("claim-boundary inflation")
    if result["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status inflation")
    if result["harmonic_block_sizes"] != [5, 4, 2, 2]:
        raise AssertionError("block-size drift")
    if result["independent_probe_cell_count"] != 400:
        raise AssertionError("independent probe count drift")
    if result["mirrored_l1_cell_count"] != 100:
        raise AssertionError("mirror cell count drift")

    layer, rebuilt = pcl.build_layer()
    if rebuilt["final_layer"]["sha256"] != EXPECTED_LAYER:
        raise AssertionError("rebuilt predecessor digest drift")
    probes = {p["id"]: p for p in result["forcing_support_rank_probes"]}
    if len(probes) != 400:
        raise AssertionError("probe identity collision")
    strata = {(s["k_class"], s["l_class"]): s for s in result["shell_strata"]}
    if len(strata) != 25:
        raise AssertionError("shell stratum count drift")

    checked = 0
    for (kn, ko), (ln, lo) in product(CLASSES, repeat=2):
        st = strata[(kn, ln)]
        activation = st["protected_factor_activation"]
        for s in range(4):
            if activation[f"n-k+{s}"] != (True if ko is None else s - ko > 0):
                raise AssertionError("k pinv activation drift")
            if activation[f"n-l+{s}"] != (True if lo is None else s - lo > 0):
                raise AssertionError("l pinv activation drift")
        pl = primitive(layer, ko, lo)
        sid = f"k_{kn}__l_{ln}"
        for channel in CHANNELS:
            for block in BLOCKS:
                rows, rank = expected_rank(pl, channel, block)
                p = probes[f"{channel}:{block}:{sid}"]
                if p["forcing_row_count"] != rows or p["support_incidence_rank_over_Q"] != rank:
                    raise AssertionError(f"forcing support-rank drift {p['id']}")
                if p["correction_candidate_admitted"] is not False:
                    raise AssertionError("candidate inflation")
                checked += 1
    if checked != 400:
        raise AssertionError("independent replay count drift")
    return {
        "status": "INDEPENDENT_T3_010_A_REPLAY_COMPLETE",
        "source_blobs_verified": len(EXPECTED_BLOBS),
        "shell_strata_verified": 25,
        "forcing_support_rank_cells_verified": checked,
        "l1_policy_verified": "mirror_only",
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main() -> int:
    import t3_010_a
    result = t3_010_a.build()
    print(json.dumps(verify(result), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
