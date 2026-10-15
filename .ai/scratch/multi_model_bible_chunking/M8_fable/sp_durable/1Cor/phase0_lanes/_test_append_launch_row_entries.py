"""Regression test for append_launch_row.py's explicit producer/catcher rule (2026-10-15, E-75 candidate).

Until 2026-10-15 the recorder's PRODUCER and CATCHER tables were empty and a toolkit-port default was written for every
lane, so the D and S launch rows recorded a wrong producer and catcher. The recorder now refuses at load time unless
every lane has an explicit entry in both tables. This test runs the real recorder (it must load) and two broken copies,
each missing one entry (each must refuse). The copies live in a temporary directory and point HERE at the real one.
Writes nothing in SP.

usage: python -B _test_append_launch_row_entries.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REC = HERE / "append_launch_row.py"
SRC = REC.read_text(encoding="utf-8")
ANCHOR = "HERE = Path(__file__).resolve().parent"


def run(text):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "append_launch_row_copy.py"
        p.write_text(text.replace(ANCHOR, "HERE = Path(%r)" % str(HERE), 1), encoding="utf-8")
        return subprocess.run([sys.executable, "-B", str(p), "--help"], capture_output=True, text=True,
                              encoding="utf-8")


def main():
    results = []
    assert SRC.count(ANCHOR) == 1, "the HERE anchor moved; update this test"
    r = run(SRC)
    results.append(("real recorder loads", r.returncode == 0))
    for name, old, new in [("missing catcher refuses", '"C1": _CHECK, "C2": _CHECK}', '"C1": _CHECK}'),
                           ("missing producer refuses", '"C2": "this lane (1 Corinthians strategy check, text first)"}',
                            '}')]:
        assert SRC.count(old) == 1, "anchor for %r not unique; update this test" % name
        r = run(SRC.replace(old, new, 1))
        results.append((name, r.returncode != 0 and "explicit PRODUCER and CATCHER" in r.stderr))
    for n, ok in results:
        print("%s %s" % ("PASS" if ok else "FAIL", n))
    bad = [n for n, ok in results if not ok]
    print("%d/%d %s" % (len(results) - len(bad), len(results), "GREEN" if not bad else "RED"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
