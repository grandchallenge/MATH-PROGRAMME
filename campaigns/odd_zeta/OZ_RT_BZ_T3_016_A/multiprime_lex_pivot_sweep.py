from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import shutil
import sys
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import lex_pivot_sweep

SOURCE_REPOSITORY = lex_pivot_sweep.SOURCE_REPOSITORY
SOURCE_COMMIT = lex_pivot_sweep.SOURCE_COMMIT
SOURCE_TREE = lex_pivot_sweep.SOURCE_TREE
SOURCE_FILES = dict(lex_pivot_sweep.SOURCE_FILES)

E1_COLUMNS = lex_pivot_sweep.E1_COLUMNS
EXPECTED_RANK = lex_pivot_sweep.EXPECTED_RANK
STANDALONE_BLOCKS = lex_pivot_sweep.STANDALONE_BLOCKS
SECTION_MODE = lex_pivot_sweep.SECTION_MODE
REFERENCE_PRIME = 4194301
REFERENCE_PROTECTED_HEAD = "91519091f47560d5bc71c5151f0d4f473b55e617"
REFERENCE_SWEEP_RUN_ID = 34905944791
REFERENCE_PROFILE_REPORT_ID = "OZ-RT-BZ-T3-016-A-LEX-PIVOT-RATIONAL-PROFILE-001"
REFERENCE_COORDINATE_MAP_SHA256 = "bcc4e2236e8c16f95e922fa936f288f1e6bf1b665b28de662413272008415865"
DEFAULT_REQUEST = HERE / "MULTIPRIME_LEX_PIVOT_SWEEP_REQUEST.json"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _is_prime(value: int) -> bool:
    n = int(value)
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def load_request(path: Path | str = DEFAULT_REQUEST) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_request(value)
    return value


def validate_request(request: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version",
        "request_id",
        "enabled",
        "section_mode",
        "expected_pivot_sha256",
        "reference_prime",
        "reference_protected_head",
        "reference_sweep_run_id",
        "reference_profile_report_id",
        "reference_coordinate_map_sha256",
        "primes",
        "source_commit",
        "source_tree",
        "n_start",
        "n_stop",
        "chunks",
        "workers_per_chunk",
        "fit_extra_rows",
        "fresh_rows",
        "solver_block_size",
        "reconstruction_fit_count",
        "holdout_count",
        "evidence_effect",
        "proof_effect",
        "promotion_effect",
    }
    missing = sorted(required - set(request))
    if missing:
        raise AssertionError(f"multi-prime lex request missing fields: {missing}")
    if request["schema_version"] != "1.0.0":
        raise AssertionError("unsupported multi-prime lex request schema")
    if not isinstance(request["request_id"], str) or not request["request_id"]:
        raise AssertionError("request_id must be non-empty")
    if not isinstance(request["enabled"], bool):
        raise AssertionError("enabled must be boolean")
    if request["section_mode"] != SECTION_MODE:
        raise AssertionError("multi-prime lex section mode drift")
    if request["source_commit"] != SOURCE_COMMIT:
        raise AssertionError("source commit drift")
    if request["source_tree"] != SOURCE_TREE:
        raise AssertionError("source tree drift")
    if int(request["reference_prime"]) != REFERENCE_PRIME:
        raise AssertionError("reference prime drift")
    if request["reference_protected_head"] != REFERENCE_PROTECTED_HEAD:
        raise AssertionError("reference protected-head drift")
    if int(request["reference_sweep_run_id"]) != REFERENCE_SWEEP_RUN_ID:
        raise AssertionError("reference sweep-run drift")
    if request["reference_profile_report_id"] != REFERENCE_PROFILE_REPORT_ID:
        raise AssertionError("reference profile identity drift")
    if request["reference_coordinate_map_sha256"] != REFERENCE_COORDINATE_MAP_SHA256:
        raise AssertionError("reference coordinate-map drift")

    primes = request["primes"]
    if not isinstance(primes, list) or len(primes) != 3:
        raise AssertionError("multi-prime lane requires exactly three additional primes")
    primes = [int(p) for p in primes]
    if len(set(primes)) != len(primes):
        raise AssertionError("additional primes must be distinct")
    if REFERENCE_PRIME in primes:
        raise AssertionError("additional primes must not repeat the admitted reference prime")
    for p in primes:
        if not _is_prime(p):
            raise AssertionError(f"non-prime modulus in multi-prime request: {p}")
        if p >= 2**31:
            raise AssertionError("prime exceeds int32 serialization bound")

    expected = request["expected_pivot_sha256"]
    if not isinstance(expected, str) or len(expected) != 64:
        raise AssertionError("expected pivot digest must be a SHA-256 hex string")
    try:
        int(expected, 16)
    except ValueError as exc:
        raise AssertionError("expected pivot digest must be hexadecimal") from exc

    start = int(request["n_start"])
    stop = int(request["n_stop"])
    if start < 1 or stop < start:
        raise AssertionError("invalid positive integer n range")
    if int(request["chunks"]) != 4:
        raise AssertionError("workflow matrix is fixed to four chunks")
    workers = int(request["workers_per_chunk"])
    if not 1 <= workers <= 8:
        raise AssertionError("workers_per_chunk outside governed bound")
    if int(request["fit_extra_rows"]) < 1 or int(request["fresh_rows"]) < 1:
        raise AssertionError("fit and fresh row reserves must be positive")
    nb = int(request["solver_block_size"])
    if nb < 1 or nb > 192:
        raise AssertionError("solver block size outside fastlin bound")
    for p in primes:
        if nb * (p - 1) ** 2 >= 2**53:
            raise AssertionError(f"float64 modular accumulation exactness bound violated for p={p}")

    total = stop - start + 1
    fit_count = int(request["reconstruction_fit_count"])
    holdout_count = int(request["holdout_count"])
    if fit_count < 3 or holdout_count < 1 or fit_count + holdout_count != total:
        raise AssertionError("reconstruction/holdout partition does not cover sample range")
    request["rational_degree_test_bound"] = lex_pivot_sweep.max_rational_degree_bound(fit_count)

    if request["evidence_effect"] != "MODULAR_CANDIDATE_ONLY":
        raise AssertionError("multi-prime sweep may emit modular candidate evidence only")
    if request["proof_effect"] != "NONE" or request["promotion_effect"] != "NONE":
        raise AssertionError("multi-prime claim firewall drift")
    return request


def chunk_ranges(request: dict[str, Any]) -> list[tuple[int, int]]:
    validate_request(request)
    start = int(request["n_start"])
    stop = int(request["n_stop"])
    chunks = int(request["chunks"])
    total = stop - start + 1
    q, r = divmod(total, chunks)
    out: list[tuple[int, int]] = []
    cursor = start
    for index in range(chunks):
        size = q + (1 if index < r else 0)
        if size <= 0:
            raise AssertionError("empty multi-prime lex chunk")
        out.append((cursor, cursor + size - 1))
        cursor += size
    if cursor != stop + 1:
        raise AssertionError("multi-prime lex chunk partition drift")
    return out


def verify_source_checkout(source: Path | str, request: dict[str, Any]) -> dict[str, Any]:
    validate_request(dict(request))
    root = Path(source).resolve()
    affine_sweep = lex_pivot_sweep.affine_sweep
    head = affine_sweep._git(root, "rev-parse", "HEAD")
    tree = affine_sweep._git(root, "rev-parse", "HEAD^{tree}")
    if head != request["source_commit"]:
        raise AssertionError(f"source head drift: {head}")
    if tree != request["source_tree"]:
        raise AssertionError(f"source tree drift: {tree}")
    blobs: dict[str, str] = {}
    for _local_name, (remote_path, expected_blob) in sorted(SOURCE_FILES.items()):
        got = affine_sweep._git(root, "rev-parse", f"{SOURCE_COMMIT}:{remote_path}")
        if got != expected_blob:
            raise AssertionError(f"source blob drift for {remote_path}: {got} != {expected_blob}")
        blobs[remote_path] = got
    return {"commit": head, "tree": tree, "blobs": blobs}


def _worker_init(source: str, cache_path: str) -> None:
    lex_pivot_sweep._worker_init(source, cache_path)


def _worker(task: tuple[int, int, int, int, int, str]) -> tuple[int, np.ndarray, dict]:
    n, p, fit_rows, fresh_rows, nb, expected = task
    section, data = lex_pivot_sweep._lex_shape(n, p, fit_rows, fresh_rows, nb, expected)
    return n, section, data


def run_chunk(
    request_path: Path | str,
    source: Path | str,
    prime_index: int,
    chunk_index: int,
    output: Path | str,
) -> dict[str, Any]:
    request_path = Path(request_path)
    request = load_request(request_path)
    if not request["enabled"]:
        raise AssertionError("refusing to execute disabled multi-prime lex request")
    prime_index = int(prime_index)
    primes = [int(p) for p in request["primes"]]
    if not 0 <= prime_index < len(primes):
        raise AssertionError("prime index outside request")
    p = primes[prime_index]

    chunk_index = int(chunk_index)
    ranges = chunk_ranges(request)
    if not 0 <= chunk_index < len(ranges):
        raise AssertionError("chunk index outside request")
    start, stop = ranges[chunk_index]
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    source = Path(source).resolve()
    source_identity = verify_source_checkout(source, request)

    cache_path = output / "qrow_cache.pkl"
    lex_pivot_sweep._install_source_modules(source, cache_path, prewarm=True)

    fit_rows = EXPECTED_RANK + int(request["fit_extra_rows"])
    fresh_rows = int(request["fresh_rows"])
    nb = int(request["solver_block_size"])
    expected = str(request["expected_pivot_sha256"])
    tasks = [(n, p, fit_rows, fresh_rows, nb, expected) for n in range(start, stop + 1)]
    workers = min(int(request["workers_per_chunk"]), len(tasks))
    ctx = mp.get_context("spawn")
    with ctx.Pool(
        processes=workers,
        initializer=_worker_init,
        initargs=(str(source), str(cache_path)),
    ) as pool:
        rows = list(pool.imap_unordered(_worker, tasks, chunksize=1))
    rows.sort(key=lambda item: item[0])

    expected_ns = list(range(start, stop + 1))
    if [row[0] for row in rows] != expected_ns:
        raise AssertionError("multi-prime chunk n ordering/coverage drift")
    sections = np.stack([row[1] for row in rows]).astype("<i4", copy=False)
    records = [row[2]["record"] for row in rows]
    coordinate_map = rows[0][2]["coordinate_map"]
    for row in rows[1:]:
        if row[2]["coordinate_map"] != coordinate_map:
            raise AssertionError("pivot or coordinate map changed inside multi-prime chunk")
    if coordinate_map["pivot_sha256"] != expected:
        raise AssertionError("multi-prime chunk pivot digest differs from request")

    coordinate_bytes = _canonical_json_bytes(coordinate_map)
    coordinate_sha = _sha256_bytes(coordinate_bytes)
    if coordinate_sha != str(request["reference_coordinate_map_sha256"]):
        raise AssertionError("multi-prime coordinate map differs from admitted reference section")
    np.savez_compressed(output / "sections.npz", sections=sections)
    (output / "coordinate-map.json").write_bytes(coordinate_bytes)
    shutil.copyfile(request_path, output / "request.json")
    metadata = {
        "schema_version": "1.0.0",
        "request_id": request["request_id"],
        "section_mode": SECTION_MODE,
        "prime_index": prime_index,
        "prime": p,
        "reference_prime": REFERENCE_PRIME,
        "reference_protected_head": REFERENCE_PROTECTED_HEAD,
        "reference_sweep_run_id": REFERENCE_SWEEP_RUN_ID,
        "reference_profile_report_id": REFERENCE_PROFILE_REPORT_ID,
        "chunk_index": chunk_index,
        "n_start": start,
        "n_stop": stop,
        "sample_count": len(rows),
        "source": source_identity,
        "fit_rows": fit_rows,
        "fresh_rows": fresh_rows,
        "section_coordinates": E1_COLUMNS,
        "expected_rank": EXPECTED_RANK,
        "standalone_blocks": STANDALONE_BLOCKS,
        "pivot_sha256": expected,
        "coordinate_map_sha256": coordinate_sha,
        "records": records,
        "evidence_effect": request["evidence_effect"],
        "proof_effect": request["proof_effect"],
        "promotion_effect": request["promotion_effect"],
    }
    (output / "metadata.json").write_bytes(_canonical_json_bytes(metadata))
    cache_path.unlink(missing_ok=True)
    return metadata


def verify_chunk(
    request_path: Path | str,
    prime_index: int,
    chunk_index: int,
    output: Path | str,
) -> dict[str, Any]:
    request = load_request(request_path)
    primes = [int(p) for p in request["primes"]]
    prime_index = int(prime_index)
    if not 0 <= prime_index < len(primes):
        raise AssertionError("prime index outside request")
    p = primes[prime_index]

    output = Path(output)
    metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
    coordinate_bytes = (output / "coordinate-map.json").read_bytes()
    coordinate_map = json.loads(coordinate_bytes)
    if _sha256_bytes(_canonical_json_bytes(coordinate_map)) != metadata["coordinate_map_sha256"]:
        raise AssertionError("coordinate map digest mismatch")
    if metadata["request_id"] != request["request_id"]:
        raise AssertionError("artifact request identity mismatch")
    if metadata["section_mode"] != SECTION_MODE or coordinate_map["section_mode"] != SECTION_MODE:
        raise AssertionError("artifact section mode mismatch")
    if int(metadata["prime_index"]) != prime_index or int(metadata["prime"]) != p:
        raise AssertionError("artifact prime identity mismatch")
    if int(metadata["reference_prime"]) != REFERENCE_PRIME:
        raise AssertionError("artifact reference-prime drift")
    if metadata["reference_protected_head"] != REFERENCE_PROTECTED_HEAD:
        raise AssertionError("artifact reference protected-head drift")
    if int(metadata["reference_sweep_run_id"]) != REFERENCE_SWEEP_RUN_ID:
        raise AssertionError("artifact reference sweep-run drift")
    if metadata["reference_profile_report_id"] != REFERENCE_PROFILE_REPORT_ID:
        raise AssertionError("artifact reference profile drift")
    if int(metadata["chunk_index"]) != int(chunk_index):
        raise AssertionError("artifact chunk identity mismatch")
    start, stop = chunk_ranges(request)[int(chunk_index)]
    if [metadata["n_start"], metadata["n_stop"]] != [start, stop]:
        raise AssertionError("artifact n-range mismatch")

    expected_pivot_sha = str(request["expected_pivot_sha256"])
    if metadata["pivot_sha256"] != expected_pivot_sha:
        raise AssertionError("artifact pivot digest mismatch")
    if metadata["coordinate_map_sha256"] != str(request["reference_coordinate_map_sha256"]):
        raise AssertionError("artifact coordinate map differs from admitted reference section")
    pivots = [int(x) for x in coordinate_map["pivot_indices"]]
    if len(pivots) != EXPECTED_RANK or lex_pivot_sweep._pivot_sha(pivots) != expected_pivot_sha:
        raise AssertionError("artifact pivot set mismatch")
    pivot_set = set(pivots)
    nonpivots = np.asarray([i for i in range(E1_COLUMNS) if i not in pivot_set], dtype=np.int64)
    if len(nonpivots) != E1_COLUMNS - EXPECTED_RANK:
        raise AssertionError("artifact nonpivot dimension mismatch")

    with np.load(output / "sections.npz", allow_pickle=False) as archive:
        sections = np.asarray(archive["sections"])
    expected_shape = (stop - start + 1, E1_COLUMNS, STANDALONE_BLOCKS)
    if sections.shape != expected_shape or sections.dtype != np.dtype("<i4"):
        raise AssertionError(f"section array drift: {sections.shape} {sections.dtype}")
    records = metadata["records"]
    if len(records) != sections.shape[0]:
        raise AssertionError("record count drift")
    for index, record in enumerate(records):
        n = start + index
        if int(record["n"]) != n or int(record["prime"]) != p:
            raise AssertionError("record n/prime ordering drift")
        if int(record["rank"]) != EXPECTED_RANK:
            raise AssertionError("rank failure in preserved artifact")
        if int(record["solver_nbad"]) != 0 or int(record["fresh_violations"]) != 0:
            raise AssertionError("failed solve preserved as evidence")
        if record["pivot_sha256"] != expected_pivot_sha:
            raise AssertionError(f"pivot drift preserved at n={n}")
        section = np.asarray(sections[index], dtype="<i4", order="C")
        if np.count_nonzero(section[nonpivots] % p):
            raise AssertionError(f"nonpivot coordinate violation at n={n}")
        if _sha256_bytes(section.tobytes(order="C")) != record["primitive_section_sha256"]:
            raise AssertionError(f"primitive section digest mismatch at n={n}")
        a0 = int(record["a0_mod_p"]) % p
        normalized_digest = record["normalized_section_sha256"]
        if a0:
            inv = pow(a0, p - 2, p)
            normalized = np.asarray((section.astype(object) * inv) % p, dtype="<i4", order="C")
            if _sha256_bytes(normalized.tobytes(order="C")) != normalized_digest:
                raise AssertionError(f"normalized section digest mismatch at n={n}")
        elif normalized_digest is not None:
            raise AssertionError("normalized digest present at singular a0 fiber")

    return {
        "request_id": request["request_id"],
        "prime_index": prime_index,
        "prime": p,
        "chunk_index": int(chunk_index),
        "n_start": start,
        "n_stop": stop,
        "samples_verified": len(records),
        "pivot_sha256": expected_pivot_sha,
        "coordinate_map_sha256": metadata["coordinate_map_sha256"],
        "proof_effect": metadata["proof_effect"],
        "promotion_effect": metadata["promotion_effect"],
    }


def verify_prime_sweep(
    request_path: Path | str,
    prime_index: int,
    outputs: list[Path | str],
) -> dict[str, Any]:
    request = load_request(request_path)
    if len(outputs) != int(request["chunks"]):
        raise AssertionError("full prime sweep verification requires every chunk")
    prime_index = int(prime_index)
    p = int(request["primes"][prime_index])
    expected_pivot_sha = str(request["expected_pivot_sha256"])
    coordinate_map_sha = None
    verified = 0
    next_n = int(request["n_start"])
    for chunk_index, output in enumerate(outputs):
        result = verify_chunk(request_path, prime_index, chunk_index, output)
        if result["n_start"] != next_n:
            raise AssertionError("full prime sweep coverage gap or overlap")
        next_n = result["n_stop"] + 1
        verified += int(result["samples_verified"])
        if result["pivot_sha256"] != expected_pivot_sha:
            raise AssertionError("full prime sweep pivot drift")
        if coordinate_map_sha is None:
            coordinate_map_sha = result["coordinate_map_sha256"]
        elif result["coordinate_map_sha256"] != coordinate_map_sha:
            raise AssertionError("full prime sweep coordinate map drift")
    if next_n != int(request["n_stop"]) + 1:
        raise AssertionError("full prime sweep terminal coverage drift")
    total = int(request["n_stop"]) - int(request["n_start"]) + 1
    if verified != total:
        raise AssertionError("full prime sweep sample count drift")
    return {
        "request_id": request["request_id"],
        "prime_index": prime_index,
        "prime": p,
        "samples_verified": verified,
        "n_start": int(request["n_start"]),
        "n_stop": int(request["n_stop"]),
        "pivot_sha256": expected_pivot_sha,
        "coordinate_map_sha256": coordinate_map_sha,
        "rational_degree_test_bound": request["rational_degree_test_bound"],
        "proof_effect": request["proof_effect"],
        "promotion_effect": request["promotion_effect"],
    }
