from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import affine_probe

SOURCE_REPOSITORY = affine_probe.SOURCE_REPOSITORY
SOURCE_COMMIT = affine_probe.SOURCE_COMMIT
SOURCE_TREE = "be780558454b704bdd016a3070d698c2e106e2b8"
SOURCE_FILES = dict(affine_probe.SOURCE_FILES)

M_ORDER = 7
E1_COLUMNS = 1624
GAUGE_COORDINATES = 576
FREE_COORDINATES = 1048
STANDALONE_BLOCKS = 7
DEFAULT_REQUEST = HERE / "AFFINE_SWEEP_REQUEST.json"

_MODULES: dict[str, Any] = {}
_SOURCE_ROOT: Path | None = None


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _git(source: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(source), *args],
        check=True,
        capture_output=True,
        text=True,
        timeout=90,
    )
    return completed.stdout.strip()


def load_request(path: Path | str = DEFAULT_REQUEST) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_request(value)
    return value


def validate_request(request: dict) -> dict:
    required = {
        "schema_version",
        "request_id",
        "enabled",
        "source_commit",
        "source_tree",
        "prime",
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
        raise AssertionError(f"affine sweep request missing fields: {missing}")
    if request["schema_version"] != "1.0.0":
        raise AssertionError("unsupported affine sweep request schema")
    if not isinstance(request["request_id"], str) or not request["request_id"]:
        raise AssertionError("request_id must be non-empty")
    if not isinstance(request["enabled"], bool):
        raise AssertionError("enabled must be boolean")
    if request["source_commit"] != SOURCE_COMMIT:
        raise AssertionError("source commit drift")
    if request["source_tree"] != SOURCE_TREE:
        raise AssertionError("source tree drift")
    if int(request["prime"]) != 4194301:
        raise AssertionError("first affine sweep prime must remain 4194301")
    if int(request["n_start"]) < 1 or int(request["n_stop"]) < int(request["n_start"]):
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
    p = int(request["prime"])
    if nb * (p - 1) ** 2 >= 2**53:
        raise AssertionError("float64 modular accumulation exactness bound violated")
    total = int(request["n_stop"]) - int(request["n_start"]) + 1
    fit_count = int(request["reconstruction_fit_count"])
    holdout_count = int(request["holdout_count"])
    if fit_count < 3 or holdout_count < 1 or fit_count + holdout_count != total:
        raise AssertionError("reconstruction/holdout partition does not cover sample range")
    if request["evidence_effect"] != "MODULAR_CANDIDATE_ONLY":
        raise AssertionError("sweep may emit modular candidate evidence only")
    if request["proof_effect"] != "NONE" or request["promotion_effect"] != "NONE":
        raise AssertionError("claim firewall drift")
    request["rational_degree_test_bound"] = max_rational_degree_bound(fit_count)
    return request


def max_rational_degree_bound(sample_count: int) -> int:
    if sample_count < 3:
        raise AssertionError("at least three samples required")
    return (int(sample_count) - 3) // 2


def chunk_ranges(request: dict) -> list[tuple[int, int]]:
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
            raise AssertionError("empty affine sweep chunk")
        out.append((cursor, cursor + size - 1))
        cursor += size
    if cursor != stop + 1:
        raise AssertionError("chunk partition drift")
    return out


def verify_source_checkout(source: Path | str, request: dict) -> dict:
    request = validate_request(dict(request))
    root = Path(source).resolve()
    head = _git(root, "rev-parse", "HEAD")
    tree = _git(root, "rev-parse", "HEAD^{tree}")
    if head != request["source_commit"]:
        raise AssertionError(f"source head drift: {head}")
    if tree != request["source_tree"]:
        raise AssertionError(f"source tree drift: {tree}")
    blobs: dict[str, str] = {}
    for _local_name, (remote_path, expected_blob) in sorted(SOURCE_FILES.items()):
        got = _git(root, "rev-parse", f"{SOURCE_COMMIT}:{remote_path}")
        if got != expected_blob:
            raise AssertionError(f"source blob drift for {remote_path}: {got} != {expected_blob}")
        blobs[remote_path] = got
    return {"commit": head, "tree": tree, "blobs": blobs}


def _install_source_modules(source: Path, cache_path: Path, *, prewarm: bool) -> None:
    global _MODULES, _SOURCE_ROOT
    source = source.resolve()
    z5la = source / "work" / "z5la"
    if str(z5la) not in sys.path:
        sys.path.insert(0, str(z5la))
    import fastlin
    import o_scan
    import o_zero
    import ordm
    import qrow
    import solve

    qrow.SRC = str(source / "work" / "z5cf" / "Qrow_phicert.m")
    qrow.CACHE = str(cache_path)
    if prewarm:
        qrow._D = None
        qrow._load()
        if not cache_path.is_file():
            raise AssertionError("Q-row cache prewarm failed")
    _MODULES = {
        "fastlin": fastlin,
        "o_scan": o_scan,
        "o_zero": o_zero,
        "ordm": ordm,
        "qrow": qrow,
        "solve": solve,
    }
    _SOURCE_ROOT = source


def _worker_init(source: str, cache_path: str) -> None:
    _install_source_modules(Path(source), Path(cache_path), prewarm=False)


def _peval(coeffs: list, x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(coeffs):
        value = (value * x + int(coefficient)) % p
    return value


def _shape(n: int, p: int, fit_rows: int, fresh_rows: int, nb: int) -> tuple[np.ndarray, dict]:
    fastlin = _MODULES["fastlin"]
    o_scan = _MODULES["o_scan"]
    o_zero = _MODULES["o_zero"]
    ordm = _MODULES["ordm"]
    solve = _MODULES["solve"]
    source = _SOURCE_ROOT
    if source is None:
        raise AssertionError("source modules not initialized")

    D = o_scan.dens(M_ORDER)["E1"]
    dk0 = sum(mu * abs(f[2]) for f, mu in D)
    dl0 = sum(mu * abs(f[3]) for f, mu in D)
    ans = solve.Ansatz(
        D,
        D,
        dk0 + 18,
        dl0 + 18,
        dk0 + 18,
        dl0 + 18,
        force_k=1,
        force_l=1,
    )
    if ans.nc != E1_COLUMNS:
        raise AssertionError(f"E1 column drift: {ans.nc}")

    gauge = [
        i
        for i, mon in enumerate(ans.mons_r)
        if 2 <= mon[0] <= 25 and 0 <= mon[1] <= 23
    ]
    if len(gauge) != GAUGE_COORDINATES:
        raise AssertionError("canonical gauge coordinate drift")
    gauge_set = set(gauge)
    free = [i for i in range(ans.nc) if i not in gauge_set]
    if len(free) != FREE_COORDINATES:
        raise AssertionError("canonical free-coordinate drift")

    lift = json.loads((source / "work" / "z5la" / "a_lift.json").read_text(encoding="utf-8"))
    avec = np.asarray([_peval(row, n, p) for row in lift["a"]], dtype=np.int64)

    pd = ordm.PDm("w3", p, n, M_ORDER, fit_rows + fresh_rows)
    Acol = ordm.acols(pd)
    stand = [j for j in pd.free if len(pd.B[j]) > 0]
    if len(stand) != STANDALONE_BLOCKS:
        raise AssertionError(f"standalone block count drift: {len(stand)}")
    _r0, _r1, _s0, _s1, op = o_zero.design(pd, ans)

    rhs = np.zeros((pd.npts, len(stand)), dtype=np.int64)
    avec_object = avec.astype(object)
    for column, block in enumerate(stand):
        slab = Acol[block * pd.npts : (block + 1) * pd.npts].astype(object)
        rhs[:, column] = [int(x) for x in (-(slab @ avec_object)) % p]

    free_array = np.asarray(free)
    fit_matrix = op[:fit_rows, free_array].astype(np.int64)
    Xfree, rank, piv, nbad = fastlin.solve(fit_matrix, rhs[:fit_rows], p, nb=nb)
    Xfree = np.asarray(Xfree, dtype=np.int64) % p
    if rank != FREE_COORDINATES or len(piv) != FREE_COORDINATES or nbad != 0:
        raise RuntimeError(f"canonical affine solve failed: rank={rank} piv={len(piv)} nbad={nbad}")

    fresh = o_zero.matmul_mod(
        op[fit_rows:, free_array],
        Xfree.astype(np.float64),
        p,
    )
    fresh = (fresh - rhs[fit_rows:]) % p
    fresh_violations = int(np.count_nonzero(fresh))
    if fresh_violations:
        raise RuntimeError(f"fresh residual violations: {fresh_violations}")

    free_i4 = np.asarray(Xfree, dtype="<i4", order="C")
    primitive_digest = _sha256_bytes(free_i4.tobytes(order="C"))
    a0 = int(avec[0]) % p
    normalized_digest = None
    if a0:
        inv = pow(a0, p - 2, p)
        normalized = np.asarray((Xfree.astype(object) * inv) % p, dtype="<i4", order="C")
        normalized_digest = _sha256_bytes(normalized.tobytes(order="C"))

    coordinate_map = {
        "e1_columns": ans.nc,
        "r_columns": len(ans.mons_r),
        "s_columns": len(ans.mons_s),
        "mons_r": [[int(a), int(b)] for a, b in ans.mons_r],
        "mons_s": [[int(a), int(b)] for a, b in ans.mons_s],
        "gauge_indices": gauge,
        "free_indices": free,
        "standalone_blocks": [str(pd.B[j]) for j in stand],
    }
    record = {
        "n": n,
        "prime": p,
        "a_mod_p": [int(x) for x in avec],
        "a0_mod_p": a0,
        "free_rank": int(rank),
        "solver_nbad": int(nbad),
        "fit_rows": fit_rows,
        "fresh_rows": fresh_rows,
        "fresh_violations": fresh_violations,
        "primitive_section_sha256": primitive_digest,
        "normalized_section_sha256": normalized_digest,
    }
    return free_i4, {"record": record, "coordinate_map": coordinate_map}


def _worker(task: tuple[int, int, int, int, int]) -> tuple[int, np.ndarray, dict]:
    n, p, fit_rows, fresh_rows, nb = task
    section, data = _shape(n, p, fit_rows, fresh_rows, nb)
    return n, section, data


def run_chunk(
    request_path: Path | str,
    source: Path | str,
    chunk_index: int,
    output: Path | str,
) -> dict:
    request_path = Path(request_path)
    request = load_request(request_path)
    if not request["enabled"]:
        raise AssertionError("refusing to execute disabled affine sweep request")
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
    _install_source_modules(source, cache_path, prewarm=True)

    p = int(request["prime"])
    fit_rows = FREE_COORDINATES + int(request["fit_extra_rows"])
    fresh_rows = int(request["fresh_rows"])
    nb = int(request["solver_block_size"])
    tasks = [(n, p, fit_rows, fresh_rows, nb) for n in range(start, stop + 1)]
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
        raise AssertionError("chunk n ordering/coverage drift")
    sections = np.stack([row[1] for row in rows]).astype("<i4", copy=False)
    records = [row[2]["record"] for row in rows]
    coordinate_map = rows[0][2]["coordinate_map"]
    coordinate_bytes = _canonical_json_bytes(coordinate_map)
    coordinate_sha = _sha256_bytes(coordinate_bytes)
    for row in rows[1:]:
        if row[2]["coordinate_map"] != coordinate_map:
            raise AssertionError("coordinate map changed inside chunk")

    np.savez_compressed(output / "sections.npz", sections=sections)
    (output / "coordinate-map.json").write_bytes(coordinate_bytes)
    shutil.copyfile(request_path, output / "request.json")
    metadata = {
        "schema_version": "1.0.0",
        "request_id": request["request_id"],
        "chunk_index": chunk_index,
        "n_start": start,
        "n_stop": stop,
        "sample_count": len(rows),
        "source": source_identity,
        "prime": p,
        "fit_rows": fit_rows,
        "fresh_rows": fresh_rows,
        "free_coordinates": FREE_COORDINATES,
        "standalone_blocks": STANDALONE_BLOCKS,
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
    chunk_index: int,
    output: Path | str,
) -> dict:
    request = load_request(request_path)
    output = Path(output)
    metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
    coordinate_bytes = (output / "coordinate-map.json").read_bytes()
    coordinate_map = json.loads(coordinate_bytes)
    if _sha256_bytes(_canonical_json_bytes(coordinate_map)) != metadata["coordinate_map_sha256"]:
        raise AssertionError("coordinate map digest mismatch")
    if metadata["request_id"] != request["request_id"]:
        raise AssertionError("artifact request identity mismatch")
    if int(metadata["chunk_index"]) != int(chunk_index):
        raise AssertionError("artifact chunk identity mismatch")
    start, stop = chunk_ranges(request)[int(chunk_index)]
    if [metadata["n_start"], metadata["n_stop"]] != [start, stop]:
        raise AssertionError("artifact n-range mismatch")
    with np.load(output / "sections.npz", allow_pickle=False) as archive:
        sections = np.asarray(archive["sections"])
    expected_shape = (stop - start + 1, FREE_COORDINATES, STANDALONE_BLOCKS)
    if sections.shape != expected_shape or sections.dtype != np.dtype("<i4"):
        raise AssertionError(f"section array drift: {sections.shape} {sections.dtype}")
    records = metadata["records"]
    if len(records) != sections.shape[0]:
        raise AssertionError("record count drift")
    p = int(request["prime"])
    for index, record in enumerate(records):
        n = start + index
        if int(record["n"]) != n:
            raise AssertionError("record n ordering drift")
        if int(record["free_rank"]) != FREE_COORDINATES:
            raise AssertionError("free-rank failure in preserved artifact")
        if int(record["solver_nbad"]) != 0 or int(record["fresh_violations"]) != 0:
            raise AssertionError("failed solve preserved as evidence")
        section = np.asarray(sections[index], dtype="<i4", order="C")
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
        "chunk_index": int(chunk_index),
        "n_start": start,
        "n_stop": stop,
        "samples_verified": len(records),
        "coordinate_map_sha256": metadata["coordinate_map_sha256"],
        "proof_effect": metadata["proof_effect"],
        "promotion_effect": metadata["promotion_effect"],
    }
