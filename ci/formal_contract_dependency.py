#!/usr/bin/env python3
"""Fail-open dependency proof for *existing* non-formal workflow contracts.

Only the precisely enumerated workflow contract scripts can avoid re-running
Lean. All changes to the material router, workflows, toolchain, registry and
unrecognised scripts retain the original full-fanout behavior.
"""
from __future__ import annotations
import ast
import json
import subprocess
from pathlib import Path

# No wildcards: a newly named validator cannot silently inherit an exception.
CONTRACT_FILES = frozenset({
    'ci/validate_workflow_coverage.py',
    'ci/validate_workflow_coverage_v2.py',
    'ci/test_workflow_coverage.py',
    'ci/test_workflow_coverage_v2.py',
    'ci/validate_workflow_semantics.py',
    'ci/test_workflow_semantics.py',
})
CONTRACT_REQUIRED_COMMANDS = frozenset({
    'ci/validate_workflow_coverage_v2.py', 'ci/test_workflow_coverage_v2.py',
    'ci/test_workflow_coverage.py', 'ci/validate_workflow_semantics.py',
    'ci/test_workflow_semantics.py',
})
# One dynamic subprocess replay is pinned by an exact Git blob in the PC-WP04
# manifest. Its validator runs in the other explicit PC-WP04 material lane.
PC_MANIFEST = 'fixtures/formal/PC-WP04/certificate_manifest.json'
KNOWN_PYTHON_SPAWN = frozenset({
    'ci/formal_validation.py', 'ci/validate_pc_wp04_fixture.py',
    'ci/test_pc_wp04_fixture.py', 'ci/formal_contract_dependency.py',
})


class DependencyUnproved(ValueError):
    pass


def _check_policy_contracts(root: Path) -> None:
    manifest = json.loads((root / 'governance/policy_shard_registry.json').read_text())
    commands = {tuple(x) for xs in manifest['shards'].values() for x in xs}
    for path in CONTRACT_REQUIRED_COMMANDS:
        if ('python3', path) not in commands:
            raise DependencyUnproved('governed contract not executable: ' + path)


def _dynamic_pc_target(root: Path) -> str:
    data = json.loads((root / PC_MANIFEST).read_text())
    replay = data['fixture_replay']
    relative = replay['validator']
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file() or target.suffix != '.py':
        raise DependencyUnproved('PC-WP04 dynamic validator path unverified')
    # Pinned manifest is itself a material PC-WP04 path. Even when it remains
    # unchanged, verify its locked validator source and byte identity.
    check = subprocess.run(['git', 'hash-object', str(target)], cwd=root,
                           capture_output=True, text=True, timeout=8)
    if check.returncode or check.stdout.strip() != replay['validator_git_blob']:
        raise DependencyUnproved('PC-WP04 replay source blob mismatch')
    return target.relative_to(root.resolve()).as_posix()


def audited_code_paths(root: Path, registry: dict) -> set[str]:
    module_lookup: dict[str, set[str]] = {}
    for directory in ('ci', 'tests', 'campaigns', 'fixtures'):
        for p in (root / directory).rglob('*.py'):
            if any(part in ('.lake', '.venv', 'node_modules', '__pycache__') for part in p.parts):
                continue
            module_lookup.setdefault(p.stem, set()).add(p.relative_to(root).as_posix())
    initial = {'ci/formal_validation.py', _dynamic_pc_target(root)}
    for lane in registry['lanes']:
        for cmd in lane['validator_commands']:
            if len(cmd) > 1 and cmd[0] in ('python', 'python3'):
                if cmd[1].endswith('.py'):
                    initial.add(cmd[1])
                elif len(cmd) == 4 and cmd[1:3] == ['-m', 'unittest'] and cmd[3].startswith('tests.test_'):
                    initial.add(cmd[3].replace('.', '/') + '.py')
                else:
                    raise DependencyUnproved('unknown Python validator invocation')
            elif cmd:
                raise DependencyUnproved('unrecognised non-Python lane validator')
    stack = list(initial)
    visited = set()
    while stack:
        relative = stack.pop()
        if relative in visited:
            continue
        visited.add(relative)
        source = root / relative
        if not source.is_file() or source.suffix != '.py':
            raise DependencyUnproved('missing Python dependency: ' + relative)
        tree = ast.parse(source.read_text(encoding='utf-8'), filename=relative)
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.Import):
                modules.extend(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.append(node.module)
                modules.extend(node.module + '.' + a.name for a in node.names)
            for module in modules:
                parts = module.split('.')
                for part in parts:
                    if part in {Path(name).stem for name in CONTRACT_FILES}:
                        raise DependencyUnproved('formal validator imports contract code: ' + relative + ':' + part)
                    if part in module_lookup:
                        stack.extend(module_lookup[part])
                if module in ('importlib', 'runpy'):
                    raise DependencyUnproved('dynamic module loader in ' + relative)
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id in ('__import__', 'eval', 'exec'):
                    raise DependencyUnproved('dynamic Python execution in ' + relative)
                if isinstance(func, ast.Attribute) and func.attr in ('import_module', 'run_module', 'run_path'):
                    raise DependencyUnproved('runtime module loading in ' + relative)
                if (isinstance(func, ast.Attribute) and func.attr in ('run', 'check_call', 'check_output', 'Popen')
                        and isinstance(func.value, ast.Name) and func.value.id == 'subprocess'
                        and relative not in KNOWN_PYTHON_SPAWN):
                    raise DependencyUnproved('unreviewed subprocess dependency: ' + relative)
    return visited


def contract_only_safe(root: Path, registry: dict) -> tuple[bool, str]:
    """Unknown identities, path changes or dynamic dependencies require full replay."""
    try:
        _check_policy_contracts(root)
        dependencies = audited_code_paths(root, registry)
        intersection = dependencies & CONTRACT_FILES
        if intersection:
            raise DependencyUnproved('formal validator imports contract code: ' + ','.join(sorted(intersection)))
        return True, 'CONTRACT_CODE_DISJOINT_FROM_FORMAL_EXECUTION'
    except (OSError, ValueError, SyntaxError, KeyError, TypeError, RuntimeError, subprocess.TimeoutExpired) as exc:
        return False, type(exc).__name__ + ':' + str(exc)[:180]
