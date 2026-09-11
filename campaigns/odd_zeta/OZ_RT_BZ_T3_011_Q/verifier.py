from pathlib import Path

_IMPL = Path(__file__).with_name("verifier_impl.py.inc")
exec(compile(_IMPL.read_text(encoding="utf-8"), str(_IMPL), "exec"), globals(), globals())
