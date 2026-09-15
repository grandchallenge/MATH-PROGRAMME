from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import lex_pivot_sweep

DEFAULT_REPORT = HERE / "LEX_PIVOT_RATIONAL_PROFILE.json"


def _canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _polyval(coefficients: list[int] | np.ndarray, x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * (x % p) + int(coefficient)) % p
    return value


def load_report(path: Path | str = DEFAULT_REPORT) -> dict[str, Any]:
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {
        "schema_version",
        "report_id",
        "protected_source_head",
        "protected_sweep_run_id",
        "request_id",
        "source_lock",
        "sweep_contract",
        "artifacts",
        "independent_sweep_readback",
        "normalized_pivot_dataset",
        "rational_profile_mod_p",
        "evidence_effect",
        "proof_effect",
        "promotion_effect",
    }
    missing = sorted(required - set(report))
    if missing:
        raise AssertionError(f"lex reconstruction report missing fields: {missing}")
    if report["schema_version"] != "1.0.0":
        raise AssertionError("unsupported lex reconstruction report schema")
    if report["evidence_effect"] != "MODULAR_CANDIDATE_ONLY":
        raise AssertionError("lex reconstruction report may record modular candidate evidence only")
    if report["proof_effect"] != "NONE" or report["promotion_effect"] != "NONE":
        raise AssertionError("lex reconstruction report claim firewall drift")
    return report


def _newton_common_denominator_profile(
    normalized: np.ndarray,
    ns: np.ndarray,
    *,
    fit_count: int,
    degree_ceiling: int,
    denominator: np.ndarray,
    p: int,
) -> dict[str, Any]:
    if normalized.ndim != 2:
        raise AssertionError("normalized scalar sample matrix must be two-dimensional")
    if len(ns) != normalized.shape[0]:
        raise AssertionError("sample-node count mismatch")
    if fit_count < 2 or not fit_count < len(ns):
        raise AssertionError("invalid fit/holdout partition")
    if np.any(np.diff(ns) != 1):
        raise AssertionError("Newton verifier requires consecutive integer sample nodes")
    if degree_ceiling >= fit_count:
        raise AssertionError("degree ceiling must be strictly below fit sample count")

    dvals = np.asarray([_polyval(denominator, int(n), p) for n in ns], dtype=np.int64)
    if np.count_nonzero(dvals == 0):
        raise AssertionError("declared common denominator vanishes on governed sample nodes")

    fit = np.asarray(normalized[:fit_count], dtype=np.int64)
    holdout = np.asarray(normalized[fit_count:], dtype=np.int64)
    zfit = fit * dvals[:fit_count, None] % p

    work = zfit.copy()
    coefficients: list[np.ndarray] = []
    numerator_degrees = np.full(normalized.shape[1], -1, dtype=np.int32)
    for order in range(degree_ceiling + 1):
        first = work[0].copy()
        coefficients.append(first)
        numerator_degrees[first != 0] = order
        work = (work[1:] - work[:-1]) % p

    if np.count_nonzero(work):
        failing = np.nonzero(np.any(work != 0, axis=0))[0]
        raise AssertionError(
            f"common-denominator numerator degree exceeds governed ceiling for {len(failing)} sequences"
        )

    coeff = np.stack(coefficients, axis=0)
    n0 = int(ns[0])
    predicted = np.empty_like(holdout)
    for row, n in enumerate(ns[fit_count:]):
        t = int(n) - n0
        choose = 1
        value = coeff[0].copy()
        for k in range(1, degree_ceiling + 1):
            choose = choose * ((t - (k - 1)) % p) % p
            choose = choose * pow(k, p - 2, p) % p
            value = (value + choose * coeff[k]) % p
        predicted[row] = value

    actual = holdout * dvals[fit_count:, None] % p
    mismatch = np.nonzero(np.any(predicted != actual, axis=0))[0]
    if len(mismatch):
        raise AssertionError(f"holdout failure for {len(mismatch)} scalar sequences")

    return {
        "fit_pass_count": int(normalized.shape[1]),
        "holdout_pass_count": int(normalized.shape[1]),
        "common_numerator_degree_max": int(numerator_degrees.max(initial=-1)),
        "numerator_degrees": numerator_degrees,
        "denominator_values": dvals,
    }


def verify_profile(
    report_path: Path | str,
    chunk_outputs: list[Path | str],
) -> dict[str, Any]:
    report = load_report(report_path)
    if len(chunk_outputs) != 4:
        raise AssertionError("lex reconstruction profile requires exactly four protected chunks")
    outputs = [Path(path) for path in chunk_outputs]

    request_paths = [path / "request.json" for path in outputs]
    request_bytes = [path.read_bytes() for path in request_paths]
    if len(set(request_bytes)) != 1:
        raise AssertionError("protected chunk request copies differ")
    request = json.loads(request_bytes[0])
    lex_pivot_sweep.validate_request(request)
    if request["request_id"] != report["request_id"]:
        raise AssertionError("report/request identity mismatch")

    sweep = lex_pivot_sweep.verify_sweep(request_paths[0], outputs)
    contract = report["sweep_contract"]
    if sweep["n_start"] != int(contract["n_start"]) or sweep["n_stop"] != int(contract["n_stop"]):
        raise AssertionError("report sweep coverage mismatch")
    if sweep["pivot_sha256"] != contract["expected_pivot_sha256"]:
        raise AssertionError("report pivot digest mismatch")
    if sweep["coordinate_map_sha256"] != contract["coordinate_map_sha256"]:
        raise AssertionError("report coordinate-map digest mismatch")

    rows: list[np.ndarray] = []
    nodes: list[int] = []
    pivot_indices: np.ndarray | None = None
    for output in outputs:
        metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
        coordinate_map = json.loads((output / "coordinate-map.json").read_text(encoding="utf-8"))
        pivots = np.asarray(coordinate_map["pivot_indices"], dtype=np.int64)
        if pivot_indices is None:
            pivot_indices = pivots
        elif not np.array_equal(pivot_indices, pivots):
            raise AssertionError("pivot-index drift across protected chunks")
        with np.load(output / "sections.npz", allow_pickle=False) as archive:
            sections = np.asarray(archive["sections"], dtype=np.int64)
        for index, record in enumerate(metadata["records"]):
            a0 = int(record["a0_mod_p"]) % int(request["prime"])
            if a0 == 0:
                raise AssertionError(f"normalization singularity at n={record['n']}")
            inverse = pow(a0, int(request["prime"]) - 2, int(request["prime"]))
            rows.append(sections[index, pivots, :] * inverse % int(request["prime"]))
            nodes.append(int(record["n"]))

    assert pivot_indices is not None
    normalized_3d = np.stack(rows, axis=0)
    normalized = normalized_3d.reshape(normalized_3d.shape[0], -1)
    ns = np.asarray(nodes, dtype=np.int64)
    expected_shape = tuple(int(x) for x in report["normalized_pivot_dataset"]["shape"])
    if normalized_3d.shape != expected_shape:
        raise AssertionError(f"normalized pivot dataset shape drift: {normalized_3d.shape} != {expected_shape}")
    digest = hashlib.sha256(normalized_3d.astype("<i4", copy=False).tobytes(order="C")).hexdigest()
    if digest != report["normalized_pivot_dataset"]["sha256"]:
        raise AssertionError("normalized pivot dataset digest drift")

    profile = report["rational_profile_mod_p"]
    all_zero = np.all(normalized == 0, axis=0)
    if int(np.count_nonzero(all_zero)) != int(profile["identically_zero_pivot_sequences"]):
        raise AssertionError("identically-zero pivot count drift")

    denominator = np.asarray(profile["common_denominator_coefficients_constant_first"], dtype=np.int64)
    if len(denominator) - 1 != int(profile["common_monic_denominator_degree"]):
        raise AssertionError("common denominator degree drift")
    if int(denominator[-1]) % int(request["prime"]) != 1:
        raise AssertionError("common denominator must remain monic")
    denominator_json_digest = hashlib.sha256(
        (json.dumps([int(x) for x in denominator], separators=(",", ":")) + "\n").encode("utf-8")
    ).hexdigest()
    if denominator_json_digest != profile["common_denominator_canonical_json_sha256"]:
        raise AssertionError("common denominator digest drift")

    reconstruction = _newton_common_denominator_profile(
        normalized,
        ns,
        fit_count=int(contract["fit_count"]),
        degree_ceiling=int(contract["balanced_degree_ceiling"]),
        denominator=denominator,
        p=int(request["prime"]),
    )
    if reconstruction["fit_pass_count"] != int(profile["fit_pass_count"]):
        raise AssertionError("fit-pass count drift")
    if reconstruction["holdout_pass_count"] != int(profile["holdout_pass_count"]):
        raise AssertionError("holdout-pass count drift")
    if reconstruction["common_numerator_degree_max"] != int(profile["common_numerator_degree_max_before_cancellation"]):
        raise AssertionError("common numerator degree drift")

    return {
        "report_id": report["report_id"],
        "protected_sweep_run_id": int(report["protected_sweep_run_id"]),
        "samples_verified": int(normalized.shape[0]),
        "pivot_scalar_sequences": int(normalized.shape[1]),
        "zero_pivot_sequences": int(np.count_nonzero(all_zero)),
        "nonzero_pivot_sequences": int(normalized.shape[1] - np.count_nonzero(all_zero)),
        "common_denominator_degree": int(len(denominator) - 1),
        "common_numerator_degree_max": int(reconstruction["common_numerator_degree_max"]),
        "balanced_degree_ceiling": int(contract["balanced_degree_ceiling"]),
        "holdout_pass_count": int(reconstruction["holdout_pass_count"]),
        "evidence_effect": report["evidence_effect"],
        "proof_effect": report["proof_effect"],
        "promotion_effect": report["promotion_effect"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the protected OZ T3-016-A lex-pivot rational profile")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--chunk", action="append", type=Path, required=True, dest="chunks")
    args = parser.parse_args()
    summary = verify_profile(args.report, args.chunks)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
