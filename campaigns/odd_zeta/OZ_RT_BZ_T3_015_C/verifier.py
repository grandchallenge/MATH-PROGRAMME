from __future__ import annotations

import sys
from pathlib import Path

# The independent verifier traverses the same deeply nested pinned Q-row AST.
# Raising only the Python recursion ceiling changes no algebraic semantics.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 20000))

_IMPL = Path(__file__).with_name("verifier_impl.py.inc")
exec(compile(_IMPL.read_text(encoding="utf-8"), str(_IMPL), "exec"), globals(), globals())

# Bind the independent governed replay to the protected merge of T3-015-B.
PROTECTED_BASE = "5882e3cd24dff62bf9331ee230274f3acd79f3f2"
