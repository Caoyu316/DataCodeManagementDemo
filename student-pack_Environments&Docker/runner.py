"""Supplied candidate loader: never imports pipeline or worked as a fallback."""
from pathlib import Path
import hashlib
import types

def candidate(path):
    path = Path(path).resolve()
    print("Candidate:", path)
    source = path.read_bytes()
    print("SHA256:", hashlib.sha256(source).hexdigest())
    module = types.ModuleType("student_candidate")
    module.__file__ = str(path)
    # Compile the same bytes we fingerprinted, never a possibly stale .pyc.
    exec(compile(source, str(path), "exec"), module.__dict__)
    for name in ("extract", "compare"):
        fn = getattr(module, name)
        if not callable(fn) or Path(fn.__code__.co_filename).resolve() != path:
            raise ValueError(name + " must be defined in the selected candidate")
    return module
