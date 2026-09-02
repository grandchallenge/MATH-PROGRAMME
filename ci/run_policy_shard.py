#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance/policy_shard_registry.json"
TIMEOUT_EXIT = 124
MAX_OVERRIDE_TIMEOUT_SECONDS = 3600


def _command(entry: object) -> list[str]:
    if not isinstance(entry, list) or not entry or not all(isinstance(item, str) and item for item in entry):
        raise RuntimeError("invalid shard command")
    return list(entry)


def _execution_policy(data: dict[str, object]) -> tuple[float, dict[tuple[str, int], tuple[float, str]]]:
    execution = data.get("execution")
    if not isinstance(execution, dict):
        raise RuntimeError("policy shard execution envelope missing")
    default_raw = execution.get("default_command_timeout_seconds")
    if not isinstance(default_raw, (int, float)) or isinstance(default_raw, bool) or default_raw <= 0:
        raise RuntimeError("default policy shard command timeout invalid")
    default_timeout = float(default_raw)

    shards = data.get("shards")
    if not isinstance(shards, dict):
        raise RuntimeError("policy shard registry missing shards")
    rows = execution.get("timeout_overrides")
    if not isinstance(rows, list):
        raise RuntimeError("policy shard timeout overrides invalid")

    overrides: dict[tuple[str, int], tuple[float, str]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise RuntimeError("policy shard timeout override must be an object")
        shard = row.get("shard")
        index = row.get("command_index")
        timeout_raw = row.get("timeout_seconds")
        reason = row.get("reason")
        expected = row.get("command")
        if not isinstance(shard, str) or not shard:
            raise RuntimeError("policy shard timeout override shard invalid")
        if not isinstance(index, int) or isinstance(index, bool) or index < 1:
            raise RuntimeError("policy shard timeout override command_index invalid")
        if not isinstance(timeout_raw, (int, float)) or isinstance(timeout_raw, bool):
            raise RuntimeError("policy shard timeout override timeout invalid")
        timeout = float(timeout_raw)
        if timeout <= default_timeout or timeout > MAX_OVERRIDE_TIMEOUT_SECONDS:
            raise RuntimeError("policy shard timeout override must exceed default and remain <= 3600 seconds")
        if not isinstance(reason, str) or len(reason.strip()) < 20:
            raise RuntimeError("policy shard timeout override reason is missing or too short")
        expected_command = _command(expected)
        commands = shards.get(shard)
        if not isinstance(commands, list) or index > len(commands):
            raise RuntimeError(f"policy shard timeout override target missing: {shard}#{index}")
        actual_command = _command(commands[index - 1])
        if actual_command != expected_command:
            raise RuntimeError(f"policy shard timeout override command drift: {shard}#{index}")
        key = (shard, index)
        if key in overrides:
            raise RuntimeError(f"duplicate policy shard timeout override: {shard}#{index}")
        overrides[key] = (timeout, reason.strip())
    return default_timeout, overrides


def _terminate_process_tree(proc: subprocess.Popen[str]) -> None:
    if proc.poll() is not None:
        return
    try:
        if os.name == "posix":
            os.killpg(proc.pid, signal.SIGTERM)
        else:
            proc.terminate()
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            os.killpg(proc.pid, signal.SIGKILL)
        else:
            proc.kill()
        proc.wait()


def _stream_command(
    cmd: list[str],
    *,
    log_handle,
    timeout_seconds: float,
    env: dict[str, str] | None = None,
) -> tuple[int, bool]:
    proc = subprocess.Popen(
        cmd,
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        start_new_session=(os.name == "posix"),
    )
    if proc.stdout is None:
        raise RuntimeError("policy shard subprocess stdout unavailable")

    reader_errors: list[BaseException] = []

    def relay() -> None:
        try:
            for line in proc.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log_handle.write(line)
                log_handle.flush()
        except BaseException as exc:  # pragma: no cover - defensive relay failure
            reader_errors.append(exc)

    reader = threading.Thread(target=relay, name="policy-shard-output", daemon=True)
    reader.start()
    timed_out = False
    try:
        returncode = proc.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        _terminate_process_tree(proc)
        returncode = TIMEOUT_EXIT
    reader.join(timeout=5)
    if reader.is_alive():
        raise RuntimeError("policy shard output relay did not terminate")
    if reader_errors:
        raise RuntimeError(f"policy shard output relay failed: {reader_errors[0]}")
    return int(returncode), timed_out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", required=True)
    parser.add_argument("--log")
    args = parser.parse_args()
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        if data.get("registry_id") != "MP-POLICY-SHARDS-001":
            raise RuntimeError("policy shard registry identity drift")
        commands = data.get("shards", {}).get(args.shard)
        if not isinstance(commands, list) or not commands:
            raise RuntimeError(f"unknown or empty policy shard: {args.shard}")
        default_timeout, overrides = _execution_policy(data)
        log = Path(args.log) if args.log else ROOT / f"policy-shard-{args.shard}.log"
        shard_started = time.perf_counter()
        with log.open("w", encoding="utf-8") as handle:
            for index, entry in enumerate(commands, 1):
                cmd = _command(entry)
                rendered = " ".join(cmd)
                timeout, reason = overrides.get((args.shard, index), (default_timeout, "default"))
                source = "override" if (args.shard, index) in overrides else "default"
                prefix = f"[{args.shard} {index}/{len(commands)}] {rendered}"
                print(prefix, flush=True)
                print(
                    f"POLICY_SHARD_START shard={args.shard} operation={index} timeout_seconds={timeout:.3f} timeout_source={source}",
                    flush=True,
                )
                if source == "override":
                    print(
                        f"POLICY_SHARD_TIMEOUT_OVERRIDE shard={args.shard} operation={index} reason={json.dumps(reason)}",
                        flush=True,
                    )
                handle.write("$ " + rendered + "\n")
                handle.flush()
                child_env = os.environ.copy()
                child_env["GCL_POLICY_SHARD"] = args.shard
                child_env["GCL_POLICY_SHARD_OPERATION"] = str(index)
                started = time.perf_counter()
                returncode, timed_out = _stream_command(
                    cmd,
                    log_handle=handle,
                    timeout_seconds=timeout,
                    env=child_env,
                )
                elapsed = time.perf_counter() - started
                if timed_out:
                    timing = (
                        f"POLICY_SHARD_TIMEOUT shard={args.shard} operation={index} "
                        f"seconds={elapsed:.3f} limit_seconds={timeout:.3f}\n"
                    )
                    print(timing, end="", flush=True)
                    handle.write(timing)
                    handle.flush()
                    return TIMEOUT_EXIT
                timing = (
                    f"POLICY_SHARD_TIMING shard={args.shard} operation={index} "
                    f"seconds={elapsed:.3f} status={'PASS' if returncode == 0 else 'FAIL'}\n"
                )
                print(timing, end="", flush=True)
                handle.write(timing)
                handle.flush()
                if returncode:
                    return returncode
        total = time.perf_counter() - shard_started
        print(f"POLICY_SHARD_TIMING_TOTAL shard={args.shard} seconds={total:.3f}")
        print(f"policy shard {args.shard}: success")
        return 0
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"policy shard execution error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
