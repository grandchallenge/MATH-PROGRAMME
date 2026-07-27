"""Finite-step fixture for NS-WP06 reduction-interface tests.

This module is not a Navier–Stokes simulation and is not evidence for
undecidability, blow-up, or independence. It provides a deterministic toy
interface that forces callers to distinguish:

* machine halting within a finite budget;
* activation of a post-halting scalar growth gate; and
* numerical threshold crossing.

The scalar gate obeys ``y' = y^2 - nu*y`` after activation and ``y' = -nu*y``
before activation. Explicit Euler is used only as a reproducible software
fixture. The module intentionally exposes no command-line entry point.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Instruction:
    """One instruction for a bounded two-counter machine."""

    op: str
    register: int = 0
    target: int = 0
    zero_target: int = 0


@dataclass(frozen=True)
class RunResult:
    halted: bool
    halt_step: int | None
    counter_state: tuple[int, int]
    gate_crossed: bool
    gate_cross_step: int | None
    final_y: float


def _is_plain_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_program(program: Sequence[Instruction]) -> None:
    if not program:
        raise ValueError("program must contain at least one instruction")
    valid_ops = {"inc", "dec_jump", "halt"}
    for index, instruction in enumerate(program):
        if not isinstance(instruction, Instruction):
            raise TypeError(f"instruction {index}: expected Instruction")
        if instruction.op not in valid_ops:
            raise ValueError(f"instruction {index}: unsupported op {instruction.op!r}")
        if not _is_plain_int(instruction.register) or instruction.register not in (0, 1):
            raise ValueError(f"instruction {index}: register must be integer 0 or 1")
        for name, target in (
            ("target", instruction.target),
            ("zero_target", instruction.zero_target),
        ):
            if not _is_plain_int(target) or target < 0 or target >= len(program):
                raise ValueError(f"instruction {index}: {name} out of range")


def _validate_numerics(
    *,
    machine_steps: int,
    dt: float,
    nu: float,
    gate_initial: float,
    threshold: float,
    substeps_per_machine_step: int,
) -> None:
    if not _is_plain_int(machine_steps) or machine_steps < 0:
        raise ValueError("machine_steps must be a non-negative integer")
    if not _is_plain_int(substeps_per_machine_step) or substeps_per_machine_step <= 0:
        raise ValueError("substeps_per_machine_step must be a positive integer")
    for name, value in (
        ("dt", dt),
        ("nu", nu),
        ("gate_initial", gate_initial),
        ("threshold", threshold),
    ):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{name} must be a finite real number")
        if not math.isfinite(float(value)):
            raise ValueError(f"{name} must be finite")
    if dt <= 0 or nu < 0 or gate_initial <= 0:
        raise ValueError("dt, nu, and gate_initial are inconsistent")
    if threshold <= gate_initial:
        raise ValueError("threshold must exceed gate_initial")


def run_fixture(
    program: Sequence[Instruction],
    initial_counters: Iterable[int] = (0, 0),
    *,
    machine_steps: int = 100,
    dt: float = 1e-3,
    nu: float = 0.25,
    gate_initial: float = 2.0,
    threshold: float = 1e6,
    substeps_per_machine_step: int = 100,
) -> RunResult:
    """Run a bounded machine and a post-halting scalar growth gate."""

    _validate_program(program)
    _validate_numerics(
        machine_steps=machine_steps,
        dt=dt,
        nu=nu,
        gate_initial=gate_initial,
        threshold=threshold,
        substeps_per_machine_step=substeps_per_machine_step,
    )

    counters = tuple(initial_counters)
    if len(counters) != 2 or any(not _is_plain_int(value) or value < 0 for value in counters):
        raise ValueError("initial_counters must contain two non-negative integers")
    mutable_counters = [counters[0], counters[1]]

    pc = 0
    halted = False
    halt_step: int | None = None
    y = float(gate_initial)
    global_substep = 0

    for step in range(machine_steps):
        if not halted:
            instruction = program[pc]
            if instruction.op == "halt":
                halted = True
                halt_step = step
            elif instruction.op == "inc":
                mutable_counters[instruction.register] += 1
                pc = instruction.target
            else:
                if mutable_counters[instruction.register] == 0:
                    pc = instruction.zero_target
                else:
                    mutable_counters[instruction.register] -= 1
                    pc = instruction.target

        for _ in range(substeps_per_machine_step):
            rhs = (y * y - nu * y) if halted else (-nu * y)
            y += dt * rhs
            global_substep += 1
            if not math.isfinite(y):
                if halted:
                    return RunResult(
                        halted=True,
                        halt_step=halt_step,
                        counter_state=tuple(mutable_counters),
                        gate_crossed=True,
                        gate_cross_step=global_substep,
                        final_y=y,
                    )
                raise FloatingPointError("pre-halting decay became non-finite")
            if y < 0:
                raise FloatingPointError("explicit Euler left the non-negative gate domain")
            if y >= threshold:
                return RunResult(
                    halted=halted,
                    halt_step=halt_step,
                    counter_state=tuple(mutable_counters),
                    gate_crossed=True,
                    gate_cross_step=global_substep,
                    final_y=y,
                )

    return RunResult(
        halted=halted,
        halt_step=halt_step,
        counter_state=tuple(mutable_counters),
        gate_crossed=False,
        gate_cross_step=None,
        final_y=y,
    )
