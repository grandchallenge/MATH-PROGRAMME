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
import affine_sweep
import lex_pivot_sweep

SOURCE_REPOSITORY = lex_pivot_sweep.SOURCE_REPOSITORY
SOURCE_COMMIT = lex_pivot_sweep.SOURCE_COMMIT
SOURCE_TREE = lex_pivot_sweep.SOURCE_TREE
SOURCE_FILES = dict(lex_pivot_sweep.SOURCE_FILES)

SECTION_MODE = lex_pivot_sweep.SECTION_MODE
EXPECTED_RANK = lex_pivot_sweep.EXPECTED_RANK
E1_COLUMNS = lex_pivot_sweep.E1_COLUMNS
STANDALONE_BLOCKS = lex_pivot_sweep.STANDALONE_BLOCKS
ANCHOR_PRIME = 4194301
ANCHOR_PROFILE_REPORT_ID = "OZ-RT-BZ-T3-016-A-LEX-PIVOT-RATIONAL-PROFILE-001"
ANCHOR_PROFILE_PROTECTED_HEAD = "510d09d164f4b0dc80388877edd58c6cb3a828af"
ANCHOR_PROFILE_BLOB_SHA = "6a22e190be3c0d4fe687a9154608134e15d1f94a"
ANCHOR_NORMALIZED_DATASET_SHA256 = "6ef4b8fcf5d60a764fe0ddf809d9e54de6c22e4a57d743aa8f14c24c7a595348"
ANCHOR_PIVOT_SHA256 = "3c1ce5a9603bf7c59ff312d4a22da9ab1d8a68a8ac34205cb192540a871fbdfe"
DEFAULT_REQUEST = HERE / "LEX_PIVOT_MULTIPRIME_REQUEST.json"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _is_prime(value: int) -> bool:
    n = int(value)
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def load_request(path: Path | str = DEFAULT_REQUEST) -> dict[str, Any]:
    request = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_request(request)
    return request


def validate_request(request: dict[str, Any]) -> dict[str, Any]:
    required = {
        "schema_version",
        "request_id",
        "enabled",
        "section_mode",
        "expected_pivot_sha256",
        "anchor_profile",
        "source_commit",
        "source_tree",
        "replay_primes",
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
        raise AssertionError(f"multiprime lex request missing fields: {missing}")
    if request["schema_version"] != "1.0.0":
        raise AssertionError("unsupported multiprime lex request schema")
    if not isinstance(request["request_id"], str) or not request["request_id"]:
        raise AssertionError("request_id must be non-empty")
    if not isinstance(request["enabled"], bool):
        raise AssertionError("enabled must be boolean")
    if request["section_mode"] != SECTION_MODE:
        raise AssertionError("multiprime lex section mode drift")
    if request["expected_pivot_sha256"] != ANCHOR_PIVOT_SHA256:
        raise AssertionError("multiprime lex pivot identity drift")

    anchor = request["anchor_profile"]
    if not isinstance(anchor, dict):
        raise AssertionError("anchor_profile must be an object")
    expected_anchor = {
        "report_id": ANCHOR_PROFILE_REPORT_ID,
        "protected_head": ANCHOR_PROFILE_PROTECTED_HEAD,
        "profile_blob_sha": ANCHOR_PROFILE_BLOB_SHA,
        "prime": ANCHOR_PRIME,
        "normalized_dataset_sha256": ANCHOR_NORMALIZED_DATASET_SHA256,
    }
    for key, expected in expected_anchor.items():
        if anchor.get(key) != expected:
            raise AssertionError(f"anchor profile drift for {key}")

    if request["source_commit"] != SOURCE_COMMIT:
        raise AssertionError("source commit drift")
    if request["source_tree"] != SOURCE_TREE:
        raise AssertionError("source tree drift")

    primes = request["replay_primes"]
    if not isinstance(primes, list) or not 2 <= len(primes) <= 8:
        raise AssertionError("replay_primes must contain between two and eight primes")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in primes):
        raise AssertionError("replay_primes must contain integers")
    if primes != sorted(primes) or len(set(primes)) != len(primes):
        raise AssertionError("replay_primes must be strictly increasing and unique")
    if ANCHOR_PRIME in primes:
        raise AssertionError("replay_primes must be independent of the admitted anchor prime")

    nb = int(request["solver_block_size"])
    if nb < 1 or nb > 192:
        raise AssertionError("solver block size outside fastlin bound")
    for prime in primes:
        if not _is_prime(prime):
            raise AssertionError(f"replay modulus is not prime: {prime}")
        if nb * (prime - 1) ** 2 >= 2**53:
            raise AssertionError(f"float64 modular accumulation exactness bound violated at p={prime}")

    if int(request["n_start"]) != 3 or int(request["n_stop"]) != 384:
        raise AssertionError("multiprime replay must preserve the admitted n=3..384 range")
    if int(request["chunks"]) != 4:
        raise AssertionError("multiprime workflow matrix is fixed to four chunks")
    workers = int(request["workers_per_chunk"])
    if not 1 <= workers <= 8:
        raise AssertionError("workers_per_chunk outside governed bound")
    if int(request["fit_extra_rows"]) < 1 or int(request["fresh_rows"]) < 1:
        raise AssertionError("fit and fresh row reserves must be positive")

    total = int(request["n_stop"]) - int(request["n_start"]) + 1
    fit_count = int(request["reconstruction_fit_count"])
    holdout_count = int(request["holdout_count"])
    if fit_count != 358 or holdout_count != 24 or fit_count + holdout_count != total:
        raise AssertionError("multiprime reconstruction partition must remain 358 fit / 24 holdout")
    request["rational_degree_test_bound"] = lex_pivot_sweep.max_rational_degree_bound(fit_count)
    if request["rational_degree_test_bound"] != 177:
        raise AssertionError("multiprime rational degree ceiling drift")

    if request["evidence_effect"] != "MODULAR_CANDIDATE_ONLY":
        raise AssertionError("multiprime sweep may emit modular candidate evidence only")
    if request["proof_effect"] != "NONE" or request["promotion_effect"] != "NONE":
        raise AssertionError("multiprime claim firewall drift")
    return request


def chunk_ranges(request: dict[str, Any]) -> list[tuple[int, int]]:
    validate_request(request)
    start = int(request["n_start"])
    stop = int(request["n_stop"])
    chunks = int(request["chunks"])
    total = stop - start + 1
    q, r = divmod(total, chunks)
    output: list[tuple[int, int]] = []
    cursor = start
    for index in range(chunks):
        size = q + (1 if index < r else 0)
        if size <= 0:
            raise AssertionError("empty multiprime lex chunk")
        output.append((cursor, cursor + size - 1))
        cursor += size
    if cursor != stop + 1:
        raise AssertionError("multiprime chunk partition drift")
    return output


def verify_source_checkout(source: Path | str, request: dict[str, Any]) -> dict[str, Any]:
    validate_request(dict(request))
    root = Path(source).resolve()
    head = affine_sweep._git(root, "rev-parse", "HEAD")
    tree = affine_sweep._git(root, "rev-parse", "HEAD^{tree}")
    if head != SOURCE_COMMIT:
        raise AssertionError(f"source head drift: {head}")
    if tree != SOURCE_TREE:
        raise AssertionError(f"source tree drift: {tree}")
    blobs: dict[str, str] = {}
    for _local_name, (remote_path, expected_blob) in sorted(SOURCE_FILES.items()):
        got = affine_sweep._git(root, "rev-parse", f"{SOURCE_COMMIT}:{remote_path}")
        if got != expected_blob:
            raise AssertionError(f"source blob drift for {remote_path}: {got} != {expected_blob}")
        blobs[remote_path] = got
    return {"commit": head, "tree": tree, "blobs": blobs}


def _require_prime(request: dict[str, Any], prime: int) -> int:
    p = int(prime)
    if p not in request["replay_primes"]:
        raise AssertionError(f"prime {p} is not authorized by the multiprime request")
    return p


def run_chunk(
    request_path: Path | str,
    source: Path | str,
    prime: int,
    chunk_index: int,
    output: Path | str,
) -> dict[str, Any]:
    request_path = Path(request_path)
    request = load_request(request_path)
    if not request["enabled"]:
        raise AssertionError("refusing to execute disabled multiprime lex request")
    p = _require_prime(request, prime)
    chunk_index = int(chunk_index)
    ranges = chunk_ranges(request)
    if not 0 <= chunk_index < len(ranges):
        raise AssertionError("chunk index outside multiprime request")
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
        initializer=lex_pivot_sweep._worker_init,
        initargs=(str(source), str(cache_path)),
    ) as pool:
        rows = list(pool.imap_unordered(lex_pivot_sweep._worker, tasks, chunksize=1))
    rows.sort(key=lambda item: item[0])

    expected_ns = list(range(start, stop + 1))
    if [row[0] for row in rows] != expected_ns:
        raise AssertionError("multiprime chunk n ordering/coverage drift")
    sections = np.stack([row[1] for row in rows]).astype("<i4", copy=False)
    records = [row[2]["record"] for row in rows]
    coordinate_map = rows[0][2]["coordinate_map"]
    for row in rows[1:]:
        if row[2]["coordinate_map"] != coordinate_map:
            raise AssertionError("pivot or coordinate map changed inside multiprime chunk")
    if coordinate_map["pivot_sha256"] != expected:
        raise AssertionError("multiprime chunk pivot digest differs from admitted anchor")

    coordinate_bytes = _canonical_json_bytes(coordinate_map)
    coordinate_sha = _sha256_bytes(coordinate_bytes)
    np.savez_compressed(output / "sections.npz", sections=sections)
    (output / "coordinate-map.json").write_bytes(coordinate_bytes)
    shutil.copyfile(request_path, output / "request.json")
    metadata = {
        "schema_version": "1.0.0",
        "request_id": request["request_id"],
        "section_mode": SECTION_MODE,
        "prime": p,
        "chunk_index": chunk_index,
        "n_start": start,
        "n_stop": stop,
        "sample_count": len(rows),
        "source": source_identity,
        "anchor_profile": request["anchor_profile"],
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
    prime: int,
    chunk_index: int,
    output: Path | str,
) -> dict[str, Any]:
    request_path = Path(request_path)
    request = load_request(request_path)
    p = _require_prime(request, prime)
    output = Path(output)

    preserved_request = output / "request.json"
    if preserved_request.read_bytes() != request_path.read_bytes():
        raise AssertionError("preserved multiprime request bytes differ from governed request")

    metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
    coordinate_bytes = (output / "coordinate-map.json").read_bytes()
    coordinate_map = json.loads(coordinate_bytes)
    if _sha256_bytes(_canonical_json_bytes(coordinate_map)) != metadata["coordinate_map_sha256"]:
        raise AssertionError("multiprime coordinate map digest mismatch")
    if metadata["request_id"] != request["request_id"]:
        raise AssertionError("multiprime artifact request identity mismatch")
    if metadata["anchor_profile"] != request["anchor_profile"]:
        raise AssertionError("multiprime artifact anchor-profile drift")
    if metadata["section_mode"] != SECTION_MODE or coordinate_map["section_mode"] != SECTION_MODE:
        raise AssertionError("multiprime artifact section mode mismatch")
    if int(metadata["prime"]) != p:
        raise AssertionError("multiprime artifact prime mismatch")
    if int(metadata["chunk_index"]) != int(chunk_index):
        raise AssertionError("multiprime artifact chunk identity mismatch")

    start, stop = chunk_ranges(request)[int(chunk_index)]
    if [metadata["n_start"], metadata["n_stop"]] != [start, stop]:
        raise AssertionError("multiprime artifact n-range mismatch")
    expected_pivot_sha = str(request["expected_pivot_sha256"])
    if metadata["pivot_sha256"] != expected_pivot_sha:
        raise AssertionError("multiprime artifact pivot digest mismatch")
    pivots = [int(x) for x in coordinate_map["pivot_indices"]]
    if len(pivots) != EXPECTED_RANK or lex_pivot_sweep._pivot_sha(pivots) != expected_pivot_sha:
        raise AssertionError("multiprime artifact pivot set mismatch")

    pivot_set = set(pivots)
    nonpivots = np.asarray([i for i in range(E1_COLUMNS) if i not in pivot_set], dtype=np.int64)
    if len(nonpivots) != E1_COLUMNS - EXPECTED_RANK:
        raise AssertionError("multiprime artifact nonpivot dimension mismatch")

    with np.load(output / "sections.npz", allow_pickle=False) as archive:
        sections = np.asarray(archive["sections"])
    expected_shape = (stop - start + 1, E1_COLUMNS, STANDALONE_BLOCKS)
    if sections.shape != expected_shape or sections.dtype != np.dtype("<i4"):
        raise AssertionError(f"multiprime section array drift: {sections.shape} {sections.dtype}")

    records = metadata["records"]
    if len(records) != sections.shape[0]:
        raise AssertionError("multiprime record count drift")
    for index, record in enumerate(records):
        n = start + index
        if int(record["n"]) != n or int(record["prime"]) != p:
            raise AssertionError("multiprime record identity drift")
        if int(record["rank"]) != EXPECTED_RANK:
            raise AssertionError("rank failure in preserved multiprime artifact")
        if int(record["solver_nbad"]) != 0 or int(record["fresh_violations"]) != 0:
            raise AssertionError("failed multiprime solve preserved as evidence")
        if record["pivot_sha256"] != expected_pivot_sha:
            raise AssertionError(f"multiprime pivot drift preserved at p={p} n={n}")
        section = np.asarray(sections[index], dtype="<i4", order="C")
        if np.count_nonzero(section[nonpivots] % p):
            raise AssertionError(f"multiprime nonpivot coordinate violation at p={p} n={n}")
        if _sha256_bytes(section.tobytes(order="C")) != record["primitive_section_sha256"]:
            raise AssertionError(f"multiprime primitive section digest mismatch at p={p} n={n}")
        a0 = int(record["a0_mod_p"]) % p
        normalized_digest = record["normalized_section_sha256"]
        if a0:
            inv = pow(a0, p - 2, p)
            normalized = np.asarray((section.astype(object) * inv) % p, dtype="<i4", order="C")
            if _sha256_bytes(normalized.tobytes(order="C")) != normalized_digest:
                raise AssertionError(f"multiprime normalized section digest mismatch at p={p} n={n}")
        elif normalized_digest is not None:
            raise AssertionError("normalized digest present at singular multiprime a0 fiber")

    return {
        "request_id": request["request_id"],
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
    prime: int,
    outputs: list[Path | str],
) -> dict[str, Any]:
    request = load_request(request_path)
    p = _require_prime(request, prime)
    if len(outputs) != int(request["chunks"]):
        raise AssertionError("prime-sweep verification requires every chunk")
    expected_pivot_sha = str(request["expected_pivot_sha256"])
    coordinate_map_sha: str | None = None
    verified = 0
    next_n = int(request["n_start"])
    for chunk_index, output in enumerate(outputs):
        result = verify_chunk(request_path, p, chunk_index, output)
        if result["n_start"] != next_n:
            raise AssertionError("prime-sweep coverage gap or overlap")
        next_n = result["n_stop"] + 1
        verified += int(result["samples_verified"])
        if result["pivot_sha256"] != expected_pivot_sha:
            raise AssertionError("prime-sweep pivot drift")
        if coordinate_map_sha is None:
            coordinate_map_sha = result["coordinate_map_sha256"]
        elif result["coordinate_map_sha256"] != coordinate_map_sha:
            raise AssertionError("prime-sweep coordinate map drift")
    if next_n != int(request["n_stop"]) + 1:
        raise AssertionError("prime-sweep terminal coverage drift")
    total = int(request["n_stop"]) - int(request["n_start"]) + 1
    if verified != total:
        raise AssertionError("prime-sweep sample count drift")
    return {
        "request_id": request["request_id"],
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


def verify_multiprime_sweep(
    request_path: Path | str,
    outputs_by_prime: dict[int, list[Path | str]],
) -> dict[str, Any]:
    request = load_request(request_path)
    expected_primes = [int(value) for value in request["replay_primes"]]
    if sorted(int(value) for value in outputs_by_prime) != expected_primes:
        raise AssertionError("multiprime output prime set differs from governed request")

    coordinate_map_sha: str | None = None
    results: list[dict[str, Any]] = []
    for prime in expected_primes:
        result = verify_prime_sweep(request_path, prime, outputs_by_prime[prime])
        if coordinate_map_sha is None:
            coordinate_map_sha = result["coordinate_map_sha256"]
        elif result["coordinate_map_sha256"] != coordinate_map_sha:
            raise AssertionError("coordinate-map identity changed across replay primes")
        results.append(result)

    return {
        "request_id": request["request_id"],
        "primes_verified": expected_primes,
        "prime_count": len(expected_primes),
        "samples_per_prime": int(request["n_stop"]) - int(request["n_start"]) + 1,
        "pivot_sha256": request["expected_pivot_sha256"],
        "coordinate_map_sha256": coordinate_map_sha,
        "evidence_effect": request["evidence_effect"],
        "proof_effect": request["proof_effect"],
        "promotion_effect": request["promotion_effect"],
    }
