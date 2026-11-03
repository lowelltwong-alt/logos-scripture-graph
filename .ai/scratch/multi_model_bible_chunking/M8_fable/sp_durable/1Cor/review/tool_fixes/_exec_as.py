"""Run a tool's source as if it lived at AS_PATH, so its own path-relative inputs resolve there (read-only use).

Used by the 1Cor tool-fix fixtures to test a STAGED copy against the installed tree before install. It writes nothing
itself; the tool's own behaviour decides what it writes (both tools tested here write nothing).
usage: _exec_as.py SOURCE AS_PATH [tool args...]
"""
import sys

sys.dont_write_bytecode = True
src, as_path = sys.argv[1], sys.argv[2]
sys.argv = [as_path] + sys.argv[3:]
with open(src, encoding="utf-8") as fh:
    code = compile(fh.read(), as_path, "exec")
exec(code, {"__name__": "__main__", "__file__": as_path})
