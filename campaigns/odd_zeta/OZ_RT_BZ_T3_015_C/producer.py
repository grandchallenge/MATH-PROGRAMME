from __future__ import annotations

import sys
from pathlib import Path

# The pinned Q-row source is a deeply nested exact AST. Preserve exact semantics
# while allowing the inherited source evaluator to traverse it without hitting
# Python's default recursion ceiling.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 20000))

_IMPL = Path(__file__).with_name("producer_impl.py.inc")
exec(compile(_IMPL.read_text(encoding="utf-8"), str(_IMPL), "exec"), globals(), globals())

# Bind the governed replay to the protected merge of T3-015-B. Functions loaded
# above resolve this global at call time, so the tested implementation bytes stay
# unchanged while the provisional diagnostic marker is replaced by live authority.
PROTECTED_BASE = "5882e3cd24dff62bf9331ee230274f3acd79f3f2"
