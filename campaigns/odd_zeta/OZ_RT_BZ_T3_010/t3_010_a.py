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

OPERATION = "SYMMETRY_REDUCED_CHANNEL_HARMONIC_BLOCK_WITH_SHELL_STRATA_001"
STAGE = "T3_010_A_EXACT_SHELL_CHANNEL_BLOCK_DECOMPOSITION_AND_VIABILITY_GATE"
PREDECESSOR_MERGE = "6b4761859174c39ea95438ea415948c16db91745"
PREDECESSOR_TREE = "eeecb37d5f8f55f67aee740efe41923e59c769e6"
PREDECESSOR_LAYER_SHA256 = "90d067ae59790fab8648d006635c14950359b66eb8b57361e61d5b47b2b3af40"

SOURCE_BLOBS = {
    "ONE_BODY_COEFFICIENT_LAYER.json": "6ed4ee15cc23a6ab1bdb40b064f1c1f8733663f7",
    "ONE_BODY_STRUCTURE_RESULT.json": "9b94915d18016d3d903d04217eadb7b10e69c7dd",
    "LETTER_SPLIT_RESULT.json": "8d9628bdc5f7c0915bc53db9e851192977c8c25b",
    "HOLONOMIC_ROUTE.json": "9e65e71a1fc268e40e2a71c411c6b364a49a94c7",
    "one_body_coefficient_layer.py": "0e09a5af6a58895750a210a58a56facfb5e094b6",
}

WEIGHT_BLOCKS = {
    "weight1": ["H_k_1", "H_kl_1", "H_nk_1", "H_nmk_1", "H_nkl_1"],
    "weight2": ["H_k_2", "H_kl_2", "H_nk_2", "H_nkl_2"],
    "weight3": ["H_k_3", "H_nk_3"],
    "weight4": ["H_k_4", "H_nk_4"],
}

CHANNEL_SCALARS = {
    "n1": ["TN1"],
    "n2": ["TN2"],
    "n3": ["TN3"],
    "k1": ["SK", "AK", "LKK", "LLK"],
    "l1": ["SL", "AL", "LLL", "LKL"],
}
INDEPENDENT_CHANNELS = ["n1", "n2", "n3", "k1"]
MIRROR_SCALAR = {
    "SK": "SL",
    "AK": "AL",
    "LKK": "LLL",
    "LLK": "LKL",
}

COORDINATE_CLASSES = [
    {"id": "interior", "offset": None, "condition": "coordinate<=n-1"},
    {"id": "edge0", "offset": 0, "condition": "coordinate=n"},
    {"id": "shell1", "offset": 1, "condition": "coordinate=n+1"},
    {"id": "shell2", "offset": 2, "condition": "coordinate=n+2"},
    {"id": "shell3", "offset": 3, "condition": "coordinate=n+3"},
]

# Exact k<->l quotient expansion of the protected 22 one-body atoms into
# the 13 letter representatives retained by LETTER_SPLIT_RESULT.json.
ATOM_EXPANSION = {
    "A_k_1": {"H_nk_1": 1, "H_k_1": -1},
    "A_l_1": {"H_nk_1": 1, "H_k_1": -1},
    "A_k_2": {"H_nk_2": 1, "H_k_2": -1},
    "A_l_2": {"H_nk_2": 1, "H_k_2": -1},
    "B_k_1": {"H_nmk_1": 1, "H_k_1": -1},
    "B_l_1": {"H_nmk_1": 1, "H_k_1": -1},
    "C_1": {"H_nkl_1": 1, "H_kl_1": -1},
    "C_2": {"H_nkl_2": 1, "H_kl_2": -1},
    "H_k_1": {"H_k_1": 1},
    "H_l_1": {"H_k_1": 1},
    "H_k_2": {"H_k_2": 1},
    "H_l_2": {"H_k_2": 1},
    "H_k_3": {"H_k_3": 1},
    "H_l_3": {"H_k_3": 1},
    "H_k_4": {"H_k_4": 1},
    "H_l_4": {"H_k_4": 1},
    "H_kl_1": {"H_kl_1": 1},
    "H_kl_2": {"H_kl_2": 1},
    "H_nk_3": {"H_nk_3": 1},
    "H_nl_3": {"H_nk_3": 1},
    "H_nk_4": {"H_nk_4": 1},
    "H_nl_4": {"H_nk_4": 1},
}


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def assert_source_locks() -> dict[str, str]:
    got = {}
    for name, want in SOURCE_BLOBS.items():
        path = PREDECESSOR / name
        sha = git_blob_sha1(path)
        if sha != want:
            raise AssertionError(f"source lock drift: {name}: {sha} != {want}")
        got[name] = sha
    summary = json.loads((PREDECESSOR / "ONE_BODY_COEFFICIENT_LAYER.json").read_text())
    if summary["final_layer"]["sha256"] != PREDECESSOR_LAYER_SHA256:
        raise AssertionError("predecessor coefficient digest drift")
    if summary["factor_profile"]["protected_factor_count"] != 8:
        raise AssertionError("protected factor count drift")
    expected = [
        [1, -1, 0, 0], [1, -1, 0, 1], [1, -1, 0, 2], [1, -1, 0, 3],
        [1, 0, -1, 0], [1, 0, -1, 1], [1, 0, -1, 2], [1, 0, -1, 3],
    ]
    if summary["factor_profile"]["protected_positive_reciprocal_factors"] != expected:
        raise AssertionError("protected reciprocal identity drift")
    if summary["protected_harmonic_shift_lemma"]["pinv_definition"] != \
            "pinv_r(x)=x^(-r) for integer x>0; 0 for integer x<=0":
        raise AssertionError("pinv semantics drift")
    return got


def validate_architecture() -> None:
    letter = json.loads((PREDECESSOR / "LETTER_SPLIT_RESULT.json").read_text())
    route = json.loads((PREDECESSOR / "HOLONOMIC_ROUTE.json").read_text())
    if letter["weight_blocks"] != WEIGHT_BLOCKS:
        raise AssertionError("5+4+2+2 harmonic block drift")
    if [len(WEIGHT_BLOCKS[k]) for k in ("weight1", "weight2", "weight3", "weight4")] != [5, 4, 2, 2]:
        raise AssertionError("harmonic block size drift")
    cd = route["channel_decomposition"]
    if cd["symmetry_reduced_channels"] != INDEPENDENT_CHANNELS:
        raise AssertionError("independent channel drift")
    if cd["protected_channels"] != ["n1", "n2", "n3", "k1", "l1"]:
        raise AssertionError("protected channel drift")
    structure = json.loads((PREDECESSOR / "ONE_BODY_STRUCTURE_RESULT.json").read_text())
    if sorted(ATOM_EXPANSION) != sorted(structure["union_one_body_atoms"]):
        raise AssertionError("22-atom expansion domain drift")
    if set().union(*map(set, WEIGHT_BLOCKS.values())) != set(letter["diagnostic_defect_matrix"]["columns"]):
        raise AssertionError("13-orbit representative drift")
    covered = [x for values in CHANNEL_SCALARS.values() for x in values]
    if sorted(covered) != sorted(pcl.SCALAR_ORDER):
        raise AssertionError("11 scalar basis is not partitioned by protected channels")
    if [MIRROR_SCALAR[x] for x in CHANNEL_SCALARS["k1"]] != CHANNEL_SCALARS["l1"]:
        raise AssertionError("k1/l1 scalar mirror drift")


def coordinate_activation(offset: int | None) -> tuple[bool, bool, bool, bool]:
    if offset is None:
        return (True, True, True, True)
    return tuple((s - offset) > 0 for s in range(4))


def shell_strata() -> list[dict]:
    out = []
    for kcls, lcls in product(COORDINATE_CLASSES, repeat=2):
        ka = coordinate_activation(kcls["offset"])
        la = coordinate_activation(lcls["offset"])
        sid = f"k_{kcls['id']}__l_{lcls['id']}"
        out.append({
            "id": sid,
            "k_class": kcls["id"],
            "l_class": lcls["id"],
            "k_offset": kcls["offset"],
            "l_offset": lcls["offset"],
            "protected_factor_activation": {
                **{f"n-k+{s}": ka[s] for s in range(4)},
                **{f"n-l+{s}": la[s] for s in range(4)},
            },
            "ordinary_rational_interior": kcls["offset"] is None and lcls["offset"] is None,
            "mirror": f"k_{lcls['id']}__l_{kcls['id']}",
        })
    if len(out) != 25 or sum(x["ordinary_rational_interior"] for x in out) != 1:
        raise AssertionError("shell partition drift")
    return out


def specialize_rat(rat: rc.Rat, k_offset: int | None, l_offset: int | None) -> rc.Rat:
    out: rc.Rat = {}
    for sig, coeff in rat.items():
        new_coeff = coeff
        new_sig = []
        killed = False
        for factor, exponent in sig:
            if len(factor) == 5 and factor[0] == pcl.PINV_TAG:
                _, a, b, c, d = factor
                ordinary = (a, b, c, d)
                if ordinary[:3] == (1, -1, 0):
                    off = k_offset
                elif ordinary[:3] == (1, 0, -1):
                    off = l_offset
                else:
                    raise AssertionError(f"unexpected protected factor {ordinary}")
                if off is None:
                    new_sig.append((ordinary, exponent))
                else:
                    z = d - off
                    if z <= 0:
                        killed = True
                        break
                    new_coeff *= Q(z) ** exponent
            else:
                new_sig.append((factor, exponent))
        if killed or new_coeff == 0:
            continue
        key = tuple(sorted(new_sig))
        out[key] = out.get(key, Q(0)) + new_coeff
        if out[key] == 0:
            del out[key]
    return out


def specialize_layer(layer: pcl.Layer, k_offset: int | None, l_offset: int | None) -> pcl.Layer:
    out: pcl.Layer = {}
    for mon, by_scalar in layer.items():
        terms = {}
        for scalar, rat in by_scalar.items():
            got = specialize_rat(rat, k_offset, l_offset)
            if got:
                terms[scalar] = got
        if terms:
            out[mon] = terms
    return out


def mul_formal(a: dict[tuple[str, ...], int], b: dict[tuple[str, ...], int]):
    out: dict[tuple[str, ...], int] = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            mon = tuple(sorted(ma + mb))
            out[mon] = out.get(mon, 0) + ca * cb
            if out[mon] == 0:
                del out[mon]
    return out


def expand_atom_monomial(mon: tuple[str, ...]) -> dict[tuple[str, ...], int]:
    out = {(): 1}
    for atom in mon:
        atom_poly = {(rep,): coeff for rep, coeff in ATOM_EXPANSION[atom].items()}
        out = mul_formal(out, atom_poly)
    return out


def primitive_layer(layer: pcl.Layer) -> pcl.Layer:
    out: pcl.Layer = {}
    for mon, by_scalar in layer.items():
        expansion = expand_atom_monomial(mon)
        for pmon, mult in expansion.items():
            if mult == 0:
                continue
            target = out.setdefault(pmon, {})
            for scalar, rat in by_scalar.items():
                merged = rc.r_add(target.get(scalar, {}), rc.r_scale(rat, Q(mult)))
                if merged:
                    target[scalar] = merged
                elif scalar in target:
                    del target[scalar]
            if not target:
                del out[pmon]
    return out


def rank_q(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    a = [[Q(x) for x in row] for row in matrix]
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][c]
        a[r] = [x / p for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def support_probe(layer: pcl.Layer, channel: str, block: str, stratum_id: str) -> dict:
    reps = set(WEIGHT_BLOCKS[block])
    scalars = CHANNEL_SCALARS[channel]
    rows = []
    for mon in sorted(layer):
        if not reps.intersection(mon):
            continue
        row = [1 if layer[mon].get(scalar) else 0 for scalar in scalars]
        if any(row):
            rows.append(row)
    rank = rank_q(rows)
    return {
        "id": f"{channel}:{block}:{stratum_id}",
        "channel": channel,
        "block": block,
        "stratum": stratum_id,
        "scalar_columns": scalars,
        "forcing_row_count": len(rows),
        "support_incidence_rank_over_Q": rank,
        "status": "STRUCTURALLY_ACTIVE_FORCING_SUPPORT" if rows else "ZERO_FORCING_SUPPORT",
        "rank_scope": "Exact rank of the 0/1 scalar-support incidence matrix after exact shell specialization; not the rank of a correction-flux elimination matrix.",
        "correction_candidate_admitted": False,
    }


def build() -> dict:
    source_locks = assert_source_locks()
    validate_architecture()
    layer, predecessor = pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != PREDECESSOR_LAYER_SHA256:
        raise AssertionError("independently rebuilt predecessor layer digest drift")
    strata = shell_strata()
    probes = []
    strata_records = []
    for st in strata:
        specialized = specialize_layer(layer, st["k_offset"], st["l_offset"])
        primitive = primitive_layer(specialized)
        strata_records.append({
            **st,
            "specialized_atom_monomials": len(specialized),
            "primitive_orbit_monomials": len(primitive),
            "specialized_layer_sha256": pcl.layer_digest(specialized),
        })
        for channel in INDEPENDENT_CHANNELS:
            for block in ("weight1", "weight2", "weight3", "weight4"):
                probes.append(support_probe(primitive, channel, block, st["id"]))
    expected_probe_count = 25 * len(INDEPENDENT_CHANNELS) * len(WEIGHT_BLOCKS)
    if len(probes) != expected_probe_count:
        raise AssertionError("probe count drift")
    mirror_cells = 25 * len(WEIGHT_BLOCKS)
    return {
        "schema_version": "1.0.0",
        "issue": 403,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "EXACT_SHELL_CHANNEL_BLOCK_DECOMPOSITION_AND_FORCING_SUPPORT_RANK_GATE_COMPLETE",
        "branch_base": "170395009fcdf8114621c321624d78a4384b6237",
        "mathematical_predecessor": {
            "protected_merge": PREDECESSOR_MERGE,
            "tree": PREDECESSOR_TREE,
            "coefficient_layer_sha256": PREDECESSOR_LAYER_SHA256,
            "source_blobs": source_locks,
        },
        "pinv_semantics": "pinv_r(x)=x^(-r) for integer x>0; 0 for integer x<=0",
        "coordinate_classes": COORDINATE_CLASSES,
        "shell_strata": strata_records,
        "shell_stratum_count": len(strata_records),
        "interior_stratum_count": 1,
        "moving_boundary_or_shell_stratum_count": 24,
        "channel_manifest": {
            "protected_channels": ["n1", "n2", "n3", "k1", "l1"],
            "independent_channels": INDEPENDENT_CHANNELS,
            "channel_scalar_partition": CHANNEL_SCALARS,
            "l1_policy": "derived only as exact k<->l mirror of k1",
            "mirror_scalar_map": MIRROR_SCALAR,
        },
        "harmonic_blocks": WEIGHT_BLOCKS,
        "harmonic_block_sizes": [5, 4, 2, 2],
        "independent_probe_cell_count": len(probes),
        "mirrored_l1_cell_count": mirror_cells,
        "forcing_support_rank_probes": probes,
        "viability_interpretation": {
            "scope": "T3-010-A forcing-side structural screen only",
            "exact": "Shell specialization, source locks, orbit expansion, 0/1 support incidence ranks, channel partition, and mirror architecture are exact.",
            "not_yet_admitted": "No correction-flux unknown basis, degree bound, candidate coefficient, elimination result, or n-holonomic recurrence is admitted by this stage.",
            "next_gate": "Instantiate bounded correction-flux bases only for structurally active cells, then compute exact coefficient-matrix ranks/consistency before elimination.",
        },
        "shell_recombination": {
            "status": "EXACT_PIECEWISE_PARTITION_COMPLETE",
            "reason": "The five coordinate classes are exhaustive and disjoint on the common n+3 box, and each protected factor has constant pinv activation on each class; specialization is the exact definition of pinv on that stratum.",
            "full_correction_layer_recombined": False,
        },
        "finite_sampling_used_as_sum_proof": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": "T3_010_A_COMPLETE__CORRECTION_FLUX_MATRIX_RANK_GATE_PENDING",
    }


def main() -> int:
    print(json.dumps(build(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
